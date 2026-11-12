# FCR 逐例核查

## RQ1_024b9da10799

**FCR · FCR-MINT · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 property_task_meaning_unresolved×1。指定类义务 {'excluded': 40}。

该例有 1 次原答、26 条调查动作和 18 条查询记录。求解结果分布 `{'sat': 14, 'unsat': 4}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 8), ('property_task_meaning_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_0267e2a8ebb2

**FCR · FCR-MINT · alarm**

主预测实际入口 mintToken(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i2）。

该例有 1 次原答、22 条调查动作和 41 条查询记录。求解结果分布 `{'sat': 29, 'unsat': 12}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 4), ('financial_property_conditions_not_established', 4)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_509887cee59bfee3ce27 | FCR-MINT | mintToken(address,uint256) | main |


## RQ1_085aaca2f412

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 1 条，最终有 2 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1, financial_property_conditions_not_established×1。指定类义务 {'excluded': 27}。

该例有 1 次原答、9 条调查动作和 3 条查询记录。求解结果分布 `{'sat': 3}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_0bf6f8bce8d9

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 2 条，最终有 2 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1, matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 9}。

该例有 2 次原答、10 条调查动作和 1 条查询记录。求解结果分布 `{'sat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 3), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_0c666ce785e8

**FCR · FCR-TRANSFER · alarm**

主预测实际入口 zero_fee_transaction(address,address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、11 条调查动作和 6 条查询记录。求解结果分布 `{'sat': 5, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 4)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_86f0a98f6f14d2b03588 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |


## RQ1_0e202076b336

**FCR · FCR-TRANSFER · not_detected**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 12}。

该例有 2 次原答、12 条调查动作和 1 条查询记录。求解结果分布 `{'sat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 4), ('property_task_meaning_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_0f3c3f400f6f

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 61}。

该例有 1 次原答、46 条调查动作和 13 条查询记录。求解结果分布 `{'unsat': 3, 'sat': 10}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 6), ('source_identity_ambiguous_or_unresolved', 2), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_15346457ba72

**FCR · FCR-DESTROY · unsupported**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 property_task_meaning_unresolved×1。指定类义务 {'excluded': 3, 'open': 1}。

该例有 2 次原答、6 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('property_task_meaning_unresolved', 2), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_1844e5d3d18e

**FCR · FCR-TRANSFER · alarm**

主预测实际入口 zero_fee_transaction(address,address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 6}。旧版也在该入口形成对应问题（i6@051252cf9fe3, i6@c9e1e9c2647a, i6@fc757553236a）。

该例有 2 次原答、48 条调查动作和 433 条查询记录。求解结果分布 `{'sat': 45, 'unsat': 388}`。问题处理原因中最常见的三项为 `[('property_task_meaning_unresolved', 4), ('source_identity_ambiguous_or_unresolved', 2), ('financial_property_conditions_not_established', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_4786759609aca1354372 | FCR-DESTROY | WitdrawTokenToHolder(address,address,uint256) | main |
| finding_76fd7ffbc2c5ad88fa84 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |
| finding_527031d11194189f9d6b | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |
| finding_3c6925d487bcba3f75cb | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |


## RQ1_18c85d7f1380

**FCR · FCR-MINT · alarm**

主预测实际入口 mintToken(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i2）。

该例有 2 次原答、17 条调查动作和 34 条查询记录。求解结果分布 `{'sat': 24, 'unknown': 10}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 6), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_bdbb8cb02eb6d06a6e4a | FCR-MINT | mintToken(address,uint256) | main |

