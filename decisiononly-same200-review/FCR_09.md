# FCR 逐例复核 · 第 9 页

[返回成员索引](CaseIndex.md)

## RQ1_fe4ace2cd8e5

DESTROY · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_55a1e2ef0f09](FCR_07.md#rq1_55a1e2ef0f09)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 13 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2::FCR-DESTROY | transferFromCrowdfund(address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×37。本次：excluded/compiler_generated_readonly_getter×22、open/relevant_source_scope_without_resolved_property×8、open/decisive_property_or_source_residual×5、excluded/committed_exits_have_no_state_or_external_effect×2。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 50 项调查动作、24 条查询记录（sat×18、unsat×6），底层求解 31 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_6e0b083bee77afd5828c`，baseline_usable → sat，条件摘要 `66f778b536f2bac322e5a86152a9f98000d1b9257ebbe94978c62641af815630`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 5306/15757 | 8438b3b78440 | 7a918453403d |
| main/1 | focused_revision | stop/analysis_received | 6729/2549 | a1e1b005596a | bbae96d3cf6a |



选定来源：main；报告 SHA-256 `5ce7d576774e0f4cae89be3ab24b2610dc243b05915e76e11f5831fb54e7cbaa`；报告位于原归档 `run/members/RQ1_fe4ace2cd8e5/attempt_1/analysis/report.json`。

## RQ1_1844e5d3d18e

TRANSFER · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_db73c28a69c2](FCR_12.md#rq1_db73c28a69c2)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 未知

指定类初始未出现，最终已形成发现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i5@051252cf9fe3 | WithdrawToken(address,uint256,address) | 未确认 | financial_property_conditions_not_established |
| i5@c9e1e9c2647a | WithdrawToken(address,uint256,address) | 未确认 | financial_property_conditions_not_established |
| obligation_question_6d7ad20fa410f80f | zero_fee_transaction(address,address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×18、source_positions_and_resolved_properties×3。本次：open/relevant_source_scope_without_resolved_property×9、open/decisive_property_or_source_residual×6、excluded/compiler_generated_readonly_getter×5、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：sat×3、unsat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_89b955700ab46e397cde | FCR-DESTROY | WitdrawTokenToHolder(address,address,uint256)@2252 | property_32223349bc4640d8f30b | E10,E25,E27,E30,E34 |
| finding_b8c1e22a8104929d0641 | FCR-MINT | WitdrawTokenToHolder(address,address,uint256)@2252 | property_91cfb0c6a2ea908e7cba | E13,E32,E36,E38,E39,E42 |
| finding_c407ab771206342193bd | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@696 | property_f0da382de40f38054d1a | E50,E68 |



该成员共 2 次真实提交；选定报告登记 69 项调查动作、57 条查询记录（sat×40、unsat×17），底层求解 52 次。反馈登记消费 1 行；检查点类别 FCR-DESTROY×1、FCR-MINT×1，最终类别 FCR-DESTROY×1、FCR-MINT×1、FCR-TRANSFER×1。

可核对的检查示例：`probe_ed25fcabf347ac174297`，local_premises_feasible → sat，条件摘要 `3e4f50a8baf3eb0a4221e8d5dda2b09ac70010414b619dc1ffe0b4d211848255`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2388/13549 | c1b2ad510197 | 4facefaf13dd |
| main/1 | focused_revision | stop/analysis_received | 3461/12761 | 2626adfaeac1 | b45ead7ca62a |



选定来源：main；报告 SHA-256 `3ea896d506844dc7dd81f02b2699b3c1188d4ce97813fe8b161e3b7eb057e918`；报告位于原归档 `run/members/RQ1_1844e5d3d18e/attempt_1/analysis/report.json`。

## RQ1_db11e3e08742

DESTROY · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_353a9b0b5006](FCR_04.md#rq1_353a9b0b5006)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 检出

前次指定类有效未检出；本次 DESTROY 未闭合而转未知。不得从另一类 PAUSE 报警推导这份修复是否成功。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | SetBurnPercent(uint256) | 未确认 | financial_property_conditions_not_established |
| i3::FCR-DESTROY | SetBurnPercent(uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_a593d3d289cb9d57::FCR-DESTROY | SetCharityPercent(uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×30。本次：excluded/compiler_generated_readonly_getter×12、excluded/committed_exits_have_no_state_or_external_effect×6、open/decisive_property_or_source_residual×5、open/relevant_source_scope_without_resolved_property×5、excluded/isolated_flag_no_nongenerated_reader_in_resolved_public_bodies×2。与最终指定类性质标识严格相同的查询结果：unsat×15、sat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_b3d8ce390e74e44df461 | FCR-PAUSE | SetBurnPercent(uint256)@4945 | property_e661e4cc0d23825a501d | E18,E2,E27,E30,E9 |
| finding_15ffa17170dfdceea3d3 | FCR-PAUSE | SetBurnPercent(uint256)@4945 | property_3e66c1fda14e0d47417a | E10,E21,E44,E5 |



该成员共 2 次真实提交；选定报告登记 92 项调查动作、149 条查询记录（unsat×86、sat×59、unknown×4），底层求解 201 次。反馈登记消费 1 行；检查点类别 FCR-PAUSE×2，最终类别 FCR-PAUSE×2。

可核对的检查示例：`probe_6a36587734a8a24ec5f8`，control_transition_preservation → sat，条件摘要 `ca89314eca98011217cbd55861c012ab18fe6056fbf7678324f45d3a289c9bea`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 5848/22228 | b16621978d52 | 087b5a4ac3ef |
| main/1 | focused_revision | stop/analysis_received | 7262/4036 | 5c1086ad09e8 | d4b2f313a038 |



选定来源：main；报告 SHA-256 `2751b3c9f5925b5ecea3d004764397d785e6b5103f630af8b9966f8f5128cbdd`；报告位于原归档 `run/members/RQ1_db11e3e08742/attempt_1/analysis/report.json`。

## RQ1_a906c0b62c0b

FREEZE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_1a94f7866801](FCR_09.md#rq1_1a94f7866801)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

主批 KeyError；独立副本使用剩余的一个首答槽，成功出报告。多个局部 SAT/UNSAT 均未形成该成员的五类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2@25c714cf1b4a | lockAddress(address,bool) | 未确认 | financial_property_conditions_not_established |
| i2@48135c7781b5 | lockAddress(address,bool) | 未确认 | financial_property_conditions_not_established |
| i2@5fc5bdfd4ce6 | lockAddress(address,bool) | 未确认 | financial_property_conditions_not_established |
| i2@977b12483c58 | lockAddress(address,bool) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×71。本次：open/relevant_source_scope_without_resolved_property×31、excluded/compiler_generated_readonly_getter×25、excluded/committed_exits_have_no_state_or_external_effect×11、open/decisive_property_or_source_residual×4。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 75 项调查动作、24 条查询记录（sat×18、unsat×6），底层求解 26 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_f1a559de29664efc4f96`，baseline_usable → sat，条件摘要 `052a6dc7b6d6f9b04cc8bd8f1febb8197f3a7d5e2375130358f5168cc690d934`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4100/15407 | 85c33f8d8b81 | 7a0dba6216a1 |
| supplement/0 | initial | stop/analysis_received | 4100/12801 | 85c33f8d8b81 | 29aba4e1c359 |



选定来源：supplement；报告 SHA-256 `255aa32257ac54d7feab7d7f646eca06e7e12f1c7e9cb3185c5d11aab00de541`；报告位于原归档 `run/technical_two/run/members/RQ1_a906c0b62c0b/attempt_1/analysis/report.json`。

## RQ1_ee2aa7f32d31

DESTROY · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_eb30c6dee989](FCR_07.md#rq1_eb30c6dee989)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 9 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | burnDragons(uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_5190fb88f9638c3a | burnFrom(address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_5ef9947bdc4c2de3 | burn(uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×24。本次：excluded/compiler_generated_readonly_getter×9、excluded/committed_exits_have_no_state_or_external_effect×6、open/decisive_property_or_source_residual×6、open/relevant_source_scope_without_resolved_property×3。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 75 项调查动作、51 条查询记录（sat×39、unsat×12），底层求解 43 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_3f3265b919819c0f6f84`，control_transition_preservation → sat，条件摘要 `16e3ed86f508a3c28fb9045e839ced4e82dce4c2a7d9fef8207c681693f2b234`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3675/22468 | 9d03c1f04df7 | e98a32e9a323 |
| main/1 | focused_revision | stop/analysis_received | 4376/18244 | cce57518bb37 | 29123fd39b2a |



选定来源：main；报告 SHA-256 `da606069bef108611f67e9418a8a6c29e2fbfdc0dbdcfdecc9e2682bd1009e3c`；报告位于原归档 `run/members/RQ1_ee2aa7f32d31/attempt_1/analysis/report.json`。

## RQ1_33d48945207e

DESTROY · 风险端。检测状态：U+。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_6ca2b0aeda43](FCR_11.md#rq1_6ca2b0aeda43)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 15 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| obligation_question_789ad6b18ec0ee3a | burnFrom(address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_bd0b616de905f2ca | burn(uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×48。本次：excluded/compiler_generated_readonly_getter×27、open/decisive_property_or_source_residual×9、open/relevant_source_scope_without_resolved_property×6、excluded/committed_exits_have_no_state_or_external_effect×5、excluded/all_extracted_exits_revert×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 47 项调查动作、0 条查询记录（无），底层求解 0 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：无已保存的程序查询。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4635/5320 | 5cc23386e445 | 7d47a42586fd |
| main/1 | focused_revision | stop/analysis_received | 5256/5145 | 4fe5e2e90337 | fe671ecf31f3 |



选定来源：main；报告 SHA-256 `5d7528c97511c165227d62e3b210a14305091412f105bd7a174edf7edebb1f6d`；报告位于原归档 `run/members/RQ1_33d48945207e/attempt_1/analysis/report.json`。

## RQ1_b84042e6eefd

PAUSE · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_475c7d9ec738](FCR_03.md#rq1_475c7d9ec738)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | disableTransfers(bool) | supported | — |
| i6::FCR-PAUSE | disableTransfers(bool) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×4、relevant_source_scope_without_resolved_property×1、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×2、open/relevant_source_scope_without_resolved_property×2、excluded/committed_exits_have_no_state_or_external_effect×1、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：sat×4、unsat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_ad4e2903c4c439719267 | FCR-PAUSE | disableTransfers(bool)@1043 | property_fe62fe370c1dd58082ef | E1,E15,E8 |
| finding_f1a6bb32fdf7170c9215 | FCR-PAUSE | disableTransfers(bool)@1043 | property_0746cbde3fe34a304e2a | E13,E18,E2 |



该成员共 2 次真实提交；选定报告登记 27 项调查动作、23 条查询记录（unsat×12、sat×11），底层求解 9 次。反馈登记消费 1 行；检查点类别 FCR-PAUSE×2，最终类别 FCR-PAUSE×2。

可核对的检查示例：`probe_6487b1f2f7d938430ba9`，control_transition_preservation → unsat，条件摘要 `3448f39e7ef0e498d3585be7774e9844a9eeeca818e2243ef8d29529a8fcfdae`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1838/11900 | 16ed03995f3c | baae848f9089 |
| main/1 | focused_revision | stop/analysis_received | 2843/12659 | 3a21c18c41a9 | 2c1c9e552d03 |



选定来源：main；报告 SHA-256 `dc4a4e9e2728e132a7b5ca6ebdb79606fe9377463581ff3fd962c324a1085b2c`；报告位于原归档 `run/members/RQ1_b84042e6eefd/attempt_1/analysis/report.json`。

## RQ1_1a94f7866801

FREEZE · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_a906c0b62c0b](FCR_09.md#rq1_a906c0b62c0b)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1@25c714cf1b4a | allowAddress(address,bool) | supported | — |
| i1@48135c7781b5 | allowAddress(address,bool) | supported | — |
| i1@5fc5bdfd4ce6 | allowAddress(address,bool) | supported | — |
| i1@977b12483c58 | allowAddress(address,bool) | supported | — |
| i3@25c714cf1b4a::FCR-FREEZE | lockAddress(address,bool) | supported | — |
| i3@48135c7781b5::FCR-FREEZE | lockAddress(address,bool) | supported | — |
| i3@5fc5bdfd4ce6::FCR-FREEZE | lockAddress(address,bool) | supported | — |
| i3@977b12483c58 | lockAddress(address,bool) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×56、decisive_property_or_source_residual×8、relevant_source_scope_without_resolved_property×4、source_positions_and_resolved_properties×3。本次：open/relevant_source_scope_without_resolved_property×27、excluded/compiler_generated_readonly_getter×25、excluded/committed_exits_have_no_state_or_external_effect×11、open/decisive_property_or_source_residual×3、open/source_positions_and_resolved_properties×3、excluded/source_positions_and_resolved_properties×2。与最终指定类性质标识严格相同的查询结果：sat×39、unsat×32。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_0ac96bf3c97df68c1a69 | FCR-FREEZE | allowAddress(address,bool)@2286 | property_f6e90c64ddfbf4c5d045 | E29,E42,E64,E8 |
| finding_82b351c0e4f8e9f40b3f | FCR-FREEZE | allowAddress(address,bool)@2286 | property_6bebfa6fd8b3bb21be9b | E22,E50,E72,E9 |
| finding_76990d40275799605825 | FCR-FREEZE | allowAddress(address,bool)@2286 | property_7b7ac09bb9b28abb0941 | E17,E35,E4,E70 |
| finding_55571e7aea4026cb10c6 | FCR-FREEZE | allowAddress(address,bool)@2286 | property_8a756408f7eb234f33bf | E1,E20,E40 |
| finding_00accb941fc3e755cd7e | FCR-PAUSE | setLocked(bool)@2804 | property_159d59e125f9888dae49 | E12,E26,E38,E62 |
| finding_160ec704279235aee984 | FCR-PAUSE | setLocked(bool)@2804 | property_c4d6acd00665f6cbd29f | E18,E36,E6,E60 |
| finding_ed54ffd0f73637e8e622 | FCR-PAUSE | setLocked(bool)@2804 | property_93c01d6e65b50dce0cbd | E11,E31,E57,E66 |
| finding_91678805d392557165b4 | FCR-PAUSE | setLocked(bool)@2804 | property_b110665920fd9d943b0c | E2,E24,E52 |
| finding_d6a6f0a6811c79a67468 | FCR-FREEZE | lockAddress(address,bool)@2547 | property_a631d6d896efe3cc06af | E27,E41,E49,E68 |
| finding_586412c4d9e53bffeab3 | FCR-FREEZE | lockAddress(address,bool)@2547 | property_9e625388bb7eef25af17 | E21,E53,E69,E7 |
| finding_7e5b441f3cfa7c0e955d | FCR-FREEZE | lockAddress(address,bool)@2547 | property_727d44aa9d48b9eba885 | E13,E34,E46,E67 |
| finding_f0f24628a48b4e3faa14 | FCR-FREEZE | lockAddress(address,bool)@2547 | property_bf455539df4dcf52a684 | E28,E3,E56 |



该成员共 2 次真实提交；选定报告登记 125 项调查动作、279 条查询记录（sat×189、unsat×90），底层求解 330 次。反馈登记消费 1 行；检查点类别 FCR-FREEZE×8、FCR-PAUSE×4，最终类别 FCR-FREEZE×8、FCR-PAUSE×4。

可核对的检查示例：`probe_24369fe1dbccfbe39ad5`，control_transition_preservation → unsat，条件摘要 `b93ff89536ef0fdbfd8ae4b144283de865009b00b55658f4481242a588f8c197`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4665/13130 | 35646798aa1a | 4da581a3f05a |
| main/1 | focused_revision | stop/analysis_received | 5070/3037 | 0009bfc2e8cf | 92398f2cf1b1 |



选定来源：main；报告 SHA-256 `4aa5b58bc46adaac233bb21905afb3a27140b3b533439253c4cc1f7a02a286b4`；报告位于原归档 `run/members/RQ1_1a94f7866801/attempt_1/analysis/report.json`。

## RQ1_af7c473b8cca

MINT · 风险端。检测状态：U+。前批 → 本批：检出 → 未知。配对成员 [RQ1_4be3030c4533](FCR_01.md#rq1_4be3030c4533)。

本轮已选输出 未知；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类性质已进入检查，指定类仍有 19 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | mintToken(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i3::FCR-MINT | setPrices(uint256,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×35、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×13、open/decisive_property_or_source_residual×6。与最终指定类性质标识严格相同的查询结果：unsat×9、sat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_a50c5365c9e2e5823a34 | FCR-TRANSFER | mintToken(address,uint256)@6472 | property_bcec8514986f7091901c | E23,E52,E64,E66,E70,E74,E78 |
| finding_59583d1b948902ec3443 | FCR-FREEZE | freezeAccount(address,bool)@6806 | property_346941ad41d25a594f8e | E10,E13,E2,E20,E26,E30,E34,E6 |
| finding_0c18e7affc404e5a9490 | FCR-TRANSFER | setPrices(uint256,uint256)@7040 | property_a3535129c81492b1b13a | E18,E71,E73,E75,E77 |



该成员共 1 次真实提交；选定报告登记 78 项调查动作、114 条查询记录（unsat×54、sat×49、unknown×11），底层求解 96 次。反馈登记消费 0 行；检查点类别 FCR-TRANSFER×2、FCR-FREEZE×1，最终类别 FCR-TRANSFER×2、FCR-FREEZE×1。

可核对的检查示例：`probe_9bc7191ad2e603297ede`，baseline_usable → sat，条件摘要 `fbae2cff5b559479b88f63fa303fce92967790d43aaca1f27044e90a12d8dcf0`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4114/14532 | 39950d1808d8 | 33d080e9b0ec |



选定来源：main；报告 SHA-256 `1c0c159ba95ad809e5f1d3ae3af9f7d402e2ee56ce3c0e5b404391d163bd4df0`；报告位于原归档 `run/members/RQ1_af7c473b8cca/attempt_1/analysis/report.json`。

## RQ1_35f857af5c9e

PAUSE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_cda3df36df22](FCR_11.md#rq1_cda3df36df22)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 6 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| obligation_question_b0e79d25c2de49ee | start() | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×10、all_source_control_writers_excluded_for_this_use×2、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×7、open/relevant_source_scope_without_resolved_property×5、open/decisive_property_or_source_residual×1。与最终指定类性质标识严格相同的查询结果：unsat×2。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 31 项调查动作、8 条查询记录（sat×5、unsat×3），底层求解 12 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_1235f3a6eaf73ac7cbb8`，baseline_usable → sat，条件摘要 `51b440f1333c49cdc11f7397b5df021cd1e2446b839ead3e112c9a57bea02385`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2458/11344 | 78f96a9e96ae | 2fdaa61dd4da |
| main/1 | focused_revision | stop/analysis_received | 3208/1910 | dc15686afe5c | 5a0a1468b93f |



选定来源：main；报告 SHA-256 `e994c47a3e43f79d8b9523bcc15bcfc6088d8fae26f8eee0c8c69bf57bc47144`；报告位于原归档 `run/members/RQ1_35f857af5c9e/attempt_1/analysis/report.json`。
