# FCR 逐例核查

## RQ1_4f9f1ce04ed8

**FCR · FCR-PAUSE · alarm**

主预测实际入口 disableTransfers(bool)；与最终支持项关联的探针 {'financial_block/sat': 1}。旧版也在该入口形成对应问题（i2）。

该例有 2 次原答、8 条调查动作和 8 条查询记录。求解结果分布 `{'unsat': 2, 'sat': 6}`。问题处理原因中最常见的三项为 `[('property_task_meaning_unresolved', 1), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_6bfbe1b6bc0f072eaae1 | FCR-PAUSE | disableTransfers(bool) | main |


## RQ1_4febca8bfe3b

**FCR · FCR-TRANSFER · alarm**

主预测实际入口 zero_fee_transaction(address,address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 2}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、9 条调查动作和 8 条查询记录。求解结果分布 `{'sat': 6, 'unsat': 2}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_8349c54b618af1a1ed45 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |
| finding_3b4979dd399b7b3a0f1d | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |


## RQ1_4feeb0c21e60

**FCR · FCR-TRANSFER · alarm**

主预测实际入口 zero_fee_transaction(address,address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i4）。

该例有 2 次原答、14 条调查动作和 5 条查询记录。求解结果分布 `{'sat': 4, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('property_task_meaning_unresolved', 3), ('financial_property_conditions_not_established', 2)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_0b01362223e2b1de4ebd | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |


## RQ1_53f9777ccdf6

**FCR · FCR-TRANSFER · unsupported**

原答讨论特权字段未初始化；出现相应线索但任务含义未确立。输出未知，缺失证据未由其他类别的报警补足。 指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 property_task_meaning_unresolved×1。指定类义务 {'excluded': 11, 'open': 1}。

该例有 2 次原答、9 条调查动作和 1 条查询记录。求解结果分布 `{'sat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 3), ('property_task_meaning_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_55a1e2ef0f09

**FCR · FCR-DESTROY · unsupported**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 37, 'open': 1}。

该例有 2 次原答、18 条调查动作和 24 条查询记录。求解结果分布 `{'sat': 19, 'unsat': 5}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2), ('property_task_meaning_unresolved', 1), ('changed_business_effect_requires_source_rebinding', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_bee4478720d8dff5f2df | FCR-MINT | setCrowdfundAddress(address) | main |
| finding_5c8c0a4fe55ec388f985 | FCR-MINT | transferFromCrowdfund(address,uint256) | main |


## RQ1_58de46f081ec

**FCR · FCR-FREEZE · not_detected**

真实回答的规范化问题中没有显式 FREEZE 类线索，覆盖出口将指定类义务均列为排除。在该作者风险版上是明确漏检，不能仅凭此证明源码无冻结效果。 指定类规范化提案 0 条，最终有 0 个同类提示或性质的问题。指定类义务 {'excluded': 31}。

该例有 2 次原答、40 条调查动作和 16 条查询记录。求解结果分布 `{'sat': 14, 'unsat': 2}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 5), ('source_identity_ambiguous_or_unresolved', 2), ('financial_property_conditions_not_established', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_1eea7faf705b08be378d | FCR-MINT | mintToken(address,uint256) | main |
| finding_fde2f03988a18d25f7be | FCR-MINT | mintToken(address,uint256) | main |


## RQ1_5b3c7cbe3d9d

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 63}。

该例有 2 次原答、85 条调查动作和 45 条查询记录。求解结果分布 `{'sat': 31, 'unsat': 14}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 10), ('source_identity_ambiguous_or_unresolved', 2), ('financial_property_conditions_not_established', 2)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_c019f751a78b758b1c8f | FCR-PAUSE | pause() | main |
| finding_e0329254759d60714688 | FCR-PAUSE | pause() | main |
| finding_fd0c6a55245a8c0496c3 | FCR-MINT | mintToken(uint256) | main |
| finding_ecefe45c4de6ccaa7417 | FCR-DESTROY | burnFrom(address,uint256) | main |


## RQ1_5eee31e70615

**FCR · FCR-DESTROY · alarm**

旧版也调查该销毁入口。新版原答与程序证据对齐到指定持有人余额的净扣减，进入主预测。 主预测实际入口 destroy(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 2}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、6 条调查动作和 4 条查询记录。求解结果分布 `{'sat': 4}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_9ebb1ad7db0ff010701f | FCR-DESTROY | destroy(address,uint256) | main |
| finding_deae7f01556055d12b4c | FCR-DESTROY | destroy(address,uint256) | main |


## RQ1_6476444da7e8

**FCR · FCR-TRANSFER · not_detected**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 3}。

该例有 2 次原答、4 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_6a278772c4f3

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 1 条，最终有 5 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×2, financial_property_conditions_not_established×2, source_identity_ambiguous_or_unresolved×1。指定类义务 {'excluded': 56}。

该例有 2 次原答、110 条调查动作和 45 条查询记录。求解结果分布 `{'sat': 35, 'unsat': 10}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 11), ('financial_property_conditions_not_established', 4), ('source_identity_ambiguous_or_unresolved', 3)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_c8352bc728ca4716109f | FCR-MINT | mintToken(uint256) | main |
| finding_7b197e2543148df374c8 | FCR-PAUSE | pause() | main |
| finding_fe3f0167b03422711a15 | FCR-PAUSE | pause() | main |

