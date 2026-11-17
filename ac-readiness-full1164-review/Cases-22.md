# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_f694e40ffba2

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-10.md#rq1_f694e40ffba2) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:521:S1 | init | TP | FN | FN | TP | matched |
| D2:521:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:521:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:521:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 报警 → report 报警

发现 `finding_6930d9b127b2fd2612ba`，根位置 811＋18，依据 `scoped_semantic_conflict`。The assessment concerns the policy governing the protected effect at source offset 811. The located duty and the deciding caller conflict at this applied source effect; this is a scoped semantic prediction. 证据 E10, E25, E49, E56

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.314 秒，模型等待 58.654 秒，真实 solver 76 次，查询投影 113 项，动作记录含缓存 46 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 16}。

最终报告 SHA `f1c3342b5faabef08032ec3f424201582babea983131ae29874f8e005597b750`，决定 SHA `7b41bd95782b621ef0b963e6c1ae2dbd9cbe2bf6bd2db3313f240b721badb776`。

## RQ1_d4aefd2e1bfc

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_d4aefd2e1bfc) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:522:author:1 | refundOwner | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {'policy_missing': 3, 'external_dependency': 10}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.235 秒，模型等待 49.642 秒，真实 solver 24 次，查询投影 24 项，动作记录含缓存 28 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 11, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `7f5f1e1d730f0c6ec68a7980654cf0aba220dbf821ea2363b675cd4745946173`，决定 SHA `0d06c605764e51e5fa21e47cb6d64efd117ea0cd5ded9b85a8b30810bf411ba4`。

## RQ1_444af83fd288

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_444af83fd288) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:524:author:1 | suicide | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 2}。相关检查决定 {'policy_missing': 10, 'external_dependency': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.603 秒，模型等待 42.025 秒，真实 solver 34 次，查询投影 43 项，动作记录含缓存 35 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 12, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `74a47c416612fa8962cd46e81beeb1deb30403fa9443b4c2573e203546171675`，决定 SHA `b0976e9d25ef9a2539a3ebf1ca488931cfa95262bfa94cc4b03bf5f2aa1690f7`。

## RQ1_6f3ba10080c4

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_6f3ba10080c4) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:525:S1 | POWHclone | FN | FN | FN | FN | no_aligned_inspection_in_obligations |
| D2:525:S2 | approve | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 12}。相关检查决定 {'external_dependency': 4, 'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 17.415 秒，模型等待 49.165 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 6 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `2f7cb4adc1279194fecc001aec8f44ca223e0ffae9eec5e4567bfa05539708cf`，决定 SHA `8b643b0cc39c494ee8d0c77f8cc1dfd0d975d2dd98db2c5e6909cfe5764ef6de`。

## RQ1_0526c008875c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_0526c008875c) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2}。相关检查决定 {'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.276 秒，模型等待 41.505 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'unparseable_top_level': 1}。

最终报告 SHA `7c1d9452bd7f60080ad14a7e8bfb906e0bc30beddada5a3e183f6422d7a83857`，决定 SHA `b23ee285d8a57f298f89fbb31d7ec7ff5b47713ee8a3b95d3e6a174a07e96ec1`。

## RQ1_528c1cef93be

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_528c1cef93be) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1}。相关检查决定 {'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.189 秒，模型等待 23.352 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'unknown_or_unshown_effect': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `3407c20d9616edba23c73f62466a8ad2f824e52fe38aeea3983b598974fb799b`，决定 SHA `eefaa2c0e28d4bf4d66d287430887cfb48179d7b3fe7750f6cf2f7398c208f61`。

## RQ1_21b38b688442

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_21b38b688442) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:528:author:1 | Constructor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_d86ce7e52b629ef8590a`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E58

发现 `finding_a292b2e93bbd2bcf866c`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E54

发现 `finding_bbfdc1c5be8d90f99234`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E50

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.235 秒，模型等待 60.062 秒，真实 solver 26 次，查询投影 66 项，动作记录含缓存 93 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 30, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `3ad4d7c26de5f036792be85a8c20329f11f55571fa5886a56e8609d207d8461a`，决定 SHA `3a41392a306e6aefc56fefbaab7f84471edcbd5f27636e128098b3fc7750ad48`。

## RQ1_e88cd683cd73

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_e88cd683cd73) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:529:author:1 | CompanyToken | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 8}。相关检查决定 {'policy_missing': 34, 'external_dependency': 26, 'self_delegation': 1, 'holder_own_transfer': 2, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 25.075 秒，模型等待 63.186 秒，真实 solver 61 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `9239f0e2a7f509683d7887a912e650c90b4b4bd935d3f6cde5c572d89245f530`，决定 SHA `13e1ebf79eb02b49ec7d1ed9c9dccf38be40d35c8fd78cf0345baf880ebe5803`。

## RQ1_e440a75a1c8a

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_e440a75a1c8a) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:530:author:1 | VTTR | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 25}。相关检查决定 {'policy_missing': 47, 'holder_own_transfer': 8, 'self_delegation': 3, 'applicable_role_guard': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 15.961 秒，模型等待 38.541 秒，真实 solver 127 次，查询投影 149 项，动作记录含缓存 145 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 46, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `932421ee3e2addf05c82c55f3d410b9262fc874906d39f50470a12100b26c796`，决定 SHA `8451dec894a104d50907a603e988e80c00a5f89e2cca4995b66dc1cf7709b2ca`。

## RQ1_f88fe59a161b

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_f88fe59a161b) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:531:author:1 | Owned2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_2f05b4baded880d37b43`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E18

发现 `finding_46c9fe8dc153cf9aed09`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E24

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.426 秒，模型等待 30.746 秒，真实 solver 11 次，查询投影 22 项，动作记录含缓存 24 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `319a57954591c787e4dce30f829d0adbb01c5c5c3fb4aefc99079049176a7d63`，决定 SHA `95d77a02b74189d0178b8ae36dc42bdee8ed7133f0b8d2fa71f17c293aae94f3`。

## RQ1_14d39ae70812

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_14d39ae70812) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 49, 'policy_missing': 2}。相关检查决定 {'external_dependency': 2, 'policy_missing': 3, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.894 秒，模型等待 30.247 秒，真实 solver 9 次，查询投影 9 项，动作记录含缓存 13 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `74aea6e2400be32c63e3a3ff3c1c4260e57e74018a74f79b96012edd22210b04`，决定 SHA `8e47821ad5cef297b696a1e38634b955e3f1fe3e567a3290c4f9c745eba9ac05`。

## RQ1_ed250fd054c9

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_ed250fd054c9) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:533:author:1 | Constructor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_7f6cd64de7151cf5e1e8`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E4, E55

发现 `finding_c9adfa5ffcf281cd8978`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E5, E59

发现 `finding_8243935a92baf87e67f7`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E6, E68

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.515 秒，模型等待 73.056 秒，真实 solver 26 次，查询投影 66 项，动作记录含缓存 88 项。诊断 {'audit_source_scope_mismatch': 2, 'no_locatable_source': 6, 'unrelated_or_secondary_graph_pairs_deferred': 28, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `041cd09945a4d0e21cea7751cba6d3afa25bbe9fa7a8c84af0425f77a6526a6b`，决定 SHA `89d6832edba923519498fb3398080fe026d6f622b762394fa89bc1f9d8c9185a`。

## RQ1_254bfee03840

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_254bfee03840) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:534:S1 | owned | TP | TP | TP | TP | matched |
| D2:534:S2 | bitexlive | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_eb1d8d74a7390b391b92`，根位置 1537＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1537 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E19

发现 `finding_43845b68c5214b236d01`，根位置 1537＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1537 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E27

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.068 秒，模型等待 36.091 秒，真实 solver 2 次，查询投影 14 项，动作记录含缓存 26 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 7, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `2271a35967f1ef555905d883828c36c712dc2b2cfcbef1d902a5db28fb0d88af`，决定 SHA `56def0513f38d1fa9c56d7f8589a16a2da5ef4a9729824cacc21f33da7efac33`。

## RQ1_4c2921d39474

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_4c2921d39474) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:535:author:1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 11, 'external_dependency': 8}。相关检查决定 {'policy_missing': 29, 'external_dependency': 16, 'nominee_acceptance': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.927 秒，模型等待 49.284 秒，真实 solver 116 次，查询投影 143 项，动作记录含缓存 111 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 39, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `3e041ed39cb61ea5fbe8c9e63bc8301cd8a4a925c91be657cec6e34a9e491b34`，决定 SHA `210529b9a9ddc5c1a0f01a40369328b48f1aaa4c27323d171b0727d3b85edaf5`。

## RQ1_913e18f76600

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_913e18f76600) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:536:author:1 | setAllowedAddress | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_31ea47f8a384e60b174c`，根位置 1077＋20，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1077 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E10, E30

发现 `finding_e1dfa8433acaf4844115`，根位置 1077＋20，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1077 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E28, E9

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.230 秒，模型等待 39.892 秒，真实 solver 43 次，查询投影 46 项，动作记录含缓存 30 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 2, 'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `bcd0228c0660a83c9076be48ca83aa468c0cad2ffde5791c77abf8770489d8bc`，决定 SHA `e02c9ea8e4ba07d4b7ccf750f0719c1e80640e8b796b80406ae65928498aaa88`。

## RQ1_03a271e0c36c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_03a271e0c36c) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:538:S1 | initialize | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 2}。相关检查决定 {'external_dependency': 4, 'policy_missing': 1, 'applicable_role_guard': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.577 秒，模型等待 75.021 秒，真实 solver 7 次，查询投影 18 项，动作记录含缓存 15 项。诊断 {'unbound_or_inapplicable_seed': 3, 'audit_source_scope_mismatch': 1, 'no_locatable_source': 6, 'unrelated_or_secondary_graph_pairs_deferred': 5}。

最终报告 SHA `e4b2c7b763235ec3b91a0d65a5606a9eb79a5481ca746e2b526e4db25d118d49`，决定 SHA `ca0d548c0c5a31833dede90436fe28f2c73eb309624b8075d906923ab9dad0fa`。

## RQ1_a533300b98f5

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-10.md#rq1_a533300b98f5) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:539:author:1 | die | FN | FN | TP | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'not_reviewed': 1}。相关检查决定 {'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.126 秒，模型等待 31.405 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `a1d3f7ee3d341e47494fb90deb946407ea20727fdf86f1ad402533072b90e313`，决定 SHA `ed22c74ec1c412548a8cc6bd1ce7191ee118fb994d138eb8cf0d62694b0e3f21`。

## RQ1_3c95d2f0314b

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_3c95d2f0314b) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:540:author:1 | MADToken | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_92efcadb03879b0ad2b8`，根位置 2567＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2567 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.603 秒，模型等待 33.604 秒，真实 solver 42 次，查询投影 45 项，动作记录含缓存 50 项。诊断 {'unbound_or_inapplicable_seed': 1, 'unrelated_or_secondary_graph_pairs_deferred': 19, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `571be7677bda16343793bff4b0e8b52e640484654d62decabc4200d61fe2cccd`，决定 SHA `285dfda8289fe75acd1ca6cbdcf3313ce6490800c46653f8730c3ead32cdc6a3`。

## RQ1_2d9b7fbe78a5

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_2d9b7fbe78a5) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:541:author:1 | Owned2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_cf6469a772240aacc8b5`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E24

发现 `finding_4132d2e17f28ee98f7ea`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E18

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.393 秒，模型等待 57.003 秒，真实 solver 12 次，查询投影 22 项，动作记录含缓存 24 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c8895cfd9c48b1023834645de5410d38be666bbe01ce76652adf8fb30cdf3e8e`，决定 SHA `24502f0de997d095ee1aaad616bb7a737112ba188f19875187bc315946bf3cb3`。

## RQ1_aadd85d114d9

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_aadd85d114d9) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1}。相关检查决定 {'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.137 秒，模型等待 32.011 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `e7b1ae2814aef7a5fa0063e721ee2d7abefedc204d95ada01c839abde4644017`，决定 SHA `f7254277960ae762ad412daa73a637248f14bfdd0a1906fd02ce7fdecb83ff29`。

## RQ1_3342a012923f

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_3342a012923f) · 检查明细 [Checks-70.json](Checks-70.json) [Checks-71.json](Checks-71.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 6}。相关检查决定 {'policy_missing': 4, 'external_dependency': 20, 'applicable_role_guard': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 26.049 秒，模型等待 36.170 秒，真实 solver 20 次，查询投影 34 项，动作记录含缓存 76 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 24, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `9fa245c9d91255c58ef551a4fee429e895faf9ae7c00b5aa920fb825aee42e3a`，决定 SHA `9fed61cc8b555cacecc21bb0bde3dc8a4672290e80d5bfc383d6490ce8ca0bae`。

## RQ1_b45fd17eae9d

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_b45fd17eae9d) · 检查明细 [Checks-71.json](Checks-71.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:544:S1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:544:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:544:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:544:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 5}。相关检查决定 {'policy_missing': 17, 'external_dependency': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.163 秒，模型等待 90.963 秒，真实 solver 73 次，查询投影 96 项，动作记录含缓存 43 项。诊断 {'unknown_or_unshown_effect': 3, 'unrelated_or_secondary_graph_pairs_deferred': 14, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `9e8e23871713c9b61de6be7a620e1b8aa03b394d14cbc906924266b85642e99e`，决定 SHA `b9edd92a70317f79064ec5ef549df95991dde6c56812da2a53558c44d012c565`。

## RQ1_da70e0077699

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_da70e0077699) · 检查明细 [Checks-71.json](Checks-71.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5, 'policy_missing': 2}。相关检查决定 {'scoped_semantic_normal': 1, 'external_dependency': 12, 'policy_missing': 4, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.886 秒，模型等待 34.675 秒，真实 solver 17 次，查询投影 37 项，动作记录含缓存 59 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 13, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `448d393333202a37846b13b18b6763f6895869b6477311b2b3b8cc61cb7ded03`，决定 SHA `431fa35350ea652ff10734cc19507ffc084d5b7980fb2293ec09ff1f87d3fcd8`。

## RQ1_9d65bd6a5d25

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_9d65bd6a5d25) · 检查明细 [Checks-71.json](Checks-71.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 9, 'external_dependency': 2}。相关检查决定 {'scope_missing': 1, 'external_dependency': 2, 'policy_missing': 27, 'applicable_role_guard': 1, 'holder_own_transfer': 4, 'self_delegation': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.056 秒，模型等待 88.358 秒，真实 solver 46 次，查询投影 65 项，动作记录含缓存 83 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 29, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `75921b1a1e46b52581f0b5920c190c0d9b8b006550fe86e8f293f3ba2052d886`，决定 SHA `3422a431b19aaae9681442809939946ddb4359652529bb99d973452a1e9ee76e`。
