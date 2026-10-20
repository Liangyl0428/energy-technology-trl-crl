# 复现与运行

当前全量入口可读取本仓库的 `config/runtime_paths.json`；跨模块 P1/P2 构建使用组装后的 `final` 运行包。先参照 [平台接入说明](PLATFORM_INTEGRATION.md) 确认运行布局。先查看[运行配置与输入清单](https://github.com/Liangyl0428/energy-topic-identification/blob/main/platform/docs/运行配置与输入清单.md)和[平台字段字典](https://github.com/Liangyl0428/energy-topic-identification/blob/main/platform/docs/数据与指标字典.md)。数据根目录、冻结语料、元数据库、BGE 模型和输出位置均可配置；相对路径相对于配置文件，不依赖启动目录。

在项目根目录先做只读预检：

```sh
.venv-hotspots/bin/python final/tools/check_inputs.py
```

外部语料、模型和元数据库不会随紧凑交付打包。搬迁时保留 `final/runtime_config.py` 与 `final/config/`，设置 `ENERGY_DATA_ROOT` 或 `ENERGY_PLATFORM_CONFIG`；缺失依赖会明确报错。基础依赖见本模块 requirements 或 pyproject。

## 修复后的成熟度导出

```sh
.venv-hotspots/bin/python final/energy-technology-trl-crl/pipelines/full_nmf/build_crl_reason.py
```

该兼容入口按现有证据引擎重建等级，导出整数/空值、状态、说明、展示文本和同名 JSON/schema，并按当前主题主表同步名称；不再把缺证据文字写入等级列。支持 `--data/--source/--out/--catalog`，可重复执行。

## 完整主题映射

```sh
.venv-hotspots/bin/python final/energy-technology-trl-crl/pipelines/full_nmf/build.py --hotspots final/energy-topic-hotspots/assets/full_nmf500
```

分类、上下文和输出目录默认从统一配置读取；热点参数在此示例中使用已交付的冻结结果。上下文需与当前对象及原文证据完全匹配，否则应先运行 `pipelines/nmf500/encode_context.py` 编码。新 build 同样导出数值类型与同步名称，因此修复不会在下次重建时丢失。

在本模块目录可单独执行原有基础引擎：

```sh
python -m trl_crl build --data data --output /tmp/trl-crl-current --no-excel
python -m trl_crl validate --data data --output /tmp/trl-crl-current
```

基础引擎的来源主题上下文不等于当前 F500 目录；前端 F 主题关联请使用 `assets/full_nmf500/case_hotspot_links.csv` 或 JSON。P0 未修改量表、证据或门槛，不会新增正式等级。

## 本地校验

在模块目录运行 `python -m pytest -q`。发布前需更新本地资产和源码指纹；当前 P0 的统一验收结果见[验收记录](https://github.com/Liangyl0428/energy-topic-identification/blob/main/platform/docs/P0修复验收.md)。完整性检查通过只说明字段、证据及版本一致，不替代主题语义审核或正式成熟度评定。
