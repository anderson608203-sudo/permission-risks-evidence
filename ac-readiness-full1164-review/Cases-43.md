# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_837b1adf4a01

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_837b1adf4a01) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_60760b12532f)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_2e5e58cf88dd1d90e10e`，根位置 760＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 760 under management_role. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E10, E11, E12, E14, E2, E6, E7, E8, E9

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.945 秒，模型等待 36.677 秒，真实 solver 13 次，查询投影 11 项，动作记录含缓存 14 项。诊断 {'unbound_or_inapplicable_seed': 2, 'audit_source_scope_mismatch': 1}。

最终报告 SHA `6b9698bf232f7abd7c257b8d20c21f67394dc34b822861336f75c9bdf6d38a18`，决定 SHA `aa29b3c717e705bb307ce88e2e1c1b93b5d5fbfb05d2c8789492aef343330a12`。

## RQ1_4f92ef93f841

任务 FCR，评价类别 FCR-TRANSFER。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_4f92ef93f841) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_660632df03e8)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 1, 'source_check_excluded': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.847 秒，模型等待 47.841 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 14 项。诊断 {'audit_effect_unbound': 1, 'no_locatable_source': 3}。

最终报告 SHA `a0b5ad3e562c890b4ae1e2f789fcb7c1c6c106e97ce6b9191862a37eecbea997`，决定 SHA `49bacaf06966afb927154d0cbc4cb9613e356744f45ec2aac62c29aa255904b7`。

## RQ1_1953f9f6b6f2

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_1953f9f6b6f2) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_58e207b56646)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 6, 'necessary_effect_absent': 2, 'no_privileged_intervention': 3}。相关检查决定 {'core_mismatch': 1, 'scope_missing': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.550 秒，模型等待 52.215 秒，真实 solver 12 次，查询投影 12 项，动作记录含缓存 20 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `5f3139f111e6993e7a55796e6b4f50f40da52030fc8dbe8c312bfa5ed033620f`，决定 SHA `374c4e0511f76e84e8ecc4f27335b547212c5b16b9f6dcd7114dbcc2b94f2573`。

## RQ1_660632df03e8

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_660632df03e8) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-43.md#rq1_4f92ef93f841)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_6bfb09f4fc303c7efe92`，根位置 1076＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1076. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E1, E3, E5, E6

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.294 秒，模型等待 51.335 秒，真实 solver 4 次，查询投影 5 项，动作记录含缓存 20 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `c539a8a1af82f5f2ed97bd61f0b3fe0b9f88c1f12cb9190433c2cb4b2eddd523`，决定 SHA `de1ee92fc42ab26a507d97c8f591abe88c7de7315b5e4319bd064955b746fc30`。

## RQ1_b884bab91ca4

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_b884bab91ca4) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-42.md#rq1_f82fc055f5dc)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_d94dcea52088cbfe9417`，根位置 833＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 833. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.415 秒，模型等待 24.999 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'explicit_effect_anchor_conflict': 2}。

最终报告 SHA `655d5286f29a0502ec005ccf482f901f43be628123d3310a8a966f3a3170c0df`，决定 SHA `bd904c81cd3c4f620fdf7a19725dac39cb7f1fc6b449619a8aafcd72168eac55`。

## RQ1_d254caa47e26

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_d254caa47e26) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_905fe6a15d0b)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_99cf330cde1c2ee1b36b`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E23, E39, E41

发现 `finding_5ce8d61f11eb4a6910cd`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E21, E34, E36

发现 `finding_8b76ce3d6617ff88cd5c`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E19, E37, E38

发现 `finding_f9d03d2a25678541a07c`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E17, E30, E33

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 26.146 秒，模型等待 16.220 秒，真实 solver 113 次，查询投影 111 项，动作记录含缓存 63 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 10}。

最终报告 SHA `e9b3b391fa14f676359639bf20fd5b2dba10c1b8a94c9cf67bfc2e016f84a727`，决定 SHA `4eb9c1cd59eebdc5d25d6607bf2daafbe87fd47f17678a441595a71b0c954ccb`。

## RQ1_43103f5773b9

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_43103f5773b9) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-27.md#rq1_1f932eab663d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 15, 'necessary_effect_absent': 15}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.368 秒，模型等待 35.381 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_source_scope_mismatch': 3}。

最终报告 SHA `4712dca4f0c61d42a24e426365ac9c597676f1807f3ddf186792f52f39ede80f`，决定 SHA `64cad84627b40c638de0d3aba80924e26ca5bbf48d6f8b5c84dd7220dce68a28`。

## RQ1_95cf7213c86a

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_95cf7213c86a) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) [Queries-65.json](Queries-65.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-34.md#rq1_6827335b3690)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 3}。相关检查决定 {'scope_missing': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 289.535 秒，模型等待 56.671 秒，真实 solver 162 次，查询投影 356 项，动作记录含缓存 148 项。诊断 {'unbound_or_inapplicable_seed': 2, 'invalid_semantic_row': 2, 'audit_source_scope_mismatch': 2, 'audit_effect_unbound': 1, 'unrelated_or_secondary_graph_pairs_deferred': 5}。

最终报告 SHA `8b990cc60ec7fd24e375a937d13fece620c3c63de5b34e9ddd309fa80eb1d84d`，决定 SHA `5576f7a66c07ae1ee6e7d0c277111dee20b7477682d02bba155e4bd7ba034950`。

## RQ1_b2aa8ebfc6c8

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_b2aa8ebfc6c8) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-65.json](Queries-65.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_11ec4918a871)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_966f1237c377d14f59fb`，根位置 2010＋343，依据 `program_support`。At burnFrom(address,uint256), a privileged effect leaves another holder with fewer rights in the same unit after attributed transfers and applicable settlement. 证据 E1, E10, E11, E12, E5

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.892 秒，模型等待 21.719 秒，真实 solver 17 次，查询投影 22 项，动作记录含缓存 11 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `14bdb96a75ead702949e42db756e6cfc4e7f6c00220ba01b798db23460640026`，决定 SHA `0821655ac73ffe43babb53dd0a2d76e1aa99be668fbffe3a7661978a732b7c9b`。

## RQ1_9451d6dac4de

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_9451d6dac4de) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-65.json](Queries-65.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-43.md#rq1_e25d32acc1f7)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_9a800bf65377b95179d3`，根位置 853＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 853. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E1

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.619 秒，模型等待 45.346 秒，真实 solver 8 次，查询投影 11 项，动作记录含缓存 18 项。诊断 {'audit_effect_unbound': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `25f86140ad8d77952a8c65b6ed2b9332d1c643be57039ae93ce13998a2cc8f42`，决定 SHA `7fe3779640bf2cc449e1bedb11d8b1cbd056db55389c43a7cbcfd5f8da9ef26a`。

## RQ1_f233c826784d

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_f233c826784d) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-65.json](Queries-65.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-27.md#rq1_1b0307d85594)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_83909d6b7ba13cd141fc`，根位置 2387＋12，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2387. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E18, E22, E23, E25

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 28.089 秒，模型等待 29.690 秒，真实 solver 80 次，查询投影 100 项，动作记录含缓存 94 项。诊断 {'missing_claim_or_source_anchor': 2, 'unrelated_or_secondary_graph_pairs_deferred': 4}。

最终报告 SHA `be88d65e51dc5d399e1df0b0a5d43bc5abf5318a9b31ce50ee919d8e508537ce`，决定 SHA `f5c26eff73000b438300191b2b793dea4b39a45e76caaba0a0ae369a70fbea4b`。

## RQ1_d19d0cf1d510

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_d19d0cf1d510) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-28.md#rq1_7fe1d2fd9226)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 36, 'necessary_effect_absent': 27, 'detached_local_holder_switch': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.810 秒，模型等待 38.066 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'missing_claim_or_source_anchor': 3}。

最终报告 SHA `33855e361bcf8cff88d165a6e742f98ab63fbf54ca210e4deea5ec99bc158c70`，决定 SHA `3ba52ffcf4da82c0ef4a75524d1253d7273b1bcde1ca8403b92933b97658982e`。

## RQ1_94c6192b0f93

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_94c6192b0f93) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-65.json](Queries-65.json) [Queries-66.json](Queries-66.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_6309dbd5f8ce)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_a6d24097c71e4f4f4218`，根位置 1612＋267，依据 `program_support`。At setLocked(address,uint256), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E1, E17, E18, E2, E24, E3, E5, E8, E9

发现 `finding_78c4d25022fb12105a41`，根位置 6644＋23，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 6644. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E16, E20, E56, E57

发现 `finding_1d701f298d4c5d70aa2c`，根位置 6644＋23，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 6644. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E26, E32, E64, E65

发现 `finding_55a3774a25380db50e2f`，根位置 1612＋267，依据 `program_support`。At setLocked(address,uint256), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E31, E40, E44

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 284.204 秒，模型等待 50.727 秒，真实 solver 856 次，查询投影 797 项，动作记录含缓存 53 项。诊断 {'audit_card_text': 1, 'action_slice_exhausted': 1, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `c1ef5cde41d7dd3e5e5904b0fd07ce3ba7fef939c474ac3244a645abfb897a5c`，决定 SHA `8948fe4fe64d7b5055190a68151de4a8aa14ad512c1bdd32c70983ac5c02f795`。

## RQ1_eb7101bcaf57

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_eb7101bcaf57) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-27.md#rq1_c66d7fc7441b)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 3, 'no_effect_in_scope': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.156 秒，模型等待 52.611 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {}。

最终报告 SHA `2e85b543680c75c2d37e45a3015f2e92d8114240bb090f90f3118b75bb4e486d`，决定 SHA `885e1c587616482e84594bffe5c656ee6c5a2f074a27158a0439f4308af32f81`。

## RQ1_e25d32acc1f7

任务 FCR，评价类别 FCR-TRANSFER。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_e25d32acc1f7) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-66.json](Queries-66.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_9451d6dac4de)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'external_dependency': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.924 秒，模型等待 41.391 秒，真实 solver 7 次，查询投影 9 项，动作记录含缓存 30 项。诊断 {'audit_effect_unbound': 3}。

最终报告 SHA `7b9f15904c57682a505e13d9b03bbbda4d898ad11d97b3161899d5e52a97376c`，决定 SHA `f813e9b575a6a47827e8d50e85304fab5df4cae14f8c9b96742bc1e9ac6e8eee`。

## RQ1_58e207b56646

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_58e207b56646) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-66.json](Queries-66.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-43.md#rq1_1953f9f6b6f2)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_e13e90e9f9e054b5084f`，根位置 1547＋382，依据 `program_support`。At burnFrom(address,uint256), a privileged effect leaves another holder with fewer rights in the same unit after attributed transfers and applicable settlement. 证据 E12, E2, E23, E25, E29, E30, E32, E35, E36, E37, E38, E6

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 27.793 秒，模型等待 29.437 秒，真实 solver 38 次，查询投影 49 项，动作记录含缓存 28 项。诊断 {'unbound_or_inapplicable_seed': 2, 'unrelated_or_secondary_graph_pairs_deferred': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `06687e45a6a806a8118b67308bc33ee784cb5d16c28d4b4f021e374d799315ac`，决定 SHA `77ba6acb49271e5d3b2f90d63f25a505913bfa2ec672d7bd25af99fa0338a908`。

## RQ1_d66edd91f212

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_d66edd91f212) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-31.md#rq1_461e1f6a078f)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.390 秒，模型等待 31.846 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `1bb4738da7b06af819a6149e19f307f39b3e6b36eba79a78c76e5208b20477bc`，决定 SHA `429e47c4ddbd4709b1cff685171e8cc737510dc7f2cb2e85901ff6b1695640c3`。

## RQ1_4d0224e0d6e1

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_4d0224e0d6e1) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-66.json](Queries-66.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-29.md#rq1_0e93114762d7)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 18, 'no_effect_in_scope': 17}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 32.967 秒，模型等待 21.676 秒，真实 solver 36 次，查询投影 38 项，动作记录含缓存 30 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `a79640b393ef76f0b3556fca52ccec018e0f007481146fe98f0bcf9fababb7d1`，决定 SHA `12cb8831abe824bf22a4f0ff48dd38e79bc31e278d290e866bb3fd6d98ec5935`。

## RQ1_3421c09bc85c

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_3421c09bc85c) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-66.json](Queries-66.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-33.md#rq1_7cc11a697bd2)。指定类风险端报警、修复端报警，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_b3ed0502b9999a9066c5`，根位置 10118＋1620，依据 `program_support`。At allocateToken(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E10, E17, E18, E50, E51, E56, E62, E63, E67, E68, E69, E7

发现 `finding_3ced98c0b930e41a6c3f`，根位置 5232＋373，依据 `program_support`。At setTokenExchangeRate(uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. The intervention can enable a new same-request outcome; baseline commitment is not established. 证据 E13, E55, E57, E59, E61, E64, E66, E76

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 24.295 秒，模型等待 35.958 秒，真实 solver 58 次，查询投影 55 项，动作记录含缓存 64 项。诊断 {'unbound_or_inapplicable_seed': 2, 'no_locatable_source': 1}。

最终报告 SHA `dd6647cd0ac1614c8020d589e8359a938dcd5dc7f8534babd07b7841cc207ecf`，决定 SHA `8201b989498867548b080c9d53e2b7f5dcdc7fb8ff2b5efd76754e0ce09cfb4a`。

## RQ1_d967ae07a958

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_d967ae07a958) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-66.json](Queries-66.json) [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_9171531dd52d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_ddae7497797c33c6819e`，根位置 8766＋643，依据 `program_support`。At burnTokens(address,uint256), a privileged effect leaves another holder with fewer rights in the same unit after attributed transfers and applicable settlement. 证据 E10, E18, E28, E36, E38, E44, E50

发现 `finding_66fe01b57cba60ca930b`，根位置 9415＋844，依据 `program_support`。The change at emitTokens(address,uint256) affects the same holder request at burnTokens(address,uint256). The checked difference is an uncompensated reduction of existing rights under the applicable consent. 证据 E21, E23, E25, E27, E43, E45, E54, E55, E6

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 27.222 秒，模型等待 13.627 秒，真实 solver 84 次，查询投影 113 项，动作记录含缓存 51 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `ce65cd8042c37d8a5d4f2f2a8182026c0a38e364ccec5909fccb65108876d3cb`，决定 SHA `b4d1836f070828da57737bc9d36d8ff8aebb32aad816a0a86ee82150f3a7265b`。

## RQ1_6239598c387b

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_6239598c387b) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-28.md#rq1_661b0064ae6b)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 1}。相关检查决定 {'scope_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.651 秒，模型等待 31.181 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'missing_claim_or_source_anchor': 2}。

最终报告 SHA `12a2375b5c8ba44ae88688a2842c75d170533989cdcf3b8622b6fb9e1ee7b3c1`，决定 SHA `942c508e25e41f89bf6ee1bf181680c21e001b994f90a6ff5559d08256dcc151`。

## RQ1_684f1de50e1a

任务 FCR，评价类别 FCR-MINT。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_684f1de50e1a) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-35.md#rq1_c3bf1a81ff5a)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 14, 'source_task_reading': 11, 'necessary_effect_absent': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.684 秒，模型等待 21.031 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `3eec40396503ea9e89462b8f16a00d7eae1e867f06111f95d98705cc6cf72f13`，决定 SHA `db3d30e5e3780b0104d6168a4d567ad037100bf818a289fa350d3c604ea4e282`。

## RQ1_f1bb587376e8

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-18.md#rq1_f1bb587376e8) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_35646ded2a70)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_2c9c5349dd4bfc22fb4f`，根位置 910＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 910. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E4

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.631 秒，模型等待 38.529 秒，真实 solver 2 次，查询投影 3 项，动作记录含缓存 5 项。诊断 {'invalid_semantic_row': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `f67b32a9efd1492627ded49ba571adbf332ff7e4f3921753e1840693702ebe29`，决定 SHA `1650ee5fd75e04483df93354d20eb249f6dfb6d36cc7ddbdbfbebf3541e06882`。

## RQ1_6c3522e11e92

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_6c3522e11e92) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-49.md#rq1_9a61667124cf)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.076 秒，模型等待 26.117 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `8492fb732cec4cf56b79beb16954cb140cf3fc9f917b37d20b81e53f3b38a369`，决定 SHA `859de5c75e587926cf1d36218298ade42b985055db0baf4b0e2625c1f2fa2a68`。
