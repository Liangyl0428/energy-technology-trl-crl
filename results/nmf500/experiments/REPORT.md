# TRL/CRL 灵敏度与证据消融

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
|       1 |         0    |                 0 | case          |                 122 |               122 |               91 |                    0 |                    0 | True                                     |
|       1 |         0    |                 0 | direction     |                 391 |               391 |              121 |                    0 |                    0 | True                                     |
|       1 |         0.6  |                 0 | case          |                 122 |               122 |               91 |                    0 |                    0 | True                                     |
|       1 |         0.6  |                 0 | direction     |                 389 |               389 |              120 |                    0 |                    0 | True                                     |
|       1 |         0.65 |                 0 | case          |                 121 |               121 |               90 |                    0 |                    0 | True                                     |
|       1 |         0.65 |                 0 | direction     |                 241 |               241 |               98 |                    0 |                    0 | True                                     |
|       1 |         0.7  |                 0 | case          |                 104 |               104 |               79 |                    0 |                    0 | True                                     |
|       1 |         0.7  |                 0 | direction     |                  22 |                22 |               20 |                    0 |                    0 | True                                     |
|       1 |         0.75 |                 0 | case          |                  48 |                48 |               41 |                    0 |                    0 | True                                     |
|       1 |         0.75 |                 0 | direction     |                   1 |                 1 |                1 |                    0 |                    0 | True                                     |

v0.2.1补充时间、对象和判据绑定校验，并修正W011证据解释；删证据检验支持依赖性，不等于删掉标准中的必要条件。全部结果仍为公开证据初评，未经独立专家验证。
