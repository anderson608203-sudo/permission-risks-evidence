# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_440857b3df3c

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_440857b3df3c) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-63.json](Queries-63.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-29.md#rq1_a4881b0828b3)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'covered_holder_grant': 2, 'scope_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 169.137 秒，模型等待 49.410 秒，真实 solver 126 次，查询投影 168 项，动作记录含缓存 118 项。诊断 {'no_locatable_source': 1, 'action_slice_exhausted': 2, 'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `63abcc44b690eb26ea3a6660096333f9cc15b8d4eb1198f9dc62ae6638ff0793`，决定 SHA `bca896f95f552735e4c2dc385967048267fde0a64e89b5a2fa3b4ea5c681e5ac`。

## RQ1_f138415fcb0f

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_f138415fcb0f) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-63.json](Queries-63.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-31.md#rq1_a294f9ad1c29)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_b3e593f8a8e7066c58ac`，根位置 778＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 778. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.245 秒，模型等待 37.341 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `a471983795b2f0e6eb6a5aef8583d722466933b7a22b37a317e9b652525ac7a9`，决定 SHA `9f70bc4baee29548566d8f6fec457d8d15af8597adfa9690fbdbc6501049aa29`。

## RQ1_cac16ccd972b

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-17.md#rq1_cac16ccd972b) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-27.md#rq1_2fde609553be)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_089e772365e437fe78e6`，根位置 904＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 904. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E10, E11

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.015 秒，模型等待 49.455 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 32 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `91de5fa1117de341d9bf4409a7d66675f3a52e96cc468f456d6aa8a9ad0649e4`，决定 SHA `59aba9803b38c2762555ab3532fd1e877e9eef50d3482bfc25ebff65754f5c1a`。

## RQ1_e5e7e5764fff

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_e5e7e5764fff) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_324b7ead5ac7)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 17}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.289 秒，模型等待 32.948 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'explicit_effect_anchor_conflict': 1}。

最终报告 SHA `f438e058e97adf2cbfc921d42341539c88413f6147a951b8e4fc929c0f66ba7f`，决定 SHA `40e6895bcedf4f0c3f966b68d32fd84bb5cefa343ce06ccd8220b760198f354d`。

## RQ1_f4327be729a4

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_f4327be729a4) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-63.json](Queries-63.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-48.md#rq1_12a3a2848c3c)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_100b8992cdc315a01a42`，根位置 1110＋308，依据 `program_support`。At burnFrom(address,uint256), a privileged effect leaves another holder with fewer rights in the same unit after attributed transfers and applicable settlement. 证据 E2, E23, E28, E29, E31, E35, E39, E5, E51, E52, E53, E55, E60, E8, E9

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.868 秒，模型等待 28.951 秒，真实 solver 17 次，查询投影 35 项，动作记录含缓存 57 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1, 'missing_claim_or_source_anchor': 1}。

最终报告 SHA `8f3378c157d3f40ba389c1d9e879ad44d5cbfddb01752a107675d54697ced460`，决定 SHA `66a928248804aa740637eaef2147bd417d116d1cfb8fa3d64419d4abce6227f4`。

## RQ1_f7686568e9cf

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_f7686568e9cf) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-63.json](Queries-63.json) [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-42.md#rq1_82b185a4c878)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_f80c681d354e96c76777`，根位置 6653＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6653 under financial_right. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E3

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 41.344 秒，模型等待 69.204 秒，真实 solver 62 次，查询投影 74 项，动作记录含缓存 68 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `c260fbd472f776d6dd1d8958dffa448c2b76139806b9f95065c53e71c6a4f6d9`，决定 SHA `38b043a9d906c047e29d45306fac4fa4654b5d2b647b416106cf7b45599d58e6`。

## RQ1_17311ea9d8e7

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_17311ea9d8e7) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-44.md#rq1_4eb968a3f9ed)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 2, 'no_effect_in_scope': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.162 秒，模型等待 42.325 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `18ee550deb17edd4882c8d0f8c1768ad50a683fd1cd2416deefb412bea8f2800`，决定 SHA `fd9c06240e3eb834d1bb37c33515a1d1920d64809e517330477f146a4b72e9b4`。

## RQ1_23abf434df32

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_23abf434df32) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_805b30020e56)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 1}。相关检查决定 {'scope_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.843 秒，模型等待 49.244 秒，真实 solver 6 次，查询投影 6 项，动作记录含缓存 18 项。诊断 {'core_unresolved_retained_for_investigation': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `a1995d846d43dd7a274fe95bc14e65782d63d220492e2c5e65952b24622661e1`，决定 SHA `aecfa4a234b5bb0d6f2fde365d1f0e1c774de6c65e018984fcf56f364ab9b189`。

## RQ1_c9a45d0b378e

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_c9a45d0b378e) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-28.md#rq1_8bacff1e94bf)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_5369f0adcc9d336d40d5`，根位置 6605＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6605. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 63.117 秒，模型等待 27.514 秒，真实 solver 63 次，查询投影 74 项，动作记录含缓存 51 项。诊断 {'audit_source_scope_mismatch': 2, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `fddc3c9828f187310762ee82eb1791e02d4eacac7b03b9e9298b2c712a9bc9e7`，决定 SHA `463aa04a613cd579790393289e81b075987009d9df7f3778aaf891339da60eb2`。

## RQ1_e38d4cc9d6fc

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_e38d4cc9d6fc) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-42.md#rq1_890376502486)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 6, 'necessary_effect_absent': 2, 'no_privileged_intervention': 1}。相关检查决定 {'source_check_excluded': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.377 秒，模型等待 42.137 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 9 项。诊断 {'unbound_or_inapplicable_seed': 3, 'invalid_issue_field_shape': 1}。

最终报告 SHA `a20c072502bb70efa0e4f1e15e86bbf1eede29663da27cc8001ed4b367f89624`，决定 SHA `3c609f8c8b3798f0a99e534c87aa1f95c23a68e645df2556906bb8bd4b74ed98`。

## RQ1_c5a4d7205b9c

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_c5a4d7205b9c) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-33.md#rq1_2fc15b03a7f9)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 8, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.645 秒，模型等待 10.036 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `f6dc5f047a460f130bdb858afb1b0687e2caecaaf8a2a2a7296247c9e8f9f48b`，决定 SHA `ac4baf14cad7c7402cb6d126e13dcc464e5d856618109c5823af76b7f0a0f5ce`。

## RQ1_cae7abe2d02e

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_cae7abe2d02e) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_7b9a317c57e5)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_a571a7cb7e85a22b6c15`，根位置 1530＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1530. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E4

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 29.926 秒，模型等待 10.930 秒，真实 solver 42 次，查询投影 15 项，动作记录含缓存 8 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `51eba3a9fe62a12436c89011497f6fd6b0ef2aa1a726baeae7339893bc7de5da`，决定 SHA `9cd17f5c4efa5a521bd08929838af67fb77b698ea8fd446dd5c279fc3ed04c3a`。

## RQ1_da692acb223b

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_da692acb223b) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-49.md#rq1_8e4c324fa1c9)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.354 秒，模型等待 60.030 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `b891f3ac15509223ddd74fcd56e60e6de77d6964316446bb32e237c639b3c84b`，决定 SHA `79913415e8a912455bb634545b6f996292b5026ebb409fe0ffd1e8708285265e`。

## RQ1_dab923cbe924

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_dab923cbe924) · 检查明细 [Checks-85.json](Checks-85.json) [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-29.md#rq1_5422392a2f99)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_05a6393ba61668fff872`，根位置 6432＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E26, E33, E34

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 79.355 秒，模型等待 25.935 秒，真实 solver 46 次，查询投影 52 项，动作记录含缓存 150 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `9e1fbb6beffc19b183707af430303c9a33856e6d89c6739d8a2c4213b2952eca`，决定 SHA `73fa960f1801208aa2fcea50eb9154791f577b6d124e6ccaedd02885b72baac1`。

## RQ1_7436b958fbde

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_7436b958fbde) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_0deaf993134d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_dc6db29466b8a4c6b26d`，根位置 2597＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2597. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E3, E5

发现 `finding_a75ff00d19b428fb68df`，根位置 2597＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2597. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E2, E4, E6

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.546 秒，模型等待 32.226 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 6 项。诊断 {'audit_source_scope_mismatch': 1, 'explicit_effect_anchor_conflict': 1, 'no_locatable_source': 1}。

最终报告 SHA `e937d320341b991863929bd2646ce65e4956c10687ab2bcd340ef0c44fe3833f`，决定 SHA `ae179429883bcfdcd9a765695c69b84cac7734e940bb83d4852d753039746b62`。

## RQ1_93214586f5e3

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_93214586f5e3) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-47.md#rq1_f8cb9b233996)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {'external_dependency': 1, 'scope_missing': 1, 'intra_ledger_transfer': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 74.648 秒，模型等待 61.906 秒，真实 solver 61 次，查询投影 63 项，动作记录含缓存 122 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `045b6d0e8e28a24e91d4417b21ad09cdd14b7b853487406f96f030388d559a67`，决定 SHA `b9944ca3108433e4fd8d46299f9b458ef82e4d18d334374f37bd38d9c9377243`。

## RQ1_afb609e0053e

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_afb609e0053e) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_7405f0959142)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_4c46722f96db72b51063`，根位置 1222＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1222. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E4, E5, E7, E8

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.542 秒，模型等待 20.722 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 7 项。诊断 {}。

最终报告 SHA `1387433156839182462aab292a2aaf2e379c8b03e23bea7786488cfb33a0028d`，决定 SHA `09f6b42b7bf8a333b69bd74b0c69b3bf28c58fe6421cb4229247bd5e6ccf0829`。

## RQ1_bba85280c610

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_bba85280c610) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-49.md#rq1_f814ab33ae2c)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_01149cbf06aadbc5c73b`，根位置 6654＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6654. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E13

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 110.965 秒，模型等待 49.883 秒，真实 solver 80 次，查询投影 92 项，动作记录含缓存 117 项。诊断 {'audit_source_scope_mismatch': 2, 'action_slice_exhausted': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `f901f2f0d89ff8f7b0b1f6e5cec96698e840daadf2cd9f7df9559cbac707f9cd`，决定 SHA `9d7a6d6eee725b47a26291bd3554a2fbe3079696a4da2b75452b5df5010f08a2`。

## RQ1_30c29cd44cad

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-17.md#rq1_30c29cd44cad) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-28.md#rq1_329e0d0d7a11)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_58157223f11f5931f558`，根位置 1127＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 1127. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E3

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.322 秒，模型等待 34.085 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {}。

最终报告 SHA `42dbb676b16a65f4475731a79807780052de84bafb7aa6864f7a9a7ca1b2832e`，决定 SHA `e9bb64449e4210fe2a09b92cda793f17f3f35eb5800c24a59ee78d8c2c407271`。

## RQ1_e1ce695fff9e

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未检出。

[实际输入](InputSource-17.md#rq1_e1ce695fff9e) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-28.md#rq1_bcafc7a40ce2)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 1, 'source_check_excluded': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.810 秒，模型等待 45.414 秒，真实 solver 9 次，查询投影 12 项，动作记录含缓存 31 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `abe109b84d9db30f65e483f2bf171eb59af500453d8ce8f02cc5bdaa16687cb2`，决定 SHA `9a8cb75c258a265ae524e3a8a6d91026002570fc505355fc62ad02af2c4c8db2`。

## RQ1_fe7add810da5

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_fe7add810da5) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-28.md#rq1_15346457ba72)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 1, 'no_effect_in_scope': 2, 'no_privileged_intervention': 1}。相关检查决定 {'source_check_excluded': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.063 秒，模型等待 43.251 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {}。

最终报告 SHA `f15fb7d980f4381cfe2a03f3ce265c430ad52009854e1e7e30f2c54e5e29a564`，决定 SHA `6b079ff4a5a88d86b7527652cbe374ceebe44fea399141a3dfd5c18b0853d4e4`。

## RQ1_a00b1c9a49ed

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_a00b1c9a49ed) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-29.md#rq1_a06d7492b7fb)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_e3dd2fa1d2ac6addb2d5`，根位置 799＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 799. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.696 秒，模型等待 30.529 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `38616a4e801d4a344fd851659cdf9dea44faf3128e08b45d4399a98366798d88`，决定 SHA `6c74b3645253007cde174e0baa1c3a08038ae94f384446743354ead2595c4065`。

## RQ1_3e235f5e70d4

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_3e235f5e70d4) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-48.md#rq1_abb48ccfac75)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 15, 'necessary_effect_absent': 14, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.220 秒，模型等待 24.303 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `4b2401f619166a0ba5016848288e942cce177133a54ecf574bf05928d6e1fa89`，决定 SHA `3f0a15232007692b8b4b1cb4341f7f715f9668561fa82cc7e5f056e3aef5e498`。

## RQ1_7a7815b00180

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_7a7815b00180) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-29.md#rq1_5b3469baa447)。指定类风险端未检出、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 6, 'necessary_effect_absent': 2, 'no_privileged_intervention': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.468 秒，模型等待 42.485 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_card_text': 1}。

最终报告 SHA `a730f73bbd9e2a948c6f0712f81c85cd175e6bfc17235495293fd6d43d4c0a42`，决定 SHA `2e624a73e4a5b7d45c29d5d1f5c27e3caf071d92b2a66fb432bdb1217403ac07`。
