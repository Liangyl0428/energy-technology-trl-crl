# 能源技术 TRL / CRL 评估

全量冻结快照已完成：4,831,088篇论文、281,295条专利、6,621条政策，共5,119,004条。查看[全量结果报告](assets/full_nmf500/REPORT.md)、[覆盖与校验记录](assets/full_nmf500/)。主题编号F0001–F0500；下方v0.2.1与750类为保留的历史结果，不能混用。

本次交付版本为重新定义的 Git `v0.2.0`：全量 NMF500、全量专利／政策候选匹配、热点与有界 TRL/CRL 重评，以及消融／灵敏度实验。主题效果比较见[结果摘要](assets/full_nmf500/topic_evaluation/RESULTS.md)和[评测口径](docs/TOPIC_EVALUATION.md)。旧 `v0.2.0`/`v0.2.1` 标签已按要求移除，历史材料保留用于比较；不要用下方样本版链接作为本次全量结果入口。

## 保留的历史样本与750类基线说明

`v0.2.1`：[严格审查与修正](docs/V0.2.1_AUDIT.md)。补齐证据时间、引文完整性、对象与判据绑定，
撤回W011缺乏支持的TRL9/CRL2，重算[500主题关联及724个证据消融情景](results/nmf500/)。
当前108个对象有TRL、23个有CRL、13个双轴齐全，4个双轴未知；均为公开证据初评。

基于可追溯证据，分别评估技术成熟度（TRL）与商业就绪度（CRL）。资料截止 **2026-09-25**。

新增[NMF500主题重算与热点联合分析](docs/NMF500.md)，输出在
`results/nmf500/`。该版重新建立主题候选关联并从原始证据复算TRL/CRL；
主题关联待语义复核，主题自身不继承案例等级。

- **TRL**：Q/GDW 12566—2025《技术成熟度评价方法》，1—9级。
- **CRL**：项目招标书的1—5级定义及调研细化的商业证据规则。
- **评价对象**：配置、场景、功能和时期明确的技术应用对象；主题目录只组织文献。

## 当前结果

|指标|数量|
|---|---:|
|当前样本版主题编号 / 历史全量主题|500 / 750|
|候选技术方向|391|
|有界评价对象|122|
|有TRL证据阶段|108|
|有CRL证据阶段|23|
|同对象两轴都有值|13|
|两轴均未知|4|

**结果属于公开证据初评，不是独立专家正式评级。** 未知轴留空；方向不取关联案例最大值或均值生成统一等级。122个对象不等于122个已确认独立技术方向。

- [结果Excel](results/技术_TRL_CRL评估结果.xlsx)：打开“技术对象结果”；还包含方向证据分布、主题目录、逐项判据、来源和缺项。
- [当前500主题联合Excel](results/nmf500/500主题热点与TRL_CRL.xlsx)：当前主题关联、热点与对象证据；根目录结果保留历史750主题组织方式。
- [结果CSV](results/assessment_units.csv) / [结果JSON](results/assessment_units.json)
- [评估报告](results/评估报告.md)
- [处理方法](docs/METHOD.md) / [数据说明](docs/DATA_SCHEMA.md) / [复现说明](docs/REPRODUCING.md)

## 处理流程

```text
750历史主题目录（当前另有500主题样本重映射）
    ↓ 识别技术名称、对象及应用任务
391候选技术方向
    ↓ 限定技术配置、应用场景和证据时期
有界评价对象 → 来源核读与引文 → 独立TRL判据 / 独立CRL判据 → 结果与缺项
```

检索或词频不直接产生等级。逐项证据门槛由原文核读形成；计算引擎验证对象、引文、事件状态和判据，并分别计算两轴。专利申请或授权不独立决定CRL；实际许可履约可作为商业证据。

## 运行

Python 3.10及以上，在仓库根目录执行：

```sh
python -m pip install -r requirements.txt
python -m trl_crl build
python -m trl_crl validate
python -m unittest discover -s tests -v
```

默认读取`data/`并输出到`results/`；自定义位置：

```sh
python -m trl_crl build --data data --output /tmp/trl-crl-results
```

结果计算完全离线，不需要API密钥。可选新闻检索只发现线索，不改变评估值：

```sh
python -m trl_crl.research "浮式风电 投运" --before 2026-09-26 --output research_output/leads.json
```

## 文件组织

```text
trl_crl/     独立判据引擎、输入校验、结果导出、可选检索
 data/       当前对象、技术方向、判据审阅、来源与必要引文
 results/    当前Excel、CSV、JSON、报告和验证记录
 docs/       方法、数据结构、复现说明
 tests/      两轴独立性、跨对象、时间、证据篡改等回归测试
```

C开头与W开头的对象ID用于来源追踪，均采用同一套规则。W为网页/项目案例编号，不是成熟度级别。

仓库保留必要引文和来源URL，不包含招标书、标准PDF或完整论文文件。离线验证能够核查引文完整性及计算过程；远端原文真实性、完整风险覆盖与正式评价仍需相应专业审查。来源使用范围见[NOTICE](NOTICE.md)。


<!-- FULL_EXPERIMENTS -->
全量消融与灵敏度实验已重新计算并通过验证。[实验报告](assets/full_nmf500/experiments/REPORT.md)。具体范围与证据边界见[实验及发布流程](docs/FULL_EXPERIMENTS.md)。


<!-- TOPIC_EVALUATION -->
本次全量版与历史主题版本、其他方法的[统一口径效果对比](assets/full_nmf500/topic_evaluation/REPORT.md)已完成；[评测口径及局限](docs/TOPIC_EVALUATION.md)。这是回溯聚类质量诊断，不是人工语义准确率或独立留出验证。
