# FCR 逐例复核 · 第 10 页

[返回成员索引](CaseIndex.md)

## RQ1_0f3c3f400f6f

FREEZE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_5b3c7cbe3d9d](FCR_05.md#rq1_5b3c7cbe3d9d)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 28 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | addSaleOwner(address) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×61。本次：open/relevant_source_scope_without_resolved_property×27、excluded/compiler_generated_readonly_getter×25、excluded/committed_exits_have_no_state_or_external_effect×8、open/decisive_property_or_source_residual×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 69 项调查动作、18 条查询记录（sat×17、unsat×1），底层求解 19 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_4c12c43fc10ba05f1bea`，baseline_usable → sat，条件摘要 `1ae99b8a1770f5f7346f3dad4755d3270790563b3ecc8163aaf4d240754432f2`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4540/10512 | b7c6622e08b2 | f895e3543532 |
| main/1 | focused_revision | stop/analysis_received | 6525/6335 | ef9d6ef02a21 | d4999cb92c17 |



选定来源：main；报告 SHA-256 `5af3d042ad89a83cc5c7070488fe38130d298f3c4021d24c4d3e649569b8b25f`；报告位于原归档 `run/members/RQ1_0f3c3f400f6f/attempt_1/analysis/report.json`。

## RQ1_cea156e41c29

PAUSE · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_d695cf0bad2e](FCR_02.md#rq1_d695cf0bad2e)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | disableTransfers(bool) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×8、decisive_property_or_source_residual×1、source_positions_and_resolved_properties×1。本次：open/relevant_source_scope_without_resolved_property×4、excluded/committed_exits_have_no_state_or_external_effect×3、excluded/compiler_generated_readonly_getter×2、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：sat×2、unsat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_e7891db706a66789424a | FCR-PAUSE | disableTransfers(bool)@923 | property_b0d2a27114ed18458d73 | E2,E5,E7 |



该成员共 2 次真实提交；选定报告登记 10 项调查动作、9 条查询记录（unsat×5、sat×4），底层求解 6 次。反馈登记消费 1 行；检查点类别 FCR-PAUSE×1，最终类别 FCR-PAUSE×1。

可核对的检查示例：`probe_17780f184a19d6ec2dd2`，control_transition_preservation → unsat，条件摘要 `ed0482655b7baf30bc0bfbcf774d40e17b00593433773379b93e12da25b49a3c`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1915/8224 | 015d9ef53825 | 177dfb8a8362 |
| main/1 | focused_revision | stop/analysis_received | 2815/2189 | 9c4331fcae3e | b81a4757b6ea |



选定来源：main；报告 SHA-256 `7c68aed1c6289e45a681245232c1e974212c1e0353f6fc5d7d9c2b0023199399`；报告位于原归档 `run/members/RQ1_cea156e41c29/attempt_1/analysis/report.json`。

## RQ1_fe11616caf66

TRANSFER · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_6476444da7e8](FCR_08.md#rq1_6476444da7e8)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | supported | — |
| i2 | zero_fee_transaction(address,address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×2、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×1、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：sat×6、unsat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_a4185a53f0253e5250f9 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@463 | property_8715f4afb7a77db3e4c1 | E2,E6 |
| finding_6c3fbba6f6388f635be0 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@463 | property_980b4eba4c3dbba96265 | E1,E4 |



该成员共 2 次真实提交；选定报告登记 6 项调查动作、8 条查询记录（sat×6、unsat×2），底层求解 3 次。反馈登记消费 1 行；检查点类别 FCR-TRANSFER×2，最终类别 FCR-TRANSFER×2。

可核对的检查示例：`probe_8ad33e66cb8a2189d7ec`，local_premises_feasible → sat，条件摘要 `2e2656458349a5929dac5392f5910f52ca2d2d69f14c472c6a7bf1b08a6f5e8e`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1537/10506 | 020e555ddd2a | 6645cbe63d3a |
| main/1 | focused_revision | stop/analysis_received | 5092/3940 | 20656667e327 | 107feba2691a |



选定来源：main；报告 SHA-256 `661a65fa266aa3db58b503781e0b9fb2e44f7c97594f7804d31a9d5e87da7e2e`；报告位于原归档 `run/members/RQ1_fe11616caf66/attempt_1/analysis/report.json`。

## RQ1_0bf6f8bce8d9

DESTROY · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_196284e657b0](FCR_04.md#rq1_196284e657b0)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 4 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | destroy(address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |
| i2::FCR-DESTROY | destroy(address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |


前批指定类义务依据：source_effect_and_privilege_relevance×9。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×3、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 18 项调查动作、1 条查询记录（sat×1），底层求解 1 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_a5cb39fdb4d6c7107e22`，original_path_commit → sat，条件摘要 `d6cecdc7c51ea943643a816b1159c7e16f9b049bcf81da23ec4c8da4eb990939`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2115/9227 | 524ef46bfdbb | 10c47c689db6 |
| main/1 | focused_revision | stop/analysis_received | 3209/2353 | f7cef46759e1 | dd6048a3821f |



选定来源：main；报告 SHA-256 `77f94635677ed1f778f33d9adc5d03b3461e19da62dbae618fa525cb970e2643`；报告位于原归档 `run/members/RQ1_0bf6f8bce8d9/attempt_1/analysis/report.json`。

## RQ1_8d60a47186e2

TRANSFER · 修复端。检测状态：TN。前批 → 本批：有效未检出 → 有效未检出。配对成员 [RQ1_7d7240a2af90](FCR_04.md#rq1_7d7240a2af90)。

本轮已选输出 有效未检出；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

这份修复端的 TRANSFER 是本轮唯一指定类别有效阴性。对应的排除理由属于实际直接效果不可行，不能推广到其余未知修复端。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |
| i2 | transfer(address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |


前批指定类义务依据：source_effect_and_privilege_relevance×4。本次：excluded/compiler_generated_readonly_getter×2、excluded/source_positions_and_resolved_properties×2。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 5 项调查动作、0 条查询记录（无），底层求解 0 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：无已保存的程序查询。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1580/9625 | 2fc884914969 | 83fc87c3810d |
| main/1 | focused_revision | stop/analysis_received | 2671/985 | e7f5690b77d7 | 7bee3d855b7b |



选定来源：main；报告 SHA-256 `17596355bc6aab058eb3691eec416c8222de353fc038c07e2d9eccc354be8309`；报告位于原归档 `run/members/RQ1_8d60a47186e2/attempt_1/analysis/report.json`。

## RQ1_bcafc7a40ce2

DESTROY · 风险端。检测状态：TP。前批 → 本批：未知 → 检出。配对成员 [RQ1_e1ce695fff9e](FCR_03.md#rq1_e1ce695fff9e)。

本轮已选输出 检出；前次同 200 份 未知；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类初始未出现，最终已形成发现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | destroy(address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×8、decisive_property_or_source_residual×1。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×2、excluded/committed_exits_have_no_state_or_external_effect×1、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：sat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_ccc50d05dd0045ee98a8 | FCR-DESTROY | destroy(address,uint256)@1047 | property_f012bb3f3a0a0ae0cf1e | E14,E15,E3,E8 |



该成员共 2 次真实提交；选定报告登记 15 项调查动作、7 条查询记录（sat×6、unsat×1），底层求解 8 次。反馈登记消费 1 行；检查点类别 无，最终类别 FCR-DESTROY×1。

可核对的检查示例：`probe_c84f4da3a0ab0bfd1c4d`，local_premises_feasible → sat，条件摘要 `40573cea1685ffbd714368bdc5c13087d9cd13cc552bfd91d20f9832cdca69d2`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1850/15821 | bb2fe461b7cf | d3980e1261ae |
| main/1 | focused_revision | stop/analysis_received | 2319/5294 | 54d37ac5304a | deba22ad1a07 |



选定来源：main；报告 SHA-256 `f2993733059fd271e5eebfcdb792de89eda10b541b42bbeec15f3e9fbdabab00`；报告位于原归档 `run/members/RQ1_bcafc7a40ce2/attempt_1/analysis/report.json`。

## RQ1_b5217318672e

TRANSFER · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_72c6b8c6b605](FCR_04.md#rq1_72c6b8c6b605)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类初始未出现，最终已形成发现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i3 | zero_fee_transaction(address,address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×8、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×2、excluded/committed_exits_have_no_state_or_external_effect×1、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：sat×3、unsat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_5b06edfde0e6a7ef4f0b | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@801 | property_088a044e79f56dab4de2 | E5,E8,E9 |



该成员共 2 次真实提交；选定报告登记 9 项调查动作、6 条查询记录（sat×5、unsat×1），底层求解 5 次。反馈登记消费 1 行；检查点类别 无，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_97455a9848b9bc0dd03a`，local_premises_feasible → sat，条件摘要 `1160dc1225fc09d10f1bf9aad992e67a5db53e555919d572cacdb62daaf4c61a`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1941/12643 | c2da80fa1e29 | eac7172580fd |
| main/1 | focused_revision | stop/analysis_received | 2474/6535 | f3e74f0e6cfa | a53cb43faff8 |



选定来源：main；报告 SHA-256 `b1f0cba2d66197e63b696d189ea80202930f7143795e813087282717ce78b748`；报告位于原归档 `run/members/RQ1_b5217318672e/attempt_1/analysis/report.json`。

## RQ1_b731957fa974

MINT · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_4968e56244c9](FCR_08.md#rq1_4968e56244c9)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2@8e89afcce351::FCR-MINT | batchTransfer(address[],uint256) | 未确认 | financial_property_conditions_not_established |
| i2@935a2911126d::FCR-MINT | batchTransfer(address[],uint256) | 未确认 | financial_property_conditions_not_established |
| i4@25c714cf1b4a | issue(address,uint256) | supported | — |
| i4@8e89afcce351 | issue(address,uint256) | supported | — |
| i4@935a2911126d | issue(address,uint256) | supported | — |
| i4@977b12483c58 | issue(address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×49、source_positions_and_resolved_properties×4。本次：excluded/compiler_generated_readonly_getter×19、open/relevant_source_scope_without_resolved_property×17、excluded/committed_exits_have_no_state_or_external_effect×7、open/decisive_property_or_source_residual×5、excluded/source_positions_and_resolved_properties×4、excluded/all_extracted_exits_revert×1。与最终指定类性质标识严格相同的查询结果：sat×8。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_0db234f90ac6cb7369a9 | FCR-PAUSE | pause()@5166 | property_dc5fb97d0123aa8f5688 | E1,E15,E29,E3,E6 |
| finding_b2691d47a293f07cb70a | FCR-PAUSE | pause()@5166 | property_9969ae77cb0722138f7e | E17,E2,E31,E5,E7 |
| finding_c04ac838295ddf208893 | FCR-MINT | issue(address,uint256)@2047 | property_8919deab397e1e08dcb1 | E13,E27 |
| finding_1965ae81f9a01886c411 | FCR-MINT | issue(address,uint256)@2047 | property_e56a7842c32b2df00bac | E10,E24 |
| finding_beaabb8199ea6cd5f39a | FCR-MINT | issue(address,uint256)@2047 | property_93eb9820af43d04c489b | E11,E26 |
| finding_b8650d8e39d55e22b29a | FCR-MINT | issue(address,uint256)@2047 | property_84906769c195b9a98d9b | E20,E9 |



该成员共 2 次真实提交；选定报告登记 76 项调查动作、28 条查询记录（sat×22、unsat×6），底层求解 24 次。反馈登记消费 1 行；检查点类别 FCR-MINT×4、FCR-PAUSE×2，最终类别 FCR-MINT×4、FCR-PAUSE×2。

可核对的检查示例：`probe_baf5fb6653d03feb7796`，local_premises_feasible → sat，条件摘要 `e38835adc78e957a4410eb3437ff92007773580b10ef227f261962d00f207e34`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4569/15908 | 1c2900553d81 | 75ac7f4fe302 |
| main/1 | focused_revision | stop/analysis_received | 5601/1772 | 73ba9719527b | c9a7ab09b28a |



选定来源：main；报告 SHA-256 `e72b70d8edc0ce860be8b9f7d537ba6b36ed199ab6dfc960db2f2fa97f7b1182`；报告位于原归档 `run/members/RQ1_b731957fa974/attempt_1/analysis/report.json`。

## RQ1_3a3d833ca142

TRANSFER · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_206d19a8539c](FCR_01.md#rq1_206d19a8539c)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类初始未出现，最终已形成发现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×3、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×2、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：sat×3、unsat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_ce96f89ea1310d4df66a | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@468 | property_919390697e581c778d11 | E3,E4,E5,E6 |



该成员共 2 次真实提交；选定报告登记 6 项调查动作、4 条查询记录（sat×3、unsat×1），底层求解 3 次。反馈登记消费 1 行；检查点类别 无，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_24e0fb95820f5c963e4d`，local_premises_feasible → sat，条件摘要 `d82f17ebcec5faa941d250c38f32678d2ef5e12774d4523c2450fc147010d8cd`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1551/5084 | 8d9e878cf83a | 38681ae3598e |
| main/1 | focused_revision | stop/analysis_received | 2066/3158 | 682938152666 | 5237b59e313d |



选定来源：main；报告 SHA-256 `cb7d02f00ad2136e720cb43951e690649fff430995a335fd8e2126a41ea5743b`；报告位于原归档 `run/members/RQ1_3a3d833ca142/attempt_1/analysis/report.json`。

## RQ1_aaeb3f57cfd0

PAUSE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_20dfd0c54b94](FCR_11.md#rq1_20dfd0c54b94)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

主批 KeyError；独立补充有报告，五类未知。反馈有意向记录，子账本显示未派发，零新增第三次请求。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i4 | transferEnable() | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×39。本次：excluded/compiler_generated_readonly_getter×21、open/relevant_source_scope_without_resolved_property×14、excluded/committed_exits_have_no_state_or_external_effect×4。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 72 项调查动作、154 条查询记录（unsat×126、sat×28），底层求解 57 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_37ca586f7c6f54b12dd1`，financial_value_post_exclusion → unsat，条件摘要 `2e1c2325a65e3db4fe8011612753f1e0f524181f43422b82a1120df511c00688`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3237/10613 | cf78a76c9c71 | 9af764f6ef03 |
| supplement/0 | initial | stop/analysis_received | 3237/8910 | cf78a76c9c71 | 93893849b1e1 |



选定来源：supplement；报告 SHA-256 `5fcd426abddfa5328af7be92d20758e7e167b54cc5ea74d7b9be06d28930495e`；报告位于原归档 `run/technical_two/run/members/RQ1_aaeb3f57cfd0/attempt_1/analysis/report.json`。
