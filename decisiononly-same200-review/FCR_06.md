# FCR 逐例复核 · 第 6 页

[返回成员索引](CaseIndex.md)

## RQ1_024b9da10799

MINT · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_73b13298e227](FCR_06.md#rq1_73b13298e227)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 18 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×40。本次：excluded/committed_exits_have_no_state_or_external_effect×18、open/relevant_source_scope_without_resolved_property×12、open/decisive_property_or_source_residual×6、excluded/compiler_generated_readonly_getter×4。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 65 项调查动作、24 条查询记录（sat×19、unsat×5），底层求解 26 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_e771d65f29df9c250430`，baseline_usable → sat，条件摘要 `8b527fbecb7d94d7dca472a05ccdb50920fcc5fda723bf147333721b83b8790d`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 9052/7974 | 942be967d839 | 93050f372bfa |
| main/1 | focused_revision | stop/analysis_received | 10364/2466 | 8fe39e68eaf8 | 935bdbfb543d |



选定来源：main；报告 SHA-256 `df25bcd854a677a54f9500bb74527b11ca6274131a8014e0ac572e330d1f0ebe`；报告位于原归档 `run/members/RQ1_024b9da10799/attempt_1/analysis/report.json`。

## RQ1_985c6fd1d4e4

FREEZE · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_46a031a993c1](FCR_02.md#rq1_46a031a993c1)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | freezeAccount(address,bool) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×7、relevant_source_scope_without_resolved_property×1、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×7、open/relevant_source_scope_without_resolved_property×1、open/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_5d45a5a62405230426d3 | FCR-FREEZE | freezeAccount(address,bool)@1476 | property_319aeaa40115b26b7a1a | E1,E2,E3 |



该成员共 2 次真实提交；选定报告登记 6 项调查动作、7 条查询记录（sat×7），底层求解 9 次。反馈登记消费 1 行；检查点类别 FCR-FREEZE×1，最终类别 FCR-FREEZE×1。

可核对的检查示例：`probe_b70a5c169b3c496340dd`，control_transition_preservation → sat，条件摘要 `e977440d2cf18816547929def59b44d0c2d555fdcdb395505163366decd00962`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1845/6115 | 1ae10c7729cd | 62f14813ecf4 |
| main/1 | focused_revision | stop/analysis_received | 2866/1339 | 182cb6ed6dd4 | eb6d390d833a |



选定来源：main；报告 SHA-256 `f7689cbfeefe3bb0f0188985e09ee4ed113c2226c34da4398177798605311c13`；报告位于原归档 `run/members/RQ1_985c6fd1d4e4/attempt_1/analysis/report.json`。

## RQ1_73b13298e227

MINT · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_024b9da10799](FCR_06.md#rq1_024b9da10799)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | mint(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i2 | distributeReward(address,address,address) | 未确认 | financial_property_conditions_not_established |
| i4::FCR-MINT | burnFrom(address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×41、decisive_property_or_source_residual×1、source_positions_and_resolved_properties×1。本次：excluded/committed_exits_have_no_state_or_external_effect×18、open/relevant_source_scope_without_resolved_property×11、open/decisive_property_or_source_residual×9、excluded/compiler_generated_readonly_getter×4、open/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_645a9b15703c88b87c96 | FCR-MINT | burnFrom(address,uint256)@23761 | property_a01f44cdb201a0af057e | E18,E25,E29,E33,E37,E41,E45 |



该成员共 2 次真实提交；选定报告登记 80 项调查动作、98 条查询记录（unsat×73、sat×25），底层求解 78 次。反馈登记消费 1 行；检查点类别 FCR-DESTROY×2、FCR-MINT×1，最终类别 FCR-MINT×1。

可核对的检查示例：`probe_400f9becfdb9d88e91ef`，financial_value_post_exclusion → unsat，条件摘要 `d106e114b2b6bc23e8e3cf355e094262037889970f55a5e84ffb7dc2a39990e0`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 10590/10558 | 706f7772b156 | a482fb36b914 |
| main/1 | focused_revision | stop/analysis_received | 11584/6347 | fdb2a5432c96 | 4fb4a59c4ee2 |



选定来源：main；报告 SHA-256 `3ae063d28de41f08e5168a579a06cdc2858aebab2c37362e287824fd9132c647`；报告位于原归档 `run/members/RQ1_73b13298e227/attempt_1/analysis/report.json`。

## RQ1_a69a455c4a25

FREEZE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_adf28b957352](FCR_06.md#rq1_adf28b957352)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 17 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i6 | freezeAccount(address,bool) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×34。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×14、open/decisive_property_or_source_residual×3。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 1 次真实提交；选定报告登记 74 项调查动作、39 条查询记录（sat×39），底层求解 39 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_1545f8a0318c3e9f253c`，prefix_reachability → sat，条件摘要 `0c2931033f3a1a3e03cf3738bf7e63f515a70ba1238d2990475329c815358803`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3810/12814 | b65ddaf82748 | a0cb432c0a32 |



选定来源：main；报告 SHA-256 `9738e4d31c1687270950c1d070e3bcf951773977e8fe7ebb5b5c980baac1fa17`；报告位于原归档 `run/members/RQ1_a69a455c4a25/attempt_1/analysis/report.json`。

## RQ1_4feeb0c21e60

TRANSFER · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_0e202076b336](FCR_11.md#rq1_0e202076b336)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类初始未出现，最终已形成发现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i5 | zero_fee_transaction(address,address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×11、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×4、open/relevant_source_scope_without_resolved_property×4、open/decisive_property_or_source_residual×3、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：sat×3、unsat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_8b839fc0cb415c57739d | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@432 | property_acbb3741d5a43ea8b85b | E1,E20,E21,E3 |



该成员共 2 次真实提交；选定报告登记 21 项调查动作、11 条查询记录（sat×8、unsat×3），底层求解 7 次。反馈登记消费 1 行；检查点类别 无，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_02a1403ac5fc8d4a7363`，local_premises_feasible → sat，条件摘要 `58ee92cb209a62424743141728453aac749271843b9628782544cb8063120672`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2126/17084 | cb914ac1aedc | ec744b197d4b |
| main/1 | focused_revision | stop/analysis_received | 3346/2518 | 1cf4cac9aef8 | 91248b1489dc |



选定来源：main；报告 SHA-256 `fa1063dcdd2b32e97b1d6f84e6339d8f3ff46063aa669d03d1574d49451bc54c`；报告位于原归档 `run/members/RQ1_4feeb0c21e60/attempt_1/analysis/report.json`。

## RQ1_adf28b957352

FREEZE · 风险端。检测状态：TP。前批 → 本批：未知 → 检出。配对成员 [RQ1_a69a455c4a25](FCR_06.md#rq1_a69a455c4a25)。

本轮已选输出 检出；前次同 200 份 未知；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | freezeAccount(address,bool) | supported | — |
| i6::FCR-FREEZE | freezeAccount(address,bool) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×32、relevant_source_scope_without_resolved_property×2、decisive_property_or_source_residual×1。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×15、open/decisive_property_or_source_residual×2、open/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：sat×32、unsat×21、unknown×5。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_6ac49b9e3a3e173a9978 | FCR-FREEZE | freezeAccount(address,bool)@6430 | property_c8c7ecbf4da521b1051a | E1,E14,E26,E35,E41,E47,E5,E53,E9 |
| finding_884e265002f928bf3499 | FCR-FREEZE | freezeAccount(address,bool)@6430 | property_d735025a5867510f639a | E10,E15,E2,E29,E58,E62,E67 |



该成员共 1 次真实提交；选定报告登记 80 项调查动作、169 条查询记录（sat×113、unsat×45、unknown×11），底层求解 187 次。反馈登记消费 0 行；检查点类别 FCR-FREEZE×2，最终类别 FCR-FREEZE×2。

可核对的检查示例：`probe_114817d4bcfff790ff89`，control_transition_preservation → sat，条件摘要 `08fca14dda97956b407735fb69d7b0f997e5f5e6dcb3fc75f488269f57ee30c5`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4009/19129 | 4bd782959964 | a7013eb75358 |



选定来源：main；报告 SHA-256 `8668ab828ead7efad80e5e591b0a044e88b0b6fe2f4adb0072043d2b4efc7df7`；报告位于原归档 `run/members/RQ1_adf28b957352/attempt_1/analysis/report.json`。

## RQ1_980e04c92f4d

FREEZE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_6a278772c4f3](FCR_12.md#rq1_6a278772c4f3)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 20 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | addSaleOwner(address) | 未确认 | financial_property_conditions_not_established |
| obligation_question_5ce022dee8dec2e7 | freezeAccount(address,bool,uint256,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×53。本次：excluded/compiler_generated_readonly_getter×24、open/relevant_source_scope_without_resolved_property×18、excluded/isolated_flag_no_nongenerated_reader_in_resolved_public_bodies×6、excluded/committed_exits_have_no_state_or_external_effect×3、open/decisive_property_or_source_residual×2。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 83 项调查动作、15 条查询记录（sat×10、unsat×5），底层求解 12 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_ac18bbfda48b8a0ec9d7`，baseline_usable → unsat，条件摘要 `f6bbf66869b9f661920ef80a5597095d004b81dbdb06a5cc0f7b449580271371`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4005/14115 | 4b8806b3ea31 | fd8324563d44 |
| main/1 | focused_revision | stop/analysis_received | 5250/8150 | e9809b4750cb | 93d55ad81922 |



选定来源：main；报告 SHA-256 `d5c41589370e4913b1e70b101db3a65763e9835fc5c05180a4067c0feccaebbb`；报告位于原归档 `run/members/RQ1_980e04c92f4d/attempt_1/analysis/report.json`。

## RQ1_e25d32acc1f7

TRANSFER · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_9451d6dac4de](FCR_04.md#rq1_9451d6dac4de)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 4 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×9。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×3、excluded/committed_exits_have_no_state_or_external_effect×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 12 项调查动作、5 条查询记录（sat×4、unsat×1），底层求解 6 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_d4f544f1f472adf95650`，original_path_commit → sat，条件摘要 `d37507fc78b951b5c70a24a6cfef0cf6ba2296a72b05558f8167bf4a43fda90f`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1895/7301 | b51924509e41 | b812456ae1dc |
| main/1 | focused_revision | stop/analysis_received | 3221/8089 | dd657085c1b6 | b8e9b917b645 |



选定来源：main；报告 SHA-256 `0807d69ee4214905a219813e2f474a5b6f22ac8d830b6cef233d1532e0adf48f`；报告位于原归档 `run/members/RQ1_e25d32acc1f7/attempt_1/analysis/report.json`。

## RQ1_35e0e8d95f92

MINT · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_c75d73e1c482](FCR_03.md#rq1_c75d73e1c482)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 18 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | totalSupply() | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×38。本次：excluded/compiler_generated_readonly_getter×20、open/relevant_source_scope_without_resolved_property×14、open/decisive_property_or_source_residual×4。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_5f8d252940cbcef0dbdf | FCR-TRANSFER | setPrices(uint256,uint256)@6370 | property_30110a5805b28093dab5 | E21,E59,E61,E62,E63,E65,E66,E67 |



该成员共 1 次真实提交；选定报告登记 77 项调查动作、124 条查询记录（sat×86、unsat×37、unknown×1），底层求解 145 次。反馈登记消费 0 行；检查点类别 FCR-TRANSFER×1，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_f77308d63d74c0e5e441`，financial_value_post_exclusion → unsat，条件摘要 `4b35904753cfe4ad4d4f67337a20ea898200d1c484e38edde6298e578cf5a81b`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3871/11126 | 06a794cee269 | 2500acc5b817 |



选定来源：main；报告 SHA-256 `cce3e87a7f704fbdcab849d951c3ffda0259cef7155873727650a2b76dd28ba7`；报告位于原归档 `run/members/RQ1_35e0e8d95f92/attempt_1/analysis/report.json`。

## RQ1_b0a696b11b0a

PAUSE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_4f9f1ce04ed8](FCR_07.md#rq1_4f9f1ce04ed8)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 5 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i3 | transfer_test(address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×8。本次：open/relevant_source_scope_without_resolved_property×4、excluded/compiler_generated_readonly_getter×3、open/decisive_property_or_source_residual×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 14 项调查动作、6 条查询记录（sat×6），底层求解 8 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_2cd49d3a9dd01c55e184`，baseline_usable → sat，条件摘要 `bf6cfcb2046492121d60bc68182bedbf967bf23065e3e3af969039528f36d3c1`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1868/15478 | 684a6724cfbd | 87de50a629a7 |
| main/1 | focused_revision | stop/analysis_received | 2851/3829 | 246b701e75e7 | 9e909d37afb8 |



选定来源：main；报告 SHA-256 `6d5cbf85ab794fb752a7fc942093e39768de71b6b8a199bad60f2a42a7cbb3dd`；报告位于原归档 `run/members/RQ1_b0a696b11b0a/attempt_1/analysis/report.json`。
