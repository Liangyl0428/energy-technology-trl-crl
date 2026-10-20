"""Front-end exports must preserve real scores, nulls and topic identity."""
import json
from pathlib import Path
import pandas as pd
import pytest
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from trl_crl.delivery import typed_units, sync_topic_metadata, write_case_table


def results(trl=4,crl=None,gates=None):
    return {'assessment_units':[{'case_id':'C1','category_id':'OLD','category_name':'old name',
            'category_ids':['OLD','OLDER'],'trl_public_evidence_stage':trl,'crl_public_evidence_stage':crl,
            'remaining_gaps':['缺少重复商业履约和经济性证据']}],
            'assessments':[{'case_id':'C1','gates':gates or []}]}


def test_integer_null_and_display_are_separate(tmp_path):
    f=typed_units(results())
    assert f.trl_public_evidence_stage.iloc[0]==4 and pd.isna(f.crl_public_evidence_stage.iloc[0])
    assert f.trl_evidence_status.iloc[0]=='supported' and f.crl_evidence_status.iloc[0]=='unknown'
    assert f.trl_display.iloc[0]=='TRL4｜实验环境验证'
    assert '商业' in f.crl_missing_evidence.iloc[0]
    p=tmp_path/'cases.csv';write_case_table(f,p)
    restored=pd.read_csv(p,dtype={'trl_public_evidence_stage':'Int64','crl_public_evidence_stage':'Int64'})
    assert restored.crl_public_evidence_stage.isna().sum()==1
    record=json.loads(p.with_suffix('.json').read_text())[0]
    assert type(record['trl_public_evidence_stage']) is int and record['crl_public_evidence_stage'] is None
    assert restored.dropna(subset=['trl_public_evidence_stage','crl_public_evidence_stage']).empty


def test_conflict_does_not_invent_or_erase_a_supported_stage():
    gates=[{'axis':'TRL','effective_status':'conflict'}]
    unknown=typed_units(results(trl=None,gates=gates))
    assert unknown.trl_evidence_status.iloc[0]=='conflict' and pd.isna(unknown.trl_public_evidence_stage.iloc[0])
    supported=typed_units(results(trl=4,gates=gates))
    assert supported.trl_evidence_status.iloc[0]=='supported' and supported.trl_has_conflict.iloc[0]
    assert supported.trl_public_evidence_stage.iloc[0]==4


@pytest.mark.parametrize('bad',['TRL4','证据不足',4.5,True,0,10])
def test_invalid_levels_fail_instead_of_coercing_to_unknown(bad):
    with pytest.raises(ValueError,match='Invalid TRL'):typed_units(results(trl=bad))


def test_current_names_and_history_are_idempotent():
    f=typed_units(results());f['legacy_category_id']=f.category_id;f['category_id']='F0001'
    catalog=pd.DataFrame({'category_id':['F0001'],'name':['Current topic']})
    f=sync_topic_metadata(f,catalog)
    assert f.category_name.iloc[0]=='Current topic' and f.legacy_category_name.iloc[0]=='old name'
    assert f.legacy_category_ids.iloc[0]==['OLD','OLDER'] and json.loads(f.category_ids.iloc[0])==['F0001']
    twice=sync_topic_metadata(f,catalog)
    pd.testing.assert_frame_equal(f,twice)
    with pytest.raises(ValueError,match='Unknown'):sync_topic_metadata(f,catalog.assign(category_id='F0002'))
    with pytest.raises(ValueError,match='unique'):sync_topic_metadata(f,pd.concat([catalog,catalog]))


def test_actual_export_matches_engine_and_supports_numeric_filtering():
    from trl_crl.pipeline import assess
    repo=Path(__file__).resolve().parents[1]
    _,r=assess(repo/'data');expected=typed_units(r).set_index('case_id')
    d=pd.read_csv(repo/'assets/full_nmf500/case_hotspot_links.csv',dtype={'trl_public_evidence_stage':'Int64','crl_public_evidence_stage':'Int64'}).set_index('case_id')
    for field in ['trl_public_evidence_stage','crl_public_evidence_stage']:
        pd.testing.assert_series_equal(d[field].sort_index(),expected[field].sort_index(),check_names=False)
    assert len(d[d.trl_public_evidence_stage.isna()])==14
    assert len(d[d.crl_public_evidence_stage.isna()])==99
    assert len(d.dropna(subset=['trl_public_evidence_stage','crl_public_evidence_stage']))==13
    assert (d.trl_public_evidence_stage.dropna().between(1,9)).all()
    assert (d.crl_public_evidence_stage.dropna().between(1,5)).all()
