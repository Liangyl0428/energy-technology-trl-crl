# 全量NMF主题与证据对象关联

`pipelines/full_nmf/build.py`读取全量论文重新拟合的目录及BGE-M3论文主题中心，并将现有有界技术对象、技术方向重新关联到新目录。全部文档来源数量来自全量分类摘要，不使用原14.2万篇样本摘要。

```sh
.venv-hotspots/bin/python energy-technology-trl-crl/pipelines/full_nmf/build.py
```

已有对象从原始证据与判据重新评估，主题关联保存Top3及余弦。主题级TRL/CRL保持空值，因为全量文档归类与成熟度证据覆盖不是同一件事。未增加外部成熟度证据，也不因为换主题而提高等级。

输出在`results/full_nmf500_20260926`，紧凑结果在全量流程完成后同步到`assets/full_nmf500`。共享全量入口与进度见主题仓库`docs/FULL_NMF.md`。
