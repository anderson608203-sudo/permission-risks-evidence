# FCR 逐例复核 · 第 11 页

[返回成员索引](CaseIndex.md)

## RQ1_1c6b43b24d4c

PAUSE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_37d9daf031da](FCR_02.md#rq1_37d9daf031da)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 39 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×100。本次：excluded/compiler_generated_readonly_getter×48、open/relevant_source_scope_without_resolved_property×28、excluded/committed_exits_have_no_state_or_external_effect×13、open/decisive_property_or_source_residual×11。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 1 次真实提交；选定报告登记 17 项调查动作、501 条查询记录（unsat×264、sat×237），底层求解 849 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_e993c2051d82d4d6eda4`，baseline_usable → sat，条件摘要 `579760bf205a6af8c12297d468b734e8296862858fb372eceb42ab3778999edc`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 7333/27976 | 356cc8f1ffc2 | 618dc92594d1 |



选定来源：main；报告 SHA-256 `930e0fb7dde11463e10e8159f988a32e2eb923c275aff453e98695e6b51696cc`；报告位于原归档 `run/members/RQ1_1c6b43b24d4c/attempt_1/analysis/report.json`。

## RQ1_983137cbe5d6

MINT · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_18c85d7f1380](FCR_07.md#rq1_18c85d7f1380)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 18 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×35。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×14、open/decisive_property_or_source_residual×4。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_c088a5596298f0dbed14 | FCR-TRANSFER | setPrices(uint256,uint256)@6364 | property_47193a56bf72a86d97ee | E12,E14,E20,E26,E28,E29,E30,E31,E32,E6 |



该成员共 2 次真实提交；选定报告登记 77 项调查动作、17 条查询记录（sat×11、unsat×5、unknown×1），底层求解 16 次。反馈登记消费 1 行；检查点类别 FCR-TRANSFER×1，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_95f45d215dcc1a2bae64`，financial_value_post_exclusion → sat，条件摘要 `8e508c625de4e10f102b5899b8c14d042e444d31b3ebbf56ff3bfbea59353619`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3836/20774 | 898bb06639d2 | bc50e2f9ff21 |
| main/1 | focused_revision | stop/analysis_received | 4437/2907 | 0e5300aaed37 | 13a5a27638e1 |



选定来源：main；报告 SHA-256 `65a819cf0af1951042a7ed6b65543b64c1ab84898843e6d8711429db20322750`；报告位于原归档 `run/members/RQ1_983137cbe5d6/attempt_1/analysis/report.json`。

## RQ1_e13bb6580d65

MINT · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_94d9f2cfc77c](FCR_03.md#rq1_94d9f2cfc77c)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | mint(address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×26、source_positions_and_resolved_properties×1。本次：excluded/committed_exits_have_no_state_or_external_effect×13、open/relevant_source_scope_without_resolved_property×7、open/decisive_property_or_source_residual×6、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：unsat×4、sat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_d74220ec2c6b51721c30 | FCR-MINT | mint(address,uint256)@12463 | property_1d77be3e90646a936074 | E16,E24,E25,E26,E7 |
| finding_833ed3f9eebc7ba3522b | FCR-DESTROY | mint(address,uint256)@12463 | property_5bccf10eaeb7c7d4074e | E13,E14,E15,E17,E27,E9 |



该成员共 2 次真实提交；选定报告登记 52 项调查动作、30 条查询记录（sat×16、unsat×14），底层求解 31 次。反馈登记消费 1 行；检查点类别 FCR-DESTROY×1、FCR-MINT×1，最终类别 FCR-DESTROY×1、FCR-MINT×1。

可核对的检查示例：`probe_2088a07935db8b978be7`，financial_value_post_exclusion → sat，条件摘要 `812ecfa6fc47e213dd3f87bfaf4cac3ca97500ab889349217572b754432e7ee0`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 6602/5576 | 7728ce54f1bf | cfe5739a1bc9 |
| main/1 | focused_revision | stop/analysis_received | 8377/2656 | 613bc674b2dc | c0778fa2aef4 |



选定来源：main；报告 SHA-256 `eddc8b418787eec0d2096b5a8935a0ea797f22d0a4b5fa0523bcd79691b7a308`；报告位于原归档 `run/members/RQ1_e13bb6580d65/attempt_1/analysis/report.json`。

## RQ1_7405f0959142

PAUSE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_afb609e0053e](FCR_01.md#rq1_afb609e0053e)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 4 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×10。本次：excluded/compiler_generated_readonly_getter×5、open/relevant_source_scope_without_resolved_property×3、excluded/committed_exits_have_no_state_or_external_effect×1、open/decisive_property_or_source_residual×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 10 项调查动作、0 条查询记录（无），底层求解 0 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：无已保存的程序查询。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2035/13142 | 0f20e2ad33f3 | 59452d125de0 |
| main/1 | focused_revision | stop/analysis_received | 3571/4362 | 9044ba5cc126 | 96f67b5ab583 |



选定来源：main；报告 SHA-256 `3812a180e8f32a346f9cf24498feb767f2cf71ccf1422b5a6fdc3825959a17ab`；报告位于原归档 `run/members/RQ1_7405f0959142/attempt_1/analysis/report.json`。

## RQ1_0e202076b336

TRANSFER · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_4feeb0c21e60](FCR_06.md#rq1_4feeb0c21e60)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 8 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×12。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×4、open/relevant_source_scope_without_resolved_property×4。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 19 项调查动作、1 条查询记录（sat×1），底层求解 1 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_354ac9d6ea6852f8e089`，original_path_commit → sat，条件摘要 `8f0ee54b6c30fa2b832c6db45e4747e51195e30394dc7dde31e423c4d0128aaa`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2102/13431 | 680134734a0d | 602e1ee3751c |
| main/1 | focused_revision | stop/analysis_received | 3231/4724 | cfd8e7ca4e42 | 0b289dd56f73 |



选定来源：main；报告 SHA-256 `ad65b581cbf46c1f7bd1df9abb65af39a773f1630e6f2b0567240ee5aed96066`；报告位于原归档 `run/members/RQ1_0e202076b336/attempt_1/analysis/report.json`。

## RQ1_20dfd0c54b94

PAUSE · 风险端。检测状态：U+。前批 → 本批：未知 → 未知。配对成员 [RQ1_aaeb3f57cfd0](FCR_10.md#rq1_aaeb3f57cfd0)。

本轮已选输出 未知；前次同 200 份 未知；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类性质已进入检查，指定类仍有 24 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1::FCR-PAUSE | addLock(address) | 未确认 | financial_property_conditions_not_established |
| i2 | enableTransfer(bool) | 未确认 | financial_property_conditions_not_established |
| obligation_question_21ca76ebf66c96e2::FCR-PAUSE | setExclude(address) | 未确认 | financial_property_conditions_not_established |
| obligation_question_3b87765b61ad516d::FCR-PAUSE | removeLock(address) | 未确认 | financial_property_conditions_not_established |
| obligation_question_40619a6812b8be60::FCR-PAUSE | addLock(address) | 未确认 | financial_property_conditions_not_established |
| obligation_question_52575cbe5b8e7ca7::FCR-PAUSE | setExclude(address) | 未确认 | financial_property_conditions_not_established |
| obligation_question_5d87acc7043cca97 | enableTransfer(bool) | 未确认 | financial_property_conditions_not_established |
| obligation_question_93ea7ab96b402b1a::FCR-PAUSE | removeLock(address) | 未确认 | financial_property_conditions_not_established |
| obligation_question_ec1b0b07a6a9b2d5 | disableLock(bool) | 未确认 | financial_property_conditions_not_established |
| obligation_question_eff164147dbe8e16 | disableLock(bool) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×46、decisive_property_or_source_residual×4、relevant_source_scope_without_resolved_property×4。本次：excluded/compiler_generated_readonly_getter×21、open/relevant_source_scope_without_resolved_property×14、open/decisive_property_or_source_residual×10、excluded/isolated_flag_no_nongenerated_reader_in_resolved_public_bodies×5、excluded/committed_exits_have_no_state_or_external_effect×4。与最终指定类性质标识严格相同的查询结果：sat×6。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_0189d1ee93391480ade4 | FCR-FREEZE | addLock(address)@2663 | property_832334bf77f0cf3d104e | E19,E28,E3,E7 |



该成员共 2 次真实提交；选定报告登记 75 项调查动作、139 条查询记录（unsat×112、sat×27），底层求解 80 次。反馈登记消费 1 行；检查点类别 FCR-FREEZE×1，最终类别 FCR-FREEZE×1。

可核对的检查示例：`probe_d9089d8761f427834320`，financial_value_post_exclusion → unsat，条件摘要 `7a870c1b4932ebacf6965ba1e1dfcc1d1b37a5d0f6293a56afdc252dc35c7975`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3768/13400 | 8004aac459ee | 22f3ca26ee64 |
| main/1 | focused_revision | stop/analysis_received | 5289/5833 | 6d9b7478f8df | 6c5c4ce7d2d0 |



选定来源：main；报告 SHA-256 `a83f87b84dd16370269802076b7f97385a7d2cd9bf6646a162ae75e20174d266`；报告位于原归档 `run/members/RQ1_20dfd0c54b94/attempt_1/analysis/report.json`。

## RQ1_6ca2b0aeda43

DESTROY · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_33d48945207e](FCR_09.md#rq1_33d48945207e)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 15 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| obligation_question_789ad6b18ec0ee3a | burnFrom(address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_bd0b616de905f2ca | burn(uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×48。本次：excluded/compiler_generated_readonly_getter×27、open/decisive_property_or_source_residual×9、open/relevant_source_scope_without_resolved_property×6、excluded/committed_exits_have_no_state_or_external_effect×5、excluded/all_extracted_exits_revert×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 44 项调查动作、0 条查询记录（无），底层求解 0 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：无已保存的程序查询。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4317/11633 | 5dd096102e04 | 49b30b7fcb12 |
| main/1 | focused_revision | stop/analysis_received | 5431/3254 | b88b26c6ea04 | c9527c511e45 |



选定来源：main；报告 SHA-256 `a47c10ca5a566142cdf34487f2fedd4c22ac000f4b3c5ec5ba2add6cc07dba6c`；报告位于原归档 `run/members/RQ1_6ca2b0aeda43/attempt_1/analysis/report.json`。

## RQ1_43103f5773b9

FREEZE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_1f932eab663d](FCR_08.md#rq1_1f932eab663d)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 15 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i4 | transfer(address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×30。本次：open/relevant_source_scope_without_resolved_property×14、excluded/committed_exits_have_no_state_or_external_effect×8、excluded/compiler_generated_readonly_getter×7、open/decisive_property_or_source_residual×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 46 项调查动作、18 条查询记录（sat×14、unsat×4），底层求解 18 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_fbfd72a66114f4096435`，baseline_usable → sat，条件摘要 `a5a9879cf9974af01d18ce424f4df0c3976c1bf5e78b72b8c4ec116eab4dfee1`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3996/9966 | feb2fa26c59c | f822ec30d09c |
| main/1 | focused_revision | stop/analysis_received | 4534/2562 | 4bd0a883ec95 | ac9fecfc9c70 |



选定来源：main；报告 SHA-256 `509b70a44acc12a07fe3d101a6a7e7d3418bf264d50ffab2ab3ac04d6fe2533f`；报告位于原归档 `run/members/RQ1_43103f5773b9/attempt_1/analysis/report.json`。

## RQ1_cda3df36df22

PAUSE · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_35f857af5c9e](FCR_09.md#rq1_35f857af5c9e)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i3 | stop() | supported | — |
| i4::FCR-PAUSE | stop() | supported | — |
| obligation_question_b0e79d25c2de49ee | start() | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×10、relevant_source_scope_without_resolved_property×2、source_positions_and_resolved_properties×2。本次：excluded/compiler_generated_readonly_getter×7、open/relevant_source_scope_without_resolved_property×5、open/decisive_property_or_source_residual×1、open/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：sat×3、unsat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_0a871f15df03cb710775 | FCR-PAUSE | stop()@2817 | property_690a6f18a9085a53ca41 | E1,E14,E20,E5 |
| finding_0c68c04b279fd587d8cc | FCR-PAUSE | stop()@2817 | property_22a822ce32a4988afb83 | E17,E2,E22,E6 |



该成员共 2 次真实提交；选定报告登记 53 项调查动作、68 条查询记录（sat×47、unsat×21），底层求解 45 次。反馈登记消费 1 行；检查点类别 FCR-PAUSE×2，最终类别 FCR-PAUSE×2。

可核对的检查示例：`probe_0bccde743b41803ff1a5`，control_transition_preservation → sat，条件摘要 `cc813226298f54673ab3cece7a6b6964b26b8da64544ff001558e62ade327734`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2501/10525 | 742e509f2ab9 | 59355e7b53eb |
| main/1 | focused_revision | stop/analysis_received | 3741/1466 | 5769a664da9f | 7fb8e41c966d |



选定来源：main；报告 SHA-256 `d7e5a5b9416f8d6ae4243863a4a3aeddf9061297efc6415fd90a0f851f85bbb8`；报告位于原归档 `run/members/RQ1_cda3df36df22/attempt_1/analysis/report.json`。

## RQ1_30177d564271

FREEZE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_c80f7a639e42](FCR_08.md#rq1_c80f7a639e42)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 16 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i5 | freezeAccount(address,bool) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×33。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×13、open/decisive_property_or_source_residual×3。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 77 项调查动作、12 条查询记录（sat×12），底层求解 12 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_14acbecf207127464425`，baseline_usable → sat，条件摘要 `a9eaa0dc307f08425009a23c3da697796cbfa2ddf048a6ff9c0fd456fd40ba18`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4086/11719 | cdb708fcbe2e | 1cb6dc85265e |
| main/1 | focused_revision | stop/analysis_received | 4687/8396 | 3b0bbef940bb | dbc194189905 |



选定来源：main；报告 SHA-256 `0bad24f86e6392572122eb0cf65bc259be451e279d2ef247f7a2ba9cc6c9ab6c`；报告位于原归档 `run/members/RQ1_30177d564271/attempt_1/analysis/report.json`。
