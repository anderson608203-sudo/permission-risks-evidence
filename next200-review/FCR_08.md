# FCR 逐例核查

## RQ1_985c6fd1d4e4

**FCR · FCR-FREEZE · alarm**

主预测实际入口 freezeAccount(address,bool)；与最终支持项关联的探针 {'financial_block/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 1 次原答、6 条调查动作和 7 条查询记录。求解结果分布 `{'sat': 7}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_7317bb3c0a04740b1a78 | FCR-FREEZE | freezeAccount(address,bool) | main |


## RQ1_9a61667124cf

**FCR · FCR-DESTROY · alarm**

主预测实际入口 destroy(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 4}。旧版也在该入口形成对应问题（i4@25c714cf1b4a, i4@8e89afcce351, i4@935a2911126d, i4@977b12483c58）。

该例有 2 次原答、102 条调查动作和 22 条查询记录。求解结果分布 `{'sat': 21, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 11), ('source_identity_ambiguous_or_unresolved', 6), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 4)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_b9e51eb4fcea8b804c0c | FCR-PAUSE | pause() | main |
| finding_7b955698dc57d416de39 | FCR-PAUSE | pause() | main |
| finding_3b317026bc5550ea6145 | FCR-DESTROY | destroy(address,uint256) | main |
| finding_95909966ecaedd4ef287 | FCR-DESTROY | destroy(address,uint256) | main |
| finding_2d563947b7e0d92a2485 | FCR-DESTROY | destroy(address,uint256) | main |
| finding_9911c1177780443a1a7c | FCR-DESTROY | destroy(address,uint256) | main |


## RQ1_9c365cb18f95

**FCR · FCR-FREEZE · alarm**

主预测实际入口 freeze(address,bool)；与最终支持项关联的探针 {'financial_block/sat': 1}。旧版也在该入口形成对应问题（i3）。

该例有 1 次原答、34 条调查动作和 21 条查询记录。求解结果分布 `{'sat': 16, 'unsat': 5}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 9), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2), ('property_task_meaning_unresolved', 2)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_10ba3383eb2722d3dbc6 | FCR-PAUSE | pause() | main |
| finding_010147c9045ea6170b17 | FCR-FREEZE | freeze(address,bool) | main |


## RQ1_a0facbcc1e38

**FCR · FCR-MINT · alarm**

主预测实际入口 mintToken(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 2}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、47 条调查动作和 32 条查询记录。求解结果分布 `{'sat': 18, 'unsat': 14}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 5), ('property_task_meaning_unresolved', 2), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_f9d2b21025b738c6988e | FCR-MINT | mintToken(address,uint256) | main |
| finding_fcb22758b6e9ac63b863 | FCR-MINT | mintToken(address,uint256) | main |
| finding_a7f8aacda1db8a4c9aef | FCR-DESTROY | withdrawLOOiX() | main |


## RQ1_a4c5ecc3c29e

**FCR · FCR-TRANSFER · not_detected**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 property_task_meaning_unresolved×1。指定类义务 {'excluded': 5}。

该例有 2 次原答、5 条调查动作和 3 条查询记录。求解结果分布 `{'sat': 1, 'unsat': 2}`。问题处理原因中最常见的三项为 `[('property_task_meaning_unresolved', 1), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_a69a455c4a25

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 0 条，最终有 0 个同类提示或性质的问题。指定类义务 {'excluded': 34}。

该例有 1 次原答、28 条调查动作和 27 条查询记录。求解结果分布 `{'sat': 27}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 3), ('financial_property_conditions_not_established', 2), ('source_identity_ambiguous_or_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_a7bf9487cc3f

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 34}。

该例有 1 次原答、28 条调查动作和 24 条查询记录。求解结果分布 `{'sat': 23, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 6), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_a7d72c1e4129

**FCR · FCR-TRANSFER · not_detected**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 12}。

该例有 2 次原答、15 条调查动作和 1 条查询记录。求解结果分布 `{'sat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 4), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1), ('property_task_meaning_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_a906c0b62c0b

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 1 条，最终有 5 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×4, source_identity_ambiguous_or_unresolved×1。指定类义务 {'excluded': 71}。

该例有 1 次原答、160 条调查动作和 6 条查询记录。求解结果分布 `{'sat': 5, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 17), ('source_identity_ambiguous_or_unresolved', 4), ('property_task_meaning_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_aaeb3f57cfd0

**FCR · FCR-PAUSE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 39}。

该例有 2 次原答、35 条调查动作和 124 条查询记录。求解结果分布 `{'sat': 8, 'unsat': 116}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 10), ('source_identity_ambiguous_or_unresolved', 3)]`。

本例没有导出的 finding。有效覆盖见逐例表。

