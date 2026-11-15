# 成员 151–160

[200 份索引](Index.md) · [本组结构化证据](Trace_16.json)

## RQ1_c29df435681e

第 151 份 · FCR-PAUSE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_c29df435681e.sol)

本批具体依据：disableTransfers(bool) 第 39 行，控制变化能阻断普通正额转出（E2、E3、E4）

配对成员 [RQ1_ffcaa562a72d](Cases_10.md#rq1_ffcaa562a72d)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 未知 / 有效未检出 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 7 → 7 次，程序用时 0.7 → 3.1 秒，本批剩余动作 0。

## RQ1_bc5855a83e2d

第 152 份 · FCR-MINT 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_bc5855a83e2d.sol)

本批具体依据：mint(address,uint256) 第 440 行，适用的程序性质给出正证（E10、E11、E22、E23、E24、E25，同性质查询 local_premises_feasible/sat, direct_effect/sat, financial_value_post_exclusion/unsat, same_request_amount_change/unsat）

配对成员 [RQ1_770ae395781c](Cases_09.md#rq1_770ae395781c)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 报警 / 未知 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 26 → 22 次，程序用时 5.7 → 10.6 秒，本批剩余动作 0。

## RQ1_c80f7a639e42

第 153 份 · FCR-FREEZE 风险 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_c80f7a639e42.sol)

本批具体依据：已纳入局部阅读的义务依据含detached_local_holder_switch、在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_30177d564271](Cases_19.md#rq1_30177d564271)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出。

本批其他类别还报出 FCR-MINT，单独记录。

原 25 对源码复核（旧轮次的观察）：24　c80f7a639e42 / 30177d564271　N/N，Q34，B。ERC20ext 应用 TokenERC20 第119、142行；派生helper第228行，冻结读取第241、244行，setter第262行。修复第243行仍有setter而helper约束被移除。两端在所读公开请求上均无此依赖，这项明确未检出有局部源码依据。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 33 → 38 次，程序用时 7.6 → 12.5 秒，本批剩余动作 0。

## RQ1_a7d72c1e4129

第 154 份 · FCR-TRANSFER 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_a7d72c1e4129.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_53f9777ccdf6](Cases_15.md#rq1_53f9777ccdf6)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 0 → 0 次，程序用时 0.1 → 2.4 秒，本批剩余动作 0。

## RQ1_15346457ba72

第 155 份 · FCR-DESTROY 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_15346457ba72.sol)

本批具体依据：destroy(address,uint256) 第 41 行，持有人权益扣减且未见同人补偿（E1）

配对成员 [RQ1_fe7add810da5](Cases_13.md#rq1_fe7add810da5)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 有效未检出 / 报警 / 报警。

原 25 对源码复核（旧轮次的观察）：07　15346457ba72 / fe7add810da5　N/N，Q0，C。GuessTheRandomNumberChallenge.destroy 两端第37行；风险第41–42行同时扣账户与供应。无可用模型分析、无专项检查。按义务ID还原后，necessary_effect_absent 属于 guess(uint8)；destroy 属于 source_task_reading。反驳“destroy已经被证实无必要效果”。非资产解释若有证据可以保留，模板未命中不能签发它。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 2 → 0 次，程序用时 0.2 → 2.2 秒，本批剩余动作 0。

## RQ1_6476444da7e8

第 156 份 · FCR-TRANSFER 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_6476444da7e8.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_fe11616caf66](Cases_18.md#rq1_fe11616caf66)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 不可用。实际求解 0 → 0 次，程序用时 0.2 → 2.1 秒，本批剩余动作 0。

## RQ1_dc06d7bad0d8

第 157 份 · FCR-FREEZE 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_dc06d7bad0d8.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_9c365cb18f95](Cases_16.md#rq1_9c365cb18f95)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 457 → 457 次，程序用时 321.6 → 300.4 秒，本批剩余动作 4。

## RQ1_9c365cb18f95

第 158 份 · FCR-FREEZE 风险 · 上批 报警 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_9c365cb18f95.sol)

上批同一类别的原始依据为 freeze(address,bool) 第 281 行，控制变化能阻断普通正额转出（E10、E12、E19、E44、E46、E48） 下方列出本批依据。

本批具体依据：依赖未能闭合的外部行为、当前请求或效果范围未闭合。

配对成员 [RQ1_dc06d7bad0d8](Cases_16.md#rq1_dc06d7bad0d8)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 未知。

本批其他类别还报出 FCR-PAUSE，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 123 → 115 次，程序用时 294.8 → 305.3 秒，本批剩余动作 44。

## RQ1_1f932eab663d

第 159 份 · FCR-FREEZE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_1f932eab663d.sol)

本批具体依据：freezeAccount(address,bool) 第 260 行，适用的程序性质给出正证（E10、E15、E6、E7、E9，同性质查询 control_transition_preservation/sat, baseline_usable/sat, financial_block/sat）

配对成员 [RQ1_43103f5773b9](Cases_19.md#rq1_43103f5773b9)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 20 → 12 次，程序用时 2.9 → 5.8 秒，本批剩余动作 0。

## RQ1_4968e56244c9

第 160 份 · FCR-MINT 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_4968e56244c9.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_b731957fa974](Cases_18.md#rq1_b731957fa974)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 报警 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 16 → 2 次，程序用时 2.8 → 6.9 秒，本批剩余动作 0。

