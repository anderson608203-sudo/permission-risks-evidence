# 成员 161–170

[200 份索引](Index.md) · [本组结构化证据](Trace_17.json)

## RQ1_fe4ace2cd8e5

第 161 份 · FCR-DESTROY 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_fe4ace2cd8e5.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_55a1e2ef0f09](Cases_15.md#rq1_55a1e2ef0f09)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 27 → 30 次，程序用时 7.3 → 7.6 秒，本批剩余动作 0。

## RQ1_1844e5d3d18e

第 162 份 · FCR-TRANSFER 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_1844e5d3d18e.sol)

本批具体依据：账本单位缺少依据、依赖未能闭合的外部行为。

配对成员 [RQ1_db73c28a69c2](Cases_20.md#rq1_db73c28a69c2)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 未知 / 未知 / 报警 / 报警 / 未知 / 未知 / 未知。

原 25 对源码复核（旧轮次的观察）：06　1844e5d3d18e / db73c28a69c2　U/U，Q6，C。Ownable 第29行声明，应用到 Ownable、Token、TokenBank。已保存的 financial_right 解析到 Token.originOwner。跨目标或从地址角色迁移金融解释到 balances_test 均无此依据。修复同源位置去掉角色门。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 7 → 0 次，程序用时 0.5 → 0.5 秒，本批剩余动作 0。

## RQ1_db11e3e08742

第 163 份 · FCR-DESTROY 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_db11e3e08742.sol)

配对修复端在费率、原额扣款和净额许可之间仍有适用同意问题。指定 DESTROY 保持未知。向第三方转付不能直接当本人补偿，冻结修复身份也不能决定程序应予排除。

本批具体依据：持有人同意适用于毛额还是净额未决。

配对成员 [RQ1_353a9b0b5006](Cases_12.md#rq1_353a9b0b5006)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 报警 / 未知 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

本批其他类别还报出 FCR-PAUSE，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 172 → 194 次，程序用时 121.6 → 299.3 秒，本批剩余动作 26。

## RQ1_a906c0b62c0b

第 164 份 · FCR-FREEZE 修复 · 上批 有效未检出 → 本批 **有效未检出**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_a906c0b62c0b.sol)

本批具体依据：已纳入局部阅读的义务依据含在该范围排除必要效果、该范围无对应效果。

配对成员 [RQ1_1a94f7866801](Cases_17.md#rq1_1a94f7866801)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 有效未检出 / 有效未检出。

基本、初始、若已保存的反馈后、最终检查点：有效未检出 → 有效未检出 → 有效未检出。上批至本批的模型分析：可用 → 可用。实际求解 3 → 17 次，程序用时 1.9 → 2.6 秒，本批剩余动作 0。

## RQ1_ee2aa7f32d31

第 165 份 · FCR-DESTROY 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_ee2aa7f32d31.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_eb30c6dee989](Cases_15.md#rq1_eb30c6dee989)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 14 → 14 次，程序用时 3.7 → 3.8 秒，本批剩余动作 0。

## RQ1_33d48945207e

第 166 份 · FCR-DESTROY 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_33d48945207e.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_6ca2b0aeda43](Cases_19.md#rq1_6ca2b0aeda43)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

原 25 对源码复核（旧轮次的观察）：12　33d48945207e / 6ca2b0aeda43　U/U，Q0，C。CREDITS 风险第196–225行。burn 减本人余额，burnFrom 减他人余额并检查和消费 allowance[holder][caller]；冻结modifier和内联冻结、日期条件仍约束风险版。修复第193、203行去该modifier，burnFrom仍保留日期、余额和同键额度。可肯定资格变化不自动越过额度；一般转账授权的业务用途是否包括让他人销毁，仍需独立依据。现有“effect_range_decided”不回答该规范问题。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 4.4 → 3.1 秒，本批剩余动作 0。

## RQ1_b84042e6eefd

第 167 份 · FCR-PAUSE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_b84042e6eefd.sol)

本批具体依据：disableTransfers(bool) 第 45 行，控制变化能阻断普通正额转出（E1、E3、E4）

配对成员 [RQ1_475c7d9ec738](Cases_11.md#rq1_475c7d9ec738)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 报警 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 12 → 7 次，程序用时 1.0 → 0.6 秒，本批剩余动作 0。

指定类结果稳定，但报警理由由 适用的程序性质给出正证 变为 控制变化能阻断普通正额转出。

## RQ1_1a94f7866801

第 168 份 · FCR-FREEZE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_1a94f7866801.sol)

本批具体依据：lockAddress(address,bool) 第 93 行，适用的程序性质给出正证（E26、E50、E57、E59、E7，同性质查询 control_transition_preservation/unsat, baseline_usable/sat, financial_block/unsat, financial_block/sat）；lockAddress(address,bool) 第 93 行，适用的程序性质给出正证（E45、E46、E5，同性质查询 control_transition_preservation/unsat, baseline_usable/sat, financial_block/unsat, financial_block/sat）；lockAddress(address,bool) 第 93 行，适用的程序性质给出正证（E20、E41、E70、E76、E77，同性质查询 control_transition_preservation/unsat, baseline_usable/sat, financial_block/unsat, financial_block/sat）；lockAddress(address,bool) 第 93 行，适用的程序性质给出正证（E14、E35、E60、E67、E69，同性质查询 control_transition_preservation/unsat, baseline_usable/sat, financial_block/unsat, financial_block/sat）；allowAddress(address,bool) 第 83 行，适用的程序性质给出正证（E30、E47、E52、E54、E9，同性质查询 control_transition_preservation/unsat, baseline_usable/sat, financial_block/unsat, financial_block/sat）；allowAddress(address,bool) 第 83 行，适用的程序性质给出正证（E16、E37、E55、E62、E64，同性质查询 control_transition_preservation/unsat, baseline_usable/sat, financial_block/unsat, financial_block/sat）；allowAddress(address,bool) 第 83 行，适用的程序性质给出正证（E24、E43、E65、E72、E74，同性质查询 control_transition_preservation/unsat, baseline_usable/sat, financial_block/unsat, financial_block/sat）；allowAddress(address,bool) 第 83 行，适用的程序性质给出正证（E2、E3、E6，同性质查询 control_transition_preservation/unsat, baseline_usable/sat, financial_block/unsat, financial_block/sat）

配对成员 [RQ1_a906c0b62c0b](Cases_17.md#rq1_a906c0b62c0b)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 报警 / 未知 / 报警 / 报警。

本批其他类别还报出 FCR-PAUSE，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 582 → 521 次，程序用时 109.5 → 99.7 秒，本批剩余动作 0。

## RQ1_af7c473b8cca

第 169 份 · FCR-MINT 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_af7c473b8cca.sol)

本批具体依据：mintToken(address,uint256) 第 201 行，受控受益人的新增权益（E3、E34，同性质查询 local_premises_feasible/sat, direct_effect/sat）

配对成员 [RQ1_4be3030c4533](Cases_09.md#rq1_4be3030c4533)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 未知 / 报警 / 报警 / 报警。

本批其他类别还报出 FCR-FREEZE，单独记录。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 138 → 269 次，程序用时 78.3 → 254.4 秒，本批剩余动作 59。

## RQ1_35f857af5c9e

第 170 份 · FCR-PAUSE 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_35f857af5c9e.sol)

本批具体依据：当前请求或效果范围未闭合。

配对成员 [RQ1_cda3df36df22](Cases_19.md#rq1_cda3df36df22)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：不可用 → 可用。实际求解 4 → 19 次，程序用时 0.6 → 3.1 秒，本批剩余动作 0。

