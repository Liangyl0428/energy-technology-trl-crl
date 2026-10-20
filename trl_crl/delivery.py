"""Typed maturity export and version-consistent topic metadata, without regrading."""
import json
from pathlib import Path
import pandas as pd
from .rules import NAMES, VERSION

GAP_WORDS = {
    'TRL': ('测试','试验','验证','验收','调试','指标','性能','可靠性','成熟度','型式','实测','对照','达标','TRL'),
    'CRL': ('商业','履约','供货','许可','销售','交易','市场','经济','收入','签约','买方','结算','CRL'),
}


def typed_units(results):
    """Add axis statuses/display fields derived from the unchanged engine output."""
    assessments = {r['case_id']:r for r in results.get('assessments', [])}
    rows = []
    for unit in results['assessment_units']:
        row = dict(unit)
        for axis in ['TRL','CRL']:
            prefix = axis.lower(); field = prefix+'_public_evidence_stage'
            level = unit.get(field)
            if level is not None and (type(level) is not int or not 1 <= level <= len(NAMES[axis])):
                raise ValueError(f'Invalid {axis} stage for {unit["case_id"]}: {level!r}')
            gates = [g for g in assessments.get(unit['case_id'], {}).get('gates', []) if g['axis']==axis]
            conflict = any(g['effective_status']=='conflict' for g in gates)
            state = 'supported' if level is not None else 'conflict' if conflict else 'unknown'
            gaps = unit.get('remaining_gaps') or []
            relevant = [g for g in gaps if any(k in g for k in GAP_WORDS[axis])]
            missing = '；'.join(relevant or (gaps if level is None else []))
            if level is None and not missing:
                missing = '现有公开证据不足以支持该轴等级；需按项目量表补充同对象证据。'
            label = NAMES[axis][level-1] if level is not None else '证据冲突' if conflict else '证据不足'
            row.update({field:level, prefix+'_evidence_status':state, prefix+'_has_conflict':conflict,
                        prefix+'_stage_name':NAMES[axis][level-1] if level is not None else None,
                        prefix+'_missing_evidence':missing,
                        prefix+'_explanation':f'{label}；仅适用于该对象配置、场景与证据期间，属于公开证据初评。',
                        prefix+'_display':f'{axis}{level}｜{label}' if level is not None else f'{axis}未知｜{label}'})
        row['paired_axes_usable'] = all(row[a+'_public_evidence_stage'] is not None for a in ['trl','crl'])
        row['maturity_rules_version'] = VERSION
        rows.append(row)
    frame = pd.DataFrame(rows)
    for a in ['trl','crl']:
        frame[a+'_public_evidence_stage'] = frame[a+'_public_evidence_stage'].astype('Int64')
    return frame


def sync_topic_metadata(frame, catalog):
    """Treat the current topic table as the sole source of current IDs/names."""
    frame = frame.copy()
    if not catalog.category_id.is_unique or catalog.category_id.isna().any() or catalog.name.isna().any() or catalog.name.astype(str).str.strip().eq('').any():
        raise ValueError('Topic catalog must have unique IDs and nonempty names')
    names = catalog.set_index('category_id')['name']
    if frame.category_id.isna().any() or not set(frame.category_id) <= set(names.index):
        raise ValueError('Unknown or missing current category_id')
    if 'legacy_category_name' not in frame:
        frame['legacy_category_name'] = frame.get('category_name', '')
    if 'category_ids' in frame and 'legacy_category_ids' not in frame:
        frame['legacy_category_ids'] = frame['category_ids']
    frame['category_name'] = frame.category_id.map(names)
    frame['category_ids'] = frame.category_id.map(lambda cid:json.dumps([cid],ensure_ascii=False))
    frame['taxonomy_version'] = 'full_nmf500_20260926'
    return frame


def case_schema():
    properties={'case_id':{'type':'string'},'category_id':{'type':'string','pattern':'^F[0-9]{4}$'},'category_name':{'type':'string'},'category_ids':{'type':'array','items':{'type':'string'}},'paired_axes_usable':{'type':'boolean'}}
    for axis,maximum in [('trl',9),('crl',5)]:
        properties[axis+'_public_evidence_stage']={'type':['integer','null'],'minimum':1,'maximum':maximum}
        properties[axis+'_evidence_status']={'enum':['supported','unknown','conflict']}
        properties[axis+'_has_conflict']={'type':'boolean'}
        properties[axis+'_stage_name']={'type':['string','null']}
        for suffix in ['missing_evidence','explanation','display']:properties[axis+'_'+suffix]={'type':'string'}
    return {'$schema':'https://json-schema.org/draft/2020-12/schema','title':'P0 bounded maturity case export','type':'array','items':{'type':'object','required':['case_id','category_id','category_name','trl_public_evidence_stage','crl_public_evidence_stage','trl_evidence_status','crl_evidence_status','paired_axes_usable'],'properties':properties},'description':'JSON integer/null contract. CSV uses empty cells for null and JSON text for category_ids. Evidence preassessment only; source rules remain unchanged.'}


def write_case_table(frame, path):
    """CSV keeps nullable integer cells; JSON preserves native integer/null types."""
    path = Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    for a in ['trl','crl']:
        frame[a+'_public_evidence_stage'] = frame[a+'_public_evidence_stage'].astype('Int64')
    tmp = path.with_suffix('.csv.tmp')
    frame.to_csv(tmp,index=False,encoding='utf-8-sig'); tmp.replace(path)
    # pandas converts nullable Int64 to native JSON integers and missing cells to null.
    records = json.loads(frame.to_json(orient='records',force_ascii=False))
    for row in records:
        if isinstance(row.get('category_ids'),str):row['category_ids']=json.loads(row['category_ids'])
    path.with_suffix('.json').write_text(json.dumps(records,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    path.with_suffix('.schema.json').write_text(json.dumps(case_schema(),ensure_ascii=False,indent=2)+'\n')


def refresh_export(data_dir, source_csv, catalog_csv, out_csv):
    from .pipeline import assess
    _, results = assess(data_dir)
    current = typed_units(results).set_index('case_id')
    source = pd.read_csv(source_csv,encoding='utf-8-sig')
    if not source.case_id.is_unique or set(source.case_id)!=set(current.index):
        raise ValueError('Case export must contain every current bounded object exactly once')
    fields = [c for c in current if c.startswith(('trl_','crl_')) or c in ['paired_axes_usable','maturity_rules_version','remaining_gaps']]
    for field in fields:
        source[field] = source.case_id.map(current[field])
    source = sync_topic_metadata(source,pd.read_csv(catalog_csv))
    write_case_table(source,out_csv)
    return source,results['SUMMARY']
