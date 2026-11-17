# 逐成员审阅

[总报告](WorkReview.md) · [成员](Members.md) · [源码](Code.md)

## RQ1_bbf6634a1913

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_bbf6634a1913)

Checks：[Checks-27.json](Checks-27.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-45.json](Evidence-45.json)

Coverage：[Coverage-12.json](Coverage-12.json)

Semantics：[Semantics-08.json](Semantics-08.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json) · [Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:3:S1 | selfdestructs | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_e182eb96add98d964f3e`，AC，units/program.sol:EncryptedToken，字节4224＋33，决定 `unbacked_source_issuance`，证据E24。The assessment concerns the policy governing the protected effect at source offset 4224. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_text": 2, "unrelated_or_secondary_graph_pairs_deferred": 24, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 9.817427626810968, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 41.22995096910745, "task_wall_seconds": 51.04738155286759}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.16839543543756008, "calls": 54, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 84}

## RQ1_1064e887af8d

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_1064e887af8d)

Checks：[Checks-04.json](Checks-04.json)

Queries：[Queries-01.json](Queries-01.json)

Evidence：[Evidence-03.json](Evidence-03.json)

Coverage：[Coverage-01.json](Coverage-01.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:7:author:1 | setDestoryAddress | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / local_bookkeeping,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 2, "unrelated_or_secondary_graph_pairs_deferred": 8, "invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 8.503951863385737, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 55.91833647666499, "task_wall_seconds": 64.42229011189193}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.061023303773254156, "calls": 18, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 32}

## RQ1_da205520b7b6

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_da205520b7b6)

Checks：[Checks-31.json](Checks-31.json)

Queries：没有该类保存记录。

Evidence：[Evidence-56.json](Evidence-56.json)

Coverage：[Coverage-15.json](Coverage-15.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:12:author:1 | dtrade | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1}

资源：{"program": {"program_investigation_seconds": 2.688957821112126, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 28.444004136603326, "task_wall_seconds": 31.13296339986846}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 8}

## RQ1_ae3727e56084

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_ae3727e56084)

Checks：[Checks-22.json](Checks-22.json)

Queries：[Queries-12.json](Queries-12.json)

Evidence：[Evidence-35.json](Evidence-35.json)

Coverage：[Coverage-11.json](Coverage-11.json)

Semantics：[Semantics-07.json](Semantics-07.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:13:author:1 | withdraw | FN→FN | still_missed | 6 / aligned_inspection_without_matching_alarm / external_dependency,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"missing_claim_or_source_anchor": 5, "no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 67, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 16.28508285107091, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 69.0117072192952, "task_wall_seconds": 85.29679233534262}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.010762205813080072, "calls": 5, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 75}

## RQ1_298ee75a547f

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_298ee75a547f)

Checks：[Checks-07.json](Checks-07.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-07.json](Evidence-07.json) · [Evidence-08.json](Evidence-08.json)

Coverage：[Coverage-03.json](Coverage-03.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:16:author:1 | VEXTOXTEAM | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_baa4f5c15271a87f96f6`，AC，units/program.sol:Newvestoriatovestox，字节3560＋60，决定 `unbacked_source_issuance`，证据E10,E11。The assessment concerns the policy governing the protected effect at source offset 3560. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 2, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 25.872712180484086, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 83.50749337952584, "task_wall_seconds": 109.38020809181035}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14095996413379908, "calls": 59, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_5870f63d1ec3

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_5870f63d1ec3)

Checks：[Checks-14.json](Checks-14.json)

Queries：没有该类保存记录。

Evidence：[Evidence-20.json](Evidence-20.json)

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:17:author:1 | execute | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{}

资源：{"program": {"program_investigation_seconds": 2.252769202925265, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 9.90884500881657, "task_wall_seconds": 12.161615930031985}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 2}

## RQ1_7ef1fb88c0dc

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_7ef1fb88c0dc)

Checks：[Checks-17.json](Checks-17.json)

Queries：没有该类保存记录。

Evidence：[Evidence-25.json](Evidence-25.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:18:author:1 | multi_x | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_semantic_row": 1, "invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.455231738742441, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 39.49518737895414, "task_wall_seconds": 41.950422985013574}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 2}

## RQ1_2490e07356b6

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_2490e07356b6)

Checks：[Checks-06.json](Checks-06.json) · [Checks-07.json](Checks-07.json)

Queries：没有该类保存记录。

Evidence：[Evidence-07.json](Evidence-07.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:19:author:1 | reward | FN→FN | still_missed | 7 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 4, "unrelated_or_secondary_graph_pairs_deferred": 27, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 6.282699856907129, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 55.343209247104824, "task_wall_seconds": 61.625911755952984}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 58}

## RQ1_947273fa2eef

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_947273fa2eef)

Checks：[Checks-18.json](Checks-18.json) · [Checks-19.json](Checks-19.json)

Queries：[Queries-10.json](Queries-10.json) · [Queries-11.json](Queries-11.json)

Evidence：[Evidence-28.json](Evidence-28.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:20:S1 | selfdestructs | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_b4cb77a089192f9a3844`，AC，units/program.sol:MyAdvancedToken，字节4332＋33，决定 `unbacked_source_issuance`，证据E27。The assessment concerns the policy governing the protected effect at source offset 4332. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 3, "no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 27, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 11.042906233109534, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 64.5427197208628, "task_wall_seconds": 75.5856278561987}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.1818128922022879, "calls": 55, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 93}

## RQ1_43b9baf37b44

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_43b9baf37b44)

Checks：[Checks-11.json](Checks-11.json) · [Checks-12.json](Checks-12.json)

Queries：[Queries-05.json](Queries-05.json)

Evidence：[Evidence-14.json](Evidence-14.json) · [Evidence-15.json](Evidence-15.json)

Coverage：[Coverage-05.json](Coverage-05.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:23:author:1 | MetaFoxToken | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_5cc350e1408dc0fa5218`，AC，units/program.sol:ClimateChangeCoin，字节3575＋60，决定 `unbacked_source_issuance`，证据E7,E8。The assessment concerns the policy governing the protected effect at source offset 3575. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 56}

资源：{"program": {"program_investigation_seconds": 26.54437013855204, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 39.696883789263666, "task_wall_seconds": 66.24125622678548}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14396304730325937, "calls": 56, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_068e1791fba5

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_068e1791fba5)

Checks：[Checks-01.json](Checks-01.json) · [Checks-02.json](Checks-02.json) · [Checks-03.json](Checks-03.json)

Queries：没有该类保存记录。

Evidence：没有该类保存记录。

Coverage：[Coverage-01.json](Coverage-01.json)

Semantics：[Semantics-01.json](Semantics-01.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:24:S1 | owned | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:24:S2 | STARTMETADOLLAR | FN→FN | still_missed | 42 / aligned_inspection_without_matching_alarm / local_bookkeeping,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_semantic_row": 1, "explicit_effect_anchor_conflict": 1, "program_investigation_seconds": 2}

资源：{"program": {"program_investigation_seconds": 1075.6376182711683, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 47.20667179906741, "task_wall_seconds": 1122.844294465147}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 0}

## RQ1_235a30b99277

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_235a30b99277)

Checks：[Checks-06.json](Checks-06.json)

Queries：[Queries-03.json](Queries-03.json)

Evidence：[Evidence-06.json](Evidence-06.json) · [Evidence-07.json](Evidence-07.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:26:S1 | selfdestructs | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_db08ab0f3b708b210b21`，AC，units/program.sol:TokenERC20，字节4015＋32，决定 `unbacked_source_issuance`，证据E29。The assessment concerns the policy governing the protected effect at source offset 4015. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 49, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 44.16559029556811, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 50.28401524107903, "task_wall_seconds": 94.44960774295032}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.4593515433371067, "calls": 79, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 156}

## RQ1_2a54840e0e44

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_2a54840e0e44)

Checks：[Checks-07.json](Checks-07.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-08.json](Evidence-08.json)

Coverage：[Coverage-03.json](Coverage-03.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:33:author:1 | mintForwarder | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 2, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 5.568172147963196, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 30.70233795698732, "task_wall_seconds": 36.270511713810265}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.00030411407351493835, "calls": 1, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 8}

## RQ1_d80631993985

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_d80631993985)

Checks：[Checks-31.json](Checks-31.json)

Queries：[Queries-16.json](Queries-16.json)

Evidence：[Evidence-56.json](Evidence-56.json)

Coverage：[Coverage-15.json](Coverage-15.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:36:author:1 | LEGEND | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_05f250cd1a350d552c66`，AC，units/program.sol:MEDELIN，字节3518＋60，决定 `unbacked_source_issuance`，证据E14,E16。The assessment concerns the policy governing the protected effect at source offset 3518 under financial_right. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 51, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 26.138477319385856, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 69.97274702740833, "task_wall_seconds": 96.11122630164027}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.1748313824646175, "calls": 62, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 129}

## RQ1_511b9f30f4b7

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_511b9f30f4b7)

Checks：[Checks-14.json](Checks-14.json)

Queries：没有该类保存记录。

Evidence：[Evidence-18.json](Evidence-18.json)

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:38:author:1 | withdrawTokens | FN→FN | still_missed | 0 / no_listed_obligation_at_reference /  |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 3, "unrelated_or_secondary_graph_pairs_deferred": 4, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 99.27346991980448, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 76.9152734442614, "task_wall_seconds": 176.18874573288485}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 22}

## RQ1_cfc98cba39c3

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_cfc98cba39c3)

Checks：[Checks-29.json](Checks-29.json)

Queries：[Queries-16.json](Queries-16.json)

Evidence：[Evidence-51.json](Evidence-51.json)

Coverage：[Coverage-14.json](Coverage-14.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:40:author:1 | init | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 9, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 10.042659755330533, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 43.20130391232669, "task_wall_seconds": 53.243965439964086}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0069361296482384205, "calls": 8, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 26}

## RQ1_6d7db4fbefe5

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_6d7db4fbefe5)

Checks：[Checks-16.json](Checks-16.json)

Queries：[Queries-09.json](Queries-09.json)

Evidence：[Evidence-23.json](Evidence-23.json) · [Evidence-24.json](Evidence-24.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:41:author:1 | CFCdistrubution | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing,scoped_semantic_normal |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_e80ca0606eab400c0abf`，AC，units/program.sol:CleanFoodCrypto，字节3551＋60，决定 `unbacked_source_issuance`，证据E10,E14。The assessment concerns the policy governing the protected effect at source offset 3551. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 25.071614973712713, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 42.84970573335886, "task_wall_seconds": 67.9213235033676}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.15002243826165795, "calls": 59, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 139}

## RQ1_cfe97b8f7250

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_cfe97b8f7250)

Checks：[Checks-29.json](Checks-29.json) · [Checks-30.json](Checks-30.json)

Queries：[Queries-16.json](Queries-16.json)

Evidence：[Evidence-51.json](Evidence-51.json) · [Evidence-52.json](Evidence-52.json) · [Evidence-53.json](Evidence-53.json) · [Evidence-54.json](Evidence-54.json) · [Evidence-55.json](Evidence-55.json)

Coverage：[Coverage-14.json](Coverage-14.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:43:author:1 | bioLock | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 248, "noncached_action_limit": 2, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 225.20890446053818, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 31.48447459563613, "task_wall_seconds": 256.6933819530532}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.7037428920157254, "calls": 313, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 690}

## RQ1_3b975bee1104

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_3b975bee1104)

Checks：[Checks-10.json](Checks-10.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-12.json](Evidence-12.json)

Coverage：[Coverage-04.json](Coverage-04.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:44:author:1 | TokenERC20 | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 1, "unrelated_or_secondary_graph_pairs_deferred": 24, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 54.34131909068674, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 35.4423687052913, "task_wall_seconds": 89.78368999389932}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.04852211149409413, "calls": 18, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 73}

## RQ1_8f44e59cd670

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_8f44e59cd670)

Checks：[Checks-18.json](Checks-18.json)

Queries：[Queries-10.json](Queries-10.json)

Evidence：[Evidence-27.json](Evidence-27.json) · [Evidence-28.json](Evidence-28.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:45:author:1 | HTX | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_57402f74a1cc53d2ec83`，AC，units/program.sol:HitexToken，字节3550＋60，决定 `unbacked_source_issuance`，证据E8,E9。The assessment concerns the policy governing the protected effect at source offset 3550 under financial_right. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 27.47918192157522, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 60.05863690935075, "task_wall_seconds": 87.53782257717103}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.16227916860952973, "calls": 59, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}
