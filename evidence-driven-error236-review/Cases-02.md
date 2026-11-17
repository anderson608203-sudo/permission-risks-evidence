# 逐成员审阅

[总报告](WorkReview.md) · [成员](Members.md) · [源码](Code.md)

## RQ1_e97f2d279ad9

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_e97f2d279ad9)

Checks：[Checks-33.json](Checks-33.json)

Queries：[Queries-17.json](Queries-17.json)

Evidence：[Evidence-61.json](Evidence-61.json) · [Evidence-62.json](Evidence-62.json)

Coverage：[Coverage-16.json](Coverage-16.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:47:S1 | Prosperity | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:47:S2 | giveBlockReward | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_985a35fe27b90efc753f`，AC，units/program.sol:eZWay，字节3979＋55，决定 `unbacked_source_issuance`，证据E29。The assessment concerns the policy governing the protected effect at source offset 3979. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 31, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 12.847297026310116, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 40.893521836958826, "task_wall_seconds": 53.740821483079344}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.29205022752285004, "calls": 76, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 98}

## RQ1_38fe09bdf4c5

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_38fe09bdf4c5)

Checks：[Checks-10.json](Checks-10.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-11.json](Evidence-11.json) · [Evidence-12.json](Evidence-12.json)

Coverage：[Coverage-04.json](Coverage-04.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:53:original:1 | Vault | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:53:original:2 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 6, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 3.229453952051699, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 58.6031549340114, "task_wall_seconds": 61.832610548939556}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.04088680446147919, "calls": 28, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 21}

## RQ1_e85ac4a50ee4

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_e85ac4a50ee4)

Checks：[Checks-33.json](Checks-33.json)

Queries：[Queries-17.json](Queries-17.json)

Evidence：[Evidence-61.json](Evidence-61.json)

Coverage：[Coverage-16.json](Coverage-16.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:57:author:1 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 7, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 2.423929014708847, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 17.850686885416508, "task_wall_seconds": 20.274617361370474}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.00782492384314537, "calls": 6, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 11}

## RQ1_2ab8786fb079

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_2ab8786fb079)

Checks：[Checks-07.json](Checks-07.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-08.json](Evidence-08.json)

Coverage：[Coverage-03.json](Coverage-03.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:58:author:1 | BluechipToken | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_6cc28e4adfb7afc1c7e4`，AC，units/program.sol:Sota，字节3625＋60，决定 `unbacked_source_issuance`，证据E10,E11。The assessment concerns the policy governing the protected effect at source offset 3625. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 2, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 25.759133773855865, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 49.74669373920187, "task_wall_seconds": 75.50583028700203}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14676685445010662, "calls": 59, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_d05efb1718e4

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_d05efb1718e4)

Checks：[Checks-30.json](Checks-30.json)

Queries：[Queries-16.json](Queries-16.json)

Evidence：[Evidence-55.json](Evidence-55.json)

Coverage：[Coverage-14.json](Coverage-14.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:60:author:1 | BMV | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_649e339fd757fd66c835`，AC，units/program.sol:BitmassExToken，字节3562＋60，决定 `unbacked_source_issuance`，证据E8,E9。The assessment concerns the policy governing the protected effect at source offset 3562. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 26.405845711007714, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 30.114717160351574, "task_wall_seconds": 56.52056503202766}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.15378705132752657, "calls": 59, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_309938a2bbb9

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_309938a2bbb9)

Checks：[Checks-09.json](Checks-09.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-10.json](Evidence-10.json) · [Evidence-11.json](Evidence-11.json)

Coverage：[Coverage-03.json](Coverage-03.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:62:author:1 | KingToken | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_1141d6b92caa4263e5af`，AC，units/program.sol:WarCoin，字节3519＋60，决定 `unbacked_source_issuance`，证据E8,E9。The assessment concerns the policy governing the protected effect at source offset 3519. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 1, "unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 26.451717763207853, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 38.37326101586223, "task_wall_seconds": 64.82498198980466}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.1562120378948748, "calls": 58, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_281f3b161467

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_281f3b161467)

Checks：[Checks-07.json](Checks-07.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-07.json](Evidence-07.json)

Coverage：[Coverage-03.json](Coverage-03.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:67:author:1 | MyTestWallet7 | FN→TP | gained | 3 / matched / source_role_reassignment,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

新增参考根命中已对应实际资格改写位置；不以同合约的mint/其它位置报警顶替。基础检查点已接纳首答，不能据此归因为程序独立或LLM独立增益。

报警 `finding_59d9999b12ee8e1d9583`，AC，units/program.sol:HelpMeSave，字节143＋15，决定 `source_role_reassignment`，证据E1,E2。The assessment concerns the policy governing the protected effect at source offset 143. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 4, "unrelated_or_secondary_graph_pairs_deferred": 4, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 2.763976480346173, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 60.868695811834186, "task_wall_seconds": 63.63267382327467}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0355052319355309, "calls": 14, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 13}

## RQ1_155abf47bb4c

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_155abf47bb4c)

Checks：[Checks-05.json](Checks-05.json)

Queries：[Queries-01.json](Queries-01.json)

Evidence：[Evidence-04.json](Evidence-04.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:76:S1 | init | FN→FN | still_missed | 11 / aligned_inspection_without_matching_alarm / local_bookkeeping,policy_missing |
| D2:76:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:76:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:76:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 9, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 4.510970083996654, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 73.3538667797111, "task_wall_seconds": 77.86483883857727}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0981886237859726, "calls": 55, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 28}

## RQ1_e35c80271bc7

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_e35c80271bc7)

Checks：[Checks-32.json](Checks-32.json)

Queries：[Queries-17.json](Queries-17.json)

Evidence：[Evidence-58.json](Evidence-58.json) · [Evidence-59.json](Evidence-59.json) · [Evidence-60.json](Evidence-60.json)

Coverage：[Coverage-15.json](Coverage-15.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:78:author:1 | StoriqaCash | FN→FN | still_missed | 6 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_semantic_row": 1, "no_locatable_source": 3, "unrelated_or_secondary_graph_pairs_deferred": 171, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 210.78302192641422, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 53.59893803764135, "task_wall_seconds": 264.38196500297636}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.2874807296320796, "calls": 100, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 508}

## RQ1_a3ce171c6be6

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_a3ce171c6be6)

Checks：[Checks-21.json](Checks-21.json)

Queries：[Queries-12.json](Queries-12.json)

Evidence：[Evidence-34.json](Evidence-34.json)

Coverage：[Coverage-10.json](Coverage-10.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:79:S1 | init | FN→FN | still_missed | 10 / aligned_inspection_without_matching_alarm / local_bookkeeping,policy_missing |
| D2:79:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:79:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:79:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_issue_kind": 1, "audit_source_scope_mismatch": 1, "unrelated_or_secondary_graph_pairs_deferred": 10, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 5.494118947535753, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 69.30071998247877, "task_wall_seconds": 74.794840706978}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.15046375710517168, "calls": 78, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 31}

## RQ1_f692c464b513

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_f692c464b513)

Checks：[Checks-34.json](Checks-34.json)

Queries：[Queries-18.json](Queries-18.json)

Evidence：[Evidence-62.json](Evidence-62.json) · [Evidence-63.json](Evidence-63.json) · [Evidence-64.json](Evidence-64.json) · [Evidence-65.json](Evidence-65.json)

Coverage：[Coverage-17.json](Coverage-17.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:87:author:1 | payout | FN→FN | still_missed | 30 / aligned_inspection_without_matching_alarm / external_dependency,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 95}

资源：{"program": {"program_investigation_seconds": 213.25111456913874, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 30.17026614677161, "task_wall_seconds": 243.4213840761222}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {"timeout": 1}, "used_seconds": 22.139207751024514, "calls": 58, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 193}

## RQ1_bae823e736e2

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_bae823e736e2)

Checks：[Checks-26.json](Checks-26.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-45.json](Evidence-45.json)

Coverage：[Coverage-12.json](Coverage-12.json)

Semantics：[Semantics-08.json](Semantics-08.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:91:author:1 | removeContract | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.2954577920027077, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 34.52695961808786, "task_wall_seconds": 36.82242101011798}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0028861910104751587, "calls": 1, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 11}

## RQ1_6247dff94d60

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_6247dff94d60)

Checks：[Checks-15.json](Checks-15.json)

Queries：没有该类保存记录。

Evidence：[Evidence-21.json](Evidence-21.json)

Coverage：[Coverage-07.json](Coverage-07.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:92:original:1 | close | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:92:original:2 | play | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.276092595886439, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 40.34716675616801, "task_wall_seconds": 42.6232637912035}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 4}

## RQ1_f25b185c19f2

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_f25b185c19f2)

Checks：[Checks-34.json](Checks-34.json)

Queries：没有该类保存记录。

Evidence：[Evidence-62.json](Evidence-62.json)

Coverage：[Coverage-17.json](Coverage-17.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:95:author:1 | DeskToken | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 2, "unrelated_or_secondary_graph_pairs_deferred": 10, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 14.044150565285236, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 54.89949319278821, "task_wall_seconds": 68.9436456989497}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 32}

## RQ1_967e7a02c55f

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_967e7a02c55f)

Checks：[Checks-19.json](Checks-19.json)

Queries：[Queries-11.json](Queries-11.json)

Evidence：[Evidence-28.json](Evidence-28.json) · [Evidence-29.json](Evidence-29.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:96:author:1 | close_bank | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 4, "unrelated_or_secondary_graph_pairs_deferred": 32, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 11.94221135089174, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 42.02787456428632, "task_wall_seconds": 53.97008836315945}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.08677191520109773, "calls": 45, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 57}

## RQ1_b4fca92c3262

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_b4fca92c3262)

Checks：[Checks-24.json](Checks-24.json) · [Checks-25.json](Checks-25.json) · [Checks-26.json](Checks-26.json)

Queries：没有该类保存记录。

Evidence：没有该类保存记录。

Coverage：[Coverage-12.json](Coverage-12.json)

Semantics：[Semantics-08.json](Semantics-08.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:97:S1 | owned | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:97:S2 | STARTMETADOLLAR | FN→FN | still_missed | 38 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "program_investigation_seconds": 2, "semantic_answer_outside_sent_scope": 1}

资源：{"program": {"program_investigation_seconds": 1065.2834750120528, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 28.163759446237236, "task_wall_seconds": 1093.447239083238}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 0}

## RQ1_d03e74720975

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_d03e74720975)

Checks：[Checks-30.json](Checks-30.json)

Queries：[Queries-16.json](Queries-16.json)

Evidence：[Evidence-55.json](Evidence-55.json)

Coverage：[Coverage-14.json](Coverage-14.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:98:author:1 | LottoCount | FN→FN | still_missed | 5 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 4, "semantic_answer_outside_sent_scope": 1}

资源：{"program": {"program_investigation_seconds": 3.1195900859311223, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 45.6771215191111, "task_wall_seconds": 48.79671471333131}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.053489651530981064, "calls": 22, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 14}

## RQ1_7eb51c5c90eb

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_7eb51c5c90eb)

Checks：[Checks-17.json](Checks-17.json)

Queries：[Queries-09.json](Queries-09.json)

Evidence：[Evidence-25.json](Evidence-25.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:104:author:1 | ActiveAdmin | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 15, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 10.432463344652206, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 22.74747125292197, "task_wall_seconds": 33.17993673682213}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.05416191974654794, "calls": 18, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 49}

## RQ1_adc795eb2050

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_adc795eb2050)

Checks：[Checks-22.json](Checks-22.json)

Queries：[Queries-12.json](Queries-12.json)

Evidence：[Evidence-34.json](Evidence-34.json) · [Evidence-35.json](Evidence-35.json)

Coverage：[Coverage-11.json](Coverage-11.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:108:original:1 | initialize | FN→FN | still_missed | 10 / aligned_inspection_without_matching_alarm / guarded_source_effect,local_bookkeeping,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 27, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 9.008326334413141, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 75.66690913867205, "task_wall_seconds": 84.6752391778864}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.03524390235543251, "calls": 15, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 108}

## RQ1_ac3501efc177

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_ac3501efc177)

Checks：[Checks-21.json](Checks-21.json)

Queries：没有该类保存记录。

Evidence：[Evidence-34.json](Evidence-34.json)

Coverage：[Coverage-10.json](Coverage-10.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:110:author:1 | destroy | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / external_dependency,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"shared_declaration_in_distinct_applied_contexts": 1, "invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.1934093818999827, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 23.66801550704986, "task_wall_seconds": 25.861426576972008}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 5}
