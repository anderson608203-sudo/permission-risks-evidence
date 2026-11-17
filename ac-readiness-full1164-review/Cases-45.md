# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_20dfd0c54b94

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_20dfd0c54b94) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-67.json](Queries-67.json) [Queries-68.json](Queries-68.json) [Queries-69.json](Queries-69.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-38.md#rq1_aaeb3f57cfd0)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_6edeb87d6a9bf9c32b34`，根位置 2421＋24，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2421. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. An already exempt agent may serve the same request if the holder granted the required allowance. 证据 E10, E18, E45, E46

发现 `finding_270b6e44062eafc7aa6e`，根位置 2421＋24，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2421. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. An already exempt agent may serve the same request if the holder granted the required allowance. 证据 E17, E32, E33, E6

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 886.585 秒，模型等待 55.319 秒，真实 solver 1764 次，查询投影 1274 项，动作记录含缓存 75 项。诊断 {'no_locatable_source': 1, 'action_slice_exhausted': 10, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'Unsupported:financial_value_continuation_identity': 2}。

最终报告 SHA `c5b167765c6e0dd00683b4300b14faf7b2b9af24df8473914adc2dcbd4a68863`，决定 SHA `8a66710c8dc7690ea65d162beb362de2b92e53d96525016dd63298dce8fe8898`。

## RQ1_d6bdc291eeef

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_d6bdc291eeef) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-69.json](Queries-69.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-35.md#rq1_09fe8189c73d)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 30.596 秒，模型等待 25.657 秒，真实 solver 23 次，查询投影 29 项，动作记录含缓存 19 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `5fd51af8844e4f4452f9c428d2e4d5cc679ba5f51013a30d6eeeea8997db139e`，决定 SHA `a81eb45a4a683ebbd616910c3dfb81a8b48cbb605754177b126a921fd3f6294b`。

## RQ1_ed58b7d7bfbb

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_ed58b7d7bfbb) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_185a84436c18)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 33, 'necessary_effect_absent': 15}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.604 秒，模型等待 26.262 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 58 项。诊断 {'Unsupported:source_semantics_unavailable:path_85b2849dece1deace263': 13}。

最终报告 SHA `edd29ed2408b5092fb18d1b3b1cd3f47f1eafff155e7cd660c50407536aa27da`，决定 SHA `9012f01a1f73b44b21a162780becd757c4a0e64e732587a3e93d6c5b2794cff4`。

## RQ1_d46f18d3b64e

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_d46f18d3b64e) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-69.json](Queries-69.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-27.md#rq1_328c13393c2c)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.642 秒，模型等待 27.028 秒，真实 solver 16 次，查询投影 16 项，动作记录含缓存 10 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `21a2511d78f64642b96733533a972afac07e226c3766b2fddb7f46b6db5fa733`，决定 SHA `c0b36a16361be7fe2adc150324ce7ddb3b49e8e72ee2d4866a1c0a2fd03434b2`。

## RQ1_8175a1b20602

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_8175a1b20602) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-69.json](Queries-69.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-28.md#rq1_21604460c189)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 21.483 秒，模型等待 44.811 秒，真实 solver 9 次，查询投影 9 项，动作记录含缓存 108 项。诊断 {}。

最终报告 SHA `48b08af4839a0939f71c3fd6a9843210305af4255a31559563a4a37b77253305`，决定 SHA `279597c28bfd62ff931d1137975080940a0b988b26aae6925d828c29a4d281f9`。

## RQ1_8ebdd1256aa7

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-18.md#rq1_8ebdd1256aa7) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-69.json](Queries-69.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_4e1e2a329c89)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_f2ce26b117f94cc09803`，根位置 740＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 740. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E8, E9

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.906 秒，模型等待 53.480 秒，真实 solver 10 次，查询投影 15 项，动作记录含缓存 25 项。诊断 {}。

最终报告 SHA `9423f60e1f7b6d3fd14622c5c8d7345d622265fa93b207c7a0da83513b70ac92`，决定 SHA `72a52b7141abc89dcb714646e69b7e4fae63ec7a6bf79c2cddd954203e2fcf7e`。

## RQ1_ad1b052af855

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_ad1b052af855) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-69.json](Queries-69.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-28.md#rq1_8b91a8024aa0)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 36.314 秒，模型等待 34.745 秒，真实 solver 15 次，查询投影 15 项，动作记录含缓存 150 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 3, 'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `a270d3d811f23e3e63fc5dc37877c83b88c53a20f7cdff08c330cc9b1f18ee34`，决定 SHA `da7e0348d6ed90220cb699749f63c0a94773792f121d26195e69d5ce833a30cd`。

## RQ1_a0facbcc1e38

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_a0facbcc1e38) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-69.json](Queries-69.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_86a0269d7608)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_df466433ddeafaabe2be`，根位置 13941＋501，依据 `program_support`。At mintToken(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E15, E16, E4, E63, E7, E72, E77, E81, E82, E84, E86, E87, E90, E91, E92, E93

发现 `finding_f0f73704368b7de5ef1d`，根位置 14448＋1972，依据 `program_support`。The change at terminateMinting() affects the same holder request at unlock(). The checked difference is a new positive entitlement for a controlled beneficiary. 证据 E100, E12, E23, E47, E56, E62, E65, E68, E74, E76

发现 `finding_6118da663ffae9d01bba`，根位置 12359＋860，依据 `program_support`。The change at withdrawLOOiX() affects the same holder request at mintToken(address,uint256). The checked difference is a new positive entitlement for a controlled beneficiary. 证据 E17, E3, E31, E46, E49, E52, E58, E61

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 114.247 秒，模型等待 35.489 秒，真实 solver 111 次，查询投影 108 项，动作记录含缓存 100 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `9bd66e3331135833ad305ac7c03682432bbbb9ffee4614b1cede9fdfd3c407cb`，决定 SHA `12ecbd4d1a2e406b9539ef416c26ea4bcfde169f32f101f9425ed0fcf21f727b`。

## RQ1_f1438202b0d6

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_f1438202b0d6) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-38.md#rq1_093a006d2f90)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.105 秒，模型等待 66.480 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'audit_source_scope_mismatch': 1}。

最终报告 SHA `b08e1bef0f4efd0be965af20cf411fbafe6295f819e4aed0df71f8336739c304`，决定 SHA `eec7ae80635e7330bd563b6b459ac8921becd70c6dcae1e826644638c129e5af`。

## RQ1_5d9b73e823c2

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-18.md#rq1_5d9b73e823c2) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-38.md#rq1_6d1be3618953)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_fd1c75e566d768cfca4a`，根位置 1038＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1038. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E2

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.276 秒，模型等待 41.337 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `e3370e6332a36896f1a45b193f56f52a6f57deef726c86b1b56a428cdd84cd83`，决定 SHA `4326222191a2ef88558d6b1159d1cc0ed2999728746a5efdc74fde02df294984`。

## RQ1_776a6b98d18f

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_776a6b98d18f) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-44.md#rq1_8456d2957fff)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'no_privileged_intervention': 1, 'necessary_effect_absent': 1}。相关检查决定 {'source_check_excluded': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.078 秒，模型等待 52.929 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'missing_claim_or_source_anchor': 1, 'explicit_effect_anchor_conflict': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `9619887fb0d980918701dc13cd41c607a383fc097b47ac35d1aa08b1a22ed8c9`，决定 SHA `3d44d11b1cd1ad68aac734a6bc555e8bdbbd51b6a73bae76685d1d6b5cc4db04`。

## RQ1_1b9c7ecc28f8

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_1b9c7ecc28f8) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-36.md#rq1_01a30be11868)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 5, 'necessary_effect_absent': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.354 秒，模型等待 42.248 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `0a04ca64248f5ffa3605e21ab823e8bb28e83acb8df06bc1c3a0c98fdaad19e1`，决定 SHA `707fbb1ab694fda4aa9334d83203d508a977965819e957e7463e9e3871d2af3b`。

## RQ1_9b3403bc5e3b

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-18.md#rq1_9b3403bc5e3b) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-36.md#rq1_18b83e12ea1f)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 7}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.872 秒，模型等待 31.423 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'explicit_effect_anchor_conflict': 2}。

最终报告 SHA `2e4373f30867d339eba9bcbedb9bb3e9924c987e08b0dc787d6c9d909c346abe`，决定 SHA `3f74bce452da83809f8a27d475703ca38a53daeefe058da15c10c54931a232d0`。

## RQ1_905fe6a15d0b

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-18.md#rq1_905fe6a15d0b) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_d254caa47e26)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 36, 'necessary_effect_absent': 27, 'detached_local_holder_switch': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.103 秒，模型等待 40.010 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'explicit_effect_anchor_conflict': 1}。

最终报告 SHA `8abca4b2dd86591260419656ca642abe86417a8c4bff1531598b679f5221a224`，决定 SHA `15e92a80385117ec54f30fb0088da2f97fdd5e127d6ae5a5af6eed01cac2b261`。

## RQ1_81780fe65981

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_81780fe65981) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-69.json](Queries-69.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-48.md#rq1_9809e3aa83b0)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_13004eff0741ea38a038`，根位置 8945＋345，依据 `program_support`。At setTransferAgent(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E10, E20, E21

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 42.545 秒，模型等待 34.213 秒，真实 solver 92 次，查询投影 102 项，动作记录含缓存 63 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 6}。

最终报告 SHA `a4384a0ba46a97dc1ec36951f9415b4ada3fa7613ce0618bf67bcb80a18da831`，决定 SHA `8969a5584b7b4963b66fceb1335587c7238101f5d180545b8da1cfc3013e378e`。

## RQ1_11ec4918a871

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_11ec4918a871) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_b2aa8ebfc6c8)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 7, 'no_privileged_intervention': 5}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.276 秒，模型等待 20.896 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'missing_claim_or_source_anchor': 1, 'no_locatable_source': 1}。

最终报告 SHA `c79e9757e364d3304f1dfeea1481bdc94b97f5c1e8e726d37738832596c15ec5`，决定 SHA `211e1e6f83cd7975ec55e6f5617a0bcd21018f3103e22bd602ec4c8aa3d8e607`。

## RQ1_0ce2d4c45f17

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_0ce2d4c45f17) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-40.md#rq1_e390407a4c29)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 6, 'no_effect_in_scope': 6}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.015 秒，模型等待 49.143 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 31 项。诊断 {'audit_effect_unbound': 2, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `3ffe29460dddac67111c83c6d731d8ea64066d48b3b634cd7746b8de41fc5355`，决定 SHA `a54e93ea6e10ae2b42b2a331dd952946d436e52447238fbce10b88dcc7bdbd03`。

## RQ1_e31cf8fce9a7

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_e31cf8fce9a7) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-49.md#rq1_2e7bb3ae70fe)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 9, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.418 秒，模型等待 26.874 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'explicit_effect_anchor_conflict': 1}。

最终报告 SHA `62ac1ca1df334f7c97c80363d21b18bdeb961b0a2e46066194c9487dd2be66d9`，决定 SHA `8755b3d221add041a913a74dd107f7ef017e51be7b91c9193eed6ef665ec9523`。

## RQ1_121bde35ec7a

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_121bde35ec7a) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-69.json](Queries-69.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_1dc640c1a56b)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_2e28be5982d70d5e0775`，根位置 1613＋24，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 1613. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E10, E6, E7

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.015 秒，模型等待 18.102 秒，真实 solver 11 次，查询投影 14 项，动作记录含缓存 14 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `ad6b93983247cb73d747f5e7b4d7460cbd35ab9a6f2908351e88016c8559a4dc`，决定 SHA `1330413666f47a504d1aa4de640bdc390a36a4f60d54d53d88a7bbc23f940cea`。

## RQ1_353a9b0b5006

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-19.md#rq1_353a9b0b5006) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-69.json](Queries-69.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-38.md#rq1_db11e3e08742)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'holder_consent_basis_unresolved': 3}。相关检查决定 {'scope_missing': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 901.058 秒，模型等待 29.257 秒，真实 solver 189 次，查询投影 143 项，动作记录含缓存 32 项。诊断 {'missing_claim_or_source_anchor': 1, 'action_slice_exhausted': 14, 'yield_to_source_bound_semantic_review': 1, 'program_investigation_budget_exhausted': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `70130673346ceebe7e33c601e5c8bc67e06fa0fb3f75e06ea2d61b2d97b2001e`，决定 SHA `13f00858d507ad24780fe997dbabd75898a1a4baef8706e61b148c2c0a532123`。

## RQ1_8bbb0c4ed7cf

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_8bbb0c4ed7cf) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-69.json](Queries-69.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-38.md#rq1_152053986776)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_f40ff2efffeb7aa15b9f`，根位置 1400＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1400. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E4, E5, E6

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.656 秒，模型等待 36.621 秒，真实 solver 14 次，查询投影 12 项，动作记录含缓存 10 项。诊断 {'audit_check_target_unbound': 2}。

最终报告 SHA `7af87a484eea061d92b02c4e6d3d81541daa32abddff23980a0a4760a0fdb9de`，决定 SHA `e3171e94274bf6e88ba87d43ded1886e719e929ae0ac07e6931ede0ba61424c7`。

## RQ1_cd25b92c3711

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_cd25b92c3711) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-69.json](Queries-69.json) [Queries-70.json](Queries-70.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-38.md#rq1_ab687024c0d2)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_799301e592b42a9ba20b`，根位置 6348＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6348. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 100.055 秒，模型等待 46.104 秒，真实 solver 67 次，查询投影 79 项，动作记录含缓存 52 项。诊断 {'audit_source_scope_mismatch': 2, 'action_slice_exhausted': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `e642116c1e9b9296f67d863273b63c8b9563ff0274f19eba42f50770aec9c36d`，决定 SHA `48cadb3507eec827d0cdaff94c189e44ff2e076ed314d78778b82b9584279a97`。

## RQ1_35646ded2a70

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-19.md#rq1_35646ded2a70) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细 [Queries-70.json](Queries-70.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_f1bb587376e8)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 4, 'necessary_effect_absent': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.344 秒，模型等待 37.851 秒，真实 solver 4 次，查询投影 4 项，动作记录含缓存 5 项。诊断 {}。

最终报告 SHA `52defb6b01e61b8b2121ec501285aec78e49d5e991b4ba183a363f9faa0323eb`，决定 SHA `b9e8895afeef6359879fe82bdba0f3e4416b1c0edaca638b53a7126afdcc5145`。

## RQ1_271b133fa427

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_271b133fa427) · 检查明细 [Checks-87.json](Checks-87.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-40.md#rq1_9f787793ef28)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_085b89b48a0edc09a365`，根位置 773＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 773. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.181 秒，模型等待 32.120 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `8f28f7357cdc7094555583233dc7a36d666b9a3309bc86adb239b6958cf5b2aa`，决定 SHA `59274b11d3fdb821da44dc514512b5dbba57433aaf05a9a48841aa8a75e6f95f`。
