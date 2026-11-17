# 逐成员审阅

[总报告](WorkReview.md) · [成员](Members.md) · [源码](Code.md)

## RQ1_c60bf13e0ef3

任务 AC，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_c60bf13e0ef3)

Checks：[Checks-28.json](Checks-28.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-47.json](Evidence-47.json) · [Evidence-48.json](Evidence-48.json) · [Evidence-49.json](Evidence-49.json) · [Evidence-50.json](Evidence-50.json)

Coverage：[Coverage-13.json](Coverage-13.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:176:original:1 | payout | FN→FN | still_missed | 30 / aligned_inspection_without_matching_alarm / external_dependency,policy_missing |
| D2:176:original:2 | payoutSelf | FN→FN | still_missed | 5 / aligned_inspection_without_matching_alarm / external_dependency,policy_missing |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 93, "semantic_answer_outside_sent_scope": 1}

资源：{"program": {"program_investigation_seconds": 144.73907934688032, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 19.21378742903471, "task_wall_seconds": 163.95286904275417}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.7331934706307948, "calls": 41, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 189}

## RQ1_d639862f5b71

任务 AC，本次报警，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_d639862f5b71)

Checks：[Checks-30.json](Checks-30.json) · [Checks-31.json](Checks-31.json)

Queries：[Queries-16.json](Queries-16.json)

Evidence：[Evidence-55.json](Evidence-55.json) · [Evidence-56.json](Evidence-56.json)

Coverage：[Coverage-15.json](Coverage-15.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

| 作者根 | 函数 | 原→本次 | 变化 | 检查/可观察断点 |
|---|---|---|---|---|
| D2:427:original:1 | setOwner | FN→TP | gained | 5 / matched / policy_missing,local_bookkeeping,source_role_reassignment |
| D2:427:original:2 | setExecutor | FN→FN | still_missed | 5 / aligned_inspection_without_matching_alarm / policy_missing,local_bookkeeping |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

新增参考根命中已对应实际资格改写位置；不以同合约的mint/其它位置报警顶替。基础检查点已接纳首答，不能据此归因为程序独立或LLM独立增益。

报警 `finding_6e3b17e6dfa3356eaad8`，AC，units/program.sol:ITGToken，字节6608＋14，决定 `source_role_reassignment`，证据E136,E2。The assessment concerns the policy governing the protected effect at source offset 6608 under current_authority_required. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification. A separate entry consumes the changed qualification at the linked source location.

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 74, "unknown_assessment_vocabulary": 1}

资源：{"program": {"program_investigation_seconds": 175.34218169748783, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 42.350007116794586, "task_wall_seconds": 217.69219121010974}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.24718737229704857, "calls": 57, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 191}

## RQ1_e6f04047bff4

任务 AC，本次未知，上批同成员报警。

[实际输入源码](InputSource-03.md#rq1_e6f04047bff4)

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
| D2:37:original:1 | RegisterDevice | TP→FN | lost | 1 / aligned_inspection_without_matching_alarm / local_bookkeeping |
| D2:37:original:2 | CollectMoney | FN→FN | still_missed | 1 / aligned_inspection_without_matching_alarm / external_dependency |

本成员参考外报警根0处，继承目标或重复finding在同一源发生点去重。

旧命中丢失：当前同根落在policy_missing/local_bookkeeping等判断；该局部决定进入最终未报警，非仅导出丢字。保存源内缺失职责和读者是否被错误排除须分别核，不能将旧TP当然视为科学真值。

无报警不代表安全。当前逐根检查和正常反证只按保存记录列出，未对未保存原答补造语义。

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 1, "unrelated_or_secondary_graph_pairs_deferred": 1}

资源：{"program": {"program_investigation_seconds": 2.498584418091923, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 42.08767282869667, "task_wall_seconds": 44.586260282900184}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.025827315635979176, "calls": 6, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 7}

## RQ1_58de46f081ec

任务 FCR，本次未检出，上批同成员未检出。

[实际输入源码](InputSource-03.md#rq1_58de46f081ec)

Checks：[Checks-14.json](Checks-14.json)

Queries：[Queries-06.json](Queries-06.json)

Evidence：[Evidence-20.json](Evidence-20.json)

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_2046acc1c802不在本批；不产生新的整对正确成绩。

指定FREEZE仍未报警。已核的incoming_only、脱接helper或普通同权益旁路不能为了参考标签造边；保留参考FN，源码结论与作者标签的分歧单列。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：58de46f081ec｜N/14｜KDA基类公开transfer/transferFrom内联扣记，派生带freeze的_transfer未被调用，独立MINT存在｜维持脱接作用反证，保护MINT。不造边。

指定检查理由：{}；其它类报警：FCR-MINT。其它类不能抵销指定类FN。

报警 `finding_2714c51b5cbb8af2bb45`，FCR-MINT，units/program.sol:KDA，字节6570＋33，决定 `new_entitlement`，证据E2。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6570. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 1, "invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 7.777697864919901, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 58.87433188594878, "task_wall_seconds": 66.65203152270988}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.044862942304462194, "calls": 14, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 17}

## RQ1_328c13393c2c

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_328c13393c2c)

Checks：[Checks-09.json](Checks-09.json)

Queries：[Queries-04.json](Queries-04.json)

Evidence：[Evidence-11.json](Evidence-11.json)

Coverage：[Coverage-04.json](Coverage-04.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_d46f18d3b64e不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：328c13393c2c｜U/67｜RoxToken；burn第323行扣caller自身；salvageTokensFromContract及killContract分别涉及外部资产/终止；scope_missing与外调缺口共存｜隔离无关回调可以修，但自身burn不能升级为他人销毁；终止/外部资产须按已批准实际权益语义另核，未确认可追回。

指定检查理由：{"scope_missing": 2}；其它类报警：FCR-MINT,FCR-PAUSE。其它类不能抵销指定类FN。

报警 `finding_a2a0721b1fb6ea4af0f3`，FCR-PAUSE，units/program.sol:ERC20Token，字节2246＋236，决定 `program_support`，证据E15,E16,E17,E3,E5。At lockUntil(uint256,string), the checked privileged change restricts the outgoing right of ordinary holders for an otherwise usable request within the recorded domain.

报警 `finding_a9c0c28412e8be14046b`，FCR-MINT，units/program.sol:ERC20Token，字节9544＋928，决定 `program_support`，证据E23,E45,E47,E49,E7。At mint(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

报警 `finding_b0eb1f1fc4705ac7f6af`，FCR-PAUSE，units/program.sol:RoxToken，字节2246＋236，决定 `program_support`，证据E19,E20,E21,E4,E6。At lockUntil(uint256,string), the checked privileged change restricts the outgoing right of ordinary holders for an otherwise usable request within the recorded domain.

报警 `finding_ef1f3ce3a938a62884ff`，FCR-MINT，units/program.sol:RoxToken，字节9544＋928，决定 `program_support`，证据E11,E24,E38,E46,E50。At mint(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 2}

资源：{"program": {"program_investigation_seconds": 18.44032620685175, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 44.49411688372493, "task_wall_seconds": 62.93444726476446}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.268457833211869, "calls": 57, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 44}

## RQ1_81a85f242b60

任务 FCR，本次未知，上批同成员报警。

[实际输入源码](InputSource-03.md#rq1_81a85f242b60)

Checks：[Checks-17.json](Checks-17.json)

Queries：[Queries-10.json](Queries-10.json)

Evidence：[Evidence-26.json](Evidence-26.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-MINT与repair参考评价，配对成员RQ1_b61f163309a1不在本批；不产生新的整对正确成绩。

原指定MINT报警撤回，但当前仍scope_missing，未得到有效阴性；同次购买反证尚未使整类别完成判断，不能计TN或有效FP纠正。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：81a85f242b60｜DappToken，op_4e1c20df49c8b5b987a8，字节5099/361｜post_exclusion的probe_1711bf7f32532c659ed1及financial_value的probe_af0a41756ff206c4cc09均SAT。修同次付款购买与自由发行的适用边界。

指定检查理由：{"scope_missing": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 2}

资源：{"program": {"program_investigation_seconds": 8.426739118993282, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 23.43201821902767, "task_wall_seconds": 31.858760294038802}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.11898852931335568, "calls": 22, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 16}

## RQ1_5b3469baa447

任务 FCR，本次报警，上批同成员未检出。

[实际输入源码](InputSource-03.md#rq1_5b3469baa447)

Checks：[Checks-15.json](Checks-15.json)

Queries：[Queries-06.json](Queries-06.json)

Evidence：[Evidence-20.json](Evidence-20.json)

Coverage：[Coverage-07.json](Coverage-07.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 报警 → initial 报警 → feedback 报警 → report 报警

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_7a7815b00180不在本批；不产生新的整对正确成绩。

本批实际scoped_final_holder_loss得到SAT且uncompensated_debit被compose消费，最终指定DESTROY报警。原owner受控、同holder余额/供应下降的源码相同，是本批唯一指定FCR风险端新增命中。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：5b3469baa447｜N/12｜CSC burnFrom第45行，owner守卫，指定holder余额与总供应下降，同时清lockedBalances；op_0f5bb77df0045e5c93bb、源码字节1755/382；多项DESTROY检查仍scope_missing，覆盖却reviewed/source_task_reading｜优先工程修复。确认阴性依据不足；直接扣减、角色和金额guard需一起接通，不能只将N改U算完成。

指定检查理由：{"uncompensated_debit": 6, "scope_missing": 2}；其它类报警：。其它类不能抵销指定类FN。

报警 `finding_c2e4a7c18bd0488d9849`，FCR-DESTROY，units/program.sol:CSC，字节2011＋24，决定 `uncompensated_debit`，证据E15,E18,E22,E26,E29,E32。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 2011 under financial_right. The qualified operation reduces another holder's position without a matching credit on this source branch.

诊断计数（重复记录，不是独立漏洞数）：{"invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 61.75029027508572, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 62.06649806397036, "task_wall_seconds": 123.81679104408249}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.34568467224016786, "calls": 50, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 55}

## RQ1_f922252cd038

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_f922252cd038)

Checks：[Checks-35.json](Checks-35.json)

Queries：[Queries-18.json](Queries-18.json)

Evidence：[Evidence-66.json](Evidence-66.json)

Coverage：[Coverage-17.json](Coverage-17.json)

Semantics：[Semantics-11.json](Semantics-11.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_c58fa03a9316不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：f922252cd038｜U/101｜ApodTokenContract；burn第322行仍为caller自身，killContract第361行终止，外部资产回调未闭合｜与328c同族处理。未证明存在可按当前定义报告的独立第三方净毁损，不承诺报警。

指定检查理由：{"scope_missing": 2}；其它类报警：FCR-MINT,FCR-PAUSE。其它类不能抵销指定类FN。

报警 `finding_233790bb0cedd334a065`，FCR-MINT，units/program.sol:ERC20Token，字节9509＋921，决定 `program_support`，证据E11,E24,E38,E46,E50。At mint(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

报警 `finding_439cca4a3b4cba01c788`，FCR-MINT，units/program.sol:ApodTokenContract，字节9509＋921，决定 `program_support`，证据E23,E45,E47,E49,E7。At mint(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

报警 `finding_28818d4b2ae94468de88`，FCR-PAUSE，units/program.sol:ERC20Token，字节2246＋236，决定 `program_support`，证据E19,E20,E21,E4,E6。At lockUntil(uint256,string), the checked privileged change restricts the outgoing right of ordinary holders for an otherwise usable request within the recorded domain.

报警 `finding_000383d634ff6daad733`，FCR-PAUSE，units/program.sol:ApodTokenContract，字节2246＋236，决定 `program_support`，证据E15,E16,E17,E3,E5。At lockUntil(uint256,string), the checked privileged change restricts the outgoing right of ordinary holders for an otherwise usable request within the recorded domain.

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 3, "unrelated_or_secondary_graph_pairs_deferred": 2}

资源：{"program": {"program_investigation_seconds": 18.485630931332707, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 63.59517176775262, "task_wall_seconds": 82.08080834010616}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.2815892156213522, "calls": 60, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 44}

## RQ1_0c8823eed851

任务 FCR，本次未检出，上批同成员未检出。

[实际输入源码](InputSource-03.md#rq1_0c8823eed851)

Checks：[Checks-04.json](Checks-04.json)

Queries：[Queries-01.json](Queries-01.json)

Evidence：[Evidence-02.json](Evidence-02.json)

Coverage：[Coverage-01.json](Coverage-01.json)

Semantics：[Semantics-01.json](Semantics-01.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未检出 → report 未检出

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_7ca60ff656fc不在本批；不产生新的整对正确成绩。

指定FREEZE仍未报警。已核的incoming_only、脱接helper或普通同权益旁路不能为了参考标签造边；保留参考FN，源码结论与作者标签的分歧单列。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：0c8823eed851｜N/0｜CalorieCoin实际检查当前为incoming_only｜未确认同holder普通出账受阻，不强报FREEZE。若有其他真实出账条件需分别核。

指定检查理由：{"incoming_only": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 1}

资源：{"program": {"program_investigation_seconds": 4.447219273075461, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 59.98360197385773, "task_wall_seconds": 64.43082468118519}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.009856420569121838, "calls": 2, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 1}

## RQ1_b472a9a0647e

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_b472a9a0647e)

Checks：[Checks-24.json](Checks-24.json)

Queries：[Queries-12.json](Queries-12.json) · [Queries-13.json](Queries-13.json) · [Queries-14.json](Queries-14.json) · [Queries-15.json](Queries-15.json)

Evidence：[Evidence-39.json](Evidence-39.json) · [Evidence-40.json](Evidence-40.json) · [Evidence-41.json](Evidence-41.json) · [Evidence-42.json](Evidence-42.json)

Coverage：[Coverage-12.json](Coverage-12.json)

Semantics：[Semantics-07.json](Semantics-07.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_1ffb833b5da1不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：b472a9a0647e｜U/463｜ColorCoin；balance用途聚合accounts与investors.lockedAmount；distribute/doUnlock_Admin包含锁仓与可用账目迁移，循环残余｜最终权益必须合并同人可得余额，不能把lockedAmount单降当净毁损。存在实现范围缺口，尚未确认具体无补偿损失。

指定检查理由：{"scope_missing": 4}；其它类报警：FCR-MINT。其它类不能抵销指定类FN。

报警 `finding_7b9e93381ed020bfc088`，FCR-MINT，units/program.sol:ColorCoin，字节34852＋545，决定 `program_support`，证据E137,E192,E197,E202,E206,E230,E234,E246,E248,E258,E260,E270,E272,E282,E284,E294,E296,E306,E308,E59。At sendCoinsForPixels(uint32,address), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

报警 `finding_0771b8ac62cdeee02a0d`，FCR-MINT，units/program.sol:ColorCoinWithPixel，字节34852＋545，决定 `program_support`，证据E138,E175,E198,E211,E223,E233,E241,E247,E253,E259,E265,E271,E277,E283,E289,E295,E301,E307,E313,E69。At sendCoinsForPixels(uint32,address), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 10, "noncached_action_limit": 1}

资源：{"program": {"program_investigation_seconds": 531.062785001006, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 35.73602983402088, "task_wall_seconds": 566.7988205468282}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 2.997126224450767, "calls": 471, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 258}

## RQ1_5b3c7cbe3d9d

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_5b3c7cbe3d9d)

Checks：[Checks-15.json](Checks-15.json)

Queries：[Queries-06.json](Queries-06.json) · [Queries-07.json](Queries-07.json)

Evidence：[Evidence-20.json](Evidence-20.json) · [Evidence-21.json](Evidence-21.json)

Coverage：[Coverage-07.json](Coverage-07.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_0f3c3f400f6f不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：5b3c7cbe3d9d｜U/83｜AdvanceToken基类transfer第171行/transferFrom第191行不读冻结状态，派生_transfer第253行才读；当前source_unit_missing来自局部管理作用｜普通同账本旁路已可见。修索引/作用范围可改善解释与覆盖，不保证转为TP。

指定检查理由：{"scope_missing": 3}；其它类报警：FCR-MINT,FCR-DESTROY,FCR-PAUSE。其它类不能抵销指定类FN。

报警 `finding_5d8b72f4a756d5b07e79`，FCR-MINT，units/program.sol:AdvanceToken，字节11956＋426，决定 `program_support`，证据E1,E118,E119,E125,E126,E129,E130,E133,E134,E22,E46,E47。At mintToken(uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

报警 `finding_c91b434d386be596e52f`，FCR-DESTROY，units/program.sol:AdvanceToken，字节11956＋426，决定 `program_support`，证据E100,E107,E136,E142,E144,E2,E23,E64,E65,E87,E88,E95,E96,E99。The change at mintToken(uint256) affects the same holder request at burnFrom(address,uint256). The checked difference is an uncompensated reduction of existing rights under the applicable consent.

报警 `finding_5804ef2bf59ed8064a96`，FCR-PAUSE，units/program.sol:BaseToken，字节2851＋13，决定 `productive_outgoing_control`，证据E29,E33,E42,E43。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2851. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger.

报警 `finding_f59e2a768222edb91ed7`，FCR-DESTROY，units/program.sol:AdvanceToken，字节14374＋47，决定 `uncompensated_debit`，证据E10,E19,E5。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 14374. The qualified operation reduces another holder's position without a matching credit on this source branch.

报警 `finding_96fec5d6d213a7f43a45`，FCR-MINT，units/program.sol:AdvanceToken，字节14128＋402，决定 `program_support`，证据E102,E106,E11,E113,E132,E135,E137,E140,E148,E150,E151,E152,E156,E157,E158,E20,E6,E86,E90,E94,E98。The change at burnFrom(address,uint256) affects the same holder request at mintToken(uint256). The checked difference is a new positive entitlement for a controlled beneficiary.

报警 `finding_6377af52105762f54d0c`，FCR-MINT，units/program.sol:AdvanceToken，字节13719＋403，决定 `program_support`，证据E105,E112,E116,E120,E138,E36,E93。The change at burn(uint256) affects the same holder request at mintToken(uint256). The checked difference is a new positive entitlement for a controlled beneficiary.

报警 `finding_a553abccd7b6476ca200`，FCR-PAUSE，units/program.sol:AdvanceToken，字节2851＋13，决定 `productive_outgoing_control`，证据E26,E30,E40,E41。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2851. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger.

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 2, "unrelated_or_secondary_graph_pairs_deferred": 13, "invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 41.074822023976594, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 54.96117929182947, "task_wall_seconds": 96.03600402409211}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.3076135339215398, "calls": 93, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 128}

## RQ1_5ab05cf437b3

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_5ab05cf437b3)

Checks：[Checks-14.json](Checks-14.json)

Queries：[Queries-06.json](Queries-06.json)

Evidence：[Evidence-20.json](Evidence-20.json)

Coverage：[Coverage-07.json](Coverage-07.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_c46de9c5394e不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：5ab05cf437b3｜U/41｜BimCoin基类transfer第75行/transferFrom第96行不读冻结，派生_transfer第167行读冻结；另有buy/oracle依赖｜分开普通旁路与购买外部依赖，不因oracle未知否决已核旁路，也不据此宣称整合约安全。

指定检查理由：{"scope_missing": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 3, "unrelated_or_secondary_graph_pairs_deferred": 6}

资源：{"program": {"program_investigation_seconds": 24.939559746999294, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 44.332369981799275, "task_wall_seconds": 69.27193378889933}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 3.61965193413198, "calls": 41, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 41}

## RQ1_33d48945207e

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_33d48945207e)

Checks：[Checks-09.json](Checks-09.json)

Queries：没有该类保存记录。

Evidence：[Evidence-11.json](Evidence-11.json)

Coverage：[Coverage-04.json](Coverage-04.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_6ca2b0aeda43不在本批；不产生新的整对正确成绩。

未进入实际求解，指定类候选/检查与权益或普通出账消费者仍有结构接线缺口；增加solver时间不能解决零查询本身。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：33d48945207e｜U/0｜CREDITS；burn第196行本人销毁，burnFrom第209行核并消耗allowance[from][caller]，复杂Frozen路径同在｜角色/复合路径可修，但已有自愿/额度反证不能丢。PAUSE成立也不能顶替DESTROY；未确认该参考FN可追回。

指定检查理由：{"scope_missing": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 1, "Unsupported:source_semantics_unavailable:path_85b2849dece1deace263": 7, "unrelated_or_secondary_graph_pairs_deferred": 3}

资源：{"program": {"program_investigation_seconds": 63.023279197048396, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 49.88343671290204, "task_wall_seconds": 112.90671899914742}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 55}

## RQ1_65379f53b3ab

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-03.md#rq1_65379f53b3ab)

Checks：[Checks-15.json](Checks-15.json)

Queries：没有该类保存记录。

Evidence：[Evidence-22.json](Evidence-22.json)

Coverage：[Coverage-07.json](Coverage-07.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_a4df6c5b7701不在本批；不产生新的整对正确成绩。

未进入实际求解，指定类候选/检查与权益或普通出账消费者仍有结构接线缺口；增加solver时间不能解决零查询本身。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：65379f53b3ab｜U/0｜SadeIT公开transfer/transferFrom真实消费_Sfiyy及_marketajcount等费率/豁免，非简单bool；0次solver｜工程上需数值控制/正额可用基线及豁免消费。高费是否阻断所有适用正额请求仍未核，不能把费率变化直接当FREEZE。

指定检查理由：{"scope_missing": 2}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1}

资源：{"program": {"program_investigation_seconds": 29.511247577611357, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 14.996961390133947, "task_wall_seconds": 44.50821145577356}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 7}

## RQ1_7cc11a697bd2

任务 FCR，本次未知，上批同成员报警。

[实际输入源码](InputSource-03.md#rq1_7cc11a697bd2)

Checks：[Checks-17.json](Checks-17.json)

Queries：[Queries-09.json](Queries-09.json)

Evidence：[Evidence-25.json](Evidence-25.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-MINT与repair参考评价，配对成员RQ1_3421c09bc85c不在本批；不产生新的整对正确成绩。

原指定MINT报警撤回，但当前仍scope_missing，未得到有效阴性；同次购买反证尚未使整类别完成判断，不能计TN或有效FP纠正。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：7cc11a697bd2｜AGGToken，op_10f20d68fc821801b4a3，字节5232/373｜probe_7a653634f52d62f2b78a及probe_72855ee598a0602b8aaf分别为上述两类SAT查询。同一通用修复，保留独立回执。

指定检查理由：{"scope_missing": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{}

资源：{"program": {"program_investigation_seconds": 9.555242109112442, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 36.03296417882666, "task_wall_seconds": 45.58821047004312}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.17395924776792526, "calls": 34, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 25}

## RQ1_55a1e2ef0f09

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_55a1e2ef0f09)

Checks：[Checks-14.json](Checks-14.json)

Queries：[Queries-06.json](Queries-06.json)

Evidence：[Evidence-19.json](Evidence-19.json)

Coverage：[Coverage-06.json](Coverage-06.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_fe4ace2cd8e5不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：55a1e2ef0f09｜U/47｜FuelToken；finalizeCrowdfund第379行由crowdfundAddress调用，将其余额移至platformAddress；并非“余额清零且总供应减少”；分配/解锁还含其他残余｜优先区分caller自有处分、募集储备转付及持有人真正损失。不能把这一转付写成销毁；其余作用尚未闭合，保留未核范围。

指定检查理由：{"scope_missing": 10}；其它类报警：FCR-MINT。其它类不能抵销指定类FN。

报警 `finding_5c4a05f49ec8ba9741e5`，FCR-MINT，units/program.sol:FuelToken，字节8249＋503，决定 `program_support`，证据E126,E127,E129,E13,E130,E132,E133,E143,E145,E147,E15,E179,E180,E181,E197,E20,E203,E204,E3,E35,E44,E47,E50,E53,E55,E58,E8,E83,E86,E89。The change at setCrowdfundAddress(address) affects the same holder request at transferFromCrowdfund(address,uint256). The checked difference is a new positive entitlement for a controlled beneficiary.

报警 `finding_23e81353770fce24f349`，FCR-MINT，units/program.sol:FuelToken，字节8758＋876，决定 `program_support`，证据E41,E52,E73,E88,E94。At transferFromCrowdfund(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 6, "invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 53.647265944164246, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 64.56243145279586, "task_wall_seconds": 118.20969985006377}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.2758289915509522, "calls": 66, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 172}

## RQ1_8921e5cc1831

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_8921e5cc1831)

Checks：[Checks-18.json](Checks-18.json)

Queries：[Queries-10.json](Queries-10.json)

Evidence：[Evidence-26.json](Evidence-26.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_d1c797e20951不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：8921e5cc1831｜U/3｜FAC派生transfer(from,to,value)第174行是三参数重载；继承两参数第70行与transferFrom第93行无冻结读取｜真实普通旁路明确，三参数受限不能替代整个权益冻结。

指定检查理由：{"scope_missing": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 1}

资源：{"program": {"program_investigation_seconds": 6.206085918471217, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 16.02640754636377, "task_wall_seconds": 22.2324956250377}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.03850898053497076, "calls": 10, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 3}

## RQ1_eb30c6dee989

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_eb30c6dee989)

Checks：[Checks-34.json](Checks-34.json)

Queries：[Queries-18.json](Queries-18.json)

Evidence：[Evidence-62.json](Evidence-62.json)

Coverage：[Coverage-17.json](Coverage-17.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_ee2aa7f32d31不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：eb30c6dee989｜U/33｜Dragon burnDragons第110行扣caller自身；burnFrom第254行有同键额度检查及消耗；局部voluntary_holder_debit，另有外调缺口｜保留这些正常依据。没有发现可直接替代为无同意第三方销毁的证据，整份未知不得强制报警。

指定检查理由：{"voluntary_holder_debit": 1}；其它类报警：FCR-TRANSFER。其它类不能抵销指定类FN。

报警 `finding_11504c733f6982a00fd8`，FCR-TRANSFER，units/program.sol:Dragon，字节3205＋595，决定 `program_support`，证据E10,E13,E14,E15,E3,E5。The change at burnDragons(uint256) affects the same holder request at transferFrom(address,address,uint256). The checked difference is a movement of existing rights to a separate position outside applicable consent.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 1}

资源：{"program": {"program_investigation_seconds": 8.629981527104974, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 23.55805132398382, "task_wall_seconds": 32.18803630908951}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.15295494394376874, "calls": 35, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 13}

## RQ1_4b4775267823

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_4b4775267823)

Checks：[Checks-13.json](Checks-13.json)

Queries：[Queries-05.json](Queries-05.json)

Evidence：[Evidence-17.json](Evidence-17.json)

Coverage：[Coverage-05.json](Coverage-05.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_6a933de928c4不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：4b4775267823｜U/61｜B2BCoinContract；burn第307行为caller自身，killContract第346行，salvage涉及外部资产｜同328c族。可修依赖隔离，不能用终止名称或外部余额替代本账本毁损证明。

指定检查理由：{"scope_missing": 4}；其它类报警：FCR-MINT,FCR-PAUSE。其它类不能抵销指定类FN。

报警 `finding_18e2c36fd0acb7d864d8`，FCR-PAUSE，units/program.sol:ERC20Token，字节3316＋236，决定 `program_support`，证据E20,E24,E30,E31,E33。At lockUntil(uint256,string), the checked privileged change restricts the outgoing right of ordinary holders for an otherwise usable request within the recorded domain.

报警 `finding_55082afdd1075bdd5a15`，FCR-MINT，units/program.sol:ERC20Token，字节8836＋1004，决定 `program_support`，证据E1,E15,E22,E23,E72,E73,E79,E80,E83,E84。At mintTokens(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

报警 `finding_87bed30bb2bb0ffc7912`，FCR-MINT，units/program.sol:B2BCoinContract，字节8836＋1004，决定 `program_support`，证据E11,E27,E28,E5,E74,E75,E77,E78,E81,E82。At mintTokens(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

报警 `finding_f6ab92dc4b9d40482454`，FCR-PAUSE，units/program.sol:B2BCoinContract，字节3316＋236，决定 `program_support`，证据E19,E21,E25,E26,E29。At lockUntil(uint256,string), the checked privileged change restricts the outgoing right of ordinary holders for an otherwise usable request within the recorded domain.

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_fields": 1, "unrelated_or_secondary_graph_pairs_deferred": 4}

资源：{"program": {"program_investigation_seconds": 21.73125729802996, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 30.793950079008937, "task_wall_seconds": 52.52521124994382}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.29373241029679775, "calls": 69, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 82}

## RQ1_6a278772c4f3

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_6a278772c4f3)

Checks：[Checks-16.json](Checks-16.json)

Queries：[Queries-07.json](Queries-07.json)

Evidence：[Evidence-22.json](Evidence-22.json) · [Evidence-23.json](Evidence-23.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_980e04c92f4d不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：6a278772c4f3｜U/84｜同族基类transfer第164行/transferFrom第184行不读冻结，派生_transfer第228行才读｜同上，不能把读者索引关联当真实调用。

指定检查理由：{"scope_missing": 3}；其它类报警：FCR-MINT,FCR-DESTROY,FCR-PAUSE。其它类不能抵销指定类FN。

报警 `finding_c4e8313b68dd4b0ac55f`，FCR-DESTROY，units/program.sol:AdvanceToken，字节10813＋47，决定 `uncompensated_debit`，证据E10,E19,E5。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 10813. The qualified operation reduces another holder's position without a matching credit on this source branch.

报警 `finding_54ebac8723ddfb636256`，FCR-MINT，units/program.sol:AdvanceToken，字节10567＋402，决定 `program_support`，证据E102,E106,E11,E117,E128,E135,E138,E140,E149,E150,E151,E153,E156,E157,E158,E20,E6,E85,E90,E94,E98。The change at burnFrom(address,uint256) affects the same holder request at mintToken(uint256). The checked difference is a new positive entitlement for a controlled beneficiary.

报警 `finding_4a4f0e9544cc0ec80423`，FCR-PAUSE，units/program.sol:BaseToken，字节2652＋13，决定 `productive_outgoing_control`，证据E28,E32,E42,E43。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2652. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger.

报警 `finding_d729c14b2f6ceb2a0d7a`，FCR-MINT，units/program.sol:AdvanceToken，字节8997＋426，决定 `program_support`，证据E1,E107,E108,E122,E123,E129,E130,E133,E134,E22,E46,E47。At mintToken(uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

报警 `finding_dfd6786c29111f0ee865`，FCR-DESTROY，units/program.sol:AdvanceToken，字节8997＋426，决定 `program_support`，证据E100,E103,E104,E111,E136,E141,E143,E2,E23,E64,E65,E86,E87,E99。The change at mintToken(uint256) affects the same holder request at burnFrom(address,uint256). The checked difference is an uncompensated reduction of existing rights under the applicable consent.

报警 `finding_df6f6325d2a9e0d03a82`，FCR-PAUSE，units/program.sol:AdvanceToken，字节2652＋13，决定 `productive_outgoing_control`，证据E27,E31,E40,E41。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2652. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger.

报警 `finding_ac4d8ce0b696439551c7`，FCR-MINT，units/program.sol:AdvanceToken，字节10158＋403，决定 `program_support`，证据E105,E109,E116,E120,E137,E36,E97。The change at burn(uint256) affects the same holder request at mintToken(uint256). The checked difference is a new positive entitlement for a controlled beneficiary.

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 13}

资源：{"program": {"program_investigation_seconds": 35.441504085902125, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 25.49009423190728, "task_wall_seconds": 60.931604120880365}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.29339754628017545, "calls": 100, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 128}
