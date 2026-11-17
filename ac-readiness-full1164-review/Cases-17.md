# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_f39b6c26d8a6

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_f39b6c26d8a6) · 检查明细 [Checks-50.json](Checks-50.json) · 查询明细 [Queries-23.json](Queries-23.json) [Queries-24.json](Queries-24.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 10, 'external_dependency': 4}。相关检查决定 {'external_dependency': 10, 'policy_missing': 35, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.732 秒，模型等待 84.390 秒，真实 solver 52 次，查询投影 88 项，动作记录含缓存 128 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 45, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `265c93753d5c51ea3aa8d92dd6dc7bcfb0b32d7cfd204ac95619b0a80ecf19fa`，决定 SHA `48c66a586c06827d50f1f0eb2839ed7c89ac4032de6c5c92149d673f13dce508`。

## RQ1_58e1f2aa45d3

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_58e1f2aa45d3) · 检查明细 [Checks-50.json](Checks-50.json) · 查询明细 [Queries-24.json](Queries-24.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:399:author:1 | Doubler | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_3c0ad9a26bd7ed326160`，根位置 365＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 365 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E5

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 44.488 秒，模型等待 41.983 秒，真实 solver 35 次，查询投影 37 项，动作记录含缓存 117 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 56, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `4bac0176f8397e871777816a2ace2f5a9694fa973ba917e46dd779b04a475789`，决定 SHA `31b4788b4cdfc882b2f74b7f5ae2f9c087f75b4c1f7c4cb41203e6fddbfd87cd`。

## RQ1_3dafc8312cd7

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_3dafc8312cd7) · 检查明细 [Checks-50.json](Checks-50.json) · 查询明细 [Queries-24.json](Queries-24.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 22, 'policy_missing': 11}。相关检查决定 {'policy_missing': 23, 'external_dependency': 2, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 34.939 秒，模型等待 40.953 秒，真实 solver 72 次，查询投影 72 项，动作记录含缓存 87 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 23, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `da00b5dd834781fef3ee9fdbd2ab02c4cdf0c542fa026ba493561032d43f64b5`，决定 SHA `8a895b72cefe233db39682afd9b734a3d33a52adcb8ace43ce903badd8ff96f0`。

## RQ1_85f6a66f39c6

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_85f6a66f39c6) · 检查明细 [Checks-50.json](Checks-50.json) · 查询明细 [Queries-24.json](Queries-24.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:401:author:1 | DESALSale | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_26428e48eb37cd12e6d8`，根位置 6056＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 6056 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E110, E21

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 292.343 秒，模型等待 21.625 秒，真实 solver 76 次，查询投影 99 项，动作记录含缓存 113 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 38, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `153d14d3e117ada0bba46ce8838f7ed1da690508852c91c413100ca9e1c256c7`，决定 SHA `b6405d7d1404c1530468b6fc7d1e475c22c60e4f6523ccef706738d4499032a8`。

## RQ1_742a666ba5fe

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_742a666ba5fe) · 检查明细 [Checks-50.json](Checks-50.json) · 查询明细 [Queries-24.json](Queries-24.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:402:author:1 | WithrawDevToken | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'holder_own_transfer': 2, 'policy_missing': 34, 'external_dependency': 26, 'self_delegation': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 24.804 秒，模型等待 25.899 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ce4c5e2ddd585c98ac36eb07ce638b73f6d6acb5a53e67f12c19249afbbefa73`，决定 SHA `0130a9f9faa162cfa1d3407e7787f1dc6a27ddfa393d3da540a9179cef675469`。

## RQ1_f1d0c1efc742

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_f1d0c1efc742) · 检查明细 [Checks-50.json](Checks-50.json) [Checks-51.json](Checks-51.json) · 查询明细 [Queries-24.json](Queries-24.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 5}。相关检查决定 {'policy_missing': 36, 'external_dependency': 36}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 47.345 秒，模型等待 43.739 秒，真实 solver 86 次，查询投影 111 项，动作记录含缓存 231 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 72, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `06b3f9d0b49bbad2a96de268bb9329c525fbc4ea91e8396265e380493537a61f`，决定 SHA `824d1d8800451905855a9761003b9920068887cf5d73655aff557ca3e8c539fe`。

## RQ1_e99440cca868

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_e99440cca868) · 检查明细 [Checks-51.json](Checks-51.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:404:original:1 | vx | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:404:original:2 | ply | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 1}。相关检查决定 {'policy_missing': 1, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.118 秒，模型等待 49.090 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `0d04ac476ed6af4381999f015714a29d18054ecb97f57c77c4b49598a354ee03`，决定 SHA `919198db2067ebabf661d426be2eced72d9fc18d84e70e4a06a26a7566389750`。

## RQ1_61055eec37f1

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_61055eec37f1) · 检查明细 [Checks-51.json](Checks-51.json) · 查询明细 [Queries-24.json](Queries-24.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 3}。相关检查决定 {'external_dependency': 15, 'policy_missing': 9, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.934 秒，模型等待 21.956 秒，真实 solver 14 次，查询投影 20 项，动作记录含缓存 63 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 14, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5ab9300c688e2cbd443d963053f0474b39b4234506c370cf8d1fb14ba5324067`，决定 SHA `7a6637d6e743af4c4ada7ec88b56810852b8ffe235d896405d6fd40f4de07ee5`。

## RQ1_1f156ef466b1

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_1f156ef466b1) · 检查明细 [Checks-51.json](Checks-51.json) · 查询明细 [Queries-24.json](Queries-24.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 5, 'external_dependency': 1}。相关检查决定 {'policy_missing': 11, 'holder_own_transfer': 4, 'external_dependency': 3, 'self_delegation': 2, 'holder_issued_transfer_scope': 6}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.795 秒，模型等待 55.719 秒，真实 solver 18 次，查询投影 18 项，动作记录含缓存 39 项。诊断 {'unknown_or_unshown_effect': 2, 'explicit_effect_anchor_conflict': 2, 'unrelated_or_secondary_graph_pairs_deferred': 14, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `6f6e1009f92fb92ba096c80d61279c64596522ba17949735be9d495a6191d5d2`，决定 SHA `29ea5659fe96e0c0b5c9d8531be42d86416935bcdd872866b8ca9aa9222fcbea`。

## RQ1_e1ca494df5a4

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_e1ca494df5a4) · 检查明细 [Checks-51.json](Checks-51.json) · 查询明细 [Queries-24.json](Queries-24.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:407:author:1 | EqvcToken | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 23, 'external_dependency': 5}。相关检查决定 {'policy_missing': 63, 'external_dependency': 37, 'self_delegation': 4, 'applicable_role_guard': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 61.156 秒，模型等待 33.999 秒，真实 solver 108 次，查询投影 122 项，动作记录含缓存 309 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 94, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `fde366bce9648a16abfa8ef581d2ccb12588eb0cb369e65c8b185c3af8aa4509`，决定 SHA `99fbb217d8e71f6978ab5fbbb32098656650905c0cdab15817dd262eaf05f74d`。

## RQ1_77486f861519

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_77486f861519) · 检查明细 [Checks-51.json](Checks-51.json) · 查询明细 [Queries-24.json](Queries-24.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:408:author:1 | constructor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_35ecc5e7d8403836d9fc`，根位置 291＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 291 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E4, E51

发现 `finding_2c45e9aa01492117d99a`，根位置 291＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 291 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E47

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 1210.663 秒，模型等待 49.946 秒，真实 solver 91 次，查询投影 105 项，动作记录含缓存 88 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 36, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `94f7f2cc177515c1fd61e9130b2a05f8a8ef07695a1a2d9bf8a32cca562f7edf`，决定 SHA `2993fafbd4c243c59c409404af134483a6fc6883083c04fc27b9c04ff70c9571`。

## RQ1_8e285b5fe9e2

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_8e285b5fe9e2) · 检查明细 [Checks-51.json](Checks-51.json) · 查询明细 [Queries-24.json](Queries-24.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:409:author:1 | Predatex1 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_77dbd8a46af61c9b08be`，根位置 2840＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2840 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 91.730 秒，模型等待 65.897 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `4df4902f8f12793fc14b75cb35c4a644a7733116c6a991b445c6b6203a3bad24`，决定 SHA `93c3c44c2cc3de2d10c0bc7bf38ed44800d3bde8fa24f0edd4b0a3ef0694ae1a`。

## RQ1_5558fa8f4749

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_5558fa8f4749) · 检查明细 [Checks-51.json](Checks-51.json) · 查询明细 [Queries-24.json](Queries-24.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 27}。相关检查决定 {'external_dependency': 45, 'policy_missing': 19, 'holder_own_transfer': 2, 'holder_issued_transfer_scope': 3, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 66.235 秒，模型等待 39.841 秒，真实 solver 21 次，查询投影 30 项，动作记录含缓存 222 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 62, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `d474cb3bca77de629c930eb8148eba0e5e179230d3ef57d290f3bef417606e69`，决定 SHA `92aacf1cc4e18c361bff96ad00006b93ff4a436af01d06813296118300412823`。

## RQ1_86e344166934

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_86e344166934) · 检查明细 [Checks-51.json](Checks-51.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:411:S1 | Kill | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1}。相关检查决定 {'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.210 秒，模型等待 19.836 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `b89c433e746ccac087d9f3812f87b6095852176e51017b357cd365ca4f388bce`，决定 SHA `2e2cf4988e819b173698d53401dcc9468fcc1180816faf2291a90781fe2b3bbb`。

## RQ1_2a3f29f582b8

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_2a3f29f582b8) · 检查明细 [Checks-51.json](Checks-51.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:412:author:1 | end_redeem_period | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 1}。相关检查决定 {'external_dependency': 18, 'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.042 秒，模型等待 106.738 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 76 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 18, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `34a603a404ff440d17869c51e4ca7624f4316353bb3278b9bedebbbbffacc762`，决定 SHA `7ce184e4bdf4ca577e3de3dd27e079c8178392bd91fb559bf136a43fb0d3a144`。

## RQ1_17542fe3fddc

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_17542fe3fddc) · 检查明细 [Checks-51.json](Checks-51.json) · 查询明细 [Queries-24.json](Queries-24.json) [Queries-25.json](Queries-25.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:413:author:1 | Ethraffle | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_8945fb234359ffb57081`，根位置 980＋23，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 980. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 571.923 秒，模型等待 25.788 秒，真实 solver 1247 次，查询投影 1265 项，动作记录含缓存 315 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 103, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `4266ce9856093a551c9e81081b0aa7db67ec2e4e1e44fb7ace5fa8f8172dd72a`，决定 SHA `54c022ee615a5f4d7e6cd0a4b53ac4d8bad1eccdbfdb0235aada4579bbc61a51`。

## RQ1_8672b1ce272c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_8672b1ce272c) · 检查明细 [Checks-51.json](Checks-51.json) [Checks-52.json](Checks-52.json) · 查询明细 [Queries-25.json](Queries-25.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 3}。相关检查决定 {'external_dependency': 9, 'policy_missing': 9, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.880 秒，模型等待 16.154 秒，真实 solver 14 次，查询投影 20 项，动作记录含缓存 45 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 8, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5513b5e5cbe8be03c18b6d1826f8205274fb233caee067c0237493861b769b28`，决定 SHA `2846d6a68852e944d6e0bcafeb6563bb5180ddfef48d607e18a13d4643f42c3c`。

## RQ1_87301d949ea4

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_87301d949ea4) · 检查明细 [Checks-52.json](Checks-52.json) · 查询明细 [Queries-25.json](Queries-25.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 3}。相关检查决定 {'external_dependency': 9, 'policy_missing': 9, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.640 秒，模型等待 25.310 秒，真实 solver 8 次，查询投影 14 项，动作记录含缓存 43 项。诊断 {'audit_source_scope_mismatch': 1, 'audit_effect_unbound': 1, 'unrelated_or_secondary_graph_pairs_deferred': 8, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `721ecd282d17506fa812b3602f46796d78ab4cdd1add7c05da8376130d72c972`，决定 SHA `eeafc388edc1cae0c77c6fd644a006c9ee08f3902149fbbc4e84a6d436f020d6`。

## RQ1_b809aa517821

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-08.md#rq1_b809aa517821) · 检查明细 [Checks-52.json](Checks-52.json) · 查询明细 [Queries-25.json](Queries-25.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:416:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_a1cba06bb74b6c2c290e`，根位置 2243＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2243. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.511 秒，模型等待 37.972 秒，真实 solver 13 次，查询投影 14 项，动作记录含缓存 16 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `b7277276028b964f65ddb4dc9f584f2ef1cb7bee5571e2bdca52ca6b2075aeb5`，决定 SHA `f3772610dc048acb2ba2f49bc3dda80708a67f336d7295cbe85dc62c5f555a21`。

## RQ1_30e6629a4a09

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_30e6629a4a09) · 检查明细 [Checks-52.json](Checks-52.json) · 查询明细 [Queries-25.json](Queries-25.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:417:author:1 | setOracleAddress | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_06ff962c90b1f259bb2d`，根位置 7212＋16，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 7212 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E34, E7

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.598 秒，模型等待 30.707 秒，真实 solver 15 次，查询投影 16 项，动作记录含缓存 52 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 22, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `49b9f069e59c82d67e558dcd771295f47010539faa3fbf6b4233ef0c62cb6c40`，决定 SHA `46baeba3d7209212b3486f101ad5a263e92ea7f3ebefc54f4101e2e757bd0eab`。

## RQ1_84ed7052a606

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_84ed7052a606) · 检查明细 [Checks-52.json](Checks-52.json) · 查询明细 [Queries-25.json](Queries-25.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:418:author:1 | init | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_e50ac58a22073045b4cc`，根位置 1588＋19，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1588 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E15

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.375 秒，模型等待 61.624 秒，真实 solver 44 次，查询投影 57 项，动作记录含缓存 24 项。诊断 {'missing_claim_or_source_anchor': 5, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 7, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `56f250173786103614ee25ccf970e276a1aa343c99ce68c8d479746da4ac481c`，决定 SHA `f5d5a33c29cf32c644adc3c55553de50fd6c38ad80f90454a19cc0ef3a01a902`。

## RQ1_9fff9a0c4cd9

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-08.md#rq1_9fff9a0c4cd9) · 检查明细 [Checks-52.json](Checks-52.json) · 查询明细 [Queries-25.json](Queries-25.json) [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:419:author:1 | UselessAirdroppedToken | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 10, 'external_dependency': 4}。相关检查决定 {'policy_missing': 113, 'external_dependency': 61, 'applicable_role_guard': 1, 'holder_own_transfer': 2, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 169.583 秒，模型等待 55.069 秒，真实 solver 80 次，查询投影 91 项，动作记录含缓存 514 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 174, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `01cb467394f6dd31cefa8ce8d4b35fabe2747d828f6a8940e6aef9ed7cd39ae7`，决定 SHA `88793d90a3fea285989b7c528b4c40c2cdc7296bc4ec6cada563102e4dc82efe`。

## RQ1_2d04d0852310

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_2d04d0852310) · 检查明细 [Checks-52.json](Checks-52.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:420:author:1 | BITDINERO | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_026d2baaf5ef52201490`，根位置 2858＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2858 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 93.223 秒，模型等待 57.003 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'invalid_semantic_row': 1, 'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `f655a8986c53751fa3ade0490419260a313a3dce6b3eabd341d3c87d94ff5578`，决定 SHA `0e932d65c6188311e3000866023c9c26b1d33ca5fd0955066aa24be37dd11322`。

## RQ1_5535d927a148

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-08.md#rq1_5535d927a148) · 检查明细 [Checks-52.json](Checks-52.json) · 查询明细 [Queries-26.json](Queries-26.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:422:author:1 | EGC | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_0f7ef4e9bf21612b972e`，根位置 3183＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 3183 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E33

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.625 秒，模型等待 66.592 秒，真实 solver 19 次，查询投影 21 项，动作记录含缓存 31 项。诊断 {'no_locatable_source': 5, 'unrelated_or_secondary_graph_pairs_deferred': 11, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `fd8c07e6fb518c6df5c912c710aa3523cb951451a3b43724f69e3d8bc382c337`，决定 SHA `13ce07bac5999dfc951db58fdf5b268fe48e539a058f48b8429cfd038b815ef7`。
