# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_a294f9ad1c29

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_a294f9ad1c29) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-41.md#rq1_f138415fcb0f)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 3, 'necessary_effect_absent': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.340 秒，模型等待 43.055 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {}。

最终报告 SHA `9af371463605cad4289a0b5ddb04b43bf9d637e5c81b44b6fd59c5f26f50ec75`，决定 SHA `6884badc40c4917b8504809cdf55faa88d58745b7715b8f78d32b601354b0261`。

## RQ1_7dc3f131a856

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_7dc3f131a856) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-34.md#rq1_166770d81e59)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.850 秒，模型等待 23.491 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `1a727b08d49bcac1b39839040741211af388d4a8ff7b2cf5c57c7bb9fff6b603`，决定 SHA `d50eb257d1459ba59348dac02c0804d72f41c10b3b62997d5bf13aa4f5287b59`。

## RQ1_acc2efe42317

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_acc2efe42317) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-33.md#rq1_ed2f6363ada8)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_edca5cbce8113e79cce5`，根位置 1044＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1044. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E10, E12, E14, E15, E17, E19, E21

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.868 秒，模型等待 83.031 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 35 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `67f8517c5fd843b66c1b0a1f83cf6a348e08ca67a998cb19a3e76ed1a8ae479b`，决定 SHA `fb5b12e29dcf99518a5fd4de97b46e1b5bf9c5fe74113af9acb78299a1fc6f9d`。

## RQ1_6ca2b0aeda43

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-13.md#rq1_6ca2b0aeda43) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-32.md#rq1_33d48945207e)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.571 秒，模型等待 39.333 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'audit_source_scope_mismatch': 3}。

最终报告 SHA `fa5c6845299ea03239e70135dabce4c3ae070a0427999369296bd682d833cc51`，决定 SHA `0ce2b300bd272f5b56174988dcfd934cbda2c0a4f05b027b09f27efcc060bf9b`。

## RQ1_b586561de97d

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_b586561de97d) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-44.json](Queries-44.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-35.md#rq1_c339d6f50fb1)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_9adcd1fc8bda9c8d3a5e`，根位置 944＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 944. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E4, E5

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.043 秒，模型等待 48.837 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 14 项。诊断 {'audit_effect_unbound': 1}。

最终报告 SHA `9734ee37715b224b4b08710e58b39aa5db8e455b9ab8a310e58dfb94cbf3f6b1`，决定 SHA `277bfa140e46076d7c2f25781b02e67324d5776f920d9b3b74f394af1f7e785f`。

## RQ1_cfd05c2b5a6b

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_cfd05c2b5a6b) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-44.json](Queries-44.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-29.md#rq1_35517bec1c74)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_2cb90103939d610f23f2`，根位置 6570＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6570. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.859 秒，模型等待 42.408 秒，真实 solver 14 次，查询投影 22 项，动作记录含缓存 15 项。诊断 {'unbound_or_inapplicable_seed': 2, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `a53fed804ac0e9ec84271d00a60d4dd3ba62604aa538a21b4febc884610e573c`，决定 SHA `9343ba2499aa0d70d5553926f29788ef2976d04d02723e09fe15bad439d95c95`。

## RQ1_5ab05cf437b3

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-13.md#rq1_5ab05cf437b3) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-44.json](Queries-44.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-42.md#rq1_c46de9c5394e)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2, 'scope_missing': 1}。相关检查决定 {'scope_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 25.241 秒，模型等待 43.184 秒，真实 solver 41 次，查询投影 37 项，动作记录含缓存 41 项。诊断 {'audit_source_scope_mismatch': 1, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 6}。

最终报告 SHA `6f3185705f8cba6dad47697a0b3200de30ca7cc1cacbe62c28477743ddc24e70`，决定 SHA `9d0e8bb4e6667e61134aa3628c0461afd7a8c44c899ddf6780992e8f0141ea11`。

## RQ1_24939507ecba

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_24939507ecba) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-44.json](Queries-44.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-27.md#rq1_dc9919de5e46)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_29f407b0fc01a924d4b0`，根位置 959＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 959 under management_role. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E2, E3, E4

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.494 秒，模型等待 17.420 秒，真实 solver 7 次，查询投影 5 项，动作记录含缓存 5 项。诊断 {'unbound_or_inapplicable_seed': 1, 'invalid_semantic_row': 1, 'no_locatable_source': 1}。

最终报告 SHA `910711ec24545ad1395377ce4ab48b6f94182013f1e5e4a110d938237827bcbb`，决定 SHA `26fec94575bce89a0446647e0d28ce40e1590416097dc9883b1083bec597af6f`。

## RQ1_abfded104a6c

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_abfded104a6c) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-44.json](Queries-44.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_14951f909aa5)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_4af25b3d87779b4c8827`，根位置 6601＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6601 under financial_right. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E1

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 86.579 秒，模型等待 63.404 秒，真实 solver 70 次，查询投影 82 项，动作记录含缓存 93 项。诊断 {'audit_source_scope_mismatch': 1, 'action_slice_exhausted': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `1ee579a195fa68eb852b973439f90caeadedc161a2bf7198837d8888b8b47841`，决定 SHA `cc575074cf69b41289df5369bac03b9448c3a0814897d1d906b9c0fb0a8d11f7`。

## RQ1_cae50a0089d5

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_cae50a0089d5) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-48.md#rq1_b7fd0e26135f)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 15, 'necessary_effect_absent': 15, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.122 秒，模型等待 38.240 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'missing_claim_or_source_anchor': 3}。

最终报告 SHA `d95613db33b7d240061a0c288c4e5c3bc21d2e7bd1d777b7d9ecf96c94ed10ec`，决定 SHA `39807095fab4160da09d04869b518814652d76daf90aac4894b789d0eca3b96e`。

## RQ1_eb71e4b3e05f

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-13.md#rq1_eb71e4b3e05f) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-40.md#rq1_05a542de9e26)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_696e7a7c5dad70c534d8`，根位置 824＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 824. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1, E2, E3

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.154 秒，模型等待 33.339 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'audit_source_scope_mismatch': 1}。

最终报告 SHA `3f015de38fca9faa74205c4e2913954ba49a85eebdaabcd2e09d599dfa51f283`，决定 SHA `6693b09be49e89acaca1990b038ab6b0d74a3e5957a1dbb8121d39c346a306a3`。

## RQ1_d3547c6cc861

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_d3547c6cc861) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-44.json](Queries-44.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_ca5c64d59fe1)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_ee4bf0323aafe2b2cd68`，根位置 1094＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1094. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.718 秒，模型等待 38.414 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'audit_card_text': 1, 'audit_source_scope_mismatch': 1}。

最终报告 SHA `c8b603d237084fcd929b0c1df1afefe68bc7070e1c52ad15d950b0ef7c517c1e`，决定 SHA `96f413ed06135518ff2c68ee61ad251a19f36ad14e5d445c84d9e6134ed77106`。

## RQ1_e48a6c07fe05

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_e48a6c07fe05) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-42.md#rq1_613d6352416c)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'necessary_effect_absent': 3}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.370 秒，模型等待 62.620 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 7 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `ad989013ef6fe83666759a5ebab5ac11d751c19a0bdc068581c01d46ac251b3e`，决定 SHA `3e16b38a065ec7a08a00743822b247ea1be35554ff837e1a9abe66602c5aa7f7`。

## RQ1_c9626779c857

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_c9626779c857) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-44.json](Queries-44.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-35.md#rq1_085aaca2f412)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_46b391a596282fa347d0`，根位置 3797＋420，依据 `program_support`。At burnFrom(address,uint256), a privileged effect leaves another holder with fewer rights in the same unit after attributed transfers and applicable settlement. 证据 E1, E12, E13, E14, E18, E19, E20, E4, E5

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.435 秒，模型等待 42.401 秒，真实 solver 6 次，查询投影 17 项，动作记录含缓存 16 项。诊断 {'missing_claim_or_source_anchor': 4}。

最终报告 SHA `abb5e2039564fb93d60f22d14d217ad6fee8974e351e1758dfd06ec01be9f2c5`，决定 SHA `6b661776f79db688023d24b311faf942ffffa8cae1f57b7f65e337188680a2c0`。

## RQ1_8b866dac95bf

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_8b866dac95bf) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-49.md#rq1_c1af7a3f4924)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 5, 'no_effect_in_scope': 5}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.128 秒，模型等待 56.023 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_effect_unbound': 1, 'no_locatable_source': 5}。

最终报告 SHA `1b74dfa3698f55077fd1d3d93bdb9818c9811ff4efcf8b128bcb33e5e6363995`，决定 SHA `d218b2f1e9d5fbf4b6c813064d095eae9091398c8340dce1b3293215ce1a7d58`。

## RQ1_4feeb0c21e60

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_4feeb0c21e60) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_0e202076b336)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_048cd6ed05c2cc120c97`，根位置 749＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 749. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E4

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.413 秒，模型等待 40.186 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `b950a8bf96fee5590c9f264d4c760c353a2361c7608ab37da7baaec211b419b8`，决定 SHA `05c54ff04a6be49b71f8d0cc33e26b75b3491d5b17daeb52c179ae706c90659c`。

## RQ1_1505712f3e55

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_1505712f3e55) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-44.json](Queries-44.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-33.md#rq1_cd03bb96c000)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 4, 'necessary_effect_absent': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.331 秒，模型等待 22.068 秒，真实 solver 2 次，查询投影 3 项，动作记录含缓存 2 项。诊断 {}。

最终报告 SHA `7a09a7076cd25863e4d3b88c0dc279a27d66d86194af12013688aea8b05d87d8`，决定 SHA `40ee25b11927c21ee57d35bf1c22d1a4e7e72f95f2e68a36a5f2a4eaa896492c`。

## RQ1_f0010e656b81

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_f0010e656b81) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-48.md#rq1_c4e8c693f07b)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'necessary_effect_absent': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.002 秒，模型等待 29.224 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `570dd447a90a3d4854194ce8a479dfd79b3a0f8f2f00d984fb3361e908db2d15`，决定 SHA `548aa2533ef282b41576ccb49d11832b1a9ec5804b3192e6355beb0d3f813ce9`。

## RQ1_816348240738

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_816348240738) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-44.json](Queries-44.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-28.md#rq1_2b63785028d0)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_7553aafe76936b5a02bb`，根位置 6642＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E13, E14, E5

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 112.036 秒，模型等待 39.865 秒，真实 solver 68 次，查询投影 79 项，动作记录含缓存 52 项。诊断 {'audit_source_scope_mismatch': 3, 'action_slice_exhausted': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `1aad0e54e88d282d100a6f259b9c76151c78c1c74dc6380e032ec1d1ce613525`，决定 SHA `ef80472b4db4e2a01bb9b4978c0af5c75f554c44b8ef2bf8c251eabf4ce5aae5`。

## RQ1_b80eb72fb713

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_b80eb72fb713) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-44.json](Queries-44.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-42.md#rq1_3b7737691ba6)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_c2618ab83c84644d3cc0`，根位置 930＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 930 under management_role. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E3, E6, E7

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.946 秒，模型等待 30.539 秒，真实 solver 13 次，查询投影 11 项，动作记录含缓存 12 项。诊断 {'unbound_or_inapplicable_seed': 2, 'audit_card_text': 1}。

最终报告 SHA `106afb914859e643fb06c3314445ae25a18682688b4357c8b1d15f28ec7afacb`，决定 SHA `1b5e467c9407a265e4cd1aad0dfc62c1ee5ecf1af9b6a8ac6039b536cee9c6be`。

## RQ1_461e1f6a078f

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_461e1f6a078f) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-45.json](Queries-45.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-43.md#rq1_d66edd91f212)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_e3f77703b9610444ae98`，根位置 3146＋27，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 3146. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E11, E12, E2, E21, E22, E23, E3, E4, E5, E6, E8

发现 `finding_b70ec90e81dfd0e8595c`，根位置 3146＋27，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 3146. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E24, E35, E46, E48

发现 `finding_d54caf4caabee47a7b83`，根位置 3146＋27，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 3146. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E18, E30, E38, E41

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 17.145 秒，模型等待 47.869 秒，真实 solver 27 次，查询投影 50 项，动作记录含缓存 41 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 6, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `de8a14c6e6c1818e29c8535e5be4bf7202f0831958fd2c69bca7bf0931b3fc3e`，决定 SHA `a8e7bd7277f4a527bc4a4c95030f476dabcb9ee64417b5dacaec3964d1fc60ef`。

## RQ1_18c85d7f1380

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_18c85d7f1380) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-45.json](Queries-45.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_983137cbe5d6)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_4f143792be68ecb2987d`，根位置 6426＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6426. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 38.544 秒，模型等待 38.728 秒，真实 solver 60 次，查询投影 71 项，动作记录含缓存 51 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `f02817a9e7579e9bfa83eeb0d9d136f99d35dcaf024b9f07b8f59b3c7a9aacf1`，决定 SHA `7ce2aca4aa5fbf8e66295ecd294b9ac39948133d74e38d1a2f43c4c7fc783d72`。

## RQ1_41590ce9c076

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-14.md#rq1_41590ce9c076) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-34.md#rq1_b2e2d198ce9b)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 6, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.608 秒，模型等待 56.499 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 7 项。诊断 {'audit_card_text': 2, 'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `2f25b878ae036b874652984eee745b22a1edc1d9de4afb288f93d68840b71b13`，决定 SHA `20a414b140d3b46bb2755f94d6e3c5276a401c1780e0e5ae96dfb3ef3e89a5ab`。

## RQ1_cea156e41c29

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_cea156e41c29) · 检查明细 [Checks-82.json](Checks-82.json) · 查询明细 [Queries-45.json](Queries-45.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_d695cf0bad2e)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_01f008dd58afd745819f`，根位置 1071＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1071. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.719 秒，模型等待 35.521 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `d65fc16d86077b13b25b4f649ba5949e91f799b7023e8e01139c1fede0078e25`，决定 SHA `fa924df3334d7eb02db573509e71f56cc02afd8639683d933be5d050d4f7d0e1`。
