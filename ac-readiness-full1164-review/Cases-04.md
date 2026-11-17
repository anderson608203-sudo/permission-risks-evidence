# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_e35c80271bc7

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_e35c80271bc7) · 检查明细 [Checks-10.json](Checks-10.json) · 查询明细 [Queries-04.json](Queries-04.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:78:author:1 | StoriqaCash | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 10, 'external_dependency': 4}。相关检查决定 {'policy_missing': 113, 'external_dependency': 61, 'self_delegation': 1, 'applicable_role_guard': 1, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 172.018 秒，模型等待 75.317 秒，真实 solver 80 次，查询投影 91 项，动作记录含缓存 515 项。诊断 {'audit_source_scope_mismatch': 3, 'unrelated_or_secondary_graph_pairs_deferred': 173, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `910e46a8e34974b73026f4cc201cb1b5e312ad24d45161d2e165697f78d81cdb`，决定 SHA `c0e0eb79a80b64b622d30757497b58922115b2e4e75b58c0cfe2682e82651acb`。

## RQ1_a3ce171c6be6

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_a3ce171c6be6) · 检查明细 [Checks-10.json](Checks-10.json) · 查询明细 [Queries-04.json](Queries-04.json) [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:79:S1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:79:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:79:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:79:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 5}。相关检查决定 {'applicable_role_guard': 1, 'policy_missing': 17, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.102 秒，模型等待 55.477 秒，真实 solver 72 次，查询投影 96 项，动作记录含缓存 43 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 14, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5cd22350973e0e5337f731f32c7ef2572c12c5e42a427abe1dad231e2d5201e0`，决定 SHA `f3c76f522a1893e7725ac3232292d1a4a4467d377aedc7a7a25ce9b68772713d`。

## RQ1_4bae85054465

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_4bae85054465) · 检查明细 [Checks-10.json](Checks-10.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 10}。相关检查决定 {'policy_missing': 20, 'holder_own_transfer': 5, 'applicable_role_guard': 2, 'self_delegation': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.219 秒，模型等待 33.960 秒，真实 solver 39 次，查询投影 40 项，动作记录含缓存 52 项。诊断 {'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 20, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `b5e24b86eeb287410180c48084ac20f188708bef4884831d54a4f627928ca09d`，决定 SHA `89a248e8609c0a88be0e1eeb25b7c43de171ed7fd69bfe566fd800b30cbb448a`。

## RQ1_d6e00d8f7f56

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-02.md#rq1_d6e00d8f7f56) · 检查明细 [Checks-10.json](Checks-10.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:81:author:1 | setAllowedAddress | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_24cfcfae7e501f6d699a`，根位置 1106＋20，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1106 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E30

发现 `finding_90f826889d9e6351454c`，根位置 1106＋20，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1106 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E34

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.771 秒，模型等待 83.263 秒，真实 solver 31 次，查询投影 70 项，动作记录含缓存 52 项。诊断 {'unknown_or_unshown_effect': 4, 'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 8, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `19f1c56b3a161c29f46733d8d70f794391ee5626e8287033f023609aae9a0d8a`，决定 SHA `58e92aafda75bdf3411879e7f5076f4b9983609da79ff30fd7b87edc5b3501f0`。

## RQ1_37498e68783c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_37498e68783c) · 检查明细 [Checks-10.json](Checks-10.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 6, 'external_dependency': 6}。相关检查决定 {'external_dependency': 37, 'policy_missing': 18, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 26.185 秒，模型等待 43.134 秒，真实 solver 44 次，查询投影 67 项，动作记录含缓存 185 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 54, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `f83853a5c4105dabeafe3fa022a9a1dcfa0a8400bfeaacaa099b53792645d226`，决定 SHA `01092a028fb79f1e4032d45acfca3daa439580e295d28366aa55b4b6c5c9dd67`。

## RQ1_0646056d402b

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_0646056d402b) · 检查明细 [Checks-10.json](Checks-10.json) [Checks-11.json](Checks-11.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 48, 'policy_missing': 4}。相关检查决定 {'policy_missing': 10, 'external_dependency': 31, 'holder_own_transfer': 1, 'applicable_role_guard': 1, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 59.695 秒，模型等待 58.003 秒，真实 solver 20 次，查询投影 26 项，动作记录含缓存 151 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 35, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `3e14202512d77bddb53f94b0888da75c45e41dd91eee92495665a5acac399bc9`，决定 SHA `77a62861d58223f8d5a373526e2018f7d1b69072854b4c8e0c20d9239a15f35d`。

## RQ1_2199b3bb427b

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_2199b3bb427b) · 检查明细 [Checks-11.json](Checks-11.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 3}。相关检查决定 {'policy_missing': 9, 'external_dependency': 9, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.060 秒，模型等待 25.349 秒，真实 solver 14 次，查询投影 20 项，动作记录含缓存 45 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 8, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `fd203ca993442bf510e0e5ab0b031873e85697d0cae667cb0430823b9938ead2`，决定 SHA `48234e0c36c559127b5582722f401a01b496879a254fe6403f953198d409230f`。

## RQ1_b974cb3eae41

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_b974cb3eae41) · 检查明细 [Checks-11.json](Checks-11.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 2}。相关检查决定 {'external_dependency': 64, 'policy_missing': 33}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 77.769 秒，模型等待 60.770 秒，真实 solver 6 次，查询投影 36 项，动作记录含缓存 350 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 97, 'noncached_action_limit': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `15b8fadd3f4d11c82e436826fa21922e8bd64eec2d5daee4a4655151047546fe`，决定 SHA `9dc3c0967523472da5321df4501e6e9d208096d2fa05a2908b0e63468ce6f826`。

## RQ1_ed7c5ffc5160

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-02.md#rq1_ed7c5ffc5160) · 检查明细 [Checks-11.json](Checks-11.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:86:author:1 | mintTo | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_80f27875a448fad6c77a`，根位置 2542＋531，依据 `program_support`。At transferFrom(address,address,uint256), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification. 证据 E1, E15

发现 `finding_dca2a3c905266a26460b`，根位置 2220＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2220. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E12

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.769 秒，模型等待 42.856 秒，真实 solver 15 次，查询投影 18 项，动作记录含缓存 17 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `2d584a31952cc5c289acf1b227bc94c4d018dc801f8b745ca35ebb1c392623ab`，决定 SHA `d9b93011d5b577e37224bca91c615177247fd01f27f884b13901d365df408178`。

## RQ1_f692c464b513

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_f692c464b513) · 检查明细 [Checks-11.json](Checks-11.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:87:author:1 | payout | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 1}。相关检查决定 {'external_dependency': 83, 'policy_missing': 11}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 161.250 秒，模型等待 39.464 秒，真实 solver 38 次，查询投影 58 项，动作记录含缓存 189 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 93, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `80adaeb3073b48ab011e1201cfc8ff3d1f1fe66e3708187d9e6a20f43093f07f`，决定 SHA `f8b5a9f759efdbd07ec9d29480d926ed9c5462bce9115f9bd15a660a7a3f2b5a`。

## RQ1_cea1b483c963

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_cea1b483c963) · 检查明细 [Checks-11.json](Checks-11.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 9, 'external_dependency': 4}。相关检查决定 {'policy_missing': 17, 'holder_own_transfer': 6, 'self_delegation': 2, 'applicable_role_guard': 3, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 13.130 秒，模型等待 53.811 秒，真实 solver 80 次，查询投影 107 项，动作记录含缓存 63 项。诊断 {'unknown_or_unshown_effect': 1, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 15, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `f48baccbf0146c42dee299b983242e43931b7c1c2a71aea0df931a866598166c`，决定 SHA `f4c5740e67dd75ecef97635a6d436e32173cb8586377b50340adb24e01862e14`。

## RQ1_a2b72affd3ef

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-02.md#rq1_a2b72affd3ef) · 检查明细 [Checks-11.json](Checks-11.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:89:author:1 | Matching_Ethers | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_86d02c8e18dba59b1d43`，根位置 1541＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1541 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 33.224 秒，模型等待 21.508 秒，真实 solver 1 次，查询投影 7 项，动作记录含缓存 157 项。诊断 {'unbound_or_inapplicable_seed': 1, 'unrelated_or_secondary_graph_pairs_deferred': 77, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `a81f3a15155643b910fda2dbedecbc924efb980d70b399d2a3c0cd7e24f53e2f`，决定 SHA `d8ee5f40085c67545c69d29a86ce320af7259998a3694780fa5dc145533ccf5e`。

## RQ1_bae823e736e2

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_bae823e736e2) · 检查明细 [Checks-11.json](Checks-11.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:91:author:1 | removeContract | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3, 'policy_missing': 1}。相关检查决定 {'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.367 秒，模型等待 26.651 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `6d453ce40a0841e25ba36283031c1a5b40cbe4f8eecf56e26f2be0bfb65436ad`，决定 SHA `cd6fb3d13d5fe72abd522b77fef9bb3cd57862fa0e938e91f988b2715741da95`。

## RQ1_6247dff94d60

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_6247dff94d60) · 检查明细 [Checks-11.json](Checks-11.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:92:original:1 | close | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:92:original:2 | play | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 1}。相关检查决定 {'external_dependency': 1, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.316 秒，模型等待 51.224 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 6 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `eedf1fc74cf0878bb2039f50639d9ff58742103bd8bdd183193097217aba681a`，决定 SHA `98a4bb8eee5837569a2851117f6a2275078c1a6ba78d5c16f286af4adcced10d`。

## RQ1_c9a2d9b618a7

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-02.md#rq1_c9a2d9b618a7) · 检查明细 [Checks-11.json](Checks-11.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:93:author:1 | FirstBloodToken | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_fb0f4234f1bc0a566366`，根位置 3827＋22，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 3827 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E67

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 19.100 秒，模型等待 35.501 秒，真实 solver 24 次，查询投影 43 项，动作记录含缓存 84 项。诊断 {'audit_card_issue_kind': 1, 'audit_effect_unbound': 1, 'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 24, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `98c9ac58d8eb214314f1c215f767e4ba524343c753889a90735a16df3e9d8bb9`，决定 SHA `886b90bc337a45289692387c3361f047cc37905857f7a9372268fb5bc28dfdcd`。

## RQ1_f25b185c19f2

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-02.md#rq1_f25b185c19f2) · 检查明细 [Checks-11.json](Checks-11.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:95:author:1 | DeskToken | FN | TP | TP | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 3, 'external_dependency': 1}。相关检查决定 {'policy_missing': 5, 'external_dependency': 6, 'holder_issued_transfer_scope': 3, 'holder_own_transfer': 4, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 13.569 秒，模型等待 53.820 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 33 项。诊断 {'missing_claim_or_source_anchor': 3, 'unrelated_or_secondary_graph_pairs_deferred': 11, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `81c25d3bde16cd78750c1b21a24e8b3ad33ee88339d8328eb2ab6e327c73eb07`，决定 SHA `7cfa5756e43ad826bae3f79afd54978f1bf1e98bb1cce7fd55a8b18048d5f57d`。

## RQ1_967e7a02c55f

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-02.md#rq1_967e7a02c55f) · 检查明细 [Checks-11.json](Checks-11.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:96:author:1 | close_bank | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 5, 'external_dependency': 1}。相关检查决定 {'policy_missing': 17, 'external_dependency': 16}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.859 秒，模型等待 62.986 秒，真实 solver 45 次，查询投影 48 项，动作记录含缓存 57 项。诊断 {'missing_claim_or_source_anchor': 4, 'audit_effect_unbound': 1, 'unrelated_or_secondary_graph_pairs_deferred': 32, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ba63fd0458b6832ce24b62827a149d77c493628a2763c15df887a9c0928f32e1`，决定 SHA `6a21359b28ff778c0476a3e60da68d5c48c0bbdaff379cb13b0c8343b1e48558`。

## RQ1_b4fca92c3262

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_b4fca92c3262) · 检查明细 [Checks-11.json](Checks-11.json) [Checks-12.json](Checks-12.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:97:S1 | owned | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:97:S2 | STARTMETADOLLAR | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 12, 'not_reviewed': 2, 'external_dependency': 6}。相关检查决定 {'policy_missing': 188, 'external_dependency': 406, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 1065.965 秒，模型等待 50.810 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'unbound_or_inapplicable_seed': 2, 'program_investigation_seconds': 2}。

最终报告 SHA `d8f450cb22a2261284a64c78847e8c0f2cb1f830fdb65ec1a81c6212c4aacb52`，决定 SHA `01c8fcf224e8eda66cced21e51396e6d8d16fa36d12ec6f271310066597ce758`。

## RQ1_d03e74720975

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_d03e74720975) · 检查明细 [Checks-12.json](Checks-12.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:98:author:1 | LottoCount | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1, 'policy_missing': 3}。相关检查决定 {'policy_missing': 7, 'applicable_role_guard': 1, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.451 秒，模型等待 45.297 秒，真实 solver 22 次，查询投影 26 项，动作记录含缓存 18 项。诊断 {'audit_source_scope_mismatch': 1, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 7, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `84e4f5bdbe7f021137f7bcd05ea9564465bc2c771cbbea9331466cd78e3df3ea`，决定 SHA `ad2b12bee1b4683a3c360bb244f526538ac84433d6a85f757076089fbb688c71`。

## RQ1_5f2ca3273ff3

任务 AC，评价类别 AC。当前报警，BG 技术失败。

[实际输入](InputSource-03.md#rq1_5f2ca3273ff3) · 检查明细 [Checks-12.json](Checks-12.json) [Checks-13.json](Checks-13.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_b1d39d78fcca81e318ce`，根位置 7595＋27，依据 `scoped_semantic_conflict`。The assessment concerns the policy governing the protected effect at source offset 7595. The located duty and the deciding caller conflict at this applied source effect; this is a scoped semantic prediction. 证据 E5

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.812 秒，模型等待 101.818 秒，真实 solver 1 次，查询投影 6 项，动作记录含缓存 78 项。诊断 {'audit_effect_unbound': 1, 'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 21, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `bdc871b85ba0a7cb431d9a351abfde6ffcc06f6e827a58a9e9a1281a5991e540`，决定 SHA `42a3c590e7d78c8fb14f8d304705405db74124e5900ee10e505745febc059987`。

## RQ1_d1f6418c49b0

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_d1f6418c49b0) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:100:author:1 | Owned2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_3bf94623620a7b5c8234`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E18

发现 `finding_8cc0d6b1aab1e965d0af`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E24

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.568 秒，模型等待 54.354 秒，真实 solver 11 次，查询投影 22 项，动作记录含缓存 24 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `23de7850b87fb0356d02d9d4c823ec0ef0bd1200ff46ce70e74679cf3a287f65`，决定 SHA `da8f25e1d8e6b86af2483654c65c95938520d976aff7da575f26c3037d9030de`。

## RQ1_b477f5b720f4

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-03.md#rq1_b477f5b720f4) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 3, 'external_dependency': 1}。相关检查决定 {'policy_missing': 4, 'holder_issued_transfer_scope': 2, 'self_delegation': 1, 'external_dependency': 3, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.419 秒，模型等待 41.297 秒，真实 solver 11 次，查询投影 13 项，动作记录含缓存 15 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `d6da2e1061f5f5d4a0a59a40dbf9ed0f2e0d0cd9bd1f5bc868bda893ea2fc11c`，决定 SHA `dce64fa91ccd05a3e86b30efc0fdfea286460129486ba459f8402af156b1b284`。

## RQ1_96afd2568bf0

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_96afd2568bf0) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:102:author:1 | Owned2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_002c57a25a72e1a4ee75`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E18

发现 `finding_26d7d3d2fbb37855b794`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E24

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.667 秒，模型等待 36.270 秒，真实 solver 12 次，查询投影 22 项，动作记录含缓存 24 项。诊断 {'unknown_or_unshown_effect': 2, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ba754fc8fbadcd0b03a9cebcfb2864c7865116cb9e938005e45ea03a7c1ddb30`，决定 SHA `bdde187ce884d4ac6ebb2900b7eea4058ac2bd9cb1611d95acef1df3cae74fe2`。

## RQ1_9b6bf82f905d

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-03.md#rq1_9b6bf82f905d) · 检查明细 [Checks-13.json](Checks-13.json) · 查询明细 [Queries-05.json](Queries-05.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:103:author:1 | OwnedResolver | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_780fa1978118de1d3250`，根位置 322＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 322 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E2

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.272 秒，模型等待 10.546 秒，真实 solver 2 次，查询投影 3 项，动作记录含缓存 2 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `736cba7d1dd205f1aa3456f55b21221c56990d3377c66cfed43bfd4f1c797228`，决定 SHA `35aa0cacee94cbbe4e1772d1b53a2520e1299e93aad174327964edcb08c99e51`。
