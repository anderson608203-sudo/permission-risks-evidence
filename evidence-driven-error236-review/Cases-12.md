# 逐成员审阅

[总报告](WorkReview.md) · [成员](Members.md) · [源码](Code.md)

## RQ1_32e1e7ce1240

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_32e1e7ce1240)

Checks：[Checks-09.json](Checks-09.json)

Queries：没有该类保存记录。

Evidence：[Evidence-11.json](Evidence-11.json)

Coverage：[Coverage-04.json](Coverage-04.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_101079fc6aa8不在本批；不产生新的整对正确成绩。

未进入实际求解，指定类候选/检查与权益或普通出账消费者仍有结构接线缺口；增加solver时间不能解决零查询本身。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：32e1e7ce1240｜U/0｜CREDITS实际出账读AccountIsFrozen、豁免及日期；构造/持有人数组残余共存，未进查询｜具有应接通的真实控制路径，优先角色、路由、提交和豁免，尚无新阳性证明。

指定检查理由：{}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_text": 1, "audit_source_scope_mismatch": 1}

资源：{"program": {"program_investigation_seconds": 18.17848599003628, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 50.904494357760996, "task_wall_seconds": 69.08298256667331}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 5}

## RQ1_eb22e4884871

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_eb22e4884871)

Checks：[Checks-33.json](Checks-33.json) · [Checks-34.json](Checks-34.json)

Queries：[Queries-18.json](Queries-18.json)

Evidence：[Evidence-62.json](Evidence-62.json)

Coverage：[Coverage-16.json](Coverage-16.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_f2f95ed8c9c1不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：eb22e4884871｜U/52｜EligmaTokenContract；burn第349行为caller自身，killContract第388行，approve/callback等外部残余｜同族处理。源码反例与未决外部作用分别保留，不预估为纯工程TP。

指定检查理由：{"scope_missing": 5}；其它类报警：FCR-MINT,FCR-PAUSE。其它类不能抵销指定类FN。

报警 `finding_b9d6eefacdfce59fb121`，FCR-MINT，units/program.sol:ERC20Token，字节10428＋928，决定 `program_support`，证据E102,E106,E110,E25,E43。At mint(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

报警 `finding_79de249c9b75592477c7`，FCR-PAUSE，units/program.sol:EligmaTokenContract，字节4834＋241，决定 `program_support`，证据E21,E23,E33,E34,E35。At lockUntil(uint256,string), the checked privileged change restricts the outgoing right of ordinary holders for an otherwise usable request within the recorded domain.

报警 `finding_8e1548ba0d8f173ab08e`，FCR-PAUSE，units/program.sol:ERC20Token，字节4834＋241，决定 `program_support`，证据E22,E24,E39,E40,E41。At lockUntil(uint256,string), the checked privileged change restricts the outgoing right of ordinary holders for an otherwise usable request within the recorded domain.

报警 `finding_b0aeb7222f8963e6bb06`，FCR-MINT，units/program.sol:EligmaTokenContract，字节10428＋928，决定 `program_support`，证据E105,E109,E29,E44,E97。At mint(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 1, "unrelated_or_secondary_graph_pairs_deferred": 4}

资源：{"program": {"program_investigation_seconds": 29.422941698227078, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 46.713118876796216, "task_wall_seconds": 76.13606474595144}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 1.0192501689307392, "calls": 70, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 118}

## RQ1_c80f7a639e42

任务 FCR，本次未检出，上批同成员未检出。

[实际输入源码](InputSource-04.md#rq1_c80f7a639e42)

Checks：[Checks-28.json](Checks-28.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-50.json](Evidence-50.json)

Coverage：[Coverage-13.json](Coverage-13.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未检出 → initial 未检出 → report 未检出

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_30177d564271不在本批；不产生新的整对正确成绩。

指定FREEZE仍未报警。已核的incoming_only、脱接helper或普通同权益旁路不能为了参考标签造边；保留参考FN，源码结论与作者标签的分歧单列。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：c80f7a639e42｜N/23｜ERC20ext普通转账不经派生冻结helper，另有锁定/残余范围｜保留已核脱接结论，其他控制不靠这一局部反证批量关闭。

指定检查理由：{}；其它类报警：FCR-MINT。其它类不能抵销指定类FN。

报警 `finding_a351087e20842117f8fe`，FCR-MINT，units/program.sol:ERC20ext，字节8240＋372，决定 `program_support`，证据E1,E10,E35,E36,E37,E38,E39,E40,E41,E42,E5,E9。At mintToken(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1, "unrelated_or_secondary_graph_pairs_deferred": 2}

资源：{"program": {"program_investigation_seconds": 12.03881378704682, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 39.83736447105184, "task_wall_seconds": 51.876181804109365}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0844622110016644, "calls": 23, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 39}

## RQ1_6eeaddaeac8f

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_6eeaddaeac8f)

Checks：[Checks-16.json](Checks-16.json)

Queries：[Queries-09.json](Queries-09.json)

Evidence：[Evidence-24.json](Evidence-24.json)

Coverage：[Coverage-08.json](Coverage-08.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_4e36475bca23不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：6eeaddaeac8f｜U/162｜MetaMoonMars；实际转账扣gross并以变化后的net检查许可，费用/同意basis未闭合；44次solver timeout，程序约900.25秒｜有计算和语义双重缺口。先复用同一grant签发/核查/消耗的数量，定向查询，不增加gross公理或预算；不能全归因为时间不足。

指定检查理由：{"scope_missing": 1, "scoped_fee_consent": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_text": 1, "action_slice_exhausted": 3, "unrelated_or_secondary_graph_pairs_deferred": 1, "yield_to_source_bound_semantic_review": 1}

资源：{"program": {"program_investigation_seconds": 218.19547945912927, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 53.746179782785475, "task_wall_seconds": 271.94166169688106}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {"timeout": 9}, "used_seconds": 178.00963586429134, "calls": 113, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 52}

## RQ1_185a84436c18

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_185a84436c18)

Checks：[Checks-05.json](Checks-05.json)

Queries：没有该类保存记录。

Evidence：[Evidence-04.json](Evidence-04.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-PAUSE与risk参考评价，配对成员RQ1_ed58b7d7bfbb不在本批；不产生新的整对正确成绩。

未进入实际求解，指定类候选/检查与权益或普通出账消费者仍有结构接线缺口；增加solver时间不能解决零查询本身。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：185a84436c18｜U/0｜CREDITS。setFrozen第79行；transfer第144行与transferFrom第169行有Frozen、个体豁免和日期的真实AND/OR，后续还登记持有人数组。当前检查scope_missing，solver=0。优先修ordinary_control_uses/ledger_routes的形状与角色来源，随后在同holder同请求上处理普通可得豁免和提交。数组记账若能引起回滚仍须保留，不能见到余额扣记就删其后果。当前证据不支持再增solver时限来解决。

指定检查理由：{"scope_missing": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1}

资源：{"program": {"program_investigation_seconds": 18.76914035482332, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 27.494785637129098, "task_wall_seconds": 46.263928396161646}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 5}

## RQ1_cbb6e67b8b81

任务 FCR，本次未知，上批同成员报警。

[实际输入源码](InputSource-04.md#rq1_cbb6e67b8b81)

Checks：[Checks-29.json](Checks-29.json)

Queries：[Queries-16.json](Queries-16.json)

Evidence：[Evidence-51.json](Evidence-51.json)

Coverage：[Coverage-13.json](Coverage-13.json)

Semantics：[Semantics-09.json](Semantics-09.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-MINT与repair参考评价，配对成员RQ1_c315645e4627不在本批；不产生新的整对正确成绩。

原指定MINT报警撤回，但当前仍scope_missing，未得到有效阴性；同次购买反证尚未使整类别完成判断，不能计TN或有效FP纠正。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：cbb6e67b8b81｜ETKSToken，op_50bc6666dd89b70b41ef，字节5091/361｜probe_be31a1bb17fb60ada98f及probe_51e74b80dbca56d7a311分别为上述两类SAT查询。同一通用修复，不按名称或修复身份排除。

指定检查理由：{"scope_missing": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"unknown_or_unshown_effect": 1}

资源：{"program": {"program_investigation_seconds": 7.340280904900283, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 28.078641839325428, "task_wall_seconds": 35.41892513819039}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.10856426414102316, "calls": 22, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 16}

## RQ1_e390407a4c29

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_e390407a4c29)

Checks：[Checks-32.json](Checks-32.json)

Queries：没有该类保存记录。

Evidence：[Evidence-60.json](Evidence-60.json)

Coverage：[Coverage-15.json](Coverage-15.json)

Semantics：[Semantics-10.json](Semantics-10.json)

Messages：[Messages-03.json](Messages-03.json)

Stages：[Stages-03.json](Stages-03.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-PAUSE与risk参考评价，配对成员RQ1_0ce2d4c45f17不在本批；不产生新的整对正确成绩。

未进入实际求解，指定类候选/检查与权益或普通出账消费者仍有结构接线缺口；增加solver时间不能解决零查询本身。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：e390407a4c29｜U/0｜PrivateDeposit。disableTransfers第37行控制transfer_test第44行的balance_test；原生币Deposit/CashOut使用另一balances表。必须分账，但不能新要求真实部署存款或已初始化owner_test才分析。roles.py第97—99行已允许FCR条件域中的未显式初始化地址作abstract_initial_role；初态合同不因函数名test改变。transfersEnabled是显式false，须有合法启用前态，不可直接假定true。推荐用同账本转账用途与条件正额余额验证单位/基线，并以显式零角色或确实无法启用的结构作反对照。结果仍须离线消费者证明，不能本审核先判TP。

指定检查理由：{"scope_missing": 4}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"no_locatable_source": 1}

资源：{"program": {"program_investigation_seconds": 4.8563683200627565, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 43.18916494073346, "task_wall_seconds": 48.045535466168076}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 13}

## RQ1_440857b3df3c

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_440857b3df3c)

Checks：[Checks-12.json](Checks-12.json)

Queries：[Queries-05.json](Queries-05.json)

Evidence：[Evidence-15.json](Evidence-15.json) · [Evidence-16.json](Evidence-16.json)

Coverage：[Coverage-05.json](Coverage-05.json)

Semantics：[Semantics-04.json](Semantics-04.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_a4881b0828b3不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：440857b3df3c｜U/126｜MyAdvancedToken；burnFrom第265行有holder额度，sell有原生币结算；covered_holder_grant与其他scope_missing并存，6次timeout及1次other｜保留有效grant和真实本人结算。只有具体作用仍缺同意/补偿时保留未知，不将合约其他未知抹掉已核正常。

指定检查理由：{"covered_holder_grant": 3, "scope_missing": 4}；其它类报警：FCR-TRANSFER,FCR-MINT,FCR-FREEZE。其它类不能抵销指定类FN。

报警 `finding_43a8f8643d08262728f1`，FCR-FREEZE，units/program.sol:MyAdvancedToken，字节6091＋228，决定 `program_support`，证据E25,E33,E34。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain.

报警 `finding_0a7c0951016df4a70530`，FCR-TRANSFER，units/program.sol:MyAdvancedToken，字节8467＋502，决定 `program_support`，证据E104,E109,E114,E119,E12,E123,E19,E194,E195,E196,E197,E198,E199,E201,E202,E203,E204,E205,E206,E36,E47,E48,E5,E99。The change at burnFrom(address,uint256) affects the same holder request at buy(). The checked difference is a movement of existing rights to a separate position outside applicable consent.

报警 `finding_9f2cd9cfcad976758ed7`，FCR-MINT，units/program.sol:MyAdvancedToken，字节8467＋502，决定 `program_support`，证据E10,E134,E135,E172,E173,E175,E176,E178,E179,E181,E182,E184,E185,E187,E200,E207,E208,E209,E21,E64,E69,E7,E74,E79,E84,E89,E94。The change at burnFrom(address,uint256) affects the same holder request at mintToken(address,uint256). The checked difference is a new positive entitlement for a controlled beneficiary.

报警 `finding_eade6750f66ae210459d`，FCR-MINT，units/program.sol:MyAdvancedToken，字节5911＋33，决定 `new_entitlement`，证据E1。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 5911. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary.

报警 `finding_12fe49bf69441579a99b`，FCR-TRANSFER，units/program.sol:MyAdvancedToken，字节5757＋328，决定 `program_support`，证据E103,E108,E113,E118,E122,E130,E4,E93,E98。The change at mintToken(address,uint256) affects the same holder request at buy(). The checked difference is a movement of existing rights to a separate position outside applicable consent.

报警 `finding_868d34a368503a907c09`，FCR-TRANSFER，units/program.sol:MyAdvancedToken，字节6325＋222，决定 `program_support`，证据E107,E121,E143,E150,E153,E159,E30,E62,E77,E92。The change at setPrices(uint256,uint256) affects the same holder request at buy(). The checked difference is a movement of existing rights to a separate position outside applicable consent.

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_text": 1, "action_slice_exhausted": 2, "unrelated_or_secondary_graph_pairs_deferred": 5}

资源：{"program": {"program_investigation_seconds": 248.14427158329636, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 33.92406487790868, "task_wall_seconds": 282.068342638202}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {"timeout": 9}, "used_seconds": 176.74112999346107, "calls": 146, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 184}

## RQ1_23abf434df32

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_23abf434df32)

Checks：[Checks-06.json](Checks-06.json)

Queries：[Queries-03.json](Queries-03.json)

Evidence：[Evidence-07.json](Evidence-07.json)

Coverage：[Coverage-02.json](Coverage-02.json)

Semantics：[Semantics-02.json](Semantics-02.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_805b30020e56不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：23abf434df32｜U/6｜ClipperCoin三参数transfer第216行才读freeze；基类两参数第113行、transferFrom第134行不读｜与FAC同类旁路，禁止按名字造覆盖。

指定检查理由：{"scope_missing": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"unbound_or_inapplicable_seed": 3, "missing_claim_or_source_anchor": 3, "unrelated_or_secondary_graph_pairs_deferred": 1}

资源：{"program": {"program_investigation_seconds": 8.86673961719498, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 45.33173310384154, "task_wall_seconds": 54.19847487611696}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.016960965935140848, "calls": 6, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 3}

## RQ1_95cf7213c86a

任务 FCR，本次未检出，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_95cf7213c86a)

Checks：[Checks-19.json](Checks-19.json)

Queries：[Queries-11.json](Queries-11.json)

Evidence：[Evidence-28.json](Evidence-28.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未检出 → feedback 未检出 → report 未检出

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_6827335b3690不在本批；不产生新的整对正确成绩。

指定FREEZE仍未报警。已核的incoming_only、脱接helper或普通同权益旁路不能为了参考标签造边；保留参考FN，源码结论与作者标签的分歧单列。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：95cf7213c86a｜U/162｜TOSC普通两参数transfer第114行不读freeze；派生_transfer第160行读冻结/额度，sendTransfer另有管理员限制｜检查同holder普通旁路，不能用管理出账或部分额度失败代替FREEZE。

指定检查理由：{"same_request_preserved": 3, "same_request_bypass": 2}；其它类报警：FCR-TRANSFER,FCR-DESTROY。其它类不能抵销指定类FN。

报警 `finding_b275ff9e08f6daaf8566`，FCR-DESTROY，units/program.sol:TOSC，字节6756＋1294，决定 `program_support`，证据E109,E111,E121,E122,E17,E20,E22,E30,E50,E56,E65,E70,E86,E91,E94,E99。The change at sendTransfer(address,address,uint256) affects the same holder request at burn(address,uint256). The checked difference is an uncompensated reduction of existing rights under the applicable consent.

报警 `finding_79eab3e059e1f7fe4808`，FCR-TRANSFER，units/program.sol:TOSC，字节6756＋1294，决定 `program_support`，证据E107,E112,E113,E119,E120,E18,E19,E21,E31,E43,E60,E68,E69,E76,E80,E97。At sendTransfer(address,address,uint256), the scoped change moves another holder’s existing rights to a separate position without the applicable holder-issued consent.

报警 `finding_bb59fb26a497485b7150`，FCR-TRANSFER，units/program.sol:TOSC，字节6484＋266，决定 `program_support`，证据E101,E104,E105,E12,E29,E41,E59,E64,E7,E74,E90,E93。The change at removePercentLock(address) affects the same holder request at sendTransfer(address,address,uint256). The checked difference is a movement of existing rights to a separate position outside applicable consent.

报警 `finding_064facdfe28b94e7fbed`，FCR-TRANSFER，units/program.sol:TOSC，字节3870＋317，决定 `program_support`，证据E14,E15,E32,E42,E48,E49,E58,E71,E77,E81,E87,E88。The change at burn(address,uint256) affects the same holder request at sendTransfer(address,address,uint256). The checked difference is a movement of existing rights to a separate position outside applicable consent.

报警 `finding_f3a506b5b2e85d62bb2a`，FCR-DESTROY，units/program.sol:TOSC，字节4034＋45，决定 `uncompensated_debit`，证据E13,E16,E33。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 4034 under financial_right. The qualified operation reduces another holder's position without a matching credit on this source branch.

报警 `finding_48978767b706bb94cb10`，FCR-DESTROY，units/program.sol:TokenERC20，字节4034＋45，决定 `uncompensated_debit`，证据E23,E26,E35。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 4034. The qualified operation reduces another holder's position without a matching credit on this source branch.

报警 `finding_401d31087e9aee2d2400`，FCR-TRANSFER，units/program.sol:TOSC，字节6157＋321，决定 `program_support`，证据E38,E53,E75,E84。The change at PercentLock(address,uint256,uint256) affects the same holder request at sendTransfer(address,address,uint256). The checked difference is a movement of existing rights to a separate position outside applicable consent.

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_text": 2, "semantic_meaning_or_explanation_polarity_unresolved": 1}

资源：{"program": {"program_investigation_seconds": 167.65911638829857, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 64.84587866580114, "task_wall_seconds": 232.50499896379188}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 1.4683686597272754, "calls": 105, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 106}

## RQ1_6239598c387b

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_6239598c387b)

Checks：[Checks-15.json](Checks-15.json)

Queries：没有该类保存记录。

Evidence：[Evidence-21.json](Evidence-21.json)

Coverage：[Coverage-07.json](Coverage-07.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_661b0064ae6b不在本批；不产生新的整对正确成绩。

未进入实际求解，指定类候选/检查与权益或普通出账消费者仍有结构接线缺口；增加solver时间不能解决零查询本身。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：6239598c387b｜U/0｜MyAdvancedToken派生_transfer及sell读freeze，但普通两参数transfer第69行、transferFrom第90行不读｜sell局部受限不自动等于该token权益冻结；E1及普通旁路分别核，不强制报警。

指定检查理由：{"scope_missing": 2, "external_dependency": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 3}

资源：{"program": {"program_investigation_seconds": 41.63317497912794, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 55.33814054308459, "task_wall_seconds": 96.9713207129389}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 131}

## RQ1_39fb6e7197c4

任务 FCR，本次未检出，上批同成员未检出。

[实际输入源码](InputSource-04.md#rq1_39fb6e7197c4)

Checks：没有该类保存记录。

Queries：没有该类保存记录。

Evidence：没有该类保存记录。

Coverage：[Coverage-04.json](Coverage-04.json)

Semantics：[Semantics-03.json](Semantics-03.json)

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未检出 → initial 未检出 → report 未检出

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_7450d39da940不在本批；不产生新的整对正确成绩。

指定FREEZE仍未报警。已核的incoming_only、脱接helper或普通同权益旁路不能为了参考标签造边；保留参考FN，源码结论与作者标签的分歧单列。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：39fb6e7197c4｜N/0｜ETJ普通转账与冻结helper脱接｜保留源码反证及参考FN。

指定检查理由：{}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 1}

资源：{"program": {"program_investigation_seconds": 4.342318232636899, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 33.39392699114978, "task_wall_seconds": 37.73624871019274}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0, "calls": 0, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 0}

## RQ1_353a9b0b5006

任务 FCR，本次失败，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_353a9b0b5006)

Checks：无最终保存记录；失败者不得据此视为0次执行。

Queries：无最终保存记录；失败者不得据此视为0次执行。

Evidence：无最终保存记录；失败者不得据此视为0次执行。

Coverage：无最终保存记录；失败者不得据此视为0次执行。

Semantics：无最终保存记录；失败者不得据此视为0次执行。

Messages：[Messages-01.json](Messages-01.json)

Stages：[Stages-01.json](Stages-01.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_db11e3e08742不在本批；不产生新的整对正确成绩。

程序预算耗尽异常逸出，未保存最终报告；错误摘要与program_investigation_budget_exhausted的规范JSON SHA精确匹配。保留三个检查点；不把其中PAUSE报警代作DESTROY结果。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：353a9b0b5006｜U/189｜Token中名为burn的函数增加余额与供应；费用/第三方入账的同意另未闭合；43次timeout，程序约901.06秒｜增记不是DESTROY正证；费用需独立核净损及同意。可优化无收益查询，但不以名字追标签，不把超时当唯一归因。

指定检查理由：{}；其它类报警：。其它类不能抵销指定类FN。

最终失败记录为TimeoutError；其理由SHA与program_investigation_budget_exhausted精确相同。最终report/manifest/export未生成，部分PAUSE阳性仅为检查点，不视为完成结果。两次请求已结算，不能自动重发。

诊断计数（重复记录，不是独立漏洞数）：{}

资源：最终计时/solver计数缺失；不是零成本。

## RQ1_abb48ccfac75

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_abb48ccfac75)

Checks：[Checks-21.json](Checks-21.json)

Queries：[Queries-12.json](Queries-12.json)

Evidence：[Evidence-34.json](Evidence-34.json)

Coverage：[Coverage-10.json](Coverage-10.json)

Semantics：[Semantics-06.json](Semantics-06.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_3e235f5e70d4不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：abb48ccfac75｜U/3｜ICBB派生三参数transfer第174行读freeze，继承两参数第70行/transferFrom第93行不读｜同重载旁路组。

指定检查理由：{"scope_missing": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"audit_card_fields": 3, "unrelated_or_secondary_graph_pairs_deferred": 1}

资源：{"program": {"program_investigation_seconds": 5.904020318761468, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 38.686274303123355, "task_wall_seconds": 44.59029761282727}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.040363344829529524, "calls": 9, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 3}

## RQ1_b7fd0e26135f

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_b7fd0e26135f)

Checks：[Checks-26.json](Checks-26.json)

Queries：[Queries-15.json](Queries-15.json)

Evidence：[Evidence-45.json](Evidence-45.json)

Coverage：[Coverage-12.json](Coverage-12.json)

Semantics：[Semantics-08.json](Semantics-08.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → report 未知

本次只按指定类FCR-FREEZE与risk参考评价，配对成员RQ1_cae50a0089d5不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：b7fd0e26135f｜U/9｜ICBB同结构三参数重载与两参数普通旁路｜同上；保持对象实际身份，不能合并成一个可用样本计算收益。

指定检查理由：{"scope_missing": 1}；其它类报警：。其它类不能抵销指定类FN。

诊断计数（重复记录，不是独立漏洞数）：{"audit_source_scope_mismatch": 1, "audit_effect_unbound": 1, "unrelated_or_secondary_graph_pairs_deferred": 1}

资源：{"program": {"program_investigation_seconds": 6.0814408347941935, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 44.66496106330305, "task_wall_seconds": 50.746403898112476}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 0.0358210145495832, "calls": 9, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 3}

## RQ1_8e4c324fa1c9

任务 FCR，本次未知，上批同成员未知。

[实际输入源码](InputSource-04.md#rq1_8e4c324fa1c9)

Checks：[Checks-18.json](Checks-18.json)

Queries：[Queries-10.json](Queries-10.json)

Evidence：[Evidence-26.json](Evidence-26.json) · [Evidence-27.json](Evidence-27.json)

Coverage：[Coverage-09.json](Coverage-09.json)

Semantics：[Semantics-05.json](Semantics-05.json)

Messages：[Messages-02.json](Messages-02.json)

Stages：[Stages-02.json](Stages-02.json)

Requests：[Requests-01.json](Requests-01.json)

阶段：basic 未知 → initial 未知 → feedback 未知 → report 未知

本次只按指定类FCR-DESTROY与risk参考评价，配对成员RQ1_da692acb223b不在本批；不产生新的整对正确成绩。

已有查询或其他类别报警，但指定类检查仍未形成可接纳判断；需区分实际同意/补偿/旁路反证与尚未绑定作用范围，不由SAT数量推定指定类TP。

上轮静态源码审阅（输入SHA相同，本轮不是重新运行结论）：8e4c324fa1c9｜U/80｜LcsChain burnFrom第201行有owner守卫，并核/消耗holder同键allowance；已有covered_holder_grant局部依据，另有scope_missing/external缺口｜保护同范围许可，补真实未决的定位。不能因为指定类参考为风险就取消有效授权反证。

指定检查理由：{"covered_holder_grant": 5, "voluntary_holder_debit": 5, "scope_missing": 4}；其它类报警：FCR-MINT,FCR-PAUSE,FCR-FREEZE。其它类不能抵销指定类FN。

报警 `finding_31018bfe56428b32a801`，FCR-MINT，units/program.sol:LcsChain，字节5584＋502，决定 `program_support`，证据E145,E150,E156,E160,E164,E169,E21,E235,E236,E250,E251,E26,E263,E264,E273,E28,E280,E281,E284,E285,E288,E291,E292,E316,E322,E323,E327,E328,E33,E332,E352,E354,E355,E359,E363,E365,E366,E367,E368,E62。The change at burnFrom(address,uint256) affects the same holder request at mintToken(address,uint256). The checked difference is a new positive entitlement for a controlled beneficiary.

报警 `finding_3a6b615a3515f36abbaa`，FCR-MINT，units/program.sol:LcsChain，字节5217＋361，决定 `program_support`，证据E12,E15,E157,E161,E165,E170,E175,E179,E241,E255,E268,E282,E286,E289,E293,E300,E304,E326,E329,E331,E333,E337,E364,E369,E370,E371,E374,E375,E389,E390,E391,E392,E393,E394,E395,E396,E397,E4,E52,E9。The change at burn(uint256) affects the same holder request at mintToken(address,uint256). The checked difference is a new positive entitlement for a controlled beneficiary.

报警 `finding_5e01478d4dd3cdb24ff7`，FCR-MINT，units/program.sol:LcsChain，字节6092＋333，决定 `program_support`，证据E112,E113,E180,E181,E185,E189,E190,E194,E195,E221,E36,E56,E76,E77。At mintToken(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition.

报警 `finding_32af36090d13cdbc1f34`，FCR-FREEZE，units/program.sol:LcsChain，字节6580＋30，决定 `productive_outgoing_control`，证据E66,E67,E72,E73。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 6580. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger.

报警 `finding_1dfadd3a6a9ef556622a`，FCR-PAUSE，units/program.sol:LcsChain，字节2387＋12，决定 `productive_outgoing_control`，证据E54,E55,E70,E71。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2387. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger.

诊断计数（重复记录，不是独立漏洞数）：{"unrelated_or_secondary_graph_pairs_deferred": 15, "invalid_top_level_or_duplicate_key": 1}

资源：{"program": {"program_investigation_seconds": 153.79182339971885, "clock_scope": "facts_through_final_decision", "model_wait_seconds": 50.14571343641728, "task_wall_seconds": 203.93754074722528}, "solver": {"limit_seconds": 900.0, "per_check_ms": 20000, "unknown_reasons": {}, "used_seconds": 4.17202028259635, "calls": 181, "upgrades": 0, "budget_exhausted": 0, "events": []}, "reported_actions": 335}
