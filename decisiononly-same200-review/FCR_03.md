# FCR 逐例复核 · 第 3 页

[返回成员索引](CaseIndex.md)

## RQ1_e1ce695fff9e

DESTROY · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_bcafc7a40ce2](FCR_10.md#rq1_bcafc7a40ce2)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 4 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | destroy(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i2::FCR-DESTROY | destroy(address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |


前批指定类义务依据：source_effect_and_privilege_relevance×9。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×3、excluded/committed_exits_have_no_state_or_external_effect×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 18 项调查动作、5 条查询记录（sat×4、unsat×1），底层求解 6 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_554edd1149eb6bacc460`，original_path_commit → sat，条件摘要 `5012bdf3a1d8be7d689c362874e6ce375ee603a642e69e45677fdfa650bbbe10`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1826/7421 | c12ea8872b1f | 8439e49eb31d |
| main/1 | focused_revision | stop/analysis_received | 2702/363 | 1bb6df2d4caf | 8c57b1d984a2 |



选定来源：main；报告 SHA-256 `3f56b05ed4a0524cf405d8bc956c06d0ff9b01c3e7fe05162108a95473f1250d`；报告位于原归档 `run/members/RQ1_e1ce695fff9e/attempt_1/analysis/report.json`。

## RQ1_c9626779c857

DESTROY · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_085aaca2f412](FCR_01.md#rq1_085aaca2f412)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | burnFrom(address,uint256) | supported | — |
| i3::FCR-DESTROY | burnFrom(address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×26、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×16、open/decisive_property_or_source_residual×5、open/relevant_source_scope_without_resolved_property×5、excluded/committed_exits_have_no_state_or_external_effect×1。与最终指定类性质标识严格相同的查询结果：sat×2、unsat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_591127958888b54d58d6 | FCR-DESTROY | burnFrom(address,uint256)@3797 | property_bad75523f03758086148 | E12,E14,E2 |
| finding_d8acc5425ffdd56ae3ea | FCR-FREEZE | UserLock(address,bool)@4223 | property_28d0409947ecd79f6013 | E1,E4,E8 |
| finding_c35bc18c1f313317b165 | FCR-DESTROY | burnFrom(address,uint256)@3797 | property_2eb202626aa08ab41066 | E15,E17,E6 |



该成员共 2 次真实提交；选定报告登记 34 项调查动作、26 条查询记录（sat×16、unsat×10），底层求解 16 次。反馈登记消费 1 行；检查点类别 FCR-DESTROY×2、FCR-FREEZE×1，最终类别 FCR-DESTROY×2、FCR-FREEZE×1。

可核对的检查示例：`probe_fabbf64f6f6062a9023b`，control_transition_preservation → sat，条件摘要 `5b2933b7d451095ecd58b24a99b65da3bbbd9564688b11df588b443bb0f17d2a`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2905/9205 | b6576f2ac884 | 86a5f9de7070 |
| main/1 | focused_revision | stop/analysis_received | 5149/5406 | 911894c0d23b | 5815624a79d5 |



选定来源：main；报告 SHA-256 `0f55d61a3418a6737a99eca927120432025236d7bfa3c3bb098584860aa2ea12`；报告位于原归档 `run/members/RQ1_c9626779c857/attempt_1/analysis/report.json`。

## RQ1_c75d73e1c482

MINT · 风险端。检测状态：U+。前批 → 本批：检出 → 未知。配对成员 [RQ1_35e0e8d95f92](FCR_06.md#rq1_35e0e8d95f92)。

本轮已选输出 未知；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类性质已进入检查，指定类仍有 19 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | mintToken(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i4::FCR-MINT | setPrices(uint256,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×38、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×20、open/relevant_source_scope_without_resolved_property×13、open/decisive_property_or_source_residual×6。与最终指定类性质标识严格相同的查询结果：unsat×7、sat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_bcf9a07b86a85cb61827 | FCR-TRANSFER | mintToken(address,uint256)@6283 | property_ff0b471bdda81078898b | E27,E60,E72,E74,E78 |
| finding_219f9334556b84ffbce4 | FCR-FREEZE | freezeAccount(address,bool)@6607 | property_339d9072b332e452e8e9 | E13,E29,E34,E4,E7 |
| finding_64bcaaf3e7a9c40333a9 | FCR-TRANSFER | setPrices(uint256,uint256)@6836 | property_6dfae2425fd47da46f9e | E23,E77,E79 |
| finding_e8c71b474fc45efd60c2 | FCR-FREEZE | freezeAccount(address,bool)@6607 | property_2914051895371d072709 | E14,E17,E39,E44,E9 |



该成员共 1 次真实提交；选定报告登记 79 项调查动作、170 条查询记录（sat×98、unsat×57、unknown×15），底层求解 175 次。反馈登记消费 0 行；检查点类别 FCR-FREEZE×2、FCR-TRANSFER×2，最终类别 FCR-FREEZE×2、FCR-TRANSFER×2。

可核对的检查示例：`probe_564737e707517d1beb08`，control_transition_preservation → sat，条件摘要 `db1fdbd8f587b35cfac6f64c735ee001087fb1537d7b598f3110d635018c1cbb`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4094/12218 | 4f526385c754 | e8740e884b13 |



选定来源：main；报告 SHA-256 `74012e6f3d49ddb3b0bc9165af2704dfb3fc17e64d562e2e987215a3c92fc31c`；报告位于原归档 `run/members/RQ1_c75d73e1c482/attempt_1/analysis/report.json`。

## RQ1_e73c99ca23e5

TRANSFER · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_1f06ce07140f](FCR_05.md#rq1_1f06ce07140f)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1@25c714cf1b4a | zero_fee_transaction(address,address,uint256) | supported | — |
| i1@8e89afcce351 | zero_fee_transaction(address,address,uint256) | supported | — |
| i1@935a2911126d | zero_fee_transaction(address,address,uint256) | supported | — |
| obligation_question_4100c968f71423e3 | transferFrom(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_542ea3d410ef358e | transfer(address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_6081f6f3f02ddf9e | transferFrom(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_812805187d98518b | transfer(address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_a90498129fb24e57 | transfer(address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_c0318c70216d909f | transferFrom(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_cf8dd3ebb518fecd | transfer(address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×43、source_positions_and_resolved_properties×7。本次：excluded/compiler_generated_readonly_getter×16、open/decisive_property_or_source_residual×12、open/relevant_source_scope_without_resolved_property×11、excluded/committed_exits_have_no_state_or_external_effect×7、excluded/source_positions_and_resolved_properties×3、excluded/all_extracted_exits_revert×1。与最终指定类性质标识严格相同的查询结果：unsat×34、sat×6。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_3449d6fa9904e3c87e6d | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@4852 | property_7c2afa4d290b5b1c8933 | E12,E43,E48,E53 |
| finding_6d55ad196420d659ea0f | FCR-DESTROY | zero_fee_transaction(address,address,uint256)@4852 | property_dd4df6618c2bb8f652b9 | E13,E25,E33,E38 |
| finding_001d7b9f3d06e395c785 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@4852 | property_fb6bf30dd1a4695b7f94 | E20,E4,E44,E54,E58 |
| finding_331b64d935538a65e3e5 | FCR-DESTROY | zero_fee_transaction(address,address,uint256)@4852 | property_65ffb5adcc80249c0114 | E28,E34,E39,E49,E9 |
| finding_f413a65fd901ff23c6ed | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@4852 | property_643422205024a75ff07b | E24,E52,E57,E61,E8 |
| finding_2b5d67058a2038d422a4 | FCR-DESTROY | zero_fee_transaction(address,address,uint256)@4852 | property_e9fd3044fcd45ca5d0ea | E10,E32,E37,E42,E47 |
| finding_5d6c0f6aab1e594037a0 | FCR-PAUSE | pause()@3551 | property_ce59b8443a7efa35798e | E1,E16,E26,E3,E6 |
| finding_27792fc061d02319f3ec | FCR-PAUSE | pause()@3551 | property_480e26582a0672ec06d9 | E17,E2,E27,E5,E7 |



该成员共 2 次真实提交；选定报告登记 72 项调查动作、129 条查询记录（unsat×100、sat×29），底层求解 61 次。反馈登记消费 1 行；检查点类别 FCR-DESTROY×3、FCR-TRANSFER×3、FCR-PAUSE×2，最终类别 FCR-DESTROY×3、FCR-TRANSFER×3、FCR-PAUSE×2。

可核对的检查示例：`probe_0fba97cb3bfe63e1553f`，financial_value_post_exclusion → unsat，条件摘要 `bad363225fe7698ee24fadafb5f79da1eddf603089721713a9474f481ccb63dc`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4591/13394 | 72c92eb3f388 | 98067764fd98 |
| main/1 | focused_revision | stop/analysis_received | 8054/2073 | 7bb1cbfea356 | 6240116427ee |



选定来源：main；报告 SHA-256 `465d7cd28bf41423c9558c8c03ded16d83563d0ccb62016bd8bb7fa78b4aa4e7`；报告位于原归档 `run/members/RQ1_e73c99ca23e5/attempt_1/analysis/report.json`。

## RQ1_c772c59e4a76

FREEZE · 风险端。检测状态：TP。前批 → 本批：未知 → 检出。配对成员 [RQ1_a7bf9487cc3f](FCR_02.md#rq1_a7bf9487cc3f)。

本轮已选输出 检出；前次同 200 份 未知；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i3 | freezeAccount(address,bool) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×33、relevant_source_scope_without_resolved_property×2、decisive_property_or_source_residual×1。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×16、open/decisive_property_or_source_residual×2、open/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：sat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_0668de84680a979e43c4 | FCR-MINT | mintToken(address,uint256)@6499 | property_7de8e22f95422422eb06 | E17,E32,E54,E55,E57,E58,E59,E61 |
| finding_d6b732d62c48493f42f9 | FCR-TRANSFER | mintToken(address,uint256)@6499 | property_4e30079054fdd0284e02 | E21,E44,E46,E47,E49,E50,E51,E53,E72 |
| finding_7d1e1c93832da0e4b09e | FCR-FREEZE | freezeAccount(address,bool)@6862 | property_ccc29183b5a58a0ed4f8 | E15,E2,E20,E28,E5,E9 |
| finding_d51e13c7b3db9ac94a5d | FCR-MINT | mintToken(address,uint256)@6499 | property_1353a874974079110b6c | E25,E52,E70,E71,E73,E74,E75,E77 |
| finding_f37f9a5012061e7b5b79 | FCR-TRANSFER | mintToken(address,uint256)@6499 | property_9449562aa9743c202b68 | E27,E60,E80,E81 |



该成员共 2 次真实提交；选定报告登记 81 项调查动作、122 条查询记录（unsat×76、sat×35、unknown×11），底层求解 74 次。反馈登记消费 1 行；检查点类别 FCR-MINT×2、FCR-TRANSFER×2、FCR-FREEZE×1，最终类别 FCR-MINT×2、FCR-TRANSFER×2、FCR-FREEZE×1。

可核对的检查示例：`probe_c8f869a9c4b0a3268579`，baseline_usable → sat，条件摘要 `e8a83b03e1b0807c298eb0f4f55a296e1bdb0cb0882dcfe2b54ef2caca022cac`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4218/15046 | c77a696daa38 | 4c2cf7149796 |
| main/1 | focused_revision | stop/analysis_received | 6319/1833 | 4fa64cf15648 | 7993f099dd4b |



选定来源：main；报告 SHA-256 `406cfeccae4e71360910881be5ed235d1da063580df7098dee5d7412c1a211f3`；报告位于原归档 `run/members/RQ1_c772c59e4a76/attempt_1/analysis/report.json`。

## RQ1_32dbc2fa2433

PAUSE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_c24c6c95ccbd](FCR_02.md#rq1_c24c6c95ccbd)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 8 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×12。本次：open/relevant_source_scope_without_resolved_property×5、excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×3。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 33 项调查动作、8 条查询记录（sat×4、unsat×4），底层求解 8 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_1fc3f0633308bd0076e5`，original_path_commit → sat，条件摘要 `07277abb40886c823b71bce6a928ed86f99b9da3f8b9e73bf29f8c72c49723e3`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2222/16693 | 4ef18e900d3b | f3e9db4220aa |
| main/1 | focused_revision | stop/analysis_received | 3014/10422 | c70d3bc916e5 | 7fe9597506a0 |



选定来源：main；报告 SHA-256 `670888afa6fd4f024d8f21a9f5f999bda2882b8532df04e06d4fa2d3a4e141ca`；报告位于原归档 `run/members/RQ1_32dbc2fa2433/attempt_1/analysis/report.json`。

## RQ1_94d9f2cfc77c

MINT · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_e13bb6580d65](FCR_11.md#rq1_e13bb6580d65)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 13 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×26。本次：excluded/committed_exits_have_no_state_or_external_effect×13、open/relevant_source_scope_without_resolved_property×7、open/decisive_property_or_source_residual×6。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 32 项调查动作、12 条查询记录（sat×11、unsat×1），底层求解 11 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_a3bc52b2f23ca4cb478f`，baseline_usable → sat，条件摘要 `7bdd3cf8e907303f2381e1e456f74b38eeb46a1bcbfbe4426c4ad925773b16ba`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 6367/6751 | 00261aa81cfb | 65f9964a48c3 |
| main/1 | focused_revision | stop/analysis_received | 7251/1090 | 2468164ef538 | 664429e959ee |



选定来源：main；报告 SHA-256 `c0f616d9660fa63415e3d16f3ee647663a238c353258de1d20054bde37fa0ddb`；报告位于原归档 `run/members/RQ1_94d9f2cfc77c/attempt_1/analysis/report.json`。

## RQ1_4169c528c5e4

MINT · 风险端。检测状态：U+。前批 → 本批：检出 → 未知。配对成员 [RQ1_2d22977434b5](FCR_07.md#rq1_2d22977434b5)。

本轮已选输出 未知；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

MINT 风险版退为未知。mintToken 上有实际报警，类别是 TRANSFER；其余 FREEZE 也不能抵销 MINT。两项 MINT 性质都未建立完整金融条件。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | mintToken(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i4::FCR-MINT | setPrices(uint256,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×35、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×15、open/decisive_property_or_source_residual×4。与最终指定类性质标识严格相同的查询结果：unsat×5、sat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_08a359e66bf1ab47f2c6 | FCR-TRANSFER | mintToken(address,uint256)@6499 | property_3ab984b611c81d570beb | E23,E59,E61,E63,E65,E67,E69,E71 |
| finding_9befac1bc20f3f4444c0 | FCR-FREEZE | freezeAccount(address,bool)@6862 | property_c3bac69476321e6bd889 | E10,E14,E24,E28,E3,E32,E36,E40,E48,E52,E6 |



该成员共 1 次真实提交；选定报告登记 76 项调查动作、193 条查询记录（sat×98、unsat×74、unknown×21），底层求解 191 次。反馈登记消费 0 行；检查点类别 FCR-FREEZE×1、FCR-TRANSFER×1，最终类别 FCR-FREEZE×1、FCR-TRANSFER×1。

可核对的检查示例：`probe_332263552837af2de14c`，control_transition_preservation → sat，条件摘要 `664ce638be1493dd59fbbae5f67d84eb664a65840d8f9d156fd7eeda65ca2268`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4218/10652 | c77a696daa38 | d74c25195b23 |



选定来源：main；报告 SHA-256 `e5e4dca9113e207eeebbbad15dcff985da71bba4797e46d1a40821f1fd3611ee`；报告位于原归档 `run/members/RQ1_4169c528c5e4/attempt_1/analysis/report.json`。

## RQ1_475c7d9ec738

PAUSE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_b84042e6eefd](FCR_09.md#rq1_b84042e6eefd)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 2 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | disableTransfers(bool) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×6。本次：excluded/compiler_generated_readonly_getter×2、open/relevant_source_scope_without_resolved_property×2、excluded/committed_exits_have_no_state_or_external_effect×1、excluded/isolated_flag_no_nongenerated_reader_in_resolved_public_bodies×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 1 次真实提交；选定报告登记 13 项调查动作、3 条查询记录（sat×2、unsat×1），底层求解 3 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_32d04fa675f16226a1bd`，baseline_usable → sat，条件摘要 `3a347278c34bcf6e9d812d62823ffc0dfc58b39f900d3e0ac917797f60222f9f`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1752/10764 | abe2f1de5811 | 4be54374b11c |



选定来源：main；报告 SHA-256 `230a8d9ef2f99bcc75429adc863beebd6f861a5ccf9c73dc89e5a0d290cf5d00`；报告位于原归档 `run/members/RQ1_475c7d9ec738/attempt_1/analysis/report.json`。

## RQ1_30c29cd44cad

DESTROY · 风险端。检测状态：TP。前批 → 本批：未知 → 检出。配对成员 [RQ1_329e0d0d7a11](FCR_07.md#rq1_329e0d0d7a11)。

本轮已选输出 检出；前次同 200 份 未知；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

前次风险端 DESTROY 为未知，本次在 destroy 入口出现指定类报警，初始检查点尚无该类，反馈行记录消费及 finding 变化。两条对应性质的查询均为 SAT。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i5 | destroy(address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×11、decisive_property_or_source_residual×1。本次：excluded/compiler_generated_readonly_getter×4、open/relevant_source_scope_without_resolved_property×4、open/decisive_property_or_source_residual×3、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：sat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_a6d46ac3d5b1f6248224 | FCR-DESTROY | destroy(address,uint256)@971 | property_882d3d3d31d0d71788fc | E11,E18,E8 |



该成员共 2 次真实提交；选定报告登记 18 项调查动作、3 条查询记录（sat×3），底层求解 3 次。反馈登记消费 1 行；检查点类别 无，最终类别 FCR-DESTROY×1。

可核对的检查示例：`probe_514cac8a7994974c4cdc`，local_premises_feasible → sat，条件摘要 `6a74848f3a4d475a9b583af13801c56d7545184aade2e0f59b21256affbc2bf5`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2063/13392 | 02aea65d0a94 | 2fddb4714b27 |
| main/1 | focused_revision | stop/analysis_received | 2382/8372 | d90c2d83fb61 | c83428882f77 |



选定来源：main；报告 SHA-256 `1257efa086ad80db7b57f6e68109599120a5d6fa88601c16b54790900a7930d2`；报告位于原归档 `run/members/RQ1_30c29cd44cad/attempt_1/analysis/report.json`。
