# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_0b0fd05c544c

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_0b0fd05c544c) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_22ff3dc40c99)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_87a612d2640cf467f704`，根位置 885＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 885. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E2

发现 `finding_621b78b7b2a362d05605`，根位置 885＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 885. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E3

发现 `finding_8f9292fdf563ac515c2f`，根位置 885＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 885. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E4

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.921 秒，模型等待 41.731 秒，真实 solver 7 次，查询投影 6 项，动作记录含缓存 6 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `b4c94da00d1d6899aa6b339299fc02a48cb9206f1659b5095d0f930b318ef7b4`，决定 SHA `cf9c9ba4df3a6a9da49a958696d55cac01b6923b2b726f0ff89cc70dcf8e313a`。

## RQ1_4eb968a3f9ed

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_4eb968a3f9ed) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-41.md#rq1_17311ea9d8e7)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_23a3b6af1d185b5d92dc`，根位置 490＋476，依据 `program_support`。At zero_fee_transaction(address,address,uint256), the scoped change moves another holder’s existing rights to a separate position without the applicable holder-issued consent. 证据 E1, E11

发现 `finding_9efcdf1a195713be313f`，根位置 807＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 807. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E3, E4, E6, E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.744 秒，模型等待 54.577 秒，真实 solver 5 次，查询投影 8 项，动作记录含缓存 5 项。诊断 {'audit_source_scope_mismatch': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `de30c4b852cd836f1fc6e3b65bee85c1f9d1bf2a0da410c80e66e364c1c016e7`，决定 SHA `3116c9214c96ac6b79ebb47c1bcac923b690e650c464dd1e9f67bd8fecd8459a`。

## RQ1_7405f0959142

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_7405f0959142) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-41.md#rq1_afb609e0053e)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 4, 'no_effect_in_scope': 6}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.496 秒，模型等待 50.599 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 11 项。诊断 {'explicit_effect_anchor_conflict': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `d3a4dcffb119d53ebd26269d833c02bacfdb2427268732a38c175b41e76f63e1`，决定 SHA `f9ed8b8a0f92db1bf8f4cbee2bf42d81322091c909ef7885fb11051962cb9150`。

## RQ1_7cd121e3acec

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_7cd121e3acec) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-28.md#rq1_a68ae7d1761d)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.291 秒，模型等待 36.475 秒，真实 solver 1 次，查询投影 18 项，动作记录含缓存 10 项。诊断 {'missing_claim_or_source_anchor': 3}。

最终报告 SHA `86edfbeafc550f77f7ccfd4e974b555bc5bfedff42cf0df49246e87d250040ec`，决定 SHA `d0addfbb575e0d3415d0a2e6a87c3378d2b8865ece4c4242ca7e24836130c55a`。

## RQ1_b84042e6eefd

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_b84042e6eefd) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-40.md#rq1_475c7d9ec738)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_5cbc66f7bb05a827c304`，根位置 1191＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1191 under transfer_condition. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E10, E11, E13, E14, E15, E5, E6, E9

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.291 秒，模型等待 81.666 秒，真实 solver 14 次，查询投影 12 项，动作记录含缓存 15 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `3cbcb5b44240b310645c73a0b364b459f012df69c3ef7a88bbcf5ec9c93fc7ef`，决定 SHA `f2929d7a0133c0be98b140ac55a6317b9ca20e9b134844c5439b072a50911fa7`。

## RQ1_88258f6d823d

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_88258f6d823d) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-29.md#rq1_16adbcc82eed)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.233 秒，模型等待 25.273 秒，真实 solver 11 次，查询投影 7 项，动作记录含缓存 14 项。诊断 {}。

最终报告 SHA `bbbbc3f16319fe11e37fceb2f049c91dc120534d1300653c4e683c42b55c2262`，决定 SHA `984e17562ccf65c70eb314574e4592b1035be65d84a81c4d249c3460807b6d37`。

## RQ1_39fb6e7197c4

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_39fb6e7197c4) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-46.md#rq1_7450d39da940)。指定类风险端未检出、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 15, 'necessary_effect_absent': 15, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.402 秒，模型等待 18.600 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `5a15f83d3d4def2bf234c446fbbc9aeeffcfa94dec5c697e895d963c49cc28d4`，决定 SHA `5c6627dddd7d8ff4d9c0aa64e24511b29fd448a1687c8c82be80bf7b8f960a39`。

## RQ1_5905f594ee2c

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_5905f594ee2c) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-46.md#rq1_493871f89451)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 2, 'source_check_excluded': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.415 秒，模型等待 53.003 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 29 项。诊断 {'explicit_effect_anchor_conflict': 2, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `c0e3cf7405d142e684e66a81ff93d290d42b75eb81131e0621977779c04f0517`，决定 SHA `c4bf870d909904f67493cd59a6d7396abc7690ac369564f2a1a715062fa03221`。

## RQ1_4e36475bca23

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_4e36475bca23) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_6eeaddaeac8f)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 8, 'source_task_reading': 3, 'voluntary_holder_debit': 2, 'necessary_effect_absent': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.998 秒，模型等待 40.345 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_card_text': 1}。

最终报告 SHA `8647042f1b8552bf8ccd49d00151de8fcea5d09a1a41de4e7ba197ba6177b9bf`，决定 SHA `b53f4996459bd0cf962c0601296d140ab44ed1c485a10bc9578de1bc2a74b17e`。

## RQ1_49ef001521e5

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_49ef001521e5) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_ba0ef60ed8a6)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 2, 'no_effect_in_scope': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.127 秒，模型等待 26.306 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `a275e99482c7a863d84d373fa930df1525f5b24438ded52c957164c17765db44`，决定 SHA `9e1b409de5b1ba96f6d9371bdc784167b7658b7d0d1cf30cee6599d3c8b82013`。

## RQ1_2d22977434b5

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_2d22977434b5) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-33.md#rq1_4169c528c5e4)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 20.615 秒，模型等待 27.656 秒，真实 solver 23 次，查询投影 29 项，动作记录含缓存 19 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `32e38918ed3e9a2e7c4f4058b2f1f8edb605955aa834e54b26f59ba191da5dd9`，决定 SHA `db502848f3d9389c4af7f08b76f8b38037053561ef94e07a7d882291bfb3a347`。

## RQ1_69def43bede4

任务 FCR，评价类别 FCR-TRANSFER。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_69def43bede4) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_708a354d4471)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.840 秒，模型等待 30.066 秒，真实 solver 7 次，查询投影 9 项，动作记录含缓存 21 项。诊断 {'unknown_or_unshown_effect': 2}。

最终报告 SHA `d465a3407ea51ad4cff679d850309a8cbc274bd302d85848eb59d42c92a795ca`，决定 SHA `bd02017bd917f477c6f2a742abf59e2e452bdf2e4ceb82e2f7c080b9aa55bdb2`。

## RQ1_05ad9d6a9255

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_05ad9d6a9255) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_a38c8e0b4785)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 5, 'necessary_effect_absent': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.145 秒，模型等待 43.129 秒，真实 solver 10 次，查询投影 15 项，动作记录含缓存 35 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `35b3339bb47f2b5dd56be86e7e6a3a826d8e77e91c4e00da8e497349f42ab7af`，决定 SHA `e5119c79300a34bdcf168b3fa4179b4a29361f120a6d9f9aa6ceaa0bc54b173e`。

## RQ1_55d45a664e73

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_55d45a664e73) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-46.md#rq1_26d74b856242)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_5968c0098206fa81077c`，根位置 1718＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1718. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E3

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.668 秒，模型等待 40.469 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 11 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `267b1f09b09aa33a010a79c79c52f1c88e7b42571aa0c1d3b5723dbbff10cb3b`，决定 SHA `26efb299f9bb4de5e66880191cdaadf2ca1a974e9431be8bd724440577e67c72`。

## RQ1_aa31074756ae

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_aa31074756ae) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-46.md#rq1_1861e7f6c2ff)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_764f8664caa32bb936ed`，根位置 795＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 795. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.141 秒，模型等待 42.126 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'audit_check_target_unbound': 2}。

最终报告 SHA `8b092d7f5737536172785a4bbcf4e95d18cdb06e28e034539cb5d0c47b41e378`，决定 SHA `f3c6e63b8e5c86105bb42360cec864fe75da4dbd7142b3e438c5d0c786a829a8`。

## RQ1_4e90985cd65a

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_4e90985cd65a) · 检查明细 [Checks-86.json](Checks-86.json) [Checks-87.json](Checks-87.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-36.md#rq1_128716025193)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 20, 'necessary_effect_absent': 20, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 900.340 秒，模型等待 46.079 秒，真实 solver 303 次，查询投影 221 项，动作记录含缓存 27 项。诊断 {'action_slice_exhausted': 14, 'program_investigation_budget_exhausted': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `37a511dc3e8be9676116ff8fe10cfa893a02a49e2361bdfdcc63b76a923927ec`，决定 SHA `8d513e5bcab31fba8bb6d146f304ff9674407c76d6ab85f7fc67533065506b64`。

## RQ1_8456d2957fff

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-18.md#rq1_8456d2957fff) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_776a6b98d18f)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_9f4587290ec3de83e384`，根位置 649＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 649. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E2, E3

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.232 秒，模型等待 53.410 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `930449783545a2c0f8c0907a7da424b629ebf204c5b860fc1f3dd771f9aaa09e`，决定 SHA `cc8d225d29d7e6dae5bce3566bc2ce4c7639fdbf37a041bbb28c96542d5f3775`。

## RQ1_32dbc2fa2433

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_32dbc2fa2433) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-49.md#rq1_c24c6c95ccbd)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 4, 'necessary_effect_absent': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.226 秒，模型等待 20.957 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `e5d1b1fa9e9479fa2edd184f3294a13ce3e8085b94226612287c470b9e9314d8`，决定 SHA `78582b6016276f4b43dba794d75dd9f3ab5bf7c35ac3aed83924d9022dd3d52d`。

## RQ1_55582b2a55f9

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_55582b2a55f9) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-39.md#rq1_caff62da8e8d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_ac9518be1a61036f454f`，根位置 834＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 834. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3, E4, E5, E6

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.363 秒，模型等待 42.511 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 4 项。诊断 {'missing_claim_or_source_anchor': 2}。

最终报告 SHA `b6075976f58ff69bf5c06e10dc7194d12e90d47ee1000aa0af48c5316ccff504`，决定 SHA `bdd76f28a4e5e148a0c50230a0e356759070b5053d1c60020d95026a5a327144`。

## RQ1_0e202076b336

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_0e202076b336) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-31.md#rq1_4feeb0c21e60)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 4, 'necessary_effect_absent': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.121 秒，模型等待 28.117 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'explicit_effect_anchor_conflict': 1}。

最终报告 SHA `996fb47dd8a06532e321cee0d5a632045e0b607ef41d058745802550f2c21707`，决定 SHA `2f0fae2af20a25af054b176d5b4b67b7462e1044c495f116fe9a974d91fc8c28`。

## RQ1_a763d3b1358b

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_a763d3b1358b) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-40.md#rq1_3f95723b36dc)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 4, 'no_effect_in_scope': 5}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.739 秒，模型等待 65.507 秒，真实 solver 9 次，查询投影 12 项，动作记录含缓存 29 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 2, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `c8c32835bb708bc47f652f0eb616404ea9cf9fd977267650a0a4779199637a0c`，决定 SHA `82864e69b2864144e4f5cff84e0176eca7b24c978dae1b75c4701510004e4fef`。

## RQ1_061399788fbe

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_061399788fbe) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-34.md#rq1_079ea1dcd765)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_d04bd28d7d45f74cf3c7`，根位置 6503＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E13, E15, E16, E4, E5

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 156.400 秒，模型等待 24.352 秒，真实 solver 50 次，查询投影 51 项，动作记录含缓存 34 项。诊断 {'action_slice_exhausted': 2, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `d9120719c47a1d205aeb495651997d63c2f09998cc7003104b50b3e47af4588e`，决定 SHA `3d9a909b6f47e7448900e43917e9d6b147919578fed1e27146d52ee5459986b2`。

## RQ1_9d38f4959633

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_9d38f4959633) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-67.json](Queries-67.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-46.md#rq1_c34d73ca2574)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_c93ceac6b5fd1122dce7`，根位置 6766＋30，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 6766. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E20, E25, E27, E30

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.094 秒，模型等待 26.525 秒，真实 solver 9 次，查询投影 17 项，动作记录含缓存 30 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `5072b01fb7e22f0bc1f17e18e0e7130ec2b6c3c728f8903ef1694f5141ef7710`，决定 SHA `759e12f0873ed7817d631b8ba27008fe60cd68d5b5dc523b8d00277f07f2b75a`。

## RQ1_727ea40e7fc7

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_727ea40e7fc7) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-46.md#rq1_f2dfe9d736b7)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 17.085 秒，模型等待 34.784 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'missing_claim_or_source_anchor': 2}。

最终报告 SHA `5e1d47d16f374c936d1987d75ea81053f457d1846b9141c4aa4b67a4cd89aa46`，决定 SHA `98c07204ac502989a5b365727ace9061245199f3fca2c39843a503adf5bcd892`。
