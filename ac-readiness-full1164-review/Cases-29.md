# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_94d9f2cfc77c

任务 FCR，评价类别 FCR-MINT。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_94d9f2cfc77c) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-36.md#rq1_e13bb6580d65)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 13, 'source_task_reading': 11, 'necessary_effect_absent': 2}。相关检查决定 {'scope_missing': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.490 秒，模型等待 41.769 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 17 项。诊断 {'missing_claim_or_source_anchor': 3, 'no_locatable_source': 1}。

最终报告 SHA `41fd31afeb724c70db2f073b4efb4d4649a540a32860cbf14e41d2a6515a820d`，决定 SHA `fbcca6f50a2ebab5ee0831a90a1250aa984979ca60c824adb56af21d9aa488d1`。

## RQ1_5b3469baa447

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_5b3469baa447) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-39.json](Queries-39.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-41.md#rq1_7a7815b00180)。指定类风险端未检出、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 6, 'necessary_effect_absent': 2, 'source_task_reading': 2, 'no_privileged_intervention': 1}。相关检查决定 {'scope_missing': 7}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.676 秒，模型等待 32.863 秒，真实 solver 12 次，查询投影 12 项，动作记录含缓存 40 项。诊断 {'audit_effect_unbound': 1}。

最终报告 SHA `eb17b65b44349cf43a71a16a3feb8e805f99ee5bc3965c7175a05ab18d1abc6c`，决定 SHA `515af22fef38857f35876f1fe6e5d89d973ea1f4931d429db06f5c4ea28e73a1`。

## RQ1_514691f1bbac

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_514691f1bbac) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-39.json](Queries-39.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-42.md#rq1_4b19849acc66)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_ad6bf461372ef314ea64`，根位置 2173＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 2173. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E5

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.060 秒，模型等待 38.782 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 17 项。诊断 {'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `fe9cfe8b677dc17aafff99add1623295c67d8a089b776c3b3b88bcf7be116ad5`，决定 SHA `2c0f569edd03bdbcb37f85db6944bd7f661966dea5c2721c0e7c6c378399da8a`。

## RQ1_f922252cd038

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_f922252cd038) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-39.json](Queries-39.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_c58fa03a9316)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 6}。相关检查决定 {'scope_missing': 9, 'external_dependency': 5}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 68.137 秒，模型等待 79.256 秒，真实 solver 101 次，查询投影 209 项，动作记录含缓存 254 项。诊断 {'shared_declaration_in_distinct_applied_contexts': 3, 'unrelated_or_secondary_graph_pairs_deferred': 19, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `cc70d661ec21d53d82d918bf7cbc170a0c2121b92d0c7e32c09f252e8bb11e2f`，决定 SHA `e48dabb51a8eeb79caf971b560fc810943f01dd49f36b5af4173bdfdb219c0d6`。

## RQ1_c4aeb6122521

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_c4aeb6122521) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_81b770577694)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 8, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.396 秒，模型等待 29.957 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {}。

最终报告 SHA `c3a15df6f3741cbda2597e1de405c689ae88686c04a7c923a8f25fbd224d8174`，决定 SHA `f273566d9f33cb16039bd6bd203ef232a12159da55c36679fd1f34e9c2068934`。

## RQ1_3876731c1c31

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_3876731c1c31) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-38.md#rq1_531369afb901)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_3fd2f9a68c2fae218515`，根位置 1329＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1329. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.587 秒，模型等待 23.937 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {'explicit_effect_anchor_conflict': 2}。

最终报告 SHA `61660c1772b30ad25a01fe04941ac0401aa06f7bb27f98b641a5b679c0d63a96`，决定 SHA `4295931177b2296258f05c39417c0aaf56d77af04c92b9104bd050c8e2a760f2`。

## RQ1_0c8823eed851

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_0c8823eed851) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-38.md#rq1_7ca60ff656fc)。指定类风险端未检出、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 12, 'necessary_effect_absent': 10, 'source_task_reading': 1, 'effect_range_decided': 1}。相关检查决定 {'incoming_only': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.720 秒，模型等待 27.844 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 22 项。诊断 {}。

最终报告 SHA `37f250e35fa1955003012a34b42e03d4867015fb029919168dbb22090567333c`，决定 SHA `db80e14f7b06da6057457f00e426bde5c81c92cea4359207b6065c58a48d0c35`。

## RQ1_c185f5a00faf

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_c185f5a00faf) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-39.json](Queries-39.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-48.md#rq1_1450fdff3528)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_998c61070a6d6b78c04b`，根位置 6806＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E24, E33, E34

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 67.407 秒，模型等待 34.854 秒，真实 solver 81 次，查询投影 94 项，动作记录含缓存 157 项。诊断 {'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `f5d3c952edea39fb5494bfcedc3864b557bdcaa4e17ba9fcc37ec163086ed7ce`，决定 SHA `c39d4da3c4fcd46c422da6c5c5864410c6ca3e9df0daed6b74cb5ecda3ce3e3e`。

## RQ1_ff45d949d1ec

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_ff45d949d1ec) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-39.json](Queries-39.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-35.md#rq1_c362e8ee6547)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_61c875a9c36dbcc553ec`，根位置 1446＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1446. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E10, E11, E13, E3, E4, E7, E8, E9

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.226 秒，模型等待 29.460 秒，真实 solver 13 次，查询投影 11 项，动作记录含缓存 12 项。诊断 {}。

最终报告 SHA `fd57e0ea12ea21886715b6f8773564b8e636685daaa2de8721ba06a1c860e240`，决定 SHA `6913864c70d635afa462558a1497f41fb81ad91005b49d945434cd2c1f6bf58e`。

## RQ1_0e93114762d7

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_0e93114762d7) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-39.json](Queries-39.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-43.md#rq1_4d0224e0d6e1)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_55527e5ef90f739eae29`，根位置 6851＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E13, E6

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 38.886 秒，模型等待 44.777 秒，真实 solver 60 次，查询投影 71 项，动作记录含缓存 51 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `114883d25681b3e902cdaeb02e0ac188146cdfcea3a86ac5a6cd619313d59249`，决定 SHA `6a38e943fec304e70e89052ab19af2a33860b3c7449a02007e911f26975d7b0a`。

## RQ1_b06b87a14839

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_b06b87a14839) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-38.md#rq1_a38f38fe9362)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'necessary_effect_absent': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.446 秒，模型等待 35.734 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'invalid_semantic_row': 1, 'audit_effect_unbound': 1}。

最终报告 SHA `7a4295766318ec2b8667628591de72089ad81ce197431a594637f6014e2ebe63`，决定 SHA `981d034e42fbc4f39729a3aa37ccc25e112ab6925043e4b53262af082c348881`。

## RQ1_a06d7492b7fb

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_a06d7492b7fb) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-41.md#rq1_a00b1c9a49ed)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 8, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.590 秒，模型等待 39.980 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_card_text': 1}。

最终报告 SHA `1a8576b97dde674bfde1f08e00eddab4107701cd82f2648dc6bbb78b7548c8af`，决定 SHA `64fbe8c9554f46d950f72c5567adfc6b7847abe82de2a5a347c07a19f186ded6`。

## RQ1_cd47d22b26a9

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_cd47d22b26a9) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-39.json](Queries-39.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-33.md#rq1_fa2207747d01)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_e294d04f583a73a821eb`，根位置 6091＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E13, E15, E16

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 95.205 秒，模型等待 50.209 秒，真实 solver 113 次，查询投影 156 项，动作记录含缓存 101 项。诊断 {'unbound_or_inapplicable_seed': 3, 'audit_card_text': 1, 'audit_source_scope_mismatch': 1, 'action_slice_exhausted': 1, 'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `3b8429051b6b23f86ff1eb59d8387ef2bf33431593914e27b3a02caf37ca8874`，决定 SHA `35e4035167783de586b1edce55ec72db121ce57448f2cf0685893600e811eaba`。

## RQ1_c19f5f8439d9

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_c19f5f8439d9) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-27.md#rq1_b03d4b98a481)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 2, 'no_effect_in_scope': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.157 秒，模型等待 36.307 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `aae60a94e2a88b648e50a15d9bcfd1238cd8e339ea95ae4df4152cea0d802feb`，决定 SHA `f6462696dc524019b5608dafb13cf717510f88747f2518260abcccb60ae01ca3`。

## RQ1_14d06cbbe5a7

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未知。

[实际输入](InputSource-13.md#rq1_14d06cbbe5a7) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_b25ec4a4cd43)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 1, 'no_effect_in_scope': 3, 'source_task_reading': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.080 秒，模型等待 33.753 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'explicit_effect_anchor_conflict': 1}。

最终报告 SHA `ef80058baa031b3394a43a7ae3c0e6aa7c83fe17a465f0ee768bce96d691c2c2`，决定 SHA `1d7c90adb8f3b9c51b901f67ace7ecc6e1c360bb2e4e53e1626874a725de518c`。

## RQ1_b472a9a0647e

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-13.md#rq1_b472a9a0647e) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-39.json](Queries-39.json) [Queries-40.json](Queries-40.json) [Queries-41.json](Queries-41.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_1ffb833b5da1)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 13}。相关检查决定 {'scope_missing': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 530.473 秒，模型等待 37.153 秒，真实 solver 463 次，查询投影 1050 项，动作记录含缓存 258 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 10, 'noncached_action_limit': 1}。

最终报告 SHA `796f46693c17b81794af2737f9102ebc98e6f2058580714f1f3603f5142c5cf0`，决定 SHA `bf55ed577bf0c6cd4852a3af3567a2b6aec433bd6116ff695a46dcc3b4be19b6`。

## RQ1_5b3c7cbe3d9d

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-13.md#rq1_5b3c7cbe3d9d) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-41.json](Queries-41.json) [Queries-42.json](Queries-42.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-30.md#rq1_0f3c3f400f6f)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'source_unit_missing': 2}。相关检查决定 {'scope_missing': 2}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 36.224 秒，模型等待 32.731 秒，真实 solver 83 次，查询投影 140 项，动作记录含缓存 137 项。诊断 {'audit_card_fields': 1, 'unrelated_or_secondary_graph_pairs_deferred': 10}。

最终报告 SHA `14dbb87f73ec359fa0b0edc163b3eb67a5e23294ea6954f39fccf96becf00038`，决定 SHA `32da187670f23ca0ebc334f271de72042f6457f80bb58af279cbc0129fd4775c`。

## RQ1_b649070a92c3

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_b649070a92c3) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-35.md#rq1_cd39ae0d15a5)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.136 秒，模型等待 26.224 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `a16e9072db6f37a111b3bd532b20170ae4a220785505c9dfbfe447b9ed896c6b`，决定 SHA `f0d98e6c6e6ca07f16f55c760bbdef4949377995fa8204d2219ec25b9b99e6a1`。

## RQ1_188b4ba2c3ef

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_188b4ba2c3ef) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_8d354778e2a5)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 16, 'no_effect_in_scope': 12, 'detached_local_holder_switch': 3}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.896 秒，模型等待 28.691 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `bd3b27c8fa42e35db380500e6a377b36b8823c8f392d465312879c6c5899151b`，决定 SHA `1e590ffd80e876dcc7a7e60e0d1611a18ba221a898830c1c474e327d93ec160e`。

## RQ1_35517bec1c74

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-13.md#rq1_35517bec1c74) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-31.md#rq1_cfd05c2b5a6b)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.234 秒，模型等待 53.140 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_source_scope_mismatch': 2, 'audit_check_target_unbound': 1}。

最终报告 SHA `1ece8c91cba2d781f67e9e1b6623b0cd9fc7001976f6d69a4a408b73b038de7b`，决定 SHA `ddaaadde70d9fb6682571b6ed94944a3f671df2a705031e9742ae8940e31b351`。

## RQ1_5422392a2f99

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-13.md#rq1_5422392a2f99) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-42.json](Queries-42.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-41.md#rq1_dab923cbe924)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 17, 'no_effect_in_scope': 17}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 34.675 秒，模型等待 43.420 秒，真实 solver 29 次，查询投影 35 项，动作记录含缓存 55 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `3885b9a9fe48ff1dd9739f09fc3f0925ed1bad7b7bb458f44f450415292c5ab7`，决定 SHA `f3237bb34bbb96e0062bf8713d89e664985012c61d3d89ad86d229aeecded8ba`。

## RQ1_a4881b0828b3

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-13.md#rq1_a4881b0828b3) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-42.json](Queries-42.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-41.md#rq1_440857b3df3c)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'scope_missing': 3}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 46.399 秒，模型等待 40.809 秒，真实 solver 42 次，查询投影 44 项，动作记录含缓存 111 项。诊断 {}。

最终报告 SHA `78595f64ba6b935eecf77ba96cb5827ad93cbfdd9aa1c01217a2d5f6a34295ba`，决定 SHA `cc820a7961efd689fd726f0c7cd483895a94a45bd22c4e3164e35a709b59d5a1`。

## RQ1_16adbcc82eed

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_16adbcc82eed) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-42.json](Queries-42.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_88258f6d823d)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_0af67f647f02f9827bea`，根位置 8061＋197，依据 `program_support`。At setTradeException(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E14, E17, E5

发现 `finding_b863fed4163b9f4b4ce6`，根位置 8061＋197，依据 `program_support`。At setTradeException(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E3, E9

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 14.079 秒，模型等待 22.932 秒，真实 solver 25 次，查询投影 36 项，动作记录含缓存 22 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `19bc7ea88caa7049f678fdaaf10173c58ce03ea2af1cf9387b233411ccbd4b02`，决定 SHA `cd1baf6d3b77f653e989ceeb93f9bc1c0e7175db38ddc7542d7ac2c3e7e0cf18`。

## RQ1_4530531bee57

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-13.md#rq1_4530531bee57) · 检查明细 [Checks-81.json](Checks-81.json) · 查询明细 [Queries-42.json](Queries-42.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-35.md#rq1_308738db6c81)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_a9de9e4bcbe530aeefbd`，根位置 1336＋13，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1336. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E2, E4, E5, E7

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.558 秒，模型等待 27.410 秒，真实 solver 4 次，查询投影 17 项，动作记录含缓存 7 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `84f3af81ed7c9916d76b7e237a89d2436838a42e86e0572398ee6bc3b51d6450`，决定 SHA `614a29190270b850266d0c8a55e7961d9d0979e3c7028bd02f6e1977d37d5c1b`。
