# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_7d975f328c51

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-09.md#rq1_7d975f328c51) · 检查明细 [Checks-60.json](Checks-60.json) [Checks-61.json](Checks-61.json) · 查询明细 [Queries-28.json](Queries-28.json) [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:473:author:1 | ownable | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_c0f4741d1ce51767d4fc`，根位置 189＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 189 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E331

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 302.258 秒，模型等待 40.700 秒，真实 solver 165 次，查询投影 257 项，动作记录含缓存 751 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 323, 'noncached_action_limit': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5fd4bf6486fb6f8939640203c8cb9a11ff93e69d44d6425e98a9dd12c43dae45`，决定 SHA `beeeceefd8eca3d0c0c58c73aed257671dae5dc15a8f4db845ff142bd87427a1`。

## RQ1_1799f2b23115

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_1799f2b23115) · 检查明细 [Checks-61.json](Checks-61.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 2}。相关检查决定 {'policy_missing': 25, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 62.576 秒，模型等待 25.716 秒，真实 solver 5 次，查询投影 6 项，动作记录含缓存 70 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 27, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `b616515b606b902390fb16abddc4fcaafd7d1b60b29e5313cf9b8ab6ad64a6e4`，决定 SHA `d6d6c04d91dbb429df1bfee254c22b9f6ff8b4067f4c39e1f4772a7390d7d99e`。

## RQ1_3d23e9eaff40

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-09.md#rq1_3d23e9eaff40) · 检查明细 [Checks-61.json](Checks-61.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:475:author:1 | isOwner | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_14fc8ab369d4fe113377`，根位置 189＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 189 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E43, E6

发现 `finding_260ece08d9f224326bdd`，根位置 189＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 189 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E65, E7

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 28.849 秒，模型等待 42.352 秒，真实 solver 21 次，查询投影 32 项，动作记录含缓存 79 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 29, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c700456d978cfffd87c405f009cbbe95ed30b24fa8abfcac70156e2b824e2d27`，决定 SHA `02a300de8873e320ff814da3e571e11850dfc4f3dcea882dce23162330280206`。

## RQ1_58c19182bf25

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-09.md#rq1_58c19182bf25) · 检查明细 [Checks-61.json](Checks-61.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:476:author:1 | transferOwnership | FN | TP | TP | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 10, 'external_dependency': 2}。相关检查决定 {'policy_missing': 29, 'holder_own_transfer': 2, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 308.625 秒，模型等待 32.402 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 85 项。诊断 {'explicit_effect_anchor_conflict': 2, 'unrelated_or_secondary_graph_pairs_deferred': 28, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `60f81e37a8676257c45b093eaaa2cf624cca187627a0c9467a21526f832e150d`，决定 SHA `0a826bb692bda0e618bb1ccd565136db0a1abddcfd0052351a7bbf3f5f56f896`。

## RQ1_80810708faca

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-09.md#rq1_80810708faca) · 检查明细 [Checks-61.json](Checks-61.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:477:author:1 | TimeDeposit | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_9e922d2483c359c106d8`，根位置 87＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 87. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.416 秒，模型等待 24.342 秒，真实 solver 7 次，查询投影 7 项，动作记录含缓存 5 项。诊断 {'explicit_effect_anchor_conflict': 3, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `18c71bbd666175968842a6a7ed897b65ce48f0ad9160b95864ef910c6d4872f6`，决定 SHA `9c20901efcedae13f0125aee8ed2b53d25ff655a7333c3006aebe8a18e82ee54`。

## RQ1_f09f7b47307f

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_f09f7b47307f) · 检查明细 [Checks-61.json](Checks-61.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:478:author:1 | cmctcybermovie | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'external_dependency': 26, 'policy_missing': 34, 'self_delegation': 1, 'holder_own_transfer': 2, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 25.047 秒，模型等待 48.650 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `268da1ccd34a5386574674bf40fdc883418714258dc9e7f08112ea0adb3882f3`，决定 SHA `0952baf017088cd89606b1c2832f631a064c3502313798c8087f6fbf8ea2e3ef`。

## RQ1_7dd1efe175e6

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_7dd1efe175e6) · 检查明细 [Checks-61.json](Checks-61.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 6, 'external_dependency': 3}。相关检查决定 {'policy_missing': 28, 'external_dependency': 95, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 375.982 秒，模型等待 38.002 秒，真实 solver 40 次，查询投影 52 项，动作记录含缓存 435 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 123, 'yield_to_source_bound_semantic_review': 1, 'semantic_meaning_or_explanation_polarity_unresolved': 1}。

最终报告 SHA `cf68fb26871d5ac136eb6133ba250727ad5acd87e812c15417423f347f62c9ca`，决定 SHA `6fc16faff011aaffeab3366b5203b4930a54c4124157d230ce7d8237d315975d`。

## RQ1_8efe2f574918

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_8efe2f574918) · 检查明细 [Checks-61.json](Checks-61.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 11, 'external_dependency': 15}。相关检查决定 {'applicable_role_guard': 1, 'policy_missing': 23, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 42.009 秒，模型等待 26.626 秒，真实 solver 72 次，查询投影 72 项，动作记录含缓存 87 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 23}。

最终报告 SHA `c5d56c0ce4b76ad3a1f5055c4474383f3b414864af08de0a71136290baa42c73`，决定 SHA `725210e826d24e3f36ea33f61067743f928cde1413d93e40402cb0ccc59aff5c`。

## RQ1_0d09697e5979

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_0d09697e5979) · 检查明细 [Checks-61.json](Checks-61.json) [Checks-62.json](Checks-62.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:481:S1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:481:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:481:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:481:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 5}。相关检查决定 {'policy_missing': 21, 'external_dependency': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.709 秒，模型等待 58.189 秒，真实 solver 78 次，查询投影 132 项，动作记录含缓存 52 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 19, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `8d0e02aa6e592309a19af2a671ceeea4e467f008695b6be72c2a0cf707583ed6`，决定 SHA `61a273b52deb9bb830c47c4d1c7f9f3537e63026f84d68301f56d18737b055e9`。

## RQ1_36b63b5f9831

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_36b63b5f9831) · 检查明细 [Checks-62.json](Checks-62.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1, 'policy_missing': 1}。相关检查决定 {'scoped_semantic_normal': 1, 'policy_missing': 1, 'external_dependency': 16}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.419 秒，模型等待 81.607 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 37 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 16, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `99016863effa75abaf67dbf98e77920068f09d10fe6e288207e79641b710bc0c`，决定 SHA `5d441426275c8b768f6190c36c635b9ba15ce2b011ac381dc83132b91bf1c4d0`。

## RQ1_4b9105923111

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_4b9105923111) · 检查明细 [Checks-62.json](Checks-62.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:483:author:1 | DESALSale | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_c4f8604c941996522339`，根位置 6051＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 6051 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E110, E21

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 225.156 秒，模型等待 72.057 秒，真实 solver 74 次，查询投影 99 项，动作记录含缓存 113 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 38, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `9986a8a6556af345c902cfc1060013b0b0eb7fffacbdaf05cf2dafbc6e7cb02e`，决定 SHA `9c2bd2f6104cbaa0999a29b595cf569426dcc6f2765cfee7e5c95df3a6506b58`。

## RQ1_dadf1b436e9d

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-10.md#rq1_dadf1b436e9d) · 检查明细 [Checks-62.json](Checks-62.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:484:S1 | selfdestructs | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 13, 'external_dependency': 4}。相关检查决定 {'self_delegation': 2, 'policy_missing': 32, 'external_dependency': 6, 'holder_own_transfer': 4, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.267 秒，模型等待 64.672 秒，真实 solver 72 次，查询投影 91 项，动作记录含缓存 111 项。诊断 {'explicit_effect_anchor_conflict': 4, 'unrelated_or_secondary_graph_pairs_deferred': 35, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `b961a2936244a1add2d8e2e1991a37e1f99c26b98dc6f268540d27b0b1270c58`，决定 SHA `b4d629dc7d4cba338248c3f0a3b300760b76bc467425c2afd6119aca86950426`。

## RQ1_240411a61f54

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_240411a61f54) · 检查明细 [Checks-62.json](Checks-62.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 5}。相关检查决定 {'external_dependency': 49, 'policy_missing': 26, 'holder_issued_transfer_scope': 3, 'self_delegation': 1, 'holder_own_transfer': 2, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 43.521 秒，模型等待 58.032 秒，真实 solver 25 次，查询投影 39 项，动作记录含缓存 278 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 75, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `3a4f3c472886bec29c1e9901e95d9fa9eb2a4e7ef78355c676f076eb9ce5850c`，决定 SHA `3a9821d2d354290e59ac8299a8dbb52976cb9a49f2d1e633e033a69ddde5d5d8`。

## RQ1_409f227124c6

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_409f227124c6) · 检查明细 [Checks-62.json](Checks-62.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:486:author:1 | HT | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'policy_missing': 34, 'external_dependency': 26, 'applicable_role_guard': 1, 'holder_own_transfer': 2, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 24.928 秒，模型等待 40.175 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `437f0ce7e19aae74df06a34f0101bd2dc50de6457f5682b4ebeb05cf6ecf8c47`，决定 SHA `ce758921cd3061346c004b49fcc37210b9e2ca7871313ef0459974179ad6ff6c`。

## RQ1_a4bb8d18e79b

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_a4bb8d18e79b) · 检查明细 [Checks-62.json](Checks-62.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 3}。相关检查决定 {'policy_missing': 19}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.823 秒，模型等待 33.379 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 44 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 19}。

最终报告 SHA `923bda1062770b710d78a6a59fee8c09856062af54f06b97163db0d326e4e2bd`，决定 SHA `69a475edfbcc69c65a4e178f0dbdd13b3bcad222f5c498f7b2e25bb121db77f3`。

## RQ1_1d0b6a82d011

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_1d0b6a82d011) · 检查明细 [Checks-62.json](Checks-62.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:488:author:1 | testhash | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_2a03c9ce9ee50a36e603`，根位置 3058＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 3058 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 121.210 秒，模型等待 33.469 秒，真实 solver 82 次，查询投影 97 项，动作记录含缓存 444 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 151, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `184f60f7f99f0804d97eb730e474ce59a284d629ec4e92a694db211337bc836b`，决定 SHA `04f59c99f1a34e3d6140b38b645b73df8c5d668d4d42168aebe3a1ff91e445c2`。

## RQ1_b589500e83ab

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_b589500e83ab) · 检查明细 [Checks-62.json](Checks-62.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:489:author:1 | ChangeOwner | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_d594d68d593def1ebb3c`，根位置 1390＋17，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1390 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.245 秒，模型等待 65.619 秒，真实 solver 27 次，查询投影 28 项，动作记录含缓存 32 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 8, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `a40effbfd112259ece36adebc81d22c6c24d742e82635c95b5c11cffa9c61245`，决定 SHA `ae939c5b83b8453fb17648d83aa66d5ad4a67c48b53af7031f7eedf1231ebb27`。

## RQ1_f91e2b168fdf

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_f91e2b168fdf) · 检查明细 [Checks-62.json](Checks-62.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:490:author:1 | Rasthen | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'policy_missing': 34, 'external_dependency': 26, 'self_delegation': 1, 'applicable_role_guard': 1, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 24.343 秒，模型等待 47.574 秒，真实 solver 60 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60}。

最终报告 SHA `a338dfea5188b5316bad7a0b5711a4c652c28caae16839cd3e89aacc947d0408`，决定 SHA `4bcc7bdf3a25b96e26cef9b687ad1a12163bbbe193d1b6aedd295320eb878a9f`。

## RQ1_b0b75749d918

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_b0b75749d918) · 检查明细 [Checks-62.json](Checks-62.json) [Checks-63.json](Checks-63.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:491:author:1 | close_bank | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 5, 'external_dependency': 1}。相关检查决定 {'policy_missing': 17, 'external_dependency': 16}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.695 秒，模型等待 68.471 秒，真实 solver 24 次，查询投影 24 项，动作记录含缓存 55 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 31, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `8e15a37a6f0569138973a1cb7beef77a2eb2ddb519f083344bdc66e8e8fc0bb0`，决定 SHA `da906e4ff9013759200975d14488c37b67fe66bab7433eb71e9d66233b971865`。

## RQ1_3f952af67006

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_3f952af67006) · 检查明细 [Checks-63.json](Checks-63.json) [Checks-64.json](Checks-64.json) [Checks-65.json](Checks-65.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 8, 'policy_missing': 9}。相关检查决定 {'policy_missing': 485, 'external_dependency': 782}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 1031.160 秒，模型等待 52.348 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 13 项。诊断 {'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `2e5c5f76867fb3ad681cbd6b9b8c31337f88c44eb2b19e7af6e7f7a68550b21f`，决定 SHA `708cef2a75d7c10df0e27137bcfa144ba99ff4b2cfb51cff3e8815ddd377da16`。

## RQ1_72646c925fa6

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_72646c925fa6) · 检查明细 [Checks-65.json](Checks-65.json) [Checks-66.json](Checks-66.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 8, 'policy_missing': 17}。相关检查决定 {'scope_missing': 1, 'policy_missing': 40, 'external_dependency': 411, 'holder_own_transfer': 8, 'applicable_role_guard': 6, 'holder_issued_transfer_scope': 6, 'self_delegation': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 944.973 秒，模型等待 49.782 秒，真实 solver 2 次，查询投影 10 项，动作记录含缓存 374 项。诊断 {'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'unrelated_or_secondary_graph_pairs_deferred': 330, 'program_investigation_seconds': 1}。

最终报告 SHA `819ab7d606008b7328182ebbbd46a87822c5abb62f86e2389a370fd0b2cf8472`，决定 SHA `ce7d70a85ebb430d60cc83dc9b0833ad41fa502c00b2495a01eb624f935d3db2`。

## RQ1_283c96463274

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_283c96463274) · 检查明细 [Checks-66.json](Checks-66.json) · 查询明细 [Queries-29.json](Queries-29.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 6, 'external_dependency': 2}。相关检查决定 {'policy_missing': 51, 'external_dependency': 8}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 24.199 秒，模型等待 44.588 秒，真实 solver 4 次，查询投影 4 项，动作记录含缓存 128 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 57, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `bde60be0a5a5a013e22e8d463bbbde90e6cdf635f9d2b41e26c83aabfe30cf30`，决定 SHA `d122131c6a10a12b28b825aa9b414c53fc546cd5b146de0f2feab068937fd9fc`。

## RQ1_5181a8367a1c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_5181a8367a1c) · 检查明细 [Checks-66.json](Checks-66.json) · 查询明细 [Queries-29.json](Queries-29.json) [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:495:S1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:495:S2 | SetReleaseDate | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:495:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:495:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2, 'policy_missing': 6}。相关检查决定 {'external_dependency': 2, 'policy_missing': 16, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.377 秒，模型等待 62.163 秒，真实 solver 59 次，查询投影 91 项，动作记录含缓存 41 项。诊断 {'invalid_semantic_row': 1, 'audit_source_scope_mismatch': 1, 'duplicate_existing_issue': 1, 'unrelated_or_secondary_graph_pairs_deferred': 16, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `0ae63c6b952a7269c1c01d4d75b31073456c2e91a63085022e06ebb3eb89e3d3`，决定 SHA `85b5c882afe795a45e7d524c06da2ab3404501d4fe58d3f4f956614aa10c50b6`。

## RQ1_ce63e7a98231

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_ce63e7a98231) · 检查明细 [Checks-66.json](Checks-66.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:496:author:1 | owned | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_cc84270c3e46bac0fb87`，根位置 313＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 313 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E25

发现 `finding_511a678ced6911092785`，根位置 313＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 313 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E21

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.873 秒，模型等待 40.529 秒，真实 solver 15 次，查询投影 44 项，动作记录含缓存 50 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 12, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `8b4c4e54088ec78ebdfd7ba54a7eb32af9f262504df551420097685b184ad428`，决定 SHA `5ec75d0577b22c05ee96bb4fc939687990a125bcb1ff465467d32d8ac774f942`。
