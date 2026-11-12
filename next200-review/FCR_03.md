# FCR 逐例核查

## RQ1_30c29cd44cad

**FCR · FCR-DESTROY · unsupported**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 property_task_meaning_unresolved×1。指定类义务 {'excluded': 11, 'open': 1}。

该例有 2 次原答、12 条调查动作和 1 条查询记录。求解结果分布 `{'sat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 4), ('property_task_meaning_unresolved', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_329e0d0d7a11

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 2 条，最终有 2 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×2。指定类义务 {'excluded': 12}。

该例有 2 次原答、10 条调查动作和 1 条查询记录。求解结果分布 `{'sat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 4)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_32dbc2fa2433

**FCR · FCR-PAUSE · not_detected**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 12}。

该例有 2 次原答、10 条调查动作和 1 条查询记录。求解结果分布 `{'sat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 4), ('property_task_meaning_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_33d48945207e

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 0 条，最终有 2 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×2。指定类义务 {'excluded': 48}。

该例有 2 次原答、43 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 5), ('property_task_meaning_unresolved', 2), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_3455b6a9ba4f

**FCR · FCR-TRANSFER · not_detected**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 9}。

该例有 2 次原答、10 条调查动作和 4 条查询记录。求解结果分布 `{'sat': 3, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 3), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_353a9b0b5006

**FCR · FCR-DESTROY · not_detected**

真实线索指出费率与实际扣减，绑定后的类别却是 PAUSE，DESTROY 覆盖表判可不报。这是标注风险版上的明确漏检；局部验证过不等于类别映射正确。 指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 32}。

该例有 2 次原答、25 条调查动作和 31 条查询记录。求解结果分布 `{'sat': 11, 'unsat': 17, 'unknown': 3}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 9), ('property_task_meaning_unresolved', 3)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_df838758dd37ce3b06ff | FCR-MINT | burn(address,uint256) | main |


## RQ1_35e0e8d95f92

**FCR · FCR-MINT · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 38}。

该例有 2 次原答、70 条调查动作和 40 条查询记录。求解结果分布 `{'sat': 28, 'unsat': 12}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 10), ('source_identity_ambiguous_or_unresolved', 4), ('financial_property_conditions_not_established', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_35f857af5c9e

**FCR · FCR-PAUSE · not_detected**

指定类规范化提案 1 条，最终有 2 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1, matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 13}。

该例有 1 次原答、31 条调查动作和 8 条查询记录。求解结果分布 `{'sat': 5, 'unsat': 3}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 7), ('property_task_meaning_unresolved', 2), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_37d9daf031da

**FCR · FCR-PAUSE · not_detected**

指定类规范化提案 1 条，最终有 5 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×4, source_identity_ambiguous_or_unresolved×1。指定类义务 {'excluded': 106}。

该例有 1 次原答、84 条调查动作和 127 条查询记录。求解结果分布 `{'unsat': 127}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 23), ('property_task_meaning_unresolved', 7), ('source_identity_ambiguous_or_unresolved', 4)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_39fb6e7197c4

**FCR · FCR-FREEZE · not_detected**

模型已提出冻结资格随所有权转移，但最终所用性质未建立；覆盖出口允许 FREEZE 阴性。未知变得明确，在这个风险版上仍是漏检。 指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 31}。

该例有 2 次原答、83 条调查动作和 6 条查询记录。求解结果分布 `{'sat': 3, 'unsat': 3}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 11), ('source_identity_ambiguous_or_unresolved', 3)]`。

本例没有导出的 finding。有效覆盖见逐例表。

