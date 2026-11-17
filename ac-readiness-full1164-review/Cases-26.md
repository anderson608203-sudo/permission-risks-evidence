# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_4580c60aec2d

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_4580c60aec2d) · 检查明细 [Checks-78.json](Checks-78.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:619:author:1 | TokenERC20 | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 6, 'external_dependency': 3}。相关检查决定 {'policy_missing': 115, 'self_delegation': 1, 'external_dependency': 69, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 904.433 秒，模型等待 86.544 秒，真实 solver 15 次，查询投影 62 项，动作记录含缓存 412 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 183, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `3d08f0b62d9740d6d102823d51855a0d59d89e501591f7254c062e4d826219c7`，决定 SHA `29679a316ecdc7fd947e92551f9899ca66e076143df8794bb7dcc8ac49775542`。

## RQ1_117582aaa497

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-11.md#rq1_117582aaa497) · 检查明细 [Checks-78.json](Checks-78.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:620:author:1 | Owned2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_9f8f9ee09dfaa133b903`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E18

发现 `finding_c9651ec98fcaec3fc59c`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E24

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.282 秒，模型等待 54.296 秒，真实 solver 10 次，查询投影 20 项，动作记录含缓存 23 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `0dceea59beb3397f0b39ee1e7fd79129206d9744beae9d4f10dd57464bd30f69`，决定 SHA `a57da2ae54c71689065496aaa8b75f6573847a2ff4c0e0c954b417da6ec51c11`。

## RQ1_535a126ff8d8

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_535a126ff8d8) · 检查明细 [Checks-78.json](Checks-78.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1, 'not_reviewed': 1}。相关检查决定 {'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.322 秒，模型等待 59.455 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'no_locatable_source': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `543a699f59a31b88e587fa7fbe0f75b0a1ce4f0f5d4ba9ca471e3287c8f89ab9`，决定 SHA `ba3e28b2beb14d834e3afe6487e435b92409cfcdda02e917dd066a595cca35f0`。

## RQ1_dee4a75fd1b4

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_dee4a75fd1b4) · 检查明细 [Checks-78.json](Checks-78.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:622:author:1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 14, 'external_dependency': 1}。相关检查决定 {'policy_missing': 20, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.266 秒，模型等待 67.800 秒，真实 solver 43 次，查询投影 65 项，动作记录含缓存 54 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 18, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `63b2e163a1f17709193a38c8c12ac85582b5cbaeb36c47c0c57e51a114a16061`，决定 SHA `60d63d029f65e18df706b23fb8e79eb1e59f6582872647235ca534e2920e2e99`。

## RQ1_52d017b96965

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-11.md#rq1_52d017b96965) · 检查明细 [Checks-78.json](Checks-78.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:623:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_1b9a169f87ddb9b36071`，根位置 2222＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2222. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E9

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.316 秒，模型等待 55.138 秒，真实 solver 31 次，查询投影 38 项，动作记录含缓存 20 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 7, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `485c93eff19ab4b261a817dd144da2e3677645b7835ffa9c2fa77e3f41f230a6`，决定 SHA `507188c1cef673397e7abcbbf60cd893f31be1b6534a1ad4fb5400d44b6211e6`。

## RQ1_b392b57fa617

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-11.md#rq1_b392b57fa617) · 检查明细 [Checks-78.json](Checks-78.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:624:author:1 | BIMI_0001 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_5a38b5f2655dc6c097b5`，根位置 125＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 125 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E5

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 20.547 秒，模型等待 22.636 秒，真实 solver 9 次，查询投影 13 项，动作记录含缓存 7 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `7a638674150f10a3052899033b8280901944fce97c5a527019bda04d642d6d1f`，决定 SHA `a1ff7ad11d5dc8bec424d1010a49fc389208abec0b6e2a92bfba51538459e502`。

## RQ1_5e9adf3cda8c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_5e9adf3cda8c) · 检查明细 [Checks-78.json](Checks-78.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:625:original:1 | constructor | FN | FN | FN | FN | no_listed_obligation_at_reference |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5, 'policy_missing': 1}。相关检查决定 {'external_dependency': 14, 'policy_missing': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 15.018 秒，模型等待 45.704 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 60 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 17, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `583e5c814184c189889aedb54d40ec780fc18c66a3d7db06320a5fee0fca9f89`，决定 SHA `5ea91b27f552298f95693a52498eb11bf85e4a1291f4a3ca232b182f439514c0`。

## RQ1_247865e5ab88

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_247865e5ab88) · 检查明细 [Checks-78.json](Checks-78.json) [Checks-79.json](Checks-79.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:626:S1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:626:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:626:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:626:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 3}。相关检查决定 {'policy_missing': 18, 'external_dependency': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.721 秒，模型等待 68.668 秒，真实 solver 64 次，查询投影 93 项，动作记录含缓存 45 项。诊断 {'explicit_effect_anchor_conflict': 2, 'unrelated_or_secondary_graph_pairs_deferred': 16, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `ac90751f5f8386a9d741e086f9b061b8f1f8cc776a5e6e98a7266972bc45fb78`，决定 SHA `e8853559f243f602a81fc0a3bfcbd6579a3b31250049d4b86a3e582e0b5d34dc`。

## RQ1_13f2a43e4b12

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_13f2a43e4b12) · 检查明细 [Checks-79.json](Checks-79.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:322:original:1 | owned | TP | TP | TP | TP | matched |
| D2:322:original:2 | requestNumber | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_aa2875b27d7d6b7fc60f`，根位置 99＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E176, E3

发现 `finding_b699310b922ba8b1080a`，根位置 99＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E118

发现 `finding_0039e90994f123defc74`，根位置 99＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E170, E2

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 168.521 秒，模型等待 36.509 秒，真实 solver 72 次，查询投影 94 项，动作记录含缓存 339 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 109, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `d26df3eac85565fc85db560513854727ff4677fac4e8b5fc895c3c1000df70e4`，决定 SHA `926bfa4ebcb3ddedcebf8888569d5b7321cbb02d96d7d16f82d5aeb07f965b50`。

## RQ1_2e5ccd7b4bd2

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_2e5ccd7b4bd2) · 检查明细 [Checks-79.json](Checks-79.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:363:original:1 | fallback | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 6, 'external_dependency': 2}。相关检查决定 {'holder_own_transfer': 4, 'external_dependency': 27, 'policy_missing': 22, 'self_delegation': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 20.653 秒，模型等待 79.312 秒，真实 solver 64 次，查询投影 71 项，动作记录含缓存 140 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 49, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `85ce55586e29a4fdc1d067c0979b50743980307adc2fa43dd51f83a8539b19db`，决定 SHA `c6ffda382e41765d3dff32b2bbec6a50544b3eb7d3c8905e6afdd39c5c66ef82`。

## RQ1_2f01be3ebc82

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_2f01be3ebc82) · 检查明细 [Checks-79.json](Checks-79.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:94:original:1 | kill | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |
| D2:94:original:2 | withdraw | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2}。相关检查决定 {'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.150 秒，模型等待 48.311 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `b64c340e38dc1f7fa957c7f665fba797643b9bddb5a4b15d289eb0dfe2053979`，决定 SHA `118621b324148353afc66860379bb170c3cc3c63ab6300eafc10442c5d18939d`。

## RQ1_3dba1c8c9669

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_3dba1c8c9669) · 检查明细 [Checks-79.json](Checks-79.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:72:original:1 | Play | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |
| D2:72:original:2 | StartRoulette | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 1}。相关检查决定 {'policy_missing': 9, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.796 秒，模型等待 47.138 秒，真实 solver 11 次，查询投影 15 项，动作记录含缓存 22 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 11, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `99afc889e551e528b5d7d3d127058b44d20ce539adb2247faad84cbb32552a1a`，决定 SHA `c626c15314a7112b4ed2c31f1cdf4acf9590233b9ae0cb392983c1f2fab3778c`。

## RQ1_4f65b1060e4d

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_4f65b1060e4d) · 检查明细 [Checks-79.json](Checks-79.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json) [Requests-03.json](Requests-03.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:313:original:1 | TokenERC20 | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:313:original:2 | initialize | FN | FN | FN | FN | no_listed_obligation_at_reference |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 6, 'external_dependency': 3}。相关检查决定 {'policy_missing': 55, 'external_dependency': 33, 'holder_own_transfer': 2, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 902.269 秒，模型等待 30.950 秒，真实 solver 11 次，查询投影 34 项，动作记录含缓存 218 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 87, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `32f54b60bf9f4276eb284f877c993e6a3c4142d361151b0deb28e727306d7611`，决定 SHA `1ff690261995c25a07852a4f2309903af445ee09a6131e3285bd17f6663e568f`。

## RQ1_5ef9f46acd2e

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_5ef9f46acd2e) · 检查明细 [Checks-79.json](Checks-79.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:54:original:1 | fallback | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |
| D2:54:original:2 | debugDestruct | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2}。相关检查决定 {'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.313 秒，模型等待 21.917 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `93f9a032a2850cd664c9128f1130fb7ed40456f3888838704cc7a032900a51e7`，决定 SHA `cdf31c8303b75ea394eba34e7ecd7bbd0198d91378e69cb59bd8738509805a1b`。

## RQ1_7623b2a26a25

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_7623b2a26a25) · 检查明细 [Checks-79.json](Checks-79.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:450:original:1 | StartRoulette | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:450:original:2 | Play | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 1}。相关检查决定 {'policy_missing': 9, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.660 秒，模型等待 46.342 秒，真实 solver 11 次，查询投影 15 项，动作记录含缓存 22 项。诊断 {'audit_card_text': 1, 'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 11, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `6f96793eae26a6750937b84d2609f132190c70ea44db46e5be01c2b8b8deced6`，决定 SHA `07d4e50f2a185022d22bf2455e34399bfb6503130d67adfb7f6b1697e6e1599f`。

## RQ1_771e49570272

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_771e49570272) · 检查明细 [Checks-79.json](Checks-79.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:421:original:1 | StartRoulette | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:421:original:2 | Play | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 1}。相关检查决定 {'external_dependency': 2, 'policy_missing': 9}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.677 秒，模型等待 64.258 秒，真实 solver 11 次，查询投影 15 项，动作记录含缓存 22 项。诊断 {'explicit_effect_anchor_conflict': 5, 'unrelated_or_secondary_graph_pairs_deferred': 11, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `db35c1768e298148e3eb6a44a4296f1d07330c620ced2d09d7dfcf7ab2dc5155`，决定 SHA `f584eed68664646e45eb4096b618e70a2302d473d96873ef1e90ed2fe0a7f97b`。

## RQ1_868007cf433c

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-12.md#rq1_868007cf433c) · 检查明细 [Checks-79.json](Checks-79.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:222:original:1 | fallback | TP | FN | FN | FN | matched |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 报警

发现 `finding_fb4d801f76c543787f2e`，根位置 799＋248，依据 `program_support`。At fallback(), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification. 证据 E3, E6, E7, E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.718 秒，模型等待 15.747 秒，真实 solver 6 次，查询投影 6 项，动作记录含缓存 6 项。诊断 {}。

最终报告 SHA `1d5f698d63d592193fda051440f91014c4d021c69898ad8f1aa143f337e677da`，决定 SHA `6ea2f5835b8ee05527e72cef975457adc644f3ef2a27dc6571775f321ef72577`。

## RQ1_999f460049c5

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_999f460049c5) · 检查明细 [Checks-79.json](Checks-79.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:523:original:1 | Play | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |
| D2:523:original:2 | StartRoulette | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 1}。相关检查决定 {'policy_missing': 9, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.762 秒，模型等待 46.134 秒，真实 solver 11 次，查询投影 15 项，动作记录含缓存 22 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 11, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `0a52524d457aee75d0fc31d6af77cbe6b2c9a6774c5b125e07999df29a26b0ff`，决定 SHA `829b6bdd53706156c88b2477d0541f5af8f07adcd3fc511612ba0facbb020dc2`。

## RQ1_ad8d0ac6a104

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_ad8d0ac6a104) · 检查明细 [Checks-79.json](Checks-79.json) · 查询明细 [Queries-36.json](Queries-36.json) · 服务回执索引 [Requests-02.json](Requests-02.json) [Requests-03.json](Requests-03.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:90:original:1 | fallback | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5, 'policy_missing': 5}。相关检查决定 {'external_dependency': 6, 'policy_missing': 32}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.905 秒，模型等待 64.566 秒，真实 solver 24 次，查询投影 48 项，动作记录含缓存 67 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 37, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `878c4db05321d5182ec3c2a3a7fbd999ef29cd0a2eb94142a4333d0f451d4f6b`，决定 SHA `8f02b3d2da7a0d7cb5bf91ee123977b2162b0990619df6a5adffa81472a06d74`。

## RQ1_b6fc6e31e760

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_b6fc6e31e760) · 检查明细 [Checks-79.json](Checks-79.json) · 查询明细 [Queries-36.json](Queries-36.json) [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:537:original:1 | payout | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:537:original:2 | payoutSelf | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 1}。相关检查决定 {'external_dependency': 95, 'policy_missing': 13, 'applicable_role_guard': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 902.832 秒，模型等待 51.689 秒，真实 solver 105 次，查询投影 122 项，动作记录含缓存 145 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 37, 'yield_to_source_bound_semantic_review': 1, 'semantic_answer_outside_sent_scope': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `c49175821c94018476975403c3cf51bdc1bf929f71c8d928420b6a1ff27c0963`，决定 SHA `48f2eb0c9b81237a184367e5150a2fef305c6217bba67f7bffcd3b1276be684c`。

## RQ1_c60bf13e0ef3

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_c60bf13e0ef3) · 检查明细 [Checks-79.json](Checks-79.json) [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-02.json](Requests-02.json) [Requests-03.json](Requests-03.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:176:original:1 | payout | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:176:original:2 | payoutSelf | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 1}。相关检查决定 {'external_dependency': 83, 'policy_missing': 11}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 144.783 秒，模型等待 64.488 秒，真实 solver 41 次，查询投影 61 项，动作记录含缓存 189 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 93, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `44e7c777cd71f7cb5d7ec96e8729b07529ff9ca1f765a6013cd257309adbd8cc`，决定 SHA `03dc7f06edfd575729d3e68439bc5737c55e65a30cf110c70378f555fa322c30`。

## RQ1_d639862f5b71

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_d639862f5b71) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:427:original:1 | setOwner | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:427:original:2 | setExecutor | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 25, 'external_dependency': 19}。相关检查决定 {'policy_missing': 127, 'external_dependency': 9, 'holder_own_transfer': 2, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 185.213 秒，模型等待 22.368 秒，真实 solver 115 次，查询投影 143 项，动作记录含缓存 311 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 132, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `7de907f12f4161b5835837cd0b52b5f9951031dabdebdbe0eed5f8e14264c33f`，决定 SHA `263603ff94a23b9c10153fa0deb83cb481d02fd708e0b9b187e6f6b35d61fe7d`。

## RQ1_e6f04047bff4

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_e6f04047bff4) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:37:original:1 | RegisterDevice | TP | TP | TP | TP | matched |
| D2:37:original:2 | CollectMoney | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_f274c51e1056d85b7a7d`，根位置 249＋23，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 249 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E16

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.929 秒，模型等待 48.252 秒，真实 solver 20 次，查询投影 21 项，动作记录含缓存 18 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `62c9b53003e32099008ae46b89355ee502ca03aa875cb4ac56cff25b94d8c74f`，决定 SHA `ec7e83eadb2996c3ca07fcbecc1b1a1d4d84f1ecc7b276c52a1f479d61be6ceb`。

## RQ1_29c15f926dbe

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_29c15f926dbe) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:242:original:1 | owned | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_e4dea61c1fc823014db2`，根位置 766＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 766 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E28

发现 `finding_d1773389a2915c957cf8`，根位置 766＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 766 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E32

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.865 秒，模型等待 24.476 秒，真实 solver 57 次，查询投影 69 项，动作记录含缓存 79 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 20, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `94b7a97e3c21d0448fe1fbe1e6e80151e5d6c6ccdff3e339285625f30b5a118c`，决定 SHA `1cb1db778fa80de64b3d8cbecec48a2a06ddf7fc39b95d23d2ce367575a02921`。
