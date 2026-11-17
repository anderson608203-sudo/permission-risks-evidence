# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_884d05d552dd

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_884d05d552dd) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-46.json](Queries-46.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_726c2d2932a1)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_358092369cf517ee6c5e`，根位置 6785＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E13, E14, E6

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 119.578 秒，模型等待 44.747 秒，真实 solver 70 次，查询投影 81 项，动作记录含缓存 52 项。诊断 {'no_locatable_source': 1, 'action_slice_exhausted': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `e5c3d202e6ff0281cbb3c4114a360d9115d62a4e2565feaa3a08c9ed91afc33a`，决定 SHA `c3c0b90920705c57eb1e2044fa5613825bee6d0c39dce222fe125b7e4971c411`。

## RQ1_e1b72a383aad

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-14.md#rq1_e1b72a383aad) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-33.md#rq1_087c027282eb)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 8, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.432 秒，模型等待 18.630 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `8522ecff195ab8640786e73a64cf20835e4894afb1e8988863bcf85c270f619f`，决定 SHA `76979b982ae2eef237cb2a3c3ba59730dc1563999603402664c0ca4d5911df56`。

## RQ1_f2f95ed8c9c1

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-14.md#rq1_f2f95ed8c9c1) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-46.json](Queries-46.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_eb22e4884871)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.445 秒，模型等待 26.778 秒，真实 solver 16 次，查询投影 16 项，动作记录含缓存 10 项。诊断 {'audit_source_scope_mismatch': 2}。

最终报告 SHA `7a0571a5ef637741f70680aff75290d6d4ed2d2cd53b290915c52a3c6a3b005d`，决定 SHA `e674568742c07be58cb5d0c41ea9ad2bf8b09a298e85f59e8019ad8755b59c3b`。

## RQ1_2fc15b03a7f9

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_2fc15b03a7f9) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-46.json](Queries-46.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-41.md#rq1_c5a4d7205b9c)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_6dd089ef56323f702137`，根位置 4366＋24，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 4366. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E13, E14, E2, E7, E8

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.593 秒，模型等待 32.587 秒，真实 solver 6 次，查询投影 17 项，动作记录含缓存 17 项。诊断 {'audit_card_text': 1}。

最终报告 SHA `3897f5cac461ddec853ea6067d7b0ff799425da0fdc033a87dff4dcbdbbd2ca3`，决定 SHA `09de3a1c49e5ecc6d8511d4be813d1b3a571c57fcddc5246929800e908b1f611`。

## RQ1_cd03bb96c000

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_cd03bb96c000) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-46.json](Queries-46.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-31.md#rq1_1505712f3e55)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_50c49b505691b5b81bce`，根位置 847＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 847. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E4

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.516 秒，模型等待 34.759 秒，真实 solver 2 次，查询投影 3 项，动作记录含缓存 5 项。诊断 {'unbound_or_inapplicable_seed': 3, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `07f3a211ede3fba9046a1272fc69f7cb4cb6784aab723fbff0b5738df2af92ed`，决定 SHA `43fa3a0ffbe4c76551d03e4539d30a1019f3141a543c3f651d8db3b343b90892`。

## RQ1_2adba86dbbfd

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_2adba86dbbfd) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-46.json](Queries-46.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-34.md#rq1_d6441d8f6b1a)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_48b2128c33a49de5adfa`，根位置 5513＋477，依据 `program_support`。At mint(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E14, E17, E3, E9

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.273 秒，模型等待 23.572 秒，真实 solver 9 次，查询投影 23 项，动作记录含缓存 15 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `3ac9797eb3228ca1b3587bf6081ec556ac7ac92240d8f297c218bef2a84b64e3`，决定 SHA `71d9a5d7467d1b8dafc58a3899f6a32bdb858a62663a6fb4aff0f9ba89c26076`。

## RQ1_e28fb002ed8f

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_e28fb002ed8f) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-46.json](Queries-46.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_779895e65a3e)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_d415658e0620f7dcee52`，根位置 2586＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E2, E6, E8

发现 `finding_956ca61f83b22f885355`，根位置 2586＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E3, E9

发现 `finding_11fc7f1a30fc3a7fb59f`，根位置 2735＋30，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 2735. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E4, E5

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.139 秒，模型等待 26.141 秒，真实 solver 15 次，查询投影 15 项，动作记录含缓存 13 项。诊断 {'audit_source_scope_mismatch': 2, 'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `2d47f6206b826cc6315d15081ae4d2562be4d722f3595cf188126605ea4c47f2`，决定 SHA `0cc11684cb1d8114ed254cd7390597c89d5eea2dc6977adcdd41b94e27998252`。

## RQ1_ed2f6363ada8

任务 FCR，评价类别 FCR-TRANSFER。当前未知，BG 未知。

[实际输入](InputSource-14.md#rq1_ed2f6363ada8) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-31.md#rq1_acc2efe42317)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'source_check_excluded': 1, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.622 秒，模型等待 84.445 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 18 项。诊断 {'audit_card_text': 2, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `a3765344ad350472e203373c0f8fd1c6c422a0b79a194962aa6d4b9d78fd1af2`，决定 SHA `c9a4e84eb0537f5a0be8086f30e42e5c8ff4ed761eb4fe0563970389aef879a0`。

## RQ1_e6b597ab2090

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-14.md#rq1_e6b597ab2090) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-46.json](Queries-46.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-35.md#rq1_791eea9e8073)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 17, 'no_effect_in_scope': 17}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 36.041 秒，模型等待 47.310 秒，真实 solver 37 次，查询投影 43 项，动作记录含缓存 65 项。诊断 {'audit_source_scope_mismatch': 2, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `588117cdce337d84fced171c7b5b60527bfa270c198a97e8b4ee6937f3729a85`，决定 SHA `289268a8eca8d0ab14691b1ce759fd292a76d625a3a0674c37a5f30dd6ccc0b6`。

## RQ1_5eee31e70615

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_5eee31e70615) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-34.md#rq1_f322b5b8495d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_72165515ee6b804218d3`，根位置 645＋31，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 645. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E2, E3

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.006 秒，模型等待 46.021 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `d3176c16b9d847c6910f9b3cf71280e0dea9f77061c9728bd0ab28e99e62413f`，决定 SHA `e357d5787b3d43e33ddacbb65cf6d09bdcd1b172e2a3aafc694023e8099f87aa`。

## RQ1_a7d72c1e4129

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-14.md#rq1_a7d72c1e4129) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-38.md#rq1_53f9777ccdf6)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 8, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.257 秒，模型等待 17.877 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `c43c5c0006dbebc7ca78992d9ab636034bf34d3b7e6da542232b9f12ecf83212`，决定 SHA `ab3e488505bd1bf9ca9ac4fdb2ca9e57c48efa5e076870b1bc81017ba5c02054`。

## RQ1_6240ab1de377

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-14.md#rq1_6240ab1de377) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-46.json](Queries-46.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-36.md#rq1_4f69da2661f7)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 29.663 秒，模型等待 40.208 秒，真实 solver 23 次，查询投影 29 项，动作记录含缓存 19 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `7f3d30c064383e92884cf0f200d727fb946f9a443e91805be761ddbeda9ab657`，决定 SHA `c3f85cbe69764f4998acf55fbe1fa363770d1ceeec76ad64bec42951b3d0dbfd`。

## RQ1_1a94f7866801

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_1a94f7866801) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-46.json](Queries-46.json) [Queries-47.json](Queries-47.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_a906c0b62c0b)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_c80dbbde3624d70e2bb9`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E38, E46, E48

发现 `finding_c29c2af5f093dcbb2a9c`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E33, E41, E42

发现 `finding_42c9fdfe6d593f9403f6`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E40, E49, E51

发现 `finding_3beb93afebafe0505e0f`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E36, E43, E45

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 27.546 秒，模型等待 16.406 秒，真实 solver 121 次，查询投影 120 项，动作记录含缓存 83 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'unrelated_or_secondary_graph_pairs_deferred': 20}。

最终报告 SHA `5ae529736525a6ce8ac30605382f703b04353a5a126c71caaa7ea605b4f48442`，决定 SHA `9f4a21bdf3a7967c2f7efc230de136ccec78afb0e7b4a7b04872f57f3bb330ce`。

## RQ1_fa2207747d01

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-14.md#rq1_fa2207747d01) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-29.md#rq1_cd47d22b26a9)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 13, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.407 秒，模型等待 44.227 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `6bf78d9dce409b14192f39cb15fe270d28f081693cb9aabb734c5f5be065e810`，决定 SHA `1618f29c1dc874b72bd39de688913f434995b2ee6208b256d6ba096bc92b170e`。

## RQ1_087c027282eb

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_087c027282eb) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-33.md#rq1_e1b72a383aad)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_bd99bbdc79c171620ed9`，根位置 785＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 785. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E3

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.592 秒，模型等待 25.897 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `4d8c5f614bda74d8299239fe6643def59b0e21752dd926a9b73f49010f818c81`，决定 SHA `0808ad9e1cc8c1463a40825043f6bebf3a2851ca6483bd27474cdbc742db9798`。

## RQ1_73b13298e227

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_73b13298e227) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-47.json](Queries-47.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_024b9da10799)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_e8b522a0fd528c8140f2`，根位置 27939＋1574，依据 `program_support`。At distributeReward(address,address,address), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E125, E126, E127, E128, E13, E134, E135, E136, E137, E140, E141, E142, E143, E146, E147, E148, E149, E152, E153, E154, E155, E17, E21, E37, E55, E56, E57, E58

发现 `finding_d71cb190a9019a5e625f`，根位置 21919＋932，依据 `program_support`。At mint(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E1, E103, E104, E160, E161, E167, E168, E171, E172, E41, E45, E46, E93, E94

发现 `finding_2f065fbbd7a710c2041f`，根位置 23761＋2374，依据 `program_support`。At burnFrom(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. The intervention can enable a new same-request outcome; baseline commitment is not established. 证据 E10, E101, E106, E132, E183, E186, E189, E192, E198, E210, E211, E69, E7, E87, E91, E96

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 95.581 秒，模型等待 48.814 秒，真实 solver 144 次，查询投影 313 项，动作记录含缓存 188 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 8}。

最终报告 SHA `a78558405f3296cc9d8be1b1af2a1b8eefa4c1676386dd5a0bfd02f1f4c2076f`，决定 SHA `359490de66d713257f1ecd6758e230ca27ed75aa1799a86d7491548c9976b2b9`。

## RQ1_65379f53b3ab

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-14.md#rq1_65379f53b3ab) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-38.md#rq1_a4df6c5b7701)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 2, 'external_dependency': 1}。相关检查决定 {'scope_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 28.694 秒，模型等待 11.009 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 7 项。诊断 {}。

最终报告 SHA `d2ec19d4818c867f2983068eab6deb09ae1655688ef06f4340da85bb6506d478`，决定 SHA `00a3bcaefbfd0ed83068b0ac742417826d73581479a7aaace97a370a7b5a2754`。

## RQ1_c87424c874d9

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-14.md#rq1_c87424c874d9) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-47.json](Queries-47.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-38.md#rq1_2b28415b963e)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 29.617 秒，模型等待 30.392 秒，真实 solver 23 次，查询投影 29 项，动作记录含缓存 19 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `203d82f96d77ecab23abe699458a4eac5611cc838d863da67f8f1de36902af28`，决定 SHA `7449035163dae730894c0c768c1469e2879f0db0b96f2f79bbb0994836e74b80`。

## RQ1_7a54127ed44c

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-14.md#rq1_7a54127ed44c) · 检查明细 [Checks-82.json](Checks-82.json) [Checks-83.json](Checks-83.json) · 查询明细 [Queries-47.json](Queries-47.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-32.md#rq1_4d2acebaa2ff)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 27.257 秒，模型等待 76.441 秒，真实 solver 23 次，查询投影 15 项，动作记录含缓存 47 项。诊断 {'audit_check_target_unbound': 3, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `bee24d0f41151c3a800b83d26126a7d600cca8aeab3fa53129532882b202d8b8`，决定 SHA `b8f043c0bfd432d1fce93e8e748f938b46b9c2fab2efa9351ea5668da90292e2`。

## RQ1_6476444da7e8

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-14.md#rq1_6476444da7e8) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-38.md#rq1_fe11616caf66)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 1, 'effect_range_decided': 1, 'no_effect_in_scope': 1}。相关检查决定 {'source_check_excluded': 2}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.234 秒，模型等待 43.790 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `4a59085e702fb8787dfab957ea9ea56525c23e10f11b622b99db6fbfc037d873`，决定 SHA `179db916d28089617b6f7e332a91d668ed51ea8abc1ea7c32ac8bb68492ca826`。

## RQ1_7cc11a697bd2

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_7cc11a697bd2) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-47.json](Queries-47.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_3421c09bc85c)。指定类风险端报警、修复端报警，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_0f630fdd99240bee7456`，根位置 5232＋373，依据 `program_support`。The change at setTokenExchangeRate(uint256) affects the same holder request at fallback(). The checked difference is a new positive entitlement for a controlled beneficiary. 证据 E1, E10, E13, E14, E15, E18

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.607 秒，模型等待 45.683 秒，真实 solver 22 次，查询投影 17 项，动作记录含缓存 16 项。诊断 {'audit_source_scope_mismatch': 3}。

最终报告 SHA `8b58a01581e10f83d5e56222592128d4b39bab2f522e8610a2cd742064b5ce40`，决定 SHA `424d2be12b1ada4539fe8393a93135385d82281d902542e0e208741f70346c85`。

## RQ1_60a6e918f2f8

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_60a6e918f2f8) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-38.md#rq1_e14ac08db6dc)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_372e9fcbc34f6dc32747`，根位置 649＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 649. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1, E2, E3, E4

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.111 秒，模型等待 26.173 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {}。

最终报告 SHA `108a4f57e8f3dc3abe36ff8d44de4149086fb8ccb47ee82b15ec6a3927e4eb40`，决定 SHA `a0b9b19ec8f2c124225c75b4342e58c4f657d8c5b92fef4d803e5ecab8359531`。

## RQ1_3db9d6846001

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-14.md#rq1_3db9d6846001) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-40.md#rq1_615f9f99c585)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.905 秒，模型等待 39.561 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'unknown_or_unshown_effect': 1}。

最终报告 SHA `634a3d6c4f83a395003e1126e1244e8376c4cb649e589ea5afa299b8dc2520a9`，决定 SHA `be4574f3f878852c68518fe050ab09be45722047ccd5c6140690a695599c334c`。

## RQ1_4169c528c5e4

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_4169c528c5e4) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-47.json](Queries-47.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_2d22977434b5)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_f80c681d354e96c76777`，根位置 6653＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6653 under financial_right. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E26

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 139.671 秒，模型等待 36.253 秒，真实 solver 90 次，查询投影 102 项，动作记录含缓存 198 项。诊断 {'action_slice_exhausted': 1, 'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `d6cbf47aedad92279a16be20eb0311280ebb9595f6731fde96400dad24ee13c9`，决定 SHA `d7a654af8b1d59815bb7ddc90234341eb9cb343eaff036129f8981d8f8f86f64`。
