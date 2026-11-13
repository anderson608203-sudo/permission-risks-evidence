# FCR 逐例复核 · 第 4 页

[返回成员索引](CaseIndex.md)

## RQ1_49db443acf1d

TRANSFER · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_4febca8bfe3b](FCR_07.md#rq1_4febca8bfe3b)。

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
| main/0 | initial | stop/analysis_received | 1523/1961 | 1638647d3974 | 6d3494defb1b |
| main/1 | focused_revision | stop/analysis_received | 2362/1739 | c15f5ae7f15a | 95be327d90ab |



选定来源：main；报告 SHA-256 `2010f1e8a32a0bcd5310d3d7563ca68f012783bc6a9b615c41f3a70b9fbdb91b`；报告位于原归档 `run/members/RQ1_49db443acf1d/attempt_1/analysis/report.json`。

## RQ1_7bfd58ffb1ae

MINT · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_cb8c3fafbda1](FCR_01.md#rq1_cb8c3fafbda1)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 检出

指定类性质已进入检查，指定类仍有 19 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | mintToken(uint256) | 未确认 | financial_property_conditions_not_established |
| i5::FCR-MINT | setPrices(uint256,uint256) | 未确认 | financial_property_conditions_not_established |
| i6 | mintToken(uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×36。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×13、open/decisive_property_or_source_residual×6。与最终指定类性质标识严格相同的查询结果：unsat×3、sat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_523eef811c60cb06c00d | FCR-TRANSFER | setPrices(uint256,uint256)@6810 | property_d5c3d97790f939313340 | E14,E32,E61,E62,E63,E65,E66,E67,E69,E70 |



该成员共 2 次真实提交；选定报告登记 74 项调查动作、49 条查询记录（sat×34、unsat×10、unknown×5），底层求解 51 次。反馈登记消费 1 行；检查点类别 FCR-TRANSFER×1，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_09ee29b0db73159f7d25`，financial_value_post_exclusion → sat，条件摘要 `cbbeafd1f1ffcecb0d36213a7403904bd7c6150eb7c6f40d04cc48d007809680`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3967/14188 | 75a80496a41b | a53f9b495131 |
| main/1 | focused_revision | stop/analysis_received | 5020/2417 | ab66c1d56560 | 47b7b6c24f92 |



选定来源：main；报告 SHA-256 `dc16da8c7deb5161f15295170940742eb99be60443e898cedf1a8d74e6b15391`；报告位于原归档 `run/members/RQ1_7bfd58ffb1ae/attempt_1/analysis/report.json`。

## RQ1_196284e657b0

DESTROY · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_0bf6f8bce8d9](FCR_10.md#rq1_0bf6f8bce8d9)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类初始未出现，最终已形成发现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | destroy(address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×8、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×3、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：sat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_aada00bcd84fe7f367a2 | FCR-DESTROY | destroy(address,uint256)@790 | property_43d2b90ad9e1ad73a641 | E12,E13,E2,E7 |



该成员共 2 次真实提交；选定报告登记 13 项调查动作、3 条查询记录（sat×3），底层求解 3 次。反馈登记消费 1 行；检查点类别 无，最终类别 FCR-DESTROY×1。

可核对的检查示例：`probe_ef122b7a443a6bf86fbf`，local_premises_feasible → sat，条件摘要 `f396a89c55333e83d28ed5c0df13cff0254832abdceb03f7273021f33a5c67ec`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2139/13761 | a4c691c08464 | 91ce6f3e3d20 |
| main/1 | focused_revision | stop/analysis_received | 2624/8402 | 0c053aa30b93 | 31968fa45cdc |



选定来源：main；报告 SHA-256 `02db0996e299520d5276c9c9fdbef6b62b1962cb78c8069d021fcb88e6693063`；报告位于原归档 `run/members/RQ1_196284e657b0/attempt_1/analysis/report.json`。

## RQ1_7d7240a2af90

TRANSFER · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_8d60a47186e2](FCR_10.md#rq1_8d60a47186e2)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | supported | — |
| i2::FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | supported | — |
| i3 | transfer(address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |
| i4 | zero_fee_transaction(address,address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×3、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×2、excluded/source_positions_and_resolved_properties×2。与最终指定类性质标识严格相同的查询结果：sat×9、unsat×3。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_79cd573ce7fecbc79df6 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@634 | property_45211031a65017b6be95 | E2,E7 |
| finding_f19af6cfa62a158e8cca | FCR-DESTROY | zero_fee_transaction(address,address,uint256)@634 | property_4d0a829868b4600c69e7 | E3,E8 |
| finding_a095d73dc1a2bfad6e18 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@634 | property_bc33fb0adcfb3004b988 | E5,E9 |
| finding_929e697cb9c5a74e751b | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@634 | property_364ace78287e30713e8d | E10,E6 |



该成员共 1 次真实提交；选定报告登记 10 项调查动作、16 条查询记录（sat×12、unsat×4），底层求解 5 次。反馈登记消费 0 行；检查点类别 FCR-TRANSFER×3、FCR-DESTROY×1，最终类别 FCR-TRANSFER×3、FCR-DESTROY×1。

可核对的检查示例：`probe_bd1f03aab697d06afa80`，local_premises_feasible → sat，条件摘要 `6585b8a1875c5ea62c58a2109159de8b3b45a9688f70d518e43e100efb155cf7`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1601/7375 | 77f4cccce199 | 270f6714e842 |



选定来源：main；报告 SHA-256 `62c93559b36c8f7d12d8b54fc6d76303b109afe4b1da78eccb0992ac99978a47`；报告位于原归档 `run/members/RQ1_7d7240a2af90/attempt_1/analysis/report.json`。

## RQ1_fbd0377ce541

PAUSE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_8e8598bb724e](FCR_12.md#rq1_8e8598bb724e)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 5 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | transferOwnership(address) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×21。本次：excluded/compiler_generated_readonly_getter×12、open/relevant_source_scope_without_resolved_property×4、excluded/committed_exits_have_no_state_or_external_effect×2、excluded/isolated_flag_no_nongenerated_reader_in_resolved_public_bodies×2、open/decisive_property_or_source_residual×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 14 项调查动作、9 条查询记录（sat×7、unsat×2），底层求解 9 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_34c37183c465b37618e4`，baseline_usable → sat，条件摘要 `4eda302105b372dd6af673afaea8ef2f5c26033b37eacc7c724687be19dd11e9`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2994/6539 | 982862512f51 | 98f3fb66d856 |
| main/1 | focused_revision | stop/analysis_received | 3663/1588 | 06260bb6cab3 | 10680c2c5387 |



选定来源：main；报告 SHA-256 `b26c66b674da744a9ec95aa776dfb5baa1a42887c0429e158df3e2326e183027`；报告位于原归档 `run/members/RQ1_fbd0377ce541/attempt_1/analysis/report.json`。

## RQ1_39fb6e7197c4

FREEZE · 风险端。检测状态：U+。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_7450d39da940](FCR_12.md#rq1_7450d39da940)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 16 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | transferOwnership(address) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×31。本次：excluded/compiler_generated_readonly_getter×15、open/decisive_property_or_source_residual×14、open/relevant_source_scope_without_resolved_property×2。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 78 项调查动作、6 条查询记录（sat×3、unsat×3），底层求解 5 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_000ce4996d72eb49a25d`，baseline_usable → sat，条件摘要 `d609116f6e02fefe6acb521e604ee9ee34ea99dc0baade0432d4e6dbe4805dac`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4102/15248 | b38ac7c8ecd3 | d082f611f80c |
| main/1 | focused_revision | stop/analysis_received | 6586/14960 | 945bebf32dd9 | 5e76d978e8c3 |



选定来源：main；报告 SHA-256 `8df1edff8d09c50b8c59720bb0df34f702b75f9b0a8e0caa9fe893c201463865`；报告位于原归档 `run/members/RQ1_39fb6e7197c4/attempt_1/analysis/report.json`。

## RQ1_9451d6dac4de

TRANSFER · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_e25d32acc1f7](FCR_06.md#rq1_e25d32acc1f7)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类初始未出现，最终已形成发现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i3 | zero_fee_transaction(address,address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×8、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×2、excluded/committed_exits_have_no_state_or_external_effect×1、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：sat×3、unsat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_434e35f19c83ea6f7c8e | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@536 | property_30de8df06c4e05783ae5 | E1,E13,E14,E8 |



该成员共 2 次真实提交；选定报告登记 14 项调查动作、9 条查询记录（sat×7、unsat×2），底层求解 9 次。反馈登记消费 1 行；检查点类别 无，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_511ff10f86107033ed1d`，local_premises_feasible → sat，条件摘要 `af589214641050b0a90d87a3eecf85000811c0e8835fdf6b2692ebfa931f2ef9`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1919/7704 | 8925c0ed84fc | 2b26b5d52798 |
| main/1 | focused_revision | stop/analysis_received | 2395/4123 | 588203194579 | 5200b31535e4 |



选定来源：main；报告 SHA-256 `3fe4f1c338766a03af13e42e54988dc104677e1ce60b235fd0c1e7e5d1c30a78`；报告位于原归档 `run/members/RQ1_9451d6dac4de/attempt_1/analysis/report.json`。

## RQ1_353a9b0b5006

DESTROY · 风险端。检测状态：U+。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_db11e3e08742](FCR_09.md#rq1_db11e3e08742)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 检出

真实工程门的量化查询存在未决边界。此次风险端保留 DESTROY 义务仍未确认，不能据提示名或 burn 名称判断净损。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1::FCR-DESTROY | burn(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i3 | transferFrom(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_a12f72e825d88d46::FCR-DESTROY | SetBurnPercent(uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_a593d3d289cb9d57::FCR-DESTROY | SetCharityPercent(uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×32。本次：excluded/compiler_generated_readonly_getter×12、open/decisive_property_or_source_residual×7、open/relevant_source_scope_without_resolved_property×7、excluded/committed_exits_have_no_state_or_external_effect×6。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 95 项调查动作、77 条查询记录（unsat×42、sat×34、unknown×1），底层求解 123 次。反馈登记消费 0 行；检查点类别 FCR-MINT×1，最终类别 无。

可核对的检查示例：`probe_5bf0338d076150d2aee4`，control_transition_preservation → sat，条件摘要 `d2eec24695afc967e525dc2f3fdd1730bbe5395dc304924dbff46f5cfad76fa3`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 6155/16567 | f4c70eef7960 | 2eb91500b9d3 |
| main/1 | focused_revision | stop/analysis_received | 7313/2563 | cc68d8c596d7 | dc1db18a0277 |



选定来源：main；报告 SHA-256 `07ad639dc75d1fcbc558bd47e8a867a1828b0c96491dc0f08985b2e070a8806e`；报告位于原归档 `run/members/RQ1_353a9b0b5006/attempt_1/analysis/report.json`。

## RQ1_72c6b8c6b605

TRANSFER · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_b5217318672e](FCR_10.md#rq1_b5217318672e)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 3 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |


前批指定类义务依据：source_effect_and_privilege_relevance×9。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×2、excluded/committed_exits_have_no_state_or_external_effect×1、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 13 项调查动作、5 条查询记录（sat×4、unsat×1），底层求解 6 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_3f3d8292730c84b10f89`，original_path_commit → sat，条件摘要 `d35f94d131e7971d8ecb230d0d64d4a80f3ed381e4ca759fb53147b771473a20`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1917/16966 | 4acc3b8b63ae | dca22678ca00 |
| main/1 | focused_revision | stop/analysis_received | 3128/6188 | f9598875a2f4 | 4804e51fa759 |



选定来源：main；报告 SHA-256 `344e23592f06a40c71fe5d93bdd000e69c22d94cfe734be4af3115bc586eb225`；报告位于原归档 `run/members/RQ1_72c6b8c6b605/attempt_1/analysis/report.json`。

## RQ1_86a0269d7608

MINT · 修复端。检测状态：U-。前批 → 本批：未知 → 未知。配对成员 [RQ1_a0facbcc1e38](FCR_12.md#rq1_a0facbcc1e38)。

本轮已选输出 未知；前次同 200 份 未知；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 17 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | mintToken(uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_fb2c14f3f720a1f8 | redeem() | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×42、decisive_property_or_source_residual×1、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×23、open/relevant_source_scope_without_resolved_property×9、open/decisive_property_or_source_residual×8、excluded/committed_exits_have_no_state_or_external_effect×4。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 77 项调查动作、15 条查询记录（sat×8、unsat×7），底层求解 16 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_eaa8db6b1c3e10580af7`，baseline_usable → sat，条件摘要 `a591c9b3eab2d704ef45132fc79190ac1076e673a08661033ce51aa76d7c4cf1`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 7725/19521 | c5c9633b7249 | 17026212dec7 |
| main/1 | focused_revision | stop/analysis_received | 8634/18191 | 0e747db224a5 | 769f28d33b8b |



选定来源：main；报告 SHA-256 `b049fe0f1234910b79bd9b7e99ba13167e267f2dd753b781b8357c1c64fbd115`；报告位于原归档 `run/members/RQ1_86a0269d7608/attempt_1/analysis/report.json`。
