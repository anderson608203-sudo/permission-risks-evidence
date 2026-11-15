# 成员 111–120

[200 份索引](Index.md) · [本组结构化证据](Trace_12.json)

## RQ1_49db443acf1d

第 111 份 · FCR-TRANSFER 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_49db443acf1d.sol)

本批具体依据：已纳入局部阅读的义务依据含已判断对应效果、在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_4febca8bfe3b](Cases_15.md#rq1_4febca8bfe3b)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.2 → 0.2 秒，本批剩余动作 0。

## RQ1_7bfd58ffb1ae

第 112 份 · FCR-MINT 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_7bfd58ffb1ae.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_cb8c3fafbda1](Cases_01.md#rq1_cb8c3fafbda1)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 报警 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

本批其他类别还报出 FCR-TRANSFER，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 25 → 168 次，程序用时 20.1 → 139.1 秒，本批剩余动作 0。

## RQ1_196284e657b0

第 113 份 · FCR-DESTROY 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_196284e657b0.sol)

本批具体依据：依赖未能闭合的外部行为、账本单位缺少依据。

配对成员 [RQ1_0bf6f8bce8d9](Cases_18.md#rq1_0bf6f8bce8d9)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 未知 / 未知 / 未知。

原 25 对源码复核（旧轮次的观察）：10　196284e657b0 / 0bf6f8bce8d9　U/U，Q1，C。MY_BANK.destroy 两端第29行，第33–34行扣测试余额/供应。唯一金融支持绑定结构体中的 balance 字段，没有落在 balance_test；专项判断缺席，报告另记外部依赖。隔离原生币账本及其外调。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 1 → 0 次，程序用时 0.3 → 0.1 秒，本批剩余动作 0。

## RQ1_7d7240a2af90

第 114 份 · FCR-TRANSFER 风险 · 上批 有效未检出 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_7d7240a2af90.sol)

普通转账仍有局部排除；另一条 zero_fee_transaction 对附表余额有真实写入，但未取得本次适用的金融单位。旧整类未检出变为 source_unit_missing，风险端两次都算 FN。纠正了过强的阴性范围，尚未恢复风险命中。

本批具体依据：账本单位缺少依据。

配对成员 [RQ1_8d60a47186e2](Cases_18.md#rq1_8d60a47186e2)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 未知 / 有效未检出 / 未知。

原 25 对源码复核（旧轮次的观察）：03　7d7240a2af90 / 8d60a47186e2　N/N，Q0，C，明确纠正原归因。IntegerOverflowAdd 第7行普通 transfer 使用 balanceOf；第24行 zero_fee_transaction 使用 balances_test，角色条件内联在第25行。原程序记录在第7行给 source_check_excluded，而第24行的问题无类别、scope_missing，TRANSFER基本覆盖却为 source_task_reading。保存的 financial_right 绑定 balanceOf。保留第7行的局部排除；给第24行的余额候选独立的单位判断。修复第24行去角色门。不能把第7行的结果当作已核特权账本。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.2 → 0.3 秒，本批剩余动作 0。

## RQ1_fbd0377ce541

第 115 份 · FCR-PAUSE 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_fbd0377ce541.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_8e8598bb724e](Cases_20.md#rq1_8e8598bb724e)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：不可用 → 可用。实际求解 0 → 3 次，程序用时 0.6 → 0.8 秒，本批剩余动作 0。

## RQ1_39fb6e7197c4

第 116 份 · FCR-FREEZE 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_39fb6e7197c4.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_7450d39da940](Cases_20.md#rq1_7450d39da940)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

原 25 对源码复核（旧轮次的观察）：25　39fb6e7197c4 / 7450d39da940　U/U，Q3，B（局部）。ETJ 实际入口第115、136行；派生helper第221行，第231、234行读冻结，第252行setter可写。修复setter在第236行。指定作用可作同范围排除；最终整类的其他未决须另看，不应用本地排除自动置阴性。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 3 → 0 次，程序用时 1.2 → 1.0 秒，本批剩余动作 0。

## RQ1_9451d6dac4de

第 117 份 · FCR-TRANSFER 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_9451d6dac4de.sol)

本批具体依据：zero_fee_transaction(address,address,uint256) 第 22 行，适用的程序性质给出正证（E1、E12、E15、E16、E5、E8，同性质查询 local_premises_feasible/sat, direct_effect/sat, direct_effect/unsat）

配对成员 [RQ1_e25d32acc1f7](Cases_14.md#rq1_e25d32acc1f7)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 有效未检出 / 报警 / 报警 / 未知 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 9 → 9 次，程序用时 0.7 → 0.7 秒，本批剩余动作 0。

## RQ1_353a9b0b5006

第 118 份 · FCR-DESTROY 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_353a9b0b5006.sol)

给费率赋值与真实销毁并非同一件事；名为 burn 的操作增加余额及供应。指定 DESTROY 仍缺少适用的持有人同意依据，不能单凭函数名报告，亦不能由此关闭其他扣款路径。

本批具体依据：持有人同意适用于毛额还是净额未决。

配对成员 [RQ1_db11e3e08742](Cases_17.md#rq1_db11e3e08742)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 报警 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

原 25 对源码复核（旧轮次的观察）：15　353a9b0b5006 / db11e3e08742　U/U，Q168，C。Token 第166行的费率控制两端都在。风险 transferFrom 第315–345行、修复第296–345行均先扣发送人gross，再从金额变量减慈善与销毁部分；接收人先得net、再得慈善部分（尽管事件另写慈善地址），供应按burn减少，后用net检查、扣同一额度。不同主体、无算术失败的分支上，接收人总入账为gross减burn。该入账既不能自动补偿发送人，也不能抹去有同意的有效转付。需核主体别名、取整、参数限制、交易最终提交、实际同意的基数及是否有有效授予，不能强设全协议gross公理；风险第471行名为burn的函数反而增加余额与供应，修复删除它不能解释费用主张消失。原记录有 net_request_with_fee，但 SetBurnPercent 的DESTROY覆盖仍为 holder_consent_basis_unresolved；证据不足以重写参考。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 215 → 375 次，程序用时 115.6 → 296.3 秒，本批剩余动作 86。

## RQ1_72c6b8c6b605

第 119 份 · FCR-TRANSFER 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_72c6b8c6b605.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_b5217318672e](Cases_18.md#rq1_b5217318672e)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 6 → 5 次，程序用时 0.4 → 0.3 秒，本批剩余动作 0。

## RQ1_86a0269d7608

第 120 份 · FCR-MINT 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_86a0269d7608.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_a0facbcc1e38](Cases_20.md#rq1_a0facbcc1e38)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：不可用 → 可用。实际求解 0 → 6 次，程序用时 4.1 → 4.7 秒，本批剩余动作 0。

