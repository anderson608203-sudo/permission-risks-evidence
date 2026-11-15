# 成员 101–110

[200 份索引](Index.md) · [本组结构化证据](Trace_11.json)

## RQ1_e1ce695fff9e

第 101 份 · FCR-DESTROY 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_e1ce695fff9e.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_bcafc7a40ce2](Cases_18.md#rq1_bcafc7a40ce2)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 6 → 0 次，程序用时 0.4 → 2.3 秒，本批剩余动作 0。

## RQ1_c9626779c857

第 102 份 · FCR-DESTROY 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_c9626779c857.sol)

本批具体依据：burnFrom(address,uint256) 第 123 行，适用的程序性质给出正证（E10、E19、E2、E20、E6、E9，同性质查询 local_premises_feasible/sat, direct_effect/sat, financial_value_post_exclusion/unsat, same_request_amount_change/unsat）

配对成员 [RQ1_085aaca2f412](Cases_09.md#rq1_085aaca2f412)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警。

本批其他类别还报出 FCR-FREEZE，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 8 → 12 次，程序用时 1.4 → 4.5 秒，本批剩余动作 0。

## RQ1_c75d73e1c482

第 103 份 · FCR-MINT 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_c75d73e1c482.sol)

本批具体依据：mintToken(address,uint256) 第 200 行，受控受益人的新增权益（E14）

配对成员 [RQ1_35e0e8d95f92](Cases_14.md#rq1_35e0e8d95f92)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 未知 / 报警 / 报警 / 报警 / 报警。

本批其他类别还报出 FCR-TRANSFER, FCR-FREEZE，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 263 → 281 次，程序用时 204.3 → 233.7 秒，本批剩余动作 15。

## RQ1_e73c99ca23e5

第 104 份 · FCR-TRANSFER 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_e73c99ca23e5.sol)

本批具体依据：zero_fee_transaction(address,address,uint256) 第 178 行，existing_rights_moved（E3）；zero_fee_transaction(address,address,uint256) 第 178 行，existing_rights_moved（E20）；zero_fee_transaction(address,address,uint256) 第 178 行，existing_rights_moved（E14）

配对成员 [RQ1_1f06ce07140f](Cases_13.md#rq1_1f06ce07140f)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警。

本批其他类别还报出 FCR-DESTROY, FCR-PAUSE，单独记录。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 57 → 38 次，程序用时 14.3 → 16.5 秒，本批剩余动作 0。

指定类结果稳定，但报警理由由 适用的程序性质给出正证 变为 existing_rights_moved。

## RQ1_c772c59e4a76

第 105 份 · FCR-FREEZE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_c772c59e4a76.sol)

本批具体依据：freezeAccount(address,bool) 第 207 行，适用的程序性质给出正证（E20、E21、E22、E23、E31、E32，同性质查询 control_transition_preservation/sat, baseline_usable/sat, financial_block/unsat, financial_block/sat）

配对成员 [RQ1_a7bf9487cc3f](Cases_10.md#rq1_a7bf9487cc3f)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 未知 / 未知 / 报警 / 报警 / 报警 / 报警 / 报警。

本批其他类别还报出 FCR-MINT，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 254 → 251 次，程序用时 299.1 → 257.7 秒，本批剩余动作 39。

## RQ1_32dbc2fa2433

第 106 份 · FCR-PAUSE 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_32dbc2fa2433.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_c24c6c95ccbd](Cases_10.md#rq1_c24c6c95ccbd)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 11 → 0 次，程序用时 0.7 → 2.5 秒，本批剩余动作 0。

## RQ1_94d9f2cfc77c

第 107 份 · FCR-MINT 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_94d9f2cfc77c.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果、已有任务阅读记录。

配对成员 [RQ1_e13bb6580d65](Cases_19.md#rq1_e13bb6580d65)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 6 → 6 次，程序用时 3.6 → 7.3 秒，本批剩余动作 0。

## RQ1_4169c528c5e4

第 108 份 · FCR-MINT 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_4169c528c5e4.sol)

本批具体依据：mintToken(address,uint256) 第 201 行，受控受益人的新增权益（E10）

配对成员 [RQ1_2d22977434b5](Cases_15.md#rq1_2d22977434b5)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 未知 / 报警 / 报警 / 报警 / 报警。

本批其他类别还报出 FCR-TRANSFER, FCR-FREEZE，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 不可用。实际求解 186 → 291 次，程序用时 299.4 → 282.3 秒，本批剩余动作 0。

## RQ1_475c7d9ec738

第 109 份 · FCR-PAUSE 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_475c7d9ec738.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_b84042e6eefd](Cases_17.md#rq1_b84042e6eefd)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.2 → 2.6 秒，本批剩余动作 0。

## RQ1_30c29cd44cad

第 110 份 · FCR-DESTROY 风险 · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_30c29cd44cad.sol)

上批同一类别的原始依据为 依赖未能闭合的外部行为、账本单位缺少依据。 下方列出本批依据。

本批具体依据：destroy(address,uint256) 第 47 行，持有人权益扣减且未见同人补偿（E1、E2）

配对成员 [RQ1_329e0d0d7a11](Cases_15.md#rq1_329e0d0d7a11)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 未知 / 报警 / 未知 / 未知 / 未知 / 报警。

原 25 对源码复核（旧轮次的观察）：11　30c29cd44cad / 329e0d0d7a11　U/U，Q11，C。BANK_SAFE.destroy 两端第43行。已采纳支持集中在资格、初始化、政策与转移条件；其他操作上的调查没有核定这笔账户扣减的单位。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 8 → 0 次，程序用时 0.5 → 2.5 秒，本批剩余动作 0。

