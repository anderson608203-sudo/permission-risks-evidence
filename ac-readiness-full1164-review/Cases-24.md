# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_bc14311821a2

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-11.md#rq1_bc14311821a2) · 检查明细 [Checks-73.json](Checks-73.json) · 查询明细 [Queries-33.json](Queries-33.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:571:S1 | selfdestructs | FN | FN | TP | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 14, 'external_dependency': 4}。相关检查决定 {'policy_missing': 33, 'holder_own_transfer': 4, 'external_dependency': 6, 'self_delegation': 2, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.341 秒，模型等待 34.140 秒，真实 solver 78 次，查询投影 97 项，动作记录含缓存 113 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 36, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ffac0fb7d6d6baebaee076748318ad337107bef6868691fe820ffc6943c1b84c`，决定 SHA `cd02a18313e607c5a489e29b4259a660ad1a08198a53f35df4719caa3e2f72fc`。

## RQ1_e5e40ec6feca

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_e5e40ec6feca) · 检查明细 [Checks-73.json](Checks-73.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:572:author:1 | destroy | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1}。相关检查决定 {'source_check_excluded': 1, 'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.148 秒，模型等待 19.069 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `6e9b25755c726482082144871e5f7effbddbf1127076ccd63814e6ef24004209`，决定 SHA `d2ab3b5810cde8d8ea0cc0d96393e09668d6c125129bfd40c401792286ec763e`。

## RQ1_23d57330c344

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_23d57330c344) · 检查明细 [Checks-73.json](Checks-73.json) [Checks-74.json](Checks-74.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2}。相关检查决定 {'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.297 秒，模型等待 35.075 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `1450ec03ced46b856d12f628a4f3edaa6db3b7c56e8102cc881a4b613b973f6f`，决定 SHA `52c7fb664d78ce3d682cc68f7eb53cc58cf2f1454da6495aa8be5bf07ce952d5`。

## RQ1_7fcdff67fecb

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_7fcdff67fecb) · 检查明细 [Checks-74.json](Checks-74.json) · 查询明细 [Queries-33.json](Queries-33.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:574:S1 | initVault | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:574:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:574:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:574:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 7}。相关检查决定 {'external_dependency': 3, 'policy_missing': 18, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.036 秒，模型等待 53.546 秒，真实 solver 62 次，查询投影 93 项，动作记录含缓存 51 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 16, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `8611807336fa18dacfa69833d0b8e106285a8fd063f9e65a4c5efbc08aa66ca1`，决定 SHA `09edc3a50fb34edac03b35779ad6474640924bb031776bbad10ec8e63ef60bde`。

## RQ1_e33d037bc98d

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-11.md#rq1_e33d037bc98d) · 检查明细 [Checks-74.json](Checks-74.json) · 查询明细 [Queries-33.json](Queries-33.json) [Queries-34.json](Queries-34.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 6, 'external_dependency': 3}。相关检查决定 {'policy_missing': 11, 'holder_own_transfer': 2, 'external_dependency': 10, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.145 秒，模型等待 24.200 秒，真实 solver 21 次，查询投影 32 项，动作记录含缓存 62 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 18, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `717ce60835604b14b939695e6b165a04506027d17fced716b0f80f59a0695c5f`，决定 SHA `36a614bcdcf89f97f8a3d2cf0293b6a95f71c9318802199d2f86b37746a118d0`。

## RQ1_de08a43a1826

任务 AC，评价类别 AC。当前未知，BG 技术失败。

[实际输入](InputSource-11.md#rq1_de08a43a1826) · 检查明细 [Checks-74.json](Checks-74.json) · 查询明细 [Queries-34.json](Queries-34.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 48, 'policy_missing': 15}。相关检查决定 {'external_dependency': 13, 'policy_missing': 146, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 113.185 秒，模型等待 36.058 秒，真实 solver 226 次，查询投影 462 项，动作记录含缓存 233 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 114, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `a1449dfdb5aaf7e0f55f58028995d310c496ec9922a89c88905690d2a06e42f0`，决定 SHA `505badeb014478ee76765fc9eed5a862162559c9eec57288c018ccd4ac1f1b4d`。

## RQ1_3d5f2e705184

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_3d5f2e705184) · 检查明细 [Checks-74.json](Checks-74.json) · 查询明细 [Queries-34.json](Queries-34.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:577:author:1 | TokenERC20 | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 6, 'external_dependency': 3}。相关检查决定 {'policy_missing': 115, 'external_dependency': 69, 'self_delegation': 1, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 905.781 秒，模型等待 65.181 秒，真实 solver 15 次，查询投影 62 项，动作记录含缓存 411 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 183, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `4b8d17f6181640929cef27d1e1e6c90755e4c9b671441c215b207216a5a4bf07`，决定 SHA `77a90cf711bcad2c6e5f37e6efc1475d1fb3da3b21b42e0a78fdc5c02d70f88b`。

## RQ1_6be1f4b67f6f

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_6be1f4b67f6f) · 检查明细 [Checks-74.json](Checks-74.json) · 查询明细 [Queries-34.json](Queries-34.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 2}。相关检查决定 {'policy_missing': 15, 'external_dependency': 21}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 22.723 秒，模型等待 46.834 秒，真实 solver 1 次，查询投影 12 项，动作记录含缓存 127 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 21, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `bbbdbe8ba2be388d3f59b2f116f369f15f37c4a04c92d00c5d3c857846ecbd2d`，决定 SHA `9dac86eea3171c7007a60278062129428071d474428f6ee643048223a5c439fd`。

## RQ1_7c1aa3f1640a

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_7c1aa3f1640a) · 检查明细 [Checks-74.json](Checks-74.json) · 查询明细 [Queries-34.json](Queries-34.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:579:author:1 | destroycontract | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 5, 'external_dependency': 3}。相关检查决定 {'policy_missing': 13, 'self_delegation': 1, 'external_dependency': 10, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 14.209 秒，模型等待 65.179 秒，真实 solver 41 次，查询投影 56 项，动作记录含缓存 56 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 22, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `85f8664655b9b662001d505c43eb81b0a11456ff1a1de77dcabfe214939c4fe0`，决定 SHA `a903d47f1e1f6ddb46d162b72a825199691747d08ba508b66335da84328ab079`。

## RQ1_3daa3272da3f

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-11.md#rq1_3daa3272da3f) · 检查明细 [Checks-74.json](Checks-74.json) · 查询明细 [Queries-34.json](Queries-34.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:580:S1 | selfdestructs | FN | TP | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 13, 'external_dependency': 3}。相关检查决定 {'policy_missing': 30, 'self_delegation': 2, 'external_dependency': 3, 'applicable_role_guard': 1, 'holder_own_transfer': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.518 秒，模型等待 63.118 秒，真实 solver 71 次，查询投影 84 项，动作记录含缓存 97 项。诊断 {'missing_claim_or_source_anchor': 2, 'unrelated_or_secondary_graph_pairs_deferred': 30, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `348027a98ac210b698d761ed58f007852852a6e520640ef2ac359a9a50aaf961`，决定 SHA `263ac63276a4877c9ced65f1b8d27adc4c06dda530b8f0bca8eb3e545b172191`。

## RQ1_a1d129031088

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_a1d129031088) · 检查明细 [Checks-74.json](Checks-74.json) · 查询明细 [Queries-34.json](Queries-34.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5, 'policy_missing': 2}。相关检查决定 {'external_dependency': 18, 'applicable_role_guard': 1, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.448 秒，模型等待 27.653 秒，真实 solver 14 次，查询投影 26 项，动作记录含缓存 66 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 18, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `0c44664634b7d2724c81e7cbfd63e6d805e3ae4f00f9efb9bfdf5e14b693e4b0`，决定 SHA `0f77ab0d11498359d1b8be7ef2bfd7289e2a20f5e2ccbad5f896317d4d51c8d4`。

## RQ1_e052d3aaca16

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-11.md#rq1_e052d3aaca16) · 检查明细 [Checks-74.json](Checks-74.json) [Checks-75.json](Checks-75.json) · 查询明细 [Queries-34.json](Queries-34.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:582:author:1 | LUVIToken | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_5121a6825c86e0a8e61c`，根位置 2837＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2837 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 92.871 秒，模型等待 49.026 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `0deebac6a147ca9832568c1a83113f860e487c9dda9a89d646bfe3f812cc4773`，决定 SHA `a968df288eeb2ea175a63060547540e724214478caaab851017491a9ae8a6026`。

## RQ1_ee18bfc3f9fb

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_ee18bfc3f9fb) · 检查明细 [Checks-75.json](Checks-75.json) · 查询明细 [Queries-34.json](Queries-34.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 13, 'external_dependency': 6}。相关检查决定 {'external_dependency': 246, 'policy_missing': 89, 'applicable_role_guard': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 928.077 秒，模型等待 28.788 秒，真实 solver 54 次，查询投影 88 项，动作记录含缓存 461 项。诊断 {'no_locatable_source': 1, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'unrelated_or_secondary_graph_pairs_deferred': 138, 'program_investigation_seconds': 1}。

最终报告 SHA `0bcb8be85ef9668dbd43c3edb11f3717979c9780d84a721188ecec92952fa36a`，决定 SHA `486ec8153c0b52a526fb4169691558fd8a01bcfb05f9603d593d6d1e0565dd57`。

## RQ1_baecb1a287ec

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_baecb1a287ec) · 检查明细 [Checks-75.json](Checks-75.json) · 查询明细 [Queries-34.json](Queries-34.json) [Queries-35.json](Queries-35.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:584:S1 | initVault | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:584:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:584:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:584:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 5}。相关检查决定 {'policy_missing': 17, 'external_dependency': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.125 秒，模型等待 48.878 秒，真实 solver 86 次，查询投影 114 项，动作记录含缓存 43 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 14, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `d8c7f6d5a653b335a2612e2d79f4f9d5add75e59daeb10f1b0883bbe2a3da004`，决定 SHA `786e84219bc81ec1d896ed114b1de374bbd8d3dd3d0ae866059a6e0582d209fe`。

## RQ1_30b4e48b4f5c

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-11.md#rq1_30b4e48b4f5c) · 检查明细 [Checks-75.json](Checks-75.json) · 查询明细 [Queries-35.json](Queries-35.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:585:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_bd7cca5fedc6c4851e26`，根位置 2208＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2208 under financial_right. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E11

发现 `finding_f0115c63cc5d0c40568c`，根位置 2530＋531，依据 `program_support`。At transferFrom(address,address,uint256), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification. 证据 E28, E4

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.207 秒，模型等待 50.763 秒，真实 solver 26 次，查询投影 30 项，动作记录含缓存 21 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 7, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `2dc5b1d7c646cdf3f1bd1d0b5200dd1b8eee57a0c326845a0fef64b36a3076a4`，决定 SHA `5e5bcb6c73001878b19c6a6773f22e1cee7a9dc0d1deed5048b5b6903cd04564`。

## RQ1_991cdff3e261

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_991cdff3e261) · 检查明细 [Checks-75.json](Checks-75.json) · 查询明细 [Queries-35.json](Queries-35.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:586:author:1 | Legendary | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'policy_missing': 34, 'external_dependency': 26, 'holder_own_transfer': 2, 'applicable_role_guard': 1, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 25.587 秒，模型等待 46.976 秒，真实 solver 61 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'audit_source_scope_mismatch': 2, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `d01cd75618fe241ee8d3567d06f0ee2ee3cb78be8b40a7ad196a09fe75f285ca`，决定 SHA `a24b141ecc18f054dfcb57cc2e322bd8d42104e9322c5007becea65fbd33e6b2`。

## RQ1_9aafb6cd1add

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-11.md#rq1_9aafb6cd1add) · 检查明细 [Checks-75.json](Checks-75.json) [Checks-76.json](Checks-76.json) · 查询明细 [Queries-35.json](Queries-35.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:587:author:1 | Owned2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_db0bd64648c3d3308a22`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E24, E3

发现 `finding_059505c9a99c79e67209`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E25, E4

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.570 秒，模型等待 30.496 秒，真实 solver 10 次，查询投影 20 项，动作记录含缓存 24 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `2111d5eea2ced117d1a8d976351d29dfd5f591816826d7f3a80093931bb336a3`，决定 SHA `0a0822a62fb4a32b771df09b97fd9bd6d02e84e3a514ff0281d2bc7dca6d2618`。

## RQ1_fa317176bacc

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_fa317176bacc) · 检查明细 [Checks-76.json](Checks-76.json) · 查询明细 [Queries-35.json](Queries-35.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:588:S1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:588:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:588:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:588:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 7}。相关检查决定 {'policy_missing': 18, 'applicable_role_guard': 1, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.049 秒，模型等待 48.746 秒，真实 solver 65 次，查询投影 93 项，动作记录含缓存 45 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 16}。

最终报告 SHA `02e9fe090aa01cde47243673738eab5959a636a68a45509fade895af5d348c7e`，决定 SHA `595ab8223a6f203079353c31f1978c80ddfd6fb4fc23fd5285b603ca7a0ba8f8`。

## RQ1_8b881d18ff63

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-11.md#rq1_8b881d18ff63) · 检查明细 [Checks-76.json](Checks-76.json) · 查询明细 [Queries-35.json](Queries-35.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:589:author:1 | WorldSafetySecurityToken | FN | TP | TP | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 13, 'external_dependency': 4}。相关检查决定 {'policy_missing': 32, 'external_dependency': 11, 'holder_own_transfer': 4, 'self_delegation': 2, 'applicable_role_guard': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 16.883 秒，模型等待 83.789 秒，真实 solver 103 次，查询投影 117 项，动作记录含缓存 129 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 42, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `00666a2350536254f9c5e5de6690e2fa3ea2f3d8adca05a55cd53b446f9afe56`，决定 SHA `bced6a85a31f49436035da03b4bf5ace53688beceb2afe245f96f04211c66c00`。

## RQ1_6c5b867c52e3

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_6c5b867c52e3) · 检查明细 [Checks-76.json](Checks-76.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 3, 'external_dependency': 1, 'not_reviewed': 1}。相关检查决定 {'policy_missing': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.352 秒，模型等待 37.125 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 9 项。诊断 {'no_locatable_source': 2, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `48852ad7913a44966e54cb1a658f020c7aab5b61fc987516c97dbc3c57ff3f8d`，决定 SHA `28cd6ca792696dbfeb572f4f6fce4b6047e003990e7660eac2ae07f581f52f72`。

## RQ1_f3cc38f76a37

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-11.md#rq1_f3cc38f76a37) · 检查明细 [Checks-76.json](Checks-76.json) · 查询明细 [Queries-35.json](Queries-35.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:591:author:1 | OOREDOOCHAIN | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_089d2d62a1f45570d9e7`，根位置 2852＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2852 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 95.844 秒，模型等待 36.930 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'invalid_issue_field_shape': 1, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5110647b4b522f507db6824d015c3cf340052c91dcb9b82efc8fa861497d32cc`，决定 SHA `4a04e21318cc4153f806b1fd7ae35c96f4f20096536e633cdb09a64f86b3a7a4`。

## RQ1_e4dcc6d46656

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-11.md#rq1_e4dcc6d46656) · 检查明细 [Checks-76.json](Checks-76.json) · 查询明细 [Queries-35.json](Queries-35.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:592:author:1 | BITDINERO | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_c7efa65c464220f69ca4`，根位置 2854＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2854 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 95.654 秒，模型等待 41.851 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5f1f66a27095c348f64ca4aec28b544acaba2411232aba51d88fe14ed491b31c`，决定 SHA `c854ecc3416398c353e41c3f175eec050aa97ca59a5a060faed6b8776e610435`。

## RQ1_b914559c9307

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-11.md#rq1_b914559c9307) · 检查明细 [Checks-76.json](Checks-76.json) · 查询明细 [Queries-35.json](Queries-35.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:593:author:1 | Owned2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_7a935eb68a27f9c17675`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E25, E4

发现 `finding_40edbcf095c5c5e308cc`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E24, E3

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.435 秒，模型等待 33.152 秒，真实 solver 12 次，查询投影 22 项，动作记录含缓存 26 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `884ec612731dacfe57f7b9dc5ac2bb69a6fd82029cee8f91f7bbb4d02c81914c`，决定 SHA `bd0581f5ff7fb5d3f278c2ea1635f2e4d733775536b2013b68359fd2d753c8a0`。

## RQ1_50afc53073f9

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_50afc53073f9) · 检查明细 [Checks-76.json](Checks-76.json) · 查询明细 [Queries-35.json](Queries-35.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:594:author:1 | initialWittness | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3, 'policy_missing': 2}。相关检查决定 {'external_dependency': 46, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 49.040 秒，模型等待 53.670 秒，真实 solver 4 次，查询投影 6 项，动作记录含缓存 164 项。诊断 {'unknown_or_unshown_effect': 3, 'unrelated_or_secondary_graph_pairs_deferred': 48, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `f706616001fa03ed09dd6e4021e0285af6a645c64d46147dcd0c3d03c3293285`，决定 SHA `35de528121ec84b798f66fa2754dc7be3ee7f838fb3e5a078407c12177e45a96`。
