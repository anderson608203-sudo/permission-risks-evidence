# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_db90e8d965d3

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_db90e8d965d3) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-35.md#rq1_4bd496781767)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 11, 'intra_ledger_transfer': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 16.472 秒，模型等待 29.187 秒，真实 solver 16 次，查询投影 16 项，动作记录含缓存 129 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `3cc6ddf9d6b7f47f5af14a47c3d39474ab28f8f0f41071a0eb3d48b9844ef1b7`，决定 SHA `784a63ef7b5570987c874f0bbb30e5b6be2a25fd31ba57f37e913bd55d39a201`。

## RQ1_868296d21a79

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_868296d21a79) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-46.md#rq1_107e84e04a84)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_b8b0716467906eaf1ab6`，根位置 1448＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 1448. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.429 秒，模型等待 30.808 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'explicit_effect_anchor_conflict': 1}。

最终报告 SHA `025fe014980aa7734172e10929fb1878a2719081cc0c6c505c657aff061ed179`，决定 SHA `aa5396dbac51cc45ac24362f95dd6358daf18ebb4ea10427a15821eaf393712f`。

## RQ1_085aaca2f412

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_085aaca2f412) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-31.md#rq1_c9626779c857)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 8, 'no_privileged_intervention': 2}。相关检查决定 {'scope_missing': 5}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.104 秒，模型等待 36.920 秒，真实 solver 3 次，查询投影 3 项，动作记录含缓存 35 项。诊断 {'invalid_semantic_row': 1}。

最终报告 SHA `63da19980f922477a01c5db07305d94f6864741566ad6e445bd93699564bdf8e`，决定 SHA `fae215e71d24e4e9e77587b6433a6083142113cd863642a5951d4f0b94e60dbf`。

## RQ1_c362e8ee6547

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_c362e8ee6547) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-29.md#rq1_ff45d949d1ec)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 5, 'necessary_effect_absent': 5}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.157 秒，模型等待 26.559 秒，真实 solver 9 次，查询投影 12 项，动作记录含缓存 38 项。诊断 {'unbound_or_inapplicable_seed': 1, 'unrelated_or_secondary_graph_pairs_deferred': 3}。

最终报告 SHA `b22f99ef372f77602dc439bd9bc6ba57d474f261628968ee4e35d7eb728b9cb8`，决定 SHA `5c565c4fd6fe9c1607f6b6e1fed1945c9961fa8fdfc8db221244c2881714b806`。

## RQ1_97348d96a47c

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_97348d96a47c) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-36.md#rq1_520f22bfdd09)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.885 秒，模型等待 25.957 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `121ce6a0dbc59fe137ced5f1e99be2a46b4a6faf87693f98a5d6ddeb93602a70`，决定 SHA `154be1cc1514cf0bd05ecd5f03abb15c406b6cde9f0f3ad4298ea42781bd1dee`。

## RQ1_cd39ae0d15a5

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_cd39ae0d15a5) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-29.md#rq1_b649070a92c3)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_b8c2c2971ac4fc3a1566`，根位置 3584＋14，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 3584. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E3, E6, E8

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.058 秒，模型等待 35.198 秒，真实 solver 6 次，查询投影 10 项，动作记录含缓存 7 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `fa0de412aaa12d12456feeb9e831bcbde284eeefc82219d542ba48432da4f43b`，决定 SHA `7d61b08b7eafd3d634310d96853bc9d37e77ad2329f48d9744fb792952a95154`。

## RQ1_507e0efe86f1

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_507e0efe86f1) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-34.md#rq1_f529b424392d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 4, 'necessary_effect_absent': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.404 秒，模型等待 50.191 秒，真实 solver 3 次，查询投影 3 项，动作记录含缓存 4 项。诊断 {'missing_claim_or_source_anchor': 1}。

最终报告 SHA `41e8fb8c1e77aecb3b2d311d4175a826fca68979a6effbe5ded628aa9bfd2177`，决定 SHA `51a6e00d0d31393a2b50ab648cfb1a917fa9a8252fdeba1c8e446602c7c7f0e0`。

## RQ1_39821973be02

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_39821973be02) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-28.md#rq1_bf35b402b6c4)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_365834668fd09034b0b1`，根位置 2925＋31，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 2925. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E10, E12, E2, E3, E4, E5, E6

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.261 秒，模型等待 31.312 秒，真实 solver 9 次，查询投影 9 项，动作记录含缓存 8 项。诊断 {}。

最终报告 SHA `f3787d03a6fc60bf95c0063c3575a720435b9805aad71fba029a61106c191295`，决定 SHA `b988babdc0187f38501f1430a0d714ed7dee2136533324266aa5563a26f92424`。

## RQ1_34d982d4a91f

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_34d982d4a91f) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-49.json](Queries-49.json) [Queries-50.json](Queries-50.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-39.md#rq1_d1e5e262ff31)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_1d58dd15608decf2f5cd`，根位置 2636＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E16, E19, E5

发现 `finding_99937e87d30e747b68ae`，根位置 2636＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E13, E15, E3

发现 `finding_7c899e0bc2c333c66781`，根位置 2636＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E21, E24, E8

发现 `finding_c5fc5583f21aa49d668a`，根位置 2636＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E1, E18, E20

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 117.817 秒，模型等待 19.101 秒，真实 solver 586 次，查询投影 455 项，动作记录含缓存 44 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 7}。

最终报告 SHA `43472e1aaf9654d8cc47f89a8ccebc32fff23523b20c967bacaa4744ae8bb03a`，决定 SHA `9e4edb1a7354d07eac36df3bfbdc318993d102cff9e74038a4a5752a00850b5c`。

## RQ1_c0126467dbc0

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_c0126467dbc0) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-50.json](Queries-50.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-37.md#rq1_4e3600087174)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_bceeee2089caffa77422`，根位置 3429＋14，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 3429. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E22, E24, E28, E30

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.400 秒，模型等待 30.773 秒，真实 solver 9 次，查询投影 13 项，动作记录含缓存 82 项。诊断 {'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `3e51278c52d8607e6cb670af1746d61c1bb4efc1a6bc03492f6c75c9a6712867`，决定 SHA `08c28d41dd8e49e602138e751b253aa7c2839fae85e8cc4600c9d4549eb03ab3`。

## RQ1_10c0d8b7db85

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_10c0d8b7db85) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-50.json](Queries-50.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_5d5acefd82bd)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_2d0138725fd329892a05`，根位置 5496＋30，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 5496. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3, E4

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.643 秒，模型等待 24.347 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 4 项。诊断 {'audit_effect_unbound': 1}。

最终报告 SHA `ab91ea0c07f2a97a884e999d677da4e663e7a109f1f021930be6b5014d899fff`，决定 SHA `64351160bdafbb915934f959fbfb580d6e02873ba9568a8e31dfc7af9816b749`。

## RQ1_c2a474194a28

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_c2a474194a28) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-50.json](Queries-50.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-46.md#rq1_11a74fb21495)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_be3448707394b0c39433`，根位置 791＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 791 under transfer_condition. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3, E4, E5, E6, E7, E8, E9

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.365 秒，模型等待 38.806 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 5 项。诊断 {'unbound_or_inapplicable_seed': 3, 'explicit_effect_anchor_conflict': 2}。

最终报告 SHA `c08c9b7e2dcfcfade8ea31ee293f962869cd597b0f6df18e961c8e40a46f5359`，决定 SHA `ec40fe5f03ce258e4cb708803f0167310503ed77d984329e8df5c7936b0f0e93`。

## RQ1_4bd496781767

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_4bd496781767) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-50.json](Queries-50.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-35.md#rq1_db90e8d965d3)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_f4a8f969d5fe4cf2c142`，根位置 3970＋34，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 3970 under financial_right. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E21

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 21.802 秒，模型等待 24.561 秒，真实 solver 25 次，查询投影 26 项，动作记录含缓存 133 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `2acb45d629bd7c80f57112ae684da4c1cda1d1a96bee238c453bac0457468a79`，决定 SHA `5f902e898aed39152925c3bfe2df36b26bd83a9b98268724e91e371ef2eb91e6`。

## RQ1_308738db6c81

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_308738db6c81) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-50.json](Queries-50.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-29.md#rq1_4530531bee57)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 1}。相关检查决定 {'scope_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.962 秒，模型等待 35.079 秒，真实 solver 3 次，查询投影 16 项，动作记录含缓存 5 项。诊断 {'audit_source_scope_mismatch': 2}。

最终报告 SHA `53bfae5ff82ea70e6553403c056f1d4fde522c23f135e812b5e13657fef0c7fe`，决定 SHA `deae7dbef6d51775da4dd293ad1b48f3d4c6ee8481b44f693f63abc2dfd4551a`。

## RQ1_c3bf1a81ff5a

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_c3bf1a81ff5a) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-50.json](Queries-50.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-43.md#rq1_684f1de50e1a)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_9ab9d3e4d21b718198ac`，根位置 12758＋746，依据 `program_support`。At mint(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E1, E17, E21, E22, E62, E63, E65, E66, E68, E69

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 12.725 秒，模型等待 24.404 秒，真实 solver 29 次，查询投影 30 项，动作记录含缓存 65 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `0493ae632e177bf814a53a112abf2795537c5633a52a6db758a7fc73c5756c4e`，决定 SHA `3bfa04bb187b1b5dba126ccc199f04147ab461d3cb50a00ae752bbe5e4d26263`。

## RQ1_6654889e07a0

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_6654889e07a0) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_cb170330826d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_7a6a4c059313321395ef`，根位置 679＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 679. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E2, E3

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.109 秒，模型等待 31.440 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `4355d43cb92248de4421c794bd62791ef15de2ae9d980cad17f6e57ff1034938`，决定 SHA `210117a7c951875c3a866506292a3a50a4b8a44d3ae206173bd6b3f0ca593850`。

## RQ1_4fb4fc48389a

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_4fb4fc48389a) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-30.md#rq1_ce670e623911)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 8, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.289 秒，模型等待 35.746 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_card_text': 1}。

最终报告 SHA `cb79f0bba8527f93e0e984d8856892e07c62bb6be9cff75ed60b7526b91d36a8`，决定 SHA `c56b320181889b512107a85d7516be44e7ee2e9802d8ac7a63b8e0f300e5a6e8`。

## RQ1_2b2d929cbd84

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_2b2d929cbd84) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_c3d569994373)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 8, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.476 秒，模型等待 25.533 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'audit_source_scope_mismatch': 1}。

最终报告 SHA `feff6eb19e0a7eabe5e917a0489f3ee4cca60974effb17989b466aa28316efec`，决定 SHA `1567a37b85835f3382abb67b4e020da0043877d86674a92cd514bbf986f01008`。

## RQ1_eb30c6dee989

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_eb30c6dee989) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-50.json](Queries-50.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-36.md#rq1_ee2aa7f32d31)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'voluntary_holder_debit': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.618 秒，模型等待 31.175 秒，真实 solver 33 次，查询投影 34 项，动作记录含缓存 13 项。诊断 {'no_locatable_source': 3, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `ad2e7f4ed5d4d9650ceb6b88d22094fcc469eddb37dbd2d2721b9ded72439840`，决定 SHA `f06d3fee7932d5590ca95b0b393e8f1c5c566d271d05749844505594e85fbbbf`。

## RQ1_239dec1e19b3

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 未知。

[实际输入](InputSource-15.md#rq1_239dec1e19b3) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-50.json](Queries-50.json) [Queries-51.json](Queries-51.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-27.md#rq1_63ed6120bd80)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_33158cd2a924b13fb23d`，根位置 2417＋25，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2417. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E13, E14, E51, E52

发现 `finding_bea9dae0764dfd0211e8`，根位置 2417＋25，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2417. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E16, E35, E36

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 915.620 秒，模型等待 43.199 秒，真实 solver 1098 次，查询投影 1016 项，动作记录含缓存 38 项。诊断 {'action_slice_exhausted': 11, 'program_investigation_seconds': 2, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `22d66c31590702ede2f09cd21316a986816575c3e839d6807d7350c8df55101c`，决定 SHA `092194793b4a0e09bc56a9ecd017815f35f5cc7ab0d863de965a0628ca355bed`。

## RQ1_c339d6f50fb1

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_c339d6f50fb1) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-51.json](Queries-51.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-31.md#rq1_b586561de97d)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → feedback 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {'external_dependency': 2, 'core_mismatch': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.800 秒，模型等待 91.791 秒，真实 solver 5 次，查询投影 4 项，动作记录含缓存 54 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `e2babd8fba907fbcdd1a3f476f3ec471c5ac0115d2ad8d8c0ecdb8d33148f40c`，决定 SHA `bfde448659f966fb3e8bce709ee3f9924748c96d7c0073fa5567f04c6784dfed`。

## RQ1_791eea9e8073

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_791eea9e8073) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-51.json](Queries-51.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-33.md#rq1_e6b597ab2090)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_998c61070a6d6b78c04b`，根位置 6806＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E11, E13, E6

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 59.439 秒，模型等待 41.333 秒，真实 solver 62 次，查询投影 74 项，动作记录含缓存 51 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `bbe2f836645bd4258642378b63faab7cbbfebecae019f3c5ffc93012be947ca4`，决定 SHA `d39ed937006bdb78f4d42907dc705b5b764665f26ce744acea83498bfcc01a17`。

## RQ1_09fe8189c73d

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_09fe8189c73d) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-51.json](Queries-51.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_d6bdc291eeef)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_fce2cdd213f1b383a0cc`，根位置 9065＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 9065. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 54.192 秒，模型等待 27.220 秒，真实 solver 60 次，查询投影 71 项，动作记录含缓存 51 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `5f4f453ae9dad5e656e1a2bb9b869c5cba7c7dcfa96b8d24bcb2505fb54e317f`，决定 SHA `6f4c8e01cb17ac7173138eb8b488f3ecae46102a4e35a99a6fdb9ce0253da5e5`。

## RQ1_21bd6c31d928

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_21bd6c31d928) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-40.md#rq1_a2b01dab39e2)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 36, 'necessary_effect_absent': 27, 'detached_local_holder_switch': 8}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.974 秒，模型等待 40.628 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_card_issue_kind': 1, 'audit_source_scope_mismatch': 1}。

最终报告 SHA `69badd8eaacea17deb360c574aaf2eafe2fe28b1e233a274a5d21702c27ff32a`，决定 SHA `23d4d9862b5432de2199a826b2753792cee33a672febd528226f8c05537786d1`。
