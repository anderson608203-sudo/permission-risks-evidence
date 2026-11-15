# 成员 191–200

[200 份索引](Index.md) · [本组结构化证据](Trace_20.json)

## RQ1_db73c28a69c2

第 191 份 · FCR-TRANSFER 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_db73c28a69c2.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_1844e5d3d18e](Cases_17.md#rq1_1844e5d3d18e)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 未知 / 未知 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：不可用 → 可用。实际求解 0 → 16 次，程序用时 0.2 → 0.9 秒，本批剩余动作 0。

## RQ1_5eee31e70615

第 192 份 · FCR-DESTROY 风险 · 上批 有效未检出 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_5eee31e70615.sol)

上批没有可用模型分析且未检出。现在 balances_test 的扣款进入所属账本，E3 的直接效果 SAT，DESTROY 在基本检查点已报警。不同对象上同时有计数与金融语义，不能将全文件带 test 的变量一律当钱。

本批具体依据：destroy(address,uint256) 第 25 行，持有人权益扣减且未见同人补偿（E2、E3，同性质查询 local_premises_feasible/sat, direct_effect/sat）

配对成员 [RQ1_f322b5b8495d](Cases_13.md#rq1_f322b5b8495d)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 有效未检出 / 有效未检出 / 报警。

原 25 对源码复核（旧轮次的观察）：09　5eee31e70615 / f322b5b8495d　N/N，Q0，C。Overflow_Add.destroy 两端第21行，风险第25–26行扣 balances_test 和供应。无可用模型分析。原记录的 necessary_effect_absent 对应普通 add(uint256)，不是 destroy；这与8456同时有独立计数和测试余额，是有辨别力的阴/阳对照。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：不可用 → 可用。实际求解 0 → 2 次，程序用时 0.0 → 0.2 秒，本批剩余动作 0。

## RQ1_6a278772c4f3

第 193 份 · FCR-FREEZE 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_6a278772c4f3.sol)

本批具体依据：账本单位缺少依据。

配对成员 [RQ1_980e04c92f4d](Cases_14.md#rq1_980e04c92f4d)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 未知 / 未知。

本批其他类别还报出 FCR-MINT, FCR-DESTROY, FCR-PAUSE，单独记录。

原 25 对源码复核（旧轮次的观察）：23　6a278772c4f3 / 980e04c92f4d　U/U，Q66，B（局部）。AdvanceToken 公开第164、184行内联转账；派生helper第228行、冻结读取第244、270行。修复第247行仍写冻结状态。真实暂停与出售管理员权限各自保留，不能替代这一FREEZE作用。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 52 → 36 次，程序用时 14.5 → 13.5 秒，本批剩余动作 29。

## RQ1_7450d39da940

第 194 份 · FCR-FREEZE 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_7450d39da940.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_39fb6e7197c4](Cases_12.md#rq1_39fb6e7197c4)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 3 → 3 次，程序用时 1.1 → 1.9 秒，本批剩余动作 0。

## RQ1_a0facbcc1e38

第 195 份 · FCR-MINT 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_a0facbcc1e38.sol)

本批具体依据：withdrawLOOiX() 第 362 行，适用的程序性质给出正证（E22、E29、E33、E39、E42、E45，同性质查询 local_premises_feasible/sat, direct_effect/unsat, financial_value_post_exclusion/unsat, same_request_amount_change/unsat, financial_value_post_exclusion/sat, financial_value/sat, financial_value/unsat）；mintToken(address,uint256) 第 408 行，适用的程序性质给出正证（E13、E4、E44、E56、E68，同性质查询 local_premises_feasible/sat, direct_effect/sat, financial_value_post_exclusion/unsat, same_request_amount_change/unsat）

配对成员 [RQ1_86a0269d7608](Cases_12.md#rq1_86a0269d7608)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 报警 / 未知 / 报警 / 报警 / 未知 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 79 → 79 次，程序用时 54.6 → 56.0 秒，本批剩余动作 55。

## RQ1_58de46f081ec

第 196 份 · FCR-FREEZE 风险 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_58de46f081ec.sol)

实际代币公开转账内联，没有经过读取冻结标志的派生 helper。指定 FREEZE 仍为未检出，按作者参考计 FN；独立 MINT 仍报警。局部源码与标签范围疑点另列。

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_2046acc1c802](Cases_20.md#rq1_2046acc1c802)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出。

本批其他类别还报出 FCR-MINT，单独记录。

原 25 对源码复核（旧轮次的观察）：21　58de46f081ec / 2046acc1c802　N/N，Q28，B。KDA 应用 TokenERC20.transfer 第70行、transferFrom 第93行。派生helper第174–192行核冻结收发双方；freezeAccount 第205行写表。修复第196行仍有setter，helper已去相关条件，两边公开转账都不经过它。实际编译AST中该风险版两个helper声明ID为251、793，引用数均为0。MINT的独立报警保留，FREEZE仍按原参考为FN。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 25 → 36 次，程序用时 4.8 → 6.2 秒，本批剩余动作 0。

## RQ1_a4c5ecc3c29e

第 197 份 · FCR-TRANSFER 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_a4c5ecc3c29e.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_cf32aac41cf2](Cases_13.md#rq1_cf32aac41cf2)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 0 → 0 次，程序用时 0.3 → 0.1 秒，本批剩余动作 0。

## RQ1_fa2207747d01

第 198 份 · FCR-FREEZE 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_fa2207747d01.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_cd47d22b26a9](Cases_09.md#rq1_cd47d22b26a9)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 3 → 9 次，程序用时 1.6 → 2.9 秒，本批剩余动作 0。

## RQ1_2046acc1c802

第 199 份 · FCR-FREEZE 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_2046acc1c802.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_58de46f081ec](Cases_20.md#rq1_58de46f081ec)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 3 → 15 次，程序用时 1.8 → 2.6 秒，本批剩余动作 0。

## RQ1_8e8598bb724e

第 200 份 · FCR-PAUSE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_8e8598bb724e.sol)

本批具体依据：disableTransfers(bool) 第 100 行，控制变化能阻断普通正额转出（E2、E4、E6）；disableTransfers(bool) 第 100 行，控制变化能阻断普通正额转出（E1、E3、E5）

配对成员 [RQ1_fbd0377ce541](Cases_12.md#rq1_fbd0377ce541)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 报警 / 未知 / 报警 / 报警 / 未知 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 不可用。实际求解 11 → 2 次，程序用时 1.6 → 0.9 秒，本批剩余动作 0。

指定类结果稳定，但报警理由由 适用的程序性质给出正证 变为 控制变化能阻断普通正额转出。

