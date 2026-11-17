# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_4a942c517226

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_4a942c517226) · 检查明细 [Checks-05.json](Checks-05.json) · 查询明细 [Queries-02.json](Queries-02.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 17, 'external_dependency': 9}。相关检查决定 {'policy_missing': 40, 'external_dependency': 5, 'holder_own_transfer': 4, 'self_delegation': 2, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 44.695 秒，模型等待 49.173 秒，真实 solver 86 次，查询投影 95 项，动作记录含缓存 140 项。诊断 {'core_unresolved_retained_for_investigation': 1, 'unrelated_or_secondary_graph_pairs_deferred': 32, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `f1287639cf1f2b3fd28c390b043da10a9fe6912205137379efd44f7b24d449bb`，决定 SHA `87d05ed9f45795af39a9d96725970d8c3265cbd0d49f9e4cb4ee196b1c3ec0cc`。

## RQ1_42a705a8b30a

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_42a705a8b30a) · 检查明细 [Checks-05.json](Checks-05.json) · 查询明细 [Queries-02.json](Queries-02.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 9, 'external_dependency': 4}。相关检查决定 {'external_dependency': 19, 'policy_missing': 20, 'self_delegation': 2, 'holder_own_transfer': 6, 'applicable_role_guard': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 17.703 秒，模型等待 60.998 秒，真实 solver 58 次，查询投影 92 项，动作记录含缓存 113 项。诊断 {'audit_source_scope_mismatch': 1, 'audit_effect_unbound': 1, 'unrelated_or_secondary_graph_pairs_deferred': 37, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `745410b3f0a790226afec68f3e518d7fbb70ab434095bc09759cd2b8cfe046a1`，决定 SHA `bc84c638cf2ad9f3471819560e33db0860942cf65fac3e9395dc214385ec80eb`。

## RQ1_102fa202b58e

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-01.md#rq1_102fa202b58e) · 检查明细 [Checks-05.json](Checks-05.json) · 查询明细 [Queries-02.json](Queries-02.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:29:author:1 | Constructor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_11ba05ccb564a9309cd4`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E49

发现 `finding_b2d86de6af17c9e8b674`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E53

发现 `finding_1ac07c2f99422d97e85e`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E45

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.321 秒，模型等待 50.382 秒，真实 solver 20 次，查询投影 60 项，动作记录含缓存 80 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 24, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `27297a74c9c7be46371bcd12eda1a2cf1e756483e3c7f78b50eb6779ca16c00d`，决定 SHA `57dae8c2e64a503aa9c213fcbc2200c96612466d19977aa90e59d4422ff29f2c`。

## RQ1_2be3e9b98fac

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-01.md#rq1_2be3e9b98fac) · 检查明细 [Checks-05.json](Checks-05.json) · 查询明细 [Queries-02.json](Queries-02.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:30:author:1 | IstriumToken | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_1634f4dc94d2e9e89ced`，根位置 755＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 755 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E21

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.677 秒，模型等待 43.310 秒，真实 solver 17 次，查询投影 29 项，动作记录含缓存 19 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `d44091152a04734eb6bfa1c54bf237fafac89b17fb96650df3138311c3ccf3fd`，决定 SHA `c042568b932799ff47b0f0c5763d1fb219dcf119c3a2774eec2a4bb8ef8ccde9`。

## RQ1_a4f43feac855

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-01.md#rq1_a4f43feac855) · 检查明细 [Checks-05.json](Checks-05.json) · 查询明细 [Queries-02.json](Queries-02.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:31:author:1 | Owned2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_5ba08069697ca74e9d2d`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E18

发现 `finding_18d7e791c848131f9e93`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E25

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.436 秒，模型等待 66.018 秒，真实 solver 12 次，查询投影 28 项，动作记录含缓存 28 项。诊断 {'no_locatable_source': 7, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `29610b540bb3cc5fd26d288b1c14e9b484bb3b8949965a8be92f0c40ed56b027`，决定 SHA `5ba6af35521441deddb00780206eb31ddb78022eb1c4846b1e75b57f3a6e8823`。

## RQ1_ffad715abd89

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_ffad715abd89) · 检查明细 [Checks-05.json](Checks-05.json) · 查询明细 [Queries-02.json](Queries-02.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 9}。相关检查决定 {'external_dependency': 54, 'policy_missing': 18, 'holder_own_transfer': 4, 'self_delegation': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 383.886 秒，模型等待 30.234 秒，真实 solver 41 次，查询投影 89 项，动作记录含缓存 244 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 72, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c2ec4c1505a126400b41348434e761a1472347a8cf8c6f653e0bcb1627437e23`，决定 SHA `3ec1d20e4a43afa91a82ef897cd59fe5ed723bd01aa35723958994814201079a`。

## RQ1_2a54840e0e44

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_2a54840e0e44) · 检查明细 [Checks-05.json](Checks-05.json) · 查询明细 [Queries-02.json](Queries-02.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:33:author:1 | mintForwarder | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 4}。相关检查决定 {'external_dependency': 2, 'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.206 秒，模型等待 29.451 秒，真实 solver 1 次，查询投影 6 项，动作记录含缓存 9 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `779e621477515a335ab6713bb9734f3572b572bb9e1689153d9c4fa2130138cc`，决定 SHA `d99337717a18e20a84499b0e39da3c73ab39eaca41430a63dd72a0d2f4193098`。

## RQ1_df8a7a882d5c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_df8a7a882d5c) · 检查明细 [Checks-05.json](Checks-05.json) · 查询明细 [Queries-02.json](Queries-02.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 3}。相关检查决定 {'policy_missing': 45, 'external_dependency': 8, 'source_check_excluded': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 68.213 秒，模型等待 40.461 秒，真实 solver 3 次，查询投影 3 项，动作记录含缓存 105 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 57, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `928fbb6a88cd6e7c040a117d762b911108b4c60d03f506baad645c77c01dd443`，决定 SHA `ed539548b0e727bb51bcec2031d63c8d317b97dde83e9efa73c4cb923ce50d1e`。

## RQ1_d7e878e5e46c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_d7e878e5e46c) · 检查明细 [Checks-05.json](Checks-05.json) · 查询明细 [Queries-02.json](Queries-02.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 6}。相关检查决定 {'policy_missing': 30, 'external_dependency': 31}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 35.969 秒，模型等待 64.656 秒，真实 solver 76 次，查询投影 101 项，动作记录含缓存 194 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 61, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `b673a2fe65c112a753da6a6feb56da9328dc8f4b43bb3f285f95af23068bf58a`，决定 SHA `1eedb4e67b5db1402d4dd55734e3425920ed9286f00d47510edc740414de966d`。

## RQ1_d80631993985

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_d80631993985) · 检查明细 [Checks-05.json](Checks-05.json) · 查询明细 [Queries-02.json](Queries-02.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:36:author:1 | LEGEND | FN | TP | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'policy_missing': 34, 'external_dependency': 26, 'holder_own_transfer': 2, 'applicable_role_guard': 1, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 27.295 秒，模型等待 75.044 秒，真实 solver 76 次，查询投影 92 项，动作记录含缓存 147 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `22280be9e2f04f25238bfa0f6478f7853ad04b72dfb96bc4b9673d15ca9ab301`，决定 SHA `e5fca65a8446de167d566273de7136c247cf548235b40fc088311788ab3a7424`。

## RQ1_511b9f30f4b7

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_511b9f30f4b7) · 检查明细 [Checks-05.json](Checks-05.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:38:author:1 | withdrawTokens | FN | FN | FN | FN | no_listed_obligation_at_reference |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {'external_dependency': 10}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 99.998 秒，模型等待 74.007 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 22 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 4, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `dd534a0fbfddd58496b310da63dc7e4cc2572f61e6bbf5f8c624f6e73c9a7916`，决定 SHA `21683042f314d1299519e494217225423e1073d90c8d437d0ef73a7ba5c86b49`。

## RQ1_fccabbab2795

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_fccabbab2795) · 检查明细 [Checks-05.json](Checks-05.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2, 'policy_missing': 2}。相关检查决定 {'external_dependency': 1, 'policy_missing': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.494 秒，模型等待 41.251 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 12 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 4}。

最终报告 SHA `552840139fe6ab9df17fa4f0527e75b44fbb3840069ff08f7e6fd454c02ec83d`，决定 SHA `6fd58fcc1297f69a6b72fe2925a18c0c4f8727c639b74647c6195c5018c3a697`。

## RQ1_cfc98cba39c3

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_cfc98cba39c3) · 检查明细 [Checks-05.json](Checks-05.json) [Checks-06.json](Checks-06.json) · 查询明细 [Queries-02.json](Queries-02.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:40:author:1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 24, 'policy_missing': 4}。相关检查决定 {'policy_missing': 8, 'external_dependency': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.457 秒，模型等待 41.506 秒，真实 solver 14 次，查询投影 18 项，动作记录含缓存 33 项。诊断 {'explicit_effect_anchor_conflict': 2, 'unrelated_or_secondary_graph_pairs_deferred': 13, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `2ab1414c91764af7bced343b7f57d46a0077b091d70816f292bf543b81e985f2`，决定 SHA `280347a7063cedda481ac80bf09bcec4cf7dd9ced32350b920c472025c00e285`。

## RQ1_6d7db4fbefe5

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_6d7db4fbefe5) · 检查明细 [Checks-06.json](Checks-06.json) · 查询明细 [Queries-02.json](Queries-02.json) [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:41:author:1 | CFCdistrubution | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'policy_missing': 34, 'external_dependency': 26, 'holder_own_transfer': 2, 'self_delegation': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 25.996 秒，模型等待 33.133 秒，真实 solver 61 次，查询投影 70 项，动作记录含缓存 150 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `a73d02e631ecfc9dd2db5c6fbb12c6ba61c8cb7d6d02494fb96262a37d425567`，决定 SHA `8c8b8b10c005a44b40fd552ba3286d942cd1d6c0300025257b5a5d14179053ca`。

## RQ1_db21f2b7c77d

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-01.md#rq1_db21f2b7c77d) · 检查明细 [Checks-06.json](Checks-06.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:42:author:1 | mintTo | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_b52eba67f674bb9d972d`，根位置 2245＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2245. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E7

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.613 秒，模型等待 57.631 秒，真实 solver 13 次，查询投影 14 项，动作记录含缓存 16 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `6866209562b1d20d63bebcff0c3719f5ed866ef998787331ef10e06b16a2818e`，决定 SHA `06ae31aab81b8ccfe2d47bb8524497af0a6e4d3c77c5f9b1584b300d32d2c275`。

## RQ1_cfe97b8f7250

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_cfe97b8f7250) · 检查明细 [Checks-06.json](Checks-06.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:43:author:1 | bioLock | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 53, 'external_dependency': 29}。相关检查决定 {'holder_own_transfer': 28, 'policy_missing': 125, 'external_dependency': 135, 'self_delegation': 7, 'applicable_role_guard': 7}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 204.293 秒，模型等待 33.706 秒，真实 solver 295 次，查询投影 389 项，动作记录含缓存 625 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 255, 'noncached_action_limit': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c195aa4893b1e126a51090ea692dbce9a4be8694a751d312f8532efe12f797ae`，决定 SHA `a2878ee1d4d0945c6b8e094ce46907285f8108611e9f1ab14a11357ca7054a4d`。

## RQ1_3b975bee1104

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_3b975bee1104) · 检查明细 [Checks-06.json](Checks-06.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:44:author:1 | TokenERC20 | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 3}。相关检查决定 {'policy_missing': 24, 'external_dependency': 9, 'self_delegation': 1, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 56.795 秒，模型等待 41.945 秒，真实 solver 18 次，查询投影 23 项，动作记录含缓存 95 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 32, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `18be255b93f6358616c58a1b7ab72ba76e058314d9d861411c807e302545d24f`，决定 SHA `42229f5e35b83479d34d1cedbd5fc6b853db151d71fab58f5ca8f5685a117b48`。

## RQ1_8f44e59cd670

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_8f44e59cd670) · 检查明细 [Checks-06.json](Checks-06.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:45:author:1 | HTX | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 8}。相关检查决定 {'policy_missing': 34, 'external_dependency': 26, 'applicable_role_guard': 1, 'self_delegation': 1, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 26.239 秒，模型等待 55.279 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'missing_claim_or_source_anchor': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `92227ee8a9c0b6fe77172c329341d8076855db7d5861b5d3dd1a4ff3df599220`，决定 SHA `df3c5f67e36588d9e8af8299966a953a29b51131cffe83294e036dabdbc69f79`。

## RQ1_413987a86ea4

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-01.md#rq1_413987a86ea4) · 检查明细 [Checks-06.json](Checks-06.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:46:S1 | fallback | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_08fb6cf8b0619f8e2aa9`，根位置 823＋29，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 823. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.264 秒，模型等待 39.015 秒，真实 solver 16 次，查询投影 16 项，动作记录含缓存 13 项。诊断 {'unknown_or_unshown_effect': 2, 'unrelated_or_secondary_graph_pairs_deferred': 3, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c100944062aadc1efde014a571cb9c6b85baee5a7bdc1d34808a8c313e351023`，决定 SHA `e7e64f6ca9e213a03a2840027495acb4a55c08ecf95d1f3a8ac66af678fe7ebe`。

## RQ1_e97f2d279ad9

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-01.md#rq1_e97f2d279ad9) · 检查明细 [Checks-06.json](Checks-06.json) [Checks-07.json](Checks-07.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:47:S1 | Prosperity | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:47:S2 | giveBlockReward | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 13, 'external_dependency': 5}。相关检查决定 {'policy_missing': 33, 'external_dependency': 9, 'self_delegation': 2, 'applicable_role_guard': 1, 'holder_own_transfer': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.963 秒，模型等待 133.865 秒，真实 solver 65 次，查询投影 84 项，动作记录含缓存 113 项。诊断 {'unbound_or_inapplicable_seed': 5, 'audit_effect_unbound': 1, 'shared_declaration_in_distinct_applied_contexts': 1, 'no_locatable_source': 5, 'unrelated_or_secondary_graph_pairs_deferred': 39, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `bfb921f507b1b71ad08aa1d1a3677d6573a7f135d827b5850e58f2f41ecb62ed`，决定 SHA `2c8c77c33503ddbe364d6260e089ffb3f4d5b7f5ad6546ee9ba9672879cb89df`。

## RQ1_0673ce4db7a3

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_0673ce4db7a3) · 检查明细 [Checks-07.json](Checks-07.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 46, 'policy_missing': 4}。相关检查决定 {'policy_missing': 10, 'external_dependency': 40, 'applicable_role_guard': 1, 'self_delegation': 1, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 44.367 秒，模型等待 44.244 秒，真实 solver 20 次，查询投影 26 项，动作记录含缓存 187 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 41}。

最终报告 SHA `4141486b141c982818d9bef6a6c8e092dd81b73f0351ec639b75d6e04d4bddf9`，决定 SHA `030c49027a7c277345e2339eca25bd40c5de07da6d97b8ec92298683b9b1ae31`。

## RQ1_8a6f195a0ea2

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_8a6f195a0ea2) · 检查明细  · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.393 秒，模型等待 24.090 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'unknown_or_unshown_effect': 1}。

最终报告 SHA `019fa4bf17ef98107fe3dce42766d1a968d083b251d3e0fb04b35e6f7d44e1dc`，决定 SHA `a434ee01bf4cb2879df45cc3a7083b99d0bcd3942b6e878d87bd3b1401ee4172`。

## RQ1_c20b10d094d5

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-02.md#rq1_c20b10d094d5) · 检查明细 [Checks-07.json](Checks-07.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:50:author:1 | ETHERanate | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_c5e56e5c45094fdf49a2`，根位置 541＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 541. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 586.391 秒，模型等待 50.088 秒，真实 solver 7 次，查询投影 7 项，动作记录含缓存 418 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 206, 'yield_to_source_bound_semantic_review': 1}。

最终报告 SHA `b95aff339e7f2eb00114db73a9804dfbae214c64d7a5192d4b0030232928998c`，决定 SHA `aa6902d2f0e4989aa0307b26eae3a93699407213fcf3a9e29ffbb1e43a1fbec4`。

## RQ1_d3ad40e95870

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_d3ad40e95870) · 检查明细 [Checks-07.json](Checks-07.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 12, 'external_dependency': 6}。相关检查决定 {'policy_missing': 15, 'applicable_role_guard': 4, 'external_dependency': 9, 'holder_own_transfer': 4, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.300 秒，模型等待 31.590 秒，真实 solver 73 次，查询投影 159 项，动作记录含缓存 95 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 19, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c4f6a3998632075725726651c2daf2dcc1f00f0046f56a9a11d4afe0e1a04c96`，决定 SHA `8a2acfb7564af292f5b74eb5681c5dfbcd966a9b6f1f8c6c24d57c29086bfe21`。
