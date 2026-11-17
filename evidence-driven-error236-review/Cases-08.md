# 逐成员审阅

[总报告](WorkReview.md) · [成员](Members.md) · [源码](Code.md)

## RQ1_b0b75749d918

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_b0b75749d918)

Checks：[Checks-23.json](Checks-23.json) · [Checks-24.json](Checks-24.json)

Queries：[Queries-12.json](Queries-12.json)

Evidence：[Evidence-39.json](Evidence-39.json)

Coverage：[Coverage-11.json](Coverage-11.json)

Semantics：[Semantics-07.json](Semantics-07.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:491:author:1 | close_bank | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 32, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 11.646251189988106, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 66.16335877683014, "task_wall_seconds": 77.80961188906804}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.07621652306988835, "calls": 45, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 57}

## RQ1_5181a8367a1c

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_5181a8367a1c)

Checks：[Checks-14.json](Checks-14.json)

Queries：[Queries-06.json](Queries-06.json)

Evidence：[Evidence-18.json](Evidence-18.json)

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:495:S1 | init | FN→FN | still_missed | 11 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |
| D2:495:S2 | SetReleaseDate | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:495:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:495:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unbound_or_inapplicable_seed": 1, "audit_effect_unbound": 1, "audit_source_scope_mismatch": 1, "unrelated_or_secondary_graph_pairs_deferred": 9, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 4.6839613215997815, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 50.59807321242988, "task_wall_seconds": 55.28203610610217}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.11140636121854186, "calls": 61, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 28}

## RQ1_fb0f325e2800

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_fb0f325e2800)

Checks：[Checks-35.json](Checks-35.json) · [Checks-36.json](Checks-36.json)

Queries：[Queries-18.json](Queries-18.json)

Evidence：[Evidence-66.json](Evidence-66.json) · [Evidence-67.json](Evidence-67.json) · [Evidence-68.json](Evidence-68.json)

Coverage：[Coverage-17.json](Coverage-17.json)

Semantics：[Semantics-11.json](Semantics-11.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:498:author:1 | ZeroXEth | FN→FN | still_missed | 6 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 173, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 172.8537991149351, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 48.471770462114364, "task_wall_seconds": 221.32557180104777}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.20868306746706367, "calls": 78, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 514}

## RQ1_116d8aeb4b40

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_116d8aeb4b40)

Checks：[Checks-04.json](Checks-04.json) · [Checks-05.json](Checks-05.json)

Queries：[Queries-01.json](Queries-01.json)

Evidence：[Evidence-03.json](Evidence-03.json) · [Evidence-04.json](Evidence-04.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:504:author:1 | spitoken | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_b145ce99e6cb5b821c88`，AC，units/program.sol:spinetwork，字节3559＋60，决定 `unbacked_source_issuance`，证据E11,E9。The assessment concerns the policy governing the protected effect at source offset 3559. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 25.701490050647408, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 32.343813164159656, "task_wall_seconds": 58.0453055719845}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14938379963859916, "calls": 59, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_2d5de0155ecf

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_2d5de0155ecf)

Checks：[Checks-07.json](Checks-07.json) · [Checks-08.json](Checks-08.json) · [Checks-09.json](Checks-09.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-08.json](Evidence-08.json) · [Evidence-09.json](Evidence-09.json)

Coverage：[Coverage-03.json](Coverage-03.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:506:author:1 | construct | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "yield_to_source_bound_semantic_review": 1, "unknown_assessment_vocabulary": 1, "unrelated_or_secondary_graph_pairs_deferred": 115, "noncached_action_limit": 1}

资源：{"program": {"program_investigation_seconds": 811.8028788953088, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 36.12935937894508, "task_wall_seconds": 847.9322429699823}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.07602657284587622, "calls": 25, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 365}

## RQ1_5add5c765bae

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_5add5c765bae)

Checks：[Checks-14.json](Checks-14.json) · [Checks-15.json](Checks-15.json)

Queries：[Queries-06.json](Queries-06.json)

Evidence：[Evidence-20.json](Evidence-20.json)

Coverage：[Coverage-07.json](Coverage-07.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:513:original:1 | disableContract | FN→FN | still_missed | 0 / no_listed_obligation_at_reference /  |
| D2:513:original:2 | setupMiniGame | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_issue_field_shape": 5, "explicit_effect_anchor_conflict": 2, "unrelated_or_secondary_graph_pairs_deferred": 54, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 22.550952814519405, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 50.353850840590894, "task_wall_seconds": 72.90480568632483}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.007898295298218727, "calls": 5, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 188}

## RQ1_79c70cdd1bf6

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_79c70cdd1bf6)

Checks：[Checks-17.json](Checks-17.json)

Queries：[Queries-09.json](Queries-09.json)

Evidence：[Evidence-25.json](Evidence-25.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:515:S1 | TimeLockr | FN→FN | still_missed | 11 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |
| D2:515:S2 | SetReleaseDate | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:515:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:515:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 3, "unrelated_or_secondary_graph_pairs_deferred": 10}

资源：{"program": {"program_investigation_seconds": 4.304327180143446, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 77.92023300612345, "task_wall_seconds": 82.22456196602434}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.10512669570744038, "calls": 61, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 29}

## RQ1_10bbee42cd76

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_10bbee42cd76)

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
| D2:518:author:1 | ActiveAdmin | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 1, "unrelated_or_secondary_graph_pairs_deferred": 15, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 10.176473732572049, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 24.591682906262577, "task_wall_seconds": 34.76815832592547}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.059193057008087635, "calls": 18, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 49}

## RQ1_f694e40ffba2

任务 AC，本次未知，上批同成员报警。

[实际输入源码](InputSource-03.md#rq1_f694e40ffba2)

Checks：[Checks-34.json](Checks-34.json)

Queries：[Queries-18.json](Queries-18.json)

Evidence：[Evidence-65.json](Evidence-65.json)

Coverage：[Coverage-17.json](Coverage-17.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:521:S1 | init | TP→FN | lost | 11 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |
| D2:521:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:521:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:521:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

旧命中丢失：当前同根落在policy_missing/local_bookkeeping等判断；该局部决定进入最终未报警，非仅导出丢字。保存源内缺失职责和读者是否被错误排除须分别核，不能将旧TP当然视为科学真值。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 9, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 4.605262694414705, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 75.58199077937752, "task_wall_seconds": 80.18725515296683}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14496724773198366, "calls": 68, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 27}

## RQ1_d4aefd2e1bfc

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_d4aefd2e1bfc)

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
| D2:522:author:1 | refundOwner | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 3, "unrelated_or_secondary_graph_pairs_deferred": 10, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 7.371577546931803, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 46.74955486599356, "task_wall_seconds": 54.12113423878327}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0661587012000382, "calls": 24, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 26}

## RQ1_444af83fd288

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_444af83fd288)

Checks：[Checks-12.json](Checks-12.json)

Queries：[Queries-05.json](Queries-05.json)

Evidence：[Evidence-16.json](Evidence-16.json)

Coverage：[Coverage-05.json](Coverage-05.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:524:author:1 | suicide | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 12, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 7.790540199261159, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 41.93547403719276, "task_wall_seconds": 49.72601622901857}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.08959233621135354, "calls": 34, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 34}

## RQ1_6f3ba10080c4

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_6f3ba10080c4)

Checks：[Checks-16.json](Checks-16.json)

Queries：没有该类保存记录。

Evidence：[Evidence-24.json](Evidence-24.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:525:S1 | POWHclone | FN→FN | still_missed | 0 / no_aligned_inspection_in_obligations /  |
| D2:525:S2 | approve | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"missing_claim_or_source_anchor": 1, "unrelated_or_secondary_graph_pairs_deferred": 4}

资源：{"program": {"program_investigation_seconds": 17.705254188273102, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 28.33178414264694, "task_wall_seconds": 46.037040054798126}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 11}

## RQ1_e88cd683cd73

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_e88cd683cd73)

Checks：[Checks-33.json](Checks-33.json)

Queries：[Queries-17.json](Queries-17.json)

Evidence：[Evidence-61.json](Evidence-61.json)

Coverage：[Coverage-16.json](Coverage-16.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:529:author:1 | CompanyToken | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_b0ce5ea26fbe9b44718b`，AC，units/program.sol:AgroLyteToken，字节3541＋60，决定 `unbacked_source_issuance`，证据E10,E8。The assessment concerns the policy governing the protected effect at source offset 3541. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 24.848106723744422, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 93.98020489932969, "task_wall_seconds": 118.82831403892487}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.1333564007654786, "calls": 55, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_e440a75a1c8a

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_e440a75a1c8a)

Checks：[Checks-33.json](Checks-33.json)

Queries：[Queries-17.json](Queries-17.json)

Evidence：[Evidence-60.json](Evidence-60.json) · [Evidence-61.json](Evidence-61.json)

Coverage：[Coverage-16.json](Coverage-16.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:530:author:1 | VTTR | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"core_unresolved_retained_for_investigation": 1, "unrelated_or_secondary_graph_pairs_deferred": 24, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 13.695025355089456, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 38.771150772925466, "task_wall_seconds": 52.466178147122264}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14922545989975333, "calls": 57, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 104}

## RQ1_254bfee03840

任务 AC，本次未知，上批同成员报警。

[实际输入源码](InputSource-03.md#rq1_254bfee03840)

Checks：[Checks-07.json](Checks-07.json)

Queries：[Queries-03.json](Queries-03.json)

Evidence：[Evidence-07.json](Evidence-07.json)

Coverage：[Coverage-03.json](Coverage-03.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:534:S1 | owned | TP→FN | lost | 2 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:534:S2 | bitexlive | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

旧命中丢失：当前同根落在policy_missing/local_bookkeeping等判断；该局部决定进入最终未报警，非仅导出丢字。保存源内缺失职责和读者是否被错误排除须分别核，不能将旧TP当然视为科学真值。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 5, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 4.045207919552922, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 52.68200084241107, "task_wall_seconds": 56.727210419252515}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.00020905118435621262, "calls": 1, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 22}

## RQ1_4c2921d39474

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_4c2921d39474)

Checks：[Checks-13.json](Checks-13.json)

Queries：[Queries-05.json](Queries-05.json) · [Queries-06.json](Queries-06.json)

Evidence：[Evidence-17.json](Evidence-17.json) · [Evidence-18.json](Evidence-18.json)

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:535:author:1 | init | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_5806b6ba4c0b7c0c2c79`，AC，units/program.sol:EthDeposit，字节2703＋21，决定 `unguarded_governed_effect`，证据E13。The assessment concerns the policy governing the protected effect at source offset 2703. A separate entry requires the stated incumbent to govern this same state. The located change has no corresponding guard under the stated policy. A separate entry consumes the changed qualification at the linked source location.

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 1, "unrelated_or_secondary_graph_pairs_deferred": 32, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 10.97236416907981, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 26.739073515869677, "task_wall_seconds": 37.711439406033605}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.6072340495884418, "calls": 86, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 100}

## RQ1_03a271e0c36c

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_03a271e0c36c)

Checks：[Checks-01.json](Checks-01.json)

Queries：[Queries-01.json](Queries-01.json)

Evidence：[Evidence-01.json](Evidence-01.json)

Coverage：[Coverage-01.json](Coverage-01.json)

Semantics：[Semantics-01.json](Semantics-01.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:538:S1 | initialize | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"audit_check_target_unbound": 3, "shared_declaration_in_distinct_applied_contexts": 1, "unrelated_or_secondary_graph_pairs_deferred": 6, "semantic_answer_outside_sent_scope": 1}

资源：{"program": {"program_investigation_seconds": 2.6611437564715743, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 61.46929638041183, "task_wall_seconds": 64.13044169405475}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.016035552602261305, "calls": 7, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 17}

## RQ1_a533300b98f5

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_a533300b98f5)

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
| D2:539:author:1 | die | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 1, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 2.09369208291173, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 13.1473333039321, "task_wall_seconds": 15.241027504205704}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 2}

## RQ1_b45fd17eae9d

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_b45fd17eae9d)

Checks：[Checks-24.json](Checks-24.json)

Queries：[Queries-12.json](Queries-12.json)

Evidence：[Evidence-39.json](Evidence-39.json)

Coverage：[Coverage-11.json](Coverage-11.json)

Semantics：[Semantics-07.json](Semantics-07.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:544:S1 | init | FN→FN | still_missed | 10 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |
| D2:544:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:544:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:544:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 2, "unrelated_or_secondary_graph_pairs_deferred": 11, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 5.1028788452968, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 62.423388179857284, "task_wall_seconds": 67.52626876998693}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.1356321289204061, "calls": 69, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 32}

## RQ1_63bf9791ac38

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_63bf9791ac38)

Checks：[Checks-15.json](Checks-15.json)

Queries：[Queries-07.json](Queries-07.json)

Evidence：[Evidence-21.json](Evidence-21.json)

Coverage：[Coverage-07.json](Coverage-07.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:551:author:1 | withdraw | FN→FN | still_missed | 6 / aligned_inspection_without_matching_alarm / external_dependency,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 3, "unrelated_or_secondary_graph_pairs_deferred": 72, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 23.456627740059048, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 47.59238207479939, "task_wall_seconds": 71.04901194619015}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.05941845569759607, "calls": 29, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 111}
