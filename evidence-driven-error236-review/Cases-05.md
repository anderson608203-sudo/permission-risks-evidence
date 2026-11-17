# 逐成员审阅

[总报告](WorkReview.md) · [成员](Members.md) · [源码](Code.md)

## RQ1_0cd685c505a3

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_0cd685c505a3)

Checks：[Checks-04.json](Checks-04.json)

Queries：[Queries-01.json](Queries-01.json)

Evidence：[Evidence-02.json](Evidence-02.json) · [Evidence-03.json](Evidence-03.json)

Coverage：[Coverage-01.json](Coverage-01.json)

Semantics：[Semantics-01.json](Semantics-01.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:265:author:1 | BITCOIMINIG | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_0ee62bb5eef668e5d2ad`，AC，units/program.sol:BITCOINMILLIONARE，字节3528＋60，决定 `unbacked_source_issuance`，证据E10,E11。The assessment concerns the policy governing the protected effect at source offset 3528 under financial_right. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 57, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 24.77753861946985, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 46.30517376540229, "task_wall_seconds": 71.0827142316848}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.15205798484385014, "calls": 59, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_c0ce67b52132

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_c0ce67b52132)

Checks：[Checks-28.json](Checks-28.json)

Queries：没有该类保存记录。

Evidence：[Evidence-46.json](Evidence-46.json)

Coverage：[Coverage-13.json](Coverage-13.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:267:author:1 | reward | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 4, "unrelated_or_secondary_graph_pairs_deferred": 20, "semantic_answer_outside_sent_scope": 1}

资源：{"program": {"program_investigation_seconds": 5.577040542382747, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 50.646342009305954, "task_wall_seconds": 56.22338448278606}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 52}

## RQ1_484b7bd1d895

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_484b7bd1d895)

Checks：[Checks-13.json](Checks-13.json)

Queries：没有该类保存记录。

Evidence：[Evidence-17.json](Evidence-17.json)

Coverage：[Coverage-05.json](Coverage-05.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:268:author:1 | Xply | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.234621176030487, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 35.06629174994305, "task_wall_seconds": 37.30091447336599}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 2}

## RQ1_befa513e0336

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_befa513e0336)

Checks：[Checks-27.json](Checks-27.json) · [Checks-28.json](Checks-28.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-46.json](Evidence-46.json)

Coverage：[Coverage-13.json](Coverage-13.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:271:author:1 | kill | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 13, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 9.818910269998014, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 37.48017893685028, "task_wall_seconds": 47.299091554712504}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.023696712218225002, "calls": 9, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 57}

## RQ1_f82d8856631a

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_f82d8856631a)

Checks：[Checks-34.json](Checks-34.json) · [Checks-35.json](Checks-35.json)

Queries：[Queries-18.json](Queries-18.json)

Evidence：[Evidence-65.json](Evidence-65.json) · [Evidence-66.json](Evidence-66.json)

Coverage：[Coverage-17.json](Coverage-17.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:280:author:1 | HT | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_2957e4d9b7c75c71decc`，AC，units/program.sol:HOTTO，字节3505＋60，决定 `unbacked_source_issuance`，证据E10,E8。The assessment concerns the policy governing the protected effect at source offset 3505. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 25.028284843079746, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 75.15760012995452, "task_wall_seconds": 100.18588697398081}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14625626057386398, "calls": 59, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_6bc986b54c91

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_6bc986b54c91)

Checks：[Checks-16.json](Checks-16.json)

Queries：[Queries-07.json](Queries-07.json) · [Queries-08.json](Queries-08.json) · [Queries-09.json](Queries-09.json)

Evidence：[Evidence-23.json](Evidence-23.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:281:author:1 | init | FN→FN | still_missed | 6 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 36, "yield_to_source_bound_semantic_review": 1, "unknown_assessment_vocabulary": 1, "program_investigation_seconds": 1}

资源：{"program": {"program_investigation_seconds": 927.6742264097556, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 44.565073132980615, "task_wall_seconds": 972.2393026007339}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 43.34979521483183, "calls": 2138, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 108}

## RQ1_9f051c86ed67

任务 AC，本次未知，上批同成员报警。

[实际输入源码](InputSource-02.md#rq1_9f051c86ed67)

Checks：[Checks-21.json](Checks-21.json)

Queries：[Queries-12.json](Queries-12.json)

Evidence：[Evidence-32.json](Evidence-32.json) · [Evidence-33.json](Evidence-33.json)

Coverage：[Coverage-10.json](Coverage-10.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:290:S1 | task | TP→FN | lost | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:290:S2 | withdrawETH | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

旧命中丢失：当前同根落在policy_missing/local_bookkeeping等判断；该局部决定进入最终未报警，非仅导出丢字。保存源内缺失职责和读者是否被错误排除须分别核，不能将旧TP当然视为科学真值。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unbound_or_inapplicable_seed": 3, "missing_claim_or_source_anchor": 4, "unrelated_or_secondary_graph_pairs_deferred": 4, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 2.979942419566214, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 51.41373168118298, "task_wall_seconds": 54.39367605885491}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0389051609672606, "calls": 19, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 18}

## RQ1_18f20020e22b

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_18f20020e22b)

Checks：[Checks-05.json](Checks-05.json)

Queries：[Queries-02.json](Queries-02.json)

Evidence：[Evidence-04.json](Evidence-04.json) · [Evidence-05.json](Evidence-05.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:292:author:1 | TeamTokensAllocation | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_ba7747b1a16fa3f7c161`，AC，units/program.sol:NEXTARIUM，字节3549＋60，决定 `unbacked_source_issuance`，证据E11,E9。The assessment concerns the policy governing the protected effect at source offset 3549. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"missing_claim_or_source_anchor": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 24.969392203725874, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 52.44019671715796, "task_wall_seconds": 77.40959144197404}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14182863663882017, "calls": 59, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_770b64940b4d

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_770b64940b4d)

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
| D2:293:author:1 | withdrawTokens | FN→FN | still_missed | 0 / no_listed_obligation_at_reference /  |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"missing_claim_or_source_anchor": 6, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 3.3066843557171524, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 44.49096674704924, "task_wall_seconds": 47.79765317309648}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 18}

## RQ1_00364c05ae79

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_00364c05ae79)

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
| D2:295:author:1 | kill | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 4, "unrelated_or_secondary_graph_pairs_deferred": 12, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 8.477760815992951, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 67.20145207643509, "task_wall_seconds": 75.67921527242288}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.024717614986002445, "calls": 9, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 52}

## RQ1_28fd11561fa6

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_28fd11561fa6)

Checks：[Checks-07.json](Checks-07.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-07.json](Evidence-07.json)

Coverage：[Coverage-03.json](Coverage-03.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:297:author:1 | initialize | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 4, "unrelated_or_secondary_graph_pairs_deferred": 2, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 2.3517269040457904, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 56.3696881220676, "task_wall_seconds": 58.721416532061994}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0002157771959900856, "calls": 1, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 9}

## RQ1_6da0b253dcb5

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_6da0b253dcb5)

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
| D2:300:author:1 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 3, "unrelated_or_secondary_graph_pairs_deferred": 2, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 2.3071592985652387, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 43.77424214920029, "task_wall_seconds": 46.08140292111784}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.021424565464258194, "calls": 8, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 10}

## RQ1_341058e186b5

任务 AC，本次未知，上批同成员报警。

[实际输入源码](InputSource-02.md#rq1_341058e186b5)

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
| D2:303:S1 | Own | TP→FN | lost | 2 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |
| D2:303:S2 | Flames | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

旧命中丢失：当前同根落在policy_missing/local_bookkeeping等判断；该局部决定进入最终未报警，非仅导出丢字。保存源内缺失职责和读者是否被错误排除须分别核，不能将旧TP当然视为科学真值。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unbound_or_inapplicable_seed": 2, "unknown_or_unshown_effect": 3, "unrelated_or_secondary_graph_pairs_deferred": 4, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 3.938258968293667, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 34.430873272009194, "task_wall_seconds": 38.369134014006704}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.019606274086982012, "calls": 8, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 22}

## RQ1_371f33f7ff6f

任务 AC，本次未知，上批同成员报警。

[实际输入源码](InputSource-02.md#rq1_371f33f7ff6f)

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
| D2:307:S1 | Ownables | TP→FN | lost | 2 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:307:S2 | MorzeF | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

旧命中丢失：当前同根落在policy_missing/local_bookkeeping等判断；该局部决定进入最终未报警，非仅导出丢字。保存源内缺失职责和读者是否被错误排除须分别核，不能将旧TP当然视为科学真值。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 17, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 7.336883923970163, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 52.081486749928445, "task_wall_seconds": 59.41837287787348}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.1160451308824122, "calls": 42, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 50}

## RQ1_4b70decadc18

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_4b70decadc18)

Checks：[Checks-13.json](Checks-13.json)

Queries：[Queries-05.json](Queries-05.json)

Evidence：[Evidence-17.json](Evidence-17.json)

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:317:author:1 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 3}

资源：{"program": {"program_investigation_seconds": 2.9359863488934934, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 60.19027351401746, "task_wall_seconds": 63.126261414028704}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.04666402889415622, "calls": 21, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 14}

## RQ1_277940cef55d

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_277940cef55d)

Checks：[Checks-07.json](Checks-07.json)

Queries：[Queries-03.json](Queries-03.json) · [Queries-04.json](Queries-04.json)

Evidence：[Evidence-07.json](Evidence-07.json)

Coverage：[Coverage-03.json](Coverage-03.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:318:author:1 | BankingPayToken | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / scope_missing,policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_facb14c4b1bc79b3af95`，AC，units/program.sol:BankingPay，字节3538＋60，决定 `unbacked_source_issuance`，证据E15,E16。The assessment concerns the policy governing the protected effect at source offset 3538 under financial_right. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 56, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 26.962155390530825, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 60.99953137245029, "task_wall_seconds": 87.96168884402141}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.5867975736036897, "calls": 73, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 139}

## RQ1_dd26f3dfb5a6

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_dd26f3dfb5a6)

Checks：[Checks-31.json](Checks-31.json)

Queries：[Queries-16.json](Queries-16.json) · [Queries-17.json](Queries-17.json)

Evidence：[Evidence-57.json](Evidence-57.json)

Coverage：[Coverage-15.json](Coverage-15.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:319:author:1 | init | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 5, "unrelated_or_secondary_graph_pairs_deferred": 9, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 9.527088002301753, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 41.85347185097635, "task_wall_seconds": 51.38056160043925}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.006647006142884493, "calls": 8, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 26}

## RQ1_852d7abd1772

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_852d7abd1772)

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
| D2:321:author:1 | withdrawTokens | FN→FN | still_missed | 0 / no_listed_obligation_at_reference /  |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"missing_claim_or_source_anchor": 4, "no_locatable_source": 2, "unrelated_or_secondary_graph_pairs_deferred": 4, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 97.51190183870494, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 61.68060562945902, "task_wall_seconds": 159.1925093079917}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 22}

## RQ1_c453f88fd0ff

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_c453f88fd0ff)

Checks：[Checks-28.json](Checks-28.json)

Queries：没有该类保存记录。

Evidence：[Evidence-47.json](Evidence-47.json)

Coverage：[Coverage-13.json](Coverage-13.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:330:author:1 | Kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.1441345219500363, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 17.508377511054277, "task_wall_seconds": 19.652513459790498}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 2}

## RQ1_9e7faad9335a

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-02.md#rq1_9e7faad9335a)

Checks：[Checks-20.json](Checks-20.json) · [Checks-21.json](Checks-21.json)

Queries：[Queries-11.json](Queries-11.json) · [Queries-12.json](Queries-12.json)

Evidence：[Evidence-32.json](Evidence-32.json)

Coverage：[Coverage-10.json](Coverage-10.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:337:S1 | transfer | FN→FN | still_missed | 5 / aligned_inspection_without_matching_alarm / policy_missing,holder_own_transfer |
| D2:337:S2 | transferFrom | FN→FN | still_missed | 7 / aligned_inspection_without_matching_alarm / holder_issued_transfer_scope,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"missing_claim_or_source_anchor": 1, "unrelated_or_secondary_graph_pairs_deferred": 55, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 77.51517545711249, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 35.7144446419552, "task_wall_seconds": 113.22962222108617}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.262438977137208, "calls": 76, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 170}
