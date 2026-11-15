# 成员 41–50

[200 份索引](Index.md) · [本组结构化证据](Trace_05.json)

## RQ1_2e5ccd7b4bd2

第 41 份 · AC  · 上批 报警 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_2e5ccd7b4bd2.sol)

上批同一类别的原始依据为 fallback() 第 121 行，适用的程序性质给出正证（E21、E4、E8，同性质查询 local_premises_feasible/sat, authorization_violation/sat） 下方列出本批依据。

本批具体依据：依赖未能闭合的外部行为、授权政策缺失、授权政策的范围缺少依据。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:363:original:1 fallback|漏检|漏检|漏检|待核|漏检|授权政策的范围缺少依据|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 62 → 40 次，程序用时 4.7 → 6.7 秒，本批剩余动作 0。

## RQ1_283c96463274

第 42 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_283c96463274.sol)

本批具体依据：授权政策缺失、依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 2，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 2 → 2 次，程序用时 2.8 → 12.9 秒，本批剩余动作 0。

## RQ1_511b9f30f4b7

第 43 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_511b9f30f4b7.sol)

本批具体依据：依赖未能闭合的外部行为、授权政策的范围缺少依据。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:38:author:1 withdrawTokens|漏检|漏检|漏检|漏检|漏检|无可定位的该入口覆盖记录|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：不可用 → 可用。实际求解 0 → 0 次，程序用时 1.7 → 77.4 秒，本批剩余动作 0。

## RQ1_e6f04047bff4

第 44 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_e6f04047bff4.sol)

本批具体依据：RegisterDevice() 第 9 行，资格取得与受保护用途对应（E1、E4，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:37:original:1 RegisterDevice|命中|命中|命中|命中|命中|已判断对应效果|
|D2:37:original:2 CollectMoney|漏检|漏检|漏检|漏检|漏检|依赖未能闭合的外部行为|

本批实际报警裁决：RegisterDevice() D2:37:original:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 1，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 2 → 2 次，程序用时 0.2 → 2.1 秒，本批剩余动作 0。

## RQ1_bbf6634a1913

第 45 份 · AC  · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_bbf6634a1913.sol)

上批同一类别的原始依据为 授权政策缺失、依赖未能闭合的外部行为。 下方列出本批依据。

本批具体依据：burnFrom(address,uint256) 第 71 行，适用的程序性质给出正证（E12、E13、E2、E6，同性质查询 local_premises_feasible/sat, authorization_violation/sat）；selfdestructs() 第 120 行，unrestricted_termination_decision（E4）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:3:S1 selfdestructs|命中|命中|漏检|漏检|命中|已判断对应效果|

本批实际报警裁决：burnFrom(address,uint256) 参考外；selfdestructs() D2:3:S1。

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 1，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 2 → 10 次，程序用时 1.1 → 4.3 秒，本批剩余动作 0。

## RQ1_4c2921d39474

第 46 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_4c2921d39474.sol)

本批具体依据：依赖未能闭合的外部行为、授权政策缺失。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:535:author:1 init|命中|命中|命中|漏检|漏检|已有任务阅读记录|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 2。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 53 → 90 次，程序用时 2.0 → 8.3 秒，本批剩余动作 0。

## RQ1_d4aefd2e1bfc

第 47 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_d4aefd2e1bfc.sol)

本批具体依据：授权政策缺失、授权政策的范围缺少依据。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:522:author:1 refundOwner|漏检|漏检|漏检|漏检|漏检|授权政策的范围缺少依据|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 31 → 24 次，程序用时 3.0 → 5.1 秒，本批剩余动作 0。

## RQ1_2490e07356b6

第 48 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_2490e07356b6.sol)

本批具体依据：授权政策的范围缺少依据、依赖未能闭合的外部行为。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:19:author:1 reward|漏检|漏检|漏检|漏检|漏检|授权政策的范围缺少依据|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.5 → 3.2 秒，本批剩余动作 0。

## RQ1_c9a2d9b618a7

第 49 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_c9a2d9b618a7.sol)

本批具体依据：transferFrom(address,address,uint256) 第 39 行，适用的程序性质给出正证（E11、E13、E14、E3，同性质查询 local_premises_feasible/sat, authorization_violation/sat）；FirstBloodToken(address,address,uint256,uint256) 第 88 行，资格取得与受保护用途对应（E17、E7，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:93:author:1 FirstBloodToken|命中|命中|命中|命中|命中|授权政策缺失|

本批实际报警裁决：transferFrom(address,address,uint256) 参考外；FirstBloodToken(address,address,uint256,uint256) D2:93:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：不可用 → 可用。实际求解 4 → 16 次，程序用时 3.4 → 9.5 秒，本批剩余动作 0。

## RQ1_b2a2fc36e6b8

第 50 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_b2a2fc36e6b8.sol)

本批具体依据：授权政策的范围缺少依据、依赖未能闭合的外部行为。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 0 → 6 次，程序用时 1.0 → 4.4 秒，本批剩余动作 0。

