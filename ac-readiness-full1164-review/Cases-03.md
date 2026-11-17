# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_1fb2708a2d46

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-02.md#rq1_1fb2708a2d46) · 检查明细 [Checks-07.json](Checks-07.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:52:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_e1aca27ffe745fdc179d`，根位置 2225＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2225. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.340 秒，模型等待 52.535 秒，真实 solver 13 次，查询投影 14 项，动作记录含缓存 16 项。诊断 {'missing_claim_or_source_anchor': 2, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `df8b9d6587f6c95de7ea856e13e7aa3feb21b479ba9e1b64e076a9ddf95328d5`，决定 SHA `96aaf27147c0dcbe815dbe10eef685185d0cb5168e833ccad5b82af04e5a253e`。

## RQ1_38fe09bdf4c5

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_38fe09bdf4c5) · 检查明细 [Checks-07.json](Checks-07.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:53:original:1 | Vault | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |
| D2:53:original:2 | kill | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 6, 'external_dependency': 2}。相关检查决定 {'policy_missing': 7, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.117 秒，模型等待 103.949 秒，真实 solver 30 次，查询投影 43 项，动作记录含缓存 23 项。诊断 {'unknown_or_unshown_effect': 2, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `537b0702e49e2680cee9dc964be153cd24c653e997522f5f66199a07c600460a`，决定 SHA `ae92a8e9602011ecd005d0c8ef83f7a3a1bc3cd4bfa83813930b06046920b67a`。

## RQ1_51a9713a1934

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_51a9713a1934) · 检查明细 [Checks-07.json](Checks-07.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 12, 'external_dependency': 12}。相关检查决定 {'policy_missing': 63, 'external_dependency': 30, 'applicable_role_guard': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 56.889 秒，模型等待 52.417 秒，真实 solver 62 次，查询投影 64 项，动作记录含缓存 194 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 86, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `0537447bba275cd1cd69eb515bf64f15a9f8b0bef74eeae9e50b81535a5d23e7`，决定 SHA `ac53251158bccbf7fb59a36ec24a0bacffda085be8a75b55853658baf3cb6cee`。

## RQ1_7ffcfed064a0

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-02.md#rq1_7ffcfed064a0) · 检查明细 [Checks-07.json](Checks-07.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:56:author:1 | Owned2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_8007084591f6691e03cf`，根位置 1532＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1532 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E18

发现 `finding_881fd33697fc70edbf4c`，根位置 1532＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1532 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E24

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.340 秒，模型等待 39.149 秒，真实 solver 11 次，查询投影 22 项，动作记录含缓存 24 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `831ed1172567a3c2e4cf02a9e61df480cfd5eddca78c12b3bd771fe1e268d492`，决定 SHA `9c50ec36c064690b46dfef82f857f54733b48a3ee65e8552fee2ab30b09e472d`。

## RQ1_e85ac4a50ee4

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_e85ac4a50ee4) · 检查明细 [Checks-07.json](Checks-07.json) · 查询明细 [Queries-03.json](Queries-03.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:57:author:1 | kill | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 1}。相关检查决定 {'policy_missing': 4, 'external_dependency': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.565 秒，模型等待 39.460 秒，真实 solver 6 次，查询投影 6 项，动作记录含缓存 11 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 7, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `142ea06f87d1cfbb655d8216c210f19fa2f07527c158a4816f68e6b74221edcd`，决定 SHA `6a6a683255b521d3659add6e99759826918ec5a8bb9681dcd29c132dc1fd6c4f`。

## RQ1_2ab8786fb079

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_2ab8786fb079) · 检查明细 [Checks-07.json](Checks-07.json) · 查询明细 [Queries-03.json](Queries-03.json) [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:58:author:1 | BluechipToken | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 8}。相关检查决定 {'holder_own_transfer': 2, 'external_dependency': 26, 'policy_missing': 34, 'applicable_role_guard': 1, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 25.781 秒，模型等待 67.747 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'explicit_effect_anchor_conflict': 2, 'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `3855e8e9febf2b38edf214bbc52c815bf150b7791651931792b2bfd5870e8089`，决定 SHA `9084f068cfb92eb252f3551b504ca10d72c5baff4ac10baf3b7be1d0e7c7f2ed`。

## RQ1_9bf7892a772d

任务 AC，评价类别 AC。当前未知，BG 技术失败。

[实际输入](InputSource-02.md#rq1_9bf7892a772d) · 检查明细 [Checks-07.json](Checks-07.json) [Checks-08.json](Checks-08.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 9, 'external_dependency': 3}。相关检查决定 {'policy_missing': 50, 'external_dependency': 19}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 63.854 秒，模型等待 27.887 秒，真实 solver 30 次，查询投影 30 项，动作记录含缓存 185 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 66, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c97be243cb23734fcf9f56848006caa6f637929ef2e377143c7f5b1400ec679f`，决定 SHA `0c93780f38de9e4aaa29687cc25afff2d446ff8716c2c29a3dd8d662b5f6fc65`。

## RQ1_d05efb1718e4

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_d05efb1718e4) · 检查明细 [Checks-08.json](Checks-08.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:60:author:1 | BMV | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 8}。相关检查决定 {'policy_missing': 34, 'external_dependency': 26, 'holder_own_transfer': 2, 'self_delegation': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 26.205 秒，模型等待 42.233 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `8933fe0d88c616dee99c1625d561e73b45119700adf1707e4bed2030369a1ff3`，决定 SHA `1b2ea3550754fd86f5ebbd1c1d028dae668f61778fe23e55f0972fc6392238f2`。

## RQ1_5f5c873c8daa

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-02.md#rq1_5f5c873c8daa) · 检查明细 [Checks-08.json](Checks-08.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:61:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_bd8bb204b941d9b02e26`，根位置 2224＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2224. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.557 秒，模型等待 36.605 秒，真实 solver 13 次，查询投影 14 项，动作记录含缓存 16 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `d9d5899c29018ce6ae2c0e8f433ac50ae23e0d46851fb83bff4121993a7eeddb`，决定 SHA `c47d9856fe9e94690c61f15ad72192da2fbaa5aecc93f2b86c3e6b4524c0368b`。

## RQ1_309938a2bbb9

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_309938a2bbb9) · 检查明细 [Checks-08.json](Checks-08.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:62:author:1 | KingToken | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'external_dependency': 26, 'policy_missing': 34, 'applicable_role_guard': 1, 'self_delegation': 1, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 26.165 秒，模型等待 49.928 秒，真实 solver 61 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `70f784615742a0b76fdcd470743ab13c3ea4f352ab910690c667ff08a06ae0f8`，决定 SHA `fbb143da9544cbfb8a28612dcd41d1d9bebbea50c0d49cffbd34c2d955a9289c`。

## RQ1_47d8a7f2761e

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-02.md#rq1_47d8a7f2761e) · 检查明细 [Checks-08.json](Checks-08.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:63:author:1 | setOracleAddress | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_849cec36e8ad1a01f636`，根位置 7268＋16，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 7268 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E34, E7

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.080 秒，模型等待 24.180 秒，真实 solver 15 次，查询投影 16 项，动作记录含缓存 52 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 22, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c57ad040b217d9bda15f81a891d57863a3c92bd6dd68d73a03f1d506c36393c9`，决定 SHA `cf71db76c9fa03f24b3b6b79677881f43aa33cf29ea702c3284ca32ca55d15c8`。

## RQ1_05019f0c86a3

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_05019f0c86a3) · 检查明细 [Checks-08.json](Checks-08.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5}。相关检查决定 {'external_dependency': 23}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.261 秒，模型等待 58.249 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 65 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 22, 'semantic_meaning_or_explanation_polarity_unresolved': 1}。

最终报告 SHA `65bc7ba470b011dcb323ecca2ce1bca1b9c90b8ff45905c5ec2429d1bfacae0b`，决定 SHA `a04194d698d8dde0a4201b637662111ce8e58ffa87951f5b7b3a037ecc7d2a49`。

## RQ1_f5828074525a

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_f5828074525a) · 检查明细 [Checks-08.json](Checks-08.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 32, 'policy_missing': 4}。相关检查决定 {'policy_missing': 59, 'applicable_role_guard': 2, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 378.446 秒，模型等待 37.632 秒，真实 solver 34 次，查询投影 43 项，动作记录含缓存 189 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 61, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ee7d3162e91323e4820c02ffbb874c70c300bb70b3b5d59e1385cd7ef20f991a`，决定 SHA `c7e6c1befae64179abc12ebb013f3e0f6aa3165092c034a0a8f26c6f40a7ec95`。

## RQ1_0dee0198d17a

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_0dee0198d17a) · 检查明细 [Checks-08.json](Checks-08.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 36, 'external_dependency': 14}。相关检查决定 {'external_dependency': 126, 'policy_missing': 86, 'applicable_role_guard': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 231.426 秒，模型等待 49.688 秒，真实 solver 97 次，查询投影 323 项，动作记录含缓存 691 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 205, 'noncached_action_limit': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `9edaac46d927aadc91cd962b63258a2df7f34f12c89f151bcb2bb07e88745077`，决定 SHA `71a86a5782524cc20c7885f3a47540ab2faeeb2119c874916a3f2005b6780c35`。

## RQ1_281f3b161467

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_281f3b161467) · 检查明细 [Checks-08.json](Checks-08.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:67:author:1 | MyTestWallet7 | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 3, 'external_dependency': 1}。相关检查决定 {'policy_missing': 6, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.931 秒，模型等待 44.193 秒，真实 solver 13 次，查询投影 14 项，动作记录含缓存 16 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 7, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `02f014da339ed98b5f60c472af50edff8895156e99127a51a4bad0c6807e5b9d`，决定 SHA `b3deed74209840abf94aea1bbca405b7cd7a16addb85abdd2e791c0cc3bcdd38`。

## RQ1_f2ab53d09329

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_f2ab53d09329) · 检查明细 [Checks-08.json](Checks-08.json) [Checks-09.json](Checks-09.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5, 'policy_missing': 3}。相关检查决定 {'external_dependency': 148, 'policy_missing': 30}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 504.266 秒，模型等待 84.572 秒，真实 solver 25 次，查询投影 25 项，动作记录含缓存 334 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 177, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `6e035c809e5de4ee51c963b6162b854226f7bb232d018bfb877ee961fa94c8fb`，决定 SHA `95c8b9155cc5ea637d33246dbd9e050877a64ce835aecb8347bb06155837d2b0`。

## RQ1_404fa1b92065

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_404fa1b92065) · 检查明细 [Checks-09.json](Checks-09.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.353 秒，模型等待 96.761 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'no_locatable_source': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `1ea310c40d00d006fd834747fb9833bd854d24bd03312761bfdbc5403c42d8b5`，决定 SHA `9995097a731ebf8990e4aa6bc9bf6c1b13f1340af199158c33f87f6602158c9a`。

## RQ1_637f82d88251

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-02.md#rq1_637f82d88251) · 检查明细 [Checks-09.json](Checks-09.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:70:author:1 | VitToken | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_83a07e7e29652199bc98`，根位置 2848＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2848 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 98.985 秒，模型等待 25.785 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c13f02949e0be9887696838ee2665540d9e466d324f9a56e440003b6553e81b0`，决定 SHA `9601b2cf00f631f9fbe382155841ad918960ffde4590d30b1e017b4c333a505b`。

## RQ1_d090e1dba88d

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_d090e1dba88d) · 检查明细 [Checks-09.json](Checks-09.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 7, 'external_dependency': 5}。相关检查决定 {'external_dependency': 95, 'policy_missing': 20, 'applicable_role_guard': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 195.262 秒，模型等待 44.139 秒，真实 solver 34 次，查询投影 43 项，动作记录含缓存 343 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 108, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `d2f25856816351d5b86f7be8cdd432f90b102916aba71937c010787bbb40eeba`，决定 SHA `0482320259c5057e01130603af0fdb89388f924d16a47a734d4b0e0a99893794`。

## RQ1_aa45d3ff1035

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_aa45d3ff1035) · 检查明细 [Checks-09.json](Checks-09.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 2}。相关检查决定 {'external_dependency': 64, 'policy_missing': 33}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 81.881 秒，模型等待 45.425 秒，真实 solver 6 次，查询投影 36 项，动作记录含缓存 349 项。诊断 {'audit_check_target_unbound': 3, 'unrelated_or_secondary_graph_pairs_deferred': 96, 'noncached_action_limit': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `3828083d2032a25962dc6bea54522aa0920933b7f9968c33b03151383ab8f179`，决定 SHA `698127c053c931c6351045e7ee43219a5129146191f81c1d2b2cf4f251d96e9c`。

## RQ1_2a70f226d760

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-02.md#rq1_2a70f226d760) · 检查明细 [Checks-09.json](Checks-09.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:74:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_3ae2643bfb6fb9848035`，根位置 2227＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2227. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E11

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.147 秒，模型等待 49.975 秒，真实 solver 21 次，查询投影 26 项，动作记录含缓存 17 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ae55881a90c9573945357c09f5c83d2da0ee5b3459939a179296e130a9ecb9bd`，决定 SHA `e3281125520627a43893786925a8eb671865ca29f1882983aaa8dd6a45604a24`。

## RQ1_2b47449398dd

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_2b47449398dd) · 检查明细 [Checks-09.json](Checks-09.json) [Checks-10.json](Checks-10.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 43, 'policy_missing': 1}。相关检查决定 {'external_dependency': 200, 'policy_missing': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 746.991 秒，模型等待 42.912 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 504 项。诊断 {'no_locatable_source': 7, 'yield_to_source_bound_semantic_review': 1, 'unrelated_or_secondary_graph_pairs_deferred': 196}。

最终报告 SHA `03530fcac8c6d60697bad40c14777ee1500bf1d0e6219a3636f43551dec396b6`，决定 SHA `2ea0fcd2a284d87f7ef1abf3843437b959d1f0d54b3a77e5572df5eb838fe07e`。

## RQ1_155abf47bb4c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_155abf47bb4c) · 检查明细 [Checks-10.json](Checks-10.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:76:S1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:76:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:76:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:76:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 3}。相关检查决定 {'external_dependency': 1, 'policy_missing': 18, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.415 秒，模型等待 68.308 秒，真实 solver 63 次，查询投影 93 项，动作记录含缓存 45 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 16, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `54240e121eb30747a49151fcf4bd54c1db9ab13f95620be3f2ad2bda96211866`，决定 SHA `134492213dea2e27b5710ec751e35aaea560478faa8530e3e975eeff8bd98785`。

## RQ1_eb323d4d8ca9

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-02.md#rq1_eb323d4d8ca9) · 检查明细 [Checks-10.json](Checks-10.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:77:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_6cea8e7fb87c18939c0c`，根位置 2224＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2224 under financial_right. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E10

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.908 秒，模型等待 47.726 秒，真实 solver 12 次，查询投影 14 项，动作记录含缓存 15 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `148c8c04c3e28a1ea7bc7f19588c12a8bd86b40a00c72f9aa060f3bd61c6fba6`，决定 SHA `f1afd5d1e588089cfa4762cc747dc49b887fa573d6926d2c0250422f8aebccc0`。
