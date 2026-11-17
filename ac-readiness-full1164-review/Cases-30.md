# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_644c45f93d78

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_644c45f93d78) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-42.json](Queries-42.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-34.md#rq1_63b77851cec0)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_ff5dbb90b20928cf8129`，根位置 8467＋502，依据 `program_support`。The change at burnFrom(address,uint256) affects the same holder request at mintToken(address,uint256). The checked difference is a new positive entitlement for a controlled beneficiary. 证据 E11, E110, E112, E113, E114, E116, E117, E122, E123, E41, E45, E49, E53, E57, E61, E64, E67, E8

发现 `finding_e6f0e619c340e61134fd`，根位置 5911＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 5911 under financial_right. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E2

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 59.575 秒，模型等待 48.061 秒，真实 solver 111 次，查询投影 154 项，动作记录含缓存 109 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `aef1039d873636bf8c038284a0238947ff7957c63a1c56b077ad56d21b6e5cc2`，决定 SHA `debb831fd0b76d4ce2d06e8da7da6214401741d116f1823aecbf471cddd50442`。

## RQ1_a7bf9487cc3f

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_a7bf9487cc3f) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-30.md#rq1_c772c59e4a76)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.919 秒，模型等待 39.409 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'missing_claim_or_source_anchor': 4}。

最终报告 SHA `8683ae98d73679d936c42748d4f6986120fdbeffabdac01a04456d2787db578c`，决定 SHA `6688efc1dcbe1a6ed89cca0bcebaad41fbf483b8b10d75c69ec21efe40524cd8`。

## RQ1_ae0fb58f9d8d

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_ae0fb58f9d8d) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-38.md#rq1_a2450795f339)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_332b259c7287f33267b8`，根位置 947＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 947. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E2

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.352 秒，模型等待 34.805 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `7e293693973bc2f9ac3b303dcf829ef81321994fa0103f457bf38d9a9a168052`，决定 SHA `fd7c9c57aae959124b4812f98aa2f67e9b84f2d4d882225ccf0a92ad0aeefe95`。

## RQ1_c772c59e4a76

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_c772c59e4a76) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-42.json](Queries-42.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_a7bf9487cc3f)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_c464f5bf000f7a08e7f2`，根位置 6862＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E13, E14, E6

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 98.638 秒，模型等待 43.307 秒，真实 solver 70 次，查询投影 82 项，动作记录含缓存 52 项。诊断 {'missing_claim_or_source_anchor': 3, 'action_slice_exhausted': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `5ae8684b669a4bd19bdeb1b323ebd52972416b863079039f046e7a9cbb79dbc0`，决定 SHA `081b8ace2c465ab2a34cbf8adfe40ff5e5ffd7a196f67b2a40810a75407a5538`。

## RQ1_ce670e623911

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_ce670e623911) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-42.json](Queries-42.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-35.md#rq1_4fb4fc48389a)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_93b6c989a2a57c45b6ea`，根位置 905＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 905. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3, E4, E5, E6

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.685 秒，模型等待 27.541 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 4 项。诊断 {'unknown_or_unshown_effect': 1}。

最终报告 SHA `de5a23b62d23f7f23e430ab78dc6966b9f26184b505b07602f3c6e9794f34c47`，决定 SHA `03a7cc89fe804af1c733e9b4722e3846f188e220f938c785685cdc56be424333`。

## RQ1_95c8d7e52370

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_95c8d7e52370) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-42.json](Queries-42.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-46.md#rq1_eb2353a0613f)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_de306af512e3d23d42fa`，根位置 6650＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6650. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 99.668 秒，模型等待 26.798 秒，真实 solver 67 次，查询投影 79 项，动作记录含缓存 52 项。诊断 {'no_locatable_source': 2, 'action_slice_exhausted': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `9f6d88b544df2bc3ed4bafe7e06f3805023bb27e2c0d42b2d197b05ca4547578`，决定 SHA `ae224fb1ab3977a64946676d8cdcb7fdfb5d801efaa904a3b6fa2808506bdccd`。

## RQ1_ce9f072e6cf8

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-13.md#rq1_ce9f072e6cf8) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-42.json](Queries-42.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-38.md#rq1_8c7b36b2c4f9)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 1, 'core_mismatch': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.935 秒，模型等待 76.819 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 49 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `1b989633cb38d9ce4776ecd3bae165351127351ef00dec9f4166fffd998c8ee6`，决定 SHA `1b0ed974824e1c642c95ac01ec6d5856199fc05ef866df36d7d92cd268fdfbb0`。

## RQ1_ede25a30c4e4

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-13.md#rq1_ede25a30c4e4) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-40.md#rq1_fccd9a0f9abd)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.272 秒，模型等待 41.981 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_effect_unbound': 1, 'no_locatable_source': 2}。

最终报告 SHA `cafa1d81604bf71728ff81cac7d03c24906a6c20094574b2f19d8e945b27c9df`，决定 SHA `18857715ad7031d5922d046d9cd7d9fe4e10f6ce73ab67621ba0ad7762520013`。

## RQ1_fd3cf52f44b8

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_fd3cf52f44b8) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-47.md#rq1_13ff7abd914b)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.872 秒，模型等待 32.213 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `5c4d4ef78e18e6e4e1b9bdfa8b33ed7dec71350bb3105772f8fc062f9e715b2e`，决定 SHA `bc389466a678b5ddebbd3076b3dc354b04c62540efc3e498a4259f5488459a43`。

## RQ1_b00cfec6e8e0

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_b00cfec6e8e0) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-42.md#rq1_af26ce7636a4)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.949 秒，模型等待 15.088 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `bac39b2fce4e1bd646c9ef8fd325d00b3f5c8b3a8699cd9c40b4982502cdcf79`，决定 SHA `51ca852e36acc0656ea9bf391b7e338ce9978d726ead7ce7e494f558e978ba54`。

## RQ1_1ffb833b5da1

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-13.md#rq1_1ffb833b5da1) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-42.json](Queries-42.json) [Queries-43.json](Queries-43.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-29.md#rq1_b472a9a0647e)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 13}。相关检查决定 {'scope_missing': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 184.958 秒，模型等待 57.759 秒，真实 solver 85 次，查询投影 248 项，动作记录含缓存 124 项。诊断 {'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 18}。

最终报告 SHA `31392b57d4f943c661ecd09124bb0d9c905e1f886f14c72a205d688c8d54c4a0`，决定 SHA `1db2ba390f49ca6c75e9a6698411af3365b0591b40df9b0910c442f267d9348a`。

## RQ1_8d60a47186e2

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_8d60a47186e2) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-42.md#rq1_7d7240a2af90)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'source_task_reading': 2, 'no_effect_in_scope': 2}。相关检查决定 {'source_check_excluded': 2}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.281 秒，模型等待 24.630 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'audit_effect_unbound': 1}。

最终报告 SHA `24eb0fccbbca4bff2675c4167f3de9f038a1a72cc064ff84568841c561109ec0`，决定 SHA `440a184d9455c4b000384257cc46c638200854978def2bab3f0efae963a933b8`。

## RQ1_0f3c3f400f6f

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-13.md#rq1_0f3c3f400f6f) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-43.json](Queries-43.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-29.md#rq1_5b3c7cbe3d9d)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'source_unit_missing': 2}。相关检查决定 {'scope_missing': 2, 'detached_local_holder_switch': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.217 秒，模型等待 47.432 秒，真实 solver 10 次，查询投影 10 项，动作记录含缓存 14 项。诊断 {'audit_card_text': 2, 'unrelated_or_secondary_graph_pairs_deferred': 5, 'semantic_meaning_or_explanation_polarity_unresolved': 1}。

最终报告 SHA `7b2a8addbf64add47a299e4fd5298baf927b2afaa30c16c3069cb39db245db85`，决定 SHA `bf51258e39c0bb99057d5f2e356624d4615bfb784ca0f6841c79be122b539bce`。

## RQ1_94fb41cd32a7

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_94fb41cd32a7) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-42.md#rq1_682abc2aac2e)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 4, 'necessary_effect_absent': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.447 秒，模型等待 19.826 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `2a5fb10b0ffdcc1c231a1cee9f4835a770e4d795dd1ed9af73f564a28b40d192`，决定 SHA `7b82f2e7d91326130b732b7f95a080b614d523e05b39f3fbd5dd06d2a4932ff8`。

## RQ1_53599b562d05

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_53599b562d05) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-43.json](Queries-43.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-34.md#rq1_28e029638666)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_f7de8559ba74ef75b090`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E23, E39, E41

发现 `finding_de9066ee8ba7d8063e08`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E21, E36, E38

发现 `finding_5597d2534e261ba8d1cd`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E18, E33, E35

发现 `finding_54fe24297bf7d78b0a52`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E17, E31, E32

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 31.643 秒，模型等待 25.764 秒，真实 solver 129 次，查询投影 123 项，动作记录含缓存 63 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 10}。

最终报告 SHA `c47add0a341d08d3841fd04237dfb67d052b4c19fd75c139eb7fb888d497461b`，决定 SHA `a8088c318a06f6df1bdbbf094e33c6271ba68f6749b420ebf5b16219a20002e7`。

## RQ1_60760b12532f

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_60760b12532f) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_837b1adf4a01)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'necessary_effect_absent': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.441 秒，模型等待 46.281 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `4657d0e5e7949f79a15098fbd3aa757ea3b4fd373ee2b6f2c240db3ca650685d`，决定 SHA `d9269be3b291b38c695aede3e309b5c933293ace2ade9cc82eb556d866265fcb`。

## RQ1_779895e65a3e

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_779895e65a3e) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-43.json](Queries-43.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-33.md#rq1_e28fb002ed8f)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 18, 'detached_local_holder_switch': 3, 'necessary_effect_absent': 16}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.289 秒，模型等待 30.672 秒，真实 solver 3 次，查询投影 3 项，动作记录含缓存 21 项。诊断 {'audit_source_scope_mismatch': 1}。

最终报告 SHA `ec39a2e0245c76270f163d1e90cb5135b568a652194747bd382e6334ba448762`，决定 SHA `f21f813bed467146d9fe0cc9c110e938ca89a7959d12c991a7147af472a7ed80`。

## RQ1_9171531dd52d

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_9171531dd52d) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-43.json](Queries-43.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_d967ae07a958)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 14, 'no_privileged_intervention': 8}。相关检查决定 {'scope_missing': 4}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 27.355 秒，模型等待 43.752 秒，真实 solver 21 次，查询投影 15 项，动作记录含缓存 94 项。诊断 {}。

最终报告 SHA `41331835953f4ce79a063593e84c22edd759fe3f21f9440ea963a89a293a4f4f`，决定 SHA `d7a31d582f54eecd1ee0f9ead1ab1264c616084d54da29728404dc5503f5859d`。

## RQ1_b0a696b11b0a

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_b0a696b11b0a) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-43.json](Queries-43.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-48.md#rq1_4f9f1ce04ed8)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 5, 'no_effect_in_scope': 3}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.682 秒，模型等待 9.775 秒，真实 solver 8 次，查询投影 6 项，动作记录含缓存 9 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `620447f3525fcc3e3eb6a82c60b8464a1ca999eb5abb8fdda9670e8463d01ab0`，决定 SHA `f440fd909cfff920a865d7432e31d55951737e0ad8992dcda17ea02ac981a628`。

## RQ1_980e04c92f4d

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-13.md#rq1_980e04c92f4d) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-43.json](Queries-43.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_6a278772c4f3)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'source_unit_missing': 2}。相关检查决定 {'scope_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.393 秒，模型等待 36.672 秒，真实 solver 6 次，查询投影 6 项，动作记录含缓存 10 项。诊断 {'missing_claim_or_source_anchor': 1, 'unrelated_or_secondary_graph_pairs_deferred': 4}。

最终报告 SHA `433d2c3daa8afab1ee9bccee8891d372ac6da5157d07730b79c813e05a3a607b`，决定 SHA `77611461b482f27e03fa673a4df61822f613fe9a3153d046dfa86424e237689c`。

## RQ1_ae0f59a34868

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_ae0f59a34868) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-43.json](Queries-43.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-37.md#rq1_d34dd1569ff4)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_31e878858c75e8a9b903`，根位置 2021＋342，依据 `program_support`。At burnFrom(address,uint256), a privileged effect leaves another holder with fewer rights in the same unit after attributed transfers and applicable settlement. 证据 E1, E10, E11, E12, E5

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.383 秒，模型等待 22.856 秒，真实 solver 17 次，查询投影 22 项，动作记录含缓存 11 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `6cef74dfadbce38bd1e0d9f6f7ca8962d96afb0cd9729dbb78161cccf61067a4`，决定 SHA `37be64fd0e5fd66e8b5f0335b6d7448a66c4ba76cd8b69798407c915f53f7961`。

## RQ1_37d9daf031da

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_37d9daf031da) · 检查明细 [Checks-81.json](Checks-81.json) [Checks-82.json](Checks-82.json) · 查询明细 [Queries-43.json](Queries-43.json) [Queries-44.json](Queries-44.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-48.md#rq1_1c6b43b24d4c)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_3a8ca4584a190b942432`，根位置 2435＋13，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2435. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E23, E24, E46, E47

发现 `finding_456e20c3c368718e6f87`，根位置 2435＋13，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2435. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E28, E30, E49, E50

发现 `finding_23c57cecbee58edf70a0`，根位置 2435＋13，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2435. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E26, E33, E34

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 919.030 秒，模型等待 57.772 秒，真实 solver 795 次，查询投影 1008 项，动作记录含缓存 29 项。诊断 {'audit_effect_unbound': 1, 'action_slice_exhausted': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `d536bc12ffcedfd4a00e81eeac61393f5cf86d9a4e5225cad00d09a7025f3d2f`，决定 SHA `5f4d15d1f2c7f69354b370ec192c589fb89834e363a020a779acdf9fc4be8822`。

## RQ1_cebbce39a728

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_cebbce39a728) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-28.md#rq1_d76214290589)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 13, 'necessary_effect_absent': 10}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.999 秒，模型等待 23.080 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `3c1b1207b81f24099336c1488452d529e21dba1cdf8b4b4f3e321bf191901e95`，决定 SHA `feadef125610718a4003c0b82498a1728ce0ec3baba9d5de1eefffcfd28cee9f`。

## RQ1_49db443acf1d

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_49db443acf1d) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-34.md#rq1_4febca8bfe3b)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'necessary_effect_absent': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.165 秒，模型等待 32.805 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `63e2451d74a8c61bbeba8513c5c25af2776bfb1900620f8d5cf8ef3f489f07aa`，决定 SHA `13a28fe6367c14dbc3e70ecc6c4d6ed02db18be66cae4f18fdbbb09b5a3ee80c`。
