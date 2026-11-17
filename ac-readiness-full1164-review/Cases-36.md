# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_128716025193

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_128716025193) · 检查明细 [Checks-83.json](Checks-83.json) · 查询明细 [Queries-51.json](Queries-51.json) [Queries-52.json](Queries-52.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-44.md#rq1_4e90985cd65a)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_969d5b054cb4f494ff6d`，根位置 10770＋32，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 10770. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E12, E14, E16, E17, E9

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 900.237 秒，模型等待 17.181 秒，真实 solver 352 次，查询投影 266 项，动作记录含缓存 32 项。诊断 {'no_locatable_source': 1, 'action_slice_exhausted': 14, 'unrelated_or_secondary_graph_pairs_deferred': 3, 'program_investigation_budget_exhausted': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `fcf67a149c500124b2ad92258f6e71436121566f7a23685e5ee9b6b755c40ad3`，决定 SHA `f67bd8b12744c2317679fb80918bc55db5cfdce37e9fc946f29abc45628489b4`。

## RQ1_e13bb6580d65

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_e13bb6580d65) · 检查明细 [Checks-83.json](Checks-83.json) [Checks-84.json](Checks-84.json) · 查询明细 [Queries-52.json](Queries-52.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-29.md#rq1_94d9f2cfc77c)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_5e2e2c764e0f932c4ebd`，根位置 12463＋710，依据 `program_support`。At mint(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E1, E10, E30, E31, E32, E33, E35, E36, E5, E9

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.545 秒，模型等待 26.629 秒，真实 solver 24 次，查询投影 24 项，动作记录含缓存 33 项。诊断 {'missing_claim_or_source_anchor': 3, 'no_locatable_source': 2, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `eb4cbc5d354200452e0773dd88cd0eb55fec07e4bbdddc424063f758225cabf4`，决定 SHA `5fb83f3af055c1d5f5bded19218f2b2c5d0e8e2f6fcf5a744f8649d57b0919c7`。

## RQ1_2082ab99d930

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_2082ab99d930) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-28.md#rq1_815bdde1a02e)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.172 秒，模型等待 59.370 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'missing_claim_or_source_anchor': 3, 'no_locatable_source': 1}。

最终报告 SHA `c936ed0f0a017bfc53f8f93f4a0edf690fed3c5a6a463a1af179ef9ba44a877e`，决定 SHA `259c809cd44f14289264c10732ceca521b342fca4243b9331902b2470d358af4`。

## RQ1_805b30020e56

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_805b30020e56) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-41.md#rq1_23abf434df32)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 15, 'necessary_effect_absent': 14, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 6.550 秒，模型等待 30.225 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `81ca3dc5481078f182fd21a0723ef487fe361b85144cd80e50790b10a260ee60`，决定 SHA `07b4ffac0ad9ad40dd9e126fd134a732823b4af2c81801870bddcc6db4e265f9`。

## RQ1_169fab614926

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_169fab614926) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-37.md#rq1_25fd2b7278c4)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'no_privileged_intervention': 1, 'necessary_effect_absent': 1}。相关检查决定 {'source_check_excluded': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.060 秒，模型等待 29.825 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {}。

最终报告 SHA `d972a2fd280bd0ff80a5412ebd62118dcb459a1fa8609a91cd494cbcb384b15c`，决定 SHA `90979972e03e6f7089ab07157219071099f6e763dc6709b7dfa57d82235c2582`。

## RQ1_b6a39de5a1bc

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_b6a39de5a1bc) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-48.md#rq1_907fc6f2c1f4)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'necessary_effect_absent': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.149 秒，模型等待 49.002 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `1320a91ef080104eaa07a609937358fccd6ad335defb3e7c5055bdbe92efced9`，决定 SHA `23fef933b47ce178329d85b0ede77d7092f25ad8b4e9d6276f748d016b42add2`。

## RQ1_0d67d852c850

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_0d67d852c850) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-52.json](Queries-52.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-34.md#rq1_45fa9e84e0d6)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 9, 'necessary_effect_absent': 4, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.114 秒，模型等待 31.307 秒，真实 solver 11 次，查询投影 12 项，动作记录含缓存 29 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `2abee0c682bb36e88513124f33b37929428423ea881fdcd9680f0ddb22b75181`，决定 SHA `05f2e4bd7bbffd928a4e801fb4530bea3f895935e5c793394569ec5c1e18c90a`。

## RQ1_7b9a317c57e5

任务 FCR，评价类别 FCR-TRANSFER。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_7b9a317c57e5) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-52.json](Queries-52.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-41.md#rq1_cae7abe2d02e)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 28.894 秒，模型等待 19.057 秒，真实 solver 41 次，查询投影 15 项，动作记录含缓存 5 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `14abf76e2d2379f4f6f4b1e082b048779dce022edbaa601bebf1a0a7b827098c`，决定 SHA `5051caa44360ead57e05101cf2ead1bcac1c317b05a0f6805c439eb7cb02d098`。

## RQ1_4096ba758662

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_4096ba758662) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-52.json](Queries-52.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-40.md#rq1_7ac0cdbee968)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_df1975f2ed02c0ef0b0c`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E18, E33, E35

发现 `finding_73613d762a73d2aa7e49`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E21, E36, E38

发现 `finding_83f82e0ed7b950a15333`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E22, E39, E41

发现 `finding_0c091dbc07e304fd47f8`，根位置 2547＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E16, E31, E32

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 26.422 秒，模型等待 24.508 秒，真实 solver 113 次，查询投影 111 项，动作记录含缓存 63 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 10}。

最终报告 SHA `02ed43fc4214be409229e42144fa529689e961bc7462470ec45d3e9e9e72ab10`，决定 SHA `f94860fd4358e2a6875700506d81eff6d4525414b7293da5ffa621db198680d8`。

## RQ1_c58fa03a9316

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_c58fa03a9316) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-52.json](Queries-52.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-29.md#rq1_f922252cd038)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 4}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.278 秒，模型等待 42.186 秒，真实 solver 16 次，查询投影 16 项，动作记录含缓存 10 项。诊断 {'missing_claim_or_source_anchor': 1}。

最终报告 SHA `0b1d177c8b7c842323779ed41cbc3bd0f7284f88421eb85dfab8db59458fc39d`，决定 SHA `d1b868694df1495536c46f9401597fa79a7cd49805c21bb71f2aba81ec6e3c17`。

## RQ1_520f22bfdd09

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_520f22bfdd09) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-52.json](Queries-52.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-35.md#rq1_97348d96a47c)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_d4df930dad45f5790f7a`，根位置 5584＋502，依据 `program_support`。The change at burnFrom(address,uint256) affects the same holder request at mintToken(address,uint256). The checked difference is a new positive entitlement for a controlled beneficiary. 证据 E101, E102, E103, E109, E110, E2, E35, E44, E47, E49, E51, E54, E7, E94, E95, E96

发现 `finding_6a9aae51c289caaf720b`，根位置 6092＋333，依据 `program_support`。At mintToken(address,uint256), the checked privilege permits positive additional rights for the controller or a beneficiary it can select. A balance increase for an independent ordinary buyer alone does not satisfy this condition. 证据 E13, E26, E27, E58, E59, E64, E65, E83, E85, E89, E9, E90, E92, E93

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 27.572 秒，模型等待 32.710 秒，真实 solver 80 次，查询投影 100 项，动作记录含缓存 94 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 4}。

最终报告 SHA `45107102ff50c2a8df7c1c4e118ea18ade148f0f60e9acee32a67187045dd5ff`，决定 SHA `f5c26eff73000b438300191b2b793dea4b39a45e76caaba0a0ae369a70fbea4b`。

## RQ1_290892078b6a

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_290892078b6a) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-52.json](Queries-52.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-39.md#rq1_1105ef7570ba)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 8, 'no_effect_in_scope': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.343 秒，模型等待 24.009 秒，真实 solver 2 次，查询投影 3 项，动作记录含缓存 3 项。诊断 {'invalid_semantic_row': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `b80b10d33e5049290a49e70b32ba340e91defb21f43aa59a8608ff6415e94ca0`，决定 SHA `bd850a0182aa140ef5ada1b4304ea847f93c70a6e7507958c535ec2512286105`。

## RQ1_1f06ce07140f

任务 FCR，评价类别 FCR-TRANSFER。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_1f06ce07140f) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-34.md#rq1_e73c99ca23e5)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {'scope_missing': 4}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 9.206 秒，模型等待 38.288 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 21 项。诊断 {'audit_effect_unbound': 1}。

最终报告 SHA `f2e398ffa1ac93ed80f5823b2faf2a9cd6758a337db80d4b727282eee7e10a0c`，决定 SHA `25510eab313e0018932532473f86b8d785c8b54a711f8723d440fdce1584d90a`。

## RQ1_726c2d2932a1

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_726c2d2932a1) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-33.md#rq1_884d05d552dd)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.762 秒，模型等待 33.535 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `3e16db66da8b2411fbb6b5f87e0a70ae68bc4bcf6073ec7862cd389ac7ac3dbd`，决定 SHA `40e8706b84f679f2f7d7238dd74026e24b35848ce61e4cbe346d5fff5fe63b48`。

## RQ1_01a30be11868

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_01a30be11868) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_1b9c7ecc28f8)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → feedback 报警 → report 报警

发现 `finding_231055481def6eca8c20`，根位置 1283＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1283. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E3

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.377 秒，模型等待 47.692 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 3 项。诊断 {'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `8889df546242326c336840b0b4e587627d87e3dccf7b3c35972147ccca0152a4`，决定 SHA `ce5598dc97e01e55307995a923584b341a299579ba55ec85b9109097e6f3a4e6`。

## RQ1_ee2aa7f32d31

任务 FCR，评价类别 FCR-DESTROY。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_ee2aa7f32d31) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-35.md#rq1_eb30c6dee989)。指定类风险端未知、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 2}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.817 秒，模型等待 44.187 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `3cf340a2f79980f3f2cd2c130d231a0b28cd04c5ca12153d662362621c05ea8d`，决定 SHA `70a86d44da7911c653eac3c8820db441199ab5689d96528169006fcd81a288ba`。

## RQ1_4f69da2661f7

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_4f69da2661f7) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-52.json](Queries-52.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-33.md#rq1_6240ab1de377)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_b096c33bf4f572d637a2`，根位置 6388＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6388. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 49.322 秒，模型等待 52.297 秒，真实 solver 60 次，查询投影 71 项，动作记录含缓存 51 项。诊断 {'missing_claim_or_source_anchor': 3, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `6d28bebca081dc2889ad090e08a5fecd3bce3667979b373dfbea52f70884ab08`，决定 SHA `d7fbebad3fc8f2c97525ccbb74dbfb780f10790848f855053ee71e448f813466`。

## RQ1_983137cbe5d6

任务 FCR，评价类别 FCR-MINT。当前未知，BG 未知。

[实际输入](InputSource-15.md#rq1_983137cbe5d6) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-52.json](Queries-52.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-31.md#rq1_18c85d7f1380)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 3}。相关检查决定 {'external_dependency': 1, 'intra_ledger_transfer': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 42.008 秒，模型等待 42.358 秒，真实 solver 45 次，查询投影 51 项，动作记录含缓存 107 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `af7e45326971d5d5514c9968f27e72c4d5da39eebe5f648d5ef9580c20092b4c`，决定 SHA `d12f70474a39ea0d02199829c964fdc456f675473d2c131f26bf2f976b64505e`。

## RQ1_8b6fb0a7e2ec

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_8b6fb0a7e2ec) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-52.json](Queries-52.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-42.md#rq1_67214f5ba58d)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_531dfbab0858f5facbb9`，根位置 7937＋228，依据 `program_support`。At freezeAccount(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E22, E23, E24

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 138.242 秒，模型等待 67.354 秒，真实 solver 89 次，查询投影 98 项，动作记录含缓存 165 项。诊断 {'action_slice_exhausted': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `2beb1c7c1a8e948fdd41f02e533d91ec73ce9642cd33b6ab3da4d41fd36556c2`，决定 SHA `78ec203ea0c8df7fa35bbb3e1f19999bd638f3999366a3794e7cfb4b2e24e063`。

## RQ1_18b83e12ea1f

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 未知。

[实际输入](InputSource-15.md#rq1_18b83e12ea1f) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-52.json](Queries-52.json) [Queries-53.json](Queries-53.json) [Queries-54.json](Queries-54.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-45.md#rq1_9b3403bc5e3b)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_a5dd37e7f04f07fcfb8a`，根位置 2423＋25，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2423. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E22, E23, E26, E4

发现 `finding_6da932bd511943a4f0cd`，根位置 2423＋25，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 2423. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E14, E15, E2, E8

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 900.238 秒，模型等待 37.605 秒，真实 solver 1075 次，查询投影 946 项，动作记录含缓存 26 项。诊断 {'no_locatable_source': 1, 'action_slice_exhausted': 7, 'program_investigation_budget_exhausted': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `07c6b752093562aa2f91609e7d10bf62696c6cb64bce75732b4467d3b9398a43`，决定 SHA `5686cfb8485561a2a0f0818791b1f8156f28edcc7d3a9c74dc7d0af01fa20ea4`。

## RQ1_7772ad9410c9

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-15.md#rq1_7772ad9410c9) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-42.md#rq1_fb76588a5316)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_50cddf013ef089bad18c`，根位置 652＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 652. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E1, E2

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.180 秒，模型等待 46.540 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 1 项。诊断 {}。

最终报告 SHA `147868b32596834aacf391ed28589508b3007bc2c4eda6c1344a5a5f188133c8`，决定 SHA `d249847e22cb1f896dbcefd808e720763bd6666c1145cf9ba2ad7d8c51489b5b`。

## RQ1_213ba5cfb58b

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-15.md#rq1_213ba5cfb58b) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-54.json](Queries-54.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-47.md#rq1_61ef4de9729e)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_c20351a5691a8e82de0c`，根位置 937＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 937. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E8, E9

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.800 秒，模型等待 47.944 秒，真实 solver 9 次，查询投影 12 项，动作记录含缓存 28 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `c913d4ab8164fcd8e6457d5d5ef45659c197f2cf4c4022ea1c891792f9c2d1a8`，决定 SHA `348762802ef5e5f384c497796f9d8da93f7b412c6bfd36c63725aaecff819703`。

## RQ1_0deaf993134d

任务 FCR，评价类别 FCR-PAUSE。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_0deaf993134d) · 检查明细  · 查询明细  · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-41.md#rq1_7436b958fbde)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 14, 'necessary_effect_absent': 7}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.108 秒，模型等待 15.520 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'explicit_effect_anchor_conflict': 1}。

最终报告 SHA `5242eff3c9efa1c692203c2a8bcc1b35e2e6348b5adf62c8aba212eb1ba660be`，决定 SHA `6c2faa5edaf6898c839c35d16f56d4fc82bad8e6e9b2072529446127b2b4b6ba`。

## RQ1_22ff3dc40c99

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-15.md#rq1_22ff3dc40c99) · 检查明细 [Checks-84.json](Checks-84.json) · 查询明细 [Queries-54.json](Queries-54.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为repair，[配对成员](Cases-44.md#rq1_0b0fd05c544c)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 5, 'necessary_effect_absent': 16}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.678 秒，模型等待 49.888 秒，真实 solver 7 次，查询投影 6 项，动作记录含缓存 3 项。诊断 {'unbound_or_inapplicable_seed': 2, 'invalid_semantic_row': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `570ec400e2b0fbc23a4e4a9c6529f4253d58a1416a0cc9aeab1e9e0201c15f99`，决定 SHA `64ca7d680b664a5e501740770666711bda9d7bde5cba330f3d94956824d72536`。
