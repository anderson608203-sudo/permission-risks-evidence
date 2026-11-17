# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_2d6f1639f8f5

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_2d6f1639f8f5) · 检查明细 [Checks-29.json](Checks-29.json) [Checks-30.json](Checks-30.json) [Checks-31.json](Checks-31.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 8, 'policy_missing': 9}。相关检查决定 {'policy_missing': 484, 'external_dependency': 782}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 1040.216 秒，模型等待 39.220 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 13 项。诊断 {'explicit_effect_anchor_conflict': 1, 'yield_to_source_bound_semantic_review': 1, 'semantic_answer_outside_sent_scope': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `2c714c7bc15980ed48221a0e54c9727b3b7348953b798519a52a0ee955f0de29`，决定 SHA `11a1f2968d838dc1c3fb4edd0d9645aa2e345987db54e9b8e1f6d109e3d244e1`。

## RQ1_9b97fa67cb3a

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-05.md#rq1_9b97fa67cb3a) · 检查明细 [Checks-31.json](Checks-31.json) · 查询明细 [Queries-13.json](Queries-13.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 1}。相关检查决定 {'applicable_role_guard': 1, 'policy_missing': 8, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.115 秒，模型等待 41.928 秒，真实 solver 21 次，查询投影 21 项，动作记录含缓存 26 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 9, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `48c4e7b26f16fc6c73994ecaeee71b8fdeb19294ea132a88f15b8e97e8e14c7a`，决定 SHA `e803b7c10f39566b75b93ac8060fb3fada43e94cf1b6f06caadcf29b919c234e`。

## RQ1_c6aa02ce6ca1

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-05.md#rq1_c6aa02ce6ca1) · 检查明细 [Checks-31.json](Checks-31.json) · 查询明细 [Queries-13.json](Queries-13.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:228:author:1 | FirstBloodToken | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_6ce75f67f4e02c4d296d`，根位置 3905＋22，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 3905 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E4, E67

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 19.506 秒，模型等待 50.936 秒，真实 solver 24 次，查询投影 43 项，动作记录含缓存 84 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 24, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `72d781172c89901ed414ffe6ebb53c0ee87597d826b88af98c358155c22f7d78`，决定 SHA `e7f2f950024395ae94826199cf86f585b78b7c5f3c5cccfcb6e3c58a7b49a462`。

## RQ1_fdd2bcee346e

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_fdd2bcee346e) · 检查明细 [Checks-31.json](Checks-31.json) · 查询明细 [Queries-13.json](Queries-13.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:229:author:1 | setupStackDepthLib | FN | TP | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 12, 'policy_missing': 1}。相关检查决定 {'policy_missing': 2, 'external_dependency': 17}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.888 秒，模型等待 70.609 秒，真实 solver 3 次，查询投影 39 项，动作记录含缓存 58 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 3, 'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `156ba684ba7e09dcc1b994565374e808b17c6793e5167f37f0056b33adcf4a4e`，决定 SHA `938eec595625ea4fe637e9651922013b3b9ee74e4394610ad5c6a18b8d0a1597`。

## RQ1_df8af90c557e

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_df8af90c557e) · 检查明细 [Checks-31.json](Checks-31.json) · 查询明细 [Queries-13.json](Queries-13.json) [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 3}。相关检查决定 {'external_dependency': 116, 'policy_missing': 13}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 641.506 秒，模型等待 37.926 秒，真实 solver 1024 次，查询投影 1027 项，动作记录含缓存 260 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 128, 'yield_to_source_bound_semantic_review': 1, 'semantic_meaning_or_explanation_polarity_unresolved': 1}。

最终报告 SHA `5fdc479be456a3cb17e109753e1017ce4b4dce12cc260ba59b9d94c5201dbaa4`，决定 SHA `9ef157a7141f759c2d42dc20b420800490157fcc5dc4a49686c143cc025451b2`。

## RQ1_57506af34f24

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_57506af34f24) · 检查明细 [Checks-31.json](Checks-31.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:231:author:1 | HT | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'external_dependency': 26, 'policy_missing': 34, 'holder_own_transfer': 2, 'self_delegation': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 26.137 秒，模型等待 59.009 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'missing_claim_or_source_anchor': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ff314a1d1667fcc1b65bb00b52786d9a9553a18abbee26648ade18bb5e272f6a`，决定 SHA `fee58115c572e55311c2253246945cc8393a2f2008edb4f60c37452d879bd0be`。

## RQ1_c88289d0510e

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_c88289d0510e) · 检查明细 [Checks-31.json](Checks-31.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:232:author:1 | selfDestruct | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 3, 'external_dependency': 3}。相关检查决定 {'policy_missing': 9, 'external_dependency': 12}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.860 秒，模型等待 72.195 秒，真实 solver 29 次，查询投影 31 项，动作记录含缓存 60 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 18, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `860051a9507673eb519bb0606036147bf68d38c6956a8877d5ed0fd3e08d48b1`，决定 SHA `59703bfe4e40dac036c153b9ddb1677004ddf84bcb7569c4cb3c04d2a568e161`。

## RQ1_ce6eb18a49a5

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-05.md#rq1_ce6eb18a49a5) · 检查明细 [Checks-31.json](Checks-31.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:233:author:1 | initialize | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_97a9cd7ad0e08ebd5348`，根位置 340＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 340 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E20

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.237 秒，模型等待 80.494 秒，真实 solver 24 次，查询投影 30 项，动作记录含缓存 24 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 9, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `81808eb8d756cf72818823b95b9a90d3526c8dabd84b77de2096de5b21a34307`，决定 SHA `1323b0058835b78ce2d8e32cae48f811584b176484c380ed3d9c69d244a0fcb5`。

## RQ1_b583a62010f6

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-05.md#rq1_b583a62010f6) · 检查明细 [Checks-31.json](Checks-31.json) [Checks-32.json](Checks-32.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:234:author:1 | HXC | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_7d298e0d7960fc6c9298`，根位置 2854＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2854 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E211

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 96.280 秒，模型等待 39.719 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 306 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 102, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `30f244dac35c3eb3c6d99df394ef669ad58a2fca190c2db97676f5876782886f`，决定 SHA `5605fd892a9fabb11a90696f3f9b1a27bae6946470b3066cb74e768c22685c42`。

## RQ1_0a9da6eb7068

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_0a9da6eb7068) · 检查明细 [Checks-32.json](Checks-32.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 4}。相关检查决定 {'external_dependency': 13, 'applicable_role_guard': 2, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.894 秒，模型等待 30.541 秒，真实 solver 2 次，查询投影 4 项，动作记录含缓存 43 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `9f1733126b8e53c6a59d86d4a9ceac89cb282289cb399fef9a3f7f26254819cf`，决定 SHA `687e04f433c6503bb15c05da4f1f6a3e23e12b61f30269a4a6f01d50507b89bb`。

## RQ1_1007b4fc52ca

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_1007b4fc52ca) · 检查明细 [Checks-32.json](Checks-32.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:236:S1 | selfdestructs | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 13, 'external_dependency': 3}。相关检查决定 {'holder_own_transfer': 4, 'policy_missing': 30, 'self_delegation': 2, 'applicable_role_guard': 1, 'external_dependency': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.043 秒，模型等待 79.809 秒，真实 solver 71 次，查询投影 84 项，动作记录含缓存 97 项。诊断 {'audit_source_scope_mismatch': 2, 'unrelated_or_secondary_graph_pairs_deferred': 30, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `3989271c3a64279bffc429a4bfeb73e8c98e7859dd48d1adb37f4f00096c9861`，决定 SHA `9e41c7ed206c169ff65be4cc7217882c26c39faba302e28529caa5c0a9056988`。

## RQ1_98573224dd77

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_98573224dd77) · 检查明细 [Checks-32.json](Checks-32.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:237:author:1 | stopCrowdsale | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 7}。相关检查决定 {'policy_missing': 19, 'holder_own_transfer': 6, 'external_dependency': 6, 'self_delegation': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 92.443 秒，模型等待 46.559 秒，真实 solver 43 次，查询投影 43 项，动作记录含缓存 70 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 19, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `112e8816479e42d45ec28aade674e6c3a68087fcbc22f2997d5fa7b1c3838f42`，决定 SHA `4da5937e2b8323ed76ba8f47775a8c5cfb105139c26198ab1dc3084976f485ad`。

## RQ1_226d8f357d3f

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-05.md#rq1_226d8f357d3f) · 检查明细 [Checks-32.json](Checks-32.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:238:author:1 | init | FN | FN | TP | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5, 'policy_missing': 7}。相关检查决定 {'external_dependency': 9, 'holder_own_transfer': 2, 'nominee_acceptance': 9, 'self_delegation': 1, 'policy_missing': 13}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.457 秒，模型等待 60.244 秒，真实 solver 19 次，查询投影 48 项，动作记录含缓存 70 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 22, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `fd3d99c2e688a5a7d284f4d2943203608d037b9ef4b1fbcd59526d04d25c9eed`，决定 SHA `ac7b24d90728fc0c448c727d299136b5807e8982af8455e0e2dccbba5854ec20`。

## RQ1_43caf1e7f7b5

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_43caf1e7f7b5) · 检查明细 [Checks-32.json](Checks-32.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:239:S1 | init | FN | TP | FN | TP | aligned_inspection_without_matching_alarm |
| D2:239:S2 | SetReleaseDate | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:239:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:239:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2, 'policy_missing': 6}。相关检查决定 {'external_dependency': 2, 'policy_missing': 16, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.307 秒，模型等待 65.203 秒，真实 solver 84 次，查询投影 115 项，动作记录含缓存 43 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 17, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `0b5fc99b58ee49f793cf23fdd6b501d4cd32b5fc8f6729f969c0a6d4afbbbb2e`，决定 SHA `d16920b363c5262c784c56c3d0db2e418a06aacc60991a162e40b4357f3a6386`。

## RQ1_e3eee1f935e0

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_e3eee1f935e0) · 检查明细 [Checks-32.json](Checks-32.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:240:author:1 | init | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 51}。相关检查决定 {'external_dependency': 11}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 24.548 秒，模型等待 59.850 秒，真实 solver 2 次，查询投影 14 项，动作记录含缓存 32 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 2, 'semantic_answer_outside_sent_scope': 1}。

最终报告 SHA `57438e2e106ff0990e47c00b38a23f5dc7868d67154c76ae6e208da5eb84c506`，决定 SHA `83a4dd21eb0b3ff7829a3a4205220988eb74b4cb93811d429e5c535bbf650300`。

## RQ1_80bba3c533cd

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_80bba3c533cd) · 检查明细 [Checks-32.json](Checks-32.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:241:S1 | initWallet | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:241:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:241:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:241:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 3}。相关检查决定 {'policy_missing': 18, 'external_dependency': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.880 秒，模型等待 83.065 秒，真实 solver 64 次，查询投影 93 项，动作记录含缓存 45 项。诊断 {'explicit_effect_anchor_conflict': 7, 'unrelated_or_secondary_graph_pairs_deferred': 16, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5305dc555302eae3269d0f70eceb7255120a456cafa47ad764910f2404e87d2c`，决定 SHA `4fd5bb1545ded0dcdf4ea109209700d156cb8a4df94031aacabbb753fb195485`。

## RQ1_0930870e6f17

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_0930870e6f17) · 检查明细 [Checks-32.json](Checks-32.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:243:author:1 | withrawDev | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'policy_missing': 34, 'external_dependency': 26, 'holder_own_transfer': 2, 'self_delegation': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 25.374 秒，模型等待 51.580 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 148 项。诊断 {'audit_source_scope_mismatch': 1, 'audit_effect_unbound': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `582f2a8cbcfc37f7608031d1f6926d9fbbc0c88be8dc43531973656482f1df7c`，决定 SHA `bf3ae8aa158c1c7ac758af46f7eda508912d58be5e874e67c94e2d9f5b974327`。

## RQ1_5d78d6a1f8f7

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-05.md#rq1_5d78d6a1f8f7) · 检查明细 [Checks-32.json](Checks-32.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:244:author:1 | XVOTOKEN | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_3b046b35a8f142a1b0a5`，根位置 2841＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2841 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E291

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 135.348 秒，模型等待 30.761 秒，真实 solver 53 次，查询投影 73 项，动作记录含缓存 429 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 142, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `08d6214795d04a7c555a50ca108750c70f53ff277a41438214f6e7a804dac0e3`，决定 SHA `7e429407a66ae451fef6eb3017cd273eade37092040762c33885ce61554ef2ed`。

## RQ1_b38cae1d4aa8

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-05.md#rq1_b38cae1d4aa8) · 检查明细 [Checks-32.json](Checks-32.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:245:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_1c408d630f2e65d07ae5`，根位置 2221＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2221. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.905 秒，模型等待 57.077 秒，真实 solver 20 次，查询投影 26 项，动作记录含缓存 17 项。诊断 {'audit_effect_unbound': 1, 'no_locatable_source': 5, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `4a73a23f2a233fcec142eec520bdb734b998cbcf64f4e264c4266a9f29ae4c47`，决定 SHA `75b3dcf0975176a37792dbf5b9451b38f640a86a7bdd63e40838415b584036fe`。

## RQ1_2a567216aa64

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_2a567216aa64) · 检查明细 [Checks-32.json](Checks-32.json) · 查询明细 [Queries-14.json](Queries-14.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:246:author:1 | ActiveAdmin | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 2}。相关检查决定 {'applicable_role_guard': 2, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.777 秒，模型等待 17.405 秒，真实 solver 2 次，查询投影 4 项，动作记录含缓存 8 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `36fd53996120d6c83d48f7f21b00de20cb54fbd577fc5a06123a2c550732b039`，决定 SHA `55727b68383b243c5e693b6925bf7c120fbb0fb8bf0834c06e6ac7355a399de8`。

## RQ1_e5fa339cd599

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-05.md#rq1_e5fa339cd599) · 检查明细 [Checks-32.json](Checks-32.json) [Checks-33.json](Checks-33.json) · 查询明细 [Queries-14.json](Queries-14.json) [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 6, 'policy_missing': 2}。相关检查决定 {'external_dependency': 28, 'policy_missing': 45}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 66.690 秒，模型等待 77.385 秒，真实 solver 57 次，查询投影 57 项，动作记录含缓存 261 项。诊断 {'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 71, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `230472a328e4be930000624ddf6755c41b81691ad8d521a6a0116c1623555f3e`，决定 SHA `1c676a9eb846d1c49dc9cc49eb7cd98a86ff183ecf8ca58e22f2a9feb382a069`。

## RQ1_f730cc94794a

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-05.md#rq1_f730cc94794a) · 检查明细 [Checks-33.json](Checks-33.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:248:author:1 | Owned2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_bc64d28b680488777b75`，根位置 1533＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1533 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E24

发现 `finding_6e618ba589cb4d9c8b93`，根位置 1533＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1533 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E18

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.525 秒，模型等待 59.886 秒，真实 solver 11 次，查询投影 22 项，动作记录含缓存 24 项。诊断 {'missing_claim_or_source_anchor': 2, 'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `1035aa64688f0f3ca7eb865d0f6cb2ceec5a8a13beeba11e723c4e91460d40f1`，决定 SHA `add04fce5d2e8aea7a93b6c4d4476388b0bc1e6e1328ef26d8868163c8927682`。

## RQ1_a3aff7048f13

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-05.md#rq1_a3aff7048f13) · 检查明细 [Checks-33.json](Checks-33.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 22, 'external_dependency': 33}。相关检查决定 {'external_dependency': 37, 'policy_missing': 227, 'applicable_role_guard': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 392.565 秒，模型等待 150.598 秒，真实 solver 117 次，查询投影 135 项，动作记录含缓存 698 项。诊断 {'no_locatable_source': 6, 'unrelated_or_secondary_graph_pairs_deferred': 250, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `6ee5456b53cf350f3c582848ffbde4d31f19f39ca91f7f1be50113e28ddb0063`，决定 SHA `6baba2138bd0b89ca1cad9172ebbb8061ee93b1fad876a3663f5a86757953550`。

## RQ1_bb52ee421443

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-05.md#rq1_bb52ee421443) · 检查明细 [Checks-33.json](Checks-33.json) · 查询明细 [Queries-15.json](Queries-15.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:250:S1 | QLinkToken | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:250:S2 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_b9625e01d7804697991b`，根位置 2227＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2227. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E10

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.548 秒，模型等待 40.681 秒，真实 solver 12 次，查询投影 14 项，动作记录含缓存 23 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 9, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `494511e3ad15d21f2f3bc488b2fa8f2113b293992bc1e50006dad13101cce224`，决定 SHA `d5f1400018c464e489f2ad52d19038a7b72746e7ba10e0ae036cf5257f4c50b6`。
