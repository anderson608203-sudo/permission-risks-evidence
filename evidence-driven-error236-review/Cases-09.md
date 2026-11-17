# 逐成员审阅

[总报告](WorkReview.md) · [成员](Members.md) · [源码](Code.md)

## RQ1_c9b9d9ecb7bb

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_c9b9d9ecb7bb)

Checks：[Checks-28.json](Checks-28.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-50.json](Evidence-50.json)

Coverage：[Coverage-13.json](Coverage-13.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:554:author:1 | initEthMultiplicator | FN→FN | still_missed | 2 / aligned_inspection_without_matching_alarm / local_bookkeeping |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_955647f9b8a4cf1829df`，AC，units/program.sol:EthMultiplicator，字节2737＋21，决定 `unguarded_governed_effect`，证据E8。The assessment concerns the policy governing the protected effect at source offset 2737. A separate entry requires the stated incumbent to govern this same state. The located change has no corresponding guard under the stated policy. A separate entry consumes the changed qualification at the linked source location.

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_text": 1, "audit_source_scope_mismatch": 2, "no_locatable_source": 3, "unrelated_or_secondary_graph_pairs_deferred": 32, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 11.290346613619477, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 102.06807173462585, "task_wall_seconds": 113.3584203752689}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.5627871607430279, "calls": 89, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 100}

## RQ1_9c985fb01894

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_9c985fb01894)

Checks：[Checks-20.json](Checks-20.json)

Queries：[Queries-11.json](Queries-11.json)

Evidence：[Evidence-32.json](Evidence-32.json)

Coverage：[Coverage-10.json](Coverage-10.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:561:S1 | init | FN→FN | still_missed | 13 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |
| D2:561:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:561:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:561:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 2, "unrelated_or_secondary_graph_pairs_deferred": 11, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 5.191606094129384, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 100.85622553387657, "task_wall_seconds": 106.04783345106989}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.13616636861115694, "calls": 74, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 32}

## RQ1_a47200b36eb7

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_a47200b36eb7)

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
| D2:562:original:1 | Vault | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:562:original:2 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unbound_or_inapplicable_seed": 1, "unrelated_or_secondary_graph_pairs_deferred": 6}

资源：{"program": {"program_investigation_seconds": 2.9478808832354844, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 53.583412661682814, "task_wall_seconds": 56.53129560314119}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.044098337180912495, "calls": 25, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 17}

## RQ1_81d27b74b2b8

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_81d27b74b2b8)

Checks：[Checks-17.json](Checks-17.json) · [Checks-18.json](Checks-18.json)

Queries：[Queries-10.json](Queries-10.json)

Evidence：[Evidence-26.json](Evidence-26.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:565:author:1 | ownerOf | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 23, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 8.311756039503962, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 61.11217831354588, "task_wall_seconds": 69.42393696308136}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.04753713821992278, "calls": 29, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 50}

## RQ1_934ccafdf988

任务 AC，本次报警，上批同成员报警。

[实际输入源码](InputSource-03.md#rq1_934ccafdf988)

Checks：[Checks-18.json](Checks-18.json)

Queries：[Queries-10.json](Queries-10.json)

Evidence：[Evidence-28.json](Evidence-28.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:567:S1 | mortal | TP→TP | retained | 2 / matched / source_role_reassignment |
| D2:567:S2 | thing | FN→FN | still_missed | 0 / no_aligned_inspection_in_obligations /  |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

报警 `finding_e10f90ad486d7ad44bb4`，AC，units/program.sol:Thing，字节76＋18，决定 `source_role_reassignment`，证据E2。The assessment concerns the policy governing the protected effect at source offset 76. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

报警 `finding_1386d33b8eabb1307c37`，AC，units/program.sol:Mortal，字节76＋18，决定 `source_role_reassignment`，证据E1。The assessment concerns the policy governing the protected effect at source offset 76. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 1, "explicit_effect_anchor_conflict": 1}

资源：{"program": {"program_investigation_seconds": 2.5941090444102883, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 70.38210570067167, "task_wall_seconds": 72.97621640563011}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.04351475229486823, "calls": 19, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 11}

## RQ1_bc14311821a2

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_bc14311821a2)

Checks：[Checks-27.json](Checks-27.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-45.json](Evidence-45.json)

Coverage：[Coverage-13.json](Coverage-13.json)

Semantics：[Semantics-08.json](Semantics-08.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:571:S1 | selfdestructs | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_d6809b461f01409e568b`，AC，units/program.sol:MyAdvancedToken，字节4332＋33，决定 `unbacked_source_issuance`，证据E17。The assessment concerns the policy governing the protected effect at source offset 4332. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"shared_declaration_in_distinct_applied_contexts": 4, "no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 34, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 12.11286906292662, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 73.52791814506054, "task_wall_seconds": 85.64079105295241}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.28507262701168656, "calls": 84, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 107}

## RQ1_e5e40ec6feca

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_e5e40ec6feca)

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
| D2:572:author:1 | destroy | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.069288835860789, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 21.78393005905673, "task_wall_seconds": 23.853220318909734}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 3}

## RQ1_7fcdff67fecb

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_7fcdff67fecb)

Checks：[Checks-17.json](Checks-17.json)

Queries：[Queries-09.json](Queries-09.json) · [Queries-10.json](Queries-10.json)

Evidence：[Evidence-25.json](Evidence-25.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:574:S1 | initVault | FN→TP | gained | 11 / matched / policy_missing,program_support,local_bookkeeping |
| D2:574:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:574:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:574:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

新增参考根命中已对应实际资格改写位置；不以同合约的mint/其它位置报警顶替。基础检查点已接纳首答，不能据此归因为程序独立或LLM独立增益。

报警 `finding_1226c36c4e15704683af`，AC，units/program.sol:Vault，字节1225＋18，决定 `program_support`，证据E2,E30。At initVault(), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification.

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 7, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 4.939428378362209, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 74.0626533003524, "task_wall_seconds": 79.0020837369375}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.12136489525437355, "calls": 69, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 25}

## RQ1_3d5f2e705184

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_3d5f2e705184)

Checks：[Checks-10.json](Checks-10.json) · [Checks-11.json](Checks-11.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-12.json](Evidence-12.json) · [Evidence-13.json](Evidence-13.json)

Coverage：[Coverage-05.json](Coverage-05.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:577:author:1 | TokenERC20 | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 157, "yield_to_source_bound_semantic_review": 1, "unknown_assessment_vocabulary": 1, "program_investigation_seconds": 1}

资源：{"program": {"program_investigation_seconds": 909.8514899411239, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 38.86654028389603, "task_wall_seconds": 948.7180341687053}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.04627680592238903, "calls": 15, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 352}

## RQ1_7c1aa3f1640a

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_7c1aa3f1640a)

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
| D2:579:author:1 | destroycontract | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 17, "invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 13.525194467511028, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 62.65446779318154, "task_wall_seconds": 76.17966463696212}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.07472450938075781, "calls": 29, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 45}

## RQ1_3daa3272da3f

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_3daa3272da3f)

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
| D2:580:S1 | selfdestructs | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_8504d7c746fe1b294585`，AC，units/program.sol:EncryptedToken，字节4226＋33，决定 `unbacked_source_issuance`，证据E24。The assessment concerns the policy governing the protected effect at source offset 4226. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 24, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 9.504894569981843, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 29.53265397809446, "task_wall_seconds": 39.037550365086645}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.16497187968343496, "calls": 54, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 84}

## RQ1_baecb1a287ec

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_baecb1a287ec)

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
| D2:584:S1 | initVault | FN→FN | still_missed | 10 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |
| D2:584:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:584:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:584:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"invalid_semantic_row": 2, "no_locatable_source": 4, "unrelated_or_secondary_graph_pairs_deferred": 11, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 5.268467457033694, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 67.2499812268652, "task_wall_seconds": 72.51845041662455}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.14652871200814843, "calls": 70, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 32}

## RQ1_991cdff3e261

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_991cdff3e261)

Checks：[Checks-20.json](Checks-20.json)

Queries：[Queries-11.json](Queries-11.json)

Evidence：[Evidence-31.json](Evidence-31.json) · [Evidence-32.json](Evidence-32.json)

Coverage：[Coverage-10.json](Coverage-10.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:586:author:1 | Legendary | FN→FN | still_missed | 4 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_306da1974ad146764967`，AC，units/program.sol:YoloChips，字节3516＋60，决定 `unbacked_source_issuance`，证据E11,E8。The assessment concerns the policy governing the protected effect at source offset 3516. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1, "unrelated_or_secondary_graph_pairs_deferred": 56, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 25.785012694075704, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 98.43416295479983, "task_wall_seconds": 124.21917749708518}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.15915064932778478, "calls": 58, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 141}

## RQ1_fa317176bacc

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_fa317176bacc)

Checks：[Checks-35.json](Checks-35.json)

Queries：[Queries-18.json](Queries-18.json)

Evidence：[Evidence-66.json](Evidence-66.json)

Coverage：[Coverage-17.json](Coverage-17.json)

Semantics：[Semantics-11.json](Semantics-11.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:588:S1 | init | FN→FN | still_missed | 11 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |
| D2:588:S2 | setRelease | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |
| D2:588:S3 | lock | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:588:S4 | kill | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"missing_claim_or_source_anchor": 1, "unrelated_or_secondary_graph_pairs_deferred": 9, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 4.514357843436301, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 60.997118999715894, "task_wall_seconds": 65.51147877797484}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.09949481161311269, "calls": 53, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 28}

## RQ1_8b881d18ff63

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_8b881d18ff63)

Checks：[Checks-18.json](Checks-18.json)

Queries：[Queries-10.json](Queries-10.json)

Evidence：[Evidence-26.json](Evidence-26.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:589:author:1 | WorldSafetySecurityToken | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_95208cbee38c30932e1c`，AC，units/program.sol:OneExchangeToken，字节4560＋33，决定 `unbacked_source_issuance`，证据E35。The assessment concerns the policy governing the protected effect at source offset 4560. The caller chooses an unbacked positive credit on an independently spendable account, outside the ledger's ordinary exchange or allocation terms.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 36, "ambiguous_confirmation_not_a_risk_judgment": 1}

资源：{"program": {"program_investigation_seconds": 15.105465868953615, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 69.05010569887236, "task_wall_seconds": 84.15557336201891}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.2278383239172399, "calls": 74, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 117}

## RQ1_50afc53073f9

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_50afc53073f9)

Checks：[Checks-13.json](Checks-13.json) · [Checks-14.json](Checks-14.json)

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
| D2:594:author:1 | initialWittness | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 2, "unrelated_or_secondary_graph_pairs_deferred": 48}

资源：{"program": {"program_investigation_seconds": 50.02610329864547, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 50.17018837016076, "task_wall_seconds": 100.1962936297059}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.009175613522529602, "calls": 4, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 164}

## RQ1_45ce1fe8110b

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_45ce1fe8110b)

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
| D2:596:author:1 | IotaGoldToken | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / local_bookkeeping,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_issue_kind": 1, "audit_source_scope_mismatch": 3, "unrelated_or_secondary_graph_pairs_deferred": 10, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 14.138036228716373, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 53.7777329524979, "task_wall_seconds": 67.91577072022483}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 32}

## RQ1_be17ecaef698

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_be17ecaef698)

Checks：[Checks-27.json](Checks-27.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-46.json](Evidence-46.json)

Coverage：[Coverage-13.json](Coverage-13.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:597:author:1 | clearBlockchain | FN→FN | still_missed | 3 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根1处，继承目标或重复finding在同一源发生点去重。

报警 `finding_537518ffcc53cd5d955c`，AC，units/program.sol:WhoWillRuleWesterosAtTheEnd，字节3242＋17，决定 `unguarded_governed_effect`，证据E13。The assessment concerns the policy governing the protected effect at source offset 3242. A separate entry requires the stated incumbent to govern this same state. The located change has no corresponding guard under the stated policy. A separate entry consumes the changed qualification at the linked source location.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 3, "unrelated_or_secondary_graph_pairs_deferred": 37, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 13.341121340170503, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 112.11453294195235, "task_wall_seconds": 125.45565607119352}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.10528997424989939, "calls": 41, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 123}

## RQ1_5ee0702dae51

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_5ee0702dae51)

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
| D2:598:author:1 | destroy | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 4, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 3.411535673774779, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 70.67169627407566, "task_wall_seconds": 74.08323368011042}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.025177482049912214, "calls": 6, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 14}

## RQ1_52d5c754a744

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_52d5c754a744)

Checks：[Checks-14.json](Checks-14.json)

Queries：[Queries-06.json](Queries-06.json)

Evidence：[Evidence-18.json](Evidence-18.json) · [Evidence-19.json](Evidence-19.json)

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:601:original:1 | BlocksureInfo | FN→FN | still_missed | 0 / no_listed_obligation_at_reference /  |
| D2:601:original:2 | onlyowner | FN→FN | still_missed | 0 / no_bound_window /  |

本成员参考外报警根3处，继承目标或重复finding在同一源发生点去重。

报警 `finding_cdc7722963df4d7bc6c2`，AC，units/program.sol:BlocksureInfo，字节329＋22，决定 `scoped_semantic_conflict`，证据E1,E4,E7。The assessment concerns the policy governing the protected effect at source offset 329. The located duty and the deciding caller conflict at this applied source effect; this is a scoped semantic prediction.

报警 `finding_4b6e3a6ced9522aeaa19`，AC，units/program.sol:BlocksureInfo，字节417＋14，决定 `program_support`，证据E2,E5。At setOwner(address), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification.

报警 `finding_acacf23afa8c83c47676`，AC，units/program.sol:BlocksureInfo，字节557＋14，决定 `scoped_semantic_conflict`，证据E3,E6。The assessment concerns the policy governing the protected effect at source offset 557. The located duty and the deciding caller conflict at this applied source effect; this is a scoped semantic prediction.

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 2.3884995658881962, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 32.28342304797843, "task_wall_seconds": 34.67192719783634}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.018481913954019547, "calls": 7, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 7}
