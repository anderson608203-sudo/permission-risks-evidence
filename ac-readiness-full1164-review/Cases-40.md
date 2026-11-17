# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_05a542de9e26

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_05a542de9e26) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-31.md#rq1_eb71e4b3e05f)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'no_privileged_intervention': 1, 'necessary_effect_absent': 1}。相关检查决定 {'source_check_excluded': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.265 秒，模型等待 44.623 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `223c28f84dacd637610da203e1258b4ec981c3732ae759d47eab579dba113f81`，决定 SHA `5c3a752ab50696415e44fc38974f8e78d7838b457aea18be2ab06a50dabae39c`。

## RQ1_7255c4e988cf

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_7255c4e988cf) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-62.json](Queries-62.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_bd99c12747fd)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_42ea42abad2e1094cdf6`，根位置 6863＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E13, E5

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 38.926 秒，模型等待 19.870 秒，真实 solver 59 次，查询投影 71 项，动作记录含缓存 51 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `da7384d3de270546614dc8eae304c6453b52d93c8a55c6349edef8764ffb9bf6`，决定 SHA `c3594995eef0071741e8966d84cfd1e003babd790cc3cc399fa17b845eeae7fd`。

## RQ1_a2b01dab39e2

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_a2b01dab39e2) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-62.json](Queries-62.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-35.md#rq1_21bd6c31d928)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_09f0caeeacb7fefcd7e3`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E22, E39, E41

发现 `finding_b41c85e303ddad22c4b1`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E21, E34, E36

发现 `finding_0281d7b343cff3435822`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E16, E30, E33

发现 `finding_20ffe9ccb2845681e504`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E19, E37, E38

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 27.841 秒，模型等待 32.583 秒，真实 solver 117 次，查询投影 114 项，动作记录含缓存 63 项。诊断 {'explicit_effect_anchor_conflict': 4, 'unrelated_or_secondary_graph_pairs_deferred': 10}。

最终报告 SHA `5d1caeeca2a3c2030b375f9b94fe3fbd9d352df070257645ebc584a81b1f71cb`，决定 SHA `f8d89eb9aed78900a73869204fdb0adb386c01a4a425d922fdb57037986f1d6a`。

## RQ1_fccd9a0f9abd

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_fccd9a0f9abd) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-62.json](Queries-62.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_ede25a30c4e4)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_313a51f0820509b0cba8`，根位置 1195＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1195. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E2, E3, E5

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.654 秒，模型等待 43.432 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 5 项。诊断 {'audit_card_text': 2, 'audit_source_scope_mismatch': 1}。

最终报告 SHA `f8b9705172eb11d7e85ba691d9bceb05450afc2d766c2312e7512e123e1e46df`，决定 SHA `8668a59922dbf86143851b0ebc2117e400515a99e53d36d20c598904616c380d`。

## RQ1_389d8dfc83d5

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_389d8dfc83d5) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-62.json](Queries-62.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-48.md#rq1_fa882017777c)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_d70a56d56fc9fe643e67`，根位置 779＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 779. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E5

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.471 秒，模型等待 38.095 秒，真实 solver 7 次，查询投影 6 项，动作记录含缓存 10 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 3, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `79eb762061c04a64366cae60fc376a2806af45310adff343704b614b98aad183`，决定 SHA `6c473e18f906cf297ba654a34ce614776c0867adb9911dc3d5d4d1ac01aaa7cd`。

## RQ1_46a031a993c1

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_46a031a993c1) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-34.md#rq1_985c6fd1d4e4)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 7, 'necessary_effect_absent': 1, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.441 秒，模型等待 31.913 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_effect_unbound': 1, 'unknown_or_unshown_effect': 1}。

最终报告 SHA `b1f030d7dc2254ebdaba8e61d677907406519de2b76e31c66982aa680defaf9d`，决定 SHA `ce2085c4122a7c4863ba014213d68545d88d28c96aafa48f305f582cd7c09525`。

## RQ1_cbb6e67b8b81

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_cbb6e67b8b81) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-62.json](Queries-62.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-46.md#rq1_c315645e4627)。指定类风险端报警、修复端报警，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_fedb5d7a2d74b4cfd402`，根位置 5091＋361，依据 `program_support`。The change at setTokenExchangeRate(uint256) affects the same holder request at fallback(). The checked difference is a new positive entitlement for a controlled beneficiary. 证据 E1, E10, E13, E14, E15, E18

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.161 秒，模型等待 20.134 秒，真实 solver 22 次，查询投影 17 项，动作记录含缓存 16 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `41f01d780b5ac7d266b46a1e2b4be83ab5d30c4e0faa6584e68e20e2ad9e21ae`，决定 SHA `6c374abc53fa4f18dc31df09972cb6f8e4ddca969a34ef1eb47146f986855975`。

## RQ1_c6f96b65d39b

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_c6f96b65d39b) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_6b70a408ccf8)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 30, 'no_effect_in_scope': 18}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.188 秒，模型等待 41.814 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_card_text': 1, 'audit_card_issue_kind': 1}。

最终报告 SHA `42d0055e9e4511d9396eba00fad62c283763469e3aaee96c61327e5309306aa1`，决定 SHA `3a3cd98a34ae3a06fde71450655feaf03fe55be78a305dd1f00827fb533e5842`。

## RQ1_35e0e8d95f92

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_35e0e8d95f92) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-62.json](Queries-62.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-40.md#rq1_c75d73e1c482)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 30.684 秒，模型等待 56.187 秒，真实 solver 23 次，查询投影 29 项，动作记录含缓存 27 项。诊断 {'core_unresolved_retained_for_investigation': 2, 'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `1a62629d21e9a6bf8f9f009274a88aa3e435a02178298e78ad88cdea70b84a0d`，决定 SHA `92ea998083cd06df9633186e1c1539743bb80620340c7ab8686089e37e47029d`。

## RQ1_dd2a94075ff4

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_dd2a94075ff4) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-62.json](Queries-62.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-46.md#rq1_6292cc10d171)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_7f444b829f9f4da46fd5`，根位置 4974＋422，依据 `program_support`。At mintTokens(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E10, E20, E51, E52, E53

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.249 秒，模型等待 18.442 秒，真实 solver 35 次，查询投影 34 项，动作记录含缓存 47 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `4687271ea7e87010cbc81c2810c95f17cfb3606a45ad19dc8603d9321a78949f`，决定 SHA `601734fe971a0b0ad69c46404d723bd535b4965f9fcbc27706f692d9cd96b767`。

## RQ1_e390407a4c29

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_e390407a4c29) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_0ce2d4c45f17)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 1}。相关检查决定 {'scope_missing': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.346 秒，模型等待 31.483 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 13 项。诊断 {}。

最终报告 SHA `aaa7a73ef2202668fc6afca791124946b134a49b7e03523e11abbd2f7fcb99cf`，决定 SHA `908d4ec0578f93f24693b25065ac9bf53938080b265eb9a13352a85d9723d2a0`。

## RQ1_81162a271264

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_81162a271264) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-42.md#rq1_cb7efb519f69)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 3, 'no_privileged_intervention': 1}。相关检查决定 {'source_check_excluded': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.169 秒，模型等待 23.206 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'unbound_or_inapplicable_seed': 1, 'no_locatable_source': 1}。

最终报告 SHA `c8ad9d103f15d8ca667a90240405553283156723c630211d4785ea44df0479ad`，决定 SHA `ed04b669e3396a6099b589f3fab900ecd40b7a78f385932e1b8a31b2e23509d3`。

## RQ1_89bac12a4446

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_89bac12a4446) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-27.md#rq1_405dd133e380)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_686e2c465348d2e5fc09`，根位置 3649＋26，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 3649 under financial_right. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E13

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.085 秒，模型等待 43.791 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 28 项。诊断 {'unbound_or_inapplicable_seed': 1}。

最终报告 SHA `96dfed25e00fa7bf58b8ec83886276342efed0e2b22fc834eec84787dd4a99cf`，决定 SHA `7c48b981dd38374fa59ae8d595b8989ee601c9d3c895c973eff2fb469d373dfb`。

## RQ1_c75d73e1c482

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_c75d73e1c482) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-62.json](Queries-62.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-40.md#rq1_35e0e8d95f92)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_d6a37f96a2b9e5a9a6e0`，根位置 6437＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6437. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E3

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 50.034 秒，模型等待 39.691 秒，真实 solver 65 次，查询投影 77 项，动作记录含缓存 66 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `11a326a401eea83c12f5578958a57c728ec21279ef2f3c7745c97327d3fd3afd`，决定 SHA `5083b1ada4069c2f71467725db9c73a14c83daf5b4847cc24970e69698d30c99`。

## RQ1_615f9f99c585

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 未知。

[实际输入](InputSource-17.md#rq1_615f9f99c585) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-62.json](Queries-62.json) [Queries-63.json](Queries-63.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-33.md#rq1_3db9d6846001)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_af328e0b4a76cdb48bc4`，根位置 2417＋25，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2417. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E13, E14, E39, E40

发现 `finding_9cf6ab1d5cf4144fbc32`，根位置 2417＋25，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2417. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E18, E33, E55, E56

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 916.786 秒，模型等待 54.936 秒，真实 solver 739 次，查询投影 662 项，动作记录含缓存 39 项。诊断 {'audit_card_text': 1, 'action_slice_exhausted': 11, 'program_investigation_seconds': 2, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `fb3b18f36a1dd149f237c27af06e2f1d46c62061c4410dabe22fb75414278ae2`，决定 SHA `fb3ec938c9189eacef9f75ad11b369763dece4e7fda767e43c2380a733f74410`。

## RQ1_903bc514300f

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_903bc514300f) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-34.md#rq1_b5ec0e7b3101)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 15, 'necessary_effect_absent': 10, 'detached_local_holder_switch': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.816 秒，模型等待 27.771 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_card_text': 1}。

最终报告 SHA `e948f7f1344eb4f951b6e972aea20f46ef64509527b7a24b6f9d820c17e3e3f8`，决定 SHA `211e5a461deee1db55535692ec17d356127deb91cceba3411288b9f2a5ead8fc`。

## RQ1_101079fc6aa8

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_101079fc6aa8) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_32e1e7ce1240)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 33, 'necessary_effect_absent': 11}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.994 秒，模型等待 31.918 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'explicit_effect_anchor_conflict': 1, 'unknown_or_unshown_effect': 1}。

最终报告 SHA `8f606384cdfc7928fa9892f878ded00a79d91a639a820a31d57a6e108daa143a`，决定 SHA `b8a0587b7c7e9509c47251193c258eedc896b90d772a8235eb6fd65a61d81d8c`。

## RQ1_532d0e522c88

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_532d0e522c88) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-63.json](Queries-63.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_3dcd11c8e603)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 17, 'no_effect_in_scope': 17}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 18.954 秒，模型等待 54.244 秒，真实 solver 23 次，查询投影 29 项，动作记录含缓存 19 项。诊断 {'unbound_or_inapplicable_seed': 2, 'no_locatable_source': 2}。

最终报告 SHA `f8234d0e60cdb3460b5d66f250969ae40a3f48cb2ea2ab78f86d8afdb023d184`，决定 SHA `a3b3f3b68f7880b5c88a0ad2e5cc73206e5a216bc8055c41ba99577cb0906113`。

## RQ1_9f787793ef28

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_9f787793ef28) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-45.md#rq1_271b133fa427)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 1, 'source_task_reading': 1, 'no_effect_in_scope': 2}。相关检查决定 {'core_mismatch': 1, 'source_check_excluded': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.267 秒，模型等待 50.083 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `795e7d63786fafa4b046120c031fe66dc98e3684afd380542e289232b7450b14`，决定 SHA `97fd67d2439a768322068f1a2d4811373374a72fc68d2d0ccc4344eb837f1351`。

## RQ1_3f95723b36dc

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_3f95723b36dc) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-63.json](Queries-63.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_a763d3b1358b)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_d6a74fa67a5c18ddead7`，根位置 836＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 836. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E10, E2, E3, E6, E7, E8

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.277 秒，模型等待 39.848 秒，真实 solver 14 次，查询投影 12 项，动作记录含缓存 10 项。诊断 {}。

最终报告 SHA `785f0a80cce10289af85851747a3bc3164830f37db48dd1f394582cb48534d8b`，决定 SHA `23fbf493fee822e2d545776a521e6a37075523dcf9b824af49129201f4623060`。

## RQ1_d758301b340c

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_d758301b340c) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-63.json](Queries-63.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-49.md#rq1_7fc3c35e6e71)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_a90779146e603b382abc`，根位置 6607＋223，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E13, E5

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 38.702 秒，模型等待 51.238 秒，真实 solver 58 次，查询投影 71 项，动作记录含缓存 51 项。诊断 {'audit_source_scope_mismatch': 2, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `ced9ad620abf61a8c5810f337a70ab9d8918f8531e529d64d0a5d6c7d2d6a5f0`，决定 SHA `e0091bc666a976997d088dc83e6c05e1b16219314740ed8f69ad34810f547bad`。

## RQ1_475c7d9ec738

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_475c7d9ec738) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-44.md#rq1_b84042e6eefd)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 3, 'no_effect_in_scope': 3}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.263 秒，模型等待 36.985 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 6 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `b23831f8f4ebeb0d9076c05015f0f9ef696446a5ce733399cbb50bbfb28f8dcb`，决定 SHA `eba6f67eb8761c0e6127c938cd12bc702e0dc39da853e19598ec59c6640f3623`。

## RQ1_1232b3f0f7ce

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_1232b3f0f7ce) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-63.json](Queries-63.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-49.md#rq1_4fbf358e6693)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_875c8c05d644cabecd9c`，根位置 2933＋31，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 2933. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E10, E12, E2, E3, E4, E5, E6

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.335 秒，模型等待 25.690 秒，真实 solver 9 次，查询投影 9 项，动作记录含缓存 8 项。诊断 {}。

最终报告 SHA `22852f41441c24e3e00f057150fdc5533981a2fa48eb43cd5f3b85c647bb9697`，决定 SHA `1561207e2935abbe9d24b45613c6dca14ce361dda1d462cfd401e9312ddfb5c3`。

## RQ1_7ac0cdbee968

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_7ac0cdbee968) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-36.md#rq1_4096ba758662)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 36, 'necessary_effect_absent': 27, 'detached_local_holder_switch': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.038 秒，模型等待 49.024 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_source_scope_mismatch': 1}。

最终报告 SHA `4035403b5dc7273c149e43316989ad8303195e5d8b1831238d533e2fdb771c8e`，决定 SHA `3c99956ab0d71776267b2ab4de5a15213d9f334bd65c44c1a60e37a915a3e614`。
