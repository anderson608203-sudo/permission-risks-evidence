# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_985c6fd1d4e4

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_985c6fd1d4e4) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-47.json](Queries-47.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-40.md#rq1_46a031a993c1)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_423083c486b03a889786`，根位置 1615＋30，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 1615. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3, E4, E5, E6

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.510 秒，模型等待 14.287 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 4 项。诊断 {}。

最终报告 SHA `e5122f8ffbf15dcfef53d411d8e2ac187e9a1a6bab4e13e8a393b7c28844931e`，决定 SHA `b56b4afe57bc64e594a40a69db9da468f88aa1db548157468d33058450f479a8`。

## RQ1_166770d81e59

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_166770d81e59) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-47.json](Queries-47.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-31.md#rq1_7dc3f131a856)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_d5cc4593b99c44931a8b`，根位置 6487＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E37, E43, E44

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 70.680 秒，模型等待 27.904 秒，真实 solver 41 次，查询投影 47 项，动作记录含缓存 171 项。诊断 {'audit_source_scope_mismatch': 1, 'shared_declaration_in_distinct_applied_contexts': 3, 'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `cdbb85b396e5070b82ba39ad1c04a3f660e543f7a57c8b97c52db6242d51b244`，决定 SHA `94e14f064b734b3ac68dc37d43a118f068a6399cb9b2a5c54dfbd45919f1f576`。

## RQ1_b5ec0e7b3101

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_b5ec0e7b3101) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-47.json](Queries-47.json) [Queries-48.json](Queries-48.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-40.md#rq1_903bc514300f)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_8ea6152aa88d68f12fe4`，根位置 1628＋288，依据 `program_support`。At setLockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E13, E14, E6, E8, E9

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 112.699 秒，模型等待 38.314 秒，真实 solver 223 次，查询投影 326 项，动作记录含缓存 35 项。诊断 {'unbound_or_inapplicable_seed': 2, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 4}。

最终报告 SHA `ed477f22d987765a8a96a0fe9098c7f688fe07fb42af841265532cea98931e73`，决定 SHA `d79dcaf3b38868bbb3ffe4e5c469d8ca40043923ea5925a8d7b5663d199adcc9`。

## RQ1_d62d0f67dced

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-14.md#rq1_d62d0f67dced) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-48.json](Queries-48.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_93e85b12cf6c)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_42ea42abad2e1094cdf6`，根位置 6863＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E13, E5

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 38.339 秒，模型等待 46.967 秒，真实 solver 59 次，查询投影 71 项，动作记录含缓存 51 项。诊断 {'audit_source_scope_mismatch': 3, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `d641e531d9e2e6d8240f5d0576f8459a8c3274a9c12713f154d55f90b4fba037`，决定 SHA `c3594995eef0071741e8966d84cfd1e003babd790cc3cc399fa17b845eeae7fd`。

## RQ1_28e029638666

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-14.md#rq1_28e029638666) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-30.md#rq1_53599b562d05)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 36, 'necessary_effect_absent': 27, 'detached_local_holder_switch': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.044 秒，模型等待 26.768 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_source_scope_mismatch': 3}。

最终报告 SHA `28b8e48ab7f0ad9277b85fe54ac7a78a3710557c30e52834725e9d912b0c1513`，决定 SHA `80d43847c819851b7605606ace44d642f62e0cb452f17403be74bec17f336f47`。

## RQ1_f529b424392d

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未检出。

[实际输入](InputSource-14.md#rq1_f529b424392d) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-35.md#rq1_507e0efe86f1)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_f79f5a0442a512055a2b`，根位置 852＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 852. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.615 秒，模型等待 29.953 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'explicit_effect_anchor_conflict': 1}。

最终报告 SHA `742780a9ee86149d6a4172bb7a9d67d203e867298da54cb5cd3f8a85ee731c66`，决定 SHA `60c0a7b7f374144ed844c9fff7bbad34e3c1c72c4eee463c9ba055d88b3acc44`。

## RQ1_55a1e2ef0f09

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-14.md#rq1_55a1e2ef0f09) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-48.json](Queries-48.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_fe4ace2cd8e5)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'scope_missing': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 16.437 秒，模型等待 42.554 秒，真实 solver 47 次，查询投影 48 项，动作记录含缓存 46 项。诊断 {'unbound_or_inapplicable_seed': 2, 'explicit_effect_anchor_conflict': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `48a747fe727415b996979eec5ba95e1c859c40effe6dbe9d3b939599360b49aa`，决定 SHA `9c6b3088be210b17f781b4eb3d2ce2f5b70782648bed562d8be722dc0260008b`。

## RQ1_d6eec0ddeec9

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-14.md#rq1_d6eec0ddeec9) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-27.md#rq1_92a10a0592ae)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_cc507c6afa0d1f5e6056`，根位置 1337＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 1337. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.269 秒，模型等待 41.487 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `8f85644bf8c7851f1361ea74f2514fa60cb52fff699b4b00af7eda7b7b58cebe`，决定 SHA `b52b5368d8c9c5b091d80b0017937a54ad89ca1e4003837d0bcf55069919ad45`。

## RQ1_adf5a6b0fab0

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_adf5a6b0fab0) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-48.json](Queries-48.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-37.md#rq1_fbb992d4ac67)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_b8a42648896cd6746d7f`，根位置 4161＋14，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 4161. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E2, E4, E6, E8

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.824 秒，模型等待 27.887 秒，真实 solver 6 次，查询投影 10 项，动作记录含缓存 7 项。诊断 {'audit_card_text': 1}。

最终报告 SHA `8a02672b0a5a8236c083a14772f36745e97f4f987196986260cc630cdb431529`，决定 SHA `87c6b6ee271c8244d0079b3a07c4f5fbbd7efae2e22828335011496d0d5db663`。

## RQ1_f322b5b8495d

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_f322b5b8495d) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-33.md#rq1_5eee31e70615)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 2, 'no_effect_in_scope': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 1.997 秒，模型等待 54.083 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'explicit_effect_anchor_conflict': 3, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `9d930a8633c21d5fa871e08390c18aa392e4b8bafcbb326ddc31298f5159bf37`，决定 SHA `df431c53ad920e3e3c602cc1f81c2893d1df3919e2d9913264eca4b8e6b90cbd`。

## RQ1_6827335b3690

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_6827335b3690) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-48.json](Queries-48.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_95cf7213c86a)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 18, 'necessary_effect_absent': 7, 'detached_local_holder_switch': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.963 秒，模型等待 35.000 秒，真实 solver 7 次，查询投影 6 项，动作记录含缓存 26 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1, 'semantic_answer_outside_sent_scope': 1}。

最终报告 SHA `5939b68fe7e16f01b80889eaecab8cfc391f79739865d4deddf6369692406ce6`，决定 SHA `5fce0d7c4323bdba5e6a8d3918065d9352d5943ad43a561353de0e82f15468eb`。

## RQ1_17f46ff7b389

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_17f46ff7b389) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-48.json](Queries-48.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-48.md#rq1_4850481cd27e)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_5124f394c65a8b80b4e1`，根位置 2086＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 2086. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E7

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.507 秒，模型等待 75.503 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 28 项。诊断 {'audit_card_text': 1, 'no_locatable_source': 5, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `2e1265b7026fd2527666d9188309b658ea0df10d9f2ef639c30cb5db6d8fa774`，决定 SHA `6fe0d699712502a2310f722d24cbe7c76700fe12cbe5681297833080b20e3694`。

## RQ1_b2e2d198ce9b

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_b2e2d198ce9b) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-48.json](Queries-48.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-31.md#rq1_41590ce9c076)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_bd71b54087dafa77ddd5`，根位置 1055＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1055. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.708 秒，模型等待 44.078 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'unbound_or_inapplicable_seed': 1, 'audit_source_scope_mismatch': 1, 'no_locatable_source': 1}。

最终报告 SHA `448ec619b80950c792e91ce1d853191a6a5744ae665efa3224f37f10bb713903`，决定 SHA `f9f9081e835bbbaf2868fc161b56b1307f3645477b050ce25f3c68d8628c8834`。

## RQ1_2ee1d93e1f45

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_2ee1d93e1f45) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-48.json](Queries-48.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_ffaaf45e84b1)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 11.210 秒，模型等待 39.554 秒，真实 solver 21 次，查询投影 18 项，动作记录含缓存 45 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `80ceab1bb8fa58e342e2913c13de34b1392dafbb27b7b4b1f6530f4f8a6e72d7`，决定 SHA `3a324299b6af352d1456b4811884a3259373346c520aa0145208b602db85eea7`。

## RQ1_079ea1dcd765

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_079ea1dcd765) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-48.json](Queries-48.json) [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-44.md#rq1_061399788fbe)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 13, 'no_effect_in_scope': 18, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 900.491 秒，模型等待 34.302 秒，真实 solver 959 次，查询投影 616 项，动作记录含缓存 23 项。诊断 {'audit_source_scope_mismatch': 1, 'action_slice_exhausted': 13, 'program_encoding_budget_exhausted': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `260502c99d2498dc5cee4155b38f44c47fbfb4c6f47bc5ad177577ce06a74091`，决定 SHA `7e68145bc12c4005e47e006a27cc2ecd5e328bf7f85ddaf0c3b9ff4a905b17a3`。

## RQ1_f589115e3485

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_f589115e3485) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-42.md#rq1_354610c52c19)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_4b7a6c66216631aacbcc`，根位置 1404＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1404. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.743 秒，模型等待 33.260 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `66d9315c309e2cf60031d4b65fb73ed766c6cd197cc2fa46f96124c5825d2ead`，决定 SHA `478e7bed076999d26c09642e5bd98523d4ce0db73cefe76fbadce520d9039607`。

## RQ1_63b77851cec0

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_63b77851cec0) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-30.md#rq1_644c45f93d78)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 29.435 秒，模型等待 60.949 秒，真实 solver 23 次，查询投影 27 项，动作记录含缓存 17 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `06d2aaf477fe807319542bdd71cec3753543a1b06a6d275407e5d9f9e78b35fc`，决定 SHA `bc19d5b6fd1d1cd0deb5e406b31c0d6d0c7fe118810c7135cc31cf280d8dbfe8`。

## RQ1_45fa9e84e0d6

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_45fa9e84e0d6) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_0d67d852c850)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_79d82576e6f3a5daf983`，根位置 2746＋30，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 2746. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E11, E12, E7, E8

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.833 秒，模型等待 46.145 秒，真实 solver 12 次，查询投影 25 项，动作记录含缓存 23 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `9b3f241313d8df56686a770278a995cec19819229e8e78c5d81654cf5b8ce615`，决定 SHA `74b148b94924334ac5a79eacea0de1d7eb15b9a0552c46de10e6b379cb964f3e`。

## RQ1_d9f9d5c86db9

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未知。

[实际输入](InputSource-15.md#rq1_d9f9d5c86db9) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-48.md#rq1_750c11959b7a)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 5, 'necessary_effect_absent': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.129 秒，模型等待 36.961 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'explicit_effect_anchor_conflict': 3, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `5fbd3f4e48fe83eeaeea3550724da70290cd19542b5a1391a7e07ad0d89c62fe`，决定 SHA `bd1844a4aae759e12b774ba3cdd997483637fa8784dc791b42f65088cf709763`。

## RQ1_e853788bd602

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_e853788bd602) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_db09d4f2c6e5)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_751f360a022e131d5068`，根位置 2947＋467，依据 `program_support`。At destroyCoins(address,uint256), a privileged effect leaves another holder with fewer rights in the same unit after attributed transfers and applicable settlement. 证据 E24, E25, E29, E41, E42, E45, E60, E61, E63, E64, E66, E70

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.472 秒，模型等待 42.689 秒，真实 solver 28 次，查询投影 43 项，动作记录含缓存 57 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `98e1aeb160909a215bb90183cf740ce7805846d72098246903e70dd409e052dd`，决定 SHA `656bb79d91d16ec98e4f2a8d249ba8222dbcd55ef6d849a0cc93db1255fc4177`。

## RQ1_8921e5cc1831

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_8921e5cc1831) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-42.md#rq1_d1c797e20951)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 1}。相关检查决定 {'scope_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.472 秒，模型等待 57.396 秒，真实 solver 3 次，查询投影 3 项，动作记录含缓存 3 项。诊断 {'audit_card_text': 1, 'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `3be0353b0dfe18628d4b5418e36c189dd7d2dc357a8194b56bd6ef0d3bde31f4`，决定 SHA `76116343bebd1026692a1b6e0ba0edd321a5941bd3583c06fe41862daa23cdfc`。

## RQ1_4febca8bfe3b

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_4febca8bfe3b) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_49db443acf1d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_ec2d51fcc89a5d713670`，根位置 460＋476，依据 `program_support`。At zero_fee_transaction(address,address,uint256), the scoped change moves another holder’s existing rights to a separate position without the applicable holder-issued consent. 证据 E1, E18

发现 `finding_6187c378745dbbd9902a`，根位置 777＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 777 under financial_right. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E10, E11, E13, E2, E3, E5, E7, E8

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.893 秒，模型等待 46.428 秒，真实 solver 5 次，查询投影 8 项，动作记录含缓存 6 项。诊断 {}。

最终报告 SHA `c4d02256565f66db0109b1098588bf011dc31076fec53be6002d12bbb220e78a`，决定 SHA `3e2e7314a261569172f5bc4a58006b59377ca04f0de742e9ebc4e7b0be0c290d`。

## RQ1_e73c99ca23e5

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_e73c99ca23e5) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_1f06ce07140f)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_c4eb647a03b016896f5c`，根位置 5144＋26，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 5144. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E1

发现 `finding_5ffeaab765eab2651701`，根位置 5144＋26，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 5144. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E5

发现 `finding_4d9d64b2a06fe36a6b90`，根位置 5144＋26，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 5144. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 15.522 秒，模型等待 42.931 秒，真实 solver 33 次，查询投影 64 项，动作记录含缓存 28 项。诊断 {'missing_claim_or_source_anchor': 1}。

最终报告 SHA `8d51adcffb4763eabc34714a87a5c6456e1db75b1f9407e90a8ef3d2c299192f`，决定 SHA `f39fd93e58cabb99f2e592a133571abd760fa482bc111b7dad217aff91944dba`。

## RQ1_d6441d8f6b1a

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_d6441d8f6b1a) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-33.md#rq1_2adba86dbbfd)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.019 秒，模型等待 45.742 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `a9d4e493228d55db6753224a1b341303f6f86169b0d459c2a267f041a69271c8`，决定 SHA `1c4f6ddcc9935d421733f0732c29e5d092e6aefc0fd0af870e6756ef3662f021`。
