# 成员 1–10

[200 份索引](Index.md) · [本组结构化证据](Trace_01.json)

## RQ1_e5f934bea8ec

第 1 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_e5f934bea8ec.sol)

本批具体依据：依赖未能闭合的外部行为、授权政策缺失、授权政策的范围缺少依据。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 3。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 2 → 0 次，程序用时 4.3 → 13.8 秒，本批剩余动作 0。

## RQ1_2c07fdcf80d4

第 2 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_2c07fdcf80d4.sol)

本批具体依据：setAllowedAddress(address) 第 29 行，资格取得与受保护用途对应（E1、E5，同性质查询 local_premises_feasible/sat, authorization_violation/sat）；setAllowedAddress(address) 第 29 行，资格取得与受保护用途对应（E2、E6，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:458:author:1 setAllowedAddress|命中|命中|命中|命中|命中|已判断对应效果|

本批实际报警裁决：setAllowedAddress(address) D2:458:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 3 → 7 次，程序用时 1.2 → 4.4 秒，本批剩余动作 0。

## RQ1_ce214e96568d

第 3 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_ce214e96568d.sol)

本批具体依据：Constructor() 第 29 行，资格取得与受保护用途对应（E2、E22，同性质查询 local_premises_feasible/sat, authorization_violation/sat）；Constructor() 第 29 行，资格取得与受保护用途对应（E26、E3，同性质查询 local_premises_feasible/sat, authorization_violation/sat）；Constructor() 第 29 行，资格取得与受保护用途对应（E1、E16，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:157:author:1 Constructor|命中|命中|命中|命中|命中|已判断对应效果|

本批实际报警裁决：Constructor() D2:157:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 13 → 19 次，程序用时 2.9 → 7.9 秒，本批剩余动作 0。

## RQ1_cb8c3fafbda1

第 4 份 · FCR-MINT 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_cb8c3fafbda1.sol)

本批具体依据：mintToken(address,uint256) 第 201 行，受控受益人的新增权益（E3）

配对成员 [RQ1_7bfd58ffb1ae](Cases_12.md#rq1_7bfd58ffb1ae)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 未知 / 报警 / 报警 / 报警 / 报警。

本批其他类别还报出 FCR-FREEZE，单独记录。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 226 → 199 次，程序用时 298.9 → 300.3 秒，本批剩余动作 81。

## RQ1_afb609e0053e

第 5 份 · FCR-PAUSE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_afb609e0053e.sol)

本批具体依据：disableTransfers(bool) 第 46 行，控制变化能阻断普通正额转出（E2、E4、E6）

配对成员 [RQ1_7405f0959142](Cases_19.md#rq1_7405f0959142)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 报警 / 报警。

原 25 对源码复核（旧轮次的观察）：19　afb609e0053e / 7405f0959142　U/U，Q11，A（由03的C调整，限测试账本范围）。CryptoRoulette 两端第42行保留角色setter并写布尔反值。风险第49–60行普通持有人转出会读取开关并真实借贷；修复第49行起保留借贷但不读开关。布尔初值为假，必须有真实setter提供可用阶段。特别补核：真实金融支持精确命中 balance_test，角色支持命中 owner_test；该表可查、可由持有人转移，足以支持本版域内该表的权益解释。PAUSE检查确实存在，但其E7记录 control_transition_preservation 的局部 UNSAT，扩大状态域的排除检查为 SAT，排除证书未成立，最终 scope_missing；其他问题的 baseline_usable 等不能移用。缺口在启用基线、方向和相同权益的效果消费，无法据此证明实际部署角色或与赌场原生币可兑换。修复本端的同一暂停作用应被排除；另一个合约功能的外调只在会改变该主张时才影响它。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 7 → 7 次，程序用时 0.6 → 2.9 秒，本批剩余动作 0。

## RQ1_b649070a92c3

第 6 份 · FCR-PAUSE 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_b649070a92c3.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_cd39ae0d15a5](Cases_13.md#rq1_cd39ae0d15a5)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 6 → 3 次，程序用时 1.4 → 3.8 秒，本批剩余动作 0。

## RQ1_0fa374173417

第 7 份 · AC  · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_0fa374173417.sol)

上批同一类别的原始依据为 授权政策缺失、依赖未能闭合的外部行为。 下方列出本批依据。

本批具体依据：mintTo(address,uint256) 第 59 行，unrestricted_issuance_decision（E4）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:311:author:1 mintTo|命中|命中|命中|漏检|命中|已判断对应效果|

本批实际报警裁决：mintTo(address,uint256) D2:311:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 18 → 29 次，程序用时 1.1 → 4.4 秒，本批剩余动作 0。

## RQ1_62bedd2d4a5a

第 8 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_62bedd2d4a5a.sol)

本批具体依据：Constructor() 第 29 行，资格取得与受保护用途对应（E1、E12，同性质查询 local_premises_feasible/sat, authorization_violation/sat）；Constructor() 第 29 行，资格取得与受保护用途对应（E16、E2，同性质查询 local_premises_feasible/sat, authorization_violation/sat）；Constructor() 第 29 行，资格取得与受保护用途对应（E18、E3，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:111:author:1 Constructor|命中|命中|命中|命中|命中|已判断对应效果|

本批实际报警裁决：Constructor() D2:111:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 不可用。实际求解 19 → 19 次，程序用时 3.8 → 8.6 秒，本批剩余动作 0。

## RQ1_b4fca92c3262

第 9 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_b4fca92c3262.sol)

本批具体依据：依赖未能闭合的外部行为、授权政策缺失。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:97:S1 owned|命中|命中|命中|漏检|漏检|已有任务阅读记录|
|D2:97:S2 STARTMETADOLLAR|漏检|命中|命中|漏检|漏检|授权政策缺失|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 40 → 70 次，程序用时 88.6 → 222.6 秒，本批剩余动作 0。

## RQ1_770b64940b4d

第 10 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_770b64940b4d.sol)

本批具体依据：依赖未能闭合的外部行为、授权政策的范围缺少依据。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:293:author:1 withdrawTokens|漏检|漏检|漏检|漏检|漏检|无可定位的该入口覆盖记录|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：不可用 → 可用。实际求解 0 → 0 次，程序用时 0.4 → 3.8 秒，本批剩余动作 0。

