# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_7cead5e1648c

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_7cead5e1648c) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:349:author:1 | AAC | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_f63eced04f616313c14c`，根位置 1651＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1651 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E4

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.686 秒，模型等待 27.503 秒，真实 solver 15 次，查询投影 17 项，动作记录含缓存 11 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `5729a7154ec71e34c047897b94de6833749a0a04c7c014d54dc495d43d006b5e`，决定 SHA `a454a3453c40eccf31ef5fcfe549a258cdcf65df162dcbbb6dd35abf83ba7188`。

## RQ1_cafc626080f8

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_cafc626080f8) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 报警

发现 `finding_195aa7b46be1329474d0`，根位置 7901＋25，依据 `program_support`。At setEtherPrice(uint256), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification. 证据 E16, E46, E78

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.879 秒，模型等待 65.190 秒，真实 solver 42 次，查询投影 57 项，动作记录含缓存 67 项。诊断 {'missing_claim_or_source_anchor': 2, 'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 21, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `e43a4af0b81b1068d44a8de082fb12bda1c82ad56bd65ad3ec614dd5a54d0161`，决定 SHA `e36badd98bb6360e2f54956dc72effdcb9610092de0c27176c3a28c21858c6d2`。

## RQ1_40c40e8002d5

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-07.md#rq1_40c40e8002d5) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:351:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_31268b7a2b0bf87a8231`，根位置 2217＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2217. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.388 秒，模型等待 30.209 秒，真实 solver 13 次，查询投影 14 项，动作记录含缓存 16 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `7112316e0b5c0dc14da5336ff8d6e2f859902993630298d012838d74c3214c10`，决定 SHA `11567efb9754953638403c4ed199f1c7ad9f758dc1a783b7e545a7775201a8ff`。

## RQ1_5fc26434af0d

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_5fc26434af0d) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 1}。相关检查决定 {'applicable_role_guard': 1, 'policy_missing': 14, 'external_dependency': 3, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.349 秒，模型等待 49.575 秒，真实 solver 43 次，查询投影 44 项，动作记录含缓存 53 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 16, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `1890ada718ee9e57cf747718abe9963fe628951dd701a6af3dc0c7e661e7571d`，决定 SHA `5c5aa074fcdf10b4ee3d89d8123a79465335a672c271631399686c7168cc4e79`。

## RQ1_a33a6b930c24

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_a33a6b930c24) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 6}。相关检查决定 {'policy_missing': 13, 'external_dependency': 34}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 29.242 秒，模型等待 32.572 秒，真实 solver 9 次，查询投影 18 项，动作记录含缓存 136 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 44, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `37a8dbda238d886959ae42606a3bc017cada4c532046a08db3a5bf8cf0d7e695`，决定 SHA `a166c54fe8d6f495bdf357e4b4f45570a641a8483bbaa35f6ae55e6df884a3fb`。

## RQ1_62f32beb7a0a

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_62f32beb7a0a) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:354:author:1 | Owned2 | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_147182e87d0293915d1c`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E18

发现 `finding_f1f36e04a26587b534cf`，根位置 1508＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1508 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E24

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.304 秒，模型等待 55.724 秒，真实 solver 11 次，查询投影 22 项，动作记录含缓存 24 项。诊断 {'no_locatable_source': 4, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `a8d057b65054420e63458ab90e67d96dd0e749486561e9e7c6e649b75d531a7e`，决定 SHA `0d5d18b3d818b7a7990ca83b526aef422b51ff86419e06111c2722b1b23f92b1`。

## RQ1_0778e0711de1

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_0778e0711de1) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 5}。相关检查决定 {'policy_missing': 21, 'scope_missing': 1, 'external_dependency': 69, 'holder_issued_transfer_scope': 3, 'applicable_role_guard': 1, 'self_delegation': 1, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 87.207 秒，模型等待 53.253 秒，真实 solver 16 次，查询投影 25 项，动作记录含缓存 341 项。诊断 {'audit_card_issue_kind': 1, 'unrelated_or_secondary_graph_pairs_deferred': 89, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `ebf4b1656ecb1cbb864f8050a2f8d6781256b22c37e85931a41d1121d6feace6`，决定 SHA `4c6cd9bd5bb45f4557e98cd4dbacbca8647a475bfe7cd7be66a13b7b0734c313`。

## RQ1_eb805b6652eb

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_eb805b6652eb) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:356:author:1 | owned | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_f3eec71ce0de6e3c82d5`，根位置 748＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 748 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E15, E4

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.347 秒，模型等待 67.567 秒，真实 solver 11 次，查询投影 14 项，动作记录含缓存 16 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 6, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `8367e067f3947333f5098a25244e61117523f731191638c6e77aa98df248b0d8`，决定 SHA `d0b9a9fa8608dcfb5930c49c82425d4645d84ac8d94ce402b4300374aab88630`。

## RQ1_e5c5b93a7049

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-07.md#rq1_e5c5b93a7049) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:357:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_053b10ca4cd596922c19`，根位置 2233＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2233. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.366 秒，模型等待 41.378 秒，真实 solver 13 次，查询投影 14 项，动作记录含缓存 16 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `8521efffd904ab01e0508b1f90d0863683f20a01f88637f5b6541cb5b377f211`，决定 SHA `b4a9c97eff2f7dc4d4d29b52311ac6855cd9075adbbe8f072dbd2d2be0112409`。

## RQ1_d3126c5cf5fe

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_d3126c5cf5fe) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 6}。相关检查决定 {'external_dependency': 90, 'policy_missing': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 69.458 秒，模型等待 89.310 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 153 项。诊断 {'audit_card_text': 1, 'unrelated_or_secondary_graph_pairs_deferred': 93, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `2a407d87df79144c6b7caf6e6936d892cdb77d2e161a46babda312e59287f343`，决定 SHA `782ee2dd74ad814b4d852e91ae4554ab221cd28fc1b255cbfb196f4605e294fc`。

## RQ1_34ab8e0115aa

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_34ab8e0115aa) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:359:S1 | PonziTokenV3 | FN | FN | FN | FN | no_aligned_inspection_in_obligations |
| D2:359:S2 | destroy | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 13, 'policy_missing': 1}。相关检查决定 {'policy_missing': 1, 'external_dependency': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 17.624 秒，模型等待 67.602 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 10 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 4, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `a8919efadf505be2dac8fc4c71c5ce273cdba707f048831e697c67480032586e`，决定 SHA `717d64e1f1eb2bccb9cf183ad5d541ebee6549ec02922cb5fc4dbe94b4973a1d`。

## RQ1_31450a049444

任务 AC，评价类别 AC。当前未知，BG 技术失败。

[实际输入](InputSource-07.md#rq1_31450a049444) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:360:original:1 | fin | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:360:original:2 | pay | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 1}。相关检查决定 {'policy_missing': 1, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.237 秒，模型等待 36.690 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `d6db37f5e77f4304cf5efee284d741e008dfe67c175aab164d74417ea537c704`，决定 SHA `68de34fd5a5ae1451e253e64af8e445cb655e413579a82fad2f1137e05dfcb1f`。

## RQ1_51ce031f9b54

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_51ce031f9b54) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {'external_dependency': 11}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.312 秒，模型等待 69.411 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 35 项。诊断 {'no_locatable_source': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `150d3db12e22f9781b67d90c91d38c7b1d8040088af7b53bfe10aaaf9f46a7c4`，决定 SHA `9675a008cb663a4bdc6a786fea74ec923526b1d07404e4b73579709afa4d706d`。

## RQ1_a821598f1700

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_a821598f1700) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:362:author:1 | setupStackDepthLib | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 19, 'policy_missing': 2}。相关检查决定 {'external_dependency': 12, 'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.516 秒，模型等待 65.452 秒，真实 solver 2 次，查询投影 32 项，动作记录含缓存 50 项。诊断 {'invalid_semantic_row': 2, 'no_locatable_source': 6, 'unrelated_or_secondary_graph_pairs_deferred': 4, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `507293d88b0262b4b26ef03ccccbbfd2e60927fddee962fdd461984376ceaa2a`，决定 SHA `7e75bdc86f6f1d4a5de240168086e9de93c80a15b4f4b023d757ecf345400af4`。

## RQ1_bb9523a9c423

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_bb9523a9c423) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:364:author:1 | reward | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 2, 'external_dependency': 2}。相关检查决定 {'policy_missing': 10, 'external_dependency': 19}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.922 秒，模型等待 31.606 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 58 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 24}。

最终报告 SHA `37ddd7b52f1c31cb8cc2b0cda4c426a99fe78a64665916146c25cb5f5208232b`，决定 SHA `5b37cd4ef05dba8013c850d3adb22b05095da7a918c2c4aa5adc8278741a6489`。

## RQ1_ee72ed73f72a

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_ee72ed73f72a) · 检查明细 [Checks-47.json](Checks-47.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:365:author:1 | changeOwner | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_539783031aeb6328ffd4`，根位置 316＋14，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 316 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E4

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.303 秒，模型等待 32.103 秒，真实 solver 14 次，查询投影 15 项，动作记录含缓存 8 项。诊断 {'unbound_or_inapplicable_seed': 1, 'no_locatable_source': 3, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `6a60db4e45e6d32d3a35e766de7919d4d861285a8d8219ad4b75b2c97a1a5cc4`，决定 SHA `a493d18753d76878f120cfc179d9fc5bae4d737f725c1f8e10b2d5655fed67c0`。

## RQ1_75175e6e6a1d

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_75175e6e6a1d) · 检查明细 [Checks-47.json](Checks-47.json) [Checks-48.json](Checks-48.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:366:author:1 | MYSLF | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_5212bb6dab10cdbf7f39`，根位置 2833＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2833 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 88.318 秒，模型等待 65.479 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5296fa8a18fe1a4960e9bf4616b87e48a0814a741ddfb7cad631f67efbb43016`，决定 SHA `2659bff5f93488b972851bbd3cc94ffe0bbc7b09fb365b0d1dd9dd36cdbf0e60`。

## RQ1_08678502716e

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_08678502716e) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 14, 'policy_missing': 1}。相关检查决定 {'policy_missing': 10, 'external_dependency': 16}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.765 秒，模型等待 90.286 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 65 项。诊断 {'audit_effect_unbound': 2, 'shared_declaration_in_distinct_applied_contexts': 3, 'unknown_or_unshown_effect': 2, 'unrelated_or_secondary_graph_pairs_deferred': 14, 'semantic_answer_outside_sent_scope': 1}。

最终报告 SHA `010251dec886b3869261ede8ca3e0a67e3a2571c2e892f4481b4b76be1431590`，决定 SHA `61ac195922bc629a8d8624c78a6b8f0c2ab6db6d61ff7532af1f7555bbbe270d`。

## RQ1_dde75f5bf9cf

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_dde75f5bf9cf) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:368:S1 | setImporter | TP | TP | TP | TP | matched |
| D2:368:S2 | setExporter | TP | TP | TP | TP | matched |
| D2:368:S3 | setImporterBank | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_40c495d33a680be1d4a7`，根位置 1674＋21，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1674 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E44

发现 `finding_33f8de7ff594ab756aab`，根位置 1731＋27，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1731 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E56

发现 `finding_07f2d227bc3a1c835e45`，根位置 1621＋21，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1621 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E37

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.465 秒，模型等待 44.006 秒，真实 solver 89 次，查询投影 114 项，动作记录含缓存 83 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 25, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `f62adc66285af1e37b2ae4110a63a2aa38c13e7870a7a76a5985d98c6aa3b8e4`，决定 SHA `3062f1664a88b8215d2302d241936031d8eff6bbbc7daa2ab27cb0450233ab63`。

## RQ1_1efb88fb92f0

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_1efb88fb92f0) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:369:author:1 | close_bank | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 5, 'external_dependency': 1}。相关检查决定 {'external_dependency': 16, 'policy_missing': 17}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.468 秒，模型等待 90.700 秒，真实 solver 24 次，查询投影 24 项，动作记录含缓存 53 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 29, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `285e6b09a55896080757232dcf1f2006935fd16071b52ede7c4ce3be29adff94`，决定 SHA `2dadc154c45beaa81d4a050f26f2bb8a2f5874cd57ee98c35e63e09ec843fa19`。

## RQ1_a949fc0b1029

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_a949fc0b1029) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 7, 'external_dependency': 4}。相关检查决定 {'applicable_role_guard': 3, 'policy_missing': 11, 'external_dependency': 24, 'source_context_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.603 秒，模型等待 81.259 秒，真实 solver 6 次，查询投影 14 项，动作记录含缓存 104 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 22, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `3949d2bc5101df5202d5d07bdcfdc7ced9b2ca82421c347b6a954018f7c868df`，决定 SHA `a72ae1b66e3cb06089b7183f07daa2c80eaebfc2528d65dd4bc2535c3243dafd`。

## RQ1_261dcad8364d

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_261dcad8364d) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1, 'not_reviewed': 1}。相关检查决定 {'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.136 秒，模型等待 87.402 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `6807a4646a96753da5cab07aaf7ab813fa705c0ce2c9b760b1d76b8da5f697c1`，决定 SHA `2d481567df63dbd577929c458643872e207b64d665903b3a715e470caa8a8aa2`。

## RQ1_61e998763707

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_61e998763707) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'external_dependency': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.325 秒，模型等待 23.002 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 10 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `5d384f344d442084386cf30e31b6dcc366ffea60d1b5170bf03b023137f01674`，决定 SHA `560bf70f63d8b27c5ab196a5560a534c0fc948f9a14965c2135e6ab9fa002cf5`。

## RQ1_acfda1a5a3f4

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_acfda1a5a3f4) · 检查明细 [Checks-48.json](Checks-48.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:373:author:1 | owned | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_aa2e509302b050d85c02`，根位置 106＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 106 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E8

发现 `finding_4ef5e7bfcaa2c37a5279`，根位置 106＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 106 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E10, E9

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.020 秒，模型等待 42.288 秒，真实 solver 87 次，查询投影 112 项，动作记录含缓存 102 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 2, 'unrelated_or_secondary_graph_pairs_deferred': 33, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `b8d50d4c5f65f4c92b88dfb138602b6bb1634114be3cea419c9c8259a8a858a4`，决定 SHA `7d25da90914f13c6f9e42554620a9c0c224439aa6460ad3545c79d25f1055f93`。
