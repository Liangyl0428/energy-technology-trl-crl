# 复现与扩展

克隆仓库后，在仓库根目录运行：

```sh
python -m pip install -r requirements.txt
python -m trl_crl build
python -m trl_crl validate
python -m unittest discover -s tests -v
```

无需项目外的历史目录、原始文献全库、API密钥或GPU。评估计算与验证均可离线执行；Excel导出使用openpyxl，纯JSON/CSV可用`--no-excel`。

```sh
python -m trl_crl build --data data --output /tmp/trl-crl-results --no-excel
python -m trl_crl validate --data data --output /tmp/trl-crl-results
```

脚本从当前门槛与证据计算结果，不把已有数值作为输入。`validate`重新运行同一输入，检查结果文件一致性、配对约束、正式等级为空和输入哈希。

回归测试覆盖两轴独立、跨对象引用、计划冒充完成、未解决反证、档案变更、来源篡改、截止日期、氢能不同配置不能拼轴、合成收入和未来产能不能直接判级，以及可移植Excel导出。

扩展数据时，先明确对象和场景，再登记来源、引文、性能要求与逐门槛判断。门槛审阅的`profile_sha256`必须对应已完成实质核读的当前技术档案。哈希更新不能代替重新审阅。

可选检索命令：

```sh
python -m trl_crl.research "质子交换膜 电解槽 投运" --before 2026-09-26 --output research_output/leads.json
```

`--before`是排他的新闻查询日期条件。搜索返回新闻线索；仍须访问原始来源、确认日期与对象，才能接受为证据。搜索不会自动写入判级输入。
