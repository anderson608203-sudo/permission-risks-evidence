# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_b11b4b1e0dc3

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_b11b4b1e0dc3) · 检查明细 [Checks-71.json](Checks-71.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 5, 'external_dependency': 2}。相关检查决定 {'policy_missing': 62, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 22.525 秒，模型等待 50.917 秒，真实 solver 32 次，查询投影 39 项，动作记录含缓存 128 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `0a968343e21a32523f36ec6459975d9dcbcc33644e65d20a81499493bf084afc`，决定 SHA `47f29e23ad72570665c2f133d81b77a794489f250d73fe8395d9222c3144cd98`。

## RQ1_a4f5912d615b

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_a4f5912d615b) · 检查明细 [Checks-71.json](Checks-71.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5}。相关检查决定 {'self_delegation': 3, 'holder_own_transfer': 2, 'holder_issued_transfer_scope': 3, 'external_dependency': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.594 秒，模型等待 67.682 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 15 项。诊断 {'missing_claim_or_source_anchor': 3, 'unrelated_or_secondary_graph_pairs_deferred': 4, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `20f032e1132d85afde387f04250fd3552e10bd8c14bd22d617a549a86ba6c31e`，决定 SHA `c99023664b5bc92ebcb962013acba719ac1f665421d5a8c7027d379362854809`。

## RQ1_6cc3d30752da

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_6cc3d30752da) · 检查明细 [Checks-71.json](Checks-71.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 17, 'policy_missing': 7}。相关检查决定 {'external_dependency': 108, 'policy_missing': 29}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 59.546 秒，模型等待 60.889 秒，真实 solver 1 次，查询投影 12 项，动作记录含缓存 352 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 135, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `872fc18e5f6b567209f84c9e1135357ac086a59f8b4b4c4bab25e264518c8215`，决定 SHA `0b157879b6707f5d146b8bd94a86333f13b85b353b1755f1a10c048ba02988db`。

## RQ1_76fc25a4f6a8

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-10.md#rq1_76fc25a4f6a8) · 检查明细 [Checks-71.json](Checks-71.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:550:author:1 | NETM | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_2f9277a786934e5e28c0`，根位置 2867＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2867 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 95.419 秒，模型等待 46.916 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `1a38cdac133190e0bf7c4f412c5197acc2d1bb4db9738f7dc7e6f7644fe7f144`，决定 SHA `31a54acc462736c85a111088f67602e1d6a9baecd3b46856649817bb2c9846fc`。

## RQ1_63bf9791ac38

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-10.md#rq1_63bf9791ac38) · 检查明细 [Checks-71.json](Checks-71.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:551:author:1 | withdraw | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {'external_dependency': 72, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 23.422 秒，模型等待 65.474 秒，真实 solver 29 次，查询投影 36 项，动作记录含缓存 111 项。诊断 {'missing_claim_or_source_anchor': 3, 'unrelated_or_secondary_graph_pairs_deferred': 72, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ea6fd0f41063b1b13a72839452235973fb7ed9912945f2c73d9b65f60f7cea39`，决定 SHA `bf9f15436697a9aa24957df4047922102d9f707a93f04131356b470b47e70393`。

## RQ1_a34628cf71df

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-11.md#rq1_a34628cf71df) · 检查明细 [Checks-71.json](Checks-71.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 10, 'external_dependency': 1}。相关检查决定 {'policy_missing': 16, 'external_dependency': 3, 'holder_own_transfer': 2, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.042 秒，模型等待 49.063 秒，真实 solver 55 次，查询投影 56 项，动作记录含缓存 56 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 16, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ae03bc28445acae8d0c36923300b25f71440513e406bb905709aa327068b7bd3`，决定 SHA `71b7387f55354cdebda01d385e2157334f0e513e3364ba14c1821f76fa2339e6`。

## RQ1_9dfa887f7b8a

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_9dfa887f7b8a) · 检查明细 [Checks-71.json](Checks-71.json) [Checks-72.json](Checks-72.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 7, 'external_dependency': 26}。相关检查决定 {'nominee_acceptance': 18, 'external_dependency': 28, 'policy_missing': 11}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 55.036 秒，模型等待 25.104 秒，真实 solver 32 次，查询投影 62 项，动作记录含缓存 147 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 30, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `bb0f4febe09752d29b84b4a8db93e090d5276a003531bca44e376a28e5550e89`，决定 SHA `60c1573f064d2ad989e85f79002c3ac57429262607b05f1cca8a619bbf74aaad`。

## RQ1_c9b9d9ecb7bb

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-11.md#rq1_c9b9d9ecb7bb) · 检查明细 [Checks-72.json](Checks-72.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:554:author:1 | initEthMultiplicator | FN | FN | TP | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 11, 'external_dependency': 8}。相关检查决定 {'external_dependency': 16, 'policy_missing': 29, 'nominee_acceptance': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 36.537 秒，模型等待 102.923 秒，真实 solver 124 次，查询投影 155 项，动作记录含缓存 111 项。诊断 {'audit_card_check_kind': 1, 'audit_effect_unbound': 3, 'unknown_or_unshown_effect': 4, 'unrelated_or_secondary_graph_pairs_deferred': 39, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `9cd5f5f5fa44942f4ed44c25b661e21f7694eab2a80e22e08c12f3f910cae8e0`，决定 SHA `fde9bf9587be66803824a7c7e75c93d94577784fe543a562d79118ce4e294ebd`。

## RQ1_b9012ed6ff89

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-11.md#rq1_b9012ed6ff89) · 检查明细 [Checks-72.json](Checks-72.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:555:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_5ec1deb1b6f046c147ba`，根位置 2226＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2226. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.746 秒，模型等待 38.920 秒，真实 solver 13 次，查询投影 14 项，动作记录含缓存 16 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `e5ab2f54ecd56025a095cd5c9280e69a0e24287a1ecef85224abbd65cf27e019`，决定 SHA `b52f2c4d27e5817840d5f3ede2be3051bc04bba6feb65b8e025dc852ec6a2667`。

## RQ1_27081006f7b5

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_27081006f7b5) · 检查明细 [Checks-72.json](Checks-72.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2, 'policy_missing': 1}。相关检查决定 {'policy_missing': 4, 'external_dependency': 6}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.562 秒，模型等待 55.905 秒，真实 solver 12 次，查询投影 13 项，动作记录含缓存 19 项。诊断 {'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 8, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `fd14916d59e0b4956b74ab63985200d5fb476829338d586ad7922a40475e15b8`，决定 SHA `8d854c7b4716dc80033f288ee049ad8afd290ba94761fffc067f3087481d10ba`。

## RQ1_baf57c0b58b1

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_baf57c0b58b1) · 检查明细 [Checks-72.json](Checks-72.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 5, 'external_dependency': 5}。相关检查决定 {'policy_missing': 9, 'external_dependency': 4, 'applicable_role_guard': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.628 秒，模型等待 43.379 秒，真实 solver 14 次，查询投影 28 项，动作记录含缓存 38 项。诊断 {'audit_card_issue_kind': 1, 'audit_source_scope_mismatch': 2, 'unrelated_or_secondary_graph_pairs_deferred': 12, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `17ff952fca2ed93aea81c53951f111a7d74cf2c3e8aa0ed8d6c8907626ca416c`，决定 SHA `f0ffdaa21e85cba1bb434e77ca922d492b78bc98da15597af0e2d7d84328dfb0`。

## RQ1_70dd6d38b9bb

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_70dd6d38b9bb) · 检查明细 [Checks-72.json](Checks-72.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 8, 'policy_missing': 2}。相关检查决定 {'external_dependency': 121, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 163.152 秒，模型等待 42.036 秒，真实 solver 8 次，查询投影 32 项，动作记录含缓存 370 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 111, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `f3e28ee818726ee3bdefda64ae88eb959479162a930e8e4390339b57e860394d`，决定 SHA `3ee796cebcaa2fd1a965a7eceea1fa0437cb40cf151a3b0dd2a4e6b79a56eb13`。

## RQ1_b7c513158cc0

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_b7c513158cc0) · 检查明细 [Checks-72.json](Checks-72.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 12, 'external_dependency': 12}。相关检查决定 {'applicable_role_guard': 3, 'external_dependency': 34, 'policy_missing': 69}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 50.484 秒，模型等待 18.363 秒，真实 solver 62 次，查询投影 64 项，动作记录含缓存 214 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 96, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `86be0faeeea2c61962bbbf8e4628d65202c3efa14946660c94f2a0a677fdb1a4`，决定 SHA `056891e2b61b9828d499f1863255ebc7dbfb3c1452142ab2f5e0f927826e425d`。

## RQ1_87c298bef07b

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_87c298bef07b) · 检查明细 [Checks-72.json](Checks-72.json) · 查询明细 [Queries-32.json](Queries-32.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 5, 'external_dependency': 7}。相关检查决定 {'applicable_role_guard': 2, 'external_dependency': 31, 'holder_own_transfer': 2, 'policy_missing': 8, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 41.192 秒，模型等待 33.233 秒，真实 solver 21 次，查询投影 22 项，动作记录含缓存 134 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 14, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `67ad14e4137752becc049a2377135211457ab6885b06f281be33bb066f8aad9e`，决定 SHA `da5013f8b32f55348522748cd63cf211008bf874c86f6f424bb626f42d0740f8`。

## RQ1_9c985fb01894

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_9c985fb01894) · 检查明细 [Checks-72.json](Checks-72.json) · 查询明细 [Queries-32.json](Queries-32.json) [Queries-33.json](Queries-33.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:561:S1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:561:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:561:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:561:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 5}。相关检查决定 {'policy_missing': 20, 'external_dependency': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.808 秒，模型等待 80.642 秒，真实 solver 80 次，查询投影 132 项，动作记录含缓存 50 项。诊断 {'audit_card_text': 1, 'audit_source_scope_mismatch': 3, 'unrelated_or_secondary_graph_pairs_deferred': 18, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `2643cbdd0c87eecb43b7aab013d66b54ebce6d3cf4f087aa955350119079b0ea`，决定 SHA `996f6f2205401e30ea77a41fa8c5b3fa1be11e20490fb8f31bbbb1b5ebc705ce`。

## RQ1_a47200b36eb7

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-11.md#rq1_a47200b36eb7) · 检查明细 [Checks-72.json](Checks-72.json) · 查询明细 [Queries-33.json](Queries-33.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:562:original:1 | Vault | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |
| D2:562:original:2 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 2}。相关检查决定 {'policy_missing': 5, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.880 秒，模型等待 65.743 秒，真实 solver 23 次，查询投影 36 项，动作记录含缓存 16 项。诊断 {'unknown_or_unshown_effect': 2, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `7e509860060db2d7a848636c6bae02cf23141d93ddf14d1c61425e59dcd46da7`，决定 SHA `feeed64632de21f10d5fa73a74c427cdc41bb8e4b582b61490892af50e4ce1ff`。

## RQ1_ceb63e679a01

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_ceb63e679a01) · 检查明细 [Checks-72.json](Checks-72.json) · 查询明细 [Queries-33.json](Queries-33.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4, 'policy_missing': 3}。相关检查决定 {'policy_missing': 9, 'external_dependency': 14}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.965 秒，模型等待 24.990 秒，真实 solver 15 次，查询投影 21 项，动作记录含缓存 46 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 21, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `d4010e5d05c034216fe6be550b2e3686524e0a25be971830e6f5510057bbc88b`，决定 SHA `bdde549197d4ec4d5cd2fa03a800fcbb2baf9cc510cf50ff39eb0671b54d5a61`。

## RQ1_85a74cdc030d

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-11.md#rq1_85a74cdc030d) · 检查明细 [Checks-72.json](Checks-72.json) [Checks-73.json](Checks-73.json) · 查询明细 [Queries-33.json](Queries-33.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:564:author:1 | DynamicPyramid | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_d24ec8aea5bbfd873a72`，根位置 324＋20，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 324 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E149

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 137.130 秒，模型等待 37.427 秒，真实 solver 26 次，查询投影 27 项，动作记录含缓存 161 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 146, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `8c67c9d51ab713c0ec25068d61fc76113ca9d213d6eefdfef81659868e196cc2`，决定 SHA `f0e61507575aeea250c693d15ec5f61aeb8b868f871b7cc0fdbec5d1372faf5d`。

## RQ1_81d27b74b2b8

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_81d27b74b2b8) · 检查明细 [Checks-73.json](Checks-73.json) · 查询明细 [Queries-33.json](Queries-33.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:565:author:1 | ownerOf | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 7, 'external_dependency': 1}。相关检查决定 {'policy_missing': 27, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.799 秒，模型等待 64.958 秒，真实 solver 26 次，查询投影 26 项，动作记录含缓存 53 项。诊断 {'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 25, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `c3871c7e83bae0aae3a8ab1cc0409c1463c47c2f7055a9f4ff8229703e5f3ad1`，决定 SHA `12541206b8f390642491f9d9406727375c857c4c7782e5fc82c7b059e5aaa724`。

## RQ1_306aa53f1e15

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-11.md#rq1_306aa53f1e15) · 检查明细 [Checks-73.json](Checks-73.json) · 查询明细 [Queries-33.json](Queries-33.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:566:author:1 | SelfDesctruction | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_974fe7788b1dbf2e12f5`，根位置 3533＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 3533 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E15, E47

发现 `finding_ae5023310197d555862d`，根位置 3533＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 3533 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E35, E9

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.392 秒，模型等待 72.708 秒，真实 solver 49 次，查询投影 54 项，动作记录含缓存 47 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 12, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `852b39862d38e77eb09e20cebb0b63c9f2d0937443237952a43e279747a66b08`，决定 SHA `59fb513cbe1e1ef5fa0f561de028ddc1c6e6d57ccc84c9f7917ddb7a0e3a9188`。

## RQ1_934ccafdf988

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-11.md#rq1_934ccafdf988) · 检查明细 [Checks-73.json](Checks-73.json) · 查询明细 [Queries-33.json](Queries-33.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:567:S1 | mortal | TP | TP | FN | TP | matched |
| D2:567:S2 | thing | FN | FN | FN | FN | no_aligned_inspection_in_obligations |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_4621bba3609d2f6fa450`，根位置 76＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 76. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E4

发现 `finding_6f745dac73f26d321419`，根位置 76＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 76. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.565 秒，模型等待 69.878 秒，真实 solver 15 次，查询投影 20 项，动作记录含缓存 17 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'no_locatable_source': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ba4fe1c7d27789a194a3375838186f1c8f3cac14ef09dfc83a7296bb75e5399a`，决定 SHA `9782bdcd70cf3119355919ff64144c0d5aba7d4981699fb27cbc977b83e1c959`。

## RQ1_b22b383bba2b

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_b22b383bba2b) · 检查明细 [Checks-73.json](Checks-73.json) · 查询明细 [Queries-33.json](Queries-33.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 45, 'external_dependency': 15}。相关检查决定 {'external_dependency': 152, 'policy_missing': 109, 'applicable_role_guard': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 260.911 秒，模型等待 41.549 秒，真实 solver 102 次，查询投影 393 项，动作记录含缓存 763 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 248, 'noncached_action_limit': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `76c757fa46d17c5c7e42e1269ad55c332fae5b3839194f02109614a664723581`，决定 SHA `3cde876bc64f2817f5b54088be25586b32a49f980e4070c16b7e5e8a6ed03140`。

## RQ1_5a32d57754dd

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-11.md#rq1_5a32d57754dd) · 检查明细 [Checks-73.json](Checks-73.json) · 查询明细 [Queries-33.json](Queries-33.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:569:author:1 | ENTS | TP | FN | FN | TP | matched |

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_1a2b9acf384b378bcf61`，根位置 2610＋134，依据 `program_support`。At ENTS(), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification. 证据 E1, E127

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 27.176 秒，模型等待 17.505 秒，真实 solver 92 次，查询投影 122 项，动作记录含缓存 150 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `d1ef9c015bd449d24a7b05ee1fa7b72ab28097bbe65ec852d0548a06f616c959`，决定 SHA `5fc81046e209d57d78381be013631dcdb34a12ed76931c25e9a71280ac34bac6`。

## RQ1_f829e1448dd4

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-11.md#rq1_f829e1448dd4) · 检查明细 [Checks-73.json](Checks-73.json) · 查询明细 [Queries-33.json](Queries-33.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5, 'policy_missing': 3}。相关检查决定 {'policy_missing': 5, 'holder_own_transfer': 2, 'external_dependency': 12}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.095 秒，模型等待 26.987 秒，真实 solver 16 次，查询投影 35 项，动作记录含缓存 59 项。诊断 {'unbound_or_inapplicable_seed': 1, 'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 14, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `f7c3daafb11e3600c2aae7e25497fc27ec0a3233bb2f23471364e98bda31bd6a`，决定 SHA `b4734053f789bbe066fa09edb8764c574ad1d2ffeed0dd7dcabdbb3355f8f8c5`。
