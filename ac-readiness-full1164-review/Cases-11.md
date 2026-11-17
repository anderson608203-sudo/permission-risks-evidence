# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_3858ff02d02c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_3858ff02d02c) · 检查明细 [Checks-33.json](Checks-33.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:251:author:1 | TokenERC20 | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 6, 'external_dependency': 3}。相关检查决定 {'policy_missing': 55, 'external_dependency': 33, 'self_delegation': 1, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 902.323 秒，模型等待 54.717 秒，真实 solver 11 次，查询投影 34 项，动作记录含缓存 218 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 87, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'action_slice_exhausted': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `7e58d846f4068fcefc895f18aed3bc92ca9b8db014c3d4fbbc4187365644a2eb`，决定 SHA `36136d627deeb93fdbd1536c0eae4ef17a19413c1c46b21f5db94e5f6d4b074e`。

## RQ1_fbc7ca489536

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-05.md#rq1_fbc7ca489536) · 检查明细 [Checks-33.json](Checks-33.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:252:author:1 | owned | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_8531c9f63ab463372ebf`，根位置 783＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 783 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E48

发现 `finding_afa2e5f57c455c0c4674`，根位置 783＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 783 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E32

发现 `finding_c23e65d9e96a6f558a98`，根位置 783＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 783 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E41

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.976 秒，模型等待 67.646 秒，真实 solver 37 次，查询投影 51 项，动作记录含缓存 47 项。诊断 {'audit_effect_unbound': 1, 'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 12, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `e3f102de447d9d20e7f913a186f34a017221cbae0b22e54d6cca50b914a90f99`，决定 SHA `59c6015933f28cd12c4d2408d9dde7f6a7f3b6d16f03d3c90de45a33e1083a18`。

## RQ1_fc71e6703f0d

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_fc71e6703f0d) · 检查明细 [Checks-33.json](Checks-33.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:253:original:1 | pay | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |
| D2:253:original:2 | fin | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 1}。相关检查决定 {'external_dependency': 1, 'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.257 秒，模型等待 34.009 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `267081788918508e2650c74d60a5f89cb73a3c619a310c98c9cbe715b532a714`，决定 SHA `77e30486429b4a878ba6947e16a5516d5288521b07e41c2a5ff9654e921f2f69`。

## RQ1_c682dc91e18c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_c682dc91e18c) · 检查明细 [Checks-33.json](Checks-33.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2}。相关检查决定 {'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.199 秒，模型等待 43.536 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `a9323701b77773073132960ebac9366353f38c1deac1ec8023af932517e5b97b`，决定 SHA `476ddbfbaf1abf9adbb953422dabdf6eb22d8bcb68d968478ef6933ae0f2bf9d`。

## RQ1_cc6f48967dd0

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_cc6f48967dd0) · 检查明细 [Checks-33.json](Checks-33.json) [Checks-34.json](Checks-34.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5, 'policy_missing': 7}。相关检查决定 {'external_dependency': 64, 'policy_missing': 14}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 156.794 秒，模型等待 37.820 秒，真实 solver 9 次，查询投影 22 项，动作记录含缓存 304 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 78, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `0805e3c782e8a068f287563befa3d3eacdce353dec377239d22db0b08e192142`，决定 SHA `3086e3da50868b4ede381035dd054767086c46cd70f43617fa199fbafa7bcc68`。

## RQ1_0b9a9d5a2319

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_0b9a9d5a2319) · 检查明细 [Checks-34.json](Checks-34.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:256:S1 | initVault | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:256:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:256:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:256:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 7}。相关检查决定 {'policy_missing': 18, 'applicable_role_guard': 1, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.969 秒，模型等待 65.530 秒，真实 solver 62 次，查询投影 93 项，动作记录含缓存 45 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 16}。

最终报告 SHA `541dd59967dc71e5a6c8d869459965f64329d5711b621e94121521797b5c2a26`，决定 SHA `20bb428c450b940b4959edb816c660740166300638ea419de170d6a644a807c3`。

## RQ1_be415055dd52

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_be415055dd52) · 检查明细 [Checks-34.json](Checks-34.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 9, 'external_dependency': 4}。相关检查决定 {'external_dependency': 24, 'policy_missing': 14, 'applicable_role_guard': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 29.825 秒，模型等待 30.376 秒，真实 solver 27 次，查询投影 79 项，动作记录含缓存 130 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 36, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ae57bec438d7a7322714179da5345a798737afb5e664e5f0342c39c65a6964ee`，决定 SHA `89e9da49a25f3fe8bc3813b015dc875629142c7733e036c37fbabfa94c750d04`。

## RQ1_f4232c234a28

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-05.md#rq1_f4232c234a28) · 检查明细 [Checks-34.json](Checks-34.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:258:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_3873e3e9c2b52577b9d3`，根位置 2550＋531，依据 `program_support`。At transferFrom(address,address,uint256), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification. 证据 E1, E17

发现 `finding_39094289e46f006807da`，根位置 2228＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2228 under financial_right. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E12

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.884 秒，模型等待 106.041 秒，真实 solver 43 次，查询投影 54 项，动作记录含缓存 23 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 8, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `9d8e2091f6b26fa9c35de47ff888dbf30e04a15f64013827114844129ddb6d05`，决定 SHA `2138c821a52b98bd5d7bb745f71f8a40beb7993679b62d5972ede7e39c07df30`。

## RQ1_356ce1d2c1cd

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_356ce1d2c1cd) · 检查明细 [Checks-34.json](Checks-34.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 11, 'external_dependency': 9}。相关检查决定 {'policy_missing': 32}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 216.296 秒，模型等待 38.520 秒，真实 solver 16 次，查询投影 18 项，动作记录含缓存 89 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 32, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `65e0350821dd28b993ef2bb252dcc9d0e6b3f43fe769b7270d7b36e210587183`，决定 SHA `98e5b0c1316bd85706a8508361e2b77b6bd4da75a3c4e8e1df566bca1d3d434d`。

## RQ1_1c78ccedbbb4

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_1c78ccedbbb4) · 检查明细 [Checks-34.json](Checks-34.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 23}。相关检查决定 {'external_dependency': 36}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 42.420 秒，模型等待 57.475 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 120 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 36, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `14869f4131143b6236de2b4211abc5b2d6f248cc092882a9c9ac0095a01d3ff3`，决定 SHA `bd91e8e5a0d416e4e1e821fb803338c56a7ce5af4ca67c5baac5ddf04b97e06a`。

## RQ1_f4451d46dab1

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-05.md#rq1_f4451d46dab1) · 检查明细 [Checks-34.json](Checks-34.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:261:author:1 | testhash | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_e7dbd5dc74e172b074e6`，根位置 3051＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 3051 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E309

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 119.295 秒，模型等待 44.736 秒，真实 solver 84 次，查询投影 99 项，动作记录含缓存 445 项。诊断 {'missing_claim_or_source_anchor': 4, 'unrelated_or_secondary_graph_pairs_deferred': 151, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `f622d226309d851ab9c704565f0238e43ce04733e385c81e5cc5ce2e4b8c37e4`，决定 SHA `be2b077cc41a2cdcbc64feb6516a8a0bcff6b02f317770878b4f9a4a2c676129`。

## RQ1_e03de50a6811

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_e03de50a6811) · 检查明细 [Checks-34.json](Checks-34.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1, 'policy_missing': 1}。相关检查决定 {'policy_missing': 1, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.342 秒，模型等待 34.807 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 6 项。诊断 {}。

最终报告 SHA `186aa46407589001a22c041789570f72b18285d17ea6deab53b965d15e6a1e6d`，决定 SHA `4c1664f878bb2c93a1c6332345033b5a953f5eb6015dbeeec1c5d4201273d6dc`。

## RQ1_13ae033611ed

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-05.md#rq1_13ae033611ed) · 检查明细 [Checks-34.json](Checks-34.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:263:author:1 | DTCC_ILOW_2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_9b2b5b988295913cb6e0`，根位置 821＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 821 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E21

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.539 秒，模型等待 25.149 秒，真实 solver 57 次，查询投影 69 项，动作记录含缓存 45 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `36000c951d569d1f78a653d979f3e3bbfdd762108db1eb3889f248fc8d9d6661`，决定 SHA `fcc1771ae7cde5455b7cf2a4865bdb69369e99838d60accc1b3b132b95ef2cd7`。

## RQ1_509dd4151768

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-05.md#rq1_509dd4151768) · 检查明细 [Checks-34.json](Checks-34.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:264:author:1 | Constructor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_34936c5a683b35c44dd4`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E53

发现 `finding_3264cfb4512547c0ee3d`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E57

发现 `finding_251ca3e505512e380eab`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E49

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.718 秒，模型等待 80.922 秒，真实 solver 30 次，查询投影 72 项，动作记录含缓存 94 项。诊断 {'invalid_issue_field_shape': 1, 'unrelated_or_secondary_graph_pairs_deferred': 30, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `9a049ce722066616c748c2ace07732818273cc96763a6de0e32f9e7d9ace0030`，决定 SHA `badaa2cd0173addab946863dc5a593e184bc904a36b0ba611efab90f7bed44b1`。

## RQ1_0cd685c505a3

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_0cd685c505a3) · 检查明细 [Checks-34.json](Checks-34.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:265:author:1 | BITCOIMINIG | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'external_dependency': 26, 'policy_missing': 34, 'applicable_role_guard': 1, 'self_delegation': 1, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 24.641 秒，模型等待 39.028 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `9b07b82f8fd5f1ddfd32dea19d898018a4f1f15f569b7f8df881767ddef78543`，决定 SHA `c49b0d7623c32358ef0df98b5287281446d9f025162b42f600e7360cc94e3e44`。

## RQ1_98c10d1902f1

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_98c10d1902f1) · 检查明细 [Checks-34.json](Checks-34.json) [Checks-35.json](Checks-35.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 16, 'policy_missing': 3}。相关检查决定 {'external_dependency': 83, 'policy_missing': 39}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 116.064 秒，模型等待 61.271 秒，真实 solver 13 次，查询投影 24 项，动作记录含缓存 271 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 122, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `3ae2e78c6b3e3f22a7213010499bacf72c889aff16a9c58ae647639fa5dcad01`，决定 SHA `5dd200e038a1e97e50ddd5dbbcf97f557c21f0ce56dff184b21ff30d4bfeb01a`。

## RQ1_c0ce67b52132

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_c0ce67b52132) · 检查明细 [Checks-35.json](Checks-35.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:267:author:1 | reward | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 2}。相关检查决定 {'policy_missing': 6, 'external_dependency': 19}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.488 秒，模型等待 98.735 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 52 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 22, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `bb6f94b179c61ca7bc2dbbcb0bcc96dfd59e9eba82a7688a2070af5410234ecf`，决定 SHA `cffeb7e857d3f677e7e5d9565a7ca55fcc4dfa129cf0145628b8a4567c3f7674`。

## RQ1_484b7bd1d895

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_484b7bd1d895) · 检查明细 [Checks-35.json](Checks-35.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:268:author:1 | Xply | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1}。相关检查决定 {'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.196 秒，模型等待 50.705 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'explicit_effect_anchor_conflict': 1, 'semantic_answer_outside_sent_scope': 1}。

最终报告 SHA `ac1c0137f99f4d551ae580d254e9542dcdf38594369aab55163e0f6a40b3d235`，决定 SHA `cc191c0bc6d00fcd50eb0ee33be6a2d7a1110cddf8b7670c77bd3f68e162639a`。

## RQ1_43f3b3792955

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-06.md#rq1_43f3b3792955) · 检查明细 [Checks-35.json](Checks-35.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:269:author:1 | constuctor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_bfa3f0ddbaec525382d8`，根位置 104＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 104 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E2

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.341 秒，模型等待 10.657 秒，真实 solver 2 次，查询投影 3 项，动作记录含缓存 2 项。诊断 {'unknown_or_unshown_effect': 1}。

最终报告 SHA `c55efefafa5fd13653f237a181759d27c3a862394699b246d9b598e7d830e7ac`，决定 SHA `75057e8844ee199243cea02b79538dab009ec1e88a372d223e8b2278790834cd`。

## RQ1_9dba071478ae

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_9dba071478ae) · 检查明细 [Checks-35.json](Checks-35.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 11}。相关检查决定 {'holder_own_transfer': 8, 'policy_missing': 31, 'self_delegation': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.721 秒，模型等待 38.875 秒，真实 solver 37 次，查询投影 44 项，动作记录含缓存 75 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 30, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `361d4c911f1b030c9dcfc2da7a64ca592d1d71f95fb633e26f003d22ead15b1a`，决定 SHA `fdfaedff319bf5f37b21241e6704e66b0040d836ee5474ee51b63f1260283221`。

## RQ1_befa513e0336

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_befa513e0336) · 检查明细 [Checks-35.json](Checks-35.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:271:author:1 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 4}。相关检查决定 {'external_dependency': 12, 'policy_missing': 6, 'holder_own_transfer': 2, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.037 秒，模型等待 36.470 秒，真实 solver 11 次，查询投影 11 项，动作记录含缓存 58 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 13, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `dfea0f9a56075705833699585c58caf95916a4c12cd598986d441c843ef9a391`，决定 SHA `9b27f5b012edc447a6926cacd2e7bebf27f5421d0f73654115e8606149547685`。

## RQ1_15861b8a3362

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_15861b8a3362) · 检查明细 [Checks-35.json](Checks-35.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'external_dependency': 8}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.630 秒，模型等待 29.497 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 22 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 8, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `da5fba73a0fbe4eead28b3f09d57a1e74232e470e5044805a16fff9bcf44c2ac`，决定 SHA `a800bcf2bbb66ef6eb30d3d6b387b3b52c77d12726a7a326032b24f7a862effe`。

## RQ1_38c47e7a430d

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_38c47e7a430d) · 检查明细 [Checks-35.json](Checks-35.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 2}。相关检查决定 {'applicable_role_guard': 1, 'external_dependency': 2, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.577 秒，模型等待 36.451 秒，真实 solver 14 次，查询投影 14 项，动作记录含缓存 13 项。诊断 {'explicit_effect_anchor_conflict': 2, 'unrelated_or_secondary_graph_pairs_deferred': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `67a2193025a8cd1681a2fe1ce6951caeba844a84df5c90e43cffbda0f45e9485`，决定 SHA `5cbfdd726dcb60cd8072b9a6b0e919d08dbd9b053aacc89f85a0e37f6de8e71c`。

## RQ1_ade4bfdad9b5

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_ade4bfdad9b5) · 检查明细 [Checks-35.json](Checks-35.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 1}。相关检查决定 {'policy_missing': 1, 'external_dependency': 12}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.372 秒，模型等待 39.408 秒，真实 solver 9 次，查询投影 9 项，动作记录含缓存 28 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 13, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `eb4df780c77c31c44937d5d22d5212ff102064deed437450134d782d7fe970b6`，决定 SHA `b30d2206a3b92dbb780d71de8b934f90080a0c1e5e8197afbd432ee751bc607b`。
