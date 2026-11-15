# 成员 121–130

[200 份索引](Index.md) · [本组结构化证据](Trace_13.json)

## RQ1_81a85f242b60

第 121 份 · FCR-MINT 修复 · 上批 有效未检出 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_81a85f242b60.sol)

本次唯一指定类修复端误报。普通购买被判 ordinary_paid_credit；另一条 setTokenExchangeRate 的 E29 在 controlled_or_self_only 约束下给出 financial_value SAT。源码的付款、购买时段、currentSupply 上限及购买者入账均存在。报告未区分调价者按相同购买规则取得更多代币与其可额外享有专属新增权益。按冻结参考记 FP，跨入口消费是否过宽为有据推断。

本批具体依据：setTokenExchangeRate(uint256) 第 156 行，适用的程序性质给出正证（E25、E29、E30、E31、E32、E5，同性质查询 financial_value/unsat, financial_value_post_exclusion/sat, financial_value/sat）

配对成员 [RQ1_b61f163309a1](Cases_10.md#rq1_b61f163309a1)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 报警 / 未知 / 有效未检出 / 报警 / 报警 / 有效未检出 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 4 → 37 次，程序用时 1.7 → 4.9 秒，本批剩余动作 0。

## RQ1_6c3522e11e92

第 122 份 · FCR-DESTROY 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_6c3522e11e92.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_9a61667124cf](Cases_13.md#rq1_9a61667124cf)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 2 → 2 次，程序用时 2.5 → 2.4 秒，本批剩余动作 0。

## RQ1_5b3c7cbe3d9d

第 123 份 · FCR-FREEZE 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_5b3c7cbe3d9d.sol)

本批具体依据：账本单位缺少依据。

配对成员 [RQ1_0f3c3f400f6f](Cases_18.md#rq1_0f3c3f400f6f)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 未知 / 未知。

本批其他类别还报出 FCR-MINT, FCR-DESTROY, FCR-PAUSE，单独记录。

原 25 对源码复核（旧轮次的观察）：22　5b3c7cbe3d9d / 0f3c3f400f6f　U/U，Q67，B（局部）。AdvanceToken 应用 BaseToken 第171、191行，实际读paused；第253行派生helper的冻结时间、账户判断第309、350行未接入。修复公开入口第171、188行，冻结setter仍在第291行。观察冻结状态的getter不能代替转出被阻。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 56 → 36 次，程序用时 15.8 → 15.2 秒，本批剩余动作 29。

## RQ1_8456d2957fff

第 124 份 · FCR-DESTROY 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_8456d2957fff.sol)

附表扣款、金融单位与角色依据在两批均支持 DESTROY；保留这一既有正确对照，不把共享程序的已有能力算作本批新增。

本批具体依据：destroy(address,uint256) 第 25 行，持有人权益扣减且未见同人补偿（E2、E3，同性质查询 local_premises_feasible/sat, direct_effect/sat）

配对成员 [RQ1_776a6b98d18f](Cases_10.md#rq1_776a6b98d18f)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 2 → 2 次，程序用时 0.2 → 0.2 秒，本批剩余动作 0。

## RQ1_cd39ae0d15a5

第 125 份 · FCR-PAUSE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_cd39ae0d15a5.sol)

本批具体依据：stop() 第 112 行，控制变化能阻断普通正额转出（E12、E15、E17、E3、E5）

配对成员 [RQ1_b649070a92c3](Cases_01.md#rq1_b649070a92c3)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 报警 / 未知 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 18 → 13 次，程序用时 2.9 → 2.5 秒，本批剩余动作 0。

指定类结果稳定，但报警理由由 适用的程序性质给出正证 变为 控制变化能阻断普通正额转出。

## RQ1_1f06ce07140f

第 126 份 · FCR-TRANSFER 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_1f06ce07140f.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_e73c99ca23e5](Cases_11.md#rq1_e73c99ca23e5)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 3 → 19 次，程序用时 2.6 → 3.1 秒，本批剩余动作 0。

## RQ1_cf32aac41cf2

第 127 份 · FCR-TRANSFER 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_cf32aac41cf2.sol)

本批具体依据：zero_fee_transaction(address,address,uint256) 第 27 行，适用的程序性质给出正证（E1、E3，同性质查询 local_premises_feasible/sat, direct_effect/sat, direct_effect/unsat）

配对成员 [RQ1_a4c5ecc3c29e](Cases_20.md#rq1_a4c5ecc3c29e)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 未知 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 3 → 3 次，程序用时 0.4 → 0.4 秒，本批剩余动作 0。

## RQ1_fe7add810da5

第 128 份 · FCR-DESTROY 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_fe7add810da5.sol)

本批具体依据：已纳入局部阅读的义务依据含已判断对应效果、在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_15346457ba72](Cases_16.md#rq1_15346457ba72)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.2 → 0.2 秒，本批剩余动作 0。

## RQ1_9a61667124cf

第 129 份 · FCR-DESTROY 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_9a61667124cf.sol)

本批具体依据：账本单位缺少依据、依赖未能闭合的外部行为。

配对成员 [RQ1_6c3522e11e92](Cases_13.md#rq1_6c3522e11e92)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 未知 / 未知 / 未知 / 未知。

本批其他类别还报出 FCR-PAUSE，单独记录。

原 25 对源码复核（旧轮次的观察）：16　9a61667124cf / 6c3522e11e92　U/U，Q20，C。BasicToken 第75行destroy、第83行zero_fee_transaction 同用 balances_test，后者提供独立用途证据；修复第75行去角色并删除后一入口。不要把另一套标准 balances 当作这张表。实跑金融支持落在 StandardToken.balances，报告有PAUSE及TRANSFER记录，没有DESTROY专项。沿实际派生目标核对，保留另一类别的有效判断。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 15 → 19 次，程序用时 6.0 → 7.0 秒，本批剩余动作 0。

## RQ1_f322b5b8495d

第 130 份 · FCR-DESTROY 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_f322b5b8495d.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_5eee31e70615](Cases_20.md#rq1_5eee31e70615)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.2 → 0.1 秒，本批剩余动作 0。

