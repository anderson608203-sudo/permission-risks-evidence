# 成员 141–150

[200 份索引](Index.md) · [本组结构化证据](Trace_15.json)

## RQ1_18c85d7f1380

第 141 份 · FCR-MINT 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_18c85d7f1380.sol)

本批具体依据：mintToken(address,uint256) 第 198 行，受控受益人的新增权益（E3）

配对成员 [RQ1_983137cbe5d6](Cases_19.md#rq1_983137cbe5d6)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 报警 / 报警 / 报警 / 未知 / 报警 / 报警 / 报警 / 报警。

本批其他类别还报出 FCR-FREEZE，单独记录。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 286 → 274 次，程序用时 260.3 → 265.4 秒，本批剩余动作 40。

## RQ1_55a1e2ef0f09

第 142 份 · FCR-DESTROY 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_55a1e2ef0f09.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_fe4ace2cd8e5](Cases_17.md#rq1_fe4ace2cd8e5)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 报警 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知 / 未知。

本批其他类别还报出 FCR-MINT，单独记录。

原 25 对源码复核（旧轮次的观察）：13　55a1e2ef0f09 / fe4ace2cd8e5　U/U，Q42，B（局部）。FuelToken.finalizePresale 第360行分配未用额度；finalizeCrowdfund 第379–401行在清算阶段由众筹地址调用，清其余额并等额记入平台。修复第338、354行等处放开权限。所读金额既有来源也有明确去向，不能直接推出毁损别的持有人权益；也不能把平台收款写成本人补偿。不同托管受益人或独立挪用主张需要另外的义务依据。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 91 → 88 次，程序用时 31.4 → 42.8 秒，本批剩余动作 64。

## RQ1_2d22977434b5

第 143 份 · FCR-MINT 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_2d22977434b5.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_4169c528c5e4](Cases_11.md#rq1_4169c528c5e4)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

本批其他类别还报出 FCR-TRANSFER，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 171 → 201 次，程序用时 188.1 → 221.6 秒，本批剩余动作 0。

## RQ1_4febca8bfe3b

第 144 份 · FCR-TRANSFER 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_4febca8bfe3b.sol)

本批具体依据：zero_fee_transaction(address,address,uint256) 第 25 行，existing_rights_moved（E2）

配对成员 [RQ1_49db443acf1d](Cases_12.md#rq1_49db443acf1d)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 未知 / 报警 / 未知 / 报警 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 3 → 0 次，程序用时 0.3 → 2.6 秒，本批剩余动作 0。

指定类结果稳定，但报警理由由 适用的程序性质给出正证 变为 existing_rights_moved。

## RQ1_3455b6a9ba4f

第 145 份 · FCR-TRANSFER 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_3455b6a9ba4f.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_0c666ce785e8](Cases_09.md#rq1_0c666ce785e8)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 6 → 0 次，程序用时 0.4 → 2.6 秒，本批剩余动作 0。

## RQ1_3b4d9f6eb96f

第 146 份 · FCR-MINT 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_3b4d9f6eb96f.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_0267e2a8ebb2](Cases_09.md#rq1_0267e2a8ebb2)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

本批其他类别还报出 FCR-TRANSFER，单独记录。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 149 → 195 次，程序用时 115.3 → 216.7 秒，本批剩余动作 4。

## RQ1_53f9777ccdf6

第 147 份 · FCR-TRANSFER 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_53f9777ccdf6.sol)

本批具体依据：zero_fee_transaction(address,address,uint256) 第 38 行，existing_rights_moved（E1）

配对成员 [RQ1_a7d72c1e4129](Cases_16.md#rq1_a7d72c1e4129)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 有效未检出 / 未知 / 报警 / 未知 / 未知 / 报警 / 报警。

原 25 对源码复核（旧轮次的观察）：02　53f9777ccdf6 / a7d72c1e4129　U/U，Q11，C。PERSONAL_BANK 同入口两端第33行；修复保留同量转移。已有资格、阶段、条件支持，三个判断未形成该TRANSFER。银行初始化时间不能顶替测试账本的单位。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 不可用。实际求解 9 → 0 次，程序用时 0.6 → 2.8 秒，本批剩余动作 0。

指定类结果稳定，但报警理由由 适用的程序性质给出正证 变为 existing_rights_moved。

## RQ1_eb30c6dee989

第 148 份 · FCR-DESTROY 风险 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_eb30c6dee989.sol)

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_ee2aa7f32d31](Cases_17.md#rq1_ee2aa7f32d31)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 有效未检出 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

原 25 对源码复核（旧轮次的观察）：14　eb30c6dee989 / ee2aa7f32d31　U/U，Q47，B（局部）。Dragon.burnDragons 两端第110行。风险版只有 burner 可调用，但第117–125行扣的是调用者本人余额，并有供应底限；修复移去入口角色门。独立 burnFrom 有其授权条件。本人销毁不能作为“特权毁损别人”的阳性，别处引入回调也不能倒推此函数扣了第三人账。 [逐对现状](FCR25.json)

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 7 → 0 次，程序用时 2.0 → 5.1 秒，本批剩余动作 0。

## RQ1_4f9f1ce04ed8

第 149 份 · FCR-PAUSE 风险 · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-risk60/RQ1_4f9f1ce04ed8.sol)

本批具体依据：disableTransfers(bool) 第 37 行，控制变化能阻断普通正额转出（E3、E5、E6）

配对成员 [RQ1_b0a696b11b0a](Cases_14.md#rq1_b0a696b11b0a)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 报警 / 有效未检出 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警 / 报警。

基本、初始、若已保存的反馈后、最终检查点：未知 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 10 → 10 次，程序用时 0.7 → 2.7 秒，本批剩余动作 0。

## RQ1_329e0d0d7a11

第 150 份 · FCR-DESTROY 修复 · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/FCR-repair60/RQ1_329e0d0d7a11.sol)

 指定类修复端仍未形成有效阴性，本对不能据此记正确。

本批具体依据：依赖未能闭合的外部行为。

配对成员 [RQ1_30c29cd44cad](Cases_11.md#rq1_30c29cd44cad)。同一指定类的 v32 / 旧主批 b5 / 最近全量 / 早前 Full200 / Decision-only / 协议版 / 73a4 / 上次同 200 / 本次依次为 有效未检出 / 有效未检出 / 未知 / 有效未检出 / 未知 / 未知 / 未知 / 未知 / 未知。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 4 → 0 次，程序用时 0.3 → 2.3 秒，本批剩余动作 0。

