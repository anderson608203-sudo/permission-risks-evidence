# 成员 21–30

[200 份索引](Index.md) · [本组结构化证据](Trace_03.json)

## RQ1_e85ac4a50ee4

第 21 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_e85ac4a50ee4.sol)

本批具体依据：授权政策的范围缺少依据、依赖未能闭合的外部行为、授权政策缺失。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:57:author:1 kill|漏检|命中|命中|漏检|漏检|授权政策的范围缺少依据|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 6 → 6 次，程序用时 0.3 → 2.4 秒，本批剩余动作 0。

## RQ1_cfe97b8f7250

第 22 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_cfe97b8f7250.sol)

本批具体依据：依赖未能闭合的外部行为、授权政策缺失。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:43:author:1 bioLock|漏检|漏检|漏检|漏检|漏检|依赖未能闭合的外部行为|

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 4 → 45 次，程序用时 15.3 → 42.3 秒，本批剩余动作 0。

## RQ1_dadf1b436e9d

第 23 份 · AC  · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_dadf1b436e9d.sol)

上批同一类别的原始依据为 授权政策缺失、依赖未能闭合的外部行为。 下方列出本批依据。

本批具体依据：selfdestructs() 第 133 行，unrestricted_termination_decision（E4）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:484:S1 selfdestructs|命中|命中|命中|漏检|命中|已判断对应效果|

本批实际报警裁决：selfdestructs() D2:484:S1。

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 2，最近全量 2。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 9 → 10 次，程序用时 1.6 → 5.0 秒，本批剩余动作 0。

## RQ1_293812debd13

第 24 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_293812debd13.sol)

本批具体依据：依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 1，最近全量 3。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 0 → 0 次，程序用时 2.7 → 9.1 秒，本批剩余动作 0。

## RQ1_de08a43a1826

第 25 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_de08a43a1826.sol)

本批具体依据：依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 0，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：不可用 → 不可用。实际求解 6 → 30 次，程序用时 13.3 → 48.9 秒，本批剩余动作 0。

## RQ1_67706b288d9c

第 26 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_67706b288d9c.sol)

本批具体依据：依赖未能闭合的外部行为、授权政策缺失。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 0，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：不可用 → 可用。实际求解 11 → 14 次，程序用时 11.5 → 23.2 秒，本批剩余动作 0。

## RQ1_fccabbab2795

第 27 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_fccabbab2795.sol)

本批具体依据：依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 0 → 0 次，程序用时 0.2 → 2.4 秒，本批剩余动作 0。

## RQ1_e7801f3e61cb

第 28 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_e7801f3e61cb.sol)

本批具体依据：授权政策缺失、依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：不可用 → 可用。实际求解 54 → 78 次，程序用时 45.3 → 122.0 秒，本批剩余动作 0。

## RQ1_e97f2d279ad9

第 29 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_e97f2d279ad9.sol)

本批具体依据：授权政策缺失、依赖未能闭合的外部行为。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:47:S1 Prosperity|命中|命中|命中|漏检|漏检|已有任务阅读记录|
|D2:47:S2 giveBlockReward|漏检|命中|命中|漏检|漏检|已有任务阅读记录|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 16 → 29 次，程序用时 2.3 → 7.0 秒，本批剩余动作 0。

## RQ1_1007b4fc52ca

第 30 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_1007b4fc52ca.sol)

本批具体依据：selfdestructs() 第 120 行，unrestricted_termination_decision（E3）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:236:S1 selfdestructs|命中|命中|漏检|命中|命中|已判断对应效果|

本批实际报警裁决：selfdestructs() D2:236:S1。

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 0，最近全量 2。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 4 → 8 次，程序用时 1.3 → 4.9 秒，本批剩余动作 0。

