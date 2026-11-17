# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_b0475500f92c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_b0475500f92c) · 检查明细 [Checks-52.json](Checks-52.json) [Checks-53.json](Checks-53.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:423:author:1 | BCN | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 10, 'external_dependency': 4}。相关检查决定 {'policy_missing': 113, 'external_dependency': 61, 'applicable_role_guard': 1, 'self_delegation': 1, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 170.170 秒，模型等待 32.835 秒，真实 solver 86 次，查询投影 97 项，动作记录含缓存 515 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 174, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `7e232f6a41974e2405b65d3cc35fa7ada07f7ab78d0c183e49cc08a1fd7b93d6`，决定 SHA `b8677aefa34bc7fbb8aa5899b61bf7e4a2bbe69a20730f8ebae324e486aab8bd`。

## RQ1_8a6e0a083b37

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_8a6e0a083b37) · 检查明细 [Checks-53.json](Checks-53.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:424:author:1 | Owanble | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_d4e3c50a4f9050161eac`，根位置 1939＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1939 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E31

发现 `finding_802a7eef7c946af17e03`，根位置 1939＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1939 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E27

发现 `finding_2bf37e8e1ca730a47584`，根位置 1939＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1939 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E23

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.295 秒，模型等待 37.518 秒，真实 solver 27 次，查询投影 56 项，动作记录含缓存 63 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 13, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `6e487cc002365852603a4157c0d7b667fa1fb9443e5bcbd8665db754372f3deb`，决定 SHA `d59f3e6c1a87dfd0e089d568e29c9eced50eac2d53d4a600e1534fc672648d03`。

## RQ1_875ea2d05b6c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_875ea2d05b6c) · 检查明细 [Checks-53.json](Checks-53.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 7, 'external_dependency': 9}。相关检查决定 {'policy_missing': 39, 'external_dependency': 4, 'holder_own_transfer': 2, 'applicable_role_guard': 1, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 17.650 秒，模型等待 36.944 秒，真实 solver 20 次，查询投影 26 项，动作记录含缓存 100 项。诊断 {'invalid_issue_field_shape': 1, 'unrelated_or_secondary_graph_pairs_deferred': 41, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `2f9da0341c4e4e33b9ea718b683d8934f78033709a28b4179091f2b1742f5e1e`，决定 SHA `c0ef24c73ee7ca49027f02622cddfb4de07fb156b52ed83cc258bc82fb5fb674`。

## RQ1_9748dc44e052

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-08.md#rq1_9748dc44e052) · 检查明细 [Checks-53.json](Checks-53.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:426:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_2a9156aae20c69082cf2`，根位置 2226＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2226. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.871 秒，模型等待 65.688 秒，真实 solver 20 次，查询投影 26 项，动作记录含缓存 18 项。诊断 {'audit_effect_unbound': 1, 'unrelated_or_secondary_graph_pairs_deferred': 6}。

最终报告 SHA `9f1026ee84434631fd9db0da2454f82b0d0c3cc57c556716fe6719464227cc21`，决定 SHA `d512af2a3c6a631b012e626df3a35f86fed5c9c7c44e64f8c844867535cc7e8f`。

## RQ1_e27b11bddd94

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-08.md#rq1_e27b11bddd94) · 检查明细 [Checks-53.json](Checks-53.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:428:author:1 | initialize | TP | FN | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_36ea29098401e4fca7c8`，根位置 2391＋15，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2391 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

发现 `finding_8d12287a7a230372ff42`，根位置 2391＋15，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2391 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E60, E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.826 秒，模型等待 67.550 秒，真实 solver 26 次，查询投影 32 项，动作记录含缓存 64 项。诊断 {'audit_source_scope_mismatch': 1, 'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 25, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `933f85f73f09ee64aa73f61a957ade26fd92fdc37e087657e441872a45286b2e`，决定 SHA `94457b98728d08e76ec6a7cbc01e40a3650261ce11a16fca03145cd66a262ef2`。

## RQ1_e30b6086bda6

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-08.md#rq1_e30b6086bda6) · 检查明细 [Checks-53.json](Checks-53.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:429:author:1 | ActiveAdmin | FN | FN | TP | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 2}。相关检查决定 {'applicable_role_guard': 2, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.767 秒，模型等待 20.279 秒，真实 solver 2 次，查询投影 4 项，动作记录含缓存 8 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `960d0459ce89a15ab8351788a846334d139751128b3920260cf7b7bab72bb883`，决定 SHA `902218e946967c82ae1cb48d99d9a7f45dd96ed3410e0dda733dc791f28e609f`。

## RQ1_f696b703e8e8

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_f696b703e8e8) · 检查明细 [Checks-53.json](Checks-53.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 58, 'policy_missing': 1}。相关检查决定 {'policy_missing': 1, 'external_dependency': 53}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 134.058 秒，模型等待 69.509 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 120 项。诊断 {'no_locatable_source': 5, 'unrelated_or_secondary_graph_pairs_deferred': 48, 'semantic_answer_outside_sent_scope': 1}。

最终报告 SHA `1d60d92b8e86c3e509159803b846fd078c88f6193e46fd52826f860708225bd1`，决定 SHA `d8079a054ac0d973b871c31d9080262fa03621b093326bd4bfdd18afe133731f`。

## RQ1_36cdc1206b94

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_36cdc1206b94) · 检查明细 [Checks-53.json](Checks-53.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 3}。相关检查决定 {'policy_missing': 36, 'external_dependency': 34}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 47.926 秒，模型等待 49.953 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 211 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 70, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `17b1b62f71e02e17c06a527f99d74e9bc6c3127f64ccc0c33a3983b9179f6a0f`，决定 SHA `e9e2f98b37b7950e72d05c7e4fea8c0a7daebc4d2527785aacc83b894e1714d0`。

## RQ1_8fc7cb311c42

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_8fc7cb311c42) · 检查明细 [Checks-53.json](Checks-53.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:432:author:1 | SiaCashCoin | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_bae27ed197cc809b46a9`，根位置 2851＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2851 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 94.017 秒，模型等待 49.116 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'missing_claim_or_source_anchor': 3, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `bc5e9606abda490e4bcf4acde50ca67b796dcc86b92b2a5c3b948c03996ed0fb`，决定 SHA `1a9d2663478acdae5881908249820de9d94f53b3918f29971f92789561f5ca73`。

## RQ1_f59464ce08bf

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_f59464ce08bf) · 检查明细 [Checks-53.json](Checks-53.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:433:author:1 | Constructor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_67433e2a53c793b23d2b`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E64

发现 `finding_14c0eb414c3d01f53ae3`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E60

发现 `finding_e21834531da0821dc879`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E68

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 23.580 秒，模型等待 56.586 秒，真实 solver 26 次，查询投影 66 项，动作记录含缓存 113 项。诊断 {'unknown_or_unshown_effect': 1, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 40, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `4c9a3763ff8c2ae1047a094afef76065cdbc489fd3ac4262065c441305f27303`，决定 SHA `5e76885a93e7c66278df0d0dfb05e86a01756cc421b51c52b8b908a985c52088`。

## RQ1_04b8f1923370

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_04b8f1923370) · 检查明细 [Checks-53.json](Checks-53.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 11, 'external_dependency': 3}。相关检查决定 {'policy_missing': 33, 'holder_own_transfer': 4, 'self_delegation': 2, 'external_dependency': 5, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 15.631 秒，模型等待 29.490 秒，真实 solver 65 次，查询投影 84 项，动作记录含缓存 107 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 37, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `405b839767b57dfac864a8d63739da609594528386c75570751ad05fd698f6fc`，决定 SHA `ae47930e3bfaac4cebf5fbfe4711b925b12fb6749f6ba204110d65fd8ad152d4`。

## RQ1_ad46f524b21d

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_ad46f524b21d) · 检查明细 [Checks-53.json](Checks-53.json) [Checks-54.json](Checks-54.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2, 'policy_missing': 3}。相关检查决定 {'external_dependency': 325, 'policy_missing': 3, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 501.198 秒，模型等待 36.820 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 501 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 325, 'yield_to_source_bound_semantic_review': 1, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `67e58e82e3d8e22c5ecab1fb95d0fbf86614cd4263143983d184da3cb28089b5`，决定 SHA `18d7d9511b121ca67d4d2883081be83e3826bd1dc766e1670d9624c3bce5693b`。

## RQ1_e9dcb22282c1

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_e9dcb22282c1) · 检查明细 [Checks-54.json](Checks-54.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:436:author:1 | destroycontract | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 3}。相关检查决定 {'policy_missing': 2, 'external_dependency': 7, 'holder_issued_transfer_scope': 6, 'holder_own_transfer': 8, 'self_delegation': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.870 秒，模型等待 69.603 秒，真实 solver 10 次，查询投影 24 项，动作记录含缓存 28 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `972e30bb7f1ac6e326c8d375a935ad1c171d76c2f3a211bfae62ad02ab9f5d0d`，决定 SHA `3dd7db6c0a913f13a02a3d68f990a878d51c268cb24426f33ecfdca3f721e95b`。

## RQ1_b4e52ed00926

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_b4e52ed00926) · 检查明细 [Checks-54.json](Checks-54.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:437:author:1 | BIMI_0001 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_defd5535a4bea2cfc8a7`，根位置 125＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 125 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 19.997 秒，模型等待 17.063 秒，真实 solver 0 次，查询投影 1 项，动作记录含缓存 1 项。诊断 {}。

最终报告 SHA `e4dda834009c69d8f78a7745755998c5d807d4aaf7fdeb1ce1f4ad573858a80c`，决定 SHA `707db750be09fdd3d10dbff66908e5dedd6d3c3a12508cfc4a7ad75fe09197d5`。

## RQ1_9b575cb4d0e1

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_9b575cb4d0e1) · 检查明细 [Checks-54.json](Checks-54.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 20}。相关检查决定 {'external_dependency': 18}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 35.194 秒，模型等待 72.169 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 66 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 18, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `206ec92113eedb7f122705fa6874c8ad91fc19b8b40d88712ea988f20b514109`，决定 SHA `63095ba2c5611a47c9555ba3b964e22ca2e60b676d4fac14155b630b98d9f844`。

## RQ1_683cd65616eb

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_683cd65616eb) · 检查明细  · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.980 秒，模型等待 30.713 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'unknown_or_unshown_effect': 4}。

最终报告 SHA `8efef48b4c41bd43e20cdfdd087683fcb622e398880e1fc55cdfec4206e3a13d`，决定 SHA `fac0781a426b5c9f6764b6d85ca8294d65eeaf24d2612cfe134056e118c041b2`。

## RQ1_9b691a13cbe7

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_9b691a13cbe7) · 检查明细 [Checks-54.json](Checks-54.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 3}。相关检查决定 {'external_dependency': 116, 'policy_missing': 13}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 426.110 秒，模型等待 49.287 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 260 项。诊断 {'unknown_or_unshown_effect': 2, 'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 128, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `71a26fc86d53f9df1fac93920c93350e7629d6f5bccf79a93218245613a0856f`，决定 SHA `cf4dc4625bcbf2cb9f53cd6a55af6d7e6fd5985e9f307377aae10cfa133f4de3`。

## RQ1_43204b7311ce

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_43204b7311ce) · 检查明细 [Checks-54.json](Checks-54.json) [Checks-55.json](Checks-55.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 41, 'policy_missing': 2}。相关检查决定 {'external_dependency': 193, 'scope_missing': 1, 'policy_missing': 7}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 700.940 秒，模型等待 52.277 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 484 项。诊断 {'yield_to_source_bound_semantic_review': 1, 'unrelated_or_secondary_graph_pairs_deferred': 192}。

最终报告 SHA `a6a0d0724fd0b93a7961ac7633618e7ed7090aa7d50bf469cb0d20987d092df3`，决定 SHA `b1a96c5f354178e51aaa25bf1a1409462dc7199198e166b847fc72db9d162d02`。

## RQ1_1d05ec2e6d83

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-09.md#rq1_1d05ec2e6d83) · 检查明细 [Checks-55.json](Checks-55.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:442:author:1 | MADToken | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_7d6c673519a35544953c`，根位置 2571＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2571 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E65

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.688 秒，模型等待 38.378 秒，真实 solver 44 次，查询投影 47 项，动作记录含缓存 50 项。诊断 {'unbound_or_inapplicable_seed': 1, 'audit_card_issue_kind': 1, 'unrelated_or_secondary_graph_pairs_deferred': 18, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `3826828ec6b74baad817e8f0717f69af3d68990c5c88e02d9e7f81cd19aa9dc6`，决定 SHA `5720a82eb16056da069930c402ab15aef8c93d25701e9da08d0862b452978b16`。

## RQ1_0a67a2a6aa84

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_0a67a2a6aa84) · 检查明细 [Checks-55.json](Checks-55.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:443:author:1 | GEXGLOBEXTOKEN | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'policy_missing': 36, 'external_dependency': 26, 'applicable_role_guard': 1, 'holder_own_transfer': 2, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 24.913 秒，模型等待 41.285 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 152 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 61, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `2539b0a42e0c2fecace8d79a631417ff56d04b890a2ef42b79e5b1987b823887`，决定 SHA `3c40eb7d376d1c83ed108c255f4b4394c3cf3ae63e4262884457dc777ddd8ce9`。

## RQ1_4280173fabd7

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-09.md#rq1_4280173fabd7) · 检查明细 [Checks-55.json](Checks-55.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:444:author:1 | owned | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_f399446b045e6dca1de2`，根位置 99＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E221, E51

发现 `finding_e9a3ceeece57d69bd037`，根位置 99＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E169, E50

发现 `finding_f43c8c8bba03f439fa33`，根位置 99＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E232, E53

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 195.064 秒，模型等待 36.641 秒，真实 solver 79 次，查询投影 141 项，动作记录含缓存 343 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 111, 'semantic_answer_outside_sent_scope': 1}。

最终报告 SHA `11f834403004cf7d9ec449687b84813eb601f27ed3a6535bc066a022e70fe9c5`，决定 SHA `cbc62c40f440a3393c25b563f1bc70f48fe480bcff36d9e202a476147c0e9528`。

## RQ1_447aa12a3c06

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_447aa12a3c06) · 检查明细 [Checks-55.json](Checks-55.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 12, 'external_dependency': 4}。相关检查决定 {'policy_missing': 36, 'external_dependency': 6, 'applicable_role_guard': 1, 'holder_own_transfer': 1, 'self_delegation': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 15.205 秒，模型等待 78.798 秒，真实 solver 66 次，查询投影 84 项，动作记录含缓存 117 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 41, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `3912c7a6fa17204df234bc19764713dc5459b715e20f2a5f7777c9f32a14ead6`，决定 SHA `2bde903dbb5c77b0061373df6209794bef109ef0fd733daebc46fe775e33f84f`。

## RQ1_14285ee7645a

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-09.md#rq1_14285ee7645a) · 检查明细 [Checks-55.json](Checks-55.json) · 查询明细 [Queries-26.json](Queries-26.json) [Queries-27.json](Queries-27.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5, 'policy_missing': 3}。相关检查决定 {'external_dependency': 14, 'policy_missing': 5, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.521 秒，模型等待 34.154 秒，真实 solver 16 次，查询投影 35 项，动作记录含缓存 67 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 16, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `48f169904c2f20eb5e6e525d4ff7013525888ffee2f4db02affe6e9b2a92e81a`，决定 SHA `ec6e03ede69189503140215464b6af6ed743bf168b1bb66389a71d74e8131c00`。

## RQ1_0e842b26f8af

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-09.md#rq1_0e842b26f8af) · 检查明细 [Checks-55.json](Checks-55.json) · 查询明细 [Queries-27.json](Queries-27.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:447:author:1 | Constructor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_6d84cfdb5a63b56c21b3`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E50

发现 `finding_8f574f915cad20d27ba9`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E54

发现 `finding_e66623f33be78e8bb5f3`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E58

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.297 秒，模型等待 49.223 秒，真实 solver 26 次，查询投影 66 项，动作记录含缓存 93 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 30, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5ba49ab2d97a976cba2843ca275698323ace8490661aaba27f9dfe1961c11b3a`，决定 SHA `f46f753722423dfda6df0d6a620f601c281e91416cd6b009d708be13afab28a7`。
