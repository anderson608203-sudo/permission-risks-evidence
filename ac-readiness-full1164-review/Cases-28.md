# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_2b63785028d0

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_2b63785028d0) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-31.md#rq1_816348240738)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.629 秒，模型等待 75.312 秒，真实 solver 3 次，查询投影 3 项，动作记录含缓存 10 项。诊断 {'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `6b70850ab3ff46009816203e30bd1c566db3880e367cda8c75dab0c0682b9669`，决定 SHA `0f9883aaaa6daeee0249afeece422579f5321231bbc5c6c3e1e5f3d5155fd882`。

## RQ1_d76214290589

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_d76214290589) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_cebbce39a728)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_b0e0661dea97cd642909`，根位置 1073＋13，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1073. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E2, E4, E5, E7

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.360 秒，模型等待 27.381 秒，真实 solver 3 次，查询投影 10 项，动作记录含缓存 7 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `c6799394e79955cc196a6ca6213ce27a869343fe730bb61e2fa3ef32feb6fcef`，决定 SHA `7d7bbc5a8ed935ea687e12b548b898677179821f33ccee0f5b30b2f2fd11223b`。

## RQ1_2d95ecb7d514

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_2d95ecb7d514) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-47.md#rq1_b3e3847ba6e9)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 25, 'necessary_effect_absent': 27}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.023 秒，模型等待 27.083 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `c00645e933c90051ea4bec633c2ec6599752e4b5bed53bae0b75a484545f3e32`，决定 SHA `a3075604c92c89c0754a24c038d08dae7a7d5c1afb083b0ea5fa5e4902c0c4bf`。

## RQ1_815bdde1a02e

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_815bdde1a02e) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_2082ab99d930)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_83940993061154c0f750`，根位置 6432＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E2, E7, E8

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 72.773 秒，模型等待 50.876 秒，真实 solver 32 次，查询投影 38 项，动作记录含缓存 21 项。诊断 {'invalid_issue_field_shape': 2}。

最终报告 SHA `041a317275aaac93c0ff98d18d248cfe8968baf2c414dc7463d0c2ba72e376ea`，决定 SHA `fc2f57792e4b9b58c3747a1c083ac1564e189c77343a9c79bd5196265bb41f43`。

## RQ1_a68ae7d1761d

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_a68ae7d1761d) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_7cd121e3acec)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_24f9ac97becf4b137324`，根位置 8835＋30，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 8835. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E15, E21, E22, E7

发现 `finding_e621fb5197dc4fd4eaff`，根位置 8835＋30，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 8835. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E11, E19, E25, E26

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.564 秒，模型等待 18.699 秒，真实 solver 8 次，查询投影 25 项，动作记录含缓存 22 项。诊断 {}。

最终报告 SHA `35fc445e6eae9bd461fa05694b7e38dee8806230890d77f3cbef0fff49b6348d`，决定 SHA `ec6f7e44fa7b10bb9c9c967d487ae914e383cc825ced6fd2940b55e769e91f53`。

## RQ1_8bacff1e94bf

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_8bacff1e94bf) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-41.md#rq1_c9a45d0b378e)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 43.951 秒，模型等待 36.112 秒，真实 solver 23 次，查询投影 29 项，动作记录含缓存 19 项。诊断 {'audit_source_scope_mismatch': 2}。

最终报告 SHA `ff5b0244407954ff3168baaea01d3fc0c126996361b0d1dc26909565d6e98058`，决定 SHA `7763d9ca4765380cd5a63d214486da576b802c2392c3d1d45918fd1e4ffaa55f`。

## RQ1_770ae395781c

任务 FCR，评价类别 FCR-MINT。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_770ae395781c) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-27.md#rq1_bc5855a83e2d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 13, 'source_task_reading': 10, 'necessary_effect_absent': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.341 秒，模型等待 26.807 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'explicit_effect_anchor_conflict': 2}。

最终报告 SHA `3e4aea86788397197546f31c3e0fd4f86dd70cd0e24babd2eb05a4a62f687f52`，决定 SHA `0eda9236b6af931abe45afadb5ba4dc48fcbeb9ec0b056c8f0ce66bfe7569ba3`。

## RQ1_3d04b623776f

任务 FCR，评价类别 FCR-TRANSFER。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_3d04b623776f) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-42.md#rq1_d41d9bdcf084)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'core_mismatch': 1, 'external_dependency': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.961 秒，模型等待 53.405 秒，真实 solver 9 次，查询投影 12 项，动作记录含缓存 29 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `f9481ada92c256c81095020d46a87167144945c293f6bcfe1b1aca1312a291a5`，决定 SHA `ded13c05c9b4616fdf789da731922e67586d3c4a1c7922aed755ac5a00d4e8fa`。

## RQ1_7597fe797887

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_7597fe797887) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_6187bc3509e7)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 17, 'no_effect_in_scope': 17}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 30.159 秒，模型等待 51.087 秒，真实 solver 23 次，查询投影 29 项，动作记录含缓存 19 项。诊断 {'explicit_effect_anchor_conflict': 1}。

最终报告 SHA `e4e93c6a63459a2ee0a27fe62b512048e4242daa898e917aeac20ab534b0b531`，决定 SHA `eae052f9103817d9ae71d217e089823a0356848197f41c386bfbdf7046c35be4`。

## RQ1_e5cc8c6eec49

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_e5cc8c6eec49) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-27.md#rq1_1c369a1de4e8)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 6, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.479 秒，模型等待 48.886 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 29 项。诊断 {'unbound_or_inapplicable_seed': 5, 'invalid_semantic_row': 3, 'unrelated_or_secondary_graph_pairs_deferred': 4, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `305b6b56a836003440a16b7644d1c0cac294f529a392b3d8bab82b7c13389c38`，决定 SHA `ed274671d690bae631bca15acd308324a89924b29f27d7c16568619e226de1fd`。

## RQ1_8b91a8024aa0

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_8b91a8024aa0) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_ad1b052af855)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_3410b18f100bc62801f6`，根位置 6175＋223，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E2, E7, E8, E9

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 111.420 秒，模型等待 37.345 秒，真实 solver 35 次，查询投影 41 项，动作记录含缓存 22 项。诊断 {'audit_source_scope_mismatch': 1, 'explicit_effect_anchor_conflict': 1, 'action_slice_exhausted': 1}。

最终报告 SHA `159f54a7ea000f51a860c2caaf2ff985ff6ef35a0380a081f7344ac35f98edb8`，决定 SHA `a710667410c275b95fbc43c80e4683f9120dda03d2719d16dde54bb13b898dc5`。

## RQ1_3a3d833ca142

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_3a3d833ca142) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-48.md#rq1_206d19a8539c)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_857ed57cbf12ab6279cf`，根位置 785＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 785 under financial_right. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E2

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.190 秒，模型等待 73.481 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `3cc93c031e10cb2f39846e9a8d8ae0cf6438246690be744c2ac83aec9489ccbd`，决定 SHA `5f811c0239485f3b3985d727b9a73ea906650fe06a87d98caa22cd2b73a9dd91`。

## RQ1_661b0064ae6b

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_661b0064ae6b) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_6239598c387b)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.654 秒，模型等待 46.678 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `2494658cefdfac51ab5bdda0477db942e6c92ccc8040d693152c9883fa2ecf45`，决定 SHA `b04ce45ac5dd664c2f9ef766fe51219343eff482e931472931df2a5000ec01df`。

## RQ1_4be3030c4533

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_4be3030c4533) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-48.md#rq1_af7c473b8cca)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 29.980 秒，模型等待 42.320 秒，真实 solver 23 次，查询投影 29 项，动作记录含缓存 19 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `2a5f1c070ddad4e7404669d1c0d296b129dec3435a273d51c9197d034612d1ef`，决定 SHA `392194c2f856d36e1d35df830fcfc058c755d6bbe8311411d71a2ec36ac490cc`。

## RQ1_7bfd58ffb1ae

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_7bfd58ffb1ae) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-28.md#rq1_cb8c3fafbda1)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'scope_missing': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 18.236 秒，模型等待 57.803 秒，真实 solver 39 次，查询投影 41 项，动作记录含缓存 79 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `a149f845792d5dae14350564104b05c9b6a80b73cbc66e95000f2ac30089c526`，决定 SHA `6c0663c176a202e72e43c34ea017ac38b0c38449f7194b5a2117cbec5ecb5bc5`。

## RQ1_bf35b402b6c4

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_bf35b402b6c4) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-35.md#rq1_39821973be02)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 9, 'necessary_effect_absent': 6, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.165 秒，模型等待 26.124 秒，真实 solver 3 次，查询投影 3 项，动作记录含缓存 6 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `7c25477942f2e7c1901a813458d86dabfad478db29a897449d69f3440e639df2`，决定 SHA `dc12bd0e5f9d446077bf28d0dc99054488e8ebf6dd3d96c774c0f4483fd362ca`。

## RQ1_15346457ba72

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_15346457ba72) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-41.md#rq1_fe7add810da5)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_a8a554fac67f8a7de487`，根位置 1112＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 1112 under financial_right. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E2, E3

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.192 秒，模型等待 55.630 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {}。

最终报告 SHA `2cd72bc335df70e4d01c177d4d250d8f56dedbb240950c9650422a6f0cb01f75`，决定 SHA `c13936c256c81abd9cb7ecc899fcc7849c75fe5b1ac782834dba2c9277c5b954`。

## RQ1_21604460c189

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_21604460c189) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_8175a1b20602)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_c464f5bf000f7a08e7f2`，根位置 6862＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E13, E6

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 86.741 秒，模型等待 37.591 秒，真实 solver 69 次，查询投影 80 项，动作记录含缓存 51 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `566bcd038f89faa116e47832c0feb8d7d487ad33d24a8ee0bd729721035e7c64`，决定 SHA `73199bcb9782a43c589efa7a125479835691c57f1e3c7b96e49dd9eadd954e88`。

## RQ1_329e0d0d7a11

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_329e0d0d7a11) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-41.md#rq1_30c29cd44cad)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 4, 'necessary_effect_absent': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.269 秒，模型等待 25.371 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'explicit_effect_anchor_conflict': 1}。

最终报告 SHA `a95117cf598bf68d34ea6cb0a17d29b561903847d4301ee6e2976f74717556ae`，决定 SHA `3b50aa0b54029fc54f54a982ad2e45a8af23db4570c891b2e67221dcf7602ef5`。

## RQ1_cb8c3fafbda1

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_cb8c3fafbda1) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) [Queries-39.json](Queries-39.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-28.md#rq1_7bfd58ffb1ae)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_3f4971131a35cce6466f`，根位置 6626＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6626. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E13

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 52.289 秒，模型等待 41.509 秒，真实 solver 72 次，查询投影 85 项，动作记录含缓存 116 项。诊断 {'audit_source_scope_mismatch': 2, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `3b8cdf4e037b48bd903b898a785b2b263cc140268753df46cac60dcd402612fb`，决定 SHA `30220691305b12cfb1302940e92dcb750ed8ef3116301775913995a3a7a0cabf`。

## RQ1_7fe1d2fd9226

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_7fe1d2fd9226) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-39.json](Queries-39.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-43.md#rq1_d19d0cf1d510)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_07ccccb4e0058c8bd511`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E39, E49, E51

发现 `finding_500e8053e1a36a717e99`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E33, E41, E43

发现 `finding_582517ca7a38bcf0b3d3`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E38, E44, E46

发现 `finding_cfdea8e1b68304791058`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E36, E47, E48

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 32.377 秒，模型等待 36.421 秒，真实 solver 145 次，查询投影 138 项，动作记录含缓存 83 项。诊断 {'audit_source_scope_mismatch': 3, 'shared_declaration_in_distinct_applied_contexts': 1, 'unrelated_or_secondary_graph_pairs_deferred': 20}。

最终报告 SHA `7785fff5dcf7d818fb9fc2863658e0915a0a22469bde784787550e793f3f8357`，决定 SHA `29f23a287c4c99e473921301c1d612ff1a3aa1bb282d5070af8862fd6b247758`。

## RQ1_bcafc7a40ce2

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_bcafc7a40ce2) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-39.json](Queries-39.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-41.md#rq1_e1ce695fff9e)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_45e8ee4dd44f54c2c9ec`，根位置 1203＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 1203. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E8, E9

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.826 秒，模型等待 48.349 秒，真实 solver 9 次，查询投影 12 项，动作记录含缓存 30 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `e7ebec0f34ab858b975d2db4886f4c31bacb948eda83a14690a05c5b21123eed`，决定 SHA `4ef7de3bcdc288c9b1e974aeb961a9bb49ab8fa6de6d3801a3117ba5a249695c`。

## RQ1_9ad7e9b41e3a

任务 FCR，评价类别 FCR-MINT。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_9ad7e9b41e3a) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-46.md#rq1_df25b8b8c6ab)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 13, 'source_task_reading': 8, 'necessary_effect_absent': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.707 秒，模型等待 39.506 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 14 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `9fbfaaaf3f78b1a2ca4fbd95ae0db2547b185f851f2d0119220417035e6e9085`，决定 SHA `ff0d94ff0d0731c1420e0dc73841f4ab1e66c305041986569758d7d1b9995148`。

## RQ1_a626fef83244

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_a626fef83244) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-39.json](Queries-39.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-39.md#rq1_0b3eb8950ea9)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_e1c4984bc8b474907963`，根位置 1513＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1513. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E10, E11, E2, E3, E5, E6, E7, E9

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 24.476 秒，模型等待 27.389 秒，真实 solver 28 次，查询投影 11 项，动作记录含缓存 10 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `29feae33c20f03760cb37a623393c8a511fc0e691e3e260e6e11aca43c7ef981`，决定 SHA `663041a050d946736739a469d105049b4f98f69885657661f6bbc5b2bcfb2c82`。
