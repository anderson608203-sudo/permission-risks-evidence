# FCR 逐例复核 · 第 12 页

[返回成员索引](CaseIndex.md)

## RQ1_db73c28a69c2

TRANSFER · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_1844e5d3d18e](FCR_09.md#rq1_1844e5d3d18e)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 未知；b5 冻结 Full 未知

指定类性质已进入检查，指定类仍有 16 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2@051252cf9fe3 | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| i2@c9e1e9c2647a | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |
| i2@fc757553236a | zero_fee_transaction(address,address,uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×21。本次：open/relevant_source_scope_without_resolved_property×9、open/decisive_property_or_source_residual×7、excluded/compiler_generated_readonly_getter×5。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_96da78c0813cd75f341e | FCR-DESTROY | WitdrawTokenToHolder(address,address,uint256)@2162 | property_7ec4853360dd92a7594d | E12,E43,E45,E47,E49 |
| finding_3f9d127bd77f0204bf76 | FCR-MINT | WitdrawTokenToHolder(address,address,uint256)@2162 | property_ad1dd09a600b02263dff | E15,E27,E35,E38,E41,E51 |



该成员共 2 次真实提交；选定报告登记 65 项调查动作、74 条查询记录（sat×50、unsat×24），底层求解 71 次。反馈登记消费 1 行；检查点类别 FCR-DESTROY×1、FCR-MINT×1，最终类别 FCR-DESTROY×1、FCR-MINT×1。

可核对的检查示例：`probe_c27a4224be2785d5adca`，financial_value_post_exclusion → sat，条件摘要 `561a43b2da2164685c0c1ceea74e5f5d4765efa6051c1b2f96c0ab249ca28de6`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2364/20630 | ee32f91c2443 | ba0405b20ec4 |
| main/1 | focused_revision | stop/analysis_received | 3366/1452 | 42c45804b96f | d35faf3ce26d |



选定来源：main；报告 SHA-256 `aadccb102456bd81bfc71288a6823dbc05ab945c31be846fc444d1c2425288f5`；报告位于原归档 `run/members/RQ1_db73c28a69c2/attempt_1/analysis/report.json`。

## RQ1_5eee31e70615

DESTROY · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_f322b5b8495d](FCR_05.md#rq1_f322b5b8495d)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i2 | destroy(address,uint256) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×3、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×2、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：sat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_181b109d4fed529598b9 | FCR-DESTROY | destroy(address,uint256)@489 | property_c665d3760e9f01e0d0dd | E3,E4,E5 |



该成员共 2 次真实提交；选定报告登记 5 项调查动作、4 条查询记录（sat×4），底层求解 2 次。反馈登记消费 1 行；检查点类别 FCR-DESTROY×1，最终类别 FCR-DESTROY×1。

可核对的检查示例：`probe_c4c5e5734e77282a537d`，local_premises_feasible → sat，条件摘要 `04f08b91de5fdaaee1cbde48b551bd1c1b148bddc9d294c2cefc05576177a5be`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1485/9676 | e22a31f629b8 | c7ff834ff2bd |
| main/1 | focused_revision | stop/analysis_received | 3918/6308 | a109b6c2bd7d | 541640539b94 |



选定来源：main；报告 SHA-256 `a94c32d23a2f257d3708c41fc88a651024a2dd0af12c0a3f0aabbd3184379c57`；报告位于原归档 `run/members/RQ1_5eee31e70615/attempt_1/analysis/report.json`。

## RQ1_6a278772c4f3

FREEZE · 风险端。检测状态：U+。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_980e04c92f4d](FCR_06.md#rq1_980e04c92f4d)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 23 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | addSaleOwner(address) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×56。本次：excluded/compiler_generated_readonly_getter×24、open/relevant_source_scope_without_resolved_property×22、excluded/isolated_flag_no_nongenerated_reader_in_resolved_public_bodies×6、excluded/committed_exits_have_no_state_or_external_effect×3、open/decisive_property_or_source_residual×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_8752e7352f6a6f051f3e | FCR-MINT | burnFrom(address,uint256)@10567 | property_2d2796ee1887eec5b5ec | E29,E38,E43,E55,E59,E63 |



该成员共 2 次真实提交；选定报告登记 81 项调查动作、51 条查询记录（unsat×27、sat×24），底层求解 43 次。反馈登记消费 1 行；检查点类别 FCR-PAUSE×2、FCR-DESTROY×1、FCR-MINT×1，最终类别 FCR-MINT×1。

可核对的检查示例：`probe_21e0c88aec30db538299`，control_transition_preservation → sat，条件摘要 `2589df731b9a8cb67caa99bea35ffd588ccade02968433b7994cd87f26b453e7`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 4998/10878 | a551ce401279 | 00dbe0a18534 |
| main/1 | focused_revision | stop/analysis_received | 5373/3924 | 8dff4410b337 | 03ff0a8ba4ae |



选定来源：main；报告 SHA-256 `311f10d0274bfdefed58a269518a46cc886df3f6177479af34c6fedbe1a4802f`；报告位于原归档 `run/members/RQ1_6a278772c4f3/attempt_1/analysis/report.json`。

## RQ1_7450d39da940

FREEZE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_39fb6e7197c4](FCR_04.md#rq1_39fb6e7197c4)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 15 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i5 | transferOwnership(address) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×30。本次：excluded/compiler_generated_readonly_getter×15、open/decisive_property_or_source_residual×13、open/relevant_source_scope_without_resolved_property×2。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 80 项调查动作、0 条查询记录（无），底层求解 0 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：无已保存的程序查询。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3944/9145 | 0c044d7a9171 | d5a93687fa6c |
| main/1 | focused_revision | stop/analysis_received | 8937/11338 | 0200504232fb | 74a8f09d92ff |



选定来源：main；报告 SHA-256 `7cea6601ca3eb838c67d0cfd77c26415a53b7177ccbdaaad576bf0ad493ca785`；报告位于原归档 `run/members/RQ1_7450d39da940/attempt_1/analysis/report.json`。

## RQ1_a0facbcc1e38

MINT · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_86a0269d7608](FCR_04.md#rq1_86a0269d7608)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | mintToken(address,uint256) | 未确认 | financial_property_conditions_not_established |
| i2 | terminateMinting() | 未确认 | financial_property_conditions_not_established |
| i3::FCR-DESTROY::FCR-MINT | withdrawLOOiX() | 未确认 | financial_property_conditions_not_established |
| i3::FCR-MINT | withdrawLOOiX() | supported | — |
| obligation_question_1164916ef1727698::FCR-MINT | transferOwnership(address) | 未确认 | financial_property_conditions_not_established |
| obligation_question_11ddf4180e769374::FCR-MINT | mintTokenBulk(address[],uint256[]) | 未确认 | financial_property_conditions_not_established |
| obligation_question_3d390db97d1a1918::FCR-MINT | acceptOwnership() | 未确认 | financial_property_conditions_not_established |
| obligation_question_7b564b4b19a628a7 | unlock() | 未确认 | financial_property_conditions_not_established |
| obligation_question_fb2c14f3f720a1f8 | redeem() | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×44、decisive_property_or_source_residual×2、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×23、open/decisive_property_or_source_residual×13、open/relevant_source_scope_without_resolved_property×7、excluded/committed_exits_have_no_state_or_external_effect×4。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_925a1289a9879daddad3 | FCR-DESTROY | mintToken(address,uint256)@13941 | property_93701ebfb1779851a574 | E21,E26,E31,E41,E46,E51,E55,E6,E68 |
| finding_8f2c53ce9c6dcd5a9a66 | FCR-DESTROY | terminateMinting()@14448 | property_b3c221241ee91e1c96f8 | E10,E17,E22,E27,E37,E42,E47,E57,E61 |
| finding_dfafe4e467814b4d45fe | FCR-MINT | withdrawLOOiX()@12359 | property_633b09f92fe969aa2349 | E40,E59,E63,E67,E7,E71 |



该成员共 2 次真实提交；选定报告登记 71 项调查动作、39 条查询记录（unsat×28、sat×11），底层求解 54 次。反馈登记消费 1 行；检查点类别 FCR-DESTROY×3、FCR-MINT×1，最终类别 FCR-DESTROY×2、FCR-MINT×1。

可核对的检查示例：`probe_21e2c5cbefd44a888482`，financial_value_post_exclusion → unsat，条件摘要 `98df2da7acee763cc6344ed2947877243f637a1d57673c7561644342242f2754`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 9068/25274 | b18c356c73b8 | 3368705229ca |
| main/1 | focused_revision | stop/analysis_received | 11597/13429 | 4394c921aa53 | ce02338ae3d2 |



选定来源：main；报告 SHA-256 `9a289ea2afe9629b8f3e39c61e9141ea971f4daf066896b43338c50d67b1dfd3`；报告位于原归档 `run/members/RQ1_a0facbcc1e38/attempt_1/analysis/report.json`。

## RQ1_58de46f081ec

FREEZE · 风险端。检测状态：U+。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_2046acc1c802](FCR_12.md#rq1_2046acc1c802)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 16 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×31。本次：excluded/compiler_generated_readonly_getter×15、open/relevant_source_scope_without_resolved_property×14、open/decisive_property_or_source_residual×2。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_d6ff7e4c32dd057f2bb6 | FCR-MINT | mintToken(address,uint256)@6416 | property_d64de912759314a20825 | E14,E28,E65,E66,E67,E69 |



该成员共 2 次真实提交；选定报告登记 78 项调查动作、37 条查询记录（unsat×22、sat×15），底层求解 37 次。反馈登记消费 1 行；检查点类别 FCR-MINT×1，最终类别 FCR-MINT×1。

可核对的检查示例：`probe_7914591ce3e4495d34c4`，financial_value_post_exclusion → unsat，条件摘要 `58a091b74715212d9dce24ad2c1f49b2eb3953e0c47b5a160ec2449bc5a8c5df`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3600/10492 | 19a25a61b4a0 | 98c8de6b32a0 |
| main/1 | focused_revision | stop/analysis_received | 4749/2117 | c2e5ae4d1677 | 86fa7f0ecbbb |



选定来源：main；报告 SHA-256 `fde131d696647b463654be2d3d2fcd8b98229f3dc1ccaeede54018a4d4c3845c`；报告位于原归档 `run/members/RQ1_58de46f081ec/attempt_1/analysis/report.json`。

## RQ1_a4c5ecc3c29e

TRANSFER · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_cf32aac41cf2](FCR_05.md#rq1_cf32aac41cf2)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 2 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | zero_fee_transaction(address,address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |


前批指定类义务依据：source_effect_and_privilege_relevance×5。本次：excluded/all_extracted_exits_revert×1、excluded/compiler_generated_readonly_getter×1、excluded/source_positions_and_resolved_properties×1、open/decisive_property_or_source_residual×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 1 次真实提交；选定报告登记 5 项调查动作、3 条查询记录（unsat×2、sat×1），底层求解 5 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_1db72dd26e861cf93b47`，baseline_usable → sat，条件摘要 `d56317ae0dd700f44c2dfcd5f3b3a24af4229443940f961c0bd16a6437f839f8`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1724/4506 | 24c44ed56a2a | 9248b162a7ec |



选定来源：main；报告 SHA-256 `534f2fe8cf927c32cb3f23c0f63c7243099814b0dc8bed1ae245036f0831f6db`；报告位于原归档 `run/members/RQ1_a4c5ecc3c29e/attempt_1/analysis/report.json`。

## RQ1_fa2207747d01

FREEZE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_cd47d22b26a9](FCR_01.md#rq1_cd47d22b26a9)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 14 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×31。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×12、open/decisive_property_or_source_residual×2。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 71 项调查动作、21 条查询记录（sat×21），底层求解 21 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_fe7eb137bf587a9958dc`，baseline_usable → sat，条件摘要 `056cf09d860fd1f54cc045db76994cb73ef3f27dd9723b0fff92e3f2609e7eea`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3663/20995 | 33e2a3a3ec9c | 76af48e26974 |
| main/1 | focused_revision | stop/analysis_received | 4302/3231 | 71e51d4ebafe | 6b7bcc2ad72e |



选定来源：main；报告 SHA-256 `7fea78ec4ca6844650bb8976a22723fa8525ba03521d5cd57efe17fd85222a9f`；报告位于原归档 `run/members/RQ1_fa2207747d01/attempt_1/analysis/report.json`。

## RQ1_2046acc1c802

FREEZE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_58de46f081ec](FCR_12.md#rq1_58de46f081ec)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 16 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×31。本次：excluded/compiler_generated_readonly_getter×15、open/relevant_source_scope_without_resolved_property×14、open/decisive_property_or_source_residual×2。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 65 项调查动作、21 条查询记录（sat×19、unsat×2），底层求解 23 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_6c686f16863e462b8666`，baseline_usable → sat，条件摘要 `bdd98ce15f2d24ee22cffe40389ff77df6f66ca289f89023a3d753b7a14cfb11`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3538/9853 | 833b1e4d2995 | 772c10f881b3 |
| main/1 | focused_revision | stop/analysis_received | 4164/2819 | 4b7b1f5670db | c5534c88cb82 |



选定来源：main；报告 SHA-256 `9322926b1384d40b866b5da750accb93dc6528c0cca8413b2acd8be723d18c16`；报告位于原归档 `run/members/RQ1_2046acc1c802/attempt_1/analysis/report.json`。

## RQ1_8e8598bb724e

PAUSE · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_fbd0377ce541](FCR_04.md#rq1_fbd0377ce541)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | transferOwnership(address) | 未确认 | financial_property_conditions_not_established |
| obligation_question_0d8022b8dc195686 | disableTransfers(bool) | supported | — |
| obligation_question_ce43884d901ec25d | disableTransfers(bool) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×17、relevant_source_scope_without_resolved_property×2、source_positions_and_resolved_properties×2。本次：excluded/compiler_generated_readonly_getter×12、open/relevant_source_scope_without_resolved_property×4、excluded/committed_exits_have_no_state_or_external_effect×2、excluded/source_positions_and_resolved_properties×2、open/decisive_property_or_source_residual×1。与最终指定类性质标识严格相同的查询结果：sat×6。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_e9b506226cf33ba9a173 | FCR-PAUSE | disableTransfers(bool)@2512 | property_6961e884df7c7bd95f33 | E10,E14,E5 |
| finding_03e200aaa9ca74254294 | FCR-PAUSE | disableTransfers(bool)@2512 | property_a564bc69258f4f13aea7 | E11,E15,E9 |



该成员共 2 次真实提交；选定报告登记 18 项调查动作、14 条查询记录（sat×14），底层求解 18 次。反馈登记消费 1 行；检查点类别 FCR-PAUSE×2，最终类别 FCR-PAUSE×2。

可核对的检查示例：`probe_b31b1ae30fc38384d9be`，control_transition_preservation → sat，条件摘要 `b8e859b3e6e7f162d67882e6b82535f9fe6cf2c6667caa365727f95eabc4e437`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3014/4301 | 552fc0a3aeb9 | 51a1ddac6744 |
| main/1 | focused_revision | stop/analysis_received | 3682/6413 | ceab6d01945f | 5c8eaf887e30 |



选定来源：main；报告 SHA-256 `96e0e44312c745b0d42eda8375ed3fc31a838a8ec6826f5aaf55211fe0d2cb95`；报告位于原归档 `run/members/RQ1_8e8598bb724e/attempt_1/analysis/report.json`。
