# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_f063a93ac733

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-19.md#rq1_f063a93ac733) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-70.json](Queries-70.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-32.md#rq1_2f2191589195)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'scope_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 32.823 秒，模型等待 55.790 秒，真实 solver 36 次，查询投影 38 项，动作记录含缓存 30 项。诊断 {'audit_source_scope_mismatch': 3}。

最终报告 SHA `8c13cbc5ff869db5f1458de33a6c8d9599908519436d2d0ef68bee96bae74bb9`，决定 SHA `a2941991a76feb03ab7f41cd574c41b0b09f4682f1b663d0ebc32d984b559968`。

## RQ1_6292cc10d171

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-19.md#rq1_6292cc10d171) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-70.json](Queries-70.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-40.md#rq1_dd2a94075ff4)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.842 秒，模型等待 26.527 秒，真实 solver 13 次，查询投影 13 项，动作记录含缓存 32 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `686a31a297f75280f2be272ba6980510ebcddd1b2fd98f1458d2ac813320faf3`，决定 SHA `b13844c1fa9173c6981f9d94cebba853abafd26286826129d1d8548296ed5125`。

## RQ1_b5217318672e

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_b5217318672e) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-70.json](Queries-70.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-37.md#rq1_72c6b8c6b605)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_664955b9333ef662a1b0`，根位置 1118＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1118. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E2

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.890 秒，模型等待 59.808 秒，真实 solver 6 次，查询投影 5 项，动作记录含缓存 18 项。诊断 {'audit_effect_unbound': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `a32d377b42cce37108b8c0595edfd4fac0664b74eec89f5d4c96f7efef905a14`，决定 SHA `f611afc4844abbe3b5acbe1137acf7e34b064d83cab9458c4a3fab8a50923710`。

## RQ1_7450d39da940

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_7450d39da940) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-70.json](Queries-70.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-44.md#rq1_39fb6e7197c4)。指定类风险端未检出、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 15, 'necessary_effect_absent': 14, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.579 秒，模型等待 20.740 秒，真实 solver 3 次，查询投影 3 项，动作记录含缓存 3 项。诊断 {}。

最终报告 SHA `aaf68a622ecea4d23618c7a9518b2c96c782a5331f3158c31c6b60b4edd3ac3d`，决定 SHA `c781ca48f52da87453be8e804d60a766c456858cb9add764a46c2ee433d9bd78`。

## RQ1_29150828cc1d

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_29150828cc1d) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-49.md#rq1_1fbdcc5aa4c2)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.859 秒，模型等待 25.671 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `8a7d4065d1b15c5e6f2236bba2227537e5abd8e349c118d88aa04b7145a0e1af`，决定 SHA `96a51146f8d3dbdb65ed7314267199b15a8a3aca322b743f5e9443b9c13e1de7`。

## RQ1_1861e7f6c2ff

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_1861e7f6c2ff) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-44.md#rq1_aa31074756ae)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 3, 'necessary_effect_absent': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.090 秒，模型等待 27.035 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `1abb6d1f5f677fb5fc1c0c4b314be7a0c9b50d35d839e37041392596f7c3349b`，决定 SHA `fa8ff87f4abcfc84d1cf25b52d3bc61cba8e57ceb3d8b472624a16982ea0c9de`。

## RQ1_f2dfe9d736b7

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_f2dfe9d736b7) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-70.json](Queries-70.json) [Queries-71.json](Queries-71.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_727ea40e7fc7)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_5328e272ebffccb38d7b`，根位置 9766＋32，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 9766. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E65, E66, E67, E71, E73

发现 `finding_5de88557002e88d46f54`，根位置 9832＋300，依据 `program_support`。At freezeWithTimestamp(address,uint256), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E68, E69, E70, E75, E77, E82, E84

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 765.962 秒，模型等待 54.672 秒，真实 solver 705 次，查询投影 1281 项，动作记录含缓存 235 项。诊断 {'yield_to_source_bound_semantic_review': 1, 'semantic_meaning_or_explanation_polarity_unresolved': 1, 'unrelated_or_secondary_graph_pairs_deferred': 5}。

最终报告 SHA `ca36edb070814168e23fa5f30293aecdd0955c55a733652bbece5f1a870d93bd`，决定 SHA `2ab2033d4b93c2117b39341dce6fd072e14341b83183b573d17790f44106e33e`。

## RQ1_11a74fb21495

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_11a74fb21495) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-35.md#rq1_c2a474194a28)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 3, 'no_effect_in_scope': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.135 秒，模型等待 54.233 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `898d9b7a3ed8f8c87d0beca7e44ec08d6ba596a565b63e1d382fb0ba8fe8d62a`，决定 SHA `2ca5f18886fcb223257b5bb23b22bf7181db799d31939cb2f3e913274bbb04b8`。

## RQ1_eb2353a0613f

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-19.md#rq1_eb2353a0613f) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-71.json](Queries-71.json) [Queries-72.json](Queries-72.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-30.md#rq1_95c8d7e52370)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 31.648 秒，模型等待 20.238 秒，真实 solver 29 次，查询投影 35 项，动作记录含缓存 33 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1}。

最终报告 SHA `f4b1d263b5582e353e8c5b81f167f379b4ae12e8407ab5d14574f07dfff8c162`，决定 SHA `b5afa7f01530855983f2818d78e6d35f9d680e55d44c35f180b2100f8b3b6b46`。

## RQ1_c315645e4627

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_c315645e4627) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-72.json](Queries-72.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-40.md#rq1_cbb6e67b8b81)。指定类风险端报警、修复端报警，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_307fdfb81e2fb6aa97e0`，根位置 8917＋1612，依据 `program_support`。At allocateToken(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E1, E10, E11, E39, E4, E40, E42, E44, E45, E47, E48, E64

发现 `finding_c294c6189821d7fb3e43`，根位置 5091＋361，依据 `program_support`。At setTokenExchangeRate(uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. The intervention can enable a new same-request outcome; baseline commitment is not established. 证据 E23, E33, E43, E49, E53, E55, E62, E7

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 21.581 秒，模型等待 24.075 秒，真实 solver 53 次，查询投影 49 项，动作记录含缓存 57 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `56a68adba966bed59dceb721fbe85befa9362e72d93f865c2377b199d35bed1f`，决定 SHA `9144fafd46dd0e26269d54c94d388b39c2815c91bac390faf15bf9af3a106352`。

## RQ1_df25b8b8c6ab

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_df25b8b8c6ab) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-72.json](Queries-72.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-28.md#rq1_9ad7e9b41e3a)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_0b047f4ec55a9767d322`，根位置 11129＋955，依据 `program_support`。At mint(uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E1, E13, E14, E5, E59, E60, E61, E62, E63, E64, E66, E67, E68, E69

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 15.873 秒，模型等待 31.771 秒，真实 solver 58 次，查询投影 57 项，动作记录含缓存 65 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 4}。

最终报告 SHA `6df3d4eba5f969a9ded1f0bf5e4bf2abb223a4d6932789649baf0d7dfb19bec3`，决定 SHA `bcab813761e981b321ce26c302bd901075e0a68c25fc9d575b7f124492fb0fb7`。

## RQ1_107e84e04a84

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_107e84e04a84) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-72.json](Queries-72.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-35.md#rq1_868296d21a79)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 3, 'necessary_effect_absent': 3}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.782 秒，模型等待 42.100 秒，真实 solver 3 次，查询投影 3 项，动作记录含缓存 29 项。诊断 {}。

最终报告 SHA `d012a5bce6d2b55c44c88f4e71ec44771dacc06ffe459345dd6f77f349410fc4`，决定 SHA `c8551581dbc21899dddc74dabf5062f6b5261fbcdd5f8675bd29cdeaeac41240`。

## RQ1_0c666ce785e8

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_0c666ce785e8) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-72.json](Queries-72.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_3455b6a9ba4f)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_07981f7b477aeb5994fc`，根位置 850＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 850. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E4

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.526 秒，模型等待 40.980 秒，真实 solver 5 次，查询投影 4 项，动作记录含缓存 11 项。诊断 {'missing_claim_or_source_anchor': 4}。

最终报告 SHA `8858737ef3847165f508d638b32842482a203fbb69663dbe2d3da9c2bfb241de`，决定 SHA `3a398dec8047e44abc7f8b50633b22a7a4f26c63838c46cc99bf994d4146d99e`。

## RQ1_c34d73ca2574

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_c34d73ca2574) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-44.md#rq1_9d38f4959633)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 18, 'necessary_effect_absent': 18}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.983 秒，模型等待 37.212 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_source_scope_mismatch': 1, 'audit_effect_unbound': 1}。

最终报告 SHA `9618b2de10d5554a91e4db3f230a0e822276ef968c05885d2968a351cef8b369`，决定 SHA `6a30d91cead27438e4c8b06949ba9ae5370c34f8b09bb6bc89e7d4705b751671`。

## RQ1_3aae751c2593

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-19.md#rq1_3aae751c2593) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_346a05c1609d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_607d8722732b726a97e6`，根位置 848＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 848. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.059 秒，模型等待 36.036 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'missing_claim_or_source_anchor': 2}。

最终报告 SHA `04cea7609ebf81966f8224dfc988b28ad7a25f5d065efa3180b5fe09f5176f9e`，决定 SHA `bd1014afc2fc0a7bb77d121d1f470efd6dafca3ffd3f8b1fb4db8a537592a08f`。

## RQ1_e81e37a2f441

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_e81e37a2f441) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-72.json](Queries-72.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_1021888c1aed)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_caf9eb59c2a08e95892d`，根位置 729＋493，依据 `program_support`。At editRestrictedAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E14, E16, E2

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 45.720 秒，模型等待 31.741 秒，真实 solver 84 次，查询投影 91 项，动作记录含缓存 36 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `40553093a578c560e9f2ca6a874cfa9dd1951aac02911fce9d4d9f58902b9cb0`，决定 SHA `e1ad328ac12fe717a504fdb934f1f54d40a82483c3881fbf9435ad26054e3aeb`。

## RQ1_cbe5fd0f01d7

任务 FCR，评价类别 FCR-TRANSFER。当前未知，BG 未知。

[实际输入](InputSource-19.md#rq1_cbe5fd0f01d7) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-72.json](Queries-72.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_4a16f8a0e313)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'source_check_excluded': 1, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.073 秒，模型等待 64.664 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 18 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `10123ba767d43035f97b253a9159f8a1eb10963c865bfdf329225a611eb1dd39`，决定 SHA `7b1c2ebb8b2a6d1f5383d6d8b8534f7d221807bf715814bdda870611f7b9beff`。

## RQ1_a69a455c4a25

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_a69a455c4a25) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-32.md#rq1_adf28b957352)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.988 秒，模型等待 17.741 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `7aa22c4284ffa2a3782bd4cafb0db54a8024857c323055bdf78367e419c359c5`，决定 SHA `923c82cc1c91c882cc125ace4d02e08be300d37f58dd0b0bc30e9e904946c6bb`。

## RQ1_26d74b856242

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_26d74b856242) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-44.md#rq1_55d45a664e73)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 6, 'necessary_effect_absent': 1, 'source_task_reading': 1}。相关检查决定 {'source_check_excluded': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.691 秒，模型等待 74.667 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 8 项。诊断 {'unbound_or_inapplicable_seed': 4, 'invalid_semantic_row': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `a7818db81be63e88013c7d1887ea81d4c8703d56dbacd19410b1b46466742c30`，决定 SHA `bdd69a33e331bab2e190c2d3546487446b45f3a141714c2cc38aa069a5318bce`。

## RQ1_c3b57b743a5c

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_c3b57b743a5c) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-72.json](Queries-72.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-47.md#rq1_5e0671b41e23)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 8, 'no_effect_in_scope': 4, 'source_task_reading': 1}。相关检查决定 {'scope_missing': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.741 秒，模型等待 35.605 秒，真实 solver 6 次，查询投影 7 项，动作记录含缓存 7 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `770f4b03367ea57e88ccfcfcd085ec12c96c548792dc464d2bc1ba298dcdbc9a`，决定 SHA `2911a4414793a652269cb03de7f9c1d2b07d3040f86e2d71146c5803b0f7e389`。

## RQ1_dc06d7bad0d8

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-19.md#rq1_dc06d7bad0d8) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-72.json](Queries-72.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_9c365cb18f95)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 53.515 秒，模型等待 49.438 秒，真实 solver 8 次，查询投影 6 项，动作记录含缓存 56 项。诊断 {}。

最终报告 SHA `bcb5c34769bbfae5bdff5002c8d5af22eba9edf6b1efffc9875cde1aeade15e3`，决定 SHA `cda67d75d03ca2abaa6ba1a8077b4978e5ac6cd8d022fa056814641bd8bb504f`。

## RQ1_4a7b94cb63c5

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_4a7b94cb63c5) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-38.md#rq1_8503a353fe8b)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 25, 'necessary_effect_absent': 35, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.758 秒，模型等待 36.500 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `b75f241aaec1b8de6c360e2bf13dba4e73171d4e6ce968a2da5233961d481614`，决定 SHA `903303909cfed17a673cd355d6cbe39d7368b0467af4fea555b57f4d59744755`。

## RQ1_1844e5d3d18e

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_1844e5d3d18e) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_db73c28a69c2)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_652c090aebea6ae35a6e`，根位置 1013＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1013. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E2

发现 `finding_3dfca9f4e79eea2be7e3`，根位置 1013＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1013. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E3

发现 `finding_774f8810c226133a881b`，根位置 1013＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1013. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.007 秒，模型等待 42.184 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'audit_card_check_kind': 1, 'audit_source_scope_mismatch': 1}。

最终报告 SHA `40c7b14fe5ceea3791c04167a01cad04ba8af441604cb304f92d8af06b03c259`，决定 SHA `61d0d1b95303c14ea5e19ceeebf0ff47bc182f008877a41d327d21351ddfcfc0`。

## RQ1_493871f89451

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-19.md#rq1_493871f89451) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-72.json](Queries-72.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_5905f594ee2c)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_e6e95306a254646a2efa`，根位置 1289＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 1289 under other_source_meaning. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E10, E11, E9

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.102 秒，模型等待 88.777 秒，真实 solver 5 次，查询投影 4 项，动作记录含缓存 38 项。诊断 {'unbound_or_inapplicable_seed': 9, 'unknown_or_unshown_effect': 1, 'unrelated_or_secondary_graph_pairs_deferred': 4, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `f4251e94401da3b54c2a701e43078a10e340cffcea058783e9a4dd20a7382f2a`，决定 SHA `18fa4ac3644229ccb51e71af5301ce94accc4bbae53958e342b5a6e9b859e655`。
