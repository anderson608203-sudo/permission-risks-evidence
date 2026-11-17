# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_80d362cce2a6

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-06.md#rq1_80d362cce2a6) · 检查明细 [Checks-35.json](Checks-35.json) · 查询明细 [Queries-15.json](Queries-15.json) [Queries-16.json](Queries-16.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:275:author:1 | owned | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_d1c72c45b6a21eed658a`，根位置 99＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E118

发现 `finding_19b34776c68b9879caad`，根位置 99＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E170, E2

发现 `finding_cbedd711394ce0be35cd`，根位置 99＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E176, E3

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 181.231 秒，模型等待 26.442 秒，真实 solver 74 次，查询投影 97 项，动作记录含缓存 340 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 109, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `587fcf6ed40cb65015220d23e5e1db2fd816d5b6cdf7ac19393537c05de69f67`，决定 SHA `a8620449dc24809f36cd3707ebacbb63c6d8af2ee801dadc0c2831fc29c4f428`。

## RQ1_3843030989b1

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_3843030989b1) · 检查明细 [Checks-35.json](Checks-35.json) · 查询明细 [Queries-16.json](Queries-16.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 2}。相关检查决定 {'external_dependency': 64, 'policy_missing': 33}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 77.338 秒，模型等待 63.670 秒，真实 solver 6 次，查询投影 36 项，动作记录含缓存 350 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 97, 'noncached_action_limit': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `fb024dd3ba311d390d750c11d41fe8eecc8bce7d00be0a3dca093de2a320ccf6`，决定 SHA `5dec0e5998fd1181cc1dab49572f3f71fd929a982b50b3891f526b1095230a09`。

## RQ1_451d90a0c512

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-06.md#rq1_451d90a0c512) · 检查明细 [Checks-35.json](Checks-35.json) · 查询明细 [Queries-16.json](Queries-16.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:277:author:1 | KingOfTheEthill | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_4e07e3e0d5b9171181e6`，根位置 1471＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 1471 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E20

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.292 秒，模型等待 47.145 秒，真实 solver 17 次，查询投影 21 项，动作记录含缓存 52 项。诊断 {'audit_card_text': 1, 'unrelated_or_secondary_graph_pairs_deferred': 16, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `5556c7d702678b0a82066f7fa94e594ae801229c8ddc2cec0a6617df14403298`，决定 SHA `3d07011d3c131048774ed985d93a5662901b3a8310ec4aa7abb6a467b38fca7e`。

## RQ1_faed8e9e25ab

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_faed8e9e25ab) · 检查明细 [Checks-35.json](Checks-35.json) [Checks-36.json](Checks-36.json) [Checks-37.json](Checks-37.json) [Checks-38.json](Checks-38.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json) [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 9, 'policy_missing': 9}。相关检查决定 {'policy_missing': 505, 'external_dependency': 782}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 1035.333 秒，模型等待 98.330 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 14 项。诊断 {'no_locatable_source': 1, 'yield_to_source_bound_semantic_review': 1, 'semantic_answer_outside_sent_scope': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `9ba4fcb183cdeee07bf508e8050cb60c0ea0ad9f627b308916311017db3245cd`，决定 SHA `1ffdd4c6f47889494b2ef572dd8cc7e29a8513c845f5edcb56ec2d2008ad2a00`。

## RQ1_9978e161eb68

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-06.md#rq1_9978e161eb68) · 检查明细 [Checks-38.json](Checks-38.json) · 查询明细 [Queries-16.json](Queries-16.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:279:author:1 | CCN | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_55c3e3d8e8b63c1fbc07`，根位置 2869＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2869 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 94.032 秒，模型等待 36.637 秒，真实 solver 39 次，查询投影 58 项，动作记录含缓存 304 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 101, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `809f8ffbb98f225b3e2365b9a2e7f6e5a1c91dc0761ddfa6b4e121d1503b597c`，决定 SHA `43a177419375760c253adf749dfe68d67013449e164f300c19769b3e76ca5fb8`。

## RQ1_f82d8856631a

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_f82d8856631a) · 检查明细 [Checks-38.json](Checks-38.json) · 查询明细 [Queries-16.json](Queries-16.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:280:author:1 | HT | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'policy_missing': 34, 'external_dependency': 26, 'holder_own_transfer': 2, 'applicable_role_guard': 1, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 24.235 秒，模型等待 41.266 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 145 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 58, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `43c333e98dc6381357e38534548352b123a8f33bf811be574ee70110bc6ed756`，决定 SHA `ea5e1a0267cb3384b43746e6081cf2211ac909a8d2b9271ff88744c1f621f024`。

## RQ1_6bc986b54c91

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_6bc986b54c91) · 检查明细 [Checks-38.json](Checks-38.json) · 查询明细 [Queries-16.json](Queries-16.json) [Queries-17.json](Queries-17.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:281:author:1 | init | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 8, 'policy_missing': 11}。相关检查决定 {'policy_missing': 28, 'external_dependency': 24, 'holder_issued_transfer_scope': 3, 'holder_own_transfer': 2, 'self_delegation': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 925.654 秒，模型等待 28.760 秒，真实 solver 2160 次，查询投影 1402 项，动作记录含缓存 140 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 52, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `3a0c42f868ed3831d1a8fb354f2fb90ce0695c024e703368a8010b817f4cfaab`，决定 SHA `f876f9510f93c08d919750d049f3942617181ebfb82a2ee78859ee27d7ac9ff1`。

## RQ1_ab71daf07a5e

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_ab71daf07a5e) · 检查明细 [Checks-38.json](Checks-38.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5, 'policy_missing': 1}。相关检查决定 {'policy_missing': 4, 'external_dependency': 66, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 45.268 秒，模型等待 49.043 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 122 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 69, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `4f0df84915b989277e70b5477f9bf333902f828e81075c4fb0b4327fdab91201`，决定 SHA `a822aeadd4c3e571076be849209ae8c7e84d7a4e097c2d708ba6950f7c93b6d3`。

## RQ1_e7801f3e61cb

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_e7801f3e61cb) · 检查明细 [Checks-38.json](Checks-38.json) [Checks-39.json](Checks-39.json) · 查询明细 [Queries-17.json](Queries-17.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 34, 'external_dependency': 40}。相关检查决定 {'external_dependency': 100, 'policy_missing': 118, 'nominee_acceptance': 15, 'applicable_role_guard': 6}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 215.084 秒，模型等待 32.025 秒，真实 solver 39 次，查询投影 57 项，动作记录含缓存 304 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 73, 'noncached_action_limit': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `d3e4bb7c68a4ff417cfe74d78809f30af387570c82450d87650e4efabbf8e03d`，决定 SHA `995996fa7259e77efad5bf148b8b6f11bfcda0471f499fdff10ffbee8f6a5c19`。

## RQ1_7cc0c88effbf

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_7cc0c88effbf) · 检查明细 [Checks-39.json](Checks-39.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'external_dependency': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.862 秒，模型等待 24.223 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 12 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 4}。

最终报告 SHA `a9a215fdd38dc56513abfd64104056e02a624dee8118d5f7be4e196964a2d808`，决定 SHA `c7892eb9ce1a797b4ee571d67a1e7e221c72c0f0be15e2771a3b92098909fa20`。

## RQ1_8aa2c298e5c8

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_8aa2c298e5c8) · 检查明细 [Checks-39.json](Checks-39.json) · 查询明细 [Queries-17.json](Queries-17.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3, 'policy_missing': 1}。相关检查决定 {'external_dependency': 59, 'policy_missing': 34}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 107.866 秒，模型等待 78.517 秒，真实 solver 2 次，查询投影 9 项，动作记录含缓存 280 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 92, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `f41e1fda126fa1d2e999f5fb63ec6f901249621e3d25eb88ffa562aa05d14b05`，决定 SHA `3ce20e039bb59b6770d92fddb06cbb8174ec2608287918573185199489d85d96`。

## RQ1_b2a6c56c3cb6

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_b2a6c56c3cb6) · 检查明细 [Checks-39.json](Checks-39.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'not_reviewed': 1}。相关检查决定 {'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.206 秒，模型等待 24.095 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'no_locatable_source': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `2bb28ee3cf24217c985ae71b1f43be245ac1ab3d5aa0110acc394526ef23ec3a`，决定 SHA `3335cd4235edc5e02458822388a6fd1fc6ea302437b098d0482431b3c6a3fed6`。

## RQ1_d167f1c5e7b4

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_d167f1c5e7b4) · 检查明细 [Checks-39.json](Checks-39.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 4}。相关检查决定 {'external_dependency': 21, 'policy_missing': 11, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.614 秒，模型等待 62.808 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 107 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 24, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `30f1632d13a1071a0d185c183e5da810cebf58680c25432da09cdebc5b263727`，决定 SHA `f728731bbd7bebd49f1d874c7c8d966a7cf2c2e5dfb86278138ed83a541a0a16`。

## RQ1_3d9158f4b24c

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-06.md#rq1_3d9158f4b24c) · 检查明细 [Checks-39.json](Checks-39.json) · 查询明细 [Queries-17.json](Queries-17.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:288:author:1 | Constrctor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_84e14655c4964236e892`，根位置 806＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 806 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E50

发现 `finding_9a3bd9ea54024254ca55`，根位置 806＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 806 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E59

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 15.555 秒，模型等待 68.955 秒，真实 solver 70 次，查询投影 94 项，动作记录含缓存 111 项。诊断 {'missing_claim_or_source_anchor': 2, 'unrelated_or_secondary_graph_pairs_deferred': 37, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `fb135946a37c7501bfcb318247325d741ba03660b584585a9bfccf9fed3e4a2c`，决定 SHA `aee0664993498ac70890deeaa5b1ac4b97dc22d99534061398ce7100c5b3aef5`。

## RQ1_172ee9b9a6da

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_172ee9b9a6da) · 检查明细 [Checks-39.json](Checks-39.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 1}。相关检查决定 {'external_dependency': 1, 'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.141 秒，模型等待 48.011 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `5d4f9a514c8b4960014e63db715af79177c2bc084da11fac7ce9f3aac9783b2f`，决定 SHA `186fe82785ba454af97e209748fb26c0bfd0ba3f3cf17e7bedd3b6f4338ab617`。

## RQ1_9f051c86ed67

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-06.md#rq1_9f051c86ed67) · 检查明细 [Checks-39.json](Checks-39.json) · 查询明细 [Queries-17.json](Queries-17.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:290:S1 | task | TP | TP | FN | TP | matched |
| D2:290:S2 | withdrawETH | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_eac644d90793c3e94c81`，根位置 995＋22，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 995. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.964 秒，模型等待 32.228 秒，真实 solver 20 次，查询投影 22 项，动作记录含缓存 17 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 3, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `cb90e0a6e9adf90e50bbf3295ba3e87b1d80f608ccdc847b5b43a43f4c2a27f1`，决定 SHA `bdaf80ee829534ce8cdf9bc292f47125398b1934ecb4c3c144d2f1728222bfe5`。

## RQ1_60f513c5151e

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_60f513c5151e) · 检查明细 [Checks-39.json](Checks-39.json) [Checks-40.json](Checks-40.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 3, 'external_dependency': 2}。相关检查决定 {'external_dependency': 325, 'applicable_role_guard': 1, 'policy_missing': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 502.830 秒，模型等待 81.443 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 501 项。诊断 {'audit_card_text': 1, 'audit_effect_unbound': 1, 'unrelated_or_secondary_graph_pairs_deferred': 325, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `9c0a4e9234f0ba74f72f8a17f2a7c8626633fa2069a3249605bdf4949b4f3871`，决定 SHA `f031ee3d2cda234f2af79833fa059ff64001abc3e8a5e8e27091ab69ad788b61`。

## RQ1_18f20020e22b

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_18f20020e22b) · 检查明细 [Checks-40.json](Checks-40.json) · 查询明细 [Queries-17.json](Queries-17.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:292:author:1 | TeamTokensAllocation | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 4}。相关检查决定 {'external_dependency': 26, 'policy_missing': 34, 'holder_own_transfer': 2, 'self_delegation': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 24.303 秒，模型等待 41.096 秒，真实 solver 62 次，查询投影 68 项，动作记录含缓存 149 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 60, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `b9434ebc9e4441c25e5843b129a1cf42189dee75a7beb54b46e188ab2e3ba71c`，决定 SHA `f5b998850940e99565345c6c1e714cc1cfa7cf4068ff983817aaa5c27e82ac56`。

## RQ1_770b64940b4d

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_770b64940b4d) · 检查明细 [Checks-40.json](Checks-40.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:293:author:1 | withdrawTokens | FN | FN | FN | FN | no_listed_obligation_at_reference |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {'external_dependency': 6}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.291 秒，模型等待 68.679 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 18 项。诊断 {'no_locatable_source': 4}。

最终报告 SHA `d54d0d42c1228e542ea5464b8d83d48e86216946e4498d72f9997cc5a629c15d`，决定 SHA `6bda8861ad2460d78910466599ffcdb942d2e5d5bfebf504cbf1d1a115c02499`。

## RQ1_e68715d35210

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_e68715d35210) · 检查明细 [Checks-40.json](Checks-40.json) · 查询明细 [Queries-17.json](Queries-17.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 3, 'external_dependency': 1}。相关检查决定 {'policy_missing': 4, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.513 秒，模型等待 28.743 秒，真实 solver 4 次，查询投影 6 项，动作记录含缓存 10 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `1ed4276c39cce57adee7fe943d9e3f72cebe64e07b6e873ff849391aef46fac4`，决定 SHA `dd34e47bdad7f16059a4027b7be26b33925e77839cbd0a12936fde2d45f42869`。

## RQ1_00364c05ae79

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_00364c05ae79) · 检查明细 [Checks-40.json](Checks-40.json) · 查询明细 [Queries-17.json](Queries-17.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:295:author:1 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 3, 'external_dependency': 4}。相关检查决定 {'scope_missing': 1, 'applicable_role_guard': 1, 'external_dependency': 12, 'policy_missing': 5, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.515 秒，模型等待 71.651 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 50 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 11, 'semantic_answer_outside_sent_scope': 1}。

最终报告 SHA `af628d74b176ec348d16385838a632e0f5920dc7fa5dc726379933bc3ff87bbc`，决定 SHA `20a45a146d8fab974db88653afc6e5383472c526506378777ed3f71b131ab607`。

## RQ1_a9d497f162fb

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_a9d497f162fb) · 检查明细 [Checks-40.json](Checks-40.json) · 查询明细  · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {'external_dependency': 11, 'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 55.755 秒，模型等待 49.186 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 34 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 12, 'semantic_answer_outside_sent_scope': 1}。

最终报告 SHA `55b59d9ef819afbc3443d106ec58feecaaf832a2c39ffc7f42f2868a30673be1`，决定 SHA `df26b58634a3f631338056fa03939417b3b38a818b2e055dedc48ee698d7e994`。

## RQ1_28fd11561fa6

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_28fd11561fa6) · 检查明细 [Checks-40.json](Checks-40.json) · 查询明细 [Queries-17.json](Queries-17.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:297:author:1 | initialize | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'applicable_role_guard': 2, 'external_dependency': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.348 秒，模型等待 51.139 秒，真实 solver 1 次，查询投影 6 项，动作记录含缓存 9 项。诊断 {'no_locatable_source': 6, 'unrelated_or_secondary_graph_pairs_deferred': 2, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `af51b7df83aaafcf85107c7698d1e248038807686c534562521aacf937ace48b`，决定 SHA `101340f67287d36d1d5672729443cc8dbf18b6586abe9d929abbf54acc982ac2`。

## RQ1_81d27180159b

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-06.md#rq1_81d27180159b) · 检查明细 [Checks-40.json](Checks-40.json) · 查询明细 [Queries-17.json](Queries-17.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 11, 'policy_missing': 1}。相关检查决定 {'external_dependency': 102, 'policy_missing': 6}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 30.586 秒，模型等待 57.731 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 307 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 106, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c6b194dbb86c44ec109f9778e3a4d80f71324ff7a5fbc6055f4d728fcb7e7fcc`，决定 SHA `73189b56f1ade656ec9c2bbc0381bbb452797cf318c9061359218959373a6121`。
