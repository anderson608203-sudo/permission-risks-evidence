# 逐成员科研审阅

[总索引](Members.md) · [源码](Code.md)

## RQ1_513d5cbf275a

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-19.md#rq1_513d5cbf275a) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-72.json](Queries-72.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-48.md#rq1_874ec6f58322)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_c93ceac6b5fd1122dce7`，根位置 6766＋30，依据 `productive_outgoing_control`。The assessment concerns a restriction on the designated holder's outgoing transfer at source offset 6766. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E22, E23, E31, E34

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 10.932 秒，模型等待 37.360 秒，真实 solver 9 次，查询投影 23 项，动作记录含缓存 48 项。诊断 {'audit_card_text': 1, 'audit_card_issue_kind': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `ef4c047087b2c3ab95b0c5a92fec77fb81cf34f19ee2126d9440e20468697433`，决定 SHA `a5a073f358727cc870e68019d4ff06ec33ef495c87be66f5bc56c408ce8c86c5`。

## RQ1_1c6b43b24d4c

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-20.md#rq1_1c6b43b24d4c) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-72.json](Queries-72.json) [Queries-73.json](Queries-73.json) [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-30.md#rq1_37d9daf031da)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 5, 'external_dependency': 11, 'source_unit_missing': 4}。相关检查决定 {'scope_missing': 9}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 980.501 秒，模型等待 50.314 秒，真实 solver 563 次，查询投影 1034 项，动作记录含缓存 19 项。诊断 {'missing_claim_or_source_anchor': 3, 'unrelated_or_secondary_graph_pairs_deferred': 1, 'program_investigation_seconds': 1}。

最终报告 SHA `fbfbd3672589e67b59cc08401fe56f529a1bbc8362db98edfa6ca8482823853e`，决定 SHA `edeefade3492f3c5425b28ffb4548fb76c21c03be870d5a2637b0235e31e7e3c`。

## RQ1_af7c473b8cca

任务 FCR，评价类别 FCR-MINT。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_af7c473b8cca) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-28.md#rq1_4be3030c4533)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_3f4971131a35cce6466f`，根位置 6626＋33，依据 `new_entitlement`。The assessment concerns a positive new entitlement for a controlled beneficiary at source offset 6626. A qualified controller changes an actual financial position by a positive issuance for a controlled beneficiary. 证据 E1

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 59.529 秒，模型等待 27.457 秒，真实 solver 62 次，查询投影 74 项，动作记录含缓存 51 项。诊断 {'audit_card_text': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `51e9ff551d8dacf36c763a642401ebf4ec45e17ea2cc310909988c70f3db90bb`，决定 SHA `d39ed937006bdb78f4d42907dc705b5b764665f26ce744acea83498bfcc01a17`。

## RQ1_bda0eaac7a22

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_bda0eaac7a22) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-03.json](Requests-03.json)

评价端为risk，[配对成员](Cases-32.md#rq1_666a61447f85)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → report 报警

发现 `finding_446ab119213bcb9f34a0`，根位置 1208＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 1208. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E1, E11, E12, E3, E5, E7, E9

发现 `finding_a53b0ac21543c2b48655`，根位置 891＋476，依据 `program_support`。At zero_fee_transaction(address,address,uint256), the scoped change moves another holder’s existing rights to a separate position without the applicable holder-issued consent. 证据 E18, E2

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.064 秒，模型等待 41.561 秒，真实 solver 5 次，查询投影 8 项，动作记录含缓存 7 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `2274d6fdcb4a341f0f14806ec31715b54c36677681de010645fefcb67e7bdb21`，决定 SHA `120175f7d3ca907bf781e83ca9545454f0debcc0970709126f04c9b846335b73`。

## RQ1_abb48ccfac75

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-20.md#rq1_abb48ccfac75) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-41.md#rq1_3e235f5e70d4)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 1}。相关检查决定 {'scope_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 4.699 秒，模型等待 57.878 秒，真实 solver 3 次，查询投影 3 项，动作记录含缓存 3 项。诊断 {'missing_claim_or_source_anchor': 1, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `ec077b244f9869b0ab881d878e020207f0d53ad48d815ad68b4bebe2edeceba2`，决定 SHA `62a99749cc1e5b06ca55a8b5b6f79a6ba9f48865b6143278ab218a3ccc214966`。

## RQ1_35f857af5c9e

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-20.md#rq1_35f857af5c9e) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-32.md#rq1_cda3df36df22)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 1}。相关检查决定 {'scope_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.538 秒，模型等待 31.110 秒，真实 solver 5 次，查询投影 9 项，动作记录含缓存 5 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `c0a264a1023fd043fa45684591a883045b8e8a859330ca1bc43e3a54a8732e2b`，决定 SHA `d646f1638acdc9ce2302e502f2417bcedc0864179889f40c7758e21723f8b61c`。

## RQ1_4f9f1ce04ed8

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_4f9f1ce04ed8) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-30.md#rq1_b0a696b11b0a)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_291a89dbcf2462983f68`，根位置 991＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 991. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E3, E4, E5

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.525 秒，模型等待 34.569 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 5 项。诊断 {'audit_source_scope_mismatch': 1, 'no_locatable_source': 1}。

最终报告 SHA `27401acd289793362f25c2bbc3c5175f3c0761c78c50e56ba5947db42adbe615`，决定 SHA `0cd6e7ba403a12827eb06e2c78c703a4622119dc5079255bfbbdce35af1a1199`。

## RQ1_c4e8c693f07b

任务 FCR，评价类别 FCR-TRANSFER。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_c4e8c693f07b) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-31.md#rq1_f0010e656b81)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_044c388db55e634052fc`，根位置 777＋31，依据 `existing_rights_moved`。The assessment concerns a transfer of another holder's existing rights at source offset 777. The qualified operation debits another holder and causally credits the same asset without an applicable holder grant. 证据 E11, E13, E2, E5, E7, E8, E9

发现 `finding_ab6ad6682b592c688d34`，根位置 460＋476，依据 `program_support`。At zero_fee_transaction(address,address,uint256), the scoped change moves another holder’s existing rights to a separate position without the applicable holder-issued consent. 证据 E17, E3

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.942 秒，模型等待 33.783 秒，真实 solver 5 次，查询投影 8 项，动作记录含缓存 6 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `492cba40167fa31dac657d2cd5463cb860a665bb099e821782737eb1b80310e8`，决定 SHA `3f2eb1ebd21f4f2a0be1f06eeab88dfed049ef65ba45c9d7b6f32c0e05e3f35f`。

## RQ1_874ec6f58322

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-20.md#rq1_874ec6f58322) · 检查明细  · 查询明细  · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-48.md#rq1_513d5cbf275a)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 18, 'necessary_effect_absent': 18}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 5.310 秒，模型等待 23.952 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `883a41666a911dd2e027d6e01260bb5926cc30f950812e3e0bc346350e1348c0`，决定 SHA `6a30d91cead27438e4c8b06949ba9ae5370c34f8b09bb6bc89e7d4705b751671`。

## RQ1_ce246116f7fb

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_ce246116f7fb) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-47.md#rq1_05b0801e5ccd)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_15462bf9c05fa9e2a239`，根位置 935＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 935. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E10, E9

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.105 秒，模型等待 41.888 秒，真实 solver 9 次，查询投影 12 项，动作记录含缓存 32 项。诊断 {'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `d42d21af67cd3b641c5e450c5cba27dc34a327fdbbf5634211435e979c2a004b`，决定 SHA `3b4b1526429f62e4e0689c2014e1952c7cc4407c3bb45df0695bc04cf0c132bc`。

## RQ1_b7fd0e26135f

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-20.md#rq1_b7fd0e26135f) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-31.md#rq1_cae50a0089d5)。指定类风险端未知、修复端未检出，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 1}。相关检查决定 {'scope_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 7.583 秒，模型等待 75.656 秒，真实 solver 9 次，查询投影 9 项，动作记录含缓存 34 项。诊断 {'audit_source_scope_mismatch': 1, 'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1}。

最终报告 SHA `271e6c38154ddc8f699c242d4194b02b13463b53b08bf41af19984fefc07aa88`，决定 SHA `334f6280241f47d4df3d74fb05f25788c9cffe7b392c1812f93ddf197f5c53fa`。

## RQ1_1450fdff3528

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-20.md#rq1_1450fdff3528) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-29.md#rq1_c185f5a00faf)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.083 秒，模型等待 68.576 秒，真实 solver 6 次，查询投影 6 项，动作记录含缓存 38 项。诊断 {'audit_effect_unbound': 1}。

最终报告 SHA `9e9458e3784418b3dc7dd4729423676942869b126cc44e8c9275497aa4bc270d`，决定 SHA `39ad093fd85732a213f5445fd33db13d4e644c66c91aa58d04a89a5c051fe347`。

## RQ1_4850481cd27e

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未知。

[实际输入](InputSource-20.md#rq1_4850481cd27e) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细  · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-34.md#rq1_17f46ff7b389)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'necessary_effect_absent': 4, 'no_effect_in_scope': 4, 'source_task_reading': 1}。相关检查决定 {'source_check_excluded': 1}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.633 秒，模型等待 39.904 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 4 项。诊断 {'no_locatable_source': 2}。

最终报告 SHA `0a24ce9f88a508ddccb9f9edf8abb31a619349c0739836a9e4f992f08c06b17c`，决定 SHA `a26489d7a1806724e6291f1ad9d625928b03b32b27e41267056094d1736cfa0c`。

## RQ1_907fc6f2c1f4

任务 FCR，评价类别 FCR-PAUSE。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_907fc6f2c1f4) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-36.md#rq1_b6a39de5a1bc)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_0bc865695ec6bf2e4228`，根位置 768＋28，依据 `productive_outgoing_control`。The assessment concerns a common restriction on ordinary outgoing transfers at source offset 768. The scoped controller change prevents the same positive outgoing use for ordinary holders without an applicable exempt agent. A committing use and its control direction were checked on the actual ledger. 证据 E1, E2, E3

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.610 秒，模型等待 20.205 秒，真实 solver 2 次，查询投影 2 项，动作记录含缓存 3 项。诊断 {'no_locatable_source': 3}。

最终报告 SHA `b1cbff842bf6fb8a5a1c18a774993ba35955a7df024c4d13318fcd99e767eb7d`，决定 SHA `bb99356402f2055961ba3f88304c098b62b18c0a9363f1c5943165399ad07bce`。

## RQ1_12a3a2848c3c

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-20.md#rq1_12a3a2848c3c) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-41.md#rq1_f4327be729a4)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 6, 'no_privileged_intervention': 2}。相关检查决定 {'scope_missing': 4}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.739 秒，模型等待 23.852 秒，真实 solver 6 次，查询投影 6 项，动作记录含缓存 19 项。诊断 {}。

最终报告 SHA `56743634edccb38e6a9a31cd94954aea56f3b9dc8410998ec9e1ed2621cf6275`，决定 SHA `996186af90f8f732fe26e4a249470aad5a2d9d6942d0bd16b3bcb7484188454d`。

## RQ1_28b8d1e3b59b

任务 FCR，评价类别 FCR-PAUSE。当前未知，BG 未知。

[实际输入](InputSource-20.md#rq1_28b8d1e3b59b) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-27.md#rq1_2ef6e8719d06)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'scope_missing': 1}。相关检查决定 {'scope_missing': 1}。理由共现不能直接证明唯一因果。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.863 秒，模型等待 41.256 秒，真实 solver 5 次，查询投影 9 项，动作记录含缓存 5 项。诊断 {'no_locatable_source': 1}。

最终报告 SHA `773b60d6ac80f9ea2307396142743029a0e2b6edec5abb1de0b6edf8338d4b72`，决定 SHA `6e0f238b7660791a90b0422f2a869b3a2483528601743f77d4f9d55d5764b768`。

## RQ1_cbf806ae77cb

任务 FCR，评价类别 FCR-FREEZE。当前报警，BG 报警。

[实际输入](InputSource-20.md#rq1_cbf806ae77cb) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-39.md#rq1_4a8515bede97)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未知 → initial 报警 → report 报警

发现 `finding_c8bd999fc8191dac294b`，根位置 2538＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E16, E31, E32

发现 `finding_2af7dbfefe18a79be57e`，根位置 2538＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E18, E33, E35

发现 `finding_1148202180b634fc9eff`，根位置 2538＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E23, E39, E41

发现 `finding_e0e04718e2f9ac0f6dc4`，根位置 2538＋251，依据 `program_support`。At lockAddress(address,bool), the checked privileged change restricts the outgoing right of the designated holder for an otherwise usable request within the recorded domain. 证据 E21, E36, E38

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 27.777 秒，模型等待 27.117 秒，真实 solver 117 次，查询投影 114 项，动作记录含缓存 63 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 10}。

最终报告 SHA `cf1b3c2f9b6a02af877730304c8a74969bf60996ff3368935963438ccec7b514`，决定 SHA `5cad276a1f5ebd16a980e910155d79be0bee1543c592f421b7de5f74912832dd`。

## RQ1_f2292d8956bc

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-20.md#rq1_f2292d8956bc) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-38.md#rq1_f1045931ef0e)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_782187082efdf4c0edeb`，根位置 2054＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 2054. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E5, E6

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.230 秒，模型等待 58.491 秒，真实 solver 1 次，查询投影 1 项，动作记录含缓存 18 项。诊断 {'no_locatable_source': 1, 'unrelated_or_secondary_graph_pairs_deferred': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `a12b5051244e7c68968d63aac3220e38c633e475e91d85e2277989eb9ba7fefb`，决定 SHA `6f533fe9d0e86f9c31e527829b1431f4058b343b67926367fef88293eb21e2ec`。

## RQ1_9809e3aa83b0

任务 FCR，评价类别 FCR-FREEZE。当前未知，BG 未知。

[实际输入](InputSource-20.md#rq1_9809e3aa83b0) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-45.md#rq1_81780fe65981)。指定类风险端报警、修复端未知，整对正确为False。其他类别报警独立记录。

阶段投影 basic 未知 → initial 未知 → report 未知

本类仍未知。明确缺口 {'external_dependency': 1}。相关检查决定 {}。理由共现不能直接证明唯一因果。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 25.035 秒，模型等待 28.643 秒，真实 solver 24 次，查询投影 16 项，动作记录含缓存 19 项。诊断 {'audit_card_issue_kind': 1, 'audit_source_scope_mismatch': 1, 'unrelated_or_secondary_graph_pairs_deferred': 2}。

最终报告 SHA `ed65fc5e7916371c7bc57e5cbaf28894e6e8a151d36c884d77d24faeb50a0e53`，决定 SHA `680392dff421236b6502bf19af253f8862f37cfbdd9bdc6cf39cf1951983fd29`。

## RQ1_206d19a8539c

任务 FCR，评价类别 FCR-TRANSFER。当前未检出，BG 未检出。

[实际输入](InputSource-20.md#rq1_206d19a8539c) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细  · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-28.md#rq1_3a3d833ca142)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 2, 'effect_range_decided': 1, 'necessary_effect_absent': 1}。相关检查决定 {'source_check_excluded': 2}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.321 秒，模型等待 35.448 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 5 项。诊断 {'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `dfbac8f6e60486b75edc39a49c1cac624693a5ac7957453b38be74e3ba67c41b`，决定 SHA `a55061ace1d49f8dbed8778e0c294b741489318e624ee0cb2faf348c6022c529`。

## RQ1_750c11959b7a

任务 FCR，评价类别 FCR-DESTROY。当前报警，BG 未知。

[实际输入](InputSource-20.md#rq1_750c11959b7a) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为risk，[配对成员](Cases-34.md#rq1_d9f9d5c86db9)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 报警 → initial 报警 → feedback 报警 → report 报警

发现 `finding_a872701d923a7d2fbc36`，根位置 723＋30，依据 `uncompensated_debit`。The assessment concerns an uncompensated loss of another holder's entitlement at source offset 723. The qualified operation reduces another holder's position without a matching credit on this source branch. 证据 E10, E9

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 3.222 秒，模型等待 51.295 秒，真实 solver 9 次，查询投影 12 项，动作记录含缓存 30 项。诊断 {'audit_effect_unbound': 4, 'unrelated_or_secondary_graph_pairs_deferred': 2, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `d7c2d7814c2db2297324eb3ff23d4bac320cb4f1f0d988b10ce6bc45570cfde1`，决定 SHA `9ea3e07732c6a3e55605265159866723a60d67ac73cfdf9c458ede12e2c5c5e6`。

## RQ1_90c233777f5e

任务 FCR，评价类别 FCR-FREEZE。当前未检出，BG 未检出。

[实际输入](InputSource-20.md#rq1_90c233777f5e) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细 [Queries-74.json](Queries-74.json) · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-38.md#rq1_6244da144ced)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 17, 'necessary_effect_absent': 16, 'detached_local_holder_switch': 1}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 8.041 秒，模型等待 53.376 秒，真实 solver 6 次，查询投影 6 项，动作记录含缓存 36 项。诊断 {'audit_source_scope_mismatch': 1, 'audit_effect_unbound': 1}。

最终报告 SHA `ed810ce4710a7ea88a3d4368f680102522f079cfa928a8e75dc717727b481381`，决定 SHA `f7bce6cc5f81a6685760ce4eac4f1392f5a6c134299798baa76f01bee11f7fcb`。

## RQ1_fa882017777c

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-20.md#rq1_fa882017777c) · 检查明细 [Checks-88.json](Checks-88.json) · 查询明细  · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-40.md#rq1_389d8dfc83d5)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → feedback 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 5, 'necessary_effect_absent': 4}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 True，本成员请求 2 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.182 秒，模型等待 38.266 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 2 项。诊断 {'no_locatable_source': 1, 'invalid_top_level_or_duplicate_key': 1}。

最终报告 SHA `f8bc2a21f72f035d2bd782c8c810bf4ba371a196a7190c2bc68444d4c89e76a9`，决定 SHA `a9b561f5ca2a56a080fa64b970ee134be9e9dc8d9557784204a4fbcb5db17a80`。

## RQ1_68cdf0f21f76

任务 FCR，评价类别 FCR-DESTROY。当前未检出，BG 未检出。

[实际输入](InputSource-20.md#rq1_68cdf0f21f76) · 检查明细  · 查询明细  · 服务回执索引 [Requests-04.json](Requests-04.json)

评价端为repair，[配对成员](Cases-27.md#rq1_1ca74e3a1b5e)。指定类风险端报警、修复端未检出，整对正确为True。其他类别报警独立记录。

阶段投影 basic 未检出 → initial 未检出 → report 未检出

当前范围允许未检出。局部依据 {'no_effect_in_scope': 3, 'necessary_effect_absent': 2}。相关检查决定 {}。参考风险端若为此状态仍计 FN。

模型分析被消费标志 False，本成员请求 1 次。该标志按定位与消费定义，收到 substantive 响应仍可能为 false。

程序 2.015 秒，模型等待 41.648 秒，真实 solver 0 次，查询投影 0 项，动作记录含缓存 0 项。诊断 {'audit_card_text': 1, 'explicit_effect_anchor_conflict': 2}。

最终报告 SHA `a1f7cfbf2dbc861808ce3f22367dfe4ef0576385e443b091b183e1cb5c7887d1`，决定 SHA `231f7822eb9d9df027c066a050ae1efb08c6750e1129684e6c67c5dc119cebe0`。
