# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_0473d5d2e0f2

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_0473d5d2e0f2) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 5}。相关检查决定 {'policy_missing': 6, 'external_dependency': 14, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.794 秒，模型等待 105.128 秒，真实 solver 6 次，查询投影 6 项，动作记录含缓存 58 项。诊断 {'no_locatable_source': 5, 'unrelated_or_secondary_graph_pairs_deferred': 17, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `204359d0481b37be6793ea3631e796a059c39fa60ac7d69c615101dad8ccff43`，决定 SHA `c9d2aa1f4b5abd7fb7fb338c8236a778fb297d192b29532b301af59e1c51109b`。

## RQ1_1e1d79252190

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_1e1d79252190) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:375:author:1 | owned | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_46f8259391dea93c5db9`，根位置 181＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 181 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E65

发现 `finding_31f7de1cf0e909987124`，根位置 181＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 181 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E69

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 47.291 秒，模型等待 66.054 秒，真实 solver 155 次，查询投影 209 项，动作记录含缓存 138 项。诊断 {'audit_card_text': 1, 'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 49, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ff152f1ef8edc1f4ee40eed79e9b7cd69048d86788a2d753354adf8903a609f9`，决定 SHA `459af4fc513e8e19efb15ca1ad57593df70b55e9ad05eb127096cb77c57d0c10`。

## RQ1_f4b9019ad4d0

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_f4b9019ad4d0) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-21.json](Queries-21.json) [Queries-22.json](Queries-22.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:376:author:1 | owned | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_d9d889e07f19ba2f02d4`，根位置 490＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 490 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.170 秒，模型等待 40.558 秒，真实 solver 17 次，查询投影 22 项，动作记录含缓存 16 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 5}。

最终报告 SHA `c9fa36bba743e39e79dd91183dbfcdcca5984c1a1b303ada733f72062b318d64`，决定 SHA `3aefc0dff655031bdf665eba4a24d9487b28a2a3d460cddf7aaf7931de4f3925`。

## RQ1_697a8658398b

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_697a8658398b) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-22.json](Queries-22.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:377:author:1 | initialize | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 7, 'external_dependency': 1}。相关检查决定 {'policy_missing': 19, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.395 秒，模型等待 41.802 秒，真实 solver 8 次，查询投影 25 项，动作记录含缓存 49 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 15, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `700a83c751b9921e302d037bd54029315bd3e488771f0a7bb89ea13a441dbf15`，决定 SHA `0424cb6a5074d315c59d64f2fd26f708539a8d38c69b80ea5f71b47bef341a67`。

## RQ1_9f7d2c8c83fd

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_9f7d2c8c83fd) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-22.json](Queries-22.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:378:author:1 | initialize | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'applicable_role_guard': 2, 'external_dependency': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.217 秒，模型等待 81.702 秒，真实 solver 1 次，查询投影 6 项，动作记录含缓存 9 项。诊断 {'explicit_effect_anchor_conflict': 3, 'unrelated_or_secondary_graph_pairs_deferred': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `dc3a35c6babcd1b38e6e0d5d511e70f3cacc2e62d7b5ea592db4d619119d14b3`，决定 SHA `fb7ca9a372182939388cc9ef79d8f90fdc1e62bdaa94ae11a13f5781e0388853`。

## RQ1_8f7326a4a6da

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-07.md#rq1_8f7326a4a6da) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-22.json](Queries-22.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:379:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_1aeced13fcf25331d1c3`，根位置 2226＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2226. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E7

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.284 秒，模型等待 49.860 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 13 项。诊断 {'audit_source_scope_mismatch': 1, 'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 5}。

最终报告 SHA `ff0ccc4b6edb863def58cf81d4bbb3915da6186648300bf1e00466d0f4cc1caa`，决定 SHA `8fca58381577a339a0a0855a1d8b73d8066d0631503d8ced7a28f507abc1c777`。

## RQ1_7f95ecbe6bad

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_7f95ecbe6bad) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-22.json](Queries-22.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:380:author:1 | SiaCashCoin | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_0be168384a2639e57ad3`，根位置 2839＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2839 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 91.511 秒，模型等待 51.173 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ca3c77b279064fca113c05c9fe5536088f26781f7998bee0b29d79f831d205d1`，决定 SHA `c46d2ba4736877856209f61eebae7c718dc6bb63caeaac3ed74b2d7deec4381b`。

## RQ1_b2a2fc36e6b8

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_b2a2fc36e6b8) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-22.json](Queries-22.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 6, 'external_dependency': 2}。相关检查决定 {'policy_missing': 13, 'external_dependency': 7}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.776 秒，模型等待 41.116 秒，真实 solver 19 次，查询投影 30 项，动作记录含缓存 55 项。诊断 {'invalid_issue_field_shape': 1, 'unrelated_or_secondary_graph_pairs_deferred': 20, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `71eb104b9bd34918ef14aca4afc4a31a44153e81ac5986bf60ef58341318201c`，决定 SHA `87fda432fb966338240ed337e57edca4f7dd1c4ea91ed1d164e107e6d2373060`。

## RQ1_6de2b3e5e82f

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_6de2b3e5e82f) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-22.json](Queries-22.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:382:author:1 | end | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 11, 'external_dependency': 1}。相关检查决定 {'external_dependency': 3, 'policy_missing': 25, 'holder_own_transfer': 6, 'self_delegation': 2, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.917 秒，模型等待 55.014 秒，真实 solver 62 次，查询投影 63 项，动作记录含缓存 73 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 26, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `eba9e44a54d2b2aa9fafb1cc665ac941321a3d7a28fd3be955b9f04b389a6fb3`，决定 SHA `04b2460709558bdc291a8df37f13c6fc30919af36672c29cb20cfc4b22525342`。

## RQ1_015eadbd72b7

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_015eadbd72b7) · 检查明细 [Checks-48.json](Checks-48.json) [Checks-49.json](Checks-49.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 6}。相关检查决定 {'external_dependency': 90, 'policy_missing': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 68.799 秒，模型等待 106.062 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 153 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 93, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `21ab447a7909b2eb6af2c9c1529b4d5649a93589b6b38c2be861da95bafd07e1`，决定 SHA `3672ebd7a18c13f633670ada626a99b6918ef23f1dc92387d71760d8ab1a22f5`。

## RQ1_004d04aafe56

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_004d04aafe56) · 检查明细 [Checks-49.json](Checks-49.json) · 查询明细 [Queries-22.json](Queries-22.json) [Queries-23.json](Queries-23.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 4}。相关检查决定 {'policy_missing': 14, 'external_dependency': 90}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 571.725 秒，模型等待 39.851 秒，真实 solver 1236 次，查询投影 1252 项，动作记录含缓存 312 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 103, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `bf6a184d5780287a3ff1c57d018dc3df06e4927a43e3bceff6019616927f8355`，决定 SHA `b32800c4e7ce86c869bde4d17175540322817e65979357b56d5b9f6967f8614d`。

## RQ1_04b90a3b2853

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_04b90a3b2853) · 检查明细 [Checks-49.json](Checks-49.json) · 查询明细 [Queries-23.json](Queries-23.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 10, 'policy_missing': 3}。相关检查决定 {'external_dependency': 70, 'policy_missing': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 274.012 秒，模型等待 62.566 秒，真实 solver 12 次，查询投影 52 项，动作记录含缓存 224 项。诊断 {'missing_claim_or_source_anchor': 1, 'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 65, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `8b3f01be387124ca30481fc234ec18f3d741e50ecb0162437f6ca5d2a831960f`，决定 SHA `11b5fa27388774c3b52ef9c67cf4998fed6c03252b9377646ab6827485004ab7`。

## RQ1_6fa43914a4bd

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_6fa43914a4bd) · 检查明细 [Checks-49.json](Checks-49.json) · 查询明细 [Queries-23.json](Queries-23.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:386:author:1 | owned | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_b5e9264c0d0a95a15968`，根位置 121＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 121 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E45

发现 `finding_3960b77b06abd42f4399`，根位置 121＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 121 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E41

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 446.475 秒，模型等待 42.901 秒，真实 solver 22 次，查询投影 33 项，动作记录含缓存 86 项。诊断 {'unknown_or_unshown_effect': 3, 'unrelated_or_secondary_graph_pairs_deferred': 34, 'yield_to_source_bound_semantic_review': 1, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `fc569a3c9e58bf4a66fad8766d9bc10f5e4cd6f3a670549b615656cda6b38cbc`，决定 SHA `4fd97d99d4fb48b6ec4c588a72a7ef35d5bd5b892683970b9a39a07a9699f9e3`。

## RQ1_67c41965bdb2

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_67c41965bdb2) · 检查明细 [Checks-49.json](Checks-49.json) · 查询明细 [Queries-23.json](Queries-23.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:387:author:1 | setAllowedAddress | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_f2eb20ee8d5a8aa319b8`，根位置 1077＋20，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1077 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E22

发现 `finding_16b9dd67893ea4546797`，根位置 1077＋20，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1077 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E26

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.882 秒，模型等待 31.076 秒，真实 solver 31 次，查询投影 34 项，动作记录含缓存 26 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 4, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `8dafcb61d66f146f470f0d603d5db14555b53154a73c51e764f83bc797bf95b9`，决定 SHA `c844bd241fd5f11ad6fd6d20ec1bfe9011b9dbd251aa73e99e4d2725a8b7002b`。

## RQ1_0904615e5961

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-08.md#rq1_0904615e5961) · 检查明细 [Checks-49.json](Checks-49.json) · 查询明细 [Queries-23.json](Queries-23.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 7, 'policy_missing': 4}。相关检查决定 {'external_dependency': 29, 'nominee_acceptance': 6, 'policy_missing': 5, 'holder_own_transfer': 2, 'holder_issued_transfer_scope': 3, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 41.478 秒，模型等待 45.893 秒，真实 solver 67 次，查询投影 119 项，动作记录含缓存 139 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 32, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `1d79f80bc3fc0a02decbc2ceac9617f3727c46519c5a4d23576f2e348a2e795d`，决定 SHA `98ff2a05d00f0972c9b6ef36cda7af4c7f55bbe7cd7cd587fcb93a9e83978e0a`。

## RQ1_e5ab2cf90f08

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_e5ab2cf90f08) · 检查明细 [Checks-49.json](Checks-49.json) · 查询明细 [Queries-23.json](Queries-23.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:389:original:1 | Vault | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |
| D2:389:original:2 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 2}。相关检查决定 {'policy_missing': 5, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.974 秒，模型等待 62.920 秒，真实 solver 22 次，查询投影 36 项，动作记录含缓存 16 项。诊断 {'missing_claim_or_source_anchor': 2, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `85e779a7ea992af38a18c735b85839bb1597f2dada033afd5e2cd69e42551b75`，决定 SHA `5699f87f4517af383deafafe84c07a00e3ca5da17519dc60f8a371601e1a48f5`。

## RQ1_c587815dd35d

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_c587815dd35d) · 检查明细 [Checks-49.json](Checks-49.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {'external_dependency': 11}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.191 秒，模型等待 64.558 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 35 项。诊断 {'no_locatable_source': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `7c2f425b1495409644db477b1dad2c02c89c95fdb42780b106899bff981a88b5`，决定 SHA `7dba86e7366804e00e3cdc08f7c36f95acc2b7f4d59d300624cc87b79a3b1cfe`。

## RQ1_545948b8fa49

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_545948b8fa49) · 检查明细 [Checks-49.json](Checks-49.json) · 查询明细 [Queries-23.json](Queries-23.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 1}。相关检查决定 {'external_dependency': 55, 'policy_missing': 18, 'self_delegation': 2, 'holder_own_transfer': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 385.311 秒，模型等待 32.357 秒，真实 solver 41 次，查询投影 95 项，动作记录含缓存 247 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 73, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5fbbb7b4dca9dfd1e825588b28ba82c11223984178d9c2883fb1e2f1dd4f2c6d`，决定 SHA `9b1f031ef92168aecd89851134ec885c3be85d8e174d6b794f1ac1bd38c9b9cc`。

## RQ1_47d903b24246

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_47d903b24246) · 检查明细 [Checks-49.json](Checks-49.json) · 查询明细 [Queries-23.json](Queries-23.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 1}。相关检查决定 {'policy_missing': 1, 'external_dependency': 9}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.079 秒，模型等待 69.776 秒，真实 solver 9 次，查询投影 9 项，动作记录含缓存 22 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 10, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `33a9762bf9c28cb03c953ea5263fc0981a39305226902ef0b3a8c34943f921e7`，决定 SHA `ecaf883f2dcc5003822bee818250965cb6f203479e468adf697c816e22c22051`。

## RQ1_afa801e14aca

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_afa801e14aca) · 检查明细 [Checks-49.json](Checks-49.json) [Checks-50.json](Checks-50.json) · 查询明细 [Queries-23.json](Queries-23.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:393:author:1 | QMQCoin | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 10, 'external_dependency': 5}。相关检查决定 {'policy_missing': 113, 'external_dependency': 62, 'holder_own_transfer': 2, 'self_delegation': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 169.165 秒，模型等待 31.621 秒，真实 solver 80 次，查询投影 97 项，动作记录含缓存 521 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 175, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `853c2d910339688aad9eec8b7ed0e57eb21d1d0bb5d15a3b0f894d4cc8378edb`，决定 SHA `ba0c288fc086fb81e826dd8af9c3796eeae808702a81fea7b9363b66b5750548`。

## RQ1_84691b172f26

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_84691b172f26) · 检查明细 [Checks-50.json](Checks-50.json) · 查询明细 [Queries-23.json](Queries-23.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:394:author:1 | CryptoMoviesToken | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_6823edfeee7d85be6262`，根位置 1916＋23，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1916 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E82

发现 `finding_010626dd1626035c8cf4`，根位置 1945＋23，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1945 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E183, E2

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 29.741 秒，模型等待 53.289 秒，真实 solver 45 次，查询投影 49 项，动作记录含缓存 190 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 78, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `8e4fac9e7de0699dd5c70cc5d5983b8ce4ea97f7e15802862197bb0a0e6c3a69`，决定 SHA `91571c68fb8d36aef3766872185c7f51ef7ba6fec9aa2014efea8dbc46417aff`。

## RQ1_11b39eaea9ae

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-08.md#rq1_11b39eaea9ae) · 检查明细 [Checks-50.json](Checks-50.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:395:author:1 | destroy | FN | FN | TP | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'not_reviewed': 1}。相关检查决定 {'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.109 秒，模型等待 12.421 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'missing_claim_or_source_anchor': 1, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `0d9ed8d4192746c70677fd89a1aa7d4f60a2fbf9e218e42e6d7e6342c24ad84d`，决定 SHA `a912fb86df390e6e13a53130bc614916edbbb12d3553eeb184dc18409c8d8f27`。

## RQ1_cec6d28cb95d

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_cec6d28cb95d) · 检查明细 [Checks-50.json](Checks-50.json) · 查询明细 [Queries-23.json](Queries-23.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:396:author:1 | Owned2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_2287d21badd02e06d913`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E18

发现 `finding_7d3a38a045ad690f7eb2`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E24

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.382 秒，模型等待 31.653 秒，真实 solver 12 次，查询投影 22 项，动作记录含缓存 24 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `675357bc1ecf67338a7e4d69429a967ceba7ab631c64932e157f3581353473c8`，决定 SHA `71b2141cf6438d04eaa86a1920df7e8b19550793a32e1892358b6e8202b223b4`。

## RQ1_7ecffa90731f

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_7ecffa90731f) · 检查明细 [Checks-50.json](Checks-50.json) · 查询明细 [Queries-23.json](Queries-23.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:397:author:1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 24, 'policy_missing': 4}。相关检查决定 {'policy_missing': 8, 'external_dependency': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.783 秒，模型等待 25.832 秒，真实 solver 14 次，查询投影 18 项，动作记录含缓存 32 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 13, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c623b67394acd463b8a9f750998da4b3ab1665ed81d8e50c7e7daa469ab0e197`，决定 SHA `b60646b21955f6725b76d6144c4a056c7a94a60780828b0d06fa2d3cfbed4966`。
