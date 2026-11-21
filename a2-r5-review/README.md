# Permission Risks · A2-R5 网页审阅

SmartBug624 成对回放中，**Simple 少报 5 处参考外报警，少命中 1 个作者根**。本方向留出家族中，Simple 撤回 3 处参考外报警，保留全部 165 个原命中。FCR 五类 15 对代表样本的指定类别结果一致。

## 阅读顺序

1. [WorkReview.md](WorkReview.md) 汇总结论、风险与尚未核实的问题。
2. [Changes.md](Changes.md) 对照 G 和 Simple 的实际代码、补丁、配置及消费者边界。
3. [AC 有效性分析](R5_EFFECTIVENESS_ANALYSIS.md) · [FCR 回归](R5_FCR_REGRESSION.md) · [方法取舍](R5_METHOD_SELECTION.md)
4. [逐合约记录](Cases/README.md) · [原逐合约 CSV](R5_EXPERIMENT_RESULTS.csv) · [六处关键差异](Evidence.md)
5. [总分和分组](Scores.json) · [封存](Freeze.json) · [版本](Versions.json) · [资源与技术状态](Resources.json) · [网页文件清单](Manifest.json)

## 核对范围

R5 对 624 份 AC 合约和 30 份 FCR 合约各运行两臂，合计 1,308 个槽，完成 1,280 个，28 个超时。两臂复用同一历史真实首答，没有新增模型请求。作者标注在预测封存后用于计分。FCR 只有代表配对回归，覆盖五类各三对。

逐合约 CSV 保留交付原字节。网页分片从同一冻结结果提取运行状态、参考根、预测和摘要。三份原报告仅调整了链接指向。源码目录收录三处变更对应的四份实际源码，以及两臂共用配置。完整归档的 SHA-256 与原证据文件摘要见 [Freeze.json](Freeze.json)。CSV 的 `raw_run` 对应完整归档中的运行目录。

可按 [verify_web.py](verify_web.py) 对照网页文件摘要，并重算主要分数、逐根变化、家族拆分及 FCR 指定类别结果。下载本目录后执行 `python -B a2-r5-review/verify_web.py`，只需 Python 标准库。完整求解回执、历史首答和原始执行环境的核验需要本地原归档。

[标签与审阅口径](WorkReview.md) · [逐例消费证据](Evidence.json)
