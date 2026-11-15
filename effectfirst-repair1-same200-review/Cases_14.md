# 成员 131–140

[200 份索引](Index.md) · [本组结构化证据](Trace_14.json)

## RQ1_024b9da10799

第 131 份 · FCR-MINT 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_024b9da10799.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果、已有任务阅读记录。

配对成员 [RQ1_73b13298e227](Cases_14.md#rq1_73b13298e227)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 13 → 13 次，程序用时 8.2 → 13.8 秒，本批剩余动作 0。

## RQ1_985c6fd1d4e4

第 132 份 · FCR-FREEZE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_985c6fd1d4e4.sol)

本批具体依据：freezeAccount(address,bool) 第 50 行，控制变化能阻断普通正额转出（E1、E2、E3）

配对成员 [RQ1_46a031a993c1](Cases_10.md#rq1_46a031a993c1)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 不可用。实际求解 1 → 1 次，程序用时 0.4 → 2.5 秒，本批剩余动作 0。

## RQ1_73b13298e227

第 133 份 · FCR-MINT 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_73b13298e227.sol)

本批具体依据：mint(address,uint256) 第 746 行，适用的程序性质给出正证（E18、E34、E43、E44，同性质查询 local_premises_feasible/sat, direct_effect/sat）；burnFrom(address,uint256) 第 808 行，适用的程序性质给出正证（E64、E7、E93，同性质查询 financial_value_post_exclusion/unsat, same_request_amount_change/unsat, financial_value_post_exclusion/sat, financial_value/sat）；distributeReward(address,address,address) 第 926 行，适用的程序性质给出正证（E12、E28、E49、E50，同性质查询 local_premises_feasible/sat, direct_effect/sat）

配对成员 [RQ1_024b9da10799](Cases_14.md#rq1_024b9da10799)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 报警 / 未知 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 83 → 80 次，程序用时 33.7 → 46.2 秒，本批剩余动作 104。

## RQ1_a69a455c4a25

第 134 份 · FCR-FREEZE 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_a69a455c4a25.sol)

本批具体依据：已纳入局部阅读的义务依据含detached_local_holder_switch、在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_adf28b957352](Cases_14.md#rq1_adf28b957352)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 不可用。实际求解 12 → 0 次，程序用时 2.5 → 4.7 秒，本批剩余动作 0。

## RQ1_4feeb0c21e60

第 135 份 · FCR-TRANSFER 风险 · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_4feeb0c21e60.sol)

上批同一类别的原始依据为 依赖未能闭合的外部行为、账本单位缺少依据。 下方列出本批依据。 两版模型分析均不可用；本版由源码读写和直接转移判断得到指定类阳性。

本批具体依据：zero_fee_transaction(address,address,uint256) 第 22 行，existing_rights_moved（E1）

配对成员 [RQ1_0e202076b336](Cases_19.md#rq1_0e202076b336)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 未知 / 未知 / 未知 / 报警。

原 25 对源码复核（旧轮次的观察）：01　4feeb0c21e60 / 0e202076b336　U/U，Q11，C。BANK_SAFE.zero_fee_transaction 风险/修复均第17行。独立 balances_test 与原银行业务账分开；已消费语义集中在资格和条件，三个判断无指定类别。先登记这个账本及特权去向；不能借银行存取款证明它是同一权益。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：不可用 → 不可用。实际求解 0 → 0 次，程序用时 0.2 → 2.5 秒，本批剩余动作 0。

## RQ1_adf28b957352

第 136 份 · FCR-FREEZE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_adf28b957352.sol)

本批具体依据：freezeAccount(address,bool) 第 197 行，适用的程序性质给出正证（E10、E11、E12、E13、E15、E25，同性质查询 baseline_usable/sat, financial_block/sat, control_transition_preservation/sat, financial_block/unsat）

配对成员 [RQ1_a69a455c4a25](Cases_14.md#rq1_a69a455c4a25)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 未知 / 未知 / 报警 / 报警 / 报警 / 报警 / 报警。

本批其他类别还报出 FCR-TRANSFER，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 308 → 236 次，程序用时 296.5 → 148.4 秒，本批剩余动作 0。

## RQ1_980e04c92f4d

第 137 份 · FCR-FREEZE 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_980e04c92f4d.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：账本单位缺少依据。

配对成员 [RQ1_6a278772c4f3](Cases_20.md#rq1_6a278772c4f3)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 0 → 10 次，程序用时 2.3 → 6.8 秒，本批剩余动作 0。

## RQ1_e25d32acc1f7

第 138 份 · FCR-TRANSFER 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_e25d32acc1f7.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_9451d6dac4de](Cases_12.md#rq1_9451d6dac4de)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 6 → 0 次，程序用时 0.4 → 2.0 秒，本批剩余动作 0。

## RQ1_35e0e8d95f92

第 139 份 · FCR-MINT 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_35e0e8d95f92.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_c75d73e1c482](Cases_11.md#rq1_c75d73e1c482)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

本批其他类别还报出 FCR-TRANSFER，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 134 → 230 次，程序用时 56.9 → 217.4 秒，本批剩余动作 0。

## RQ1_b0a696b11b0a

第 140 份 · FCR-PAUSE 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_b0a696b11b0a.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_4f9f1ce04ed8](Cases_15.md#rq1_4f9f1ce04ed8)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 8 → 8 次，程序用时 0.6 → 2.6 秒，本批剩余动作 0。

