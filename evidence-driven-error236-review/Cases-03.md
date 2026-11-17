# 逐成员审阅

[总报告](WorkReview.md) · [成员](Members.md) · [源码](Code.md)

## RQ1_6e4c18c9b391

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_6e4c18c9b391)

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
| D2:114:author:1 | initialize | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unbound_or_inapplicable_seed": 1, "invalid_semantic_row": 3, "no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 5}

资源：{"program": {"program_investigation_seconds": 2.8215243918821216, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 81.90785273490474, "task_wall_seconds": 84.72937876684591}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0338900052011013, "calls": 14, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 19}

## RQ1_5296ceb53c68

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_5296ceb53c68)

Checks：[Checks-14.json](Checks-14.json)

Queries：[Queries-06.json](Queries-06.json)

Evidence：[Evidence-18.json](Evidence-18.json)

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json) · [Messages-02.json](Messages-02.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:120:author:1 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 3, "semantic_answer_outside_sent_scope": 1}

资源：{"program": {"program_investigation_seconds": 2.9947595773264766, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 37.82621090253815, "task_wall_seconds": 40.82097251387313}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.03797940677031875, "calls": 12, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 18}

## RQ1_bbcf89ce1cf0

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_bbcf89ce1cf0)

Checks：[Checks-27.json](Checks-27.json)

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
| D2:121:author:1 | BitcoinPro | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 7, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 3.6059575537219644, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 33.534188758116215, "task_wall_seconds": 37.1401485549286}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0075272503308951855, "calls": 5, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 18}

## RQ1_671ac389b102

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_671ac389b102)

Checks：[Checks-15.json](Checks-15.json) · [Checks-16.json](Checks-16.json)

Queries：[Queries-07.json](Queries-07.json)

Evidence：[Evidence-22.json](Evidence-22.json)

Coverage：[Coverage-07.json](Coverage-07.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:126:author:1 | ominiraprotocol | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_3fe079d69c576ac145f6`，AC，units/program.sol:OminiraProtocol，字节3709＋60，决定 `unbacked_source_issuance`，证据E10,E8。The assessment concerns the policy governing the protected effect at source offset 3709. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unbound_or_inapplicable_seed": 1, "explicit_effect_anchor_conflict": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 26.05263281799853, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 48.69309148192406, "task_wall_seconds": 74.74572741612792}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.16016256110742688, "calls": 58, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_01900f3f9b7c

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_01900f3f9b7c)

Checks：[Checks-01.json](Checks-01.json)

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
| D2:130:author:1 | selfdestructs | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_9e794b7ed771cf0dd847`，AC，units/program.sol:EncryptedToken，字节4284＋33，决定 `unbacked_source_issuance`，证据E26。The assessment concerns the policy governing the protected effect at source offset 4284. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unbound_or_inapplicable_seed": 3, "audit_source_scope_mismatch": 3, "unrelated_or_secondary_graph_pairs_deferred": 29, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 10.996315400116146, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 61.32568875467405, "task_wall_seconds": 72.3220060649328}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.2095081084407866, "calls": 61, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 96}

## RQ1_e515838cbad0

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_e515838cbad0)

Checks：[Checks-33.json](Checks-33.json)

Queries：没有该类保存记录。

Evidence：[Evidence-61.json](Evidence-61.json)

Coverage：[Coverage-16.json](Coverage-16.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:132:author:1 | approve | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 3, "semantic_meaning_or_explanation_polarity_unresolved": 1}

资源：{"program": {"program_investigation_seconds": 17.671728141605854, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 51.462459893431515, "task_wall_seconds": 69.13418951584026}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 10}

## RQ1_1d6aaf3026d0

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_1d6aaf3026d0)

Checks：[Checks-06.json](Checks-06.json)

Queries：[Queries-02.json](Queries-02.json) · [Queries-03.json](Queries-03.json)

Evidence：[Evidence-05.json](Evidence-05.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:133:author:1 | init | FN→FN | still_missed | 6 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 35, "yield_to_source_bound_semantic_review": 1, "unknown_assessment_vocabulary": 1, "action_slice_exhausted": 2, "program_investigation_seconds": 1}

资源：{"program": {"program_investigation_seconds": 959.6107223234139, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 25.220846466720104, "task_wall_seconds": 984.8315714211203}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {"timeout": 1}, "used_seconds": 52.609321429394186, "calls": 2035, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 102}

## RQ1_6505f6beccc4

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_6505f6beccc4)

Checks：[Checks-15.json](Checks-15.json)

Queries：[Queries-07.json](Queries-07.json)

Evidence：[Evidence-21.json](Evidence-21.json) · [Evidence-22.json](Evidence-22.json)

Coverage：[Coverage-07.json](Coverage-07.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:138:author:1 | CryptoRoulette | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unbound_or_inapplicable_seed": 1, "unrelated_or_secondary_graph_pairs_deferred": 11, "invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 3.0020939060486853, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 55.52794676274061, "task_wall_seconds": 58.53004231210798}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.02504530781880021, "calls": 9, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 34}

## RQ1_da88771c652e

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_da88771c652e)

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
| D2:139:original:1 | fallback / delegatedFwd | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |
| D2:139:original:2 | upgrade | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 4, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 2.383168390020728, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 37.08085825573653, "task_wall_seconds": 39.46402804600075}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 12}

## RQ1_74db7b05248a

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_74db7b05248a)

Checks：[Checks-17.json](Checks-17.json)

Queries：没有该类保存记录。

Evidence：[Evidence-25.json](Evidence-25.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:145:author:1 | cleanUpAfterYourself | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 2, "explicit_effect_anchor_conflict": 1, "unrelated_or_secondary_graph_pairs_deferred": 18, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 3.467757281381637, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 44.89889968978241, "task_wall_seconds": 48.366658804006875}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 27}

## RQ1_224d9bccba32

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_224d9bccba32)

Checks：[Checks-06.json](Checks-06.json)

Queries：[Queries-03.json](Queries-03.json)

Evidence：[Evidence-05.json](Evidence-05.json) · [Evidence-06.json](Evidence-06.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:152:author:1 | VoipTken | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_50cf022658271fe59934`，AC，units/program.sol:VoipToken，字节3505＋60，决定 `unbacked_source_issuance`，证据E7,E8。The assessment concerns the policy governing the protected effect at source offset 3505 under financial_right. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 2, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 26.45464961696416, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 52.395811622962356, "task_wall_seconds": 78.85046314122155}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14812411926686764, "calls": 59, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_58a929410f82

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_58a929410f82)

Checks：[Checks-14.json](Checks-14.json)

Queries：[Queries-06.json](Queries-06.json)

Evidence：[Evidence-20.json](Evidence-20.json)

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:153:S1 | init | FN→FN | still_missed | 11 / aligned_inspection_without_matching_alarm / local_bookkeeping,policy_missing |
| D2:153:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:153:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:153:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_issue_kind": 1, "audit_source_scope_mismatch": 2, "unrelated_or_secondary_graph_pairs_deferred": 9, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 4.546709503978491, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 67.11649639019743, "task_wall_seconds": 71.66320805996656}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.1014310703612864, "calls": 53, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 28}

## RQ1_4325a2042776

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_4325a2042776)

Checks：[Checks-11.json](Checks-11.json)

Queries：[Queries-05.json](Queries-05.json)

Evidence：[Evidence-14.json](Evidence-14.json)

Coverage：[Coverage-05.json](Coverage-05.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:163:author:1 | SaveCryptoNetwork | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_65da59076332c10680b6`，AC，units/program.sol:Ethtex，字节3524＋60，决定 `unbacked_source_issuance`，证据E13,E14。The assessment concerns the policy governing the protected effect at source offset 3524 under financial_right. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 56, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 26.840457504149526, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 46.15640322305262, "task_wall_seconds": 72.99686331907287}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.5457257642410696, "calls": 72, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 139}

## RQ1_bc34a2568a3c

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_bc34a2568a3c)

Checks：[Checks-27.json](Checks-27.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-45.json](Evidence-45.json) · [Evidence-46.json](Evidence-46.json)

Coverage：[Coverage-13.json](Coverage-13.json)

Semantics：[Semantics-08.json](Semantics-08.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:173:author:1 | TokenERC20 | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 1, "unrelated_or_secondary_graph_pairs_deferred": 77, "yield_to_source_bound_semantic_review": 1, "unknown_assessment_vocabulary": 1, "program_investigation_seconds": 1}

资源：{"program": {"program_investigation_seconds": 902.343101428356, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 43.278276688884944, "task_wall_seconds": 945.6213803282008}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.03345092153176665, "calls": 11, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 193}

## RQ1_4f19278de7d5

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_4f19278de7d5)

Checks：[Checks-13.json](Checks-13.json)

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
| D2:181:author:1 | init | FN→FN | still_missed | 9 / aligned_inspection_without_matching_alarm / policy_missing,external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 26}

资源：{"program": {"program_investigation_seconds": 11.87416713917628, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 40.261233574710786, "task_wall_seconds": 52.13540250482038}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.03628107998520136, "calls": 34, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 100}

## RQ1_935718dd81f8

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_935718dd81f8)

Checks：[Checks-18.json](Checks-18.json)

Queries：没有该类保存记录。

Evidence：[Evidence-28.json](Evidence-28.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:184:author:1 | IotaGoldToken | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_text": 1, "unrelated_or_secondary_graph_pairs_deferred": 10, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 14.172333450056612, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 57.26601726282388, "task_wall_seconds": 71.43835256388411}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 33}

## RQ1_4fd6378fe4c6

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_4fd6378fe4c6)

Checks：[Checks-13.json](Checks-13.json)

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
| D2:195:author:1 | init | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 9, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 9.60919761331752, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 28.181238740682602, "task_wall_seconds": 37.79043823108077}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.007585807237774134, "calls": 8, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 26}

## RQ1_52e58c397987

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_52e58c397987)

Checks：[Checks-14.json](Checks-14.json)

Queries：[Queries-06.json](Queries-06.json)

Evidence：[Evidence-19.json](Evidence-19.json)

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:198:author:1 | ActiveAdmin | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1}

资源：{"program": {"program_investigation_seconds": 6.810315690934658, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 31.58626532694325, "task_wall_seconds": 38.396582745946944}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.012869848404079676, "calls": 5, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 5}

## RQ1_cf9b77e51d01

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_cf9b77e51d01)

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
| D2:201:author:1 | detOwner | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{}

资源：{"program": {"program_investigation_seconds": 27.26748997112736, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 50.073280359618366, "task_wall_seconds": 77.34077194612473}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.08278667228296399, "calls": 20, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 21}

## RQ1_59943c2ee47d

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-01.md#rq1_59943c2ee47d)

Checks：没有该类保存记录。

Queries：没有该类保存记录。

Evidence：没有该类保存记录。

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:204:author:1 | _0x0000006e2b22_lets_not_compete__821 | FN→FN | still_missed | 0 / no_aligned_inspection_in_obligations /  |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1}

资源：{"program": {"program_investigation_seconds": 2.0673238611780107, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 14.393678063061088, "task_wall_seconds": 16.461003752890974}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 0}
