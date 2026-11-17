# AC Readiness · Full1164 审阅入口

请先读[WorkReview.md](WorkReview.md)，再读[Changes.md](Changes.md)。两个数据集均已完成并在评分前冻结。本批AC为194TP／8FP／287FN，FCR Macro-F1 94.10%、整对161/270，技术错误0。未决与失败按既定规则处理。

## 无需下载的完整阅读路径

1. [逐成员索引](Members.md)导航624份AC和540份FCR，每份链接到实际输入、真实检查与查询、服务回执索引及阶段投影。
2. [481个AC独立根](Roots.md)、[270个FCR对](Pairs.md)、[289条AC裁决](Adjudication.json)与[评分](Scores.json)支持逐项复核。
3. [实际方法和运行器](Code.md)列出完整源码、配置、worker、真实Client与依赖文件，Method分段可以直接读全部内容。
4. [冻结](Freeze.json)、[版本](Versions.json)、[资源](Resources.json)、[机制诊断](Mechanisms.json)、[九份技术恢复](TechnicalRecovery.json)、[Baseline来源](Baselines.md)及[本人核验](SelfReview.md)保留身份和边界。

Cases为逐例审阅，InputSource为全部1164实际源码，Checks为全部46261项实际检查，Queries为全部63846条查询投影，Requests为全部1879次服务回执索引。E编号只在同一成员内有效。basic在初答接纳后，阶段变化不当作LLM消融。

## Release附件

PR_ACReadiness_Full1164_Lite.zip保存网页版、独立评分材料、全部1164最终安全报告、预测导出、查询和服务回执。PR_ACReadiness_Full1164_Source.zip保存本次完整运行源码、配置与运行器原目录。两个附件均有.sha256。

归档实际方法`2e0fcbed9cc0d530e7e3591f6bee6e1cba70a79bad01167c2381b43637debe17`，配置`40ca33d909fef65652dd9e956d33639b05adb464dd2c7f0a82c140e8d421c7c4`。阅读应固定最终上传提交或发布标签，避免main后续变化。若Release下载失败，按上面网页链接仍可独立核对成员、源码、决定与评分。原始模型正文未保存。
