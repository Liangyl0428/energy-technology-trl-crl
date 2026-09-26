"""Attach NMF500 retrieval associations and recompute the existing evidence gates."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import sys

import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(ROOT / 'energy-topic-hotspots/pipelines/nmf500'))
from trl_crl.pipeline import INPUT_NAMES, write_outputs
from trl_crl.common import read, write, file_sha, canonical_sha
from build import safe_excel
from mapping import ranked_links

NMF = ROOT / 'energy-topic-identification/pipelines/keyword_nmf/results'
HOT = ROOT / 'energy-topic-hotspots/outputs/nmf500_v021'


def build(work, output):
    context = work / 'context'
    rows = read(context / 'contexts.json')
    audit = read(context / 'ENCODING.json')
    signature = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    if audit['input_sha256'] != signature:
        raise ValueError('Context signature mismatch')
    embeddings = np.load(context / 'embeddings.npy')
    catalog = pd.read_csv(HOT / 'topic_catalog.csv')
    centroids = np.load(HOT / 'topic_centroids.npy')
    links = ranked_links(rows, embeddings, centroids, catalog)
    data = {n: read(REPO / 'data' / f'{n}.json') for n in INPUT_NAMES}
    original_manifest = {n: file_sha(REPO / 'data' / f'{n}.json') for n in INPUT_NAMES}
    cases = links[links.entity_type.eq('case') & links['rank'].eq(1)].set_index('entity_id')
    directions = links[links.entity_type.eq('direction') & links['rank'].eq(1)].set_index('entity_id')
    # Remapping preserves the current audited IDs, scopes, profiles and evidence.
    # New category fields are retrieval associations, not amendments to evidence scope.
    for obj in data['objects']:
        cid = obj['case_id']
        obj['legacy_category_id'] = obj.get('category_id')
        obj['legacy_category_name'] = obj.get('category_name')
        obj['category_id'] = cases.loc[cid, 'category_id']
        obj['category_name'] = cases.loc[cid, 'category_name']
        obj['category_mapping_status'] = 'automatic_candidate_needs_semantic_review'
    for link in data['case_technology_links']:
        link['legacy_category_id'] = link.get('category_id')
        link['category_id'] = cases.loc[link['case_id'], 'category_id']
        link['theme_mapping_status'] = 'automatic_candidate_needs_semantic_review'
    data['theme_direction_links'] = [dict(link_id='NMF500-' + tid, category_id=r.category_id, technology_id=tid, relation='retrieval_candidate_direction_in_theme', mapping_status='automatic_candidate_needs_semantic_review', basis='BGE-M3 direction context cosine to NMF paper centroid; pending semantic verification', cosine=float(r.cosine), relabels_documents=False, transfers_maturity=False) for tid, r in directions.iterrows()]
    transfer = pd.read_parquet(HOT / 'patent_policy_assignments.parquet')
    counts = transfer.groupby(['topic_1_id', 'source']).size().unstack(fill_value=0)
    themes = []
    for r in catalog.itertuples():
        children = directions[directions.category_id.eq(r.category_id)]
        npat = int(counts.patent.get(r.topic_id, 0))
        npol = int(counts.policy.get(r.topic_id, 0))
        themes.append({'category_id': r.category_id, 'category_name': r.name, 'documents': int(r.uniform_assigned_papers) + npat + npol, 'paper_documents': int(r.uniform_assigned_papers), 'patent_documents': npat, 'policy_documents': npol, 'candidate_direction_ids': children.index.tolist(), 'candidate_direction_names': children.entity_name.tolist(), 'processing_status': 'automatic_candidate_mapping_needs_review', 'processing_reason': '新NMF主题；方向与案例余弦关联待核读，证据等级仅属于原有有界对象', 'formal_trl': None, 'formal_crl': None})
    data['themes'] = themes
    hot_summary = read(HOT / 'SUMMARY.json')
    data['dataset'].update(classification_themes=500, candidate_directions=len(directions), total_source_records=hot_summary['input_papers'] + len(transfer), assigned_records=hot_summary['eligible_papers'] + len(transfer), unassigned_or_quarantined_records=hot_summary['input_papers']-hot_summary['eligible_papers'], source_document_distribution_note='NMF500 frozen-sample theme counts; papers use fixed-H L2 contribution labels, patents/policies use paper-centroid cosine; dates and confidence audited separately.', new_evidence_search_performed=False, taxonomy_run='nmf500-sample-v0.2.1', evidence_refresh_note='Existing accepted evidence re-evaluated independently; evidence cutoff remains 2026-09-25; theme mapping alone does not upgrade either axis')
    inputs = work / 'inputs'
    inputs.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    overlay_names = {'dataset', 'objects', 'case_technology_links', 'themes', 'theme_direction_links'}
    for name, values in data.items():
        if name in overlay_names:
            write(inputs / f'{name}.json', values)
        else:
            # Preserve the evidence bytes too, so portable replay has the same
            # input hashes rather than merely equivalent JSON serialization.
            shutil.copy2(REPO / 'data' / f'{name}.json', inputs / f'{name}.json')
    links.to_csv(output / 'theme_context_top3.csv', index=False, encoding='utf-8-sig')
    summary = write_outputs(inputs, output)
    units = pd.DataFrame(read(output / 'assessment_units.json'))
    units['topic_id'] = units.case_id.map(cases.topic_id)
    units['mapping_cosine'] = units.case_id.map(cases.cosine)
    units['mapping_margin'] = units.case_id.map(cases.top1_top2_margin)
    units['mapping_needs_review'] = True
    hotspot_file = 'reviewed_hotspot_metrics.csv' if (HOT / 'reviewed_hotspot_metrics.csv').exists() else 'hotspot_metrics.csv'
    potential_file = 'reviewed_potential_metrics.csv' if (HOT / 'reviewed_potential_metrics.csv').exists() else 'potential_metrics.csv'
    hotspots = pd.read_csv(HOT / hotspot_file).set_index('category_id')
    potential = pd.read_csv(HOT / potential_file).set_index('category_id')
    for name in ['core_numeric_candidate', 'core_robust_candidate', 'emerging_numeric_candidate', 'emerging_robust_candidate', 'core_score', 'emerging_score']:
        units[name] = units.category_id.map(hotspots[name])
    units['potential_numeric_candidate'] = units.category_id.map(potential.potential_numeric_candidate)
    for name in ['core_followup', 'emerging_followup', 'potential_followup', 'review_display_name', 'scope_review_status']:
        if name in hotspots:
            units[name] = units.category_id.map(hotspots[name])
    units.to_csv(output / 'case_hotspot_links.csv', index=False, encoding='utf-8-sig')
    profiles = []
    for r in catalog.itertuples():
        own = units[units.category_id.eq(r.category_id)]
        def distribution(field):
            return dict(Counter(str(int(v)) if pd.notna(v) else 'unknown' for v in own[field]))
        profile = {'category_id': r.category_id, 'name': r.name, 'core_numeric_candidate': bool(hotspots.loc[r.category_id, 'core_numeric_candidate']), 'emerging_numeric_candidate': bool(hotspots.loc[r.category_id, 'emerging_numeric_candidate']), 'potential_numeric_candidate': bool(potential.loc[r.category_id, 'potential_numeric_candidate']), 'candidate_case_count': len(own), 'candidate_case_ids': own.case_id.tolist(), 'candidate_trl_distribution': distribution('trl_public_evidence_stage'), 'candidate_crl_distribution': distribution('crl_public_evidence_stage'), 'candidate_same_case_pairs': [{'case_id': a.case_id, 'TRL': int(a.trl_public_evidence_stage), 'CRL': int(a.crl_public_evidence_stage)} for a in own[own.paired_axes_usable].itertuples()], 'theme_trl': None, 'theme_crl': None, 'mapping_review_required': True, 'interpretation': '候选关联案例的证据分布；关联未经语义确认，不能视为主题统一TRL/CRL'}
        for name in ['core_followup', 'emerging_followup', 'potential_followup']:
            profile[name] = bool(hotspots.loc[r.category_id, name]) if name in hotspots else False
        profile['review_display_name'] = hotspots.loc[r.category_id, 'review_display_name'] if 'review_display_name' in hotspots else r.name
        profiles.append(profile)
    write(output / 'theme_evidence_profiles.json', profiles)
    profile_frame = pd.DataFrame(profiles)
    csv_profile = profile_frame.copy()
    for col in ['candidate_case_ids', 'candidate_trl_distribution', 'candidate_crl_distribution', 'candidate_same_case_pairs']:
        csv_profile[col] = csv_profile[col].map(lambda v: json.dumps(v, ensure_ascii=False))
    csv_profile.to_csv(output / 'theme_evidence_profiles.csv', index=False, encoding='utf-8-sig')
    # Recompute original cases too: a new taxonomy must not change evidence-stage results.
    from trl_crl.pipeline import assess
    old_units = pd.DataFrame(assess(REPO / 'data')[1]['assessment_units']).set_index('case_id')
    comparison = units.set_index('case_id')[['trl_public_evidence_stage', 'crl_public_evidence_stage']].join(old_units[['trl_public_evidence_stage', 'crl_public_evidence_stage']], rsuffix='_original')
    changed = {}
    for axis in ['trl', 'crl']:
        col = f'{axis}_public_evidence_stage'
        changed[axis] = int((comparison[col].fillna(-1) != comparison[col+'_original'].fillna(-1)).sum())
    if any(changed.values()):
        raise ValueError('Taxonomy change unexpectedly changed evidence stages')
    comparison.reset_index().to_csv(output / 'axis_recalculation_check.csv', index=False, encoding='utf-8-sig')
    coverage = {'theme_count': 500, 'bounded_cases_recomputed': len(units), 'directions_remapped': len(directions), 'themes_with_top1_candidate_cases': int(profile_frame.candidate_case_count.gt(0).sum()), 'themes_without_top1_candidate_cases': int(profile_frame.candidate_case_count.eq(0).sum()), 'all_new_mapping_links_require_review': True, 'new_external_sources_added': 0, 'stage_changes_after_taxonomy_switch': changed, 'source_evidence_cutoff': data['dataset']['assessment_cutoff'], 'hotspot_cutoff': hot_summary['cutoff']}
    write(output / 'MAPPING_SUMMARY.json', coverage)
    write(output / 'PROVENANCE.json', {'original_input_hashes': original_manifest, 'selected_nmf_sha256': file_sha(NMF/'selected_nmf.joblib'), 'centroids_sha256': file_sha(HOT/'topic_centroids.npy'), 'context_encoding': audit, 'hotspot_input_hashes': {p: file_sha(HOT/p) for p in ['topic_catalog.csv', hotspot_file, potential_file]}})
    safe_excel({'统计与范围': pd.DataFrame([{'item': k, 'value': v} for k, v in {**summary, **coverage}.items()]), '500主题证据分布': profile_frame, '技术对象与热点': units, '主题关联Top3': links, '原文来源': pd.DataFrame(data['sources']), '逐项证据引文': pd.DataFrame(data['evidence']), '同对象双轴': pd.DataFrame(read(output/'same_case_coordinates.json')), '缺项': pd.DataFrame(read(output/'evidence_gaps.json'))}, output/'500主题热点与TRL_CRL.xlsx')
    report = output / '评估报告.md'
    with report.open('a') as f:
        f.write(f'''\n## NMF500重算范围\n\n500主题目录已接入；391个已有技术方向和122个有界对象重新建立同空间BGE-M3候选关联，保存Top3、余弦和间隔。500主题中有{coverage['themes_with_top1_candidate_cases']}个获得Top1候选案例关联，其余{coverage['themes_without_top1_candidate_cases']}个尚无此类案例覆盖。关联需要语义确认，主题级TRL/CRL均留空。\n\n全部122个对象从原始判据、观测和引文重新计算，TRL有值{summary['objects_with_trl']}，CRL有值{summary['objects_with_crl']}，同对象两轴有值{summary['objects_with_both']}，两轴均未知{summary['objects_with_neither']}。v0.2.1已撤回W011缺乏运行结果与用户反馈支持的两轴；其余判定不因主题变化而改变。此次未增加外部证据，不能据主题变更宣称成熟度升级。证据截止2026-09-25，热点趋势截止2026-06-30；二者时间含义分别记录。\n\n联合查看500主题热点与TRL_CRL.xlsx中的“技术对象与热点”和“500主题证据分布”。样本规模约16.6万条，不是原约512万条全量重分类。\n''')
    print(json.dumps({**summary, **coverage}, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, default=REPO / 'work/nmf500')
    p.add_argument('--output', type=Path, default=REPO / 'results/nmf500')
    args = p.parse_args()
    with threadpool_limits(2):
        build(args.work, args.output)
