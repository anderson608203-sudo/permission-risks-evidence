# FCR 逐例核查

## RQ1_6c3522e11e92

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 1 条，最终有 6 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×4, source_identity_ambiguous_or_unresolved×1, matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 53}。

该例有 2 次原答、84 条调查动作和 15 条查询记录。求解结果分布 `{'sat': 6, 'unsat': 9}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 11), ('source_identity_ambiguous_or_unresolved', 4), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 4)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_6ca2b0aeda43

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 0 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 48}。

该例有 2 次原答、31 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 6), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_72c6b8c6b605

**FCR · FCR-TRANSFER · not_detected**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 9}。

该例有 2 次原答、9 条调查动作和 2 条查询记录。求解结果分布 `{'sat': 2}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 5)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_73b13298e227

**FCR · FCR-MINT · alarm**

主预测实际入口 mint(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i2）。

该例有 2 次原答、56 条调查动作和 42 条查询记录。求解结果分布 `{'sat': 20, 'unsat': 22}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 9), ('source_identity_ambiguous_or_unresolved', 3), ('financial_property_conditions_not_established', 3)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_67fd37cdf9c27ed9debc | FCR-MINT | mint(address,uint256) | main |
| finding_8536957c1593a27b6d08 | FCR-DESTROY | burnFrom(address,uint256) | main |


## RQ1_7405f0959142

**FCR · FCR-PAUSE · not_detected**

指定类规范化提案 0 条，最终有 0 个同类提示或性质的问题。指定类义务 {'excluded': 10}。

该例有 2 次原答、8 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 2), ('property_task_meaning_unresolved', 1), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_7450d39da940

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 30}。

该例有 2 次原答、51 条调查动作和 3 条查询记录。求解结果分布 `{'sat': 3}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 5), ('property_task_meaning_unresolved', 4), ('source_identity_ambiguous_or_unresolved', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_770ae395781c

**FCR · FCR-MINT · not_detected**

指定类规范化提案 0 条，最终有 0 个同类提示或性质的问题。指定类义务 {'excluded': 25}。

该例有 1 次原答、12 条调查动作和 9 条查询记录。求解结果分布 `{'sat': 8, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 4)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_776a6b98d18f

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 2 条，最终有 2 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×2。指定类义务 {'excluded': 4}。

该例有 2 次原答、6 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 3)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_7a54127ed44c

**FCR · FCR-PAUSE · unsupported**

修复版的 PAUSE 从有效不报变为未知，判别能力退化，但没有产生新的指定类误报。 指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 32, 'open': 2}。

该例有 2 次原答、43 条调查动作和 6 条查询记录。求解结果分布 `{'sat': 5, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 5), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 5), ('property_task_meaning_unresolved', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_7bfd58ffb1ae

**FCR · FCR-MINT · not_detected**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 36}。

该例有 2 次原答、41 条调查动作和 67 条查询记录。求解结果分布 `{'sat': 52, 'unsat': 15}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 5), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 5), ('source_identity_ambiguous_or_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。

