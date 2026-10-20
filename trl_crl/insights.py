"""Object-scoped decisions and gate-level traceability; never regrade here."""
from collections import Counter
from .pipeline import assess
from .delivery import typed_units
from .rules import NAMES, VERSION as RULES_VERSION, requirements
from p1_common import VERSION, TAXONOMY, read, table, write, sha

TRL_ACTIONS = {
    1: '明确应用对象、场景和功能，再决定是否开展概念验证。',
    2: '补齐技术路线、设计方案和关键功能的理论验证。',
    3: '安排关键功能的实验室或离线验证，并预先定义验收指标。',
    4: '围绕目标工况开展部件集成与模拟环境测试，事先确定性能要求。',
    5: '明确原型尺度与关键使用条件，准备系统级原型验证。',
    6: '评估示范或工程测试条件，核对型号、典型环境及验收指标。',
    7: '准备系统级产品试运行，完成测试清单和问题闭环。',
    8: '补充实际工程成功应用、性能达成与推广条件证据。',
    9: '针对甲方场景核查适配性、可靠性、运维及成本，不能仅凭已有工程应用直接采购。',
}
CRL_ACTIONS = {
    1: '明确目标客户及需求，开展可记录的用户试用或商业模式验证。',
    2: '核查目标客户、实际合同与交付结算；市场探索尚不足以证明商业履约。',
    3: '补齐重复交付、供应和运维能力及持续商业经济性证据。',
    4: '核查细分市场分母、市场地位和持续经营能力。',
    5: '持续核查适用细分市场、经营期间与竞争能力是否变化。',
}


def joint_interpretation(trl, crl):
    if trl is None and crl is None:
        return '两轴证据均不足；先收集同配置、同场景与适用期间的技术和商业材料。'
    if trl is None:
        return '已有商业轴线索，技术轴未知；商业活动不能替代技术测试证据。'
    if crl is None:
        return '技术轴已有公开证据支持，商业轴未知；不能据此认定无商业活动或可以商业推广。'
    if trl <= 3 and crl >= 4:
        return '技术证据停留在理论或更早阶段而商业证据较高；优先核对两轴是否属于同一配置、场景与时期，并补齐技术证据。'
    if trl >= 7 and crl <= 2:
        return '工程应用方面已有证据，但商业证据仅支持探索或更早阶段；优先核查实际履约与经济性。'
    if trl >= 7 and crl == 3:
        return '工程与早期商业履约均有证据；能否复制推广仍需重复交付、运维能力与持续经济性核查。'
    return '两轴分别反映技术验证与商业活动；按下一阶段门槛安排验证和补证，不能合成为主题成熟度。'


def build(repo, topic_cards):
    base = repo / 'assets/full_nmf500'; dest = base / 'p1'
    data, result = assess(repo / 'data')
    cases = read(base / 'case_hotspot_links.json')
    computed = {r['case_id']: r for r in result['assessment_units']}
    observations = {o['observation_id']: o for o in data['observations']}
    assessments = {r['case_id']: r for r in result['assessments']}
    evidence = {e['evidence_id']: e for e in data['evidence']}
    typed = {r['case_id']: r for r in typed_units(result).to_dict('records')}
    rows, gates = [], []
    for case in cases:
        cid = case['case_id']; unit = computed[cid]; source = typed[cid]
        for axis in ['trl', 'crl']:
            if case[axis + '_public_evidence_stage'] != unit[axis + '_public_evidence_stage']:
                raise ValueError('P1 cannot use stale P0 grades')
        refs = sorted(e['evidence_id'] for e in data['evidence'] if e['case_id'] == cid)
        row = {**case, 'insight_id': 'MI-' + cid, 'business_version': VERSION,
               'joint_interpretation': joint_interpretation(unit['trl_public_evidence_stage'], unit['crl_public_evidence_stage']),
               'case_specific_gaps': unit['remaining_gaps'], 'evidence_ids': refs,
               'evidence_links': [{'evidence_id': eid, 'source_id': evidence[eid]['source_id'],
                                   'url': evidence[eid]['source_url'], 'quote_sha256': evidence[eid]['quote_sha256']} for eid in refs],
               'association_review_status': 'candidate_mapping_pending_review',
               'generation_method': 'deterministic_gate_template_v1', 'model': None, 'prompt_version': None,
               'limitations': ['公开证据初评，未完成独立专家正式评定。',
                              '证据期间与评估截止日分开；不代表今天的产品状态。',
                              '主题关联为相似度候选，对象等级不能转移给关联主题。']}
        for axis, actions in [('TRL', TRL_ACTIONS), ('CRL', CRL_ACTIONS)]:
            prefix = axis.lower(); level = unit[prefix + '_public_evidence_stage']
            target = level + 1 if level is not None and level < len(NAMES[axis]) else None
            own = [g for g in assessments[cid]['gates'] if g['axis'] == axis]
            missing = [g for g in own if g['effective_status'] != 'met' and
                       (target is None and level is None or g['level'] == target)]
            row[prefix + '_next_stage_to_investigate'] = target
            row[prefix + '_next_actions'] = [actions[level] if level is not None else
                ('先取得同对象的设计、测试条件和已完成验证结果，确定可支持的阶段。' if axis == 'TRL' else
                 '先核查同对象的客户、试用、合同和履约期间；缺少材料不能判为 CRL1。'),
                '结合对象配置、用途和边界制定专属细则，并安排独立领域审核。']
            row[prefix + '_evidence_gap_requirements'] = [
                {'gate_id': f'{cid}:{axis}:{g["level"]}:{g["key"]}',
                 'level': g['level'], 'requirement': g['requirement'],
                 'status': g['effective_status'], 'meaning': '当前未获证据支持或尚未核实，不等同于实际性能未达标'}
                for g in missing]
            row[prefix + '_supported_gate_ids'] = [f'{cid}:{axis}:{g["level"]}:{g["key"]}'
                for g in own if level == g['level'] and g['effective_status'] == 'met']
            row[prefix + '_explanation'] = source[prefix + '_explanation']
            for g in own:
                obs_ids = g['observation_ids']
                if any(observations[i]['case_id'] != cid for i in obs_ids):
                    raise ValueError('Cross-object gate evidence')
                gates.append({**g, 'gate_id': f'{cid}:{axis}:{g["level"]}:{g["key"]}',
                              'evidence_ids': sorted({observations[i]['evidence_id'] for i in obs_ids}),
                              'maturity_rules_version': RULES_VERSION})
        rows.append(row)
    distributions = []
    for card in topic_cards:
        cid = card['category_id']; own = [r for r in rows if r['category_id'] == cid]
        dist = lambda a: dict(Counter(str(r[a + '_public_evidence_stage']) if r[a + '_public_evidence_stage'] is not None else 'unknown' for r in own))
        distributions.append({'category_id': cid, 'case_count': len(own), 'case_ids': [r['case_id'] for r in own],
                              'trl_distribution': dist('trl'), 'crl_distribution': dist('crl'),
                              'paired_case_ids': [r['case_id'] for r in own if r['paired_axes_usable']],
                              'theme_trl': None, 'theme_crl': None,
                              'mapping_scope': 'current_primary_candidate_only',
                              'review_status': 'candidate_mapping_pending_review',
                              'interpretation': '候选关联对象的证据分布；样本非行业普查，不能按最大值或均值给主题评级。' if own else '当前没有候选关联对象；不表示该方向没有成熟产品。',
                              'taxonomy_version': TAXONOMY, 'business_version': VERSION})
    for name, records in [('case_insights', rows), ('gate_evidence', gates),
                          ('topic_case_distributions', distributions), ('evidence_index', data['evidence']),
                          ('observation_index', data['observations']), ('source_index', data['sources'])]:
        table(dest / name, records)
    write(dest / 'INPUTS.json', {'version': VERSION, 'files': {
        str(p.relative_to(repo)): sha(p) for p in [base / 'case_hotspot_links.json', *sorted((repo / 'data').glob('*.json'))]}})
    return rows, distributions
