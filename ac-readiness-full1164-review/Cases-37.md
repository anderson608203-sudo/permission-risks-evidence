# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_9c365cb18f95

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_9c365cb18f95) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-54.json](Queries-54.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-46.md#rq1_dc06d7bad0d8)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_f2c1f4329df7d47f58a9`，根位置 8403＋32，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 8403. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E44, E45, E58, E60

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 124.372 秒，模型等待 32.799 秒，真实 solver 26 次，查询投影 44 项，动作记录含缓存 161 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 9}。

最终报告 SHA `c22013412c2a82e1ecd1cdde2041d33d64ccf557496132fb4635ea7895ceb6ce`，决定 SHA `0cbf00830cc644258b63b2672c0a3162bdc794de7aca8d554eb61e04c82c8da4`。

## RQ1_d34dd1569ff4

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_d34dd1569ff4) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-54.json](Queries-54.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-30.md#rq1_ae0f59a34868)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 7, 'no_privileged_intervention': 5, 'necessary_effect_absent': 3}。相关检查决定 {'core_mismatch': 1, 'scope_missing': 4}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.536 秒，模型等待 38.629 秒，真实 solver 7 次，查询投影 6 项，动作记录含缓存 53 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1, 'missing_claim_or_source_anchor': 1}。

最终报告 SHA `5ad33d9f812ee111b88f71d7c7df534ac8278b001a9f13b5b55a090ca4b6085a`，决定 SHA `5b9c93269cf2f0556ba33f83bae4c7972583adcf7a72bf1905720e8f1b30df40`。

## RQ1_b731957fa974

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_b731957fa974) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-54.json](Queries-54.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-38.md#rq1_4968e56244c9)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_4b311e30187287a73dcb`，根位置 2231＋28，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 2231. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E6

发现 `finding_cf69aa625b0cf58c2ca3`，根位置 2231＋28，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 2231. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E14

发现 `finding_e5f1b8546e3a88b5d3b8`，根位置 2231＋28，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 2231. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E11

发现 `finding_9f84919578b1cdf54de3`，根位置 2231＋28，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 2231. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E15

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.843 秒，模型等待 28.050 秒，真实 solver 6 次，查询投影 23 项，动作记录含缓存 22 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `75176f6d8f2b627238692b51b31cbd51c8aed7f53568cd65c509276a971126b3`，决定 SHA `37b4fff9f185b6f7d9570cf5fcd1780e380d7f9bc740513c1a29c82e775534c6`。

## RQ1_ffaaf45e84b1

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 未知。

[实际输入](InputSource-16.md#rq1_ffaaf45e84b1) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-54.json](Queries-54.json) [Queries-55.json](Queries-55.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-34.md#rq1_2ee1d93e1f45)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_7696d213e4122631cecc`，根位置 2423＋25，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2423. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E22, E44, E45, E9

发现 `finding_835ef3973f51b21165d4`，根位置 2423＋25，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2423. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E15, E27, E29, E5

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 900.653 秒，模型等待 21.798 秒，真实 solver 966 次，查询投影 841 项，动作记录含缓存 38 项。诊断 {'explicit_effect_anchor_conflict': 1, 'action_slice_exhausted': 11, 'program_investigation_budget_exhausted': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `fba268dd7f2ea65e6eb88f903c806046fee3528f256e5d2188c77938bf02eb30`，决定 SHA `1cff3976736f9da263720c4dfe050537cb0f56e6b633fead3b6262f13a2e7def`。

## RQ1_30177d564271

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_30177d564271) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-38.md#rq1_c80f7a639e42)。指定类风险端未检出、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 15, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.695 秒，模型等待 65.384 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'audit_source_scope_mismatch': 3, 'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `014a9e1d1f58eb8c8cff256858fc435903fb82be102f90113cf59ec3772e7ac5`，决定 SHA `1b055d68614c4d926596c3aceb2acc9247a8555ded3e584a6ada5940131e170a`。

## RQ1_4a16f8a0e313

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_4a16f8a0e313) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-55.json](Queries-55.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-46.md#rq1_cbe5fd0f01d7)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_552021aae9616a2b0ad8`，根位置 2086＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 2086. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E4

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.108 秒，模型等待 62.792 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 15 项。诊断 {'missing_claim_or_source_anchor': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `a5ca4f98a797f91e6d1a3b466451d1dfdca98cb78f7d2c53e7a7ca2e149b7524`，决定 SHA `99e8ecb636dec3d237948e78e3cb3b7bfa11b9ab1bfdad1fcaabd158a37f6308`。

## RQ1_4b4775267823

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_4b4775267823) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-55.json](Queries-55.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-42.md#rq1_6a933de928c4)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {'scope_missing': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 18.940 秒，模型等待 25.272 秒，真实 solver 61 次，查询投影 70 项，动作记录含缓存 82 项。诊断 {'missing_claim_or_source_anchor': 1, 'unrelated_or_secondary_graph_pairs_deferred': 4}。

最终报告 SHA `8f53741bf3e068683c1fc2f161d19e9ac9b30e894d6e749215ead0fadb2a61a4`，决定 SHA `abb63e2a261fc09b4d31d86dc1fac0375f5c30c0cfeca01d069991965c11d384`。

## RQ1_6a278772c4f3

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_6a278772c4f3) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-55.json](Queries-55.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_980e04c92f4d)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'source_unit_missing': 2}。相关检查决定 {'scope_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 33.431 秒，模型等待 27.902 秒，真实 solver 84 次，查询投影 140 项，动作记录含缓存 137 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 10}。

最终报告 SHA `bb398e54d4113b4c44542d01dcc8abf51373c79cdfeabb4de6b4b9a2188eecf1`，决定 SHA `c7ae74bf566031288672afef424832da606ed6fa8f0a01a2a1513c7b08ca477f`。

## RQ1_72c6b8c6b605

任务 FCR，评价类别 FCR-TRANSFER。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_72c6b8c6b605) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-55.json](Queries-55.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-46.md#rq1_b5217318672e)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 1, 'source_check_excluded': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.766 秒，模型等待 57.857 秒，真实 solver 6 次，查询投影 5 项，动作记录含缓存 19 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `8a7c40743f80044c737bd6a706437bf7f2c128c088d818e999594bfdc46a519d`，决定 SHA `9b16bc275f83534dcc84d192270dd31694a388d6684243eab8f2664189380413`。

## RQ1_5262763dfbae

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_5262763dfbae) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-55.json](Queries-55.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_3818be4752ff)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_998c61070a6d6b78c04b`，根位置 6806＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E13, E6

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 60.228 秒，模型等待 22.716 秒，真实 solver 62 次，查询投影 74 项，动作记录含缓存 51 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `a78a80f5a4a9fdd7e2004211a3c17f203be1967693259fd94dfecb79a811dc4b`，决定 SHA `d39ed937006bdb78f4d42907dc705b5b764665f26ce744acea83498bfcc01a17`。

## RQ1_32e1e7ce1240

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_32e1e7ce1240) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-40.md#rq1_101079fc6aa8)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 6}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.327 秒，模型等待 13.920 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `d65e0c8677da0dc8df84fe5512a41f520e6e0dce6b79793f5ca16cb5be8eec61`，决定 SHA `02322e398bde14f9c8b78656672a10ee23ccc570a64c9d6b72d338125daa6299`。

## RQ1_4e3600087174

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_4e3600087174) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-35.md#rq1_c0126467dbc0)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 16, 'necessary_effect_absent': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.931 秒，模型等待 33.004 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `5b9750e8e685081c516c77048776d5e223527553f63ca8a315f3ea602b27fc5e`，决定 SHA `70a6167695085cfcd6093bfb0348846d939963ff51fb98b72485a9ff8f674155`。

## RQ1_fbb992d4ac67

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_fbb992d4ac67) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-34.md#rq1_adf5a6b0fab0)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 7, 'necessary_effect_absent': 7}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.934 秒，模型等待 37.498 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'unbound_or_inapplicable_seed': 6, 'no_locatable_source': 1}。

最终报告 SHA `0ce9bc304a0233348119c7a572acc99046bb40e6f4b6b940c865fa9478de2856`，决定 SHA `1ea20c5298d7e9c694a50b6e83b4b89160e4055b7391af3f3ff7b02c7272aa5c`。

## RQ1_ba0ef60ed8a6

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_ba0ef60ed8a6) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-55.json](Queries-55.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_49ef001521e5)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_37be7bc46f56a504fe8d`，根位置 1223＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1223. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E2, E3, E5

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.486 秒，模型等待 48.962 秒，真实 solver 6 次，查询投影 8 项，动作记录含缓存 5 项。诊断 {'audit_source_scope_mismatch': 1, 'no_locatable_source': 1}。

最终报告 SHA `57ae379efee781e2d934f4018b6c35fbe440b6f6cf559024ddb6c83f191dc19e`，决定 SHA `aeff7d37a637a3508c93742c4f8fdaf13c519fb47a80a9a361c5414ddb90434a`。

## RQ1_6187bc3509e7

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_6187bc3509e7) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-55.json](Queries-55.json) [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-28.md#rq1_7597fe797887)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_998c61070a6d6b78c04b`，根位置 6806＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E18, E27, E28

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 52.937 秒，模型等待 51.904 秒，真实 solver 72 次，查询投影 85 项，动作记录含缓存 116 项。诊断 {'audit_card_text': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `0e8483068707ee8dcd14d2c60d9dc083a898067c6447b46b52cf19dcf2ab7351`，决定 SHA `1b98594af4597d5225af37d63b44e427178740139e3e877bc97049a100aa27a0`。

## RQ1_8528c7edab2f

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_8528c7edab2f) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_f88298f30fee)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 1}。相关检查决定 {'scope_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.586 秒，模型等待 63.683 秒，真实 solver 10 次，查询投影 14 项，动作记录含缓存 53 项。诊断 {'audit_source_scope_mismatch': 2, 'no_locatable_source': 2, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `bdf46de29e6e91ed3081454f5e4f5e596bb4f7529629c11f127e23dc0519bf88`，决定 SHA `2cf1aab87b629248ecbc7376570d19536c32055fab885fe40656c95950af8307`。

## RQ1_a38c8e0b4785

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_a38c8e0b4785) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_05ad9d6a9255)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_7c911e5d45673ef07318`，根位置 834＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 834. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.572 秒，模型等待 29.998 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'missing_claim_or_source_anchor': 1}。

最终报告 SHA `07806020ec005a49fd8fa746e567b4dbbaed76d43105dbfed48c2fc9e9dbf1bf`，决定 SHA `964148098b1094b75bab89e244067c76f724c0b6ed810e2a712f113e30adcd31`。

## RQ1_143874b8f077

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_143874b8f077) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_896e92a15772)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_29c2209591021628d9f3`，根位置 657＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 657. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1, E2

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.133 秒，模型等待 39.256 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {}。

最终报告 SHA `e25a1c3c94048dfa086363f3966f620b16efad93c759952a62db8d50767b2a22`，决定 SHA `4aa536eb13c410fd2bdab67fa6a07dd41e1fdcace846af29173364090b5b4f6d`。

## RQ1_708a354d4471

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_708a354d4471) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_69def43bede4)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_7dc85d8ea29040ab2026`，根位置 764＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 764. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E11, E12, E14, E16, E5, E8, E9

发现 `finding_8e3d048b33d798e77889`，根位置 447＋476，依据 `program_support`。At zero_fee_transaction(address,address,uint256), the scoped change moves another holder’s existing rights to a separate position without the applicable holder-issued consent. 证据 E31, E6

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.709 秒，模型等待 75.699 秒，真实 solver 17 次，查询投影 23 项，动作记录含缓存 32 项。诊断 {'audit_effect_unbound': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `850043089a399f7f96b30eacc37267aac8d6ab6f5ff585dacc41cef13de237ff`，决定 SHA `78b81405ed284b6421cd6e62c31b1108ec0a047181e1a16ed25db27eb4fe43f3`。

## RQ1_eb22e4884871

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_eb22e4884871) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-33.md#rq1_f2f95ed8c9c1)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {'scope_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 15.377 秒，模型等待 31.414 秒，真实 solver 52 次，查询投影 58 项，动作记录含缓存 44 项。诊断 {'audit_card_text': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `ac3c3b2919e5736b105c4c430a2f5bcf5f008a93dae55a599e88af9eb3d83ebd`，决定 SHA `1edd7e9dc5dde9075224c0bcb749f50b7ea4a16032653ca57d104934532aa10b`。

## RQ1_7cfdf5697377

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_7cfdf5697377) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-27.md#rq1_4a9d5241617f)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_3f4971131a35cce6466f`，根位置 6626＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6626 under financial_right. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E19

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 66.999 秒，模型等待 64.992 秒，真实 solver 78 次，查询投影 91 项，动作记录含缓存 156 项。诊断 {'audit_card_source_refs': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `046f655b303e7352c09c32cd6cfe29df0161479ffa05baae557cbc43024c5e7a`，决定 SHA `7105f59947e84b8169513db765a3de568efd3e94835b2b7d28ce618280689170`。

## RQ1_25fd2b7278c4

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_25fd2b7278c4) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_169fab614926)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_184224ed2cb60608d875`，根位置 819＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 819. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E2, E4

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.466 秒，模型等待 54.948 秒，真实 solver 14 次，查询投影 9 项，动作记录含缓存 4 项。诊断 {'audit_source_scope_mismatch': 1}。

最终报告 SHA `a37d4bbfc350ac4e2e137368edb28ad58afdc1796871f7292543f24373f2ab18`，决定 SHA `5b02742b077ba3d51dcd6152c623ed79664bc1f3e126c5580756cce9f4ecfe98`。

## RQ1_b25ec4a4cd43

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_b25ec4a4cd43) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-29.md#rq1_14d06cbbe5a7)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_f7c10d504d4ca8576a82`，根位置 1465＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1465. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.880 秒，模型等待 48.238 秒，真实 solver 5 次，查询投影 7 项，动作记录含缓存 21 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2, 'semantic_answer_outside_sent_scope': 1, 'semantic_meaning_or_explanation_polarity_unresolved': 1}。

最终报告 SHA `e6e5979d575741741c0425d8b2e255b9cb2ff926344a0c871364d71ed0238f2e`，决定 SHA `0ab1c0cfa6d5fae2ad12bef73eb13c878494e0fb360bc5d113b67ce43a9f5965`。

## RQ1_0bf6f8bce8d9

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未知。

[实际输入](InputSource-16.md#rq1_0bf6f8bce8d9) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_196284e657b0)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 5, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.393 秒，模型等待 60.610 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_effect_unbound': 1, 'no_locatable_source': 3}。

最终报告 SHA `053ccd70b5aeb97f0bef0801a5ec9b1a73daed05ee1c07d7b27a08f9d1d0ff7b`，决定 SHA `6562a7372c92f1a384e26b59e05f5b8ad9821d11fafcc6590d94295df2512ec9`。
