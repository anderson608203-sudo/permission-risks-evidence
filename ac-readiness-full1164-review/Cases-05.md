# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_7eb51c5c90eb

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_7eb51c5c90eb) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:104:author:1 | ActiveAdmin | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 5}。相关检查决定 {'external_dependency': 11, 'policy_missing': 6, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.382 秒，模型等待 29.625 秒，真实 solver 18 次，查询投影 18 项，动作记录含缓存 52 项。诊断 {'missing_claim_or_source_anchor': 1, 'unrelated_or_secondary_graph_pairs_deferred': 17, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ecefb0f86cb0b9b7366aebed5284081b8e7cf26be6ffc0e1ab4768703f5774a2`，决定 SHA `db86bc4ab97db630f866e3ea32750ec337a4be7918aee685ef50f4a99c66568d`。

## RQ1_722e54765950

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_722e54765950) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:105:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_4f7f125b8dbb477761de`，根位置 2222＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2222 under financial_right. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E11

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.083 秒，模型等待 48.575 秒，真实 solver 23 次，查询投影 26 项，动作记录含缓存 20 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 7, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `8ee28424bef24322cf2e9976102e821e62fb58311a38cc983c0b1a03071eddb6`，决定 SHA `3ff1458e4c676f782c3157388bc6493d45c79254304e93b442711716c2d483c1`。

## RQ1_3f5582773b12

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_3f5582773b12) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 7}。相关检查决定 {'external_dependency': 12, 'nominee_acceptance': 6}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.257 秒，模型等待 73.887 秒，真实 solver 0 次，查询投影 8 项，动作记录含缓存 44 项。诊断 {'audit_card_text': 1, 'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 12, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `a3539274418fe64eabd33fcaf1124193744bbe606fef4f42fe926bb92d03ddd8`，决定 SHA `e48214b0dbb8fa4adbf9d7b0e270058c0a56370c73cf1c680e1a6dae38a2b048`。

## RQ1_42cd873440a3

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_42cd873440a3) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'external_dependency': 7}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.473 秒，模型等待 56.380 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 16 项。诊断 {'no_locatable_source': 1, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `5625b5c7b02ce462056755ee14c67a63f9cd60a59cbf9e92b948bae94dce3c7e`，决定 SHA `465c5c8e2f005dc450becf2e0f77ca66eeb299dceeb483fef42f32dbcf43e5f1`。

## RQ1_adc795eb2050

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_adc795eb2050) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:108:original:1 | initialize | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 1}。相关检查决定 {'external_dependency': 21, 'policy_missing': 11, 'applicable_role_guard': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.214 秒，模型等待 55.319 秒，真实 solver 16 次，查询投影 32 项，动作记录含缓存 121 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 31, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ba4e0511003f8c7098cca7768b2db53dc5b3768cd57e2fc39c7b077b34b99083`，决定 SHA `7d72a144b791ec241dcbfe9c0dc4f46833513d64c9e5bbe041c50eda246eb458`。

## RQ1_9e690544f022

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_9e690544f022) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 11, 'external_dependency': 16}。相关检查决定 {'holder_own_transfer': 8, 'applicable_role_guard': 3, 'external_dependency': 51, 'policy_missing': 25, 'self_delegation': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 30.336 秒，模型等待 51.231 秒，真实 solver 33 次，查询投影 114 项，动作记录含缓存 267 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 73, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `10231b71fbfbfb3d66aec07e30fd6338930177361b1ae81dc059c858cabcc7ff`，决定 SHA `8abcc848cf283c984636cd566c2c6a7660dc7ba5ca02bb352f30fc7337077db0`。

## RQ1_ac3501efc177

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_ac3501efc177) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:110:author:1 | destroy | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 1}。相关检查决定 {'external_dependency': 1, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.184 秒，模型等待 19.435 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `e28b99bb65b6425d116a1858a7fb4073469a2ab529ec13a2c6488b3a21368668`，决定 SHA `84050e71280bba919bd266b6129f4671972f4098f4c0706d75c3a5508c21a837`。

## RQ1_62bedd2d4a5a

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_62bedd2d4a5a) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-05.json](Queries-05.json) [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:111:author:1 | Constructor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_625347be9714f40f2975`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E50

发现 `finding_d6f939e13ae0fc4f2137`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E58

发现 `finding_7d065067eb60442d68ec`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E54

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.230 秒，模型等待 49.595 秒，真实 solver 26 次，查询投影 66 项，动作记录含缓存 93 项。诊断 {'audit_effect_unbound': 2, 'unrelated_or_secondary_graph_pairs_deferred': 30, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `8540a6e1d3ce9935779eb3ea6c9ba41dae24b748aa24663bd22ae44b34848022`，决定 SHA `11135f1f6ceb4684e2b583c3a0cf5bd56f57120ef79d493ad4de078bccb154b6`。

## RQ1_3df2913c0653

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_3df2913c0653) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 7, 'policy_missing': 9}。相关检查决定 {'policy_missing': 47, 'holder_issued_transfer_scope': 6, 'external_dependency': 29, 'holder_own_transfer': 4, 'self_delegation': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 70.746 秒，模型等待 38.736 秒，真实 solver 4 次，查询投影 17 项，动作记录含缓存 227 项。诊断 {'unknown_or_unshown_effect': 1, 'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 76, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `8d533c50c01a8185f88de641941448e9c3885d23c2d004a5dc9b1953b9d294a0`，决定 SHA `dce2ea980267ae07f6c20149fc8510e479bd5067c864a5344d8613a495ac2bb4`。

## RQ1_6674f42c37b9

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_6674f42c37b9) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:113:author:1 | Ownable | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_aa1753ba247d45e98373`，根位置 4961＋642，依据 `program_support`。At transfer(address,uint256), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification. 证据 E104, E129, E20, E66

发现 `finding_5355f5caccd876824ee0`，根位置 3214＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 3214 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E64, E7

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 328.501 秒，模型等待 48.669 秒，真实 solver 53 次，查询投影 57 项，动作记录含缓存 94 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 40, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `412928975b62e9e3d64ceab6221a1873a18ab9119865963a35a5514c5b07be9e`，决定 SHA `7e404edf3e9477a68882ad4db6683621406f7b7db5f6b323dabf4678f17915ef`。

## RQ1_6e4c18c9b391

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_6e4c18c9b391) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:114:author:1 | initialize | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 2}。相关检查决定 {'external_dependency': 4, 'applicable_role_guard': 2, 'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.795 秒，模型等待 46.426 秒，真实 solver 7 次，查询投影 18 项，动作记录含缓存 15 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `fd1648089aaec0469bda9ec64b01dc0b6012ff0a3f5e02c7f9bbf7c71e4fcf38`，决定 SHA `8d180cafe08d7cac027b887983a68454259e240c3f7d8b2b54bab4067ce28bcf`。

## RQ1_fe06586a5fa7

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_fe06586a5fa7) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:115:author:1 | setOwner | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_3298780bbc1db6e0fd22`，根位置 700＋14，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 700 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E70

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 75.772 秒，模型等待 38.286 秒，真实 solver 42 次，查询投影 78 项，动作记录含缓存 133 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 58, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `31dff58b804edbbcf932e4f6ffbcfa4964dbbf1cbef424a63a38283fb369f624`，决定 SHA `f085bb8b42b673da7941d4a53ecc58b6a013717786c7108845cea08743a0bfcd`。

## RQ1_873a97b72ee6

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_873a97b72ee6) · 检查明细 [Checks-13.json](Checks-13.json) [Checks-14.json](Checks-14.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:116:author:1 | MAC | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_8b9d0e93930b9f64cc8d`，根位置 2844＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2844 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 97.383 秒，模型等待 42.376 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5a4c79a8db52196807079cc83a82e0ad34c7f085ba8dc788790838851b114500`，决定 SHA `cc0a315694725b4b76cec28b21824a4d21c80ce8574ac2a8eadf3716f79b5f85`。

## RQ1_a1af72ed0932

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-03.md#rq1_a1af72ed0932) · 检查明细 [Checks-14.json](Checks-14.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:117:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_f0b4e8d645beaee4e80d`，根位置 2225＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2225. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E9

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.703 秒，模型等待 56.947 秒，真实 solver 11 次，查询投影 14 项，动作记录含缓存 20 项。诊断 {'no_locatable_source': 5, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `2826a1bdfa6dd53508ec76b12ec2c269423c61b1c9c1e930bc24f846bbb2cbc5`，决定 SHA `8a1db31458a68adc550faaf3373ac7c5a753b51bf0e8428f137c81bdb33928dc`。

## RQ1_06fc1aece17b

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_06fc1aece17b) · 检查明细 [Checks-14.json](Checks-14.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:118:author:1 | owned | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_51b50e0ce4179615e9f0`，根位置 99＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E170, E2

发现 `finding_8bccae6640b1d94b343b`，根位置 99＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E118

发现 `finding_409e06b082be61bae291`，根位置 99＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E176, E3

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 169.661 秒，模型等待 18.797 秒，真实 solver 72 次，查询投影 94 项，动作记录含缓存 339 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 109, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `0af74217662be52a868d83a14d539772fb41954ad53943f26142b5d002d7a4c8`，决定 SHA `cc4e738b650dac49472ca62cc4c6adad1fc8a8b2344bb44a1b703c716eb18fa6`。

## RQ1_30d9b2008c70

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_30d9b2008c70) · 检查明细 [Checks-14.json](Checks-14.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:119:author:1 | Constructor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_9052b7cd1e13c3bd49e3`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

发现 `finding_e64bd98a1ee356dd35d9`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E50

发现 `finding_2a8c8e74d3687b4d2df9`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E54

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.784 秒，模型等待 87.277 秒，真实 solver 26 次，查询投影 64 项，动作记录含缓存 92 项。诊断 {'unknown_or_unshown_effect': 2, 'unrelated_or_secondary_graph_pairs_deferred': 30, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `d6a8fdf7da22bda5376e4a474a60dfc4ceb69de87ed17fe13777f746cd9ee8bc`，决定 SHA `01cc81b19b3a74f3277f2411c395a659a5263190ee5bf50a71d5a00098cd773a`。

## RQ1_5296ceb53c68

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_5296ceb53c68) · 检查明细 [Checks-14.json](Checks-14.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:120:author:1 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 2}。相关检查决定 {'scoped_semantic_normal': 1, 'policy_missing': 2, 'external_dependency': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.030 秒，模型等待 33.631 秒，真实 solver 8 次，查询投影 8 项，动作记录含缓存 12 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1, 'semantic_answer_outside_sent_scope': 1}。

最终报告 SHA `7eeba2fa9a57cd758d159f53a112ad03eac93760a54927d7b526da5c6f6306c4`，决定 SHA `dc334bf0c67aa0a4c322c3ddd30b3a2b9c84bebe968342d3213e14b6e8b4c28a`。

## RQ1_bbcf89ce1cf0

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-03.md#rq1_bbcf89ce1cf0) · 检查明细 [Checks-14.json](Checks-14.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:121:author:1 | BitcoinPro | FN | FN | TP | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 1}。相关检查决定 {'policy_missing': 4, 'external_dependency': 6, 'self_delegation': 1, 'holder_own_transfer': 2, 'holder_issued_transfer_scope': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.765 秒，模型等待 49.611 秒，真实 solver 5 次，查询投影 6 项，动作记录含缓存 19 项。诊断 {'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 8, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c414a64b354574547b012a852b8484e845ad24bac08e8e2fe968927dc3cbeca0`，决定 SHA `cb776715b39076293b06d507436a5c2ede8c34b569d2f94dcc9abe3766fd922c`。

## RQ1_af407c4bc5c0

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_af407c4bc5c0) · 检查明细 [Checks-14.json](Checks-14.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:122:author:1 | Leg | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_59e9f31be2e2d7d7a8fd`，根位置 2839＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2839 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 93.719 秒，模型等待 68.517 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'invalid_semantic_row': 2, 'missing_claim_or_source_anchor': 5, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `3adef7535c146174d28a3b34901b8f8943870b66e60e5bbee0257b591ff1e872`，决定 SHA `8b94e03b0157db8f62f5610e24fe10b03fe1c5e13c16155a62bc37e263d56daa`。

## RQ1_6799c13e80ef

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_6799c13e80ef) · 检查明细 [Checks-14.json](Checks-14.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:123:author:1 | Constructor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_16e86589c836c2573d78`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E53

发现 `finding_63148aca94dd34b8b67c`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E45

发现 `finding_787a337c7e3e0a6ccbc5`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E49

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.248 秒，模型等待 43.655 秒，真实 solver 20 次，查询投影 60 项，动作记录含缓存 80 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 24, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `8cce6c69a4d9a63113cca4ffbedad60b6cb83ada23646981752d36dcdbe4bd2a`，决定 SHA `7dd1c4a0648a18827e429bab04ac55648f12a03a21d080e3182accb2e3beede0`。

## RQ1_0f49bef729a8

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_0f49bef729a8) · 检查明细 [Checks-14.json](Checks-14.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:124:author:1 | owned | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_f8895f7ba4923b0c8615`，根位置 122＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 122 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E26

发现 `finding_2fea5386189e27dfa39b`，根位置 122＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 122 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E33

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.604 秒，模型等待 46.636 秒，真实 solver 27 次，查询投影 32 项，动作记录含缓存 32 项。诊断 {'audit_effect_unbound': 1, 'unknown_or_unshown_effect': 2, 'unrelated_or_secondary_graph_pairs_deferred': 7, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `56d8192ae05dfbfb28cc73f1078e9d0906bd130d17a8ad8e3c38d0f247ada9a2`，决定 SHA `72bd80c2d955fd6df119d4a255b7552615e1b721f2da91542ce5ac49812ca04b`。

## RQ1_763f48e4e3b3

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_763f48e4e3b3) · 检查明细 [Checks-14.json](Checks-14.json) [Checks-15.json](Checks-15.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 10, 'external_dependency': 1}。相关检查决定 {'policy_missing': 42, 'external_dependency': 49, 'holder_own_transfer': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 59.011 秒，模型等待 45.616 秒，真实 solver 33 次，查询投影 92 项，动作记录含缓存 242 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 87, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `42d2e2e7d6c5160b1b1dd93846f512d966b2cab6c5bf3db31826ee976a249acb`，决定 SHA `56483a65aa68d781502d8a28bc9013e02c33b7eb13c1340180c73b2b28f843f8`。

## RQ1_671ac389b102

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_671ac389b102) · 检查明细 [Checks-15.json](Checks-15.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:126:author:1 | ominiraprotocol | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'policy_missing': 35, 'external_dependency': 26, 'holder_own_transfer': 2, 'self_delegation': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 25.711 秒，模型等待 83.466 秒，真实 solver 60 次，查询投影 68 项，动作记录含缓存 150 项。诊断 {'unbound_or_inapplicable_seed': 2, 'unrelated_or_secondary_graph_pairs_deferred': 61, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `f2ce3735eb7577c6d8482f561e705419d48fd9a476d535602dd69cc82bbc3b9e`，决定 SHA `0ad55ee056854b1c925a6e813afd518a52207b092d0ef554b822ec61299dda46`。

## RQ1_8679b39112d1

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-03.md#rq1_8679b39112d1) · 检查明细 [Checks-15.json](Checks-15.json) · 查询明细 [Queries-06.json](Queries-06.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:127:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_52cbc207ce0344b79153`，根位置 2222＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2222. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.610 秒，模型等待 57.038 秒，真实 solver 13 次，查询投影 14 项，动作记录含缓存 16 项。诊断 {'explicit_effect_anchor_conflict': 5, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `338bd9e529b7a42240d421f495ddd54fc3be2b7d4973b8a708a0bc4f91e10032`，决定 SHA `22f6d5def411b4841dee4a865a827b1bd7fc8dbb14e8841c3fa37d51415780bb`。
