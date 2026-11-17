# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_34bd4d44b11a

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_34bd4d44b11a) · 检查明细 [Checks-66.json](Checks-66.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:497:author:1 | setOwner | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_7fa1995f1d546c537654`，根位置 700＋14，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 700 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E65

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 90.048 秒，模型等待 26.528 秒，真实 solver 55 次，查询投影 68 项，动作记录含缓存 186 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 59, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `07a89ddb654185b10942cc847fa0a7e2417267fa9da931b906e52acff03ce61b`，决定 SHA `ee7598fee9a35cb74de9042ada2ceab79456c5995081442eb2f5ae046662e9f6`。

## RQ1_fb0f325e2800

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_fb0f325e2800) · 检查明细 [Checks-66.json](Checks-66.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:498:author:1 | ZeroXEth | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 10, 'external_dependency': 4}。相关检查决定 {'external_dependency': 61, 'policy_missing': 113, 'holder_own_transfer': 2, 'applicable_role_guard': 1, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 172.112 秒，模型等待 55.800 秒，真实 solver 80 次，查询投影 91 项，动作记录含缓存 517 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 174, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `a2c00104f42f6b98b85301df64876616c5dece7a99ddd189baa86b4a836d1892`，决定 SHA `4548e5c07fb9a64f878c40f962a78cc1731b5b58d600d505d15d0c6be0323d85`。

## RQ1_0ff5d2904232

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_0ff5d2904232) · 检查明细 [Checks-66.json](Checks-66.json) [Checks-67.json](Checks-67.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:499:author:1 | SiaCashCoin | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_98d8d6afed0956537114`，根位置 2839＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2839 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 92.115 秒，模型等待 62.548 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'unbound_or_inapplicable_seed': 4, 'unknown_or_unshown_effect': 2, 'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `646e8037e68f8e0f1b396091b33d768078bce0b7a113879c3f1871c1ce29c62a`，决定 SHA `3c655b37f8847b370a939d63d04631d00809f7d0b7af7ba111d4368c5e4608ff`。

## RQ1_9b04bb6baa4b

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_9b04bb6baa4b) · 检查明细 [Checks-67.json](Checks-67.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:500:author:1 | ioxis | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_96cec127047b020b8966`，根位置 2832＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2832 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 92.133 秒，模型等待 78.027 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `55820ac37315d7f5237defd309a058df7b696c5c0e01a0fd8011db3249ff8b5d`，决定 SHA `97d22a526174bfc648f226968d929118394d5283a382f032ffb36b4c055b9b73`。

## RQ1_b8449e28b73a

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_b8449e28b73a) · 检查明细 [Checks-67.json](Checks-67.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:501:author:1 | setOwner | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_ca9e9cc93a19eac40c06`，根位置 700＋14，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 700 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E2, E24

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 16.912 秒，模型等待 87.483 秒，真实 solver 25 次，查询投影 37 项，动作记录含缓存 50 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'unknown_or_unshown_effect': 7, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 13, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `f57d3857f585fe2b158bc375c529697dbf1663b2ec8eed558031cd719534f17a`，决定 SHA `a1ff3ed4e21669d126bbef5627d70d62522676e3a67fb8cda640cd5fd17152b4`。

## RQ1_be5c3e642eb1

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_be5c3e642eb1) · 检查明细 [Checks-67.json](Checks-67.json) [Checks-68.json](Checks-68.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 6, 'policy_missing': 4}。相关检查决定 {'policy_missing': 440, 'external_dependency': 19}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 920.692 秒，模型等待 25.575 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 184 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 173, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `fc98d23fbeef43279c41848a5236f473e2612b8948f7fb1a5ffaba3f83cb3474`，决定 SHA `184b41e53e2a3b25216bdc2aa745235eb369a8d95970fa6dadcdec506b3878f0`。

## RQ1_579c10166d84

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_579c10166d84) · 检查明细 [Checks-68.json](Checks-68.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 22, 'policy_missing': 22}。相关检查决定 {'external_dependency': 86, 'policy_missing': 34, 'applicable_role_guard': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 54.023 秒，模型等待 17.916 秒，真实 solver 100 次，查询投影 202 项，动作记录含缓存 438 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 119, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `30ef5eaa8d4d62bb492021a970f4d9824952de6afc1f0eef8be521a33d04b4b6`，决定 SHA `c8cdd26faf17e8e24b286c47f4f0d8b24d8e965caf1591eb489787fa2306bae8`。

## RQ1_116d8aeb4b40

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_116d8aeb4b40) · 检查明细 [Checks-68.json](Checks-68.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:504:author:1 | spitoken | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 8}。相关检查决定 {'external_dependency': 26, 'policy_missing': 34, 'self_delegation': 1, 'holder_own_transfer': 2, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 25.117 秒，模型等待 35.639 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `17b0a90cbc07c38c159944ae4795c7d76d620d2e52f0be2397b4db28e5b17d97`，决定 SHA `9de2a143ab9a0e09d8a2a1947252c4001fdcb06126b79d312fea1be5c3e0dded`。

## RQ1_8a2daa767297

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_8a2daa767297) · 检查明细 [Checks-68.json](Checks-68.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 2}。相关检查决定 {'external_dependency': 60, 'applicable_role_guard': 2, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 197.426 秒，模型等待 30.225 秒，真实 solver 8 次，查询投影 10 项，动作记录含缓存 132 项。诊断 {'missing_claim_or_source_anchor': 1, 'unrelated_or_secondary_graph_pairs_deferred': 62, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `36c120e7b0a88a369ea70e94bcd9cb5b0902876e5dbb55073d1045e9fe33545c`，决定 SHA `a30e8067b41c3413a44a72dfe50af9ffdf60336113a9ed1247d251e05d0a5b7f`。

## RQ1_2d5de0155ecf

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_2d5de0155ecf) · 检查明细 [Checks-68.json](Checks-68.json) [Checks-69.json](Checks-69.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:506:author:1 | construct | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 26, 'external_dependency': 17}。相关检查决定 {'policy_missing': 205, 'external_dependency': 119}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 784.650 秒，模型等待 38.830 秒，真实 solver 47 次，查询投影 58 项，动作记录含缓存 367 项。诊断 {'no_locatable_source': 1, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'unrelated_or_secondary_graph_pairs_deferred': 123, 'noncached_action_limit': 1}。

最终报告 SHA `d1616c23b73660879e266aab0352c3b1dbf40e0624b2a855794604703cb31f36`，决定 SHA `1be2945cfa29cef0cd2947fa8bd5c54e7ef8a51e87472b717c7e260c84728351`。

## RQ1_dcd2e6a9c27c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_dcd2e6a9c27c) · 检查明细 [Checks-69.json](Checks-69.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1, 'policy_missing': 4}。相关检查决定 {'policy_missing': 9, 'external_dependency': 6}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.020 秒，模型等待 63.750 秒，真实 solver 1 次，查询投影 6 项，动作记录含缓存 39 项。诊断 {'audit_source_scope_mismatch': 1, 'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 13, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `48b31d1a2c6355d2450818f8c1854caedfda1bc87a077a9b6e59f0f7cd792f50`，决定 SHA `c30fb638f61e56f0d3037d8baf0487267ef0ad7c1bc1242ede7cb7886432a2cf`。

## RQ1_b2a70d211f2c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_b2a70d211f2c) · 检查明细 [Checks-69.json](Checks-69.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 3, 'external_dependency': 2}。相关检查决定 {'policy_missing': 6, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.889 秒，模型等待 32.269 秒，真实 solver 19 次，查询投影 19 项，动作记录含缓存 17 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 7, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `e45ca46f837d4640e3530e9398adcb3526689495a5314e503b2f94fa882ee807`，决定 SHA `8f1189464d2a6cdb2c7076a15c02dbe019b55a5929ac21e98a27c3a74c602875`。

## RQ1_7c965e77d1a3

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-10.md#rq1_7c965e77d1a3) · 检查明细 [Checks-69.json](Checks-69.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:509:author:1 | Mint | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_e5ccee67f2c7c02cf346`，根位置 659＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 659. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.412 秒，模型等待 32.066 秒，真实 solver 17 次，查询投影 19 项，动作记录含缓存 17 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 4, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c740ac23b5d2a730812d20b3f4ecf93acb04aa9434cb5afddd10795c28c3f943`，决定 SHA `50a0d430bb8c1c52a12527d028dc60e8bd793a9c8541a5a7955af2c6e8c306f9`。

## RQ1_9fea8632716d

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_9fea8632716d) · 检查明细 [Checks-69.json](Checks-69.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:510:author:1 | Ballot | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_66b744c30b41c0d88f34`，根位置 354＋24，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 354 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E54, E99

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 15.404 秒，模型等待 51.859 秒，真实 solver 29 次，查询投影 39 项，动作记录含缓存 76 项。诊断 {'audit_source_scope_mismatch': 1, 'audit_effect_unbound': 1, 'unrelated_or_secondary_graph_pairs_deferred': 25}。

最终报告 SHA `1ea508edbba874f90e2bc24106334fcdc13a48c88d767c60edca2c4221055742`，决定 SHA `e96b28b2ab7d29374da5177a67c47618921caa7b92215d1c2bcd27c78ec76894`。

## RQ1_1c88f0c3168e

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-10.md#rq1_1c88f0c3168e) · 检查明细 [Checks-69.json](Checks-69.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:511:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_d2cabc20aa07888e9b80`，根位置 2240＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2240. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E7

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.500 秒，模型等待 52.706 秒，真实 solver 11 次，查询投影 22 项，动作记录含缓存 14 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 4, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `9c48986175a6ad9ae1dd6e4ae8b2578696ddf5db6dbb5ba4f6a1cdf0a90035bd`，决定 SHA `d514537050b01bbc9f81f40130e46f6a48cddc0d428007983108a53a7eee4626`。

## RQ1_e14a7e50bf65

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_e14a7e50bf65) · 检查明细 [Checks-69.json](Checks-69.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:512:author:1 | XBornID | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_4317ed2bfcdecd62234d`，根位置 2838＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2838 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 93.376 秒，模型等待 30.900 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `091820d35059c7dbbdd778c75fba16302ff6aa91757d10658ff81bfdb7479279`，决定 SHA `6536d276ade5c966a4b757600facaf89e62d4ded067c25d1a3cb8fa147ab83ee`。

## RQ1_5add5c765bae

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_5add5c765bae) · 检查明细 [Checks-69.json](Checks-69.json) · 查询明细 [Queries-30.json](Queries-30.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:513:original:1 | disableContract | FN | FN | FN | FN | no_listed_obligation_at_reference |
| D2:513:original:2 | setupMiniGame | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 4}。相关检查决定 {'external_dependency': 54, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 23.385 秒，模型等待 48.670 秒，真实 solver 5 次，查询投影 11 项，动作记录含缓存 188 项。诊断 {'no_locatable_source': 7, 'unrelated_or_secondary_graph_pairs_deferred': 54, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `61e1beddfa7bd4950b05ee7af7de37fd066cb98688cb03b8ebb71cfbcfb0b108`，决定 SHA `cb692ce03ba43294497179d1cc11a3c16f15a643a95b29cdb1a294060928c03a`。

## RQ1_a6cdc37d0ed2

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_a6cdc37d0ed2) · 检查明细 [Checks-69.json](Checks-69.json) · 查询明细 [Queries-30.json](Queries-30.json) [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 10, 'external_dependency': 4}。相关检查决定 {'policy_missing': 21, 'external_dependency': 19, 'self_delegation': 2, 'applicable_role_guard': 3, 'holder_own_transfer': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 18.082 秒，模型等待 31.782 秒，真实 solver 58 次，查询投影 92 项，动作记录含缓存 115 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 37, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `21da29d82f1a55ac66bb9a2437a35abb892553ab8dc662656181a9541e215922`，决定 SHA `34748c787d0d9607446e92ca4448bb511c4b950de485fce8dd2420db1050cdcb`。

## RQ1_79c70cdd1bf6

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_79c70cdd1bf6) · 检查明细 [Checks-69.json](Checks-69.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:515:S1 | TimeLockr | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:515:S2 | SetReleaseDate | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:515:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:515:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2, 'policy_missing': 6}。相关检查决定 {'policy_missing': 16, 'external_dependency': 2, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.872 秒，模型等待 59.642 秒，真实 solver 69 次，查询投影 103 项，动作记录含缓存 43 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 17, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `3b930b3d819a6270f1f522b19c91b82c34c5c39454b665544223a42614851784`，决定 SHA `6aaa332aa699c346eba5967e2b4816682a87ca3135b86aa54d8b36fce2463ef4`。

## RQ1_23050a44102c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_23050a44102c) · 检查明细 [Checks-69.json](Checks-69.json) [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 16, 'policy_missing': 3}。相关检查决定 {'policy_missing': 39, 'external_dependency': 83}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 120.619 秒，模型等待 52.352 秒，真实 solver 13 次，查询投影 24 项，动作记录含缓存 271 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 122, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5ebca21cf89da2b069f28a9b4d84edb6f5cc17340251984b3de8738149ef0ad2`，决定 SHA `49b6bb1197c27cdc341d92ee2f07da7df2325e21185030ec6b36a51d5795ebfc`。

## RQ1_82ebda7c26e1

任务 AC，评价类别 AC。当前未知，BG 技术失败。

[实际输入](InputSource-10.md#rq1_82ebda7c26e1) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 3, 'external_dependency': 6}。相关检查决定 {'external_dependency': 21, 'holder_own_transfer': 2, 'policy_missing': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.535 秒，模型等待 85.213 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 74 项。诊断 {'audit_effect_unbound': 1, 'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 21}。

最终报告 SHA `df922c40a7d90aa7eafbe6598681ccf0d556a7ec616078401d59eccf0f0065b8`，决定 SHA `ebfe6b21d3012f7d7733e347fbc4b74c08850465d4fb4f59729e9cb3bd725af6`。

## RQ1_10bbee42cd76

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_10bbee42cd76) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:518:author:1 | ActiveAdmin | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 5}。相关检查决定 {'policy_missing': 6, 'external_dependency': 11, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.066 秒，模型等待 38.660 秒，真实 solver 18 次，查询投影 18 项，动作记录含缓存 52 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 17, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `d45a6ce86d646919ba351eff6d33bc4ee02f3a5d8298a67fa5181fec2cbeb350`，决定 SHA `280a7b7cec315658c06ece4329b1bc3a55bfcd7341cdda9fff5f268e59f4a263`。

## RQ1_7254da486214

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_7254da486214) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.188 秒，模型等待 52.513 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'no_locatable_source': 1, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `5df0883a7df603fe27392c10b35f025cc7cd878fcdd402ed379f81429b9aa26d`，决定 SHA `456479943e35e6e79c9e117ab9d68dc09170b09e5a54cf6a9af85b868da30413`。

## RQ1_7f2a186aa874

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_7f2a186aa874) · 检查明细 [Checks-70.json](Checks-70.json) · 查询明细 [Queries-31.json](Queries-31.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 6}。相关检查决定 {'policy_missing': 20}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.758 秒，模型等待 26.692 秒，真实 solver 24 次，查询投影 24 项，动作记录含缓存 40 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 20, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `b8965d47fb6fd45fbcaaee56d4e16993508cec8f23fb750b8804b32c556b4bb8`，决定 SHA `84d0735355ab80a48db42f7d6d7efd5070e9d361fa7c9509fa99414e32f515ad`。
