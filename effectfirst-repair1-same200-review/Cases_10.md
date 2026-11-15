# 成员 91–100

[200 份索引](Index.md) · [本组结构化证据](Trace_10.json)

## RQ1_c24c6c95ccbd

第 91 份 · FCR-PAUSE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_c24c6c95ccbd.sol)

本批具体依据：disableTransfers(bool) 第 62 行，控制变化能阻断普通正额转出（E2、E3、E4）

配对成员 [RQ1_32dbc2fa2433](Cases_11.md#rq1_32dbc2fa2433)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 未知 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 14 → 7 次，程序用时 1.0 → 2.7 秒，本批剩余动作 0。

## RQ1_b61f163309a1

第 92 份 · FCR-MINT 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_b61f163309a1.sol)

本批具体依据：allocateToken(address,uint256) 第 315 行，适用的程序性质给出正证（E11、E18、E19、E3、E57、E60，同性质查询 local_premises_feasible/sat, direct_effect/sat, financial_value_post_exclusion/unsat, same_request_amount_change/unsat, financial_value_post_exclusion/sat, financial_value/unsat）；setTokenExchangeRate(uint256) 第 156 行，适用的程序性质给出正证（E14、E65、E70、E75、E78、E80，同性质查询 financial_value_post_exclusion/sat, financial_value/sat, financial_value/unsat）

配对成员 [RQ1_81a85f242b60](Cases_13.md#rq1_81a85f242b60)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 未知 / 报警 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 70 → 82 次，程序用时 16.9 → 27.7 秒，本批剩余动作 11。

## RQ1_776a6b98d18f

第 93 份 · FCR-DESTROY 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_776a6b98d18f.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果、已有任务阅读记录。

配对成员 [RQ1_8456d2957fff](Cases_13.md#rq1_8456d2957fff)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：不可用 → 可用。实际求解 0 → 0 次，程序用时 0.0 → 2.1 秒，本批剩余动作 0。

## RQ1_a7bf9487cc3f

第 94 份 · FCR-FREEZE 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_a7bf9487cc3f.sol)

本批具体依据：已纳入局部阅读的义务依据含detached_local_holder_switch、在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_c772c59e4a76](Cases_11.md#rq1_c772c59e4a76)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 15 → 7 次，程序用时 3.0 → 6.0 秒，本批剩余动作 0。

## RQ1_46a031a993c1

第 95 份 · FCR-FREEZE 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_46a031a993c1.sol)

本批具体依据：已纳入局部阅读的义务依据含detached_local_holder_switch、在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_985c6fd1d4e4](Cases_14.md#rq1_985c6fd1d4e4)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.3 → 2.3 秒，本批剩余动作 0。

## RQ1_7a54127ed44c

第 96 份 · FCR-PAUSE 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_7a54127ed44c.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_4d2acebaa2ff](Cases_10.md#rq1_4d2acebaa2ff)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 22 → 29 次，程序用时 10.6 → 27.9 秒，本批剩余动作 0。

## RQ1_ffcaa562a72d

第 97 份 · FCR-PAUSE 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_ffcaa562a72d.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_c29df435681e](Cases_16.md#rq1_c29df435681e)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.3 → 2.7 秒，本批剩余动作 0。

## RQ1_4d2acebaa2ff

第 98 份 · FCR-PAUSE 风险 · 上批 报警 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_4d2acebaa2ff.sol)

上批同一类别的原始依据为 setTransfersPaused(bool) 第 555 行，控制变化能阻断普通正额转出（E19、E28、E37、E4、E44、E62，同性质查询 control_transition_preservation/sat, baseline_usable/sat, financial_block/unknown, financial_block/sat, control_transition_preservation/unsat） 下方列出本批依据。

本批具体依据：当前请求或效果范围未闭合、依赖未能闭合的外部行为。

配对成员 [RQ1_7a54127ed44c](Cases_10.md#rq1_7a54127ed44c)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 未知 / 未知 / 未知 / 未知 / 未知 / 报警 / 未知。

本批其他类别还报出 FCR-DESTROY，单独记录。

原 25 对源码复核（旧轮次的观察）：18　4d2acebaa2ff / 7a54127ed44c　U/U，Q6，A（缩窄到普通委托转出）。D100Token 第543–555行最后一次写入才是开关的实际值。直接 transfer 第650行有可执行onlyOwner，第675–676行还覆盖临时份额写入，不能作为普通持有人自由转出的基线。实际可比较的是第683–701行已有授权的 transferFrom、非豁免spender、有效份额换算和正额提交。transferAndCall 调实际 transfer；decreaseAllowance 第728行临时写开关后在738行又过owner门，普通人失败整笔回滚。修复移除setter，改写若干入口/账本。已知豁免或已授权豁免代理须按同权利核对，不能推广到所有账户都停转。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 393 → 241 次，程序用时 297.6 → 307.7 秒，本批剩余动作 169。

## RQ1_37d9daf031da

第 99 份 · FCR-PAUSE 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_37d9daf031da.sol)

本批具体依据：当前请求或效果范围未闭合、依赖未能闭合的外部行为、账本单位缺少依据。

配对成员 [RQ1_1c6b43b24d4c](Cases_19.md#rq1_1c6b43b24d4c)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 未知 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

原 25 对源码复核（旧轮次的观察）：17　37d9daf031da / 1c6b43b24d4c　U/U，Q308，A。RubusFundBlackToken 应用 Pausable.pause 第91–99行，普通 transfer 第168行、transferFrom 第262行均实际读取 !paused，在普通收款分支有实际扣/记余额，并保留余额、vesting和额度条件。第196/293行起的特殊赎回收款分支另有外调；该分支的回调不能否决普通收款分支。修复删除pause入口，仍有读取开关的转账。逐入口还原，连实际派生目标的pause/transfer都被记为PAUSE的 necessary_effect_absent，专项检查没有PAUSE；308项全在回调。优先修共同控制关系进入基本目录及调度；这不能单独证明每条原回调查询都无用。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 0 → 243 次，程序用时 192.5 → 310.9 秒，本批剩余动作 124。

## RQ1_d695cf0bad2e

第 100 份 · FCR-PAUSE 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_d695cf0bad2e.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_cea156e41c29](Cases_18.md#rq1_cea156e41c29)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：不可用 → 可用。实际求解 0 → 7 次，程序用时 0.1 → 2.5 秒，本批剩余动作 0。

