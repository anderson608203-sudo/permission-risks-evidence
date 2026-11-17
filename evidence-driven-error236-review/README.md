# Permission Risks：236错误集真实复测审阅

请按 **[WorkReview](WorkReview.md) → [Changes](Changes.md) → 本页导航 → [Code实际源码](Code.md)** 阅读。

本批方法fb113462、配置40ca33d9，203 AC＋33 FCR，不是新Full1164。归档、人口和冻结核验通过，235份最终报告＋1份预算异常失败。AC同成员10TP/51FP/286FN（上批9/0/287）；7新增、6丢失。FCR指定类仅新增1 DESTROY；MINT3误报撤回但仍未知，不能算3 TN。暂不支持直接扩大运行。

| 目标 | 直接阅读 |
|---|---|
| 全236成员及逐例 | [Members](Members.md) |
| 全296作者根与新旧变化 | [Roots](Roots.md) |
| FCR五类、33份指定结果 | [FCR](FCR.md) |
| 实际235报告检查/证据/查询/语义/请求 | [Evidence](Evidence.md)、[逐成员定位](EvidenceIndex.json) |
| 完整112源码、方法99、真实worker七文件 | [Code](Code.md)、[文件SHA](MethodFiles.json) |
| 评分、冻结、源码配置与资源 | [Scores](Scores.json)、[Freeze](Freeze.json)、[Versions](Versions.json)、[Resources](Resources.json) |
| LLM机制和审阅限制 | [LLM](LLM.json)、[SelfReview](SelfReview.json) |
| 历史同人口根映射 | [History](History.md) |

InputSource页是全部236份实际输入完整源码，UTF-8字节SHA逐件匹配；Method页是本批完整生产源码与真实运行器。网页中的分片均可直接读，不需要下载或Python。

Release附件为`PR_Error236_Lite.zip`、`PR_Error236_Source.zip`及各自`.sha256`；应优先读网页。Lite保存安全报告原件、过程和独立评分材料；Source保存原目录完整源码、配置和精确差异。GitHub自动生成的Source code ZIP不是这两个研究附件。

上传后固定最终提交或发布标签阅读，不以未来main替代。原模型正文、思维链、具体地址实参/交易序列/SMT/赋值没有恢复；源码中原有内容按原字节保留。未知、未运行、失败不当安全，不改变历史Gold或评分。

核算与边界：[评分规则](ScoringPolicy.json) · [独立原件复算](IndependentAudit.json)。

可选：[标准库只读复算脚本](Recompute.py)。用`--lite PR_Error236_Lite.zip --source PR_Error236_Source.zip`直接核算两个ZIP，无需解压、安装方法依赖或运行检测；根因语义仍由审阅侧匹配表负责。不能执行Python时继续按网页定向阅读。
