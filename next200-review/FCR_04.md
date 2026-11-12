# FCR 逐例核查

## RQ1_3a3d833ca142

**FCR · FCR-TRANSFER · alarm**

旧版已保留相同转移入口和风险线索，但映射为 unresolved；新版在条件性状态域核查同账本扣款与入账，形成指定类主报警。并未证明特定部署已激活该角色。 主预测实际入口 zero_fee_transaction(address,address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、4 条调查动作和 4 条查询记录。求解结果分布 `{'sat': 3, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_fc58dba4b23d0478dc7a | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |


## RQ1_3b4d9f6eb96f

**FCR · FCR-MINT · not_detected**

指定类规范化提案 0 条，最终有 0 个同类提示或性质的问题。指定类义务 {'excluded': 35}。

该例有 1 次原答、6 条调查动作和 43 条查询记录。求解结果分布 `{'sat': 29, 'unsat': 13, 'unknown': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 6)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_4169c528c5e4

**FCR · FCR-MINT · alarm**

主预测实际入口 mintToken(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 1 次原答、20 条调查动作和 34 条查询记录。求解结果分布 `{'sat': 24, 'unknown': 10}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 7), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_27dd2fdda9f4facd8001 | FCR-MINT | mintToken(address,uint256) | main |


## RQ1_43103f5773b9

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 30}。

该例有 1 次原答、44 条调查动作和 9 条查询记录。求解结果分布 `{'sat': 8, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 4), ('financial_property_conditions_not_established', 3), ('property_task_meaning_unresolved', 3)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_46a031a993c1

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 9}。

该例有 1 次原答、11 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 3), ('financial_property_conditions_not_established', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_475c7d9ec738

**FCR · FCR-PAUSE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 6}。

该例有 1 次原答、16 条调查动作和 3 条查询记录。求解结果分布 `{'sat': 2, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 5), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_4968e56244c9

**FCR · FCR-MINT · not_detected**

指定类规范化提案 1 条，最终有 3 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×2, source_identity_ambiguous_or_unresolved×1。指定类义务 {'excluded': 49}。

该例有 1 次原答、49 条调查动作和 15 条查询记录。求解结果分布 `{'sat': 7, 'unsat': 8}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 5), ('source_identity_ambiguous_or_unresolved', 3), ('financial_property_conditions_not_established', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_49db443acf1d

**FCR · FCR-TRANSFER · not_detected**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 4}。

该例有 2 次原答、4 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_4be3030c4533

**FCR · FCR-MINT · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 property_task_meaning_unresolved×1。指定类义务 {'excluded': 35}。

该例有 1 次原答、47 条调查动作和 35 条查询记录。求解结果分布 `{'sat': 25, 'unsat': 10}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 7), ('financial_property_conditions_not_established', 3), ('source_identity_ambiguous_or_unresolved', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_4d2acebaa2ff

**FCR · FCR-PAUSE · unsupported**

指定类规范化提案 1 条，最终有 3 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×3。指定类义务 {'excluded': 34, 'open': 6}。

该例有 2 次原答、41 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 11), ('property_task_meaning_unresolved', 3), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。

