# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_b03d4b98a481

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_b03d4b98a481) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

评价端为risk，[配对成员](Cases-29.md#rq1_c19f5f8439d9)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_484c8bdb9aef709c823c`，根位置 763＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 763. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3, E4, E5, E6

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.456 秒，模型等待 35.430 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 4 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `aaf4f6bde44251f7e3a93d2952b7c1633a6ccbc583c97664d2e1f371c5802904`，决定 SHA `51ae99524ba5d04f4423a07751cfa38467bd1d5e2e33f5ceafd03641259ee490`。

## RQ1_84e7dfe8abc4

任务 FCR，评价类别 FCR-TRANSFER。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_84e7dfe8abc4) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

评价端为repair，[配对成员](Cases-47.md#rq1_431ecfc00827)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.365 秒，模型等待 54.611 秒，真实 solver 5 次，查询投影 4 项，动作记录含缓存 14 项。诊断 {'no_locatable_source': 3, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `55f9bc4d47eb6f466479b5eb37cede965410c350dff1c7fa0e2f487d9f399bed`，决定 SHA `13e925b3be5809dd5af35d374d8857e2aa4a291c366254ffcb4fbd747827fdc7`。

## RQ1_58de46f081ec

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_58de46f081ec) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-01.json](Requests-01.json)

评价端为risk，[配对成员](Cases-42.md#rq1_2046acc1c802)。指定类风险端未检出、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 15, 'necessary_effect_absent': 15, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.212 秒，模型等待 49.451 秒，真实 solver 14 次，查询投影 22 项，动作记录含缓存 15 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `621d6fb527829d70614d54f8f633523596da582c6b4512cb68a06e3607777184`，决定 SHA `9343ba2499aa0d70d5553926f29788ef2976d04d02723e09fe15bad439d95c95`。

## RQ1_328c13393c2c

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_328c13393c2c) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_d46f18d3b64e)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {'scope_missing': 7}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 30.291 秒，模型等待 65.881 秒，真实 solver 67 次，查询投影 122 项，动作记录含缓存 112 项。诊断 {'audit_check_target_unbound': 1, 'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 6, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `4f06c3f048ead8c3efda1500b32c7a07e3221d060f3794a0cb5a66475785f8f6`，决定 SHA `d4f21398c573465801bdea2c9a8bc80c8602a290e3aff8016006458dfa682d3f`。

## RQ1_bc5855a83e2d

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_bc5855a83e2d) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-28.md#rq1_770ae395781c)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_6513fed624d919274475`，根位置 13539＋737，依据 `program_support`。At mint(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E1, E20, E21, E22, E23, E4, E7, E8

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.652 秒，模型等待 22.963 秒，真实 solver 22 次，查询投影 17 项，动作记录含缓存 23 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `bc94d30c7e1e469f79df4c7671c8ace570fa46670f9dd67e331fdb29e5443fdb`，决定 SHA `22e9161eafa248161c12831379107630a2fb5b8b5972874006ca5e297f4f9a67`。

## RQ1_1ca74e3a1b5e

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-12.md#rq1_1ca74e3a1b5e) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-48.md#rq1_68cdf0f21f76)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_99be8857edde17ffb3b5`，根位置 1046＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 1046. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E5, E6

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.598 秒，模型等待 51.777 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 8 项。诊断 {'unbound_or_inapplicable_seed': 3, 'invalid_semantic_row': 2, 'audit_effect_unbound': 2, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `d2d72d17578b25f28e5838a9881253b6947087e7ba663e46bd9aab9f71f0e0b7`，决定 SHA `5a52d14c7cc580adab94e08c58230138489ea01018f29694952fa01e036575d4`。

## RQ1_1f932eab663d

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_1f932eab663d) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-43.md#rq1_43103f5773b9)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_135ec9841e1a9dd781a1`，根位置 8128＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.670 秒，模型等待 12.889 秒，真实 solver 4 次，查询投影 4 项，动作记录含缓存 3 项。诊断 {'explicit_effect_anchor_conflict': 2}。

最终报告 SHA `62b7bc765f9598c6e1db9ae26c941cfd39f60493ff325b143b5a4fd95c822d89`，决定 SHA `af3a7d83efa93f93538772e391ec2a934999b958e81f38944672773ae357f579`。

## RQ1_1c369a1de4e8

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_1c369a1de4e8) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-28.md#rq1_e5cc8c6eec49)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_77039abcc584a77c096d`，根位置 2165＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2165. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3, E4, E5, E6, E7, E8, E9

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.132 秒，模型等待 52.049 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 5 项。诊断 {}。

最终报告 SHA `4c83494aa35352ec30cffabb9b3a6e14b282cdfa3a602852cfc0a2d6c0d594d8`，决定 SHA `36b2968236bc3e727f7b3a1f48410886ea5360e66821765ae877c606940b2274`。

## RQ1_0858684eb758

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_0858684eb758) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-42.md#rq1_3ec097691998)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_01149cbf06aadbc5c73b`，根位置 6654＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6654. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 38.757 秒，模型等待 57.185 秒，真实 solver 59 次，查询投影 71 项，动作记录含缓存 51 项。诊断 {'missing_claim_or_source_anchor': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `11cfacf16131f4275871ec5e08dccb546ed05f69e96bc7a62b3c846bbb0b73e1`，决定 SHA `c3594995eef0071741e8966d84cfd1e003babd790cc3cc399fa17b845eeae7fd`。

## RQ1_f27cacd5f34a

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_f27cacd5f34a) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-42.md#rq1_56bac052a93a)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 158.456 秒，模型等待 55.917 秒，真实 solver 333 次，查询投影 211 项，动作记录含缓存 11 项。诊断 {}。

最终报告 SHA `b9e7792b716f9533910c9be292a165b404d23e7b63f63143c5cd34bbd5669a3d`，决定 SHA `753d79050fa966577a558e10fa8c0aadcf72baeb47d2b096bef9a5ae45c35852`。

## RQ1_4a9d5241617f

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_4a9d5241617f) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-37.json](Queries-37.json) [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_7cfdf5697377)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {'scope_missing': 1, 'external_dependency': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 529.154 秒，模型等待 64.605 秒，真实 solver 91 次，查询投影 161 项，动作记录含缓存 147 项。诊断 {'audit_source_scope_mismatch': 1, 'action_slice_exhausted': 7, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `a94b424b4deb30d4f39cf641baf5e666f275076a62dd7345047369a1372c48a2`，决定 SHA `2c86e78a95a5bd3796bfb8252e23a4b27725f3e09a9cef9c26375a3bf579dfae`。

## RQ1_2fde609553be

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_2fde609553be) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-41.md#rq1_cac16ccd972b)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 1, 'source_check_excluded': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.879 秒，模型等待 39.035 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 14 项。诊断 {'audit_card_text': 1}。

最终报告 SHA `bc0843be731da1248a55ecdf3ff107f454f975d3de477570206628a3827181b5`，决定 SHA `ba3db6577386078ba7794895526b9aba199837fa5282d87d45e60f2900ae01d9`。

## RQ1_92a10a0592ae

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_92a10a0592ae) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-34.md#rq1_d6eec0ddeec9)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 3, 'necessary_effect_absent': 1, 'no_privileged_intervention': 1, 'source_task_reading': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.081 秒，模型等待 49.990 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `51b1f157147fed0edb7bcd37f77f7b4bcf21117a91dbfdd6f9fe3f41ec222e9e`，决定 SHA `989ffcd29aff5d39dfe932b9b75bee65404e62f7f8695d002bddfd3f16a87e68`。

## RQ1_c66d7fc7441b

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_c66d7fc7441b) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-43.md#rq1_eb7101bcaf57)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_1fad21378b68b2e14a05`，根位置 755＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 755. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3, E4, E5, E6

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.431 秒，模型等待 33.584 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 4 项。诊断 {'missing_claim_or_source_anchor': 3}。

最终报告 SHA `80a9e6f5144526dec162c48fdfbfed3a9c942b7a53ca70cd451d33cfd69f9c3f`，决定 SHA `5c03e2f9bd0785634784e09f6cc6a52b4642712d3637b25eb592de7a4262d627`。

## RQ1_be34c834fd22

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_be34c834fd22) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-27.md#rq1_0322a88dff3d)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.057 秒，模型等待 37.674 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `1f8a63e4d8b63b6ebe153b204bd0e9a442bb83a36b588741dc4d69bf5f52edc9`，决定 SHA `154be1cc1514cf0bd05ecd5f03abb15c406b6cde9f0f3ad4298ea42781bd1dee`。

## RQ1_2ef6e8719d06

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_2ef6e8719d06) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-48.md#rq1_28b8d1e3b59b)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_ea461201ac6122b6bec6`，根位置 3184＋14，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 3184. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E2, E4, E6, E8

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.009 秒，模型等待 24.788 秒，真实 solver 6 次，查询投影 10 项，动作记录含缓存 7 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `c8bfe0c8ae5d86d75822da9b84572d66e056f5602c688817b8e6007ad980b2b3`，决定 SHA `c0e7d3d34382b52192892ab2853cbad5f6fbe69ff9446a1a8a9c88bcb22e3608`。

## RQ1_63ed6120bd80

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_63ed6120bd80) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-35.md#rq1_239dec1e19b3)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.714 秒，模型等待 30.300 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_source_scope_mismatch': 2}。

最终报告 SHA `27f7363410e52a5abc92e2f96ede725e34708d4b7b0f76f0c4f18e5978ea893d`，决定 SHA `008ffbad52c62ba07c4bfbb3c9134a763efcc76f65870183cb8f0633170c6a15`。

## RQ1_1b0307d85594

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_1b0307d85594) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-43.md#rq1_f233c826784d)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.723 秒，模型等待 21.473 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `b6f151bfde00d7745cba8c5d6255f4c21496355e5b29b2c76914eb8dfa9bf6ab`，决定 SHA `958279e81ea307dfdd0f8e0545c6ef731bb138c6a1f549ab2297bc21512059cd`。

## RQ1_405dd133e380

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_405dd133e380) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-40.md#rq1_89bac12a4446)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 6, 'source_task_reading': 4, 'necessary_effect_absent': 2}。相关检查决定 {'scope_missing': 4}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.942 秒，模型等待 26.216 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 21 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `4cab5ed3c68711a117b52744e1c95927068e84ba244b9910bf103deb745b707b`，决定 SHA `4c4708aed0238400beebe3fa96b3dc30c17368ed2b964fe9c74e592e587640dd`。

## RQ1_81a85f242b60

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_81a85f242b60) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-42.md#rq1_b61f163309a1)。指定类风险端报警、修复端报警，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_eccf677cbe68eb8968c5`，根位置 5099＋361，依据 `program_support`。The change at setTokenExchangeRate(uint256) affects the same holder request at fallback(). The checked difference is a new positive entitlement for a controlled beneficiary. 证据 E1, E10, E13, E14, E15, E18

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.603 秒，模型等待 22.426 秒，真实 solver 22 次，查询投影 17 项，动作记录含缓存 16 项。诊断 {'explicit_effect_anchor_conflict': 3, 'no_locatable_source': 1}。

最终报告 SHA `7b193a60a972defc3a56401c817ea05d4b0e233afe39fa2dcbb691075baaa956`，决定 SHA `ffd0adea12174c93769c86775d31679a114cf56d7e696ddab10b8ad3d31a917e`。

## RQ1_6af8dad9e222

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-12.md#rq1_6af8dad9e222) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_a9742b3414d8)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 1, 'source_check_excluded': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.928 秒，模型等待 31.845 秒，真实 solver 9 次，查询投影 12 项，动作记录含缓存 31 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `d7925374ff85a93d3516b99fa2d7f1ce1c4e9aab09f6022a4fa416b4e0b275a1`，决定 SHA `749d3dd6db3d96c1bc97a834b2af8871eaf0df9e841558177befb92b186a4779`。

## RQ1_237ffc6da6a2

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-12.md#rq1_237ffc6da6a2) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-42.md#rq1_45f5c9057f72)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_d6d52af8f1b5b236a723`，根位置 990＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 990. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E7

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.797 秒，模型等待 46.142 秒，真实 solver 6 次，查询投影 4 项，动作记录含缓存 17 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `40abe920a30f8164ee284760c32659c890ed0cb711dee7f5ec7483c7f1cc16e6`，决定 SHA `1ec912f4e4f10125590d4b229efdf340b39b99353da098a9e013dbc0d2f2523b`。

## RQ1_dc9919de5e46

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-12.md#rq1_dc9919de5e46) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-31.md#rq1_24939507ecba)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'necessary_effect_absent': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.463 秒，模型等待 36.266 秒，真实 solver 4 次，查询投影 3 项，动作记录含缓存 12 项。诊断 {'audit_effect_unbound': 1}。

最终报告 SHA `8533785f07b4af32e3768d8d0af7975118d280c0e98302da0ab5abc47274f992`，决定 SHA `a0b50c1bcea61c58aeeaabfbe34c3f60118f7cbc95206b01367533831ea3cd65`。

## RQ1_0322a88dff3d

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-12.md#rq1_0322a88dff3d) · 检查明细 [Checks-80.json](Checks-80.json) · 查询明细 [Queries-38.json](Queries-38.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-27.md#rq1_be34c834fd22)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_a9752c7390dd67f01363`，根位置 6580＋30，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 6580. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E17, E19, E20, E21

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 28.122 秒，模型等待 43.293 秒，真实 solver 80 次，查询投影 100 项，动作记录含缓存 94 项。诊断 {'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 4}。

最终报告 SHA `a51929051770caf1a133ed7e551145a8ef9aa3f7791b29ef8a54e4c356704d21`，决定 SHA `f5c26eff73000b438300191b2b793dea4b39a45e76caaba0a0ae369a70fbea4b`。
