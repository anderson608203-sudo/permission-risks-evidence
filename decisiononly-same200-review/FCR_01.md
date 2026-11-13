# FCR 逐例复核 · 第 1 页

[返回成员索引](CaseIndex.md)

## RQ1_cb8c3fafbda1

MINT · 风险端。检测状态：U+。前批 → 本批：检出 → 未知。配对成员 [RQ1_7bfd58ffb1ae](FCR_04.md#rq1_7bfd58ffb1ae)。

本轮已选输出 未知；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类性质已进入检查，指定类仍有 19 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | mintToken(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i7::FCR-MINT | setPrices(uint256,uint256) | 未确认 | financial_property_conditions_not_established |
| i8::FCR-MINT | mintToken(address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×35、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×13、open/decisive_property_or_source_residual×6。与最终指定类性质标识严格相同的查询结果：sat×1、unsat×1。标识变化不能反推旧证据无效。


该成员共 1 次真实提交；选定报告登记 94 项调查动作、79 条查询记录（unsat×42、sat×37），底层求解 80 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_58b146f21a7e82cebd0d`，baseline_usable → sat，条件摘要 `3999d953a0e34506058b742aa489dbec3dd535f6ae2735aee1024deae20d279b`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4114/13845 | 39950d1808d8 | 594936b5da46 |



选定来源：main；报告 SHA-256 `46cc0defaab5eaf0f2a6e338dd49af1b7e421e3452d081a540be5656e7cb2a9a`；报告位于原归档 `run/members/RQ1_cb8c3fafbda1/attempt_1/analysis/report.json`。

## RQ1_afb609e0053e

PAUSE · 风险端。检测状态：U+。前批 → 本批：未知 → 未知。配对成员 [RQ1_7405f0959142](FCR_11.md#rq1_7405f0959142)。

本轮已选输出 未知；前次同 200 份 未知；v32 冻结 Full 检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 4 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | disableTransfers(bool) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×8、decisive_property_or_source_residual×1、relevant_source_scope_without_resolved_property×1。本次：excluded/compiler_generated_readonly_getter×5、open/decisive_property_or_source_residual×2、open/relevant_source_scope_without_resolved_property×2、excluded/committed_exits_have_no_state_or_external_effect×1。与最终指定类性质标识严格相同的查询结果：unsat×1。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 13 项调查动作、11 条查询记录（unsat×7、sat×4），底层求解 6 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_cc3a56004af272bc5aed`，control_transition_preservation → unsat，条件摘要 `f52ee49ddb9ddde2c9108d9d64905a8ddbc455c34eb38976155d9d8570d9572b`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2137/13503 | 3b6041fe553c | 40afa07ca9d6 |
| main/1 | focused_revision | stop/analysis_received | 3453/7393 | d6a8d5dd8294 | 0ccd9344bd01 |



选定来源：main；报告 SHA-256 `88ca8965fe1cc1b0be71d20f0c87d49e33b2877e6d4e96d518bc8f4d4acf88de`；报告位于原归档 `run/members/RQ1_afb609e0053e/attempt_1/analysis/report.json`。

## RQ1_b649070a92c3

PAUSE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_cd39ae0d15a5](FCR_05.md#rq1_cd39ae0d15a5)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 6 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i3 | stop() | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×25。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×6、excluded/isolated_flag_no_nongenerated_reader_in_resolved_public_bodies×2。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 57 项调查动作、9 条查询记录（sat×8、unsat×1），底层求解 10 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_f28dfd4dcf1671be6f2a`，baseline_usable → sat，条件摘要 `27fb2d9da63222e1edb40b0bd9273b83e927d9687969017a22ec29050d7b6b06`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2765/9098 | a02b1ce2be90 | 61128a659602 |
| main/1 | focused_revision | stop/analysis_received | 3706/7271 | 34db76ed4a15 | 70cb607b4b26 |



选定来源：main；报告 SHA-256 `8aabe724b15f27ab2980a1e5c3a499e3dba2cb9d8af053d5d859acfe289ce2a5`；报告位于原归档 `run/members/RQ1_b649070a92c3/attempt_1/analysis/report.json`。

## RQ1_770ae395781c

MINT · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_bc5855a83e2d](FCR_08.md#rq1_bc5855a83e2d)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 12 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×25。本次：excluded/committed_exits_have_no_state_or_external_effect×13、open/decisive_property_or_source_residual×6、open/relevant_source_scope_without_resolved_property×6。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 24 项调查动作、9 条查询记录（sat×8、unsat×1），底层求解 8 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_24f0dd9073422389fe5a`，baseline_usable → sat，条件摘要 `b3fe9eaec7c0aef5874a93ce0cb1f18cb7d360fc56015c745152e6b2b0e83558`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 5706/7766 | 21b4973d5ce4 | 38fcb047710b |
| main/1 | focused_revision | stop/analysis_received | 7641/1423 | d8063792ecef | 34458f9157c1 |



选定来源：main；报告 SHA-256 `30f57afaf4101eb856467c8ecf51d58d57a1d84510b5560454ccc349cd04a04f`；报告位于原归档 `run/members/RQ1_770ae395781c/attempt_1/analysis/report.json`。

## RQ1_cd47d22b26a9

FREEZE · 风险端。检测状态：TP。前批 → 本批：未知 → 检出。配对成员 [RQ1_fa2207747d01](FCR_12.md#rq1_fa2207747d01)。

本轮已选输出 检出；前次同 200 份 未知；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | freezeAccount(address,bool) | supported | — |
| i5::FCR-FREEZE | freezeAccount(address,bool) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×31、relevant_source_scope_without_resolved_property×2、decisive_property_or_source_residual×1。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×14、open/decisive_property_or_source_residual×3。与最终指定类性质标识严格相同的查询结果：sat×16、unknown×12。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_98656bbed33db0df04a2 | FCR-FREEZE | freezeAccount(address,bool)@6091 | property_4174ba5d7d72ef314366 | E17,E30,E4,E73,E87 |
| finding_00bb36c1f8003aa41b0f | FCR-MINT | burn(uint256)@8100 | property_7dd9c93deee99bd6e082 | E101,E106,E51,E75,E82,E89,E95 |



该成员共 1 次真实提交；选定报告登记 108 项调查动作、70 条查询记录（sat×35、unsat×23、unknown×12），底层求解 64 次。反馈登记消费 0 行；检查点类别 FCR-FREEZE×1、FCR-MINT×1，最终类别 FCR-FREEZE×1、FCR-MINT×1。

可核对的检查示例：`probe_26f6b95521a5f6b78416`，control_transition_preservation → sat，条件摘要 `36b2e7f42c63a5324c78e3974ea714012648a65695e8aa9e88c238d3700e4f30`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4139/7265 | fc25a4840ac8 | 4ffd3251c119 |



选定来源：main；报告 SHA-256 `c0168a22a55bb8dcd7de8a0182edbb88549c1c3aa8566da2001aaf3590ab9ecb`；报告位于原归档 `run/members/RQ1_cd47d22b26a9/attempt_1/analysis/report.json`。

## RQ1_0267e2a8ebb2

MINT · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_3b4d9f6eb96f](FCR_07.md#rq1_3b4d9f6eb96f)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | mintToken(address,uint256) | supported | — |
| i3::FCR-MINT | setPrices(uint256,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×35、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×13、open/decisive_property_or_source_residual×5、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：unsat×11、sat×3。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_77106d27d9a3c0b98c86 | FCR-MINT | mintToken(address,uint256)@6472 | property_6e347405de984a8383b5 | E28,E4,E40,E52,E60,E64,E68,E72 |
| finding_c2df67c34e5664baf99e | FCR-TRANSFER | mintToken(address,uint256)@6472 | property_34fa388f56632efd4692 | E19,E36,E48,E58,E62,E66,E70,E74,E76 |
| finding_e308c1fa7f7dd6f05e30 | FCR-FREEZE | freezeAccount(address,bool)@6806 | property_f0f16533ed383a449c68 | E10,E13,E16,E2,E20,E24,E5,E8 |
| finding_07539d531699622f48fe | FCR-TRANSFER | setPrices(uint256,uint256)@7040 | property_a8bf18a97e897a942cf7 | E22,E61,E63,E65,E67,E69,E71,E73,E75,E79 |



该成员共 1 次真实提交；选定报告登记 80 项调查动作、150 条查询记录（unsat×74、sat×65、unknown×11），底层求解 145 次。反馈登记消费 0 行；检查点类别 FCR-TRANSFER×2、FCR-FREEZE×1、FCR-MINT×1，最终类别 FCR-TRANSFER×2、FCR-FREEZE×1、FCR-MINT×1。

可核对的检查示例：`probe_b8ec9be47a438da07752`，baseline_usable → sat，条件摘要 `44b01f368066ecc714e89230a7b50030e18030096428eb7d8fbc8da921c84766`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4114/18861 | 39950d1808d8 | 5e496148903e |



选定来源：main；报告 SHA-256 `2a797c5caac1b150f869f231355208b59339dac558d67267cbdde159890eb772`；报告位于原归档 `run/members/RQ1_0267e2a8ebb2/attempt_1/analysis/report.json`。

## RQ1_0c666ce785e8

TRANSFER · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_3455b6a9ba4f](FCR_07.md#rq1_3455b6a9ba4f)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类初始未出现，最终已形成发现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | supported | — |
| i2 | CashOut(uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×8、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×2、excluded/committed_exits_have_no_state_or_external_effect×1、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：sat×3、unsat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_662bafce7461669af514 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@533 | property_bf771e0d214806b52fb8 | E1,E14,E15,E8 |



该成员共 2 次真实提交；选定报告登记 15 项调查动作、9 条查询记录（sat×7、unsat×2），底层求解 9 次。反馈登记消费 1 行；检查点类别 无，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_8554844f83917b96f8cb`，local_premises_feasible → sat，条件摘要 `b278ca86d12bbfebba10758dfe46afc531f4f211954951a9b12291a57ac47a9c`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1912/23215 | 34ba704ff337 | db2b45c407ab |
| main/1 | focused_revision | stop/analysis_received | 2431/3732 | e0d3d3ac67c6 | 572140155925 |



选定来源：main；报告 SHA-256 `58028d625ac9a964bfb9b88ed99c52829ed15d2801c755481ff0e1de864f305a`；报告位于原归档 `run/members/RQ1_0c666ce785e8/attempt_1/analysis/report.json`。

## RQ1_4be3030c4533

MINT · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_af7c473b8cca](FCR_09.md#rq1_af7c473b8cca)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 18 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | totalSupply() | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×35。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×14、open/decisive_property_or_source_residual×4。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_a0ada79afe5689ac2a41 | FCR-TRANSFER | setPrices(uint256,uint256)@6564 | property_0267b2e8b2b468ccfce8 | E23,E29,E65,E67,E69,E7,E71,E73,E74,E77 |



该成员共 2 次真实提交；选定报告登记 87 项调查动作、83 条查询记录（sat×65、unsat×18），底层求解 95 次。反馈登记消费 1 行；检查点类别 FCR-TRANSFER×1，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_cce3efe5e7aa1bca6b95`，financial_value_post_exclusion → sat，条件摘要 `b59ef80a8e99ea270a2282f9fc98c217e58c5dcf37a5779ab51ca8bd9da142e3`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3889/15970 | 17e277c689a7 | 671f1b94c82f |
| main/1 | focused_revision | stop/analysis_received | 4477/1540 | 359c237a0599 | fd307e2517c2 |



选定来源：main；报告 SHA-256 `603b6e2e3b53c0ea0b1540ccaf6c01c516023c9bcf1bb206a40ba6b99e819f34`；报告位于原归档 `run/members/RQ1_4be3030c4533/attempt_1/analysis/report.json`。

## RQ1_206d19a8539c

TRANSFER · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_3a3d833ca142](FCR_10.md#rq1_3a3d833ca142)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 1 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |


前批指定类义务依据：source_effect_and_privilege_relevance×4。本次：excluded/compiler_generated_readonly_getter×2、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 4 项调查动作、0 条查询记录（无），底层求解 0 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：无已保存的程序查询。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1527/2381 | 71b82bc04353 | 03594bedf05b |
| main/1 | focused_revision | stop/analysis_received | 2650/1365 | c2036b11449d | b68cd811dc61 |



选定来源：main；报告 SHA-256 `cea79f94004bee5edb55fe282a3f716839d5b52e037ee659b85575be1e6bc5db`；报告位于原归档 `run/members/RQ1_206d19a8539c/attempt_1/analysis/report.json`。

## RQ1_085aaca2f412

DESTROY · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_c9626779c857](FCR_03.md#rq1_c9626779c857)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 10 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | burnFrom(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i2::FCR-DESTROY | burnFrom(address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×27。本次：excluded/compiler_generated_readonly_getter×16、open/decisive_property_or_source_residual×5、open/relevant_source_scope_without_resolved_property×5、excluded/committed_exits_have_no_state_or_external_effect×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 30 项调查动作、6 条查询记录（sat×6），底层求解 6 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_8cf1b08ce3bed0d290c6`，baseline_usable → sat，条件摘要 `b3f072af8888f4c73b738d47e4f18264329d55c92e21312995753a00dd883cfd`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2793/11893 | 99d8b290455c | ddcc39105f0f |
| main/1 | focused_revision | stop/analysis_received | 4794/9781 | cc81d3f11ffa | b69a733766d7 |



选定来源：main；报告 SHA-256 `19429a5fe8cfc43d3067dfded50ebc82a6bb10cbb427816340bf4ad5a4eeef02`；报告位于原归档 `run/members/RQ1_085aaca2f412/attempt_1/analysis/report.json`。
