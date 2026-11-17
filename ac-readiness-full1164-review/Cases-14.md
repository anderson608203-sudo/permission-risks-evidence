# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_032cdc396341

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_032cdc396341) · 检查明细 [Checks-44.json](Checks-44.json) · 查询明细 [Queries-19.json](Queries-19.json) · 服务回执索引 [Requests-01.json](Requests-01.json) [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 7, 'policy_missing': 1}。相关检查决定 {'external_dependency': 3, 'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.027 秒，模型等待 49.309 秒，真实 solver 1 次，查询投影 6 项，动作记录含缓存 12 项。诊断 {'missing_claim_or_source_anchor': 4, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `e98a8a42f2e6621012497c801202f85c89420bdf0b697bddc22eaf3396871748`，决定 SHA `5fe85abed57521dc41d48fdb6486631b11eabc0e0c8d29a800233be7e0ac0c26`。

## RQ1_3092779b88eb

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-07.md#rq1_3092779b88eb) · 检查明细 [Checks-44.json](Checks-44.json) · 查询明细 [Queries-19.json](Queries-19.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:326:author:1 | mintTo | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_952316dbd274e5d6509d`，根位置 2225＋23，依据 `unbacked_source_issuance`。The assessment concerns the policy governing the protected effect at source offset 2225. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms. 证据 E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.401 秒，模型等待 74.560 秒，真实 solver 13 次，查询投影 14 项，动作记录含缓存 16 项。诊断 {'explicit_effect_anchor_conflict': 5, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `682b31230373b8fd004a109825bee4f5c49621bd79268ab80d4ed40b9846e2b5`，决定 SHA `df9a827d7169313160cc825e79b86c444c89fc1d690f5f471b4de2cbfb796041`。

## RQ1_2ca53b535ccd

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_2ca53b535ccd) · 检查明细 [Checks-44.json](Checks-44.json) · 查询明细 [Queries-19.json](Queries-19.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:327:author:1 | initialize | TP | FN | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_4a6a80beca66c5342842`，根位置 840＋15，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 840 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E13, E152

发现 `finding_6c72aedc5a42c56e86a5`，根位置 840＋15，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 840 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E118, E7

发现 `finding_e15ff59785b5b9208b96`，根位置 840＋15，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 840 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E117, E5

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.153 秒，模型等待 43.586 秒，真实 solver 38 次，查询投影 86 项，动作记录含缓存 154 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 43, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `a285bed6a27d8cd18b480f9f170e8498059c445d0752f41fb23f2d403737f4f0`，决定 SHA `2f97680413899be6932274e168d3b25d561a55078d181696bbeadd95a808ce45`。

## RQ1_ca65e2d77908

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_ca65e2d77908) · 检查明细 [Checks-44.json](Checks-44.json) · 查询明细 [Queries-19.json](Queries-19.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:328:author:1 | Leg | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_ad440890ca8f2d44b25c`，根位置 2844＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2844 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E209

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 90.832 秒，模型等待 50.854 秒，真实 solver 38 次，查询投影 58 项，动作记录含缓存 303 项。诊断 {'audit_source_scope_mismatch': 3, 'unrelated_or_secondary_graph_pairs_deferred': 100, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `522220a78f4f0d19a8ad52df8d14d83a5c4961566e53f896d40510803bef1381`，决定 SHA `a9a37079e26d919d05243e93015968878ae76665347648ddba780037aaeffd5f`。

## RQ1_5e33b7b64e99

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_5e33b7b64e99) · 检查明细 [Checks-44.json](Checks-44.json) · 查询明细 [Queries-19.json](Queries-19.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 21, 'policy_missing': 24}。相关检查决定 {'external_dependency': 75, 'policy_missing': 61, 'applicable_role_guard': 18, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 121.042 秒，模型等待 33.861 秒，真实 solver 150 次，查询投影 246 项，动作记录含缓存 415 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 126, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `4b2c171c7b28f44adc7b065dc69c86b12b38c39bbba13743a84b4e186edb15f6`，决定 SHA `3dae8d64e5c76754396cd186bc7b236557af6a8b06da262f2976c393b5e18248`。

## RQ1_c453f88fd0ff

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_c453f88fd0ff) · 检查明细 [Checks-44.json](Checks-44.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:330:author:1 | Kill | FN | TP | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1}。相关检查决定 {'policy_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.244 秒，模型等待 23.062 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `29201ae8c013a1feb4f156c2e9befe34fffc295b91e296ba3b31d1d5fad373b1`，决定 SHA `4410c7222025ab2114dfdd8a8a12a092a92c14981b478739d50ac5a8722a3f8e`。

## RQ1_9dd80d8e49b0

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_9dd80d8e49b0) · 检查明细 [Checks-44.json](Checks-44.json) · 查询明细 [Queries-19.json](Queries-19.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3, 'policy_missing': 1}。相关检查决定 {'policy_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.736 秒，模型等待 14.640 秒，真实 solver 2 次，查询投影 3 项，动作记录含缓存 5 项。诊断 {}。

最终报告 SHA `d6f99378a6b9d320b59b3878b2f996f45fc89464c158b0eca5ab2e54813feb4c`，决定 SHA `f77f610e614567a4f8dc84c7c4d73fba4e8542b9f717738dc2f351674f3a646c`。

## RQ1_032ffa20eb40

任务 AC，评价类别 AC。当前未知，BG 技术失败。

[实际输入](InputSource-07.md#rq1_032ffa20eb40) · 检查明细 [Checks-44.json](Checks-44.json) · 查询明细 [Queries-19.json](Queries-19.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 9, 'external_dependency': 1}。相关检查决定 {'external_dependency': 75, 'applicable_role_guard': 1, 'holder_own_transfer': 4, 'policy_missing': 17, 'self_delegation': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 439.235 秒，模型等待 35.655 秒，真实 solver 44 次，查询投影 76 项，动作记录含缓存 319 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 92, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `1b4c5fc76e48b1458220d80082f2ca1198db84c1ba6c7ae76d49edc44c041f07`，决定 SHA `45a905753acf43fd6c943fd31b47215e4bb394e6083f499ab67528eb5ebf9f39`。

## RQ1_bd9ce34be5a6

任务 AC，评价类别 AC。当前报警，BG 未知。

[实际输入](InputSource-07.md#rq1_bd9ce34be5a6) · 检查明细 [Checks-44.json](Checks-44.json) · 查询明细 [Queries-19.json](Queries-19.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:333:author:1 | MyTestWallet7 | TP | TP | FN | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_a2d87a76027e0c9ba7ea`，根位置 110＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 110. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.808 秒，模型等待 26.969 秒，真实 solver 11 次，查询投影 13 项，动作记录含缓存 9 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `a6ac0de483af78fcc81de4f3a38e58e1bbf39c791832a47076cf77aee0ad34fb`，决定 SHA `7562ef1b5ee5278e5fe9610fc68f848c6f44daf70b8d4f03c44d5c39c9830d5d`。

## RQ1_679bfbe1c927

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_679bfbe1c927) · 检查明细 [Checks-44.json](Checks-44.json) · 查询明细 [Queries-19.json](Queries-19.json) [Queries-20.json](Queries-20.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:334:author:1 | Constructor | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_db7b25e67af7529cea09`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E54

发现 `finding_ec7f6001d5ac2d70bc9d`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E50

发现 `finding_df78f2f4cb13439ec862`，根位置 793＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 793 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E3, E58

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.241 秒，模型等待 70.017 秒，真实 solver 26 次，查询投影 66 项，动作记录含缓存 93 项。诊断 {'explicit_effect_anchor_conflict': 3, 'unrelated_or_secondary_graph_pairs_deferred': 30, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `1e76ae9bee69ba37f1a33d024e5d6074203a4457d4d279409db44d72756e9da1`，决定 SHA `791cd8597b19ee5a30194a05c6dd6b7d22fa02f9a6aa699f37d567828ac36ffe`。

## RQ1_0eca3d93c688

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_0eca3d93c688) · 检查明细 [Checks-44.json](Checks-44.json) [Checks-45.json](Checks-45.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1, 'policy_missing': 1}。相关检查决定 {'policy_missing': 1, 'external_dependency': 18}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.229 秒，模型等待 23.352 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 39 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 18}。

最终报告 SHA `01fad54ddd5ddc52905eb93487483e6a8a23f6fc81f6d3fd2aabe3097a8212c5`，决定 SHA `03184618ebff716125a78b8406601c8fbd14206b9ebb289e7bc1274334a90ddb`。

## RQ1_5c484e218f4b

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_5c484e218f4b) · 检查明细 [Checks-45.json](Checks-45.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 20, 'policy_missing': 2}。相关检查决定 {'external_dependency': 31, 'policy_missing': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 59.184 秒，模型等待 93.022 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 131 项。诊断 {'missing_claim_or_source_anchor': 2, 'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 31, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `530969111fe4e6eff979ee435187963048fa08fd197db46cf920a06931a1bd45`，决定 SHA `e75211552c6ed7a3bdd0a16e5e1bdbf05d80121dc53b709d1b065d41461c3533`。

## RQ1_9e7faad9335a

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_9e7faad9335a) · 检查明细 [Checks-45.json](Checks-45.json) · 查询明细 [Queries-20.json](Queries-20.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:337:S1 | transfer | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |
| D2:337:S2 | transferFrom | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 5}。相关检查决定 {'policy_missing': 64, 'holder_issued_transfer_scope': 3, 'holder_own_transfer': 2, 'applicable_role_guard': 1, 'self_delegation': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 83.952 秒，模型等待 40.254 秒，真实 solver 75 次，查询投影 86 项，动作记录含缓存 190 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 64, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `346c05226e72e9a42695c7579c32730b1f23cb2c8bb7852fbdb70ded15fa002d`，决定 SHA `81eb2b405d893dfadfeec10266c0273839f5767cf12f6b4b041f28cea47b2041`。

## RQ1_6c5de7dc129a

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_6c5de7dc129a) · 检查明细 [Checks-45.json](Checks-45.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:338:author:1 | delegate_2x | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2, 'not_reviewed': 1}。相关检查决定 {'external_dependency': 3, 'scope_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.336 秒，模型等待 16.612 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 8 项。诊断 {}。

最终报告 SHA `27a05ccc3a22412e009b2ab5254c8a8cce1afdfff689464d6887143975164653`，决定 SHA `44224e6f576653a1a9e14d1067f6f9ca3eebe3995085b18b2aa770703158fc8f`。

## RQ1_52d7ed57b3c6

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_52d7ed57b3c6) · 检查明细 [Checks-45.json](Checks-45.json) · 查询明细 [Queries-20.json](Queries-20.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 4, 'external_dependency': 5}。相关检查决定 {'external_dependency': 69, 'policy_missing': 22, 'applicable_role_guard': 1, 'holder_issued_transfer_scope': 3, 'self_delegation': 1, 'holder_own_transfer': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 94.193 秒，模型等待 34.082 秒，真实 solver 17 次，查询投影 25 项，动作记录含缓存 346 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 91, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `51b91a2c40820f317efc784afbede0fbb50c9416b9f4b3552aeef765198eb18a`，决定 SHA `e2164ecf6510d641d7f23b9dcd297fd4a3c1fa946f140bd6b451c227267050b1`。

## RQ1_67706b288d9c

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_67706b288d9c) · 检查明细 [Checks-45.json](Checks-45.json) · 查询明细 [Queries-20.json](Queries-20.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 28, 'external_dependency': 14}。相关检查决定 {'external_dependency': 126, 'policy_missing': 69, 'applicable_role_guard': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 203.381 秒，模型等待 30.472 秒，真实 solver 80 次，查询投影 261 项，动作记录含缓存 673 项。诊断 {'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 187, 'noncached_action_limit': 2, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `c69b175e3b2a48388d5963da5089ebf1fa9e1589da7ba29bd4da300134bc5b61`，决定 SHA `3dfae82febad7ec7119412527a2b593fcab1f9851a36f9283188d96911139b3f`。

## RQ1_5bc96eda4b9f

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_5bc96eda4b9f) · 检查明细 [Checks-45.json](Checks-45.json) [Checks-46.json](Checks-46.json) · 查询明细 [Queries-20.json](Queries-20.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:341:S1 | Mining24 | TP | TP | TP | TP | matched |
| D2:341:S2 | ToOwner | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_e9d0718fde795cd7487a`，根位置 2968＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2968 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E248

发现 `finding_cc528004ac460f40f3a7`，根位置 3071＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 3071 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E249, E5

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 78.235 秒，模型等待 31.917 秒，真实 solver 86 次，查询投影 94 项，动作记录含缓存 351 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 120, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `b874f601032dd63619f2e2b5496ec29b721a5d281b8cf618b8fc50f1640a4d73`，决定 SHA `a6a605555ffcd34c105c4c712d80fce86127f0ec392201a208240edb1db8f6e4`。

## RQ1_cacdbfec861f

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_cacdbfec861f) · 检查明细 [Checks-46.json](Checks-46.json) · 查询明细 [Queries-20.json](Queries-20.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:342:author:1 | Token | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_3f2b49fa313a7e8290d5`，根位置 588＋11，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 588 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E14

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.963 秒，模型等待 41.815 秒，真实 solver 3 次，查询投影 4 项，动作记录含缓存 15 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 3, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `a6929d75bc8fdaec5fb00ee62b3d55ee45e60cd468eff9a4c2bdc51e97b0f475`，决定 SHA `11cfec7968bbb06f57fbe0f326022af6a940f4ec5882af1347277df6ef63ec58`。

## RQ1_a1dd972c93be

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_a1dd972c93be) · 检查明细 [Checks-46.json](Checks-46.json) · 查询明细 [Queries-20.json](Queries-20.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:343:author:1 | Doubler | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_f07eb322b224a4820458`，根位置 373＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 373 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E1, E109

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 45.132 秒，模型等待 21.620 秒，真实 solver 37 次，查询投影 39 项，动作记录含缓存 114 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 54, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `1af77ca2e64e180d9057885d6b9a60f810df3bf77ed0be90ec67b790d0967077`，决定 SHA `456de79b8a6bbedf1a25c2abf7051548861007657d2b9de3295fc8003a4bfb32`。

## RQ1_12eee489708e

任务 AC，评价类别 AC。当前未知，BG 报警。

[实际输入](InputSource-07.md#rq1_12eee489708e) · 检查明细 [Checks-46.json](Checks-46.json) · 查询明细  · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:344:original:1 | fin | FN | FN | TP | TP | aligned_inspection_without_matching_alarm |
| D2:344:original:2 | pay | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 1, 'external_dependency': 1}。相关检查决定 {'policy_missing': 1, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.181 秒，模型等待 89.319 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `18c21b965e3037b8b81aa6ea79f502c1dd6fe56132f8479476ddf64d94e3b7bc`，决定 SHA `2b0d82aace94c63c071fff40f3dce058be7dae511a7d39d0b7a482feda4ca0e0`。

## RQ1_157ad458dd23

任务 AC，评价类别 AC。当前报警，BG 报警。

[实际输入](InputSource-07.md#rq1_157ad458dd23) · 检查明细 [Checks-46.json](Checks-46.json) · 查询明细 [Queries-20.json](Queries-20.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:345:author:1 | ARBITRAGEToken | TP | TP | TP | TP | matched |

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_0d991e42a1957c20f1b9`，根位置 2591＋18，依据 `source_role_reassignment`。The assessment concerns the policy governing the protected effect at source offset 2591 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location. 证据 E2, E66

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.645 秒，模型等待 54.618 秒，真实 solver 38 次，查询投影 41 项，动作记录含缓存 51 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 19, 'unknown_assessment_vocabulary': 1}。

最终报告 SHA `2bb627c2b51e4d4f6108cae22cb9fe64387815db556ee57b5340bde30e4a38ff`，决定 SHA `231f94c3d63d35aea474b9b66fb5b48e9d41b33695ec3f5d0d1e946a757a504a`。

## RQ1_89eba7cb4ce4

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_89eba7cb4ce4) · 检查明细 [Checks-46.json](Checks-46.json) · 查询明细 [Queries-20.json](Queries-20.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

此成员没有作者 AC 参考根，现有报警按参考外作用计 FP。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 42, 'external_dependency': 21}。相关检查决定 {'policy_missing': 114, 'external_dependency': 236, 'applicable_role_guard': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 431.519 秒，模型等待 65.375 秒，真实 solver 111 次，查询投影 406 项，动作记录含缓存 947 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 337, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'noncached_action_limit': 1}。

最终报告 SHA `a76f72e8ed685bff1113e7e6c9c902f72891f639badc7e996aee68cdcc130ef6`，决定 SHA `79629332b2d7ffe99fb1e10661e2730789f646d688acdf6ba8a96b5749948fd6`。

## RQ1_191a7df49b99

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_191a7df49b99) · 检查明细 [Checks-46.json](Checks-46.json) · 查询明细 [Queries-20.json](Queries-20.json) [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:347:S1 | init | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:347:S2 | setRelease | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:347:S3 | lock | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |
| D2:347:S4 | kill | FN | FN | FN | TP | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 7}。相关检查决定 {'policy_missing': 18, 'external_dependency': 1, 'applicable_role_guard': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.707 秒，模型等待 55.335 秒，真实 solver 61 次，查询投影 93 项，动作记录含缓存 45 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 16, 'ambiguous_confirmation_not_a_risk_judgment': 1}。

最终报告 SHA `b0210f7b917379b6b3aba7703052ec77b098f2cba87cc6b4529458bf270d8d05`，决定 SHA `97187c52d74dfd633f2b1b9dd879d09207f21d44c1c9b4dfed82c9c2ebe54673`。

## RQ1_ffbee73ba561

任务 AC，评价类别 AC。当前未知，BG 未知。

[实际输入](InputSource-07.md#rq1_ffbee73ba561) · 检查明细 [Checks-46.json](Checks-46.json) [Checks-47.json](Checks-47.json) · 查询明细 [Queries-21.json](Queries-21.json) · 服务回执索引 [Requests-02.json](Requests-02.json)

| 作者根 | 函数 | 当前 | 最近SmartBug | BG | v32 | 可观察断点 |
|---|---|---|---|---|---|---|
| D2:348:author:1 | TokenERC20 | FN | FN | FN | FN | aligned_inspection_without_matching_alarm |

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'policy_missing': 8, 'external_dependency': 3}。相关检查决定 {'policy_missing': 62, 'external_dependency': 33, 'holder_own_transfer': 2, 'self_delegation': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 900.982 秒，模型等待 41.202 秒，真实 solver 34 次，查询投影 62 项，动作记录含缓存 242 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 94, 'yield_to_source_bound_semantic_review': 1, 'unknown_assessment_vocabulary': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `fe17cbcb95fe129480f54fd23b66a5d1b06b691dbb9512bf86f28ea8aa7e96f6`，决定 SHA `13f51a6348ecb5a78044adb23a7224a910efa146b34206d7ca7348c90376fa0f`。
