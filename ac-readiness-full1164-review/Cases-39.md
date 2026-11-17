# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_c45fb3515d93

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_c45fb3515d93) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-39.md#rq1_1a822f2e408c)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_20b794f6af407669af5c`，根位置 6110＋14，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 6110. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E10, E11, E13, E15

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.855 秒，模型等待 17.744 秒，真实 solver 26 次，查询投影 26 项，动作记录含缓存 28 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `ccc4cd562aa19035b2199162559206f3295a40841602df4ba8d1cd6122a5b547`，决定 SHA `3f220ce7d4730ba10a63a4ae5353a0e47cc321fdc297e1cac31ce33a943fc637`。

## RQ1_3b4d9f6eb96f

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_3b4d9f6eb96f) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-56.json](Queries-56.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_0267e2a8ebb2)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 30.189 秒，模型等待 57.787 秒，真实 solver 23 次，查询投影 29 项，动作记录含缓存 19 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `bf5e73fbee4db738cdd9c71a903d206899260e46370ab769ada171cc06aa6b0e`，决定 SHA `392194c2f856d36e1d35df830fcfc058c755d6bbe8311411d71a2ec36ac490cc`。

## RQ1_1105ef7570ba

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_1105ef7570ba) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_290892078b6a)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_5e1506131c6177422f40`，根位置 785＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 785. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E2

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.585 秒，模型等待 18.059 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'invalid_semantic_row': 1, 'audit_source_scope_mismatch': 1, 'explicit_effect_anchor_conflict': 2}。

最终报告 SHA `6c6366afbc5628bd3b9bcd5fa83ffcdf327124a7f5793de48d047fb121e2e99c`，决定 SHA `7da4c2f288804e475a3ca19fbdc1d91e2ec2d8cd9f6b1179b5601963227782af`。

## RQ1_4a8515bede97

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_4a8515bede97) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-48.md#rq1_cbf806ae77cb)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 36, 'necessary_effect_absent': 27, 'detached_local_holder_switch': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.446 秒，模型等待 51.876 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 6 项。诊断 {'core_unresolved_retained_for_investigation': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `ae7a506a5031dfa10ae7af112fc253dc5e0214decdc357d2890699c8fba7ed68`，决定 SHA `c72f82a4175b17776bc6301eaa435ac6b464ef3e70e9796a67ccf03b859e2513`。

## RQ1_81b770577694

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-16.md#rq1_81b770577694) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-29.md#rq1_c4aeb6122521)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_36cb72df45d9fc220dfe`，根位置 1155＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 1155. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.525 秒，模型等待 22.429 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `89f1eb57d7310ce0a893c08d1e8d1d79fd87923ef2be4fa761859c713d8c469b`，决定 SHA `8be4d9dad1b855cb95d794d45fbf7d3e5de84d477ff1ce461c62c0b99023b7c1`。

## RQ1_d1e5e262ff31

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_d1e5e262ff31) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-35.md#rq1_34d982d4a91f)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 41, 'necessary_effect_absent': 27, 'detached_local_holder_switch': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.396 秒，模型等待 38.345 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_effect_unbound': 1, 'audit_source_scope_mismatch': 2}。

最终报告 SHA `84061ab377a6f4058a1f7baeff72a51a6ba9628c5ff403af8b47338fcfb2c39a`，决定 SHA `a8a0f05cde29c0760a879f25f7a5e253a8c1e61104247f41a5ad5b7c72c2ff98`。

## RQ1_6eeaddaeac8f

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_6eeaddaeac8f) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-56.json](Queries-56.json) [Queries-57.json](Queries-57.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_4e36475bca23)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'holder_consent_basis_unresolved': 2}。相关检查决定 {'scope_missing': 11}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 900.249 秒，模型等待 73.363 秒，真实 solver 162 次，查询投影 140 项，动作记录含缓存 32 项。诊断 {'action_slice_exhausted': 13, 'yield_to_source_bound_semantic_review': 1, 'program_investigation_budget_exhausted': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `779374338442de4a03dec78493e1784b1586d460c3b754df5c3beda972f8f2ca`，决定 SHA `c04d80d94e132d83e6c1630667d3132c844c0072bb7415e0f8860bde221e5c44`。

## RQ1_c3d569994373

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-16.md#rq1_c3d569994373) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-35.md#rq1_2b2d929cbd84)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_d5701ee46fc03f8673f5`，根位置 850＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 850. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.643 秒，模型等待 17.422 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'explicit_effect_anchor_conflict': 1}。

最终报告 SHA `a1cc5f14f55536dea16c432ba87d69ee6bbc7b31a3bc726b243a672cb7b355db`，决定 SHA `2713ad50788de4c58b71764c37f4b55cf5798cff95ff3b02ac9f9daef31ea29d`。

## RQ1_0267e2a8ebb2

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_0267e2a8ebb2) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-57.json](Queries-57.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-39.md#rq1_3b4d9f6eb96f)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_3f4971131a35cce6466f`，根位置 6626＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6626. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E19

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 68.443 秒，模型等待 53.182 秒，真实 solver 79 次，查询投影 91 项，动作记录含缓存 156 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `a2b69680c5d28faa9f66b4fc65aaa4dbceb706262546b48c7178cc2df784993d`，决定 SHA `68f22cb0e3d9672a7e06e7ec0383bf0f77fcec26e4ad49fdb916f60a3834d1bc`。

## RQ1_324b7ead5ac7

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_324b7ead5ac7) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-57.json](Queries-57.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-41.md#rq1_e5e7e5764fff)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_11c802f2f7e6fc6971a1`，根位置 9274＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E13, E14, E5

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 54.175 秒，模型等待 20.060 秒，真实 solver 60 次，查询投影 71 项，动作记录含缓存 51 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `f4022fa6783c30bc0b9665b9eb12cc46236a912c8c9901cc31ed71b3bfd15903`，决定 SHA `6f4c8e01cb17ac7173138eb8b488f3ecae46102a4e35a99a6fdb9ce0253da5e5`。

## RQ1_caff62da8e8d

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_caff62da8e8d) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-57.json](Queries-57.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-44.md#rq1_55582b2a55f9)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 5, 'necessary_effect_absent': 5}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.150 秒，模型等待 71.445 秒，真实 solver 9 次，查询投影 12 项，动作记录含缓存 31 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `f3d6a92b29832665babc119bc9951e3797b6317d56c29b9f19b00aa8f8fff40c`，决定 SHA `1fd6c50e3d3e84e678dc3511cc69a8172edddb1695a94c2bfe192d858082b95d`。

## RQ1_8d354778e2a5

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_8d354778e2a5) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-57.json](Queries-57.json) [Queries-58.json](Queries-58.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-29.md#rq1_188b4ba2c3ef)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_435400df97718934af9a`，根位置 3563＋337，依据 `program_support`。At addLock(address), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E1, E16, E18, E2, E3, E32, E35, E4, E5, E6

发现 `finding_b7433460b402e1ea770b`，根位置 3906＋221，依据 `program_support`。At setExclude(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E12, E23, E24, E33

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 506.891 秒，模型等待 37.337 秒，真实 solver 801 次，查询投影 569 项，动作记录含缓存 24 项。诊断 {'action_slice_exhausted': 6, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `fd510bec51ea6e9b39af034ff8fd3d173b7b77a3e6d68ac9404af1db33990548`，决定 SHA `8cc0df67dda2c7dc4092742dc7c986603e990d4aac703f18821d455f5b7d31ae`。

## RQ1_3dcd11c8e603

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_3dcd11c8e603) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-58.json](Queries-58.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-40.md#rq1_532d0e522c88)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_01f2b972d0f7871a2ad2`，根位置 6606＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E24, E33, E34

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 67.503 秒，模型等待 34.741 秒，真实 solver 80 次，查询投影 91 项，动作记录含缓存 156 项。诊断 {'audit_source_scope_mismatch': 2, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `b65b3a200b7462ee7e31a141c1d304215d0df79ab8b12d4fb59b8e104a107796`，决定 SHA `bff98f999eede8afb9c084d00ac71b5bcd08802aacb328dafb979f37ebde001c`。

## RQ1_a9742b3414d8

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-16.md#rq1_a9742b3414d8) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-27.md#rq1_6af8dad9e222)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_7aa68f38b0f56ed2d042`，根位置 1218＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 1218. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1, E2

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.531 秒，模型等待 43.087 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'missing_claim_or_source_anchor': 2, 'audit_source_scope_mismatch': 1}。

最终报告 SHA `880bc696e6e669b1fa07fe66380bd34e6bbe724454b7a8f5f51da69889ec55ff`，决定 SHA `28ce6f5162f8f1ab75f40c13ce48e697c8679e95d01b1376ce674360d7c0a73e`。

## RQ1_f88298f30fee

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_f88298f30fee) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-58.json](Queries-58.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-37.md#rq1_8528c7edab2f)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_43e4991dda14abb87612`，根位置 4100＋14，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 4100. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E13, E15, E7, E8

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.358 秒，模型等待 26.210 秒，真实 solver 11 次，查询投影 20 项，动作记录含缓存 13 项。诊断 {}。

最终报告 SHA `8cb7f8c7f5ba64d7a6f42e5cbf74991c5f816628dc48614e83bd25ddad0fd0d7`，决定 SHA `3260b542f829d044b8ab4a918dce93ae10d8a0e1ad19dbfdaa3f6340c9803bb1`。

## RQ1_1a822f2e408c

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-16.md#rq1_1a822f2e408c) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-58.json](Queries-58.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_c45fb3515d93)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 1}。相关检查决定 {'scope_missing': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.823 秒，模型等待 40.464 秒，真实 solver 32 次，查询投影 28 项，动作记录含缓存 38 项。诊断 {'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `337818565b36e69baf6fa5c2b62ad21496022c851f20efde4e2b234b10ffb1ff`，决定 SHA `d3612dd21c8932c49fa54eb7689042842882c7ea3a2220c475938d8d04bed34c`。

## RQ1_82d1cda193c4

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_82d1cda193c4) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-32.md#rq1_91d0edd5d20c)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'necessary_effect_absent': 3}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.133 秒，模型等待 53.829 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `99f51070d298ede015a5c04b0e4615cad506a7139d1326d76b1fa67b73636d09`，决定 SHA `88bd7532fd9fd00b183aedb386d2532942d7fc8870d96fcdfd88f09c50fb6e5c`。

## RQ1_2495364b313d

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_2495364b313d) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-58.json](Queries-58.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-47.md#rq1_f74603cd2593)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 20, 'necessary_effect_absent': 14}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.897 秒，模型等待 44.855 秒，真实 solver 17 次，查询投影 13 项，动作记录含缓存 9 项。诊断 {}。

最终报告 SHA `fd67203eb3bff431d4c34e6fb8daf5ff0135f6044ab42710711c985bf07cd38a`，决定 SHA `39be93a09d00864f346f7bf139a5f15be60613e1f621c317341502b71ce23882`。

## RQ1_14f47df9bd94

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-16.md#rq1_14f47df9bd94) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-47.md#rq1_97f9b80f268e)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 36, 'necessary_effect_absent': 27, 'detached_local_holder_switch': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.088 秒，模型等待 28.928 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_source_scope_mismatch': 2}。

最终报告 SHA `7a660d4168a61d6054044d7d653698fe50b1a04f7d15242de123864622c772e3`，决定 SHA `bc8b893422b56393040752025a926d3d54d31140818db6751296611ca1eb285c`。

## RQ1_cf32aac41cf2

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-16.md#rq1_cf32aac41cf2) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-58.json](Queries-58.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_a4c5ecc3c29e)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_65829a35ac8c7c2e1b4c`，根位置 929＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 929. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E1, E3, E4, E6

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.195 秒，模型等待 29.685 秒，真实 solver 3 次，查询投影 4 项，动作记录含缓存 4 项。诊断 {}。

最终报告 SHA `86f5b5d53d3f9b4d23afd207f93895cfc2772d169e0d78d36145b488c112ecd3`，决定 SHA `cdd6124a1a6ef2f46534d03f2ac03e6d01d6a3b6335b0142c1e08e022f7c94b0`。

## RQ1_196284e657b0

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-17.md#rq1_196284e657b0) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-37.md#rq1_0bf6f8bce8d9)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_fe689153f6d8150c19c1`，根位置 946＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 946. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1, E2

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.778 秒，模型等待 40.941 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'audit_effect_unbound': 1}。

最终报告 SHA `c45f3d234d308a9e2394e985d2ba39696d8c3866bdca84aa6c9f930c50540cf8`，决定 SHA `ce3fd82c8f2faf04c8710316fa12cdf35805eb8e45556c8b9a200c54e2e8d9fe`。

## RQ1_185a84436c18

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_185a84436c18) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_ed58b7d7bfbb)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 5, 'scope_missing': 1}。相关检查决定 {'scope_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.538 秒，模型等待 32.406 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'audit_source_scope_mismatch': 2, 'audit_effect_unbound': 1}。

最终报告 SHA `abf0b54a917f676164b1b6e0cc5de06e2254a80df1925f8dab49dff01abe8b46`，决定 SHA `02322e398bde14f9c8b78656672a10ee23ccc570a64c9d6b72d338125daa6299`。

## RQ1_0b3eb8950ea9

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_0b3eb8950ea9) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-28.md#rq1_a626fef83244)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.188 秒，模型等待 37.754 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `8ddbac98910f484174ccc8957045551a4a35842227b39993bf4270fe8d7abb53`，决定 SHA `15744694b77275513475ad7d09f82e64f55bb66cdf604371f1c1b36a09c0b3a7`。

## RQ1_6b70a408ccf8

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_6b70a408ccf8) · 检查明细 [Checks-85.json](Checks-85.json) · 查询明细 [Queries-58.json](Queries-58.json) [Queries-59.json](Queries-59.json) [Queries-60.json](Queries-60.json) [Queries-61.json](Queries-61.json) [Queries-62.json](Queries-62.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-40.md#rq1_c6f96b65d39b)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_bd8b042802c9b5a05fc3`，根位置 2374＋25，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2374. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. An already exempt agent may serve the same request if the holder granted the required allowance. 证据 E14, E38, E39, E8

发现 `finding_8a74300c9291a6f6fa19`，根位置 2374＋25，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2374. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. An already exempt agent may serve the same request if the holder granted the required allowance. 证据 E12, E20, E46, E47

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 900.357 秒，模型等待 31.582 秒，真实 solver 2230 次，查询投影 2811 项，动作记录含缓存 32 项。诊断 {'missing_claim_or_source_anchor': 1, 'action_slice_exhausted': 1, 'program_investigation_budget_exhausted': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `1a5e1806829e09098e70c478e0d5863414df8215dbd6b7480d99a1a3eb299f62`，决定 SHA `b0762ce1b4f1aa18233f8ca5e1cf576446ed8a488fa6991d10ad893df4f9c556`。
