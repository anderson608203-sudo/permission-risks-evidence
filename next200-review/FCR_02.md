# FCR 逐例核查

## RQ1_196284e657b0

**FCR · FCR-DESTROY · alarm**

主预测实际入口 destroy(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i2）。

该例有 2 次原答、10 条调查动作和 3 条查询记录。求解结果分布 `{'sat': 3}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 2)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_cfaaf05072e197fe58ff | FCR-DESTROY | destroy(address,uint256) | main |


## RQ1_1a94f7866801

**FCR · FCR-FREEZE · alarm**

主预测实际入口 allowAddress(address,bool), lockAddress(address,bool)；与最终支持项关联的探针 {'financial_block/sat': 3}。旧版也在该入口形成对应问题（i1@977b12483c58, i2@5fc5bdfd4ce6, i2@977b12483c58）。

该例有 2 次原答、144 条调查动作和 103 条查询记录。求解结果分布 `{'unsat': 49, 'sat': 54}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 23), ('source_identity_ambiguous_or_unresolved', 8), ('property_task_meaning_unresolved', 4)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_5a8f054e8272c1eab5b7 | FCR-PAUSE | setLocked(bool) | main |
| finding_c10cb18a0f64207303a6 | FCR-PAUSE | setLocked(bool) | main |
| finding_de28860c6bab40d8d8b0 | FCR-FREEZE | lockAddress(address,bool) | main |
| finding_0b9836f61545adb080ea | FCR-FREEZE | lockAddress(address,bool) | main |
| finding_1b4e48e4ed9a32781c86 | FCR-FREEZE | allowAddress(address,bool) | main |


## RQ1_1c6b43b24d4c

**FCR · FCR-PAUSE · not_detected**

指定类规范化提案 0 条，最终有 0 个同类提示或性质的问题。指定类义务 {'excluded': 100}。

该例有 1 次原答、12 条调查动作和 226 条查询记录。求解结果分布 `{'unsat': 176, 'sat': 50}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 9), ('property_task_meaning_unresolved', 4)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_1f06ce07140f

**FCR · FCR-TRANSFER · unsupported**

指定类规范化提案 2 条，最终有 11 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×7, financial_property_conditions_not_established×3, source_identity_ambiguous_or_unresolved×1。指定类义务 {'excluded': 48, 'open': 2}。

该例有 2 次原答、71 条调查动作和 27 条查询记录。求解结果分布 `{'sat': 17, 'unsat': 10}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 7), ('financial_property_conditions_not_established', 5), ('source_identity_ambiguous_or_unresolved', 4)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_1f932eab663d

**FCR · FCR-FREEZE · alarm**

主预测实际入口 freezeAccount(address,bool)；与最终支持项关联的探针 {'financial_block/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 1 次原答、44 条调查动作和 16 条查询记录。求解结果分布 `{'sat': 14, 'unsat': 2}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 7), ('source_identity_ambiguous_or_unresolved', 2)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_58d724eecae3c77f888f | FCR-FREEZE | freezeAccount(address,bool) | main |


## RQ1_2046acc1c802

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 31}。

该例有 2 次原答、45 条调查动作和 18 条查询记录。求解结果分布 `{'sat': 16, 'unsat': 2}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 7), ('source_identity_ambiguous_or_unresolved', 2), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_206d19a8539c

**FCR · FCR-TRANSFER · not_detected**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 4}。

该例有 2 次原答、4 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_20dfd0c54b94

**FCR · FCR-PAUSE · unsupported**

两版都识别暂停开关。新版先遇到基类入口歧义，再对派生目标检查金融阻断；存在开放义务和未执行动作，原命中退为未知。 指定类规范化提案 3 条，最终有 6 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×5, source_identity_ambiguous_or_unresolved×1。指定类义务 {'excluded': 46, 'open': 8}。

该例有 2 次原答、81 条调查动作和 161 条查询记录。求解结果分布 `{'sat': 61, 'unsat': 100}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 16), ('source_identity_ambiguous_or_unresolved', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_2d22977434b5

**FCR · FCR-MINT · not_detected**

指定类规范化提案 0 条，最终有 0 个同类提示或性质的问题。指定类义务 {'excluded': 35}。

该例有 1 次原答、8 条调查动作和 32 条查询记录。求解结果分布 `{'sat': 22, 'unsat': 10}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 5), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_30177d564271

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 0 条，最终有 0 个同类提示或性质的问题。指定类义务 {'excluded': 33}。

该例有 2 次原答、34 条调查动作和 15 条查询记录。求解结果分布 `{'sat': 15}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 4), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 4), ('source_identity_ambiguous_or_unresolved', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。

