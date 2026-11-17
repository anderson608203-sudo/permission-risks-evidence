# 逐成员审阅

[总报告](WorkReview.md) · [成员](Members.md) · [源码](Code.md)

## RQ1_f1e26706fa55

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_f1e26706fa55)

Checks：[Checks-34.json](Checks-34.json)

Queries：没有该类保存记录。

Evidence：[Evidence-62.json](Evidence-62.json)

Coverage：[Coverage-17.json](Coverage-17.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:604:author:1 | execute | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{}

资源：{"program": {"program_investigation_seconds": 2.157033943105489, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 10.140902703162283, "task_wall_seconds": 12.297940716147423}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 2}

## RQ1_e3be5dad4539

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_e3be5dad4539)

Checks：[Checks-32.json](Checks-32.json) · [Checks-33.json](Checks-33.json)

Queries：[Queries-17.json](Queries-17.json)

Evidence：[Evidence-60.json](Evidence-60.json)

Coverage：[Coverage-16.json](Coverage-16.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:606:author:1 | nexus | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_3df3cb23ad704f611317`，AC，units/program.sol:NEXUS，字节3528＋60，决定 `unbacked_source_issuance`，证据E10,E8。The assessment concerns the policy governing the protected effect at source offset 3528. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 24.66655712807551, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 48.157964304089546, "task_wall_seconds": 72.82452365010977}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14728735154494643, "calls": 59, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_af0f1c0fc521

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_af0f1c0fc521)

Checks：[Checks-22.json](Checks-22.json)

Queries：没有该类保存记录。

Evidence：[Evidence-35.json](Evidence-35.json)

Coverage：[Coverage-11.json](Coverage-11.json)

Semantics：[Semantics-07.json](Semantics-07.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:611:author:1 | press | FN→FN | still_missed | 37 / aligned_inspection_without_matching_alarm / external_dependency,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 4, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 15.749684872105718, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 53.83609383972362, "task_wall_seconds": 69.58578100195155}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 78}

## RQ1_0bcbefea1890

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_0bcbefea1890)

Checks：[Checks-04.json](Checks-04.json)

Queries：[Queries-01.json](Queries-01.json)

Evidence：[Evidence-02.json](Evidence-02.json)

Coverage：[Coverage-01.json](Coverage-01.json)

Semantics：[Semantics-01.json](Semantics-01.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:614:S1 | selfdestructs | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_aeabdf16dbc2d1c93785`，AC，units/program.sol:EncryptedToken，字节4226＋33，决定 `unbacked_source_issuance`，证据E24。The assessment concerns the policy governing the protected effect at source offset 4226. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 24, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 9.27879267418757, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 56.148430238012224, "task_wall_seconds": 65.42722493922338}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.16564687388017774, "calls": 54, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 84}

## RQ1_0e3c3362706f

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_0e3c3362706f)

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
| D2:616:author:1 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 5, "invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.3680991870351136, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 46.75999384187162, "task_wall_seconds": 49.12809453578666}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0076510184444487095, "calls": 6, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 9}

## RQ1_4580c60aec2d

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_4580c60aec2d)

Checks：[Checks-12.json](Checks-12.json) · [Checks-13.json](Checks-13.json)

Queries：[Queries-05.json](Queries-05.json)

Evidence：[Evidence-16.json](Evidence-16.json) · [Evidence-17.json](Evidence-17.json)

Coverage：[Coverage-05.json](Coverage-05.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:619:author:1 | TokenERC20 | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 157, "yield_to_source_bound_semantic_review": 1, "ambiguous_confirmation_not_a_risk_judgment": 1, "program_investigation_seconds": 1}

资源：{"program": {"program_investigation_seconds": 907.4249027171172, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 47.39681705413386, "task_wall_seconds": 954.8217246900313}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.07966949604451656, "calls": 15, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 350}

## RQ1_dee4a75fd1b4

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_dee4a75fd1b4)

Checks：[Checks-31.json](Checks-31.json)

Queries：[Queries-17.json](Queries-17.json)

Evidence：[Evidence-57.json](Evidence-57.json)

Coverage：[Coverage-15.json](Coverage-15.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:622:author:1 | init | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根2处，继承目标或重复finding在同一源发生点去重。

报警 `finding_3640c948bf9cafe6790b`，AC，units/program.sol:Vault，字节1073＋18，决定 `source_role_reassignment`，证据E11。The assessment concerns the policy governing the protected effect at source offset 1073. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

报警 `finding_dfbe3c76a66155b062ae`，AC，units/program.sol:Transferable，字节926＋19，决定 `source_role_reassignment`，证据E30,E8。The assessment concerns the policy governing the protected effect at source offset 926 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

报警 `finding_b6f437dfe62a4e83be14`，AC，units/program.sol:Transferable，字节1073＋18，决定 `source_role_reassignment`，证据E10。The assessment concerns the policy governing the protected effect at source offset 1073. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

报警 `finding_7f0ad117180d829e0670`，AC，units/program.sol:Vault，字节926＋19，决定 `source_role_reassignment`，证据E24,E4。The assessment concerns the policy governing the protected effect at source offset 926 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 10, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 4.154126258566976, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 78.73640641476959, "task_wall_seconds": 82.89053455600515}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.08961381856352091, "calls": 37, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 42}

## RQ1_5e9adf3cda8c

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_5e9adf3cda8c)

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
| D2:625:original:1 | constructor | FN→FN | still_missed | 0 / no_listed_obligation_at_reference /  |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 17}

资源：{"program": {"program_investigation_seconds": 15.25522224465385, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 49.57960971444845, "task_wall_seconds": 64.83483412396163}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0016650143079459667, "calls": 1, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 60}

## RQ1_247865e5ab88

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_247865e5ab88)

Checks：[Checks-06.json](Checks-06.json)

Queries：[Queries-03.json](Queries-03.json)

Evidence：[Evidence-07.json](Evidence-07.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:626:S1 | init | FN→FN | still_missed | 11 / aligned_inspection_without_matching_alarm / local_bookkeeping,policy_missing |
| D2:626:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:626:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:626:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"audit_effect_unbound": 2, "unrelated_or_secondary_graph_pairs_deferred": 9, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 4.35361464926973, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 59.12562543479726, "task_wall_seconds": 63.47924152575433}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.10380701767280698, "calls": 55, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 28}

## RQ1_13f2a43e4b12

任务 AC，本次报警，上批同成员报警。

[实际输入源码](InputSource-03.md#rq1_13f2a43e4b12)

Checks：[Checks-05.json](Checks-05.json)

Queries：[Queries-01.json](Queries-01.json)

Evidence：[Evidence-04.json](Evidence-04.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:322:original:1 | owned | TP→TP | retained | 3 / matched / source_role_reassignment,local_bookkeeping |
| D2:322:original:2 | requestNumber | FN→FN | still_missed | 49 / aligned_inspection_without_matching_alarm / local_bookkeeping,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

报警 `finding_03820e9ebed0f00cdf58`，AC，units/program.sol:RandomLedgerService，字节99＋18，决定 `source_role_reassignment`，证据E127,E50。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

报警 `finding_c70ab8aea2723d25920e`，AC，units/program.sol:Mortal，字节99＋18，决定 `source_role_reassignment`，证据E139,E51。The assessment concerns the policy governing the protected effect at source offset 99 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 23, "semantic_answer_outside_sent_scope": 1}

资源：{"program": {"program_investigation_seconds": 92.68146167183295, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 31.735186732839793, "task_wall_seconds": 124.41665065474808}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.10081447008997202, "calls": 48, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 84}

## RQ1_2e5ccd7b4bd2

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_2e5ccd7b4bd2)

Checks：[Checks-09.json](Checks-09.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-09.json](Evidence-09.json) · [Evidence-10.json](Evidence-10.json)

Coverage：[Coverage-03.json](Coverage-03.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:363:original:1 | fallback | FN→FN | still_missed | 30 / aligned_inspection_without_matching_alarm / policy_missing,external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"shared_declaration_in_distinct_applied_contexts": 1, "core_unresolved_retained_for_investigation": 1, "no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 51, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 20.819911590777338, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 47.930027530062944, "task_wall_seconds": 68.7499411390163}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.27359757479280233, "calls": 64, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 146}

## RQ1_2f01be3ebc82

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_2f01be3ebc82)

Checks：[Checks-09.json](Checks-09.json)

Queries：没有该类保存记录。

Evidence：[Evidence-10.json](Evidence-10.json)

Coverage：[Coverage-03.json](Coverage-03.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:94:original:1 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:94:original:2 | withdraw | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.1463784645311534, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 22.136328430380672, "task_wall_seconds": 24.2827083398588}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 4}

## RQ1_3dba1c8c9669

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_3dba1c8c9669)

Checks：[Checks-11.json](Checks-11.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-13.json](Evidence-13.json)

Coverage：[Coverage-05.json](Coverage-05.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:72:original:1 | Play | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |
| D2:72:original:2 | StartRoulette | FN→TP | gained | 2 / matched / source_role_reassignment,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

新增参考根命中已对应实际资格改写位置；不以同合约的mint/其它位置报警顶替。基础检查点已接纳首答，不能据此归因为程序独立或LLM独立增益。

报警 `finding_433b1ea8456b06934be6`，AC，units/program.sol:R，字节542＋26，决定 `source_role_reassignment`，证据E3。The assessment concerns the policy governing the protected effect at source offset 542. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_text": 2, "unrelated_or_secondary_graph_pairs_deferred": 9, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 2.80542908096686, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 62.05406582308933, "task_wall_seconds": 64.85950017301366}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.03397881519049406, "calls": 12, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 20}

## RQ1_4f65b1060e4d

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_4f65b1060e4d)

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
| D2:313:original:1 | TokenERC20 | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:313:original:2 | initialize | FN→FN | still_missed | 0 / no_listed_obligation_at_reference /  |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 1, "unrelated_or_secondary_graph_pairs_deferred": 77, "yield_to_source_bound_semantic_review": 1, "unknown_assessment_vocabulary": 1, "program_investigation_seconds": 1}

资源：{"program": {"program_investigation_seconds": 902.6233111186884, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 55.40939420834184, "task_wall_seconds": 958.0327092017978}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.06944123562425375, "calls": 11, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 195}

## RQ1_5ef9f46acd2e

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_5ef9f46acd2e)

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
| D2:54:original:1 | fallback | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:54:original:2 | debugDestruct | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_semantic_row": 1, "no_locatable_source": 2, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 2.086678826715797, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 48.51732071209699, "task_wall_seconds": 50.604001629631966}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 4}

## RQ1_7623b2a26a25

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_7623b2a26a25)

Checks：[Checks-17.json](Checks-17.json)

Queries：[Queries-09.json](Queries-09.json)

Evidence：[Evidence-25.json](Evidence-25.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:450:original:1 | StartRoulette | FN→TP | gained | 2 / matched / source_role_reassignment,policy_missing |
| D2:450:original:2 | Play | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

新增参考根命中已对应实际资格改写位置；不以同合约的mint/其它位置报警顶替。基础检查点已接纳首答，不能据此归因为程序独立或LLM独立增益。

报警 `finding_915051b0830836d8438c`，AC，units/program.sol:TestingR，字节550＋26，决定 `source_role_reassignment`，证据E1。The assessment concerns the policy governing the protected effect at source offset 550. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

诊断计数（重复记录，不是独立漏洞数）：{"unbound_or_inapplicable_seed": 2, "invalid_semantic_row": 1, "no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 9, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 2.7688837400637567, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 35.425646979827434, "task_wall_seconds": 38.19453257415444}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.03244840633124113, "calls": 12, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 20}

## RQ1_771e49570272

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_771e49570272)

Checks：[Checks-17.json](Checks-17.json)

Queries：[Queries-09.json](Queries-09.json)

Evidence：[Evidence-25.json](Evidence-25.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:421:original:1 | StartRoulette | FN→TP | gained | 2 / matched / policy_missing,source_role_reassignment |
| D2:421:original:2 | Play | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

新增参考根命中已对应实际资格改写位置；不以同合约的mint/其它位置报警顶替。基础检查点已接纳首答，不能据此归因为程序独立或LLM独立增益。

报警 `finding_111c5a70dda08eded290`，AC，units/program.sol:TestR，字节546＋26，决定 `source_role_reassignment`，证据E4。The assessment concerns the policy governing the protected effect at source offset 546. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

诊断计数（重复记录，不是独立漏洞数）：{"explicit_effect_anchor_conflict": 2, "unrelated_or_secondary_graph_pairs_deferred": 9, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 2.648594724945724, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 74.22634562011808, "task_wall_seconds": 76.87494211597368}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.035662426613271236, "calls": 12, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 20}

## RQ1_999f460049c5

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_999f460049c5)

Checks：[Checks-20.json](Checks-20.json)

Queries：[Queries-11.json](Queries-11.json)

Evidence：[Evidence-32.json](Evidence-32.json)

Coverage：[Coverage-10.json](Coverage-10.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:523:original:1 | Play | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / external_dependency |
| D2:523:original:2 | StartRoulette | FN→TP | gained | 2 / matched / policy_missing,source_role_reassignment |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

新增参考根命中已对应实际资格改写位置；不以同合约的mint/其它位置报警顶替。基础检查点已接纳首答，不能据此归因为程序独立或LLM独立增益。

报警 `finding_91c8bc0d31ec3f171b85`，AC，units/program.sol:R，字节558＋26，决定 `source_role_reassignment`，证据E2。The assessment concerns the policy governing the protected effect at source offset 558. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_check_kind": 1, "audit_source_scope_mismatch": 2, "unrelated_or_secondary_graph_pairs_deferred": 8, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 2.756120015401393, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 70.43890975555405, "task_wall_seconds": 73.19503247691318}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.060830837581306696, "calls": 20, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 20}

## RQ1_ad8d0ac6a104

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_ad8d0ac6a104)

Checks：[Checks-21.json](Checks-21.json)

Queries：[Queries-12.json](Queries-12.json)

Evidence：[Evidence-34.json](Evidence-34.json)

Coverage：[Coverage-11.json](Coverage-11.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:90:original:1 | fallback | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 10, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 5.749515174422413, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 72.06592823145911, "task_wall_seconds": 77.81544553022832}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.03157481737434864, "calls": 12, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 28}

## RQ1_b6fc6e31e760

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_b6fc6e31e760)

Checks：[Checks-26.json](Checks-26.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-42.json](Evidence-42.json) · [Evidence-43.json](Evidence-43.json) · [Evidence-44.json](Evidence-44.json) · [Evidence-45.json](Evidence-45.json)

Coverage：[Coverage-12.json](Coverage-12.json)

Semantics：[Semantics-08.json](Semantics-08.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:537:original:1 | payout | FN→FN | still_missed | 30 / aligned_inspection_without_matching_alarm / external_dependency,policy_missing |
| D2:537:original:2 | payoutSelf | FN→FN | still_missed | 5 / aligned_inspection_without_matching_alarm / policy_missing,external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 34, "yield_to_source_bound_semantic_review": 1, "program_investigation_seconds": 1}

资源：{"program": {"program_investigation_seconds": 905.3502106708474, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 73.38155094208196, "task_wall_seconds": 978.7317641139962}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 26.359296879265457, "calls": 104, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 109}
