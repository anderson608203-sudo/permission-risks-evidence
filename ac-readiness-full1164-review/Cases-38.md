# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_152053986776

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_152053986776) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-45.md#rq1_8bbb0c4ed7cf)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 5, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.181 秒，模型等待 46.373 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 19 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `17b8f7078bda93f6c4334e04212f4df3246ba18dd4d59bf2cf7393b94ab15971`，决定 SHA `c7178471ccd80469a4c0533f76911de080f8aabec703fb9029d2c455186c3aeb`。

## RQ1_4968e56244c9

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_4968e56244c9) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_b731957fa974)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'intra_ledger_transfer': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.529 秒，模型等待 31.443 秒，真实 solver 3 次，查询投影 3 项，动作记录含缓存 4 项。诊断 {}。

最终报告 SHA `b9804798f1e240e9631443ec1bebcc61d1eef64057e190a66ae50724936e6622`，决定 SHA `3d3127e6359176a210baddf386fd2e90f04c2800f000373353673a804ec869ce`。

## RQ1_7ca60ff656fc

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_7ca60ff656fc) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-29.md#rq1_0c8823eed851)。指定类风险端未检出、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 12, 'necessary_effect_absent': 12}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.891 秒，模型等待 30.264 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 6 项。诊断 {}。

最终报告 SHA `68bd786256c248c654472f9b3c242a5c77875e3ebbbe4562dfcf3a6e87aadc51`，决定 SHA `8ef2138056eb7e17b85f55763d6e739fb6f9512c21e3df5995ae7bb9ec6b4996`。

## RQ1_53f9777ccdf6

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_53f9777ccdf6) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-33.md#rq1_a7d72c1e4129)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_5089e94fb9fcd4e01d2b`，根位置 1118＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1118. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.621 秒，模型等待 26.956 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'missing_claim_or_source_anchor': 1}。

最终报告 SHA `5b443abc9e27db897e13d2b2030e410113d2cfd991bc4c7e39d522ed119580ba`，决定 SHA `064871e8fbe49d5196acd5691d76e3666e1d869a665640acc5e6a5ebfdfd017c`。

## RQ1_2b28415b963e

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_2b28415b963e) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-33.md#rq1_c87424c874d9)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_a6f6637797807d66c123`，根位置 6321＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6321. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 38.795 秒，模型等待 48.751 秒，真实 solver 60 次，查询投影 71 项，动作记录含缓存 51 项。诊断 {'audit_source_scope_mismatch': 1, 'audit_check_target_unbound': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `e472c127a89945537b0df7bec5ceb3217c6f560162bed819ee2bb06f0ca8b7a9`，决定 SHA `7be92c73888c9301bc6fbf2d32d44a48406a5df9a0949ac913d48db6a8eca6f6`。

## RQ1_6244da144ced

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_6244da144ced) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-48.md#rq1_90c233777f5e)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_27b7bf3a56139b971e74`，根位置 6173＋223，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E12, E14, E7

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 41.821 秒，模型等待 35.716 秒，真实 solver 33 次，查询投影 38 项，动作记录含缓存 64 项。诊断 {'audit_effect_unbound': 1}。

最终报告 SHA `b57f483bcfcc3795c6d92799663810789c7b68945aff517dccb09c8c51254d20`，决定 SHA `473edd305dd39bcedd9dd7e766ee50d3139f34e778235cba9593d449f73ce67f`。

## RQ1_a4df6c5b7701

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_a4df6c5b7701) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-33.md#rq1_65379f53b3ab)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 16, 'necessary_effect_absent': 10}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.553 秒，模型等待 19.396 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 3}。

最终报告 SHA `e1e81d03d34c034340e7f8ddc565b576217bcc9d87588be221859a8ed5ec2f88`，决定 SHA `6930428d804f86272fd90ae3e34c809735aad23c8e887f26d49b962d58656f1d`。

## RQ1_f1045931ef0e

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_f1045931ef0e) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-48.md#rq1_f2292d8956bc)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'source_check_excluded': 1, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.921 秒，模型等待 38.061 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 18 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `ec2b67df12a0d0f81ae0870b1a09fe660fc2195265acf74bbe6c35f7eab81aec`，决定 SHA `46954b94f08c43e117d8aef48639d5bd89cb88c0b0dd271405d2d8d103892632`。

## RQ1_a2450795f339

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_a2450795f339) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-30.md#rq1_ae0fb58f9d8d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'necessary_effect_absent': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.099 秒，模型等待 46.351 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `cee68969f3dfb3bf7577ee4db06d4a862b06cbb1a13f36e51eee0628b2270824`，决定 SHA `bff7ec7c886b2013cae2788bc83d0f0da0a470f6f357dc908afe4cf9828867fc`。

## RQ1_5379e0feddf5

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_5379e0feddf5) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_3e457bb920d2)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_ea466f0cf54f4fbeb421`，根位置 2249＋30，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 2249. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E10, E11, E5

发现 `finding_d9f0db867ef38056bbf8`，根位置 2249＋30，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 2249. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E12, E13, E3, E6

发现 `finding_09ab2876dcce4c5b7c87`，根位置 2249＋30，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 2249. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E14, E15, E4, E7

模型分析被消费标志 False，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.200 秒，模型等待 41.989 秒，真实 solver 3 次，查询投影 3 项，动作记录含缓存 13 项。诊断 {'core_unresolved_retained_for_investigation': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `299a423985696b35906332df31f1bd2db557bfed29cc5566b50c4311d94e0be2`，决定 SHA `73436b8d70603a38deb8eafe3871c8bfeea251d353de776bd300df49928033a0`。

## RQ1_6d1be3618953

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_6d1be3618953) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-45.md#rq1_5d9b73e823c2)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 1, 'source_task_reading': 1, 'no_effect_in_scope': 2}。相关检查决定 {'core_mismatch': 1, 'source_check_excluded': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.456 秒，模型等待 40.292 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `c468a311c0964311c0deec97553b91cbe8259d4a48eb10d0820c8fdda2448d09`，决定 SHA `2ee6e73da3fb3a166822984a599eca2a131aa1757701e012d2fb0638df03b652`。

## RQ1_a38f38fe9362

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_a38f38fe9362) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-29.md#rq1_b06b87a14839)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_4cf60c9bda8f09cc3fa4`，根位置 935＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 935. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E10, E11, E2, E3, E5, E6, E7, E9

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.525 秒，模型等待 55.415 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 7 项。诊断 {}。

最终报告 SHA `d74653b4d0d6c2474926d423fe93ccd655b9b0d8813781ed548f96875a272814`，决定 SHA `5f1cc810ed0f583a1089e0aff4805dad5e3c3009a44e6f800a68c1d043b7e900`。

## RQ1_531369afb901

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_531369afb901) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-29.md#rq1_3876731c1c31)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 3, 'necessary_effect_absent': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.143 秒，模型等待 28.697 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_effect_unbound': 1, 'no_locatable_source': 1}。

最终报告 SHA `4f6bfadeba910803daeeefd694e524ec843b3bb4f2ed2cc0d5820fe1f3851dc6`，决定 SHA `6a61894119bddfe0e343195bcc8a7560df694aced67081c15eda013558704aea`。

## RQ1_fe11616caf66

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_fe11616caf66) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-33.md#rq1_6476444da7e8)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_69fd27ca3e231e9e7735`，根位置 780＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 780. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E3

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.352 秒，模型等待 48.439 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'unbound_or_inapplicable_seed': 3, 'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `e3bdcac7490b7582b5c2031f2150a68f248009cca656e38f0e9fe8a957836441`，决定 SHA `40290abda8af40e5ce3cf29c9320c7c51e29e22df37bd339ad453479a3cbb9a1`。

## RQ1_e14ac08db6dc

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_e14ac08db6dc) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-33.md#rq1_60a6e918f2f8)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'no_privileged_intervention': 1, 'necessary_effect_absent': 1}。相关检查决定 {'source_check_excluded': 2}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.212 秒，模型等待 21.037 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {}。

最终报告 SHA `2abb780cee303a40650fe25b19272376c94447f85e76f98552c473e779c8357e`，决定 SHA `3874f844a434ed79432e8d0c38d9b518c50d5cf0ac75de55e6ab4d9bf0db96a9`。

## RQ1_c80f7a639e42

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_c80f7a639e42) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-37.md#rq1_30177d564271)。指定类风险端未检出、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.592 秒，模型等待 41.263 秒，真实 solver 23 次，查询投影 28 项，动作记录含缓存 39 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `c3b681d661b960c6241a31daca26bd1ef43bfdce584a6f0f076be0cb8c0bb049`，决定 SHA `a244c45eead70e7e558eee0d0d32a586a7e4c3db246f8b8fb76407678b498c56`。

## RQ1_db11e3e08742

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_db11e3e08742) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-45.md#rq1_353a9b0b5006)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'holder_consent_basis_unresolved': 2}。相关检查决定 {'scope_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 900.148 秒，模型等待 42.741 秒，真实 solver 194 次，查询投影 159 项，动作记录含缓存 29 项。诊断 {'action_slice_exhausted': 13, 'yield_to_source_bound_semantic_review': 1, 'program_investigation_budget_exhausted': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `4ac2d8333e09f86056ad3c2473b417da84e8a91e42e69c09beeab62b930bd0a2`，决定 SHA `9585679810b8e8a7953a9417c8bd41e02e3a5c619d11e6ac564ca98fe8b21b3e`。

## RQ1_0a95fcc25752

任务 FCR，评价类别 FCR-TRANSFER。当前未知，BG 未检出。

[实际输入](InputSource-16.md#rq1_0a95fcc25752) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-32.md#rq1_fa502559ffda)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 1, 'source_check_excluded': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.239 秒，模型等待 54.129 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 18 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `5b45be75d1e43c5694e0cfbd1a8d6e3a7ed63066181ecde4de22671926a4a018`，决定 SHA `a80dbe1ea4bd6286ee81ddca479e5dc566646551135567ed49c6283d43cb2780`。

## RQ1_8c7b36b2c4f9

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-16.md#rq1_8c7b36b2c4f9) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_ce9f072e6cf8)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_ea6d679312892a8786bb`，根位置 1293＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 1293. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1, E2

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.594 秒，模型等待 53.397 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'unbound_or_inapplicable_seed': 4, 'invalid_semantic_row': 2, 'no_locatable_source': 3}。

最终报告 SHA `aa0c50e8c105f36a10bc819a05dd6e116e245313775a09c461bec1d89dcb825b`，决定 SHA `c405fe9835c14479dfbb33643e5637d85a283ef892cd4473010b30e5d2802a24`。

## RQ1_aaeb3f57cfd0

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_aaeb3f57cfd0) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-45.md#rq1_20dfd0c54b94)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 14, 'no_effect_in_scope': 25}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.554 秒，模型等待 39.597 秒，真实 solver 14 次，查询投影 32 项，动作记录含缓存 22 项。诊断 {'audit_effect_unbound': 2}。

最终报告 SHA `7277ee2ac827c1b4ddf91b112789ec5edbb99678fecad5cf99de7249ce365af5`，决定 SHA `6d9e06fae4b16646e34858af513260335f6e97e3286c4fa26babfc46be46b315`。

## RQ1_c29df435681e

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_c29df435681e) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_ffcaa562a72d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_9c97fdbcbd11c2eed4ca`，根位置 1057＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1057. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.874 秒，模型等待 29.761 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'audit_card_text': 1}。

最终报告 SHA `672fa2d4d8a5ec76c0fef517663f3e4847df6a826753531efc29c8bc67235fca`，决定 SHA `27ae23dfcf6f6079f494dda5c41ae86a6fff3b64e39285889c71eb3967bcdfbe`。

## RQ1_093a006d2f90

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_093a006d2f90) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_f1438202b0d6)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_e88e27b6cfa8072f26d9`，根位置 2298＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2298. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.098 秒，模型等待 28.237 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `377823db13b0e8ac0cd0d9cff7a21d8f7a5e6bfe614ea7f0c4fd059f025d43a7`，决定 SHA `52ab2390377623af8b77ee20eec5ea553689d0fd67140a9217eb0b542bd170c9`。

## RQ1_ab687024c0d2

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_ab687024c0d2) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-45.md#rq1_cd25b92c3711)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 23.721 秒，模型等待 71.762 秒，真实 solver 26 次，查询投影 32 项，动作记录含缓存 28 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `db3af016a54daa69bb56aa62899c37a60981c5737b3a27144c6e853208898d61`，决定 SHA `e700fbc399efcab75ef8013f744ba711cda131cdcf3ea6d40d46f1c77050f06b`。

## RQ1_8503a353fe8b

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_8503a353fe8b) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-46.md#rq1_4a7b94cb63c5)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_60d356c1bd71439e4463`，根位置 9121＋28，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 9121. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E10, E2, E5, E8

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.286 秒，模型等待 44.747 秒，真实 solver 3 次，查询投影 11 项，动作记录含缓存 9 项。诊断 {'invalid_issue_field_shape': 1}。

最终报告 SHA `af5698bb6cb92cfbf34e5e0f66a4b88781b683cfc788f5ed737737a32197acb3`，决定 SHA `ea0eea6fd9e5e8c21b0385ded84189953a8c8c61bec9c67ea762134ed6d47477`。
