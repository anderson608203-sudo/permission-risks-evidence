# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_67214f5ba58d

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_67214f5ba58d) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-36.md#rq1_8b6fb0a7e2ec)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 17, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.812 秒，模型等待 40.805 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'explicit_effect_anchor_conflict': 1}。

最终报告 SHA `9d0870de0030c3a5451a2fdc55cddf2668beec2b517367b92c35f92552d0905b`，决定 SHA `5df37cef1f7aceef009ee37c8f24c16d61a095129a5a8f98d18aa64311ec1747`。

## RQ1_666ef53ce174

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_666ef53ce174) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-49.md#rq1_97f70f5113f4)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 9, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.763 秒，模型等待 41.782 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `45a67d3aaf4c6e7fbc803193f6c5a389bba4905314dccd9a0faa126078b85bda`，决定 SHA `2b65ce208f1ae6789ebbdf89a10d595c29bced7cfdcaeea68d66c2310430beca`。

## RQ1_f82fc055f5dc

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_f82fc055f5dc) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_b884bab91ca4)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 5, 'no_effect_in_scope': 5}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.462 秒，模型等待 48.426 秒，真实 solver 5 次，查询投影 4 项，动作记录含缓存 12 项。诊断 {'missing_claim_or_source_anchor': 3}。

最终报告 SHA `983ce0053181838365a17a6a0144f74344a7d8aee797cfe3c6cc103cbb74398c`，决定 SHA `b2f884581a6f3f824287bd4b36d552cd4728b2df3087e3ba3898bfefb04970a1`。

## RQ1_3ec097691998

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_3ec097691998) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-27.md#rq1_0858684eb758)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {'external_dependency': 1, 'intra_ledger_transfer': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 46.741 秒，模型等待 45.244 秒，真实 solver 45 次，查询投影 51 项，动作记录含缓存 110 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `0e57b25cc7b753fb3d6b74862f37189df7f93f8cbc97f99445df96e4927483d1`，决定 SHA `ec8a493019b32badca64dd6b9ae1573c71e907fadc1f1c640b93d6411c3c03a7`。

## RQ1_682abc2aac2e

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_682abc2aac2e) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_94fb41cd32a7)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_32da4515812c40b34f3f`，根位置 1038＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1038. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E2

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.552 秒，模型等待 18.129 秒，真实 solver 2 次，查询投影 3 项，动作记录含缓存 4 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `cc60341e2d5dc93f4348d25b92e203a2fcc6e566704bfb6eaaaa3e4fd1201266`，决定 SHA `b523bb78fa5c2942199e0637cf1491214fe9291aaad170e54d68f9b65091fe1a`。

## RQ1_7d7240a2af90

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_7d7240a2af90) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_8d60a47186e2)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_4457a71dd2949529a0e6`，根位置 936＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 936. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E1, E2, E4, E6

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.546 秒，模型等待 28.811 秒，真实 solver 3 次，查询投影 4 项，动作记录含缓存 4 项。诊断 {'audit_effect_unbound': 1}。

最终报告 SHA `6b5fe997c026194a5ef338a88780d8fdc6ea4db885c053467d393fa43c950eb4`，决定 SHA `75cc23df6acc07b6e82bc02152482a79d2f2b601b058f578c57b5f43ea24ee82`。

## RQ1_800879bacef4

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_800879bacef4) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_9bec10ec0076)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_efd6497a997b870741f1`，根位置 1092＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1092. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3, E4, E5, E6

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.522 秒，模型等待 30.939 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 4 项。诊断 {'unbound_or_inapplicable_seed': 3, 'no_locatable_source': 1}。

最终报告 SHA `8d1ecaa22f94f670f8fb22f5827cbd6cf1110796e4f0b9c2bfc5dd2b8f6d853d`，决定 SHA `c51cb86a975d57ee4678187ab00c56757f6a2804859e87c85a55069ea7965a55`。

## RQ1_2046acc1c802

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_2046acc1c802) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-27.md#rq1_58de46f081ec)。指定类风险端未检出、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 15, 'necessary_effect_absent': 15, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.094 秒，模型等待 26.771 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `623974d39903df7206ba64557835f87f94e753148e7be3e61a09e2a9920ef3e8`，决定 SHA `ad358f8ae45b08c348476eb9c6675b071de607f97f2e03c94beae8b494ed59dd`。

## RQ1_fb76588a5316

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_fb76588a5316) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-36.md#rq1_7772ad9410c9)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 1, 'no_effect_in_scope': 1, 'no_privileged_intervention': 1}。相关检查决定 {'source_check_excluded': 2}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.088 秒，模型等待 73.003 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 7 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `859ffad1590972314dabad17a768ad697063cfb210776fd995c889c31825066d`，决定 SHA `e54c401e0949fde54eabe9ece6d01f61696e686fd241e19fa25c61db91ac1a43`。

## RQ1_56bac052a93a

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-17.md#rq1_56bac052a93a) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-27.md#rq1_f27cacd5f34a)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_a5bd5741e500f9c634bb`，根位置 4017＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 4017. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E2

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 22.715 秒，模型等待 31.747 秒，真实 solver 27 次，查询投影 9 项，动作记录含缓存 6 项。诊断 {'audit_source_scope_mismatch': 3, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `3d85ac2e5fc3e480cf0b88b0447b268f1a2e7bba3325f9122170a51173faea97`，决定 SHA `6afa6810c35df987015422ea551c4be3fae46551c739ff600b1b1023ef88330e`。

## RQ1_af26ce7636a4

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_af26ce7636a4) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_b00cfec6e8e0)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_b94adadc9836c1da1a3e`，根位置 6491＋223，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E17, E24, E26

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 69.102 秒，模型等待 14.711 秒，真实 solver 72 次，查询投影 83 项，动作记录含缓存 100 项。诊断 {'unknown_or_unshown_effect': 1, 'shared_declaration_in_distinct_applied_contexts': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `22acb7cf251589fe0fda12d5d4410b984795961dad460bfc35d31897cd4b8fcf`，决定 SHA `88455a00d2c2fd7ae26ed59124ccc85cf4cd5cb74848e3d82040778cf1222b9e`。

## RQ1_6a933de928c4

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_6a933de928c4) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_4b4775267823)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.235 秒，模型等待 41.414 秒，真实 solver 16 次，查询投影 16 项，动作记录含缓存 10 项。诊断 {'missing_claim_or_source_anchor': 2}。

最终报告 SHA `d2c356022b6c04dd43107b630260086626538c379000ccdab82a4c37675f1322`，决定 SHA `9b64e109df7daaf537b0d39ce7db8dc92aff9c44b4c816a0cb5daeadf70e0813`。

## RQ1_82b185a4c878

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_82b185a4c878) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-41.md#rq1_f7686568e9cf)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 20.862 秒，模型等待 50.075 秒，真实 solver 23 次，查询投影 29 项，动作记录含缓存 19 项。诊断 {'audit_source_scope_mismatch': 4}。

最终报告 SHA `42ab85b1ad8c46adf25c35aed3cf8262a4694d24205102b7838092c6903b06eb`，决定 SHA `db502848f3d9389c4af7f08b76f8b38037053561ef94e07a7d882291bfb3a347`。

## RQ1_4b19849acc66

任务 FCR，评价类别 FCR-TRANSFER。当前未知，BG 未知。

[实际输入](InputSource-17.md#rq1_4b19849acc66) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-29.md#rq1_514691f1bbac)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'external_dependency': 3, 'source_check_excluded': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.733 秒，模型等待 43.446 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 48 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 4}。

最终报告 SHA `26e783d71804ab999e19a8524ed69d4ee263a99d1ac793fae0e28d290f96d85a`，决定 SHA `f99f14eca90e9cb4152d6720bea2cf23a7e36fec7f5fe03913ed5b86f3365afb`。

## RQ1_354610c52c19

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_354610c52c19) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-34.md#rq1_f589115e3485)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 5, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.908 秒，模型等待 54.608 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 16 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `dde40ac44ec3d9baa3813ae0e626ea4754be9882a106c1adeebfe439c85cbdcb`，决定 SHA `e0d2a3196318821132a2645ea474f0b25e7b6e1d359c26b4cd7f6bd995853faa`。

## RQ1_c46de9c5394e

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_c46de9c5394e) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-31.md#rq1_5ab05cf437b3)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 16, 'necessary_effect_absent': 18}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 22.673 秒，模型等待 32.668 秒，真实 solver 35 次，查询投影 31 项，动作记录含缓存 33 项。诊断 {'audit_source_scope_mismatch': 4, 'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `c7cad270043da3e71cfd1e3a6cf0524d0f68646f7d120c7811acaaad4efef0ce`，决定 SHA `fd03d8044b8a6abeeb2aa23677a332bd91a05d4bfda58ba3fe9da334dc2e0449`。

## RQ1_d41d9bdcf084

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_d41d9bdcf084) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-28.md#rq1_3d04b623776f)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_2c57cefee65d4d437a44`，根位置 1063＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1063. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E10, E5, E7, E9

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.221 秒，模型等待 38.040 秒，真实 solver 10 次，查询投影 13 项，动作记录含缓存 26 项。诊断 {}。

最终报告 SHA `9e131410b3c69fa597e9a3e3ab095f50bc4a95b820f2e175268b64b646cec0ab`，决定 SHA `068a5641602593e2af12e0fb88e6431c857eb0f23e68e17cc9d33f5e2005117f`。

## RQ1_d1c797e20951

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_d1c797e20951) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-34.md#rq1_8921e5cc1831)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 15, 'necessary_effect_absent': 14, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.979 秒，模型等待 16.044 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `9183f9039c8b60bf0b4c83714961e284bcd23c1609546023c098cc7096c73173`，决定 SHA `05b407ad1e450369a8e0ae4a4220c81fb63edf7d12944d9ac40ada27b1565742`。

## RQ1_3b7737691ba6

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_3b7737691ba6) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-31.md#rq1_b80eb72fb713)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'necessary_effect_absent': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.347 秒，模型等待 25.432 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {}。

最终报告 SHA `33b5e523b2990c02b396495f149735f1a25eef47ca6a4c8224d5cb66db5273e0`，决定 SHA `b1280af8fa77262dfafba486ca5daba5d68786337f8a796a9f45d64c29b0db85`。

## RQ1_cb7efb519f69

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-17.md#rq1_cb7efb519f69) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-40.md#rq1_81162a271264)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_f3bf36e646e85dc27e15`，根位置 667＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 667. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.191 秒，模型等待 39.415 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'audit_card_text': 1}。

最终报告 SHA `2aea0c53febf34a11ce5138242de4f17ad1a07fde54c8bae2cab2ad7201d728f`，决定 SHA `0643770b80cad5a822d403113fca79716cb8cc7df6f8bb847326ec1baf08999b`。

## RQ1_613d6352416c

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_613d6352416c) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-31.md#rq1_e48a6c07fe05)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_8b19159a562988b0ecde`，根位置 760＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 760. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.418 秒，模型等待 15.099 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `cbb9b0e9f3cd6df8e4980e3a61594a201c3c967c7826121564c07a36c4450c7a`，决定 SHA `219094ef4e8a6cf378ff1ac27a4945290c735d6cde1526bac7e6530fb409e9cc`。

## RQ1_890376502486

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-17.md#rq1_890376502486) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-41.md#rq1_e38d4cc9d6fc)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_e1e3f96423a89cd79e71`，根位置 1111＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 1111. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E4

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.712 秒，模型等待 71.234 秒，真实 solver 4 次，查询投影 6 项，动作记录含缓存 8 项。诊断 {'unbound_or_inapplicable_seed': 3, 'no_locatable_source': 1}。

最终报告 SHA `10d01f8668bfdeb90e44575d62c9f51a918a5b1ab846598fbef22ec2d9fbc5f3`，决定 SHA `dd50f4a5635833e806207c4a28cc6df786c2e4e332972bb01976a011d04d097e`。

## RQ1_b61f163309a1

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-17.md#rq1_b61f163309a1) · 检查明细 [Checks-86.json](Checks-86.json) · 查询明细 [Queries-64.json](Queries-64.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-27.md#rq1_81a85f242b60)。指定类风险端报警、修复端报警，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_442d99bc20a094d4f25f`，根位置 5099＋361，依据 `program_support`。At setTokenExchangeRate(uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. The intervention can enable a new same-request outcome; baseline commitment is not established. 证据 E13, E40, E54, E67, E75, E78, E82, E90

发现 `finding_3ad924465535c241f3e4`，根位置 9882＋1612，依据 `program_support`。At allocateToken(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E10, E17, E18, E66, E69, E7, E70, E73, E74, E77, E80, E81

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 31.284 秒，模型等待 42.782 秒，真实 solver 68 次，查询投影 61 项，动作记录含缓存 88 项。诊断 {'audit_source_scope_mismatch': 1}。

最终报告 SHA `a4deac806aa01eb2f658dd68a72872258ebb2fad27b1f0a3b3c7fab03b112a8c`，决定 SHA `54637053c31931cd4eb9842422e45fb3bc19d11a03e909fbd5e4a05ee5f9b218`。

## RQ1_45f5c9057f72

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-17.md#rq1_45f5c9057f72) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-27.md#rq1_237ffc6da6a2)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 8, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.173 秒，模型等待 15.518 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_card_text': 1, 'audit_source_scope_mismatch': 1}。

最终报告 SHA `608c674b6f4d8391f8ea0edaf9ad914a4e26cb15b95a640d581528ed8a57cb56`，决定 SHA `37b3173f8962008877fc23ec85626f9cce0069d066c5341fb97c92be95064201`。
