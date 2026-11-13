# FCR 逐例复核 · 第 8 页

[返回成员索引](CaseIndex.md)

## RQ1_c29df435681e

PAUSE · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_ffcaa562a72d](FCR_02.md#rq1_ffcaa562a72d)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 未知

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | disableTransfers(bool) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×8、relevant_source_scope_without_resolved_property×1、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×3、open/relevant_source_scope_without_resolved_property×2、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：sat×2、unsat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_b0ef7430d98835717a7d | FCR-PAUSE | disableTransfers(bool)@909 | property_a97f7ff685570dbdbe5c | E1,E5,E7 |



该成员共 2 次真实提交；选定报告登记 14 项调查动作、10 条查询记录（sat×5、unsat×5），底层求解 7 次。反馈登记消费 1 行；检查点类别 FCR-PAUSE×1，最终类别 FCR-PAUSE×1。

可核对的检查示例：`probe_cb4a7aa9fff82c64004b`，control_transition_preservation → unsat，条件摘要 `6b084634199d90be1481ae26a9ff9992e73936be1d23cd86744e9b6f5900e207`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2373/9344 | 21f2b935a6e9 | d6c47ecb42c2 |
| main/1 | focused_revision | stop/analysis_received | 3022/1892 | 94499cbba9bb | b855e4f2a1ca |



选定来源：main；报告 SHA-256 `d83909aecd7c2d05d0151853ca0aa71d832a2ad5c19e060c1e8c14ab966c8bc7`；报告位于原归档 `run/members/RQ1_c29df435681e/attempt_1/analysis/report.json`。

## RQ1_bc5855a83e2d

MINT · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_770ae395781c](FCR_01.md#rq1_770ae395781c)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | mint(address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×25、source_positions_and_resolved_properties×1。本次：excluded/committed_exits_have_no_state_or_external_effect×13、open/decisive_property_or_source_residual×6、open/relevant_source_scope_without_resolved_property×6、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：unsat×4、sat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_d36272eb56947bc6f0c4 | FCR-MINT | mint(address,uint256)@13539 | property_7e4c02b9ab8978961434 | E15,E17,E18,E2,E41,E42,E43 |



该成员共 2 次真实提交；选定报告登记 43 项调查动作、32 条查询记录（unsat×18、sat×14），底层求解 27 次。反馈登记消费 1 行；检查点类别 FCR-MINT×1，最终类别 FCR-MINT×1。

可核对的检查示例：`probe_e60bc404565decb43e2d`，financial_value_post_exclusion → unsat，条件摘要 `9c5aa77cc533bf730745185c1e2671f9ef95295cbd2814fe9e91e9fd9214b26d`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 5954/4320 | 769196c9534b | 7385e77779e0 |
| main/1 | focused_revision | stop/analysis_received | 8231/969 | 18150dd45584 | 1d41e46a6de8 |



选定来源：main；报告 SHA-256 `1c1e4a2fa464dda23ad29b64b01ae171589aae0ec43c401f5076276fdaf68e55`；报告位于原归档 `run/members/RQ1_bc5855a83e2d/attempt_1/analysis/report.json`。

## RQ1_c80f7a639e42

FREEZE · 风险端。检测状态：U+。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_30177d564271](FCR_11.md#rq1_30177d564271)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 17 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i3 | freezeAccount(address,bool) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×34。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×14、open/decisive_property_or_source_residual×3。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_f4b0f2067c1dfb68141e | FCR-MINT | mintToken(address,uint256)@8240 | property_252e7b201662472f4d63 | E13,E63,E65,E66,E67,E69 |



该成员共 2 次真实提交；选定报告登记 70 项调查动作、53 条查询记录（unsat×30、sat×23），底层求解 39 次。反馈登记消费 1 行；检查点类别 FCR-MINT×1，最终类别 FCR-MINT×1。

可核对的检查示例：`probe_9975b5c09739544308a2`，financial_value_post_exclusion → unsat，条件摘要 `0f17d7ebaf359f9188ee49e7bf5b8091d3308f55c243fe5ea930e67455706389`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4276/13147 | cca51a8fec44 | 7acf51404b23 |
| main/1 | focused_revision | stop/analysis_received | 5692/4348 | 74b4b72434ad | 9c924817650a |



选定来源：main；报告 SHA-256 `bf7e6f4daa6e922404e36350a3c723a05490648b193a0fd48a4115e6c2f111c2`；报告位于原归档 `run/members/RQ1_c80f7a639e42/attempt_1/analysis/report.json`。

## RQ1_a7d72c1e4129

TRANSFER · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_53f9777ccdf6](FCR_07.md#rq1_53f9777ccdf6)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 7 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i4 | zero_fee_transaction(address,address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |


前批指定类义务依据：source_effect_and_privilege_relevance×12。本次：excluded/compiler_generated_readonly_getter×4、open/relevant_source_scope_without_resolved_property×4、open/decisive_property_or_source_residual×3、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 17 项调查动作、1 条查询记录（sat×1），底层求解 1 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_7af7f1db6f8f9c1b3d94`，original_path_commit → sat，条件摘要 `be1d81a4484cd0c7bd686fc4511f742837b3fd628e1eb5dcab7c462fd0c87060`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2143/13041 | dfd6df3c0d36 | cd7652cddf19 |
| main/1 | focused_revision | stop/analysis_received | 2865/3398 | 25794568cdc5 | fbe3afa3a60c |



选定来源：main；报告 SHA-256 `4f9588f67e0cc2f65095949d68c4b2e0c828b486d478d9cf558f79baef646e25`；报告位于原归档 `run/members/RQ1_a7d72c1e4129/attempt_1/analysis/report.json`。

## RQ1_15346457ba72

DESTROY · 风险端。检测状态：U+。前批 → 本批：未知 → 未知。配对成员 [RQ1_fe7add810da5](FCR_05.md#rq1_fe7add810da5)。

本轮已选输出 未知；前次同 200 份 未知；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 2 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | destroy(address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×3、decisive_property_or_source_residual×1。本次：excluded/committed_exits_have_no_state_or_external_effect×1、excluded/compiler_generated_readonly_getter×1、open/decisive_property_or_source_residual×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：sat×1。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 5 项调查动作、1 条查询记录（sat×1），底层求解 1 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_3a97b9400a252021c7a7`，local_premises_feasible → sat，条件摘要 `a8ac20e495d408b9f44c1db02f989fb9638d7ea7465f71e221b1c9da4b03a4c0`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1620/8693 | a7bc7afe22c1 | 9c8db6f30f7d |
| main/1 | focused_revision | stop/analysis_received | 2170/7276 | a03c2d313365 | 2f5d9cabc86c |



选定来源：main；报告 SHA-256 `1df4765ef8c15fc1bb85baa8de8b806415cfeaa28bef8f1f5a3469bb93707ce8`；报告位于原归档 `run/members/RQ1_15346457ba72/attempt_1/analysis/report.json`。

## RQ1_6476444da7e8

TRANSFER · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_fe11616caf66](FCR_10.md#rq1_fe11616caf66)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 1 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |


前批指定类义务依据：source_effect_and_privilege_relevance×3。本次：excluded/compiler_generated_readonly_getter×1、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 5 项调查动作、0 条查询记录（无），底层求解 0 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：无已保存的程序查询。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1513/5209 | 10262581eb16 | 3a4c9fa3daae |
| main/1 | focused_revision | stop/analysis_received | 2716/2167 | b44e186b3fef | c20bf6908943 |



选定来源：main；报告 SHA-256 `502e4ab078b909c56fe3f6101bb2e2388758614c20964b9b858228e4dd81293e`；报告位于原归档 `run/members/RQ1_6476444da7e8/attempt_1/analysis/report.json`。

## RQ1_dc06d7bad0d8

FREEZE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_9c365cb18f95](FCR_08.md#rq1_9c365cb18f95)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 13 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i5 | frozenAccount(address) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×33。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×9、open/decisive_property_or_source_residual×4、excluded/committed_exits_have_no_state_or_external_effect×2、excluded/all_extracted_exits_revert×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 41 项调查动作、87 条查询记录（unsat×84、sat×3），底层求解 6 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_397ed76a9fc7844f1d78`，baseline_usable → sat，条件摘要 `b2997f0f1864227d7287d1b0834d8a75026c87230fb8682a4141f521ad044540`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4507/12192 | 0cbe9557d682 | 8dd0ecd1c76e |
| main/1 | focused_revision | stop/analysis_received | 5097/13487 | b43943b9d1e1 | 643338900218 |



选定来源：main；报告 SHA-256 `34d49281fab05fb8b0966aa8a7d48c5a199e6dbd2d85f455834c096ea1f82cfd`；报告位于原归档 `run/members/RQ1_dc06d7bad0d8/attempt_1/analysis/report.json`。

## RQ1_9c365cb18f95

FREEZE · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_dc06d7bad0d8](FCR_08.md#rq1_dc06d7bad0d8)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i3 | freeze(address,bool) | supported | — |
| obligation_question_a63b01ec332bff28 | validatePublisher(address,bool,string) | 未确认 | financial_property_conditions_not_established |
| obligation_question_ad0497f3d27ce841::FCR-FREEZE | validateWallet(address,bool,string) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×37、relevant_source_scope_without_resolved_property×3、decisive_property_or_source_residual×2、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×16、open/decisive_property_or_source_residual×6、excluded/committed_exits_have_no_state_or_external_effect×2、excluded/all_extracted_exits_revert×1、open/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_ca9365e6c62dcbc79211 | FCR-PAUSE | pause()@2407 | property_61bc418570be28186ddd | E1,E17,E28,E5,E9 |
| finding_70e4d239fd414578f532 | FCR-FREEZE | freeze(address,bool)@8244 | property_616b2fe3c87fcc1ba808 | E11,E18,E3,E34,E7 |



该成员共 2 次真实提交；选定报告登记 73 项调查动作、103 条查询记录（unsat×84、sat×19），底层求解 27 次。反馈登记消费 1 行；检查点类别 FCR-FREEZE×1、FCR-PAUSE×1，最终类别 FCR-FREEZE×1、FCR-PAUSE×1。

可核对的检查示例：`probe_c8b3d1cc9e7b2c97ee90`，financial_value_post_exclusion → unsat，条件摘要 `5b919d652f2cb7b2741dd509b90338e7a9fee82ba2108d3bd2af041b2efcb0a5`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 5222/15784 | 5c65d67bd3d8 | d0ae3cbfc67b |
| main/1 | focused_revision | stop/analysis_received | 7206/4829 | 7b68c26b0c20 | 1207c6d596d3 |



选定来源：main；报告 SHA-256 `9f6ec348f689c65789717aad0a07db58e498f44181eadc4695fb1c3405625f24`；报告位于原归档 `run/members/RQ1_9c365cb18f95/attempt_1/analysis/report.json`。

## RQ1_1f932eab663d

FREEZE · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_43103f5773b9](FCR_11.md#rq1_43103f5773b9)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | freezeAccount(address,bool) | supported | — |
| i2@ede9e899e099::FCR-FREEZE | transferFrom(address,address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×29、relevant_source_scope_without_resolved_property×1、source_positions_and_resolved_properties×1。本次：open/relevant_source_scope_without_resolved_property×14、excluded/committed_exits_have_no_state_or_external_effect×8、excluded/compiler_generated_readonly_getter×7、excluded/source_positions_and_resolved_properties×1、open/decisive_property_or_source_residual×1。与最终指定类性质标识严格相同的查询结果：sat×3。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_575c7f944b78829d4998 | FCR-FREEZE | freezeAccount(address,bool)@8128 | property_9272950abd8954220412 | E15,E2,E39,E6 |



该成员共 2 次真实提交；选定报告登记 39 项调查动作、16 条查询记录（sat×15、unsat×1），底层求解 15 次。反馈登记消费 1 行；检查点类别 FCR-FREEZE×1，最终类别 FCR-FREEZE×1。

可核对的检查示例：`probe_2dabc53255b75453c7e6`，control_transition_preservation → sat，条件摘要 `ee12866ab7ed55b193d97c4d633771f62a166cb31eda7535570b82ec2009d06d`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4066/10523 | 135f031760ba | 7f81f4b9ba53 |
| main/1 | focused_revision | stop/analysis_received | 4908/5929 | d0f80273be26 | baac6a2c01f3 |



选定来源：main；报告 SHA-256 `b2cdd4d81cc8856fe214e2b24497e90ca4396ad7e11c765288be856e10f6e947`；报告位于原归档 `run/members/RQ1_1f932eab663d/attempt_1/analysis/report.json`。

## RQ1_4968e56244c9

MINT · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_b731957fa974](FCR_10.md#rq1_b731957fa974)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 检出

指定类性质已进入检查，指定类仍有 22 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1@8e89afcce351 | batchTransfer(address[],uint256) | 未确认 | financial_property_conditions_not_established |
| i1@935a2911126d | batchTransfer(address[],uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×49。本次：excluded/compiler_generated_readonly_getter×19、open/relevant_source_scope_without_resolved_property×17、excluded/committed_exits_have_no_state_or_external_effect×7、open/decisive_property_or_source_residual×5、excluded/all_extracted_exits_revert×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 66 项调查动作、24 条查询记录（sat×16、unsat×8），底层求解 19 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_70989d85e7053f15f265`，baseline_usable → sat，条件摘要 `d213ce5872b7f2a1c7074500b72fad1a449fb54e9cf9fe3b0fceb5f842b252be`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4383/16872 | 238b7faa4c35 | 2ff4ae87398d |
| main/1 | focused_revision | stop/analysis_received | 4861/6050 | 0917b1ed1a5e | bf36592197db |



选定来源：main；报告 SHA-256 `88e9eb5ffbc6a2b03d7d89dc0bac20d6627540d60b55269c522905d5f9a417d0`；报告位于原归档 `run/members/RQ1_4968e56244c9/attempt_1/analysis/report.json`。
