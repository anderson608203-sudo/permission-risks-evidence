# FCR 逐例复核 · 第 7 页

[返回成员索引](CaseIndex.md)

## RQ1_18c85d7f1380

MINT · 风险端。检测状态：U+。前批 → 本批：检出 → 未知。配对成员 [RQ1_983137cbe5d6](FCR_11.md#rq1_983137cbe5d6)。

本轮已选输出 未知；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类性质已进入检查，指定类仍有 19 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | mintToken(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i4::FCR-MINT | setPrices(uint256,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×35、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×13、open/decisive_property_or_source_residual×6。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_eb4a657e75b5eeffb468 | FCR-FREEZE | freezeAccount(address,bool)@6606 | property_449dbf39c0a3e693da8b | E13,E25,E37,E51,E6 |
| finding_8fc33a05e62a4908f421 | FCR-FREEZE | freezeAccount(address,bool)@6606 | property_2614ebe5e489b9494cea | E14,E2,E27,E57,E63,E69,E7 |



该成员共 1 次真实提交；选定报告登记 83 项调查动作、165 条查询记录（sat×94、unsat×56、unknown×15），底层求解 179 次。反馈登记消费 0 行；检查点类别 FCR-FREEZE×2，最终类别 FCR-FREEZE×2。

可核对的检查示例：`probe_93dff20203a659951ad6`，control_transition_preservation → sat，条件摘要 `7a150f007f8e2b8b35d3dbd688450d9165d24ef7a7df04ec84c2348ad05b6013`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4061/13144 | 18165dccc773 | 30a28f6ed57c |



选定来源：main；报告 SHA-256 `5a1736dc08314f619dafbbee3161af7102571a6aa8027ce00db7a5b0208a5b41`；报告位于原归档 `run/members/RQ1_18c85d7f1380/attempt_1/analysis/report.json`。

## RQ1_55a1e2ef0f09

DESTROY · 风险端。检测状态：U+。前批 → 本批：未知 → 未知。配对成员 [RQ1_fe4ace2cd8e5](FCR_09.md#rq1_fe4ace2cd8e5)。

本轮已选输出 未知；前次同 200 份 未知；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 检出

指定类性质已进入检查，指定类仍有 14 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1::FCR-DESTROY | setCrowdfundAddress(address) | 未确认 | financial_property_conditions_not_established |
| i2::FCR-DESTROY | deliverPresaleFuelBalances(address[],uint256[]) | 未确认 | financial_property_conditions_not_established |
| i3::FCR-DESTROY | releaseVanbexTeamTokens() | 未确认 | financial_property_conditions_not_established |
| i4 | finalizeCrowdfund() | 未确认 | financial_property_conditions_not_established |
| i8::FCR-DESTROY | finalizePresale() | 未确认 | financial_property_conditions_not_established |
| obligation_question_73e3cb1eb5764c06::FCR-DESTROY | transferFromCrowdfund(address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×37、decisive_property_or_source_residual×1。本次：excluded/compiler_generated_readonly_getter×22、open/decisive_property_or_source_residual×7、open/relevant_source_scope_without_resolved_property×7、excluded/committed_exits_have_no_state_or_external_effect×2。与最终指定类性质标识严格相同的查询结果：unsat×20。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_c47dfd5e34282f9c3d45 | FCR-MINT | setCrowdfundAddress(address)@8249 | property_dcdeacda53f51c2fa63e | E24,E36 |
| finding_afbc6bc09f2b89895531 | FCR-MINT | releaseVanbexTeamTokens()@9640 | property_ab68e90d68df0c5a2bbd | E52,E8 |
| finding_378799f236830fb7f0f4 | FCR-MINT | finalizePresale()@10206 | property_3a72685b84c81d008e35 | E22,E48 |



该成员共 1 次真实提交；选定报告登记 83 项调查动作、53 条查询记录（unsat×44、sat×9），底层求解 33 次。反馈登记消费 0 行；检查点类别 FCR-MINT×3，最终类别 FCR-MINT×3。

可核对的检查示例：`probe_76faff3ce0385821fb5f`，financial_value_post_exclusion → sat，条件摘要 `3f9e7072aff975768266b308905949a1adac75bcbdd4b290dc94b41f0aa6f478`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 5655/12859 | 0c0ed61a1ffc | 0bb19a17f86f |



选定来源：main；报告 SHA-256 `37c43af5e5e3871b4d08583c8d2450fc6eb0ae0b8ed318dbd87831707a077a93`；报告位于原归档 `run/members/RQ1_55a1e2ef0f09/attempt_1/analysis/report.json`。

## RQ1_2d22977434b5

MINT · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_4169c528c5e4](FCR_03.md#rq1_4169c528c5e4)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 18 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | totalSupply() | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×35。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×14、open/decisive_property_or_source_residual×4。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 1 次真实提交；选定报告登记 76 项调查动作、71 条查询记录（sat×56、unsat×9、unknown×6），底层求解 77 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_51a06ec67ece08a02e77`，prefix_reachability → sat，条件摘要 `3a393c9c730bd358eaedbb42440fc3d630b87c6701300adffb74dec1613e6646`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3976/21160 | 14cfb2c0fa28 | 24fcb0069b77 |



选定来源：main；报告 SHA-256 `4614022af08102771b18a3ec49b2d2c45660ddf47302ba030ca154b185f64462`；报告位于原归档 `run/members/RQ1_2d22977434b5/attempt_1/analysis/report.json`。

## RQ1_4febca8bfe3b

TRANSFER · 风险端。检测状态：U+。前批 → 本批：检出 → 未知。配对成员 [RQ1_49db443acf1d](FCR_04.md#rq1_49db443acf1d)。

本轮已选输出 未知；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

TRANSFER 解释已经编入至少一个性质，但最终查询数为零；有类别不明确及错反馈范围诊断。记录不能确定哪一条诊断单独造成漏检。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×3、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×2、excluded/source_bound_counter_only_no_outgoing_effect_dependence×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 4 项调查动作、0 条查询记录（无），底层求解 0 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：无已保存的程序查询。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1547/5075 | c01440a76c01 | 78f02ce5f728 |
| main/1 | focused_revision | stop/analysis_received | 2336/7588 | e12467e1fbb1 | f58d153c7212 |



选定来源：main；报告 SHA-256 `274ceb3d8ddf38031c17e2ec84d0a3c0122c46b699d7b9e1b28254ac20ffbf16`；报告位于原归档 `run/members/RQ1_4febca8bfe3b/attempt_1/analysis/report.json`。

## RQ1_3455b6a9ba4f

TRANSFER · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_0c666ce785e8](FCR_01.md#rq1_0c666ce785e8)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 3 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |


前批指定类义务依据：source_effect_and_privilege_relevance×9。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×2、excluded/committed_exits_have_no_state_or_external_effect×1、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 13 项调查动作、5 条查询记录（sat×4、unsat×1），底层求解 6 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_5d0af1c720562e43feec`，original_path_commit → sat，条件摘要 `0884040d4d6e77db3116096d2ac134f5d91d991888b0f1c70ac032975f52b06b`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1888/8121 | 00b0124b8699 | 9f66a056f550 |
| main/1 | focused_revision | stop/analysis_received | 3184/3445 | d167a11489a0 | 73361540f685 |



选定来源：main；报告 SHA-256 `d9f55e344acfaea70a67015522e7d778e5675dd66b14d9604df4e1724e29bcfc`；报告位于原归档 `run/members/RQ1_3455b6a9ba4f/attempt_1/analysis/report.json`。

## RQ1_3b4d9f6eb96f

MINT · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_0267e2a8ebb2](FCR_01.md#rq1_0267e2a8ebb2)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 18 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×35。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×14、open/decisive_property_or_source_residual×4。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_4fa0d5bfd3ef593fb218 | FCR-TRANSFER | setPrices(uint256,uint256)@6564 | property_df7ece5ee09386722493 | E16,E21,E22,E23,E25,E26,E27,E28,E7 |



该成员共 2 次真实提交；选定报告登记 71 项调查动作、39 条查询记录（sat×26、unsat×8、unknown×5），底层求解 41 次。反馈登记消费 1 行；检查点类别 FCR-TRANSFER×1，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_d2805973dfd1db34c27c`，financial_value_post_exclusion → sat，条件摘要 `71d61e7b1b3caf7856e135b8d372408857d762cfaf4e2786638fe238223989f5`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3889/10664 | 17e277c689a7 | fd79daa9bc63 |
| main/1 | focused_revision | stop/analysis_received | 4477/3052 | 648a7b147741 | 914873eaf21f |



选定来源：main；报告 SHA-256 `4aad40bad2423411ddfc47bfb0cc848ea056c93f33b63008e5b290b153b97fda`；报告位于原归档 `run/members/RQ1_3b4d9f6eb96f/attempt_1/analysis/report.json`。

## RQ1_53f9777ccdf6

TRANSFER · 风险端。检测状态：TP。前批 → 本批：未知 → 检出。配对成员 [RQ1_a7d72c1e4129](FCR_08.md#rq1_a7d72c1e4129)。

本轮已选输出 检出；前次同 200 份 未知；v32 冻结 Full 检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

TRANSFER 风险端从未知到检出；初始检查点未报，之后可定位到同一交易入口、一次已消费反馈和最终指定类证据。没有同版消融以量化独立收益。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| obligation_question_21b4916e0c69cc45 | zero_fee_transaction(address,address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×11、decisive_property_or_source_residual×1。本次：excluded/compiler_generated_readonly_getter×4、open/relevant_source_scope_without_resolved_property×4、open/decisive_property_or_source_residual×3、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：sat×3、unsat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_05f244d64470fd902541 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@801 | property_6002de8c5918f9f4c7c3 | E10,E16 |



该成员共 2 次真实提交；选定报告登记 16 项调查动作、5 条查询记录（sat×4、unsat×1），底层求解 4 次。反馈登记消费 1 行；检查点类别 无，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_bc4382abea3ddfd323d3`，local_premises_feasible → sat，条件摘要 `f9047cca96baed811805a57e79c8d0249f620fe4e4bbf26c03b052e915b23eea`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2167/9622 | e2f82092f009 | edc39e74fb06 |
| main/1 | focused_revision | stop/analysis_received | 3368/13487 | 7b4ba717420b | 61730e43daad |



选定来源：main；报告 SHA-256 `02a51d370c80821f5c23d3f210b7123a711fec46ab2cedfa55829886720363e7`；报告位于原归档 `run/members/RQ1_53f9777ccdf6/attempt_1/analysis/report.json`。

## RQ1_eb30c6dee989

DESTROY · 风险端。检测状态：U+。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_ee2aa7f32d31](FCR_09.md#rq1_ee2aa7f32d31)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 9 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | burnDragons(uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_5190fb88f9638c3a | burnFrom(address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_5ef9947bdc4c2de3 | burn(uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×23、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×9、excluded/committed_exits_have_no_state_or_external_effect×6、open/decisive_property_or_source_residual×6、open/relevant_source_scope_without_resolved_property×3。与最终指定类性质标识严格相同的查询结果：unsat×18、sat×4。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_8bf64938e13efa5f5260 | FCR-TRANSFER | burnDragons(uint256)@3205 | property_93b7075d31714012ac22 | E10,E16,E24,E29,E30,E31,E35 |



该成员共 2 次真实提交；选定报告登记 75 项调查动作、124 条查询记录（unsat×93、sat×31），底层求解 136 次。反馈登记消费 1 行；检查点类别 FCR-TRANSFER×1，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_35966d87b71e21e0f735`，financial_value_post_exclusion → unsat，条件摘要 `7deda24aa7ed429222c995b6cfa30d1317f6290e39ae9c9707b6d5e2c9919741`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3696/17831 | c7fd27217ec8 | d30c47fe3c35 |
| main/1 | focused_revision | stop/analysis_received | 6305/1522 | de2437028b1c | 45dd961ffe86 |



选定来源：main；报告 SHA-256 `421db6b9ca6c529d06a1dc9f9804bd63bc22ed82296799afa9128043bfcab0a4`；报告位于原归档 `run/members/RQ1_eb30c6dee989/attempt_1/analysis/report.json`。

## RQ1_4f9f1ce04ed8

PAUSE · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_b0a696b11b0a](FCR_06.md#rq1_b0a696b11b0a)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 有效未检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2::FCR-PAUSE | transfer_test(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i5 | disableTransfers(bool) | supported | — |
| i6::FCR-PAUSE | transfer_test(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i7 | disableTransfers(bool) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×6、relevant_source_scope_without_resolved_property×1、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×3、open/relevant_source_scope_without_resolved_property×3、excluded/source_positions_and_resolved_properties×1、open/decisive_property_or_source_residual×1。与最终指定类性质标识严格相同的查询结果：sat×4、unsat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_85f09c4a60e545bdb49c | FCR-PAUSE | disableTransfers(bool)@843 | property_bc058721ad3212519078 | E13,E19,E2 |
| finding_b2cdf0409fe34e0c36d8 | FCR-PAUSE | disableTransfers(bool)@843 | property_b38a5240235fd40aa812 | E14,E24,E3 |



该成员共 2 次真实提交；选定报告登记 32 项调查动作、29 条查询记录（sat×15、unsat×14），底层求解 20 次。反馈登记消费 1 行；检查点类别 FCR-PAUSE×2，最终类别 FCR-PAUSE×2。

可核对的检查示例：`probe_1131ff8d031f2aca594a`，control_transition_preservation → unsat，条件摘要 `39656903ecb3f19177f1e9ecde2831a1fcef38e37e5dbeb33a78166df96e2c95`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1888/7487 | 7f7d47201cf9 | f913adfc6e32 |
| main/1 | focused_revision | stop/analysis_received | 2535/2224 | ba5749663ae7 | 6c867910973d |



选定来源：main；报告 SHA-256 `d58cd756168ab9126f53c1d99c028a6141b534aedbdf601e6c52225e8818602e`；报告位于原归档 `run/members/RQ1_4f9f1ce04ed8/attempt_1/analysis/report.json`。

## RQ1_329e0d0d7a11

DESTROY · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_30c29cd44cad](FCR_03.md#rq1_30c29cd44cad)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 7 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i4 | destroy(address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |


前批指定类义务依据：source_effect_and_privilege_relevance×12。本次：excluded/compiler_generated_readonly_getter×4、open/relevant_source_scope_without_resolved_property×4、open/decisive_property_or_source_residual×3、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 22 项调查动作、1 条查询记录（sat×1），底层求解 1 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_3ab39d7264867b9e09c0`，original_path_commit → sat，条件摘要 `2b199b85bad71093562a98cdead426666ce30b00edfa0604226955b881bc487b`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2039/24087 | 86dc7b24454c | c5f9567546ab |
| main/1 | focused_revision | stop/analysis_received | 3090/6635 | f9e1b504666b | da3d63799751 |



选定来源：main；报告 SHA-256 `445bcba0b7a9dde72ddfff3c2c68a8426237916fd826f6c33963ad3704fdd9e5`；报告位于原归档 `run/members/RQ1_329e0d0d7a11/attempt_1/analysis/report.json`。
