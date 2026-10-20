"""Refresh typed maturity fields; never put explanation text in a level column."""
from pathlib import Path
import argparse
import json
import sys
REPO=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO))
from trl_crl.delivery import refresh_export


def build(data_dir,source_csv,out_csv,catalog_csv=None):
    catalog_csv=catalog_csv or REPO.parent/'energy-topic-identification/assets/full_nmf500/topic_catalog.csv'
    frame,_=refresh_export(data_dir,source_csv,catalog_csv,out_csv)
    return len(frame),int(frame.trl_public_evidence_stage.isna().sum()),int(frame.crl_public_evidence_stage.isna().sum())


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--data',type=Path,default=REPO/'data')
    p.add_argument('--source',type=Path,default=REPO/'assets/full_nmf500/case_hotspot_links.csv')
    p.add_argument('--out',type=Path,default=REPO/'assets/full_nmf500/case_hotspot_links.csv')
    p.add_argument('--catalog',type=Path,default=REPO.parent/'energy-topic-identification/assets/full_nmf500/topic_catalog.csv')
    a=p.parse_args();n,t,c=build(a.data,a.source,a.out,a.catalog)
    print(json.dumps({'rows':n,'trl_unknown':t,'crl_unknown':c,'level_type':'integer_or_null','explanations_in_separate_fields':True},ensure_ascii=False))
