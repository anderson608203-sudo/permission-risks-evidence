# 成员 171–180

[200 份索引](Index.md) · [本组结构化证据](Trace_18.json)

## RQ1_0f3c3f400f6f

第 171 份 · FCR-FREEZE 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_0f3c3f400f6f.sol)

本批具体依据：账本单位缺少依据。

配对成员 [RQ1_5b3c7cbe3d9d](Cases_13.md#rq1_5b3c7cbe3d9d)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 3.4 → 3.4 秒，本批剩余动作 0。

## RQ1_cea156e41c29

第 172 份 · FCR-PAUSE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_cea156e41c29.sol)

本批具体依据：disableTransfers(bool) 第 43 行，控制变化能阻断普通正额转出（E2、E3、E4）

配对成员 [RQ1_d695cf0bad2e](Cases_10.md#rq1_d695cf0bad2e)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 7 → 7 次，程序用时 0.8 → 0.6 秒，本批剩余动作 0。

指定类结果稳定，但报警理由由 适用的程序性质给出正证 变为 控制变化能阻断普通正额转出。

## RQ1_fe11616caf66

第 173 份 · FCR-TRANSFER 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_fe11616caf66.sol)

本批具体依据：zero_fee_transaction(address,address,uint256) 第 20 行，适用的程序性质给出正证（E2、E3，同性质查询 local_premises_feasible/sat, direct_effect/sat, direct_effect/unsat）

配对成员 [RQ1_6476444da7e8](Cases_16.md#rq1_6476444da7e8)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 未知 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 3 → 3 次，程序用时 0.3 → 0.3 秒，本批剩余动作 0。

## RQ1_0bf6f8bce8d9

第 174 份 · FCR-DESTROY 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_0bf6f8bce8d9.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_196284e657b0](Cases_12.md#rq1_196284e657b0)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 1 → 0 次，程序用时 0.4 → 0.3 秒，本批剩余动作 0。

## RQ1_8d60a47186e2

第 175 份 · FCR-TRANSFER 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_8d60a47186e2.sol)

本批具体依据：已纳入局部阅读的义务依据含已判断对应效果、该范围无对应效果。

配对成员 [RQ1_7d7240a2af90](Cases_12.md#rq1_7d7240a2af90)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：不可用 → 可用。实际求解 0 → 0 次，程序用时 0.0 → 0.3 秒，本批剩余动作 0。

## RQ1_bcafc7a40ce2

第 176 份 · FCR-DESTROY 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_bcafc7a40ce2.sol)

本批具体依据：依赖未能闭合的外部行为、账本单位缺少依据。

配对成员 [RQ1_e1ce695fff9e](Cases_11.md#rq1_e1ce695fff9e)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 未知 / 报警 / 未知 / 未知 / 未知。

原 25 对源码复核（旧轮次的观察）：08　bcafc7a40ce2 / e1ce695fff9e　U/U，Q5，C。PrivateBank.destroy 两端第39行。已有问题定位在第39行但未定类别；金融支持指向原银行 balances，测试供应 totalSupply 得到 nonfinancial_counter 支持。须核对与测试账本同量扣减是否构成可独立确认的权益用途；任一标签均不应直接覆盖另一个账本。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 6 → 6 次，程序用时 0.3 → 0.4 秒，本批剩余动作 0。

## RQ1_b5217318672e

第 177 份 · FCR-TRANSFER 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_b5217318672e.sol)

本批具体依据：账本单位缺少依据、依赖未能闭合的外部行为。

配对成员 [RQ1_72c6b8c6b605](Cases_12.md#rq1_72c6b8c6b605)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 未知 / 未知 / 未知。

原 25 对源码复核（旧轮次的观察）：04　b5217318672e / 72c6b8c6b605　U/U，Q5，C。ETH_FUND 两端第31行；运行确实定位过第31行，但未定类别。角色标在 owner_test，金融支持标在主表 balances；日志计数也有不同标注。应先处理同一张表，不能合并这几条支持。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 6 → 6 次，程序用时 0.4 → 0.5 秒，本批剩余动作 0。

## RQ1_b731957fa974

第 178 份 · FCR-MINT 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_b731957fa974.sol)

本批具体依据：issue(address,uint256) 第 79 行，受控受益人的新增权益（E24、E44，同性质查询 local_premises_feasible/sat, direct_effect/sat）；issue(address,uint256) 第 79 行，受控受益人的新增权益（E25、E45，同性质查询 local_premises_feasible/sat, direct_effect/sat）；issue(address,uint256) 第 79 行，受控受益人的新增权益（E21、E43，同性质查询 local_premises_feasible/sat, direct_effect/sat）；issue(address,uint256) 第 79 行，受控受益人的新增权益（E10、E41，同性质查询 local_premises_feasible/sat, direct_effect/sat）

配对成员 [RQ1_4968e56244c9](Cases_16.md#rq1_4968e56244c9)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 报警 / 报警 / 报警。

本批其他类别还报出 FCR-PAUSE，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 24 → 28 次，程序用时 6.1 → 5.5 秒，本批剩余动作 0。

## RQ1_3a3d833ca142

第 179 份 · FCR-TRANSFER 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_3a3d833ca142.sol)

此附表转付在两批均能取得金融单位及实际角色的支持，指定 TRANSFER 稳定命中。和同构附表仍缺单位的成员应分别按其本次语义核对。

本批具体依据：zero_fee_transaction(address,address,uint256) 第 20 行，适用的程序性质给出正证（E2、E3，同性质查询 local_premises_feasible/sat, direct_effect/sat, direct_effect/unsat）

配对成员 [RQ1_206d19a8539c](Cases_09.md#rq1_206d19a8539c)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 3 → 3 次，程序用时 0.3 → 0.4 秒，本批剩余动作 0。

## RQ1_aaeb3f57cfd0

第 180 份 · FCR-PAUSE 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_aaeb3f57cfd0.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_20dfd0c54b94](Cases_19.md#rq1_20dfd0c54b94)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 72 → 71 次，程序用时 12.6 → 15.0 秒，本批剩余动作 0。

