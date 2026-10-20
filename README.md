# 能源技术 TRL / CRL 评估

依据明确配置、场景和时期的公开证据，分别评估技术验证阶段 TRL 与商业活动阶段 CRL，并给出下一步验证、示范或尽调问题。主题用于组织信息，不直接获得成熟度等级。

当前 **122 个对象**中，108 个有 TRL，23 个有 CRL，13 个双轴均已知，99 个 CRL 未知。等级是公开证据初评，正式等级保持空值；证据截止 2026-09-25，不代表今天的产品状态。

| 输出 | 用途 | 入口 |
|---|---|---|
| P2 对象决策卡 | 配置、场景、双轴解释、具体核查清单；38 个对象有业务主题关联候选 | [JSON](assets/full_nmf500/p2/case_decision_cards.json) |
| P1 门槛与证据 | 支持某阶段的原始引文、未支持门槛和补证要求 | [对象解读](assets/full_nmf500/p1/case_insights.json) / [门槛证据](assets/full_nmf500/p1/gate_evidence.json) |
| 类型修正后的基础接口 | 等级只包含整数或 null；状态、说明和展示文本分列 | [JSON](assets/full_nmf500/case_hotspot_links.json) / [Schema](assets/full_nmf500/case_hotspot_links.schema.json) |

TRL3 表示理论可行性验证，CRL4 表示规模化商业应用。若同时出现，应先核对是否同一对象配置、场景和时期，不能直接称技术成熟。当前数据没有 CRL4 案例。未知不等于最低等级，对象等级不外推为主题等级。

**尚未按最新 KWD 72 主题重新关联或扩充证据。** P2 和 F500 主题链接均有各自的版本与候选状态。

## 代码与使用

- [判据](trl_crl/rules.py)、[引擎](trl_crl/engine.py)、[决策解读](trl_crl/insights.py)、[类型化导出](trl_crl/delivery.py)。
- [对象与证据](data/)、[主题关联](pipelines/full_nmf/build.py)、[敏感性实验](assets/full_nmf500/experiments/REPORT.md)。
- [业务手册](https://github.com/Liangyl0428/energy-topic-identification/blob/main/platform/docs/P2业务主题与决策使用手册.md)、[使用范围](NOTICE.md)。

```bash
python -m pip install -r requirements.txt -r requirements-nmf500.txt pytest
python -m pytest tests -q
python tools/check_current_release.py
python -m trl_crl build --output /tmp/trl-crl-rebuild
python -m trl_crl validate --output /tmp/trl-crl-rebuild
```

## 数据与运行边界

Git 保存源码、配置、紧凑统计、抽样证据和业务解读。大型原始 `data/`、冻结语料、向量、模型、数据库和全量逐篇导出继续留在外部工作区。克隆仓库可阅读交付及运行测试，不等于拥有全量重算输入。

全量流水线通过 `config/runtime_paths.json` 指定输入，支持 `ENERGY_DATA_ROOT`、`ENERGY_CORPUS_DIR`、`ENERGY_METADATA_DB`、`ENERGY_CLASSIFICATION_RUN` 等环境变量。相对路径按配置文件位置解析。三个仓库并列克隆可进行联合运行；跨模块 P1/P2 构建请先组装平台目录，见[平台接入说明](docs/PLATFORM_INTEGRATION.md)。

本次为仓库整理和现有成果同步，未重训分类、重算热点或抬高成熟度等级。各版本范围和编号必须随接口展示；程序检查通过不等于语义准确率或专家验收通过。

[算法方法](docs/METHOD.md) · [复现说明](docs/REPRODUCING.md) · [文件用途](docs/PROJECT_STRUCTURE.md) · [核心文件清单](docs/CORE_FILES.md)
