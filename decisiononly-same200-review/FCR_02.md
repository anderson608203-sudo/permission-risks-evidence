# FCR 逐例复核 · 第 2 页

[返回成员索引](CaseIndex.md)

## RQ1_c24c6c95ccbd

PAUSE · 风险端。检测状态：TP。前批 → 本批：检出 → 检出。配对成员 [RQ1_32dbc2fa2433](FCR_03.md#rq1_32dbc2fa2433)。

本轮已选输出 检出；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 有效未检出

指定类在初始检查点已出现。以同类主报警和所连证据计分；不能单独归功于反馈或图。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i3 | disableTransfers(bool) | supported | — |
| i6::FCR-PAUSE | disableTransfers(bool) | supported | — |


前批指定类义务依据：source_effect_and_privilege_relevance×11、relevant_source_scope_without_resolved_property×1、source_positions_and_resolved_properties×1。本次：open/relevant_source_scope_without_resolved_property×5、excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×3、excluded/source_positions_and_resolved_properties×1。与最终指定类性质标识严格相同的查询结果：sat×4、unsat×2。标识变化不能反推旧证据无效。

| 发现 ID | 类别 | 入口及字节偏移 | 性质 ID | 证据引用 |
|---|---|---|---|---|
| finding_e6931b5172d072a0f2d7 | FCR-PAUSE | disableTransfers(bool)@1481 | property_7b1e418ab955bf821a35 | E10,E18,E2 |
| finding_a8fd83e1efe85a632bdb | FCR-PAUSE | disableTransfers(bool)@1481 | property_156f1a8d54adeb0375f1 | E13,E21,E3 |



该成员共 2 次真实提交；选定报告登记 38 项调查动作、22 条查询记录（unsat×12、sat×10），底层求解 9 次。反馈登记消费 1 行；检查点类别 FCR-PAUSE×2，最终类别 FCR-PAUSE×2。

可核对的检查示例：`probe_33bad7d30567356aa2ee`，control_transition_preservation → unsat，条件摘要 `2db6e6358be409d7e40883035723a67604b188e0cc006a0dddbd19ad1508e70c`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2284/20209 | 3606001688ce | 933d8e47782b |
| main/1 | focused_revision | stop/analysis_received | 2974/13473 | 6d2744ba5770 | fb40f40a42f2 |



选定来源：main；报告 SHA-256 `813da3a1f5ae6e424951c47e1e6930dede39cb5098e6c6f541645493c7223a20`；报告位于原归档 `run/members/RQ1_c24c6c95ccbd/attempt_1/analysis/report.json`。

## RQ1_b61f163309a1

MINT · 风险端。检测状态：U+。前批 → 本批：检出 → 未知。配对成员 [RQ1_81a85f242b60](FCR_05.md#rq1_81a85f242b60)。

本轮已选输出 未知；前次同 200 份 检出；v32 冻结 Full 检出；最近全量方法，同成员 检出；b5 冻结 Full 检出

初始检查点有 MINT，最终指定类转未知；其修复端反而出现 MINT。最终记录显示条件未建立，丢失的具体原答句子不可还原。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | allocateToken(address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_0e67a8ac14fb9ccf | fallback() | 未确认 | financial_property_conditions_not_established |
| obligation_question_f52f3f49026ceae0::FCR-MINT | setTokenExchangeRate(uint256) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×34、decisive_property_or_source_residual×1、source_positions_and_resolved_properties×1。本次：excluded/compiler_generated_readonly_getter×15、open/relevant_source_scope_without_resolved_property×11、open/decisive_property_or_source_residual×6、excluded/committed_exits_have_no_state_or_external_effect×4。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 71 项调查动作、34 条查询记录（sat×17、unsat×17），底层求解 33 次。反馈登记消费 1 行；检查点类别 FCR-MINT×1，最终类别 无。

可核对的检查示例：`probe_bd4f68c73215a880a615`，baseline_usable → sat，条件摘要 `6d0ec5d2174b5bbb597428edb2cd49e925853965076a3685146e74cac8c767d2`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 5467/11108 | 63146fec989d | 7c92e3ea94fb |
| main/1 | focused_revision | stop/analysis_received | 7525/4233 | 9658c45339c5 | 61b63a05ddc6 |



选定来源：main；报告 SHA-256 `6fa3633f4c909632fd447c62029dcce4b4d0be1dd4798f2b2abbf748cede26e4`；报告位于原归档 `run/members/RQ1_b61f163309a1/attempt_1/analysis/report.json`。

## RQ1_776a6b98d18f

DESTROY · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_8456d2957fff](FCR_05.md#rq1_8456d2957fff)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 1 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | destroy(address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |
| i2::FCR-DESTROY | destroy(address,uint256) | excluded | matched_direct_effect_impossible_on_all_applicable_positions_and_paths |


前批指定类义务依据：source_effect_and_privilege_relevance×4。本次：excluded/compiler_generated_readonly_getter×2、excluded/source_positions_and_resolved_properties×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 1 次真实提交；选定报告登记 8 项调查动作、0 条查询记录（无），底层求解 0 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：无已保存的程序查询。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1460/6541 | e1c91119a3e6 | c16c9fba8d72 |



选定来源：main；报告 SHA-256 `efce25c9f9e28d56d20e477e9b81c5416d3e2cbf3987bb74cff0f2e80dc974e1`；报告位于原归档 `run/members/RQ1_776a6b98d18f/attempt_1/analysis/report.json`。

## RQ1_a7bf9487cc3f

FREEZE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_c772c59e4a76](FCR_03.md#rq1_c772c59e4a76)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 17 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i5 | freezeAccount(address,bool) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×34。本次：excluded/compiler_generated_readonly_getter×17、open/relevant_source_scope_without_resolved_property×14、open/decisive_property_or_source_residual×3。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 71 项调查动作、12 条查询记录（sat×11、unsat×1），底层求解 13 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_e3ce1b1a7182e8799779`，baseline_usable → sat，条件摘要 `b0929beb8fb039f96bfd8a5deb4e757905e7022f440162e2d0c4567372c6d0fa`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 3901/10490 | dfb4a2cd36a1 | d12bdd0135b1 |
| main/1 | focused_revision | stop/analysis_received | 4514/2555 | 3663849bc49e | df1592272db7 |



选定来源：main；报告 SHA-256 `ca9eb2ab7eab8d3eb359a6bce31662f6eb6a5f3acdfbb6ff12b04d239a5074f9`；报告位于原归档 `run/members/RQ1_a7bf9487cc3f/attempt_1/analysis/report.json`。

## RQ1_46a031a993c1

FREEZE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_985c6fd1d4e4](FCR_06.md#rq1_985c6fd1d4e4)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 1 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i1 | freezeAccount(address,bool) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×9。本次：excluded/compiler_generated_readonly_getter×7、excluded/isolated_flag_no_nongenerated_reader_in_resolved_public_bodies×1、open/relevant_source_scope_without_resolved_property×1。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 1 次真实提交；选定报告登记 15 项调查动作、0 条查询记录（无），底层求解 0 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：无已保存的程序查询。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1759/5003 | a4d216de5cfa | 578490a81c15 |



选定来源：main；报告 SHA-256 `f9584fa69b6176d0591c6ba47f900b0dcbeed0c88ad7b36a96558637e2e990a9`；报告位于原归档 `run/members/RQ1_46a031a993c1/attempt_1/analysis/report.json`。

## RQ1_7a54127ed44c

PAUSE · 修复端。检测状态：U-。前批 → 本批：未知 → 未知。配对成员 [RQ1_4d2acebaa2ff](FCR_02.md#rq1_4d2acebaa2ff)。

本轮已选输出 未知；前次同 200 份 未知；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

指定类性质已进入检查，指定类仍有 14 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i5 | transfersPaused() | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×32、decisive_property_or_source_residual×2。本次：excluded/committed_exits_have_no_state_or_external_effect×15、open/relevant_source_scope_without_resolved_property×12、excluded/compiler_generated_readonly_getter×5、open/decisive_property_or_source_residual×2。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 58 项调查动作、6 条查询记录（sat×5、unsat×1），底层求解 7 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_64930703bedc2cc1f28f`，baseline_usable → sat，条件摘要 `9a46d5e41fe0e916f2a522fad89cb8ef2eb539a82682e154b0f5c1e2ba35be0f`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 8802/17622 | 86765d4f16d9 | 063752a0805d |
| main/1 | focused_revision | stop/analysis_received | 19277/11321 | d5eb7e7f67e6 | be5fc46f8e6d |



选定来源：main；报告 SHA-256 `cb0c5b3e0ed2deff6d0d74ca29908809e800befe071a6f88a9e5c76dfaf0a16b`；报告位于原归档 `run/members/RQ1_7a54127ed44c/attempt_1/analysis/report.json`。

## RQ1_ffcaa562a72d

PAUSE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_c29df435681e](FCR_08.md#rq1_c29df435681e)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 5 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×9。本次：excluded/compiler_generated_readonly_getter×4、open/decisive_property_or_source_residual×3、open/relevant_source_scope_without_resolved_property×2。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 21 项调查动作、1 条查询记录（sat×1），底层求解 1 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_bc9566bd33c139480489`，original_path_commit → sat，条件摘要 `a441684b8904bdf011d982e3c74530df19ffb98f9a39d651542866a25b1a6eca`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 2245/13619 | 812d6da09e2b | a244323610a9 |
| main/1 | focused_revision | stop/analysis_received | 6870/9704 | 304c34cf7279 | c21808be405a |



选定来源：main；报告 SHA-256 `ffc5da2e8c0f4e077d01b29ad88064c74c1752e23441042e9536390d60466148`；报告位于原归档 `run/members/RQ1_ffcaa562a72d/attempt_1/analysis/report.json`。

## RQ1_4d2acebaa2ff

PAUSE · 风险端。检测状态：U+。前批 → 本批：未知 → 未知。配对成员 [RQ1_7a54127ed44c](FCR_02.md#rq1_7a54127ed44c)。

本轮已选输出 未知；前次同 200 份 未知；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 检出

指定类性质已进入检查，指定类仍有 20 项入口义务开放。其他类别与局部检查结果不能代替本类判断。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i3::FCR-PAUSE | rebase(uint256,int256) | 未确认 | financial_property_conditions_not_established |
| i4 | setTransfersPaused(bool) | 未确认 | financial_property_conditions_not_established |
| i6::FCR-PAUSE | setUserBanStatus(address,bool) | 未确认 | financial_property_conditions_not_established |
| i7::FCR-PAUSE | decreaseAllowance(address,uint256) | 未确认 | financial_property_conditions_not_established |
| obligation_question_61eec233b35a113c | transferOwnership(address) | 未确认 | financial_property_conditions_not_established |
| obligation_question_aa971f5cf396ec94 | renounceOwnership() | 未确认 | financial_property_conditions_not_established |
| obligation_question_ac2e983168298266::FCR-PAUSE | setTransferPauseExempt(address,bool) | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×34、decisive_property_or_source_residual×4、relevant_source_scope_without_resolved_property×2。本次：excluded/committed_exits_have_no_state_or_external_effect×15、open/relevant_source_scope_without_resolved_property×12、open/decisive_property_or_source_residual×8、excluded/compiler_generated_readonly_getter×5。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 85 项调查动作、3 条查询记录（sat×3），底层求解 5 次。反馈登记消费 1 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_9641e1672b70994b7df8`，baseline_usable → sat，条件摘要 `76f7721066a499cdbec139f2ccac80ecd0e2d298dcc58701bccd975ebee874b7`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 9774/23717 | d1101b24cf05 | c332636aae0f |
| main/1 | focused_revision | stop/analysis_received | 13594/9578 | ddf15448c41e | e5f53fc8ab59 |



选定来源：main；报告 SHA-256 `ca6792f473c040268677afae48a9f71af823704f8a2d646510c741ed069b7a73`；报告位于原归档 `run/members/RQ1_4d2acebaa2ff/attempt_1/analysis/report.json`。

## RQ1_37d9daf031da

PAUSE · 风险端。检测状态：U+。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_1c6b43b24d4c](FCR_11.md#rq1_1c6b43b24d4c)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 检出；最近全量方法，同成员 未知；b5 冻结 Full 检出

指定类性质已进入检查，指定类仍有 45 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


| 指定类问题 | 源函数 | 判定 | 理由代码 |
|---|---|---|---|
| i3@25c714cf1b4a | pause() | 未确认 | financial_property_conditions_not_established |
| i3@8a6e7ddb34e3 | pause() | 未确认 | financial_property_conditions_not_established |
| i3@977b12483c58 | pause() | 未确认 | financial_property_conditions_not_established |
| i3@dbdd1793df6c | pause() | 未确认 | financial_property_conditions_not_established |


前批指定类义务依据：source_effect_and_privilege_relevance×106。本次：excluded/compiler_generated_readonly_getter×48、open/relevant_source_scope_without_resolved_property×28、open/decisive_property_or_source_residual×17、excluded/committed_exits_have_no_state_or_external_effect×13。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 1 次真实提交；选定报告登记 46 项调查动作、186 条查询记录（unsat×145、sat×41），底层求解 256 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_025824acca96f7007cbe`，baseline_usable → sat，条件摘要 `bd12310221f61e7569f7563142fe3fbb608a43cfd4209c6073c028da023df551`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 7870/22569 | 29c310d9a770 | 1a157e5ea64a |



选定来源：main；报告 SHA-256 `334a52b0e2e7960da46d2e9647d6056e283599194edbc399adef49d5ebbf17b0`；报告位于原归档 `run/members/RQ1_37d9daf031da/attempt_1/analysis/report.json`。

## RQ1_d695cf0bad2e

PAUSE · 修复端。检测状态：U-。前批 → 本批：有效未检出 → 未知。配对成员 [RQ1_cea156e41c29](FCR_10.md#rq1_cea156e41c29)。

本轮已选输出 未知；前次同 200 份 有效未检出；v32 冻结 Full 有效未检出；最近全量方法，同成员 有效未检出；b5 冻结 Full 有效未检出

没有可定位的最终指定类性质，指定类仍有 4 项入口义务开放。旧版明确不报现变为未知，不算正确阴性或有效纠错。


最终检查记录没有编入指定类的性质。

前批指定类义务依据：source_effect_and_privilege_relevance×9。本次：open/relevant_source_scope_without_resolved_property×4、excluded/committed_exits_have_no_state_or_external_effect×3、excluded/compiler_generated_readonly_getter×2。与最终指定类性质标识严格相同的查询结果：无。标识变化不能反推旧证据无效。


该成员共 2 次真实提交；选定报告登记 7 项调查动作、3 条查询记录（sat×2、unsat×1），底层求解 4 次。反馈登记消费 0 行；检查点类别 无，最终类别 无。

可核对的检查示例：`probe_a3522ddfe26985fe3f4f`，baseline_usable → sat，条件摘要 `cbeccd52a259fb918750a3f9a204ea723785454f8f000bfa5ad78f50dac024a3`。


| 来源/序号 | 阶段 | 完成/消费 | 输入/输出 | 请求摘要前12位 | 回答摘要前12位 |
|---|---|---|---|---|---|
| main/0 | initial | stop/analysis_received | 1859/5597 | 364bb784faf7 | 1b9492dfbfd4 |
| main/1 | focused_revision | stop/analysis_received | 2622/2314 | 5f143f2e7bcd | 32101f62b710 |



选定来源：main；报告 SHA-256 `05f49535bb2201f13bf6f53bd9284c5b9307c88792b8199274d8148d3d51fb94`；报告位于原归档 `run/members/RQ1_d695cf0bad2e/attempt_1/analysis/report.json`。
