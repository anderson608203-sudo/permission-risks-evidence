# FCR 逐例复核 · 第 5 页

[返回成员索引](CaseIndex.md)

## RQ1_81a85f242b60

MINT · 修复端。检测状态：FP。前批 → 本批：有效未检出 → 检出。配对成员 [RQ1_b61f163309a1](FCR_02.md#rq1_b61f163309a1)。

本轮已选输出 检出；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 检出

指定类新 FP 落在 setTokenExchangeRate，匹配到 financial_value 和 financial_value_post_exclusion 的 SAT。旧配对差异表显示该端改行覆盖 fallback；仅比较函数位置不足以证明独立的供应膨胀或否定此报警。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | fallback() | 未确认 | financial_property_conditions_not_established |
| obligation_question_f52f3f49026ceae0::FCR-MINT | setTokenExchangeRate(uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×34。本次：excluded/compiler_generated_readonly_getter×15、open/relevant_source_scope_without_resolved_property×11、excluded/committed_exits_have_no_state_or_external_effect×4、open/decisive_property_or_source_residual×4。与最终指定类性质标识严格相同的查询结果：sat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_791735b8d73c4a612f06 | FCR-MINT | setTokenExchangeRate(uint256)@5099 | property_6fa91020bb6574f0cb79 | E30,E42,E43,E45,E46,E52 |



该成员共 2 次真实提交；选定报告登记 53 项调查动作、20 条查询记录（sat×16、unsat×4），底层求解 18 次。反馈登记消费 0 行；检查点类别 FCR-MINT×1，最终类别 FCR-MINT×1。

可核对的检查示例：`probe_61fcf96e4bcff677b954`，financial_value_post_exclusion → sat，条件摘要 `4d0e2d1665962caae91d37906e10149d7c08116b9f2c44aa11c81b5c5a266adc`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4602/17598 | 843c15aa3c0f | da83ffc643b4 |
| main/1 | focused_revision | stop/analysis_received | 5608/11654 | ab6e3d4de0fe | c3fccfc034aa |



选定来源：main；报告 SHA-256 `f4abbea45f1ea11601ac125340ac2d4fe01ca285da5b0a5d889010b7f25d6b9a`；报告位于原归档 `run/members/RQ1_81a85f242b60/attempt_1/analysis/report.json`。

## RQ1_6c3522e11e92

DESTROY · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_9a61667124cf](FCR_05.md#rq1_9a61667124cf)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 26 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2@8e89afcce351::FCR-DESTROY | batchTransfer(address[],uint256) | 未确认 | financial_property_conditions_not_established |
| i2@935a2911126d::FCR-DESTROY | batchTransfer(address[],uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×53。本次：open/relevant_source_scope_without_resolved_property×21、excluded/compiler_generated_readonly_getter×19、excluded/committed_exits_have_no_state_or_external_effect×7、open/decisive_property_or_source_residual×5、excluded/all_extracted_exits_revert×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 64 项调查动作、21 条查询记录（sat×13、unsat×8），底层求解 16 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_1dd6bfdea674da91f890`，baseline_usable → sat，条件摘要 `43ef76539936a4563404073bbad2bcc9c2426908db49a2501b65d5d5ab601f0e`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4476/13321 | 34502f4fd40c | ee1e68fb3efc |
| main/1 | focused_revision | stop/analysis_received | 4266/12441 | 6d992194ca9f | 4419da6f1bce |



选定来源：main；报告 SHA-256 `d502d698fa16faa745791d3bb65803d9964300814b8a492666a64ac256215e6b`；报告位于原归档 `run/members/RQ1_6c3522e11e92/attempt_1/analysis/report.json`。

## RQ1_5b3c7cbe3d9d

FREEZE · 风险端。检测状态：U+。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_0f3c3f400f6f](FCR_10.md#rq1_0f3c3f400f6f)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 30 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i5 | addSaleOwner(address) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×63。本次：open/relevant_source_scope_without_resolved_property×29、excluded/compiler_generated_readonly_getter×25、excluded/committed_exits_have_no_state_or_external_effect×8、open/decisive_property_or_source_residual×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_e2d3ef8aa2355931545b | FCR-MINT | mintToken(uint256)@11956 | property_536e90912ea60996799d | E19,E40,E71,E73,E75,E77 |
| finding_1ed9a36599413b244ce3 | FCR-DESTROY | mintToken(uint256)@11956 | property_e7962d0403a493e6fff1 | E21,E34,E45,E49,E54,E57,E80 |
| finding_1fb3c7e9049daa8491a7 | FCR-MINT | burnFrom(address,uint256)@14128 | property_35a2dc40c35d1dc3c940 | E27,E38,E43,E51,E53,E55,E68 |
| finding_b9c833d188a81f0c5af6 | FCR-PAUSE | pause()@2642 | property_24610c3d2881a6994d74 | E24,E3,E35,E9 |



该成员共 2 次真实提交；选定报告登记 80 项调查动作、63 条查询记录（unsat×34、sat×29），底层求解 56 次。反馈登记消费 1 行；检查点类别 FCR-MINT×2、FCR-PAUSE×2、FCR-DESTROY×1，最终类别 FCR-MINT×2、FCR-DESTROY×1、FCR-PAUSE×1。

可核对的检查示例：`probe_c71e02e122c96b6e0469`，control_transition_preservation → sat，条件摘要 `643d31bacf533486c6a6eaa8373bad726ef5c1f0789f7c466d2e8ae3e7409dfa`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 6032/10198 | 97c95d15b73e | 167409b76129 |
| main/1 | focused_revision | stop/analysis_received | 7713/3616 | c8e60d8835b8 | 5832a35b3251 |



选定来源：main；报告 SHA-256 `d8d1a8c3788abe0c70a37a93ca1a8a686db203600ab417462c7a4f767f3219a9`；报告位于原归档 `run/members/RQ1_5b3c7cbe3d9d/attempt_1/analysis/report.json`。

## RQ1_8456d2957fff

DESTROY · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_776a6b98d18f](FCR_02.md#rq1_776a6b98d18f)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | destroy(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i2::FCR-DESTROY | destroy(address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×3、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×2、open/decisive_property_or_source_residual×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：sat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_cc6fe5419446ac9036f9 | FCR-DESTROY | destroy(address,uint256)@493 | property_5bd35c7cb3a49be69a48 | E5,E7 |



该成员共 2 次真实提交；选定报告登记 9 项调查动作、4 条查询记录（sat×4），底层求解 2 次。反馈登记消费 1 行；检查点类别 FCR-DESTROY×2，最终类别 FCR-DESTROY×1。

可核对的检查示例：`probe_88317bbff1ef845c533c`，local_premises_feasible → sat，条件摘要 `eeb98282dca8f3cc5caf37fe001299544fc561b43f99fc53c3b90d04dfda3bfb`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1484/7374 | 8bce3d026eb8 | a541e784ff34 |
| main/1 | focused_revision | stop/analysis_received | 3611/4026 | 86e353ed0360 | a94a1af1aa1c |



选定来源：main；报告 SHA-256 `b34f9673bf52f5049f8aff37249a572808c6fb0537a4ffec6e5c1c21c79384a0`；报告位于原归档 `run/members/RQ1_8456d2957fff/attempt_1/analysis/report.json`。

## RQ1_cd39ae0d15a5

PAUSE · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_b649070a92c3](FCR_01.md#rq1_b649070a92c3)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | stop() | supported | — |
| i6::FCR-PAUSE | stop() | supported | — |
| obligation_question_b687c5811d9b567c | start() | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×21、relevant_source_scope_without_resolved_property×2、source_positions_and_resolved_properties×2。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×6、open/decisive_property_or_source_residual×1、open/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：sat×6、unsat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_61a198646d7f3aa08c2b | FCR-PAUSE | stop()@3473 | property_d9ddb66ff840e292eee8 | E1,E12,E20,E5 |
| finding_a212c0336013b9b898e7 | FCR-PAUSE | stop()@3473 | property_7910ef72fece723f7385 | E17,E2,E23,E6 |



该成员共 2 次真实提交；选定报告登记 57 项调查动作、68 条查询记录（sat×52、unsat×16），底层求解 52 次。反馈登记消费 1 行；检查点类别 FCR-PAUSE×2，最终类别 FCR-PAUSE×2。

可核对的检查示例：`probe_e7721184bd2fe2fc41a6`，control_transition_preservation → sat，条件摘要 `77506125b4fb9f7d2da41edc5dc21528ef82e4b1b78cec6cafcd8c35a9acb60d`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2822/9015 | ba399f1db738 | 823fa6a2b829 |
| main/1 | focused_revision | stop/analysis_received | 3849/4742 | 481ba0faf94d | 5127b747ee88 |



选定来源：main；报告 SHA-256 `85ae378f8e1c5f873a0b56062d7aba054a4bcda7a5393a9b6a19a906e4a08c16`；报告位于原归档 `run/members/RQ1_cd39ae0d15a5/attempt_1/analysis/report.json`。

## RQ1_1f06ce07140f

TRANSFER · 修复端。检测状态：U-。前批 → 本批：未知 → 未知。配对成员 [RQ1_e73c99ca23e5](FCR_03.md#rq1_e73c99ca23e5)。

本轮已选输出 未知；前次同 200 份 未知；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 26 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1@25c714cf1b4a | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| i1@8e89afcce351 | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| i1@935a2911126d | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| i2@25c714cf1b4a::FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| i2@8e89afcce351::FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| i2@935a2911126d::FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| i4@8e89afcce351 | transfer(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i4@935a2911126d | transfer(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i5@8e89afcce351::FCR-TRANSFER | transfer(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i5@935a2911126d::FCR-TRANSFER | transfer(address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_4100c968f71423e3 | transferFrom(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_6081f6f3f02ddf9e | transferFrom(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_812805187d98518b | transfer(address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_c0318c70216d909f | transferFrom(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_cf8dd3ebb518fecd | transfer(address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×46、decisive_property_or_source_residual×2、source_positions_and_resolved_properties×2。本次：excluded/compiler_generated_readonly_getter×16、open/decisive_property_or_source_residual×15、open/relevant_source_scope_without_resolved_property×11、excluded/committed_exits_have_no_state_or_external_effect×7、excluded/all_extracted_exits_revert×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 1 次真实提交；选定报告登记 76 项调查动作、3 条查询记录（unsat×3），底层求解 1 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_7d37a2591f2403feb67a`，baseline_usable → unsat，条件摘要 `b808388584564c3b5cf6ef1637b7774dfa6c5741e314eb6dc94947ff41522dae`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4506/12929 | cc63c8a73958 | ed9ad7f409c4 |



选定来源：main；报告 SHA-256 `5d53251981b527a217275f0bf785dd12fd34d45ac69e1b18ef469cf5dff836ab`；报告位于原归档 `run/members/RQ1_1f06ce07140f/attempt_1/analysis/report.json`。

## RQ1_cf32aac41cf2

TRANSFER · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_a4c5ecc3c29e](FCR_12.md#rq1_a4c5ecc3c29e)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类初始未出现，最终已形成发现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×5、source_positions_and_resolved_properties×1。本次：open/relevant_source_scope_without_resolved_property×2、excluded/all_extracted_exits_revert×1、excluded/compiler_generated_readonly_getter×1、excluded/source_positions_and_resolved_properties×1、open/decisive_property_or_source_residual×1。与最终指定类性质标识严格相同的查询结果：sat×3、unsat×1。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_e048d2de8b1048a8da38 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256)@612 | property_0ad7c7925c0eb58281d7 | E1,E4,E8,E9 |



该成员共 2 次真实提交；选定报告登记 9 项调查动作、4 条查询记录（sat×3、unsat×1），底层求解 3 次。反馈登记消费 1 行；检查点类别 无，最终类别 FCR-TRANSFER×1。

可核对的检查示例：`probe_411ee7d37c769e4798e7`，local_premises_feasible → sat，条件摘要 `2b294adea7d0bdf0b82186b908c9af674049a88dab89498f2f3423a227e0f157`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1822/11685 | a01724964806 | 0d675b132862 |
| main/1 | focused_revision | stop/analysis_received | 2305/1443 | 3ad703102ba0 | 5863e194f6b6 |



选定来源：main；报告 SHA-256 `49a4bba955d318ac8c68608767e304db0911c8a482bad7e721b5a11b834d2099`；报告位于原归档 `run/members/RQ1_cf32aac41cf2/attempt_1/analysis/report.json`。

## RQ1_fe7add810da5

DESTROY · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_15346457ba72](FCR_08.md#rq1_15346457ba72)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 2 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | destroy(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i2::FCR-DESTROY | destroy(address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |


前批指定类义务依据：source_effect_and_privilege_relevance×4。本次：excluded/committed_exits_have_no_state_or_external_effect×1、excluded/compiler_generated_readonly_getter×1、open/decisive_property_or_source_residual×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 8 项调查动作、0 条查询记录（无），底层求解 0 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：无已保存的程序查询。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1596/6256 | 01dafd557e1c | 0add59e632bc |
| main/1 | focused_revision | stop/analysis_received | 2779/2859 | 27417d626668 | 63537754cf52 |



选定来源：main；报告 SHA-256 `6114d77b97d2b8d656fc5e30080abb55f1212b3dd9774b99a45ff484b3581ed6`；报告位于原归档 `run/members/RQ1_fe7add810da5/attempt_1/analysis/report.json`。

## RQ1_9a61667124cf

DESTROY · 风险端。检测状态：U+。前批 → 本批：检出 → 未知。配对成员 [RQ1_6c3522e11e92](FCR_05.md#rq1_6c3522e11e92)。

本轮已选输出 未知；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 30 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i3@8e89afcce351::FCR-DESTROY | batchTransfer(address[],uint256) | 未确认 | financial_property_conditions_not_established |
| i3@935a2911126d::FCR-DESTROY | batchTransfer(address[],uint256) | 未确认 | financial_property_conditions_not_established |
| i4@25c714cf1b4a | destroy(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i4@8e89afcce351 | destroy(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i4@935a2911126d | destroy(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i4@977b12483c58 | destroy(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i5@25c714cf1b4a::FCR-DESTROY | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×53、source_positions_and_resolved_properties×4。本次：open/relevant_source_scope_without_resolved_property×20、excluded/compiler_generated_readonly_getter×19、open/decisive_property_or_source_residual×10、excluded/committed_exits_have_no_state_or_external_effect×7、excluded/all_extracted_exits_revert×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_2ee3cbb0ec4c947cba97 | FCR-PAUSE | pause()@5690 | property_0ed2f58bc03abadc5d1a | E1,E19,E3,E37,E6 |
| finding_0da4ee86d02dbce17a5e | FCR-PAUSE | pause()@5690 | property_317eea0c4306bcd83615 | E2,E21,E39,E5,E7 |



该成员共 2 次真实提交；选定报告登记 64 项调查动作、29 条查询记录（sat×20、unsat×9），底层求解 24 次。反馈登记消费 1 行；检查点类别 FCR-PAUSE×2，最终类别 FCR-PAUSE×2。

可核对的检查示例：`probe_6bbc6a2784b73fabb1b2`，control_transition_preservation → sat，条件摘要 `6aa592b682fdf87964bcb92db893597db65983fdda1ad2b33792906a528fb935`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4777/17732 | 0834a4a7809c | ec4cb975769e |
| main/1 | focused_revision | stop/analysis_received | 4444/3590 | 71fc622c2aa7 | d877b6ff1245 |



选定来源：main；报告 SHA-256 `df48d3a313c57afbc9ffb3adae3ce03d0dc78f5850036ccd68c0848c3e30be04`；报告位于原归档 `run/members/RQ1_9a61667124cf/attempt_1/analysis/report.json`。

## RQ1_f322b5b8495d

DESTROY · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_5eee31e70615](FCR_12.md#rq1_5eee31e70615)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 2 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | destroy(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i2::FCR-DESTROY | destroy(address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×4。本次：excluded/compiler_generated_readonly_getter×2、open/decisive_property_or_source_residual×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 8 项调查动作、0 条查询记录（无），底层求解 0 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：无已保存的程序查询。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1461/6959 | 343dfb5d22bd | 79361c215cf1 |
| main/1 | focused_revision | stop/analysis_received | 2407/1552 | e9179ddd3d23 | b20b0c957f29 |



选定来源：main；报告 SHA-256 `e949172433b7e69859f722cc0d6167f30e94791d5f7761c3f14a3a41ed6d9b89`；报告位于原归档 `run/members/RQ1_f322b5b8495d/attempt_1/analysis/report.json`。
