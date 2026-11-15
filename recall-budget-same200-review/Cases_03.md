# 成员 21–30

[200 份索引](Index.md) · [本组结构化证据](Trace_03.json)

## RQ1_e85ac4a50ee4

第 21 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_e85ac4a50ee4.sol)

实际源内没有可据以补造的 owner，当前见到 policy_scope_unsubstantiated 和外部依赖。作者参考与当前授权规格的缺项独立登记，保留原 FN。

本批具体依据：授权政策的范围缺少依据、依赖未能闭合的外部行为。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:57:author:1 kill|漏检|命中|命中|漏检|漏检|授权政策的范围缺少依据|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 6 → 6 次，程序用时 0.3 → 0.3 秒，本批剩余动作 0。

## RQ1_cfe97b8f7250

第 22 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_cfe97b8f7250.sol)

本批具体依据：依赖未能闭合的外部行为。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:43:author:1 bioLock|漏检|漏检|漏检|漏检|漏检|依赖未能闭合的外部行为|

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 12 → 4 次，程序用时 16.3 → 15.3 秒，本批剩余动作 0。

## RQ1_dadf1b436e9d

第 23 份 · AC  · 上批 报警 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_dadf1b436e9d.sol)

上批 selfdestructs 的终止根已命中，本批仍定位同一入口，实际政策却停在 policy_missing。首答可用，聚焦回复不可用，整份程序用时约 1.6 秒。记录支持政策未绑定，缺少原答正文，不能反推出模型具体说了什么。

本批具体依据：授权政策缺失、依赖未能闭合的外部行为。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:484:S1 selfdestructs|命中|命中|命中|命中|漏检|授权政策缺失|

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 2，最近全量 2。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 11 → 9 次，程序用时 1.6 → 1.6 秒，本批剩余动作 0。

## RQ1_293812debd13

第 24 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_293812debd13.sol)

本批具体依据：依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 1，最近全量 3。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 3.0 → 2.7 秒，本批剩余动作 0。

## RQ1_de08a43a1826

第 25 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_de08a43a1826.sol)

本批具体依据：依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 0，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 99 → 6 次，程序用时 19.9 → 13.3 秒，本批剩余动作 0。

## RQ1_67706b288d9c

第 26 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_67706b288d9c.sol)

本批具体依据：依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 0，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 20 → 11 次，程序用时 12.7 → 11.5 秒，本批剩余动作 0。

## RQ1_fccabbab2795

第 27 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_fccabbab2795.sol)

本批具体依据：依赖未能闭合的外部行为、授权政策缺失。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.2 → 0.2 秒，本批剩余动作 0。

## RQ1_e7801f3e61cb

第 28 份 · AC  · 上批 报警 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_e7801f3e61cb.sol)

proposeOwnership 只设置候任人；acceptOwnership 校验候任人后才交权。当前该入口的实际局部依据为 nominee_acceptance，旧参考外报警得到局部纠正。两次模型分析均不可用，整份 AC 仍未决。

本批具体依据：授权政策缺失、依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

上批参考外组的去向：proposeOwnership(address) 已撤报，有同范围正常依据。

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 83 → 54 次，程序用时 47.5 → 45.3 秒，本批剩余动作 0。

## RQ1_e97f2d279ad9

第 29 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_e97f2d279ad9.sol)

本批具体依据：依赖未能闭合的外部行为。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:47:S1 Prosperity|命中|命中|命中|漏检|漏检|已有任务阅读记录|
|D2:47:S2 giveBlockReward|漏检|命中|命中|漏检|漏检|已有任务阅读记录|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 47 → 16 次，程序用时 3.6 → 2.3 秒，本批剩余动作 0。

## RQ1_1007b4fc52ca

第 30 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_1007b4fc52ca.sol)

终止根继续命中。burnFrom 的旧报警消失，源码确有同一 holder 给调用者的 allowance 检查和扣减。本轮归档对此入口只给 source_task_reading，能复核源码，不能确认是哪条特定反证导致撤报。

本批具体依据：selfdestructs() 第 119 行，适用的程序性质给出正证（E3、E8，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:236:S1 selfdestructs|命中|命中|漏检|命中|命中|已判断对应效果|

上批参考外组的去向：burnFrom(address,uint256) 已撤报，仅有通用阅读记录。

本批实际报警裁决：selfdestructs() D2:236:S1。

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 0，最近全量 2。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 6 → 4 次，程序用时 1.2 → 1.3 秒，本批剩余动作 0。

