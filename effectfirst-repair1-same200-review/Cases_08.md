# 成员 71–80

[200 份索引](Index.md) · [本组结构化证据](Trace_08.json)

## RQ1_2be3e9b98fac

第 71 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_2be3e9b98fac.sol)

本批具体依据：IstriumToken(address) 第 25 行，资格取得与受保护用途对应（E1、E21，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:30:author:1 IstriumToken|命中|命中|命中|命中|命中|授权政策缺失|

本批实际报警裁决：IstriumToken(address) D2:30:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 7 → 11 次，程序用时 0.6 → 3.6 秒，本批剩余动作 0。

## RQ1_a533300b98f5

第 72 份 · AC  · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_a533300b98f5.sol)

上批同一类别的原始依据为 授权政策缺失。 下方列出本批依据。

本批具体依据：die() 第 4 行，unrestricted_termination_decision（E1）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:539:author:1 die|漏检|命中|漏检|漏检|命中|已判断对应效果|

本批实际报警裁决：die() D2:539:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 0.1 → 2.5 秒，本批剩余动作 0。

## RQ1_be17ecaef698

第 73 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_be17ecaef698.sol)

本批具体依据：授权政策缺失、依赖未能闭合的外部行为。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:597:author:1 clearBlockchain|漏检|漏检|命中|漏检|漏检|授权政策缺失|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 1，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 不可用。实际求解 20 → 25 次，程序用时 1.5 → 6.7 秒，本批剩余动作 0。

## RQ1_0bcbefea1890

第 74 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_0bcbefea1890.sol)

本批具体依据：selfdestructs() 第 120 行，unrestricted_termination_decision（E3）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:614:S1 selfdestructs|命中|命中|命中|命中|命中|已判断对应效果|

本批实际报警裁决：selfdestructs() D2:614:S1。

参考外组数（组 ID 跨方法不可直接等同）：v32 2，b5 0，最近全量 2。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 9 → 8 次，程序用时 1.3 → 5.3 秒，本批剩余动作 0。

## RQ1_c20b10d094d5

第 75 份 · AC  · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_c20b10d094d5.sol)

上批同一类别的原始依据为 授权政策缺失。 下方列出本批依据。

本批具体依据：ETHERanate() 第 24 行，资格取得与受保护用途对应（E1、E8）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:50:author:1 ETHERanate|命中|命中|命中|漏检|命中|已判断对应效果|

本批实际报警裁决：ETHERanate() D2:50:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 6 → 105 次，程序用时 31.5 → 269.5 秒，本批剩余动作 0。

## RQ1_4f19278de7d5

第 76 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_4f19278de7d5.sol)

本批具体依据：依赖未能闭合的外部行为、授权政策的范围缺少依据、授权政策缺失。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:181:author:1 init|漏检|漏检|漏检|漏检|漏检|依赖未能闭合的外部行为、该范围无对应效果|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 2 → 30 次，程序用时 2.4 → 8.3 秒，本批剩余动作 0。

## RQ1_b6fc6e31e760

第 77 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_b6fc6e31e760.sol)

本批具体依据：授权政策的范围缺少依据、依赖未能闭合的外部行为。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:537:original:1 payout|命中|命中|命中|漏检|漏检|授权政策的范围缺少依据|
|D2:537:original:2 payoutSelf|漏检|命中|命中|漏检|漏检|授权政策的范围缺少依据|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：可用 → 可用。实际求解 75 → 76 次，程序用时 107.5 → 145.4 秒，本批剩余动作 0。

## RQ1_852d7abd1772

第 78 份 · AC  · 上批 未知 → 本批 **未知**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_852d7abd1772.sol)

本批具体依据：依赖未能闭合的外部行为。

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:321:author:1 withdrawTokens|漏检|漏检|漏检|漏检|漏检|无可定位的该入口覆盖记录|

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：未知 → 未知 → 未知 → 未知。上批至本批的模型分析：不可用 → 不可用。实际求解 0 → 0 次，程序用时 1.7 → 89.5 秒，本批剩余动作 0。

## RQ1_9fea8632716d

第 79 份 · AC  · 上批 报警 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_9fea8632716d.sol)

本批具体依据：Ballot(uint8) 第 16 行，资格取得与受保护用途对应（E1、E10、E17，同性质查询 local_premises_feasible/sat, authorization_violation/sat）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:510:author:1 Ballot|命中|命中|命中|命中|命中|授权政策缺失|

本批实际报警裁决：Ballot(uint8) D2:510:author:1。

参考外组数（组 ID 跨方法不可直接等同）：v32 1，b5 0，最近全量 0。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：不可用 → 可用。实际求解 2 → 16 次，程序用时 0.6 → 6.1 秒，本批剩余动作 0。

## RQ1_34ab8e0115aa

第 80 份 · AC  · 上批 未知 → 本批 **报警**。 [实际合约源码](https://github.com/anderson608203-sudo/permission-risks-evidence/blob/9a43eacf7cb8ea74903736b53cfb8216a9a3806f/same200-contract-inputs/AC80/RQ1_34ab8e0115aa.sol)

上批同一类别的原始依据为 依赖未能闭合的外部行为、授权政策缺失。 下方列出本批依据。

本批具体依据：destroy() 第 189 行，unrestricted_termination_decision（E3）

|独立参考及入口|v32|b5|最近全量|上批|本次|本次在该入口的依据|
|---|---|---|---|---|---|---|
|D2:359:S1 PonziTokenV3|漏检|命中|命中|漏检|漏检|已有任务阅读记录|
|D2:359:S2 destroy|命中|命中|命中|漏检|命中|已判断对应效果|

本批实际报警裁决：destroy() D2:359:S2。

参考外组数（组 ID 跨方法不可直接等同）：v32 0，b5 1，最近全量 1。

基本、初始、若已保存的反馈后、最终检查点：报警 → 报警 → 报警 → 报警。上批至本批的模型分析：可用 → 可用。实际求解 0 → 0 次，程序用时 1.6 → 19.8 秒，本批剩余动作 0。

