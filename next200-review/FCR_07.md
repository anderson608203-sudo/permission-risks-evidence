# FCR 逐例核查

## RQ1_7d7240a2af90

**FCR · FCR-TRANSFER · alarm**

主预测实际入口 zero_fee_transaction(address,address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、6 条调查动作和 4 条查询记录。求解结果分布 `{'sat': 3, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_ffdb352efbbf981b62d3 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |


## RQ1_81a85f242b60

**FCR · FCR-MINT · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 34}。

该例有 1 次原答、39 条调查动作和 18 条查询记录。求解结果分布 `{'sat': 15, 'unsat': 3}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 5), ('financial_property_conditions_not_established', 3), ('source_identity_ambiguous_or_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_8456d2957fff

**FCR · FCR-DESTROY · alarm**

主预测实际入口 destroy(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 2}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、8 条调查动作和 6 条查询记录。求解结果分布 `{'sat': 6}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_f6187ec2248d3f514322 | FCR-DESTROY | destroy(address,uint256) | main |
| finding_1d380979fce772f96139 | FCR-DESTROY | destroy(address,uint256) | main |


## RQ1_86a0269d7608

**FCR · FCR-MINT · unsupported**

指定类规范化提案 3 条，最终有 2 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1, financial_property_conditions_not_established×1。指定类义务 {'excluded': 43, 'open': 1}。

该例有 2 次原答、50 条调查动作和 15 条查询记录。求解结果分布 `{'sat': 8, 'unsat': 7}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 4), ('financial_property_conditions_not_established', 4), ('source_identity_ambiguous_or_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_8d60a47186e2

**FCR · FCR-TRANSFER · not_detected**

指定类规范化提案 2 条，最终有 2 个同类提示或性质的问题。记录的终止原因 property_task_meaning_unresolved×1, matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 4}。

该例有 2 次原答、4 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('property_task_meaning_unresolved', 1), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_8e8598bb724e

**FCR · FCR-PAUSE · alarm**

主预测实际入口 disableTransfers(bool)；与最终支持项关联的探针 {'financial_block/sat': 2}。

该例有 2 次原答、22 条调查动作和 17 条查询记录。求解结果分布 `{'sat': 16, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 4), ('property_task_meaning_unresolved', 1), ('financial_property_conditions_not_established', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_920d31ebe9e3f5777e81 | FCR-PAUSE | disableTransfers(bool) | main |
| finding_66c6839d47fb6f19538a | FCR-PAUSE | disableTransfers(bool) | main |


## RQ1_9451d6dac4de

**FCR · FCR-TRANSFER · alarm**

主预测实际入口 zero_fee_transaction(address,address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i5）。

该例有 2 次原答、12 条调查动作和 6 条查询记录。求解结果分布 `{'sat': 5, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 4)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_ace0e91ace5afc2ba1cc | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |


## RQ1_94d9f2cfc77c

**FCR · FCR-MINT · not_detected**

指定类规范化提案 0 条，最终有 0 个同类提示或性质的问题。指定类义务 {'excluded': 26}。

该例有 2 次原答、16 条调查动作和 15 条查询记录。求解结果分布 `{'sat': 13, 'unsat': 2}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 5)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_980e04c92f4d

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 53}。

该例有 1 次原答、61 条调查动作和 10 条查询记录。求解结果分布 `{'sat': 7, 'unsat': 3}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 5), ('financial_property_conditions_not_established', 3), ('source_identity_ambiguous_or_unresolved', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_983137cbe5d6

**FCR · FCR-MINT · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 source_identity_ambiguous_or_unresolved×1。指定类义务 {'excluded': 35}。

该例有 1 次原答、35 条调查动作和 44 条查询记录。求解结果分布 `{'sat': 31, 'unsat': 13}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 5), ('financial_property_conditions_not_established', 5), ('source_identity_ambiguous_or_unresolved', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。

