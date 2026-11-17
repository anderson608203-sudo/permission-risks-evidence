# 逐例变化与因果审阅

[总报告](WorkReview.md) · [全部成员](Members.md) · [全部根](Roots.md) · [全部配对](Pairs.md)

以下“已确认”仅表示冻结记录及源码支持的实际消费链。历史模型正文缺失的差异标为可能原因，未用重构回答替代。

## AC相对最近SmartBug的18个改变根

### D2:36:author:1 · LEGEND

[RQ1_d80631993985](Cases-02.md#rq1_d80631993985)，TP→FN。实际窗口[[2607, 2716]]，记录决定{'policy_missing': 4}，相关理由{'expected_authorization_not_established': 4}。

已确认原根本次没有匹配报警，最终保持未知或报了其他根。所列policy_missing或external_dependency是当前可证断点；没有历史逐字回答，不能断言模型怎样改变了意见。

### D2:95:author:1 · DeskToken

[RQ1_f25b185c19f2](Cases-04.md#rq1_f25b185c19f2)，TP→FN。实际窗口[[696, 916]]，记录决定{'policy_missing': 3}，相关理由{'expected_authorization_not_established': 3}。

已确认原根本次没有匹配报警，最终保持未知或报了其他根。所列policy_missing或external_dependency是当前可证断点；没有历史逐字回答，不能断言模型怎样改变了意见。

### D2:138:author:1 · CryptoRoulette

[RQ1_6505f6beccc4](Cases-06.md#rq1_6505f6beccc4)，TP→FN。实际窗口[[291, 382]]，记录决定{'policy_missing': 3}，相关理由{'expected_authorization_not_established': 3}。

已确认原根本次没有匹配报警，最终保持未知或报了其他根。所列policy_missing或external_dependency是当前可证断点；没有历史逐字回答，不能断言模型怎样改变了意见。

### D2:184:author:1 · IotaGoldToken

[RQ1_935718dd81f8](Cases-08.md#rq1_935718dd81f8)，TP→FN。实际窗口[[696, 920]]，记录决定{'policy_missing': 3}，相关理由{'expected_authorization_not_established': 3}。

已确认原根本次没有匹配报警，最终保持未知或报了其他根。所列policy_missing或external_dependency是当前可证断点；没有历史逐字回答，不能断言模型怎样改变了意见。

### D2:186:author:1 · initialize

[RQ1_b47a735f7e64](Cases-08.md#rq1_b47a735f7e64)，FN→TP。实际窗口[[2906, 3048]]，记录决定{'source_role_reassignment': 2, 'policy_missing': 8}，相关理由{'expected_authorization_not_established': 8}。

已确认新增最终消费 source_role_reassignment, source_role_reassignment。位置与性质见检查分片；尚不能独立估计程序关系、LLM语义和随机响应各自的边际贡献。

### D2:229:author:1 · setupStackDepthLib

[RQ1_fdd2bcee346e](Cases-10.md#rq1_fdd2bcee346e)，TP→FN。实际窗口[[2240, 2408]]，记录决定{'policy_missing': 2, 'external_dependency': 1}，相关理由{'expected_authorization_not_established': 3}。

已确认原根本次没有匹配报警，最终保持未知或报了其他根。所列policy_missing或external_dependency是当前可证断点；没有历史逐字回答，不能断言模型怎样改变了意见。

### D2:239:S1 · init

[RQ1_43caf1e7f7b5](Cases-10.md#rq1_43caf1e7f7b5)，TP→FN。实际窗口[[468, 607]]，记录决定{'policy_missing': 11}，相关理由{'expected_authorization_not_established': 11}。

已确认原根本次没有匹配报警，最终保持未知或报了其他根。所列policy_missing或external_dependency是当前可证断点；没有历史逐字回答，不能断言模型怎样改变了意见。

### D2:327:author:1 · initialize

[RQ1_2ca53b535ccd](Cases-14.md#rq1_2ca53b535ccd)，FN→TP。实际窗口[[775, 917], [2617, 2866]]，记录决定{'policy_missing': 19, 'source_role_reassignment': 3}，相关理由{'expected_authorization_not_established': 19}。

已确认新增最终消费 source_role_reassignment, source_role_reassignment, source_role_reassignment。位置与性质见检查分片；尚不能独立估计程序关系、LLM语义和随机响应各自的边际贡献。

### D2:330:author:1 · Kill

[RQ1_c453f88fd0ff](Cases-14.md#rq1_c453f88fd0ff)，TP→FN。实际窗口[[377, 438]]，记录决定{'policy_missing': 1}，相关理由{'expected_authorization_not_established': 1}。

已确认原根本次没有匹配报警，最终保持未知或报了其他根。所列policy_missing或external_dependency是当前可证断点；没有历史逐字回答，不能断言模型怎样改变了意见。

### D2:428:author:1 · initialize

[RQ1_e27b11bddd94](Cases-18.md#rq1_e27b11bddd94)，FN→TP。实际窗口[[2326, 2468], [3373, 3556]]，记录决定{'source_role_reassignment': 2, 'policy_missing': 21}，相关理由{'expected_authorization_not_established': 21}。

已确认新增最终消费 source_role_reassignment, source_role_reassignment。位置与性质见检查分片；尚不能独立估计程序关系、LLM语义和随机响应各自的边际贡献。

### D2:449:author:1 · BEN

[RQ1_e174c093cc1b](Cases-19.md#rq1_e174c093cc1b)，FN→TP。实际窗口[[2799, 2921]]，记录决定{'program_support': 1, 'policy_missing': 5}，相关理由{'expected_authorization_not_established': 5}。

已确认新增最终消费 program_support。位置与性质见检查分片；尚不能独立估计程序关系、LLM语义和随机响应各自的边际贡献。

### D2:476:author:1 · transferOwnership

[RQ1_58c19182bf25](Cases-20.md#rq1_58c19182bf25)，TP→FN。实际窗口[[839, 998]]，记录决定{'policy_missing': 1}，相关理由{'expected_authorization_not_established': 1}。

已确认原根本次没有匹配报警，最终保持未知或报了其他根。所列policy_missing或external_dependency是当前可证断点；没有历史逐字回答，不能断言模型怎样改变了意见。

### D2:521:S1 · init

[RQ1_f694e40ffba2](Cases-22.md#rq1_f694e40ffba2)，FN→TP。实际窗口[[772, 909]]，记录决定{'policy_missing': 10, 'scoped_semantic_conflict': 1}，相关理由{'expected_authorization_not_established': 10}。

已确认新增最终消费 scoped_semantic_conflict。位置与性质见检查分片；尚不能独立估计程序关系、LLM语义和随机响应各自的边际贡献。

### D2:569:author:1 · ENTS

[RQ1_5a32d57754dd](Cases-23.md#rq1_5a32d57754dd)，FN→TP。实际窗口[[2610, 2744]]，记录决定{'program_support': 1, 'policy_missing': 4}，相关理由{'expected_authorization_not_established': 4}。

已确认新增最终消费 program_support。位置与性质见检查分片；尚不能独立估计程序关系、LLM语义和随机响应各自的边际贡献。

### D2:580:S1 · selfdestructs

[RQ1_3daa3272da3f](Cases-24.md#rq1_3daa3272da3f)，TP→FN。实际窗口[[4954, 5028]]，记录决定{'policy_missing': 1}，相关理由{'expected_authorization_not_established': 1}。

已确认原根本次没有匹配报警，最终保持未知或报了其他根。所列policy_missing或external_dependency是当前可证断点；没有历史逐字回答，不能断言模型怎样改变了意见。

### D2:589:author:1 · WorldSafetySecurityToken

[RQ1_8b881d18ff63](Cases-24.md#rq1_8b881d18ff63)，TP→FN。实际窗口[[3718, 3920]]，记录决定{'policy_missing': 3}，相关理由{'expected_authorization_not_established': 3}。

已确认原根本次没有匹配报警，最终保持未知或报了其他根。所列policy_missing或external_dependency是当前可证断点；没有历史逐字回答，不能断言模型怎样改变了意见。

### D2:596:author:1 · IotaGoldToken

[RQ1_45ce1fe8110b](Cases-25.md#rq1_45ce1fe8110b)，TP→FN。实际窗口[[705, 929]]，记录决定{'policy_missing': 3}，相关理由{'expected_authorization_not_established': 3}。

已确认原根本次没有匹配报警，最终保持未知或报了其他根。所列policy_missing或external_dependency是当前可证断点；没有历史逐字回答，不能断言模型怎样改变了意见。

### D2:222:original:1 · fallback

[RQ1_868007cf433c](Cases-26.md#rq1_868007cf433c)，FN→TP。实际窗口[[799, 1047]]，记录决定{'policy_missing': 2, 'program_support': 1}，相关理由{'expected_authorization_not_established': 2}。

已确认新增最终消费 program_support。位置与性质见检查分片；尚不能独立估计程序关系、LLM语义和随机响应各自的边际贡献。

## FCR相对BG的所有状态变化

### FCR-DESTROY · RQ1_1ca74e3a1b5e

[风险端](Cases-27.md#rq1_1ca74e3a1b5e) 未知→报警，[修复端](Cases-48.md#rq1_68cdf0f21f76) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 2}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_237ffc6da6a2

[风险端](Cases-27.md#rq1_237ffc6da6a2) 未知→报警，[修复端](Cases-42.md#rq1_45f5c9057f72) 未检出→未检出，整对False→True。

risk实际检查决定{'external_dependency': 1, 'uncompensated_debit': 1}，未决缺口{'external_dependency': 1}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_bcafc7a40ce2

[风险端](Cases-28.md#rq1_bcafc7a40ce2) 报警→报警，[修复端](Cases-41.md#rq1_e1ce695fff9e) 未检出→未知，整对True→False。

repair实际检查决定{'external_dependency': 1, 'source_check_excluded': 1}，未决缺口{'external_dependency': 1}。当前未检出或未知按保存范围列出；撤回报警后仍未知不算有效误报纠正。

### FCR-DESTROY · RQ1_eb71e4b3e05f

[风险端](Cases-31.md#rq1_eb71e4b3e05f) 未知→报警，[修复端](Cases-40.md#rq1_05a542de9e26) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 3}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_2476ba262811

[风险端](Cases-32.md#rq1_2476ba262811) 未知→报警，[修复端](Cases-49.md#rq1_627eebfd65db) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 1}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-TRANSFER · RQ1_fa502559ffda

[风险端](Cases-32.md#rq1_fa502559ffda) 报警→报警，[修复端](Cases-38.md#rq1_0a95fcc25752) 未检出→未知，整对True→False。

repair实际检查决定{'external_dependency': 1, 'source_check_excluded': 1}，未决缺口{'external_dependency': 1}。当前未检出或未知按保存范围列出；撤回报警后仍未知不算有效误报纠正。

### FCR-DESTROY · RQ1_f529b424392d

[风险端](Cases-34.md#rq1_f529b424392d) 未检出→报警，[修复端](Cases-35.md#rq1_507e0efe86f1) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 1}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_d6eec0ddeec9

[风险端](Cases-34.md#rq1_d6eec0ddeec9) 未知→报警，[修复端](Cases-27.md#rq1_92a10a0592ae) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 1}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-TRANSFER · RQ1_17f46ff7b389

[风险端](Cases-34.md#rq1_17f46ff7b389) 报警→报警，[修复端](Cases-48.md#rq1_4850481cd27e) 未知→未检出，整对False→True。

repair实际检查决定{'source_check_excluded': 1}，未决缺口{}。当前未检出或未知按保存范围列出；撤回报警后仍未知不算有效误报纠正。

### FCR-PAUSE · RQ1_239dec1e19b3

[风险端](Cases-35.md#rq1_239dec1e19b3) 未知→报警，[修复端](Cases-27.md#rq1_63ed6120bd80) 未知→未知，整对False→False。

risk实际检查决定{'productive_outgoing_control': 2, 'scope_missing': 2}，未决缺口{'scope_missing': 2, 'external_dependency': 1}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-PAUSE · RQ1_18b83e12ea1f

[风险端](Cases-36.md#rq1_18b83e12ea1f) 未知→报警，[修复端](Cases-45.md#rq1_9b3403bc5e3b) 未知→未知，整对False→False。

risk实际检查决定{'scope_missing': 2, 'productive_outgoing_control': 2}，未决缺口{'external_dependency': 7, 'scope_missing': 2}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_7772ad9410c9

[风险端](Cases-36.md#rq1_7772ad9410c9) 未知→报警，[修复端](Cases-42.md#rq1_fb76588a5316) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 2}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-PAUSE · RQ1_ffaaf45e84b1

[风险端](Cases-37.md#rq1_ffaaf45e84b1) 未知→报警，[修复端](Cases-34.md#rq1_2ee1d93e1f45) 未知→未知，整对False→False。

risk实际检查决定{'scope_missing': 2, 'productive_outgoing_control': 2}，未决缺口{'scope_missing': 2, 'external_dependency': 1}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-TRANSFER · RQ1_b25ec4a4cd43

[风险端](Cases-37.md#rq1_b25ec4a4cd43) 报警→报警，[修复端](Cases-29.md#rq1_14d06cbbe5a7) 未知→未检出，整对False→True。

repair实际检查决定{}，未决缺口{}。当前未检出或未知按保存范围列出；撤回报警后仍未知不算有效误报纠正。

### FCR-DESTROY · RQ1_8c7b36b2c4f9

[风险端](Cases-38.md#rq1_8c7b36b2c4f9) 未知→报警，[修复端](Cases-30.md#rq1_ce9f072e6cf8) 未知→未知，整对False→False。

risk实际检查决定{'uncompensated_debit': 2}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_81b770577694

[风险端](Cases-39.md#rq1_81b770577694) 未知→报警，[修复端](Cases-29.md#rq1_c4aeb6122521) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 1}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_c3d569994373

[风险端](Cases-39.md#rq1_c3d569994373) 未知→报警，[修复端](Cases-35.md#rq1_2b2d929cbd84) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 1}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_a9742b3414d8

[风险端](Cases-39.md#rq1_a9742b3414d8) 未知→报警，[修复端](Cases-27.md#rq1_6af8dad9e222) 未知→未知，整对False→False。

risk实际检查决定{'uncompensated_debit': 2}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_196284e657b0

[风险端](Cases-39.md#rq1_196284e657b0) 未知→报警，[修复端](Cases-37.md#rq1_0bf6f8bce8d9) 未知→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 2}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

repair实际检查决定{}，未决缺口{}。当前未检出或未知按保存范围列出；撤回报警后仍未知不算有效误报纠正。

### FCR-PAUSE · RQ1_615f9f99c585

[风险端](Cases-40.md#rq1_615f9f99c585) 未知→报警，[修复端](Cases-33.md#rq1_3db9d6846001) 未知→未知，整对False→False。

risk实际检查决定{'scope_missing': 2, 'productive_outgoing_control': 2}，未决缺口{'scope_missing': 2, 'external_dependency': 1}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_cac16ccd972b

[风险端](Cases-41.md#rq1_cac16ccd972b) 未知→报警，[修复端](Cases-27.md#rq1_2fde609553be) 未知→未知，整对False→False。

risk实际检查决定{'external_dependency': 1, 'uncompensated_debit': 2}，未决缺口{'external_dependency': 1}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_30c29cd44cad

[风险端](Cases-41.md#rq1_30c29cd44cad) 未知→报警，[修复端](Cases-28.md#rq1_329e0d0d7a11) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 1}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_56bac052a93a

[风险端](Cases-42.md#rq1_56bac052a93a) 未知→报警，[修复端](Cases-27.md#rq1_f27cacd5f34a) 未知→未知，整对False→False。

risk实际检查决定{'uncompensated_debit': 1}，未决缺口{'external_dependency': 4}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_cb7efb519f69

[风险端](Cases-42.md#rq1_cb7efb519f69) 未知→报警，[修复端](Cases-40.md#rq1_81162a271264) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 1}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_890376502486

[风险端](Cases-42.md#rq1_890376502486) 未知→报警，[修复端](Cases-41.md#rq1_e38d4cc9d6fc) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 1}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_f1bb587376e8

[风险端](Cases-43.md#rq1_f1bb587376e8) 未知→报警，[修复端](Cases-45.md#rq1_35646ded2a70) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 1}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_8456d2957fff

[风险端](Cases-44.md#rq1_8456d2957fff) 未知→报警，[修复端](Cases-45.md#rq1_776a6b98d18f) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 2}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_8ebdd1256aa7

[风险端](Cases-45.md#rq1_8ebdd1256aa7) 未知→报警，[修复端](Cases-32.md#rq1_4e1e2a329c89) 未知→未知，整对False→False。

risk实际检查决定{'external_dependency': 1, 'uncompensated_debit': 2}，未决缺口{'external_dependency': 1}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-TRANSFER · RQ1_0c666ce785e8

[风险端](Cases-46.md#rq1_0c666ce785e8) 报警→报警，[修复端](Cases-32.md#rq1_3455b6a9ba4f) 未知→未检出，整对False→True。

repair实际检查决定{}，未决缺口{}。当前未检出或未知按保存范围列出；撤回报警后仍未知不算有效误报纠正。

### FCR-DESTROY · RQ1_3aae751c2593

[风险端](Cases-46.md#rq1_3aae751c2593) 未知→报警，[修复端](Cases-47.md#rq1_346a05c1609d) 未检出→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 1}，未决缺口{}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_493871f89451

[风险端](Cases-46.md#rq1_493871f89451) 未知→报警，[修复端](Cases-44.md#rq1_5905f594ee2c) 未知→未知，整对False→False。

risk实际检查决定{'external_dependency': 2, 'uncompensated_debit': 3}，未决缺口{'external_dependency': 1}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_f2292d8956bc

[风险端](Cases-48.md#rq1_f2292d8956bc) 未知→报警，[修复端](Cases-38.md#rq1_f1045931ef0e) 未知→未知，整对False→False。

risk实际检查决定{'uncompensated_debit': 2, 'external_dependency': 1}，未决缺口{'external_dependency': 1}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

### FCR-DESTROY · RQ1_750c11959b7a

[风险端](Cases-48.md#rq1_750c11959b7a) 未知→报警，[修复端](Cases-34.md#rq1_d9f9d5c86db9) 未知→未检出，整对False→True。

risk实际检查决定{'uncompensated_debit': 2, 'external_dependency': 1}，未决缺口{'external_dependency': 1}。有最终阳性消费，具体同人账本/阻断证据见逐例检查。

repair实际检查决定{}，未决缺口{}。当前未检出或未知按保存范围列出；撤回报警后仍未知不算有效误报纠正。

## AC本次8个参考外位置

- [RQ1_ed7c5ffc5160](Cases-04.md#rq1_ed7c5ffc5160)，transferFrom，字节位置2542，依据program_support，按固定参考列FP。At transferFrom(address,address,uint256), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification.

- [RQ1_5f2ca3273ff3](Cases-04.md#rq1_5f2ca3273ff3)，addSigner，字节位置7595，依据scoped_semantic_conflict，按固定参考列FP。The assessment concerns the policy governing the protected effect at source offset 7595. The located duty and the deciding caller conflict at this applied source effect; this is a scoped semantic prediction.

- [RQ1_6674f42c37b9](Cases-05.md#rq1_6674f42c37b9)，transfer，字节位置4961，依据program_support，按固定参考列FP。At transfer(address,uint256), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification.

- [RQ1_597e2ef1991a](Cases-06.md#rq1_597e2ef1991a)，transferFrom，字节位置2551，依据program_support，按固定参考列FP。At transferFrom(address,address,uint256), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification.

- [RQ1_e7c2ee23438d](Cases-06.md#rq1_e7c2ee23438d)，buy，字节位置1777，依据program_support，按固定参考列FP。At buy(), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification.

- [RQ1_f4232c234a28](Cases-11.md#rq1_f4232c234a28)，transferFrom，字节位置2550，依据program_support，按固定参考列FP。At transferFrom(address,address,uint256), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification.

- [RQ1_cafc626080f8](Cases-15.md#rq1_cafc626080f8)，setEtherPrice，字节位置7901，依据program_support，按固定参考列FP。At setEtherPrice(uint256), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification.

- [RQ1_30b4e48b4f5c](Cases-24.md#rq1_30b4e48b4f5c)，transferFrom，字节位置2530，依据program_support，按固定参考列FP。At transferFrom(address,address,uint256), the committing effect admits a requester outside the applicable source-bound qualification. The check compares the effective guard with the bound authorization requirement, including any alternative qualification.
