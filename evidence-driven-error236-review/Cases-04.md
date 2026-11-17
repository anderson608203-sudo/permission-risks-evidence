# 逐成员审阅

[总报告](WorkReview.md) · [成员](Members.md) · [源码](Code.md)

## RQ1_701182c88214

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_701182c88214)

Checks：[Checks-16.json](Checks-16.json) · [Checks-17.json](Checks-17.json)

Queries：[Queries-09.json](Queries-09.json)

Evidence：[Evidence-24.json](Evidence-24.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:209:S1 | selfdestructs | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_8ed425cc06428287bd6d`，AC，units/program.sol:EncryptedToken，字节4224＋33，决定 `unbacked_source_issuance`，证据E24。The assessment concerns the policy governing the protected effect at source offset 4224. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"audit_check_target_unbound": 1, "audit_source_scope_mismatch": 1, "unrelated_or_secondary_graph_pairs_deferred": 24, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 9.292362525127828, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 59.4922975380905, "task_wall_seconds": 68.78466208232567}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.1622932953760028, "calls": 54, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 84}

## RQ1_35daecd5f1b7

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_35daecd5f1b7)

Checks：[Checks-09.json](Checks-09.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-11.json](Evidence-11.json)

Coverage：[Coverage-04.json](Coverage-04.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:216:author:1 | init | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 5, "semantic_answer_outside_sent_scope": 1}

资源：{"program": {"program_investigation_seconds": 2.572028797119856, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 93.02306435024366, "task_wall_seconds": 95.59509507613257}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.02689038822427392, "calls": 16, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 14}

## RQ1_e8110e8f607f

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_e8110e8f607f)

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
| D2:219:S1 | initalize | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:219:S2 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1, "shared_declaration_in_distinct_applied_contexts": 1, "unrelated_or_secondary_graph_pairs_deferred": 5, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 2.833474861923605, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 74.52157110115513, "task_wall_seconds": 77.35504758125171}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.03806554200127721, "calls": 24, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 15}

## RQ1_c29ef00e048d

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_c29ef00e048d)

Checks：[Checks-28.json](Checks-28.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-46.json](Evidence-46.json) · [Evidence-47.json](Evidence-47.json)

Coverage：[Coverage-13.json](Coverage-13.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:221:author:1 | cmctcybermovie | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_1f01be997c8af48d5c4f`，AC，units/program.sol:chaincybercmctmovie，字节3557＋60，决定 `unbacked_source_issuance`，证据E7,E9。The assessment concerns the policy governing the protected effect at source offset 3557. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 24.498327555134892, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 30.397776030004025, "task_wall_seconds": 54.89610548596829}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.13814637111499906, "calls": 58, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_7bcc48e80f05

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_7bcc48e80f05)

Checks：[Checks-17.json](Checks-17.json)

Queries：没有该类保存记录。

Evidence：[Evidence-25.json](Evidence-25.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:225:author:1 | delegatecall_selfdestruct | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / scope_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{}

资源：{"program": {"program_investigation_seconds": 2.0858713588677347, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 9.186633128207177, "task_wall_seconds": 11.272506501991302}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 2}

## RQ1_fdd2bcee346e

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_fdd2bcee346e)

Checks：[Checks-36.json](Checks-36.json)

Queries：[Queries-18.json](Queries-18.json)

Evidence：[Evidence-68.json](Evidence-68.json)

Coverage：[Coverage-17.json](Coverage-17.json)

Semantics：[Semantics-11.json](Semantics-11.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:229:author:1 | setupStackDepthLib | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / policy_missing,external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"shared_declaration_in_distinct_applied_contexts": 5, "unrelated_or_secondary_graph_pairs_deferred": 2}

资源：{"program": {"program_investigation_seconds": 4.574690097011626, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 83.17053143074736, "task_wall_seconds": 87.74522358272225}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.004245653748512268, "calls": 3, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 59}

## RQ1_57506af34f24

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_57506af34f24)

Checks：[Checks-14.json](Checks-14.json)

Queries：[Queries-06.json](Queries-06.json)

Evidence：[Evidence-19.json](Evidence-19.json) · [Evidence-20.json](Evidence-20.json)

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:231:author:1 | HT | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_713d96c6fc73e950e0b4`，AC，units/program.sol:HOTTO，字节3505＋60，决定 `unbacked_source_issuance`，证据E10,E11。The assessment concerns the policy governing the protected effect at source offset 3505. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 24.88318680273369, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 86.2408314011991, "task_wall_seconds": 111.12402120511979}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.15169268334284425, "calls": 59, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 140}

## RQ1_c88289d0510e

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_c88289d0510e)

Checks：[Checks-28.json](Checks-28.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-50.json](Evidence-50.json)

Coverage：[Coverage-13.json](Coverage-13.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:232:author:1 | selfDestruct | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 19, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 5.672432047314942, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 118.74010489881039, "task_wall_seconds": 124.4125391189009}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.03678447566926479, "calls": 33, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 64}

## RQ1_1007b4fc52ca

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_1007b4fc52ca)

Checks：[Checks-04.json](Checks-04.json)

Queries：[Queries-01.json](Queries-01.json)

Evidence：[Evidence-03.json](Evidence-03.json)

Coverage：[Coverage-01.json](Coverage-01.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:236:S1 | selfdestructs | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_79686dbd60d930810f81`，AC，units/program.sol:EncryptedToken，字节4224＋33，决定 `unbacked_source_issuance`，证据E24。The assessment concerns the policy governing the protected effect at source offset 4224 under financial_right. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 24, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 9.399039581418037, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 55.29727921122685, "task_wall_seconds": 64.69632106367499}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.17258942453190684, "calls": 54, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 84}

## RQ1_98573224dd77

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_98573224dd77)

Checks：[Checks-19.json](Checks-19.json)

Queries：[Queries-11.json](Queries-11.json)

Evidence：[Evidence-30.json](Evidence-30.json)

Coverage：[Coverage-10.json](Coverage-10.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:237:author:1 | stopCrowdsale | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 17, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 88.20189517457038, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 49.211134244222194, "task_wall_seconds": 137.41303189191967}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.12420099461451173, "calls": 43, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 65}

## RQ1_226d8f357d3f

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_226d8f357d3f)

Checks：[Checks-06.json](Checks-06.json)

Queries：[Queries-03.json](Queries-03.json)

Evidence：[Evidence-06.json](Evidence-06.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:238:author:1 | init | FN→FN | still_missed | 7 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"missing_claim_or_source_anchor": 3, "unrelated_or_secondary_graph_pairs_deferred": 20, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 5.9857251779176295, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 53.03271114313975, "task_wall_seconds": 59.01843800302595}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.01843066792935133, "calls": 14, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 66}

## RQ1_43caf1e7f7b5

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_43caf1e7f7b5)

Checks：[Checks-12.json](Checks-12.json)

Queries：[Queries-05.json](Queries-05.json)

Evidence：[Evidence-15.json](Evidence-15.json)

Coverage：[Coverage-05.json](Coverage-05.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:239:S1 | init | FN→FN | still_missed | 11 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |
| D2:239:S2 | SetReleaseDate | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:239:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:239:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 4, "unrelated_or_secondary_graph_pairs_deferred": 10, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 4.442015887703747, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 100.02886905614287, "task_wall_seconds": 104.47088726004586}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.12118847481906414, "calls": 65, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 29}

## RQ1_e3eee1f935e0

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_e3eee1f935e0)

Checks：[Checks-33.json](Checks-33.json)

Queries：[Queries-17.json](Queries-17.json)

Evidence：[Evidence-60.json](Evidence-60.json)

Coverage：[Coverage-16.json](Coverage-16.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:240:author:1 | init | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"missing_claim_or_source_anchor": 11, "unrelated_or_secondary_graph_pairs_deferred": 3}

资源：{"program": {"program_investigation_seconds": 23.767103181686252, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 56.47693937411532, "task_wall_seconds": 80.24404422612861}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.003037414513528347, "calls": 2, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 35}

## RQ1_80bba3c533cd

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_80bba3c533cd)

Checks：[Checks-17.json](Checks-17.json)

Queries：[Queries-10.json](Queries-10.json)

Evidence：[Evidence-25.json](Evidence-25.json) · [Evidence-26.json](Evidence-26.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:241:S1 | initWallet | FN→FN | still_missed | 11 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |
| D2:241:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:241:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:241:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 5, "unrelated_or_secondary_graph_pairs_deferred": 9, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 4.291994873434305, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 77.97342653386295, "task_wall_seconds": 82.26542350836098}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.09119049413129687, "calls": 54, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 28}

## RQ1_0930870e6f17

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_0930870e6f17)

Checks：[Checks-03.json](Checks-03.json)

Queries：[Queries-01.json](Queries-01.json)

Evidence：[Evidence-01.json](Evidence-01.json)

Coverage：[Coverage-01.json](Coverage-01.json)

Semantics：[Semantics-01.json](Semantics-01.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:243:author:1 | withrawDev | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_4a0b06f9e313666f9417`，AC，units/program.sol:SurgeToken，字节3515＋60，决定 `unbacked_source_issuance`，证据E13,E17。The assessment concerns the policy governing the protected effect at source offset 3515. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 25.907028273679316, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 57.652657398954034, "task_wall_seconds": 83.55968774668872}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.19047792023047805, "calls": 73, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 140}

## RQ1_2a567216aa64

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_2a567216aa64)

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
| D2:246:author:1 | ActiveAdmin | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 1, "unknown_or_unshown_effect": 1}

资源：{"program": {"program_investigation_seconds": 6.779820985160768, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 34.84362836787477, "task_wall_seconds": 41.623450935818255}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.01392131857573986, "calls": 5, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 5}

## RQ1_bb52ee421443

任务 AC，本次报警，上批同成员报警。

[实际输入源码](InputSource-02.md#rq1_bb52ee421443)

Checks：[Checks-26.json](Checks-26.json) · [Checks-27.json](Checks-27.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-45.json](Evidence-45.json)

Coverage：[Coverage-12.json](Coverage-12.json)

Semantics：[Semantics-08.json](Semantics-08.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:250:S1 | QLinkToken | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / local_bookkeeping,policy_missing |
| D2:250:S2 | mintTo | TP→TP | retained | 1 / matched / unbacked_source_issuance |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

报警 `finding_b38430131a9f10ed892d`，AC，units/program.sol:EthLendToken，字节2227＋23，决定 `unbacked_source_issuance`，证据E10。The assessment concerns the policy governing the protected effect at source offset 2227. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 1, "unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 7, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 3.66629342129454, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 53.97657998977229, "task_wall_seconds": 57.64287512283772}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.017880203668028116, "calls": 12, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 21}

## RQ1_3858ff02d02c

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_3858ff02d02c)

Checks：[Checks-09.json](Checks-09.json) · [Checks-10.json](Checks-10.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-11.json](Evidence-11.json)

Coverage：[Coverage-04.json](Coverage-04.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:251:author:1 | TokenERC20 | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 77, "yield_to_source_bound_semantic_review": 1, "unknown_assessment_vocabulary": 1, "program_investigation_seconds": 1}

资源：{"program": {"program_investigation_seconds": 902.6650434546173, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 41.16456980025396, "task_wall_seconds": 943.8296162681654}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.06363258883357048, "calls": 11, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 195}

## RQ1_fc71e6703f0d

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_fc71e6703f0d)

Checks：[Checks-36.json](Checks-36.json)

Queries：没有该类保存记录。

Evidence：[Evidence-68.json](Evidence-68.json)

Coverage：[Coverage-17.json](Coverage-17.json)

Semantics：[Semantics-11.json](Semantics-11.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:253:original:1 | pay | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / external_dependency |
| D2:253:original:2 | fin | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.210855206940323, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 58.5061110840179, "task_wall_seconds": 60.71696770284325}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 4}

## RQ1_0b9a9d5a2319

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_0b9a9d5a2319)

Checks：[Checks-04.json](Checks-04.json)

Queries：[Queries-01.json](Queries-01.json)

Evidence：[Evidence-02.json](Evidence-02.json)

Coverage：[Coverage-01.json](Coverage-01.json)

Semantics：[Semantics-01.json](Semantics-01.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:256:S1 | initVault | FN→FN | still_missed | 11 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |
| D2:256:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:256:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:256:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_text": 1, "unrelated_or_secondary_graph_pairs_deferred": 7, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 4.727394682355225, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 57.79350901627913, "task_wall_seconds": 62.520907171070576}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.11693719262257218, "calls": 65, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 25}
