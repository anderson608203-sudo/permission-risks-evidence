# R5 关键变化及作用回执

下表使用冻结作者根和位置匹配口径。撤回的五处参考外报警均找到同作用额度证明。位置为原合约文件的字节偏移，供已持原件的审阅者复核。源码文件、对象、路径、固定回复和实际预测可通过中性记录对齐。 [核查字段](Evidence.json) · [逐合约记录](Cases/README.md)

| 成员 | 评分变化 | 对应作用或位置 | 其余边界 |
|---|---|---|---|
| RQ1_cba197c27f19 | 撤回 1 FP | transferFrom，2546 | 原独立发行命中保留 |
| RQ1_3092779b88eb | 撤回 1 FP | transferFrom，2547 | 与前项同源码家族 |
| RQ1_e4944522697f | 撤回 1 FP | transferFrom，2928 | 留出家族 |
| RQ1_5ee0702dae51 | 撤回 1 FP | transferFrom，1674 | 留出家族 |
| RQ1_447e629016cc | 撤回 1 FP | transferFrom，2289 | 整体从报警回到未知 |
| RQ1_9e7faad9335a | 减少 1 TP | D2:337:S2，G 匹配窗口 1647–2165 | 父作用得到正常证明，派生同名作用仍需核定 |

最后一行中，G 的位置属于 `StandardToken.transferFrom`，Simple 的正常证明落在父合约余额作用偏移 1906。另一个同名函数的窗口为 6042–6216，属于 `STCDR.transferFrom`。冻结参考仅保存函数名，原计分保留 1 TP 损失。独立的作者根 `D2:337:S1` 继续命中。 [实际绑定、证明和两个窗口](Evidence.json)

FCR 唯一报告位置差异在 RQ1_353a9b0b5006。两臂的 DESTROY 同为未知，PAUSE 同为报警。G 的报告多一个 PAUSE 位置。G 和 Simple 分别执行 32 和 31 个动作，均发起 204 次求解并到达程序时间边界。该批没有 FCR 的 Simple 正常额度证明。 [位置和耗时字段](Evidence.json) · [全五类逐合约投影](Cases/FCR.json)

回执采用保留字段视图，含实际 `operation`、`Property`、源位置、声明和语义项摘要。原对象摘要和完整归档定位见 [Freeze.json](Freeze.json)。
