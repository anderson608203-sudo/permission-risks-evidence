# 成员 81–90

[200 份索引](Index.md) · [本组结构化证据](Trace_09.json)

## RQ1_0526c008875c

第 81 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_0526c008875c.sol)

本批具体依据：授权政策缺失。

该成员没有作者 AC 参考根因。参考外报警仍计入误报分组。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 3 → 0 次，程序用时 0.2 → 0.1 秒，本批剩余动作 0。

## RQ1_9aafb6cd1add

第 82 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_9aafb6cd1add.sol)

Owned2 资格重配继续命中。旧 transferFrom 报警已撤，当前该入口的政策范围为 policy_scope_unsubstantiated，即使同合约别处有阳性也不能算此处已获阴性。

本批具体依据：Owned2() 第 37 行，资格取得与受保护用途对应（E12、E2，同性质查询 local_premises_feasible/sat, authorization_violation/sat）；Owned2() 第 37 行，资格取得与受保护用途对应（E1、E8，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:587:author:1 Owned2|命中|命中|命中|命中|命中|已判断对应效果|

上批参考外组的去向：transferFrom(address,address,uint256) 已撤报，原效果未决。

本批实际报警裁决：Owned2() D2:587:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 36 → 20 次，程序用时 1.2 → 1.1 秒，本批剩余动作 0。

## RQ1_84ed7052a606

第 83 份 · AC  · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_84ed7052a606.sol)

DepositContract.init 重配 Holder 的源码判断在基本检查点已经成立。后续反馈未形成可用分析，最终仍保留该根。

本批具体依据：init() 第 67 行，资格取得与受保护用途对应（E1、E5，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:418:author:1 init|命中|漏检|命中|漏检|命中|已判断对应效果|

本批实际报警裁决：init() D2:418:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 1，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 16 → 16 次，程序用时 0.7 → 0.7 秒，本批剩余动作 0。

## RQ1_770ae395781c

第 84 份 · FCR-MINT 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_770ae395781c.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果、已有任务阅读记录。

配对成员 [RQ1_bc5855a83e2d](Cases_16.md#rq1_bc5855a83e2d)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 0 → 6 次，程序用时 2.9 → 3.3 秒，本批剩余动作 0。

## RQ1_cd47d22b26a9

第 85 份 · FCR-FREEZE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_cd47d22b26a9.sol)

本批具体依据：freezeAccount(address,bool) 第 183 行，适用的程序性质给出正证（E13、E19、E2、E41、E48、E50，同性质查询 control_transition_preservation/sat, baseline_usable/sat, financial_block/unknown, financial_block/sat, financial_block/unsat）

配对成员 [RQ1_fa2207747d01](Cases_20.md#rq1_fa2207747d01)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 未知 / 报警 / 报警 / 报警 / 报警。

本批其他类别还报出 FCR-MINT，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 100 → 93 次，程序用时 114.0 → 298.4 秒，本批剩余动作 125。

## RQ1_0267e2a8ebb2

第 86 份 · FCR-MINT 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_0267e2a8ebb2.sol)

本批具体依据：mintToken(address,uint256) 第 201 行，受控受益人的新增权益（E17、E35，同性质查询 local_premises_feasible/sat, direct_effect/sat）

配对成员 [RQ1_3b4d9f6eb96f](Cases_15.md#rq1_3b4d9f6eb96f)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警。

本批其他类别还报出 FCR-FREEZE，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 173 → 290 次，程序用时 118.8 → 258.7 秒，本批剩余动作 26。

## RQ1_0c666ce785e8

第 87 份 · FCR-TRANSFER 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_0c666ce785e8.sol)

本批具体依据：账本单位缺少依据、依赖未能闭合的外部行为。

配对成员 [RQ1_3455b6a9ba4f](Cases_15.md#rq1_3455b6a9ba4f)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 报警 / 未知 / 未知。

原 25 对源码复核（旧轮次的观察）：05　0c666ce785e8 / 3455b6a9ba4f　U/U，Q5，C。PrivateBank 两端第22行。实际金融支持在 balances，当前的三项检查定位其他业务；上批的该类 program_support 此次未保住。这是风险侧相对上一协议批唯一丢失的命中。没有逐字回答，不能断言某句措辞造成丢失。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 6 → 6 次，程序用时 0.3 → 0.6 秒，本批剩余动作 0。

## RQ1_4be3030c4533

第 88 份 · FCR-MINT 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_4be3030c4533.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_af7c473b8cca](Cases_17.md#rq1_af7c473b8cca)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 186 → 185 次，程序用时 119.9 → 299.7 秒，本批剩余动作 50。

## RQ1_206d19a8539c

第 89 份 · FCR-TRANSFER 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_206d19a8539c.sol)

本批具体依据：已纳入局部阅读的义务依据含已判断对应效果、在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_3a3d833ca142](Cases_18.md#rq1_3a3d833ca142)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.2 → 0.2 秒，本批剩余动作 0。

## RQ1_085aaca2f412

第 90 份 · FCR-DESTROY 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_085aaca2f412.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_c9626779c857](Cases_11.md#rq1_c9626779c857)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.3 → 0.5 秒，本批剩余动作 0。

