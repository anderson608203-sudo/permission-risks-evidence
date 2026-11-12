# FCR 逐例核查

## RQ1_adf28b957352

**FCR · FCR-FREEZE · unsupported**

指定类规范化提案 2 条，最终有 2 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1, financial_property_conditions_not_established×1。指定类义务 {'excluded': 32, 'open': 3}。

该例有 2 次原答、66 条调查动作和 56 条查询记录。求解结果分布 `{'sat': 38, 'unknown': 12, 'unsat': 6}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 7), ('financial_property_conditions_not_established', 7), ('source_identity_ambiguous_or_unresolved', 3)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_af7c473b8cca

**FCR · FCR-MINT · alarm**

主预测实际入口 mintToken(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 1 次原答、16 条调查动作和 48 条查询记录。求解结果分布 `{'sat': 33, 'unsat': 15}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 5), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2), ('property_task_meaning_unresolved', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_e91cce0358b3cfc222cf | FCR-MINT | mintToken(address,uint256) | main |


## RQ1_afb609e0053e

**FCR · FCR-PAUSE · unsupported**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'open': 2, 'excluded': 8}。

该例有 2 次原答、11 条调查动作和 17 条查询记录。求解结果分布 `{'unsat': 5, 'sat': 12}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 3), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_b0a696b11b0a

**FCR · FCR-PAUSE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 8}。

该例有 2 次原答、20 条调查动作和 9 条查询记录。求解结果分布 `{'unsat': 2, 'sat': 7}`。问题处理原因中最常见的三项为 `[('property_task_meaning_unresolved', 3), ('financial_property_conditions_not_established', 2), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_b5217318672e

**FCR · FCR-TRANSFER · alarm**

主预测实际入口 zero_fee_transaction(address,address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、10 条调查动作和 6 条查询记录。求解结果分布 `{'sat': 5, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 3)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_204f4f1dd335d5e6d2a5 | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |


## RQ1_b61f163309a1

**FCR · FCR-MINT · alarm**

主预测实际入口 allocateToken(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 1 次原答、14 条调查动作和 29 条查询记录。求解结果分布 `{'sat': 16, 'unsat': 13}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 3), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_f450b513f6a436c8e63c | FCR-MINT | allocateToken(address,uint256) | main |


## RQ1_b649070a92c3

**FCR · FCR-PAUSE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1。指定类义务 {'excluded': 25}。

该例有 1 次原答、31 条调查动作和 9 条查询记录。求解结果分布 `{'sat': 8, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 7), ('property_task_meaning_unresolved', 2), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_b731957fa974

**FCR · FCR-MINT · alarm**

主预测实际入口 issue(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 4}。旧版也在该入口形成对应问题（i4@25c714cf1b4a, i4@8e89afcce351, i4@935a2911126d, i4@977b12483c58）。

该例有 2 次原答、81 条调查动作和 44 条查询记录。求解结果分布 `{'sat': 31, 'unsat': 13}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 9), ('financial_property_conditions_not_established', 5), ('property_task_meaning_unresolved', 2)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_df586862ee69e80cbe3e | FCR-MINT | issue(address,uint256) | main |
| finding_173d7afd243fd426874f | FCR-MINT | issue(address,uint256) | main |
| finding_2bbd4761f52c42550308 | FCR-MINT | issue(address,uint256) | main |
| finding_259179b7b6bdef8e3d84 | FCR-MINT | issue(address,uint256) | main |
| finding_cf049dc6ab376ea4eaeb | FCR-PAUSE | pause() | main |
| finding_44a109d59edcb9ff5caa | FCR-PAUSE | pause() | main |


## RQ1_b84042e6eefd

**FCR · FCR-PAUSE · alarm**

主预测实际入口 disableTransfers(bool)；与最终支持项关联的探针 {'financial_block/sat': 2}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、11 条调查动作和 12 条查询记录。求解结果分布 `{'unsat': 5, 'sat': 7}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_d4a288004d86b138f096 | FCR-PAUSE | disableTransfers(bool) | main |
| finding_228d582a4514969a516d | FCR-PAUSE | disableTransfers(bool) | main |


## RQ1_bc5855a83e2d

**FCR · FCR-MINT · alarm**

主预测实际入口 mint(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 1 次原答、26 条调查动作和 8 条查询记录。求解结果分布 `{'sat': 8}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 4), ('source_identity_ambiguous_or_unresolved', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_b8d8e26d13a9fa7fb906 | FCR-MINT | mint(address,uint256) | main |

