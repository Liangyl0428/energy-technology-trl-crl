# 全量主题关联下的 TRL/CRL 灵敏度与证据消融

{
  "cases": 122,
  "sources": 114,
  "passages": 126,
  "observations": 453,
  "scenario_count": 724,
  "source_loo_cases_with_any_axis_changed": 118,
  "source_loo_fragile_known_trl": 108,
  "source_loo_fragile_known_crl": 23,
  "upgrades": 0,
  "cross_axis_ablation_independence_passed": true,
  "frozen_evidence_only": true,
  "new_remote_evidence_added": 0,
  "limitation": "Conservative withdrawal: any removed citation resets the gate to unknown; remaining support is not semantically re-adjudicated. Not an accuracy experiment.",
  "time_limit": "All 126 available_by values are 2026-09-25. Earlier knowledge-date tests return unknown; they cannot reconstruct historical maturity.",
  "mapping_limit": "Top3 expands candidate coverage only. No cosine threshold certifies semantic correctness or transfers grades."
}

## 留一实验

|                            |   ('changed_cases', 'min') |   ('changed_cases', 'mean') |   ('changed_cases', 'max') |   ('unchanged_fraction', 'min') |   ('unchanged_fraction', 'mean') |   ('unchanged_fraction', 'max') |   ('known_to_unknown', 'min') |   ('known_to_unknown', 'mean') |   ('known_to_unknown', 'max') |
|:---------------------------|---------------------------:|----------------------------:|---------------------------:|--------------------------------:|---------------------------------:|--------------------------------:|------------------------------:|-------------------------------:|------------------------------:|
| ('observation_loo', 'CRL') |                          0 |                    0.152318 |                          1 |                        0.991803 |                         0.998751 |                               1 |                             0 |                       0.152318 |                             1 |
| ('observation_loo', 'TRL') |                          0 |                    0.701987 |                          1 |                        0.991803 |                         0.994246 |                               1 |                             0 |                       0.701987 |                             1 |
| ('passage_loo', 'CRL')     |                          0 |                    0.18254  |                          1 |                        0.991803 |                         0.998504 |                               1 |                             0 |                       0.18254  |                             1 |
| ('passage_loo', 'TRL')     |                          0 |                    0.873016 |                          1 |                        0.991803 |                         0.992844 |                               1 |                             0 |                       0.873016 |                             1 |
| ('source_loo', 'CRL')      |                          0 |                    0.201754 |                         10 |                        0.918033 |                         0.998346 |                               1 |                             0 |                       0.201754 |                            10 |
| ('source_loo', 'TRL')      |                          0 |                    0.947368 |                          8 |                        0.934426 |                         0.992235 |                               1 |                             0 |                       0.947368 |                             8 |

整体平均保持率会被每次未受影响的对象抬高，应重点读取 case_fragility.csv 中各对象自身证据脆弱性。未知不是 0 级，等级降幅只对消融后仍有等级者计算。

## 来源类型与时间

| kind                 | scenario                          | axis   |   removed_evidence |   removed_observations |   changed_cases |   unchanged_fraction |   known_cases |   unknown_fraction |   known_to_unknown | mean_drop_among_still_known   |   upgrades |
|:---------------------|:----------------------------------|:-------|-------------------:|-----------------------:|----------------:|---------------------:|--------------:|-------------------:|-------------------:|:------------------------------|-----------:|
| source_type_ablation | government_case_compilation       | TRL    |                 10 |                     62 |               8 |             0.934426 |           100 |           0.180328 |                  8 |                               |          0 |
| source_type_ablation | government_case_compilation       | CRL    |                 10 |                     62 |              10 |             0.918033 |            13 |           0.893443 |                 10 |                               |          0 |
| source_type_ablation | paper                             | TRL    |                 97 |                    322 |              90 |             0.262295 |            18 |           0.852459 |                 90 |                               |          0 |
| source_type_ablation | paper                             | CRL    |                 97 |                    322 |               3 |             0.97541  |            20 |           0.836066 |                  3 |                               |          0 |
| source_type_ablation | patent                            | TRL    |                  4 |                      4 |               4 |             0.967213 |           104 |           0.147541 |                  4 |                               |          0 |
| source_type_ablation | patent                            | CRL    |                  4 |                      4 |               0 |             1        |            23 |           0.811475 |                  0 |                               |          0 |
| source_type_ablation | policy                            | TRL    |                  3 |                     19 |               1 |             0.991803 |           107 |           0.122951 |                  1 |                               |          0 |
| source_type_ablation | policy                            | CRL    |                  3 |                     19 |               3 |             0.97541  |            20 |           0.836066 |                  3 |                               |          0 |
| source_type_ablation | public_project_or_research_source | TRL    |                 12 |                     46 |               5 |             0.959016 |           103 |           0.155738 |                  5 |                               |          0 |
| source_type_ablation | public_project_or_research_source | CRL    |                 12 |                     46 |               7 |             0.942623 |            16 |           0.868852 |                  7 |                               |          0 |
| source_type_ablation | public_research_source            | TRL    |                  0 |                      0 |               0 |             1        |           108 |           0.114754 |                  0 |                               |          0 |
| source_type_ablation | public_research_source            | CRL    |                  0 |                      0 |               0 |             1        |            23 |           0.811475 |                  0 |                               |          0 |
| availability_cutoff  | 2025-12-31                        | TRL    |                126 |                    453 |             108 |             0.114754 |             0 |           1        |                108 |                               |          0 |
| availability_cutoff  | 2025-12-31                        | CRL    |                126 |                    453 |              23 |             0.811475 |             0 |           1        |                 23 |                               |          0 |
| availability_cutoff  | 2026-06-30                        | TRL    |                126 |                    453 |             108 |             0.114754 |             0 |           1        |                108 |                               |          0 |
| availability_cutoff  | 2026-06-30                        | CRL    |                126 |                    453 |              23 |             0.811475 |             0 |           1        |                 23 |                               |          0 |
| availability_cutoff  | 2026-09-24                        | TRL    |                126 |                    453 |             108 |             0.114754 |             0 |           1        |                108 |                               |          0 |
| availability_cutoff  | 2026-09-24                        | CRL    |                126 |                    453 |              23 |             0.811475 |             0 |           1        |                 23 |                               |          0 |
| availability_cutoff  | 2026-09-25                        | TRL    |                  0 |                      0 |               0 |             1        |           108 |           0.114754 |                  0 |                               |          0 |
| availability_cutoff  | 2026-09-25                        | CRL    |                  0 |                      0 |               0 |             1        |            23 |           0.811475 |                  0 |                               |          0 |

## 映射阈值（Top1，无间隔门槛）

|   top_k |   cosine_min |   top1_margin_min | entity_type   |   retained_entities |   candidate_links |   covered_topics |   theme_trl_assigned |   theme_crl_assigned | mapping_still_requires_semantic_review   |
|--------:|-------------:|------------------:|:--------------|--------------------:|------------------:|-----------------:|---------------------:|---------------------:|:-----------------------------------------|
|       1 |         0    |                 0 | case          |                 122 |               122 |               86 |                    0 |                    0 | True                                     |
|       1 |         0    |                 0 | direction     |                 391 |               391 |              114 |                    0 |                    0 | True                                     |
|       1 |         0.6  |                 0 | case          |                 122 |               122 |               86 |                    0 |                    0 | True                                     |
|       1 |         0.6  |                 0 | direction     |                 391 |               391 |              114 |                    0 |                    0 | True                                     |
|       1 |         0.65 |                 0 | case          |                 120 |               120 |               85 |                    0 |                    0 | True                                     |
|       1 |         0.65 |                 0 | direction     |                 311 |               311 |               95 |                    0 |                    0 | True                                     |
|       1 |         0.7  |                 0 | case          |                 100 |               100 |               74 |                    0 |                    0 | True                                     |
|       1 |         0.7  |                 0 | direction     |                  30 |                30 |               21 |                    0 |                    0 | True                                     |
|       1 |         0.75 |                 0 | case          |                  47 |                47 |               37 |                    0 |                    0 | True                                     |
|       1 |         0.75 |                 0 | direction     |                   1 |                 1 |                1 |                    0 |                    0 | True                                     |

当前引擎执行时间、对象和判据绑定校验；删证据检验支持依赖性，不等于删掉标准中的必要条件。全部结果仍为公开证据初评，未经独立专家验证。


## 全量版本绑定

{
  "cases": 122,
  "sources": 114,
  "passages": 126,
  "observations": 453,
  "scenario_count": 724,
  "source_loo_cases_with_any_axis_changed": 118,
  "source_loo_fragile_known_trl": 108,
  "source_loo_fragile_known_crl": 23,
  "upgrades": 0,
  "cross_axis_ablation_independence_passed": true,
  "frozen_evidence_only": true,
  "new_remote_evidence_added": 0,
  "limitation": "Conservative withdrawal: any removed citation resets the gate to unknown; remaining support is not semantically re-adjudicated. Not an accuracy experiment.",
  "time_limit": "All 126 available_by values are 2026-09-25. Earlier knowledge-date tests return unknown; they cannot reconstruct historical maturity.",
  "mapping_limit": "Top3 expands candidate coverage only. No cosine threshold certifies semantic correctness or transfers grades.",
  "full_population_records": 5119004,
  "classification_summary_sha256": "67d7d140720a99a87ae46fcf171e34515c1629ae4a402aa116dc30b1e4683568",
  "mapping_sha256": "ba84ce24ab2002824f6c04dec3540e692764f861cbaed607843df4dc470825a2",
  "input_evidence_sha256": {
    "case_technology_links.json": "3fd73326885e8898824ecd1dd6c6bd40b07346fc964aa0f06a022ff8629f24dc",
    "dataset.json": "0fc17d5665e3b5f2482bd18f4629622c664914c71228795b1e01090cd7e70743",
    "evidence.json": "e2d5c3ba55de858c421e95000caaaf56e9c8218a8d46a5d09d2abac89687e4f3",
    "gate_reviews.json": "a18ac5b185463eb7f6e5793f70557606fa2da091f4f56ecdbe6aa5a9b9a17f2e",
    "objects.json": "65b3e2f15781f2a5bb82c818b0e220189f6b662ca799ed276cebbac500cce2d2",
    "observations.json": "66dfd4fed7f0aa4b499ee1f97c740129fc1067dbafe16f5fa95b9e7dcab223b3",
    "observed_facts.json": "d96b1a188d6fe42ccc56bc052c09d7542e48141ece3339557bd6cf9360e7edd5",
    "sources.json": "9f30ec20cbe0cbdd795aeef6c9af934af809df24042a53d9704ff61b219b4f35",
    "technical_profiles.json": "5bb35c207205ac5e17316103c3fa6659714aedf9595d3f4a2af78725c0682d81",
    "technology_registry.json": "dd388a7c93a4fb0a5cbb4dea25fef23c1a3e28795b72ec2e9b5021e42416c452",
    "theme_direction_links.json": "dcab5996a8eb883ac245dc58214809b5d6ed32d7407b7a4c00cad50ba5c9fef6",
    "themes.json": "ff9d5912300e6010fdbe8072ac13f3189b6026ae0c423805e2a2c290b687cf12"
  },
  "rerun_with_full_mapping": true,
  "classification_scope": "all frozen sources",
  "maturity_scope": "all existing bounded evidence objects; no fabricated grades for 500 themes"
}

证据实验通过共用评估引擎执行。全量关联不代表512万条记录都具有成熟度证据。
