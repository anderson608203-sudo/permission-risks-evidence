# 逐成员审阅

[总报告](WorkReview.md) · [成员](Members.md) · [源码](Code.md)

## RQ1_6c5de7dc129a

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_6c5de7dc129a)

Checks：[Checks-16.json](Checks-16.json)

Queries：没有该类保存记录。

Evidence：[Evidence-23.json](Evidence-23.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:338:author:1 | delegate_2x | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 2.4446314121596515, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 33.864252293948084, "task_wall_seconds": 36.30888543324545}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 8}

## RQ1_12eee489708e

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_12eee489708e)

Checks：[Checks-05.json](Checks-05.json)

Queries：没有该类保存记录。

Evidence：[Evidence-04.json](Evidence-04.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:344:original:1 | fin | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:344:original:2 | pay | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 2, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 2.234526344574988, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 53.74329821951687, "task_wall_seconds": 55.977826461195946}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 4}

## RQ1_191a7df49b99

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_191a7df49b99)

Checks：[Checks-05.json](Checks-05.json) · [Checks-06.json](Checks-06.json)

Queries：[Queries-02.json](Queries-02.json)

Evidence：[Evidence-05.json](Evidence-05.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:347:S1 | init | FN→FN | still_missed | 11 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |
| D2:347:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:347:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:347:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 2, "unrelated_or_secondary_graph_pairs_deferred": 7, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 4.344263983424753, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 55.99022876424715, "task_wall_seconds": 60.33449458191171}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.08814357640221715, "calls": 44, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 24}

## RQ1_ffbee73ba561

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_ffbee73ba561)

Checks：[Checks-36.json](Checks-36.json)

Queries：[Queries-18.json](Queries-18.json)

Evidence：[Evidence-68.json](Evidence-68.json) · [Evidence-69.json](Evidence-69.json)

Coverage：[Coverage-17.json](Coverage-17.json)

Semantics：[Semantics-11.json](Semantics-11.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:348:author:1 | TokenERC20 | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 84, "yield_to_source_bound_semantic_review": 1, "unknown_assessment_vocabulary": 1, "action_slice_exhausted": 1, "program_investigation_seconds": 1}

资源：{"program": {"program_investigation_seconds": 902.9168639089912, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 39.182988316286355, "task_wall_seconds": 942.0998556050472}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.1493564830161631, "calls": 34, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 219}

## RQ1_34ab8e0115aa

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_34ab8e0115aa)

Checks：[Checks-09.json](Checks-09.json)

Queries：没有该类保存记录。

Evidence：[Evidence-11.json](Evidence-11.json)

Coverage：[Coverage-04.json](Coverage-04.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:359:S1 | PonziTokenV3 | FN→FN | still_missed | 0 / no_aligned_inspection_in_obligations /  |
| D2:359:S2 | destroy | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 4, "semantic_meaning_or_explanation_polarity_unresolved": 1}

资源：{"program": {"program_investigation_seconds": 17.331500697880983, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 44.973014801274985, "task_wall_seconds": 62.30451766680926}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 12}

## RQ1_31450a049444

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_31450a049444)

Checks：[Checks-09.json](Checks-09.json)

Queries：没有该类保存记录。

Evidence：[Evidence-11.json](Evidence-11.json)

Coverage：[Coverage-03.json](Coverage-03.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:360:original:1 | fin | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:360:original:2 | pay | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.1259418027475476, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 36.73987175524235, "task_wall_seconds": 38.865815692581236}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 4}

## RQ1_a821598f1700

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_a821598f1700)

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
| D2:362:author:1 | setupStackDepthLib | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"missing_claim_or_source_anchor": 14, "unrelated_or_secondary_graph_pairs_deferred": 4, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 11.836744990665466, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 27.375112544279546, "task_wall_seconds": 39.21185911586508}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0030296528711915016, "calls": 2, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 48}

## RQ1_bb9523a9c423

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_bb9523a9c423)

Checks：[Checks-27.json](Checks-27.json)

Queries：没有该类保存记录。

Evidence：[Evidence-45.json](Evidence-45.json)

Coverage：[Coverage-12.json](Coverage-12.json)

Semantics：[Semantics-08.json](Semantics-08.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:364:author:1 | reward | FN→FN | still_missed | 7 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 4, "unrelated_or_secondary_graph_pairs_deferred": 27, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 5.8463723990134895, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 91.2720099799335, "task_wall_seconds": 97.11838509188965}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 58}

## RQ1_1efb88fb92f0

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_1efb88fb92f0)

Checks：[Checks-06.json](Checks-06.json)

Queries：[Queries-03.json](Queries-03.json)

Evidence：[Evidence-05.json](Evidence-05.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:369:author:1 | close_bank | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 2, "unrelated_or_secondary_graph_pairs_deferred": 32, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 11.088400847744197, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 82.14837239403278, "task_wall_seconds": 93.2367752767168}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.07023484772071242, "calls": 44, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 58}

## RQ1_697a8658398b

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_697a8658398b)

Checks：[Checks-16.json](Checks-16.json)

Queries：[Queries-07.json](Queries-07.json)

Evidence：[Evidence-22.json](Evidence-22.json)

Coverage：[Coverage-07.json](Coverage-07.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:377:author:1 | initialize | FN→FN | still_missed | 12 / aligned_inspection_without_matching_alarm / local_bookkeeping,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 2, "unrelated_or_secondary_graph_pairs_deferred": 2, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 3.1670466028153896, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 50.10117604024708, "task_wall_seconds": 53.268224090803415}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0013862932100892067, "calls": 2, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 13}

## RQ1_9f7d2c8c83fd

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_9f7d2c8c83fd)

Checks：[Checks-21.json](Checks-21.json)

Queries：[Queries-12.json](Queries-12.json)

Evidence：[Evidence-33.json](Evidence-33.json)

Coverage：[Coverage-10.json](Coverage-10.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:378:author:1 | initialize | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_semantic_row": 3, "audit_source_scope_mismatch": 1, "unrelated_or_secondary_graph_pairs_deferred": 2, "semantic_answer_outside_sent_scope": 1}

资源：{"program": {"program_investigation_seconds": 2.3207196444272995, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 41.513375295326114, "task_wall_seconds": 43.83409646572545}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.00019630230963230133, "calls": 1, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 8}

## RQ1_6de2b3e5e82f

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_6de2b3e5e82f)

Checks：[Checks-16.json](Checks-16.json)

Queries：[Queries-09.json](Queries-09.json)

Evidence：[Evidence-24.json](Evidence-24.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:382:author:1 | end | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 25, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 8.902012705337256, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 35.519132538698614, "task_wall_seconds": 44.421147075947374}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14940484426915646, "calls": 56, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 70}

## RQ1_e5ab2cf90f08

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_e5ab2cf90f08)

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
| D2:389:original:1 | Vault | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:389:original:2 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 5, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 2.8913932582363486, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 125.94750781962648, "task_wall_seconds": 128.83890328975394}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.041908771730959415, "calls": 22, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 16}

## RQ1_afa801e14aca

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_afa801e14aca)

Checks：[Checks-22.json](Checks-22.json) · [Checks-23.json](Checks-23.json)

Queries：[Queries-12.json](Queries-12.json)

Evidence：[Evidence-35.json](Evidence-35.json) · [Evidence-36.json](Evidence-36.json) · [Evidence-37.json](Evidence-37.json)

Coverage：[Coverage-11.json](Coverage-11.json)

Semantics：[Semantics-07.json](Semantics-07.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:393:author:1 | QMQCoin | FN→FN | still_missed | 6 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 174, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 194.9039492532611, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 54.27568166702986, "task_wall_seconds": 249.17963346419856}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.2245352636091411, "calls": 79, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 516}

## RQ1_11b39eaea9ae

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_11b39eaea9ae)

Checks：[Checks-05.json](Checks-05.json)

Queries：没有该类保存记录。

Evidence：[Evidence-04.json](Evidence-04.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:395:author:1 | destroy | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.080031921621412, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 20.2357847946696, "task_wall_seconds": 22.315818382427096}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 2}

## RQ1_7ecffa90731f

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_7ecffa90731f)

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
| D2:397:author:1 | init | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 9, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 9.391149832867086, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 35.61914355028421, "task_wall_seconds": 45.01029518712312}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.006590947043150663, "calls": 8, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 26}

## RQ1_742a666ba5fe

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_742a666ba5fe)

Checks：[Checks-17.json](Checks-17.json)

Queries：[Queries-09.json](Queries-09.json)

Evidence：[Evidence-24.json](Evidence-24.json) · [Evidence-25.json](Evidence-25.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:402:author:1 | WithrawDevToken | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_4dc7ecd404b36ff70cf7`，AC，units/program.sol:StreamCashToken，字节3555＋60，决定 `unbacked_source_issuance`，证据E11,E8。The assessment concerns the policy governing the protected effect at source offset 3555. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"missing_claim_or_source_anchor": 1, "no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 25.901512236800045, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 30.645556563977152, "task_wall_seconds": 56.5470711030066}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14548724936321378, "calls": 58, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_e99440cca868

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_e99440cca868)

Checks：[Checks-33.json](Checks-33.json)

Queries：没有该类保存记录。

Evidence：[Evidence-62.json](Evidence-62.json)

Coverage：[Coverage-16.json](Coverage-16.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:404:original:1 | vx | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:404:original:2 | ply | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.0488763959147036, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 40.975323072168976, "task_wall_seconds": 43.02420104201883}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 4}

## RQ1_e1ca494df5a4

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_e1ca494df5a4)

Checks：[Checks-31.json](Checks-31.json) · [Checks-32.json](Checks-32.json)

Queries：[Queries-17.json](Queries-17.json)

Evidence：[Evidence-57.json](Evidence-57.json) · [Evidence-58.json](Evidence-58.json)

Coverage：[Coverage-15.json](Coverage-15.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:407:author:1 | EqvcToken | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / local_bookkeeping,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 77, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 56.90318016288802, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 26.02683706022799, "task_wall_seconds": 82.93001965014264}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.25987677881494164, "calls": 83, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 265}

## RQ1_86e344166934

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_86e344166934)

Checks：[Checks-18.json](Checks-18.json)

Queries：没有该类保存记录。

Evidence：[Evidence-26.json](Evidence-26.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:411:S1 | Kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.276846411637962, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 11.597842046059668, "task_wall_seconds": 13.874689811840653}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 2}
