# FCR 逐例核查

## RQ1_e73c99ca23e5

**FCR · FCR-TRANSFER · alarm**

主预测实际入口 zero_fee_transaction(address,address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 4}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、74 条调查动作和 62 条查询记录。求解结果分布 `{'sat': 34, 'unsat': 28}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 8), ('financial_property_conditions_not_established', 4), ('property_task_meaning_unresolved', 2)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_4a4bec3366904d537f30 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |
| finding_54dfe019f5ad1a3e8261 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |
| finding_4c24aa17119da66926d9 | FCR-PAUSE | pause() | main |
| finding_7bda4a05c0a8f5b07115 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |
| finding_834f54fb811ef4b3a8c5 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |
| finding_7816af0efe3f13b68aa0 | FCR-PAUSE | pause() | main |


## RQ1_eb30c6dee989

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 2 条，最终有 3 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×3。指定类义务 {'excluded': 24}。

该例有 2 次原答、17 条调查动作和 26 条查询记录。求解结果分布 `{'sat': 20, 'unsat': 6}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 4), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_ee2aa7f32d31

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 2 条，最终有 2 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×2。指定类义务 {'excluded': 24}。

该例有 1 次原答、24 条调查动作和 55 条查询记录。求解结果分布 `{'sat': 49, 'unsat': 6}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 3), ('financial_property_conditions_not_established', 3)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_f322b5b8495d

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 1 条，最终有 2 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×2。指定类义务 {'excluded': 4}。

该例有 2 次原答、7 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_fa2207747d01

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 31}。

该例有 1 次原答、44 条调查动作和 18 条查询记录。求解结果分布 `{'sat': 18}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 8), ('source_identity_ambiguous_or_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_fbd0377ce541

**FCR · FCR-PAUSE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 21}。

该例有 1 次原答、23 条调查动作和 9 条查询记录。求解结果分布 `{'sat': 7, 'unsat': 2}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 5), ('financial_property_conditions_not_established', 2), ('property_task_meaning_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_fe11616caf66

**FCR · FCR-TRANSFER · alarm**

主预测实际入口 zero_fee_transaction(address,address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、6 条调查动作和 4 条查询记录。求解结果分布 `{'sat': 3, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('source_identity_ambiguous_or_unresolved', 1), ('financial_property_conditions_not_established', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_d5761327736303899eeb | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |


## RQ1_fe4ace2cd8e5

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 37}。

该例有 2 次原答、21 条调查动作和 15 条查询记录。求解结果分布 `{'unsat': 7, 'sat': 8}`。问题处理原因中最常见的三项为 `[('property_task_meaning_unresolved', 4), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2), ('financial_property_conditions_not_established', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_fe7add810da5

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 property_task_meaning_unresolved×1。指定类义务 {'excluded': 4}。

该例有 2 次原答、7 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('property_task_meaning_unresolved', 2), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_ffcaa562a72d

**FCR · FCR-PAUSE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 9}。

该例有 1 次原答、23 条调查动作和 4 条查询记录。求解结果分布 `{'sat': 1, 'unsat': 3}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 6), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1), ('property_task_meaning_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。

