# 成员 51–60

[200 份索引](Index.md) · [本组结构化证据](Trace_06.json)

## RQ1_3f952af67006

第 51 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_3f952af67006.sol)

本批具体依据：依赖未能闭合的外部行为、授权政策缺失。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 5 → 5 次，程序用时 37.4 → 29.6 秒，本批剩余动作 0。

## RQ1_a3aff7048f13

第 52 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_a3aff7048f13.sol)

本批具体依据：依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：不可用 → 不可用。实际求解 2 → 2 次，程序用时 60.3 → 58.1 秒，本批剩余动作 0。

## RQ1_fc71e6703f0d

第 53 份 · AC  · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_fc71e6703f0d.sol)

fin 中 tx.origin 的资格条件与唯一终止效果同属这一入口。首答不可用，收到可用的聚焦回复后仍要经过程序核查，最终才出现 fin 报警。独立 pay 根仍漏检；这条时间顺序不能量化反馈的独立贡献。

本批具体依据：fin() 第 11 行，适用的程序性质给出正证（E1、E4，同性质查询 local_premises_feasible/sat, authorization_violation/sat, authorization_violation/unsat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:253:original:1 pay|漏检|漏检|漏检|漏检|漏检|依赖未能闭合的外部行为|
|D2:253:original:2 fin|命中|命中|命中|漏检|命中|已判断对应效果|

本批实际报警裁决：fin() D2:253:original:2。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 0 → 4 次，程序用时 0.1 → 0.2 秒，本批剩余动作 0。

## RQ1_947273fa2eef

第 54 份 · AC  · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_947273fa2eef.sol)

selfdestructs 的唯一终止效果最终通过程序支持，聚焦回复可用。上次同一根未命中；本次基本、初始检查点均未出现该最终结论。

本批具体依据：selfdestructs() 第 132 行，适用的程序性质给出正证（E10、E2，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:20:S1 selfdestructs|命中|命中|漏检|漏检|命中|已判断对应效果|

本批实际报警裁决：selfdestructs() D2:20:S1。

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 2，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 9 → 11 次，程序用时 1.6 → 1.5 秒，本批剩余动作 0。

## RQ1_679bfbe1c927

第 55 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_679bfbe1c927.sol)

本批具体依据：Constructor() 第 29 行，资格取得与受保护用途对应（E1、E8，同性质查询 local_premises_feasible/sat, authorization_violation/sat）；Constructor() 第 29 行，资格取得与受保护用途对应（E14、E3，同性质查询 local_premises_feasible/sat, authorization_violation/sat）；Constructor() 第 29 行，资格取得与受保护用途对应（E12、E2，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:334:author:1 Constructor|命中|命中|命中|命中|命中|已判断对应效果|

本批实际报警裁决：Constructor() D2:334:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 25 → 13 次，程序用时 4.0 → 3.0 秒，本批剩余动作 0。

## RQ1_28fd11561fa6

第 56 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_28fd11561fa6.sol)

本批具体依据：授权政策缺失、依赖未能闭合的外部行为。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:297:author:1 initialize|命中|命中|命中|漏检|漏检|依赖未能闭合的外部行为|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：不可用 → 可用。实际求解 0 → 9 次，程序用时 0.1 → 0.3 秒，本批剩余动作 0。

## RQ1_b11b4b1e0dc3

第 57 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_b11b4b1e0dc3.sol)

本批具体依据：依赖未能闭合的外部行为、授权政策缺失。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 24 → 12 次，程序用时 4.1 → 2.1 秒，本批剩余动作 0。

## RQ1_403e9f180228

第 58 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_403e9f180228.sol)

本批具体依据：授权政策缺失。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 4 → 2 次，程序用时 0.7 → 0.7 秒，本批剩余动作 0。

## RQ1_bc34a2568a3c

第 59 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_bc34a2568a3c.sol)

本批具体依据：授权政策缺失、依赖未能闭合的外部行为。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:173:author:1 TokenERC20|命中|命中|命中|漏检|漏检|已有任务阅读记录|

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 1，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：不可用 → 可用。实际求解 0 → 4 次，程序用时 56.2 → 56.2 秒，本批剩余动作 0。

## RQ1_ae0fe8386d33

第 60 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_ae0fe8386d33.sol)

本批具体依据：LittleCactus() 第 14 行，资格取得与受保护用途对应（E1）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:224:author:1 LittleCactus|命中|命中|命中|命中|命中|已判断对应效果|

本批实际报警裁决：LittleCactus() D2:224:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 4 → 6 次，程序用时 9.2 → 8.9 秒，本批剩余动作 0。

