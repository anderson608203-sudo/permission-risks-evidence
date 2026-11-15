# 成员 11–20

[200 份索引](Index.md) · [本组结构化证据](Trace_02.json)

## RQ1_b809aa517821

第 11 份 · AC  · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_b809aa517821.sol)

上批同一类别的原始依据为 授权政策缺失、依赖未能闭合的外部行为。 下方列出本批依据。

本批具体依据：mintTo(address,uint256) 第 59 行，unrestricted_issuance_decision（E4）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:416:author:1 mintTo|命中|命中|命中|漏检|命中|已判断对应效果|

本批实际报警裁决：mintTo(address,uint256) D2:416:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 10 → 29 次，程序用时 0.5 → 3.9 秒，本批剩余动作 0。

## RQ1_868007cf433c

第 12 份 · AC  · 上批 报警 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_868007cf433c.sol)

上批同一类别的原始依据为 fallback() 第 29 行，适用的程序性质给出正证（E1、E3，同性质查询 local_premises_feasible/sat, authorization_violation/sat, authorization_violation/unsat）；fallback() 第 29 行，适用的程序性质给出正证（E2、E4，同性质查询 local_premises_feasible/sat, authorization_violation/sat, authorization_violation/unsat） 下方列出本批依据。

本批具体依据：授权政策缺失。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:222:original:1 fallback|漏检|漏检|漏检|命中|漏检|授权政策缺失|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 4 → 2 次，程序用时 0.4 → 3.2 秒，本批剩余动作 0。

## RQ1_96012699cf50

第 13 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_96012699cf50.sol)

本批具体依据：依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 0 → 0 次，程序用时 2.5 → 7.3 秒，本批剩余动作 0。

## RQ1_51a9713a1934

第 14 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_51a9713a1934.sol)

本批具体依据：依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 5，b5 1，最近全量 2。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 38 → 38 次，程序用时 4.9 → 31.8 秒，本批剩余动作 0。

## RQ1_afa801e14aca

第 15 份 · AC  · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_afa801e14aca.sol)

上批同一类别的原始依据为 授权政策缺失、依赖未能闭合的外部行为。 下方列出本批依据。 根因裁决待核。QMQCoin 取得 owner，但最终报告具体落在 distr 内的供给扣记。

本批具体依据：QMQCoin() 第 101 行，适用的程序性质给出正证（E1、E4、E8、E9，同性质查询 local_premises_feasible/sat, authorization_violation/sat, authorization_violation/unsat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:393:author:1 QMQCoin|命中|命中|命中|漏检|待核|unassessed_role_change|

本批实际报警裁决：QMQCoin() 对应根待核。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 1，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 11 → 76 次，程序用时 3.9 → 12.1 秒，本批剩余动作 0。

## RQ1_adc795eb2050

第 16 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_adc795eb2050.sol)

本批具体依据：依赖未能闭合的外部行为。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:108:original:1 initialize|漏检|漏检|漏检|漏检|漏检|已有任务阅读记录|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 6 → 5 次，程序用时 1.0 → 3.7 秒，本批剩余动作 0。

## RQ1_a4bb8d18e79b

第 17 份 · AC  · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_a4bb8d18e79b.sol)

本批具体依据：已纳入局部阅读的义务依据含该范围无对应效果、已有任务阅读记录。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.2 → 2.2 秒，本批剩余动作 0。

## RQ1_6674f42c37b9

第 18 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_6674f42c37b9.sol)

本批具体依据：Ownable() 第 86 行，资格取得与受保护用途对应（E13、E3，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:113:author:1 Ownable|命中|命中|命中|命中|命中|已判断对应效果|

本批实际报警裁决：Ownable() D2:113:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 1，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 29 → 17 次，程序用时 160.6 → 180.9 秒，本批剩余动作 0。

## RQ1_2a3f29f582b8

第 19 份 · AC  · 上批 报警 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_2a3f29f582b8.sol)

上批同一类别的原始依据为 end_redeem_period() 第 65 行，适用的程序性质给出正证（E1、E2，同性质查询 local_premises_feasible/sat, authorization_violation/sat, authorization_violation/unsat） 下方列出本批依据。

本批具体依据：依赖未能闭合的外部行为、授权政策缺失。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:412:author:1 end_redeem_period|漏检|命中|命中|命中|漏检|授权政策缺失|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 4 → 0 次，程序用时 0.3 → 2.6 秒，本批剩余动作 0。

## RQ1_053265dda42e

第 20 份 · AC  · 上批 报警 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_053265dda42e.sol)

上批同一类别的原始依据为 fallback() 第 22 行，适用的程序性质给出正证（E1、E7，同性质查询 local_premises_feasible/sat, authorization_violation/sat） 下方列出本批依据。

本批具体依据：授权政策的范围缺少依据、授权政策缺失。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

上批参考外组的去向：fallback() 已撤报，原效果未决。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 1，最近全量 2。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 20 → 3 次，程序用时 0.7 → 2.8 秒，本批剩余动作 0。

