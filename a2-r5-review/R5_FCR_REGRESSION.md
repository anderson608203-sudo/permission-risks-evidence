# R5 FCR 代表配对回归

五类各 3 对，共 30 份真实合约。G 完成 30 份，Simple 完成 30 份。指定类别与完整五类投影在 1 份存在位置差异的合约上仍一致。
指定类别的宏平均 F1 为 **88.00%／88.00%**。整对正确为 **7／7** 对，各以 15 对为分母。这些是代表配对的回归结果。

| 指定风险 | 方法 | 对数 | TP | FP | FN | TN | 风险端未知 | 修复端未知 | 整对正确 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| DESTROY | G | 3 | 2 | 0 | 1 | 1 | 1 | 2 | 1 |
| DESTROY | R4-Simple | 3 | 2 | 0 | 1 | 1 | 1 | 2 | 1 |
| FREEZE | G | 3 | 2 | 0 | 1 | 2 | 1 | 1 | 1 |
| FREEZE | R4-Simple | 3 | 2 | 0 | 1 | 2 | 1 | 1 | 1 |
| MINT | G | 3 | 3 | 0 | 0 | 1 | 0 | 2 | 1 |
| MINT | R4-Simple | 3 | 3 | 0 | 0 | 1 | 0 | 2 | 1 |
| PAUSE | G | 3 | 2 | 0 | 1 | 2 | 1 | 1 | 1 |
| PAUSE | R4-Simple | 3 | 2 | 0 | 1 | 2 | 1 | 1 | 1 |
| TRANSFER | G | 3 | 3 | 0 | 0 | 3 | 0 | 0 | 3 |
| TRANSFER | R4-Simple | 3 | 3 | 0 | 0 | 3 | 0 | 0 | 3 |

FN 已包含风险端未知。修复端未知单列。整对正确要求风险端发出指定类别警报，同时修复端有同类别的有效阴性。FCR 选样优先覆盖以往整对正确、风险端漏报与修复端未知，某一类缺少相应历史情形时按固定哈希补位，共 2 次。标签在两臂结果封存后才参与计分。

唯一的位置差异来自 RQ1_353a9b0b5006。G 多报了偏移 4751 的 PAUSE，两臂仍保留另两处 PAUSE，指定的 DESTROY 均保持未知。两臂同跑 204 次求解，均触及 900 秒程序边界，G 最终登记 32 个动作，Simple 为 31。FCR 回执中 Simple 的额度证明条数为 0。差异与收尾时多完成一项作用检查相符，具体调度因果仍无受控复跑证据。[原始位置和时间差异](Evidence.json)

| 指定风险 | 风险成员 | 修复成员 | G 风险端／修复端 | Simple 风险端／修复端 |
|---|---|---|---|---|
| DESTROY | RQ1_f1bb587376e8 | RQ1_35646ded2a70 | alarm／not_detected | alarm／not_detected |
| DESTROY | RQ1_353a9b0b5006 | RQ1_db11e3e08742 | unsupported／unsupported | unsupported／unsupported |
| DESTROY | RQ1_56bac052a93a | RQ1_f27cacd5f34a | alarm／unsupported | alarm／unsupported |
| FREEZE | RQ1_6244da144ced | RQ1_90c233777f5e | alarm／not_detected | alarm／not_detected |
| FREEZE | RQ1_32e1e7ce1240 | RQ1_101079fc6aa8 | unsupported／not_detected | unsupported／not_detected |
| FREEZE | RQ1_9c365cb18f95 | RQ1_dc06d7bad0d8 | alarm／unsupported | alarm／unsupported |
| MINT | RQ1_e13bb6580d65 | RQ1_94d9f2cfc77c | alarm／not_detected | alarm／not_detected |
| MINT | RQ1_0858684eb758 | RQ1_3ec097691998 | alarm／unsupported | alarm／unsupported |
| MINT | RQ1_bba85280c610 | RQ1_f814ab33ae2c | alarm／unsupported | alarm／unsupported |
| PAUSE | RQ1_b884bab91ca4 | RQ1_f82fc055f5dc | alarm／not_detected | alarm／not_detected |
| PAUSE | RQ1_185a84436c18 | RQ1_ed58b7d7bfbb | unsupported／not_detected | unsupported／not_detected |
| PAUSE | RQ1_4530531bee57 | RQ1_308738db6c81 | alarm／unsupported | alarm／unsupported |
| TRANSFER | RQ1_53f9777ccdf6 | RQ1_a7d72c1e4129 | alarm／not_detected | alarm／not_detected |
| TRANSFER | RQ1_b25ec4a4cd43 | RQ1_14d06cbbe5a7 | alarm／not_detected | alarm／not_detected |
| TRANSFER | RQ1_9451d6dac4de | RQ1_e25d32acc1f7 | alarm／not_detected | alarm／not_detected |

[冻结选样](Cases/FCR.json) · [逐方法原始结果索引](Scores.json) · [结果 CSV](R5_EXPERIMENT_RESULTS.csv)
