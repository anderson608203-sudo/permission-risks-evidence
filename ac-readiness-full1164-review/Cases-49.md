# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_7fc3c35e6e71

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-20.md#rq1_7fc3c35e6e71) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-40.md#rq1_d758301b340c)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 20, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 21.902 秒，模型等待 19.925 秒，真实 solver 12 次，查询投影 12 项，动作记录含缓存 108 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 2, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `f7619bc49744666db9beff70a0710fd8251d1086b84e15dee573737502b72c01`，决定 SHA `8fa069906610f78696f11269a634bf2a4ba252cdd069729a83657be3f2a150c9`。

## RQ1_4fbf358e6693

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-20.md#rq1_4fbf358e6693) · 检查明细  · 查询明细  · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-40.md#rq1_1232b3f0f7ce)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 9, 'necessary_effect_absent': 6, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.077 秒，模型等待 32.771 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `7603513ee428cc3773dfc20bc6208a135cceb779d42f99b3e4a77c9bdd33c448`，决定 SHA `7769bf53486d422252c9c9a9a466a37c4b5951dac0d3a8aafbfb5af522ca5d77`。

## RQ1_9a61667124cf

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_9a61667124cf) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-43.md#rq1_6c3522e11e92)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_5cdb36b8233083086846`，根位置 2314＋476，依据 `program_support`。The change at zero_fee_transaction(address,address,uint256) affects the same holder request at destroy(address,uint256). The checked difference is an uncompensated reduction of existing rights under the applicable consent. 证据 E26, E42, E50

发现 `finding_29aa01e6c09296ba1c14`，根位置 2238＋31，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 2238. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E13

发现 `finding_909525133ed6c87a7d2f`，根位置 2238＋31，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 2238. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E17

发现 `finding_5c8db039c14c8afdfc46`，根位置 2238＋31，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 2238. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E11

发现 `finding_af215061f98ad2e4c2b0`，根位置 2314＋476，依据 `program_support`。The change at zero_fee_transaction(address,address,uint256) affects the same holder request at destroy(address,uint256). The checked difference is an uncompensated reduction of existing rights under the applicable consent. 证据 E22, E41, E49

发现 `finding_9d9568e0f5318c33be7f`，根位置 2314＋476，依据 `program_support`。The change at zero_fee_transaction(address,address,uint256) affects the same holder request at destroy(address,uint256). The checked difference is an uncompensated reduction of existing rights under the applicable consent. 证据 E32, E43, E8

发现 `finding_0183655798340caf8f2d`，根位置 2314＋476，依据 `program_support`。The change at zero_fee_transaction(address,address,uint256) affects the same holder request at destroy(address,uint256). The checked difference is an uncompensated reduction of existing rights under the applicable consent. 证据 E16, E38, E46

发现 `finding_3290737074fab943750f`，根位置 2238＋31，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 2238. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E19

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 15.191 秒，模型等待 20.753 秒，真实 solver 38 次，查询投影 64 项，动作记录含缓存 38 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `4d85ce0478b1661e054f57150f2ba563bbb299f0623cfbfabc388b0836503fa3`，决定 SHA `16ba35ee09c97e9a822399ad77e1bc66f9b10199637bb7a34a6656d4a13fda73`。

## RQ1_f814ab33ae2c

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-20.md#rq1_f814ab33ae2c) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-41.md#rq1_bba85280c610)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 26.507 秒，模型等待 47.378 秒，真实 solver 36 次，查询投影 42 项，动作记录含缓存 64 项。诊断 {'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `c54b7c855b0e16d64f45f2b44f33a34d23ae9edd2a3d86ea8b1964225468d14c`，决定 SHA `892f5fa861862104c2431cf9fec023ea44527f74434e36ba9af1cdd18a0a8520`。

## RQ1_1fbdcc5aa4c2

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_1fbdcc5aa4c2) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-46.md#rq1_29150828cc1d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_7c87a3c27d7617bcd427`，根位置 6859＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E13, E14, E5

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 98.186 秒，模型等待 60.488 秒，真实 solver 67 次，查询投影 79 项，动作记录含缓存 52 项。诊断 {'audit_source_scope_mismatch': 2, 'action_slice_exhausted': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `aa00a321b53c2d057af19282f655eb5e66200832c32eb4837a096eecac438249`，决定 SHA `ae224fb1ab3977a64946676d8cdcb7fdfb5d801efaa904a3b6fa2808506bdccd`。

## RQ1_2e7bb3ae70fe

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_2e7bb3ae70fe) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-45.md#rq1_e31cf8fce9a7)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_8542412ec6011ce73c95`，根位置 1101＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1101. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.810 秒，模型等待 36.367 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'explicit_effect_anchor_conflict': 2}。

最终报告 SHA `ef2b576b4c80fb3c37a9a240683755a95bda55453aa96ad78f06b45cb87538d6`，决定 SHA `e03131854f564fcaaba50ce200719c60a548d026568c7e3d0a133061e7cf5b5e`。

## RQ1_627eebfd65db

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-20.md#rq1_627eebfd65db) · 检查明细  · 查询明细  · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-32.md#rq1_2476ba262811)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 3, 'necessary_effect_absent': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 1.946 秒，模型等待 37.443 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `3e9574c732af33d1595d93a2679b3033c400fd72288056a58a4e41f3390f3055`，决定 SHA `b25b45cb9b8fd830e7bbc2518c781ac95d7bb83239972e3e82024953013aaceb`。

## RQ1_97f70f5113f4

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_97f70f5113f4) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-42.md#rq1_666ef53ce174)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_6514cc3621dd06713869`，根位置 1455＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1455. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.849 秒，模型等待 60.377 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'invalid_top_level_or_duplicate_key': 1, 'audit_source_scope_mismatch': 2, 'audit_effect_unbound': 1}。

最终报告 SHA `29126462cad55ae07f9e6d4094b1be65d971365278f6b5175893ad6c2bbd43f9`，决定 SHA `97384e037f126d6b041f07fe400c79326e972225f4f54ec3c2a4cb5060a93c08`。

## RQ1_c1af7a3f4924

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_c1af7a3f4924) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-31.md#rq1_8b866dac95bf)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_ecda060ad27d216daffa`，根位置 1046＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1046. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.469 秒，模型等待 50.467 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `56ed6f6f366d7ee897400f63f631c6d97ac827c369b0be07ec7ccfcc79294e54`，决定 SHA `c10a3173959d667daf27cc7bcdc8035785a52911842e3e1124248b03a70e2397`。

## RQ1_a8487b34a72c

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_a8487b34a72c) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细  · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-32.md#rq1_c2fb82269cd6)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_58ecb02ad84bfabf7721`，根位置 840＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 840. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.440 秒，模型等待 25.592 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'unbound_or_inapplicable_seed': 1, 'no_locatable_source': 1}。

最终报告 SHA `30477d3dd02ed577353ae313ecdc902a5cd1b234a3a110ed186eeac834d33b49`，决定 SHA `bd913de04589da17124251a3f8dbc0c530fa41427b514fcd8af2a28e719a75cd`。

## RQ1_8e4c324fa1c9

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-20.md#rq1_8e4c324fa1c9) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) [Queries-75.json](Queries-75.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-41.md#rq1_da692acb223b)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'covered_holder_grant': 2, 'scope_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 27.883 秒，模型等待 29.892 秒，真实 solver 80 次，查询投影 100 项，动作记录含缓存 94 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 4}。

最终报告 SHA `31e12fdbed4cbee63946bd7b088be8526faeead23f98b69eae0c50bdc8002783`，决定 SHA `f5c26eff73000b438300191b2b793dea4b39a45e76caaba0a0ae369a70fbea4b`。

## RQ1_c24c6c95ccbd

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_c24c6c95ccbd) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-75.json](Queries-75.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-44.md#rq1_32dbc2fa2433)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_b94f047ae07400aa6929`，根位置 1629＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1629. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.578 秒，模型等待 32.807 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'audit_source_scope_mismatch': 2}。

最终报告 SHA `2849e9af3dd06d364e7d2c250fd020eaa3e9e4551d4ca5fc1209c2e7d8ad4a74`，决定 SHA `48b51d45ea3c46884d5c5f45a0fe49d51b6ce61c9eff0b58d91805aec436fab9`。
