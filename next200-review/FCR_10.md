# FCR 逐例核查

## RQ1_bcafc7a40ce2

**FCR · FCR-DESTROY · unsupported**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 property_task_meaning_unresolved×1。指定类义务 {'excluded': 8, 'open': 1}。

该例有 2 次原答、16 条调查动作和 5 条查询记录。求解结果分布 `{'sat': 4, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 4), ('property_task_meaning_unresolved', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_c24c6c95ccbd

**FCR · FCR-PAUSE · alarm**

主预测实际入口 disableTransfers(bool)；与最终支持项关联的探针 {'financial_block/sat': 2}。

该例有 1 次原答、12 条调查动作和 12 条查询记录。求解结果分布 `{'sat': 9, 'unsat': 3}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 2), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_daaba9edf1064bd5ca87 | FCR-PAUSE | disableTransfers(bool) | main |
| finding_a4a692dac664fb6ab84d | FCR-PAUSE | disableTransfers(bool) | main |


## RQ1_c29df435681e

**FCR · FCR-PAUSE · alarm**

主预测实际入口 disableTransfers(bool)；与最终支持项关联的探针 {'financial_block/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、10 条调查动作和 10 条查询记录。求解结果分布 `{'sat': 7, 'unsat': 3}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 2), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_badd36c3ef9106602d99 | FCR-PAUSE | disableTransfers(bool) | main |


## RQ1_c75d73e1c482

**FCR · FCR-MINT · alarm**

主预测实际入口 mintToken(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、52 条调查动作和 57 条查询记录。求解结果分布 `{'sat': 39, 'unknown': 15, 'unsat': 3}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 9), ('source_identity_ambiguous_or_unresolved', 4), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 3)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_88730853088a8adb57a0 | FCR-MINT | mintToken(address,uint256) | main |


## RQ1_c772c59e4a76

**FCR · FCR-FREEZE · unsupported**

指定类规范化提案 1 条，最终有 3 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×3。指定类义务 {'excluded': 33, 'open': 3}。

该例有 1 次原答、30 条调查动作和 37 条查询记录。求解结果分布 `{'sat': 26, 'unknown': 11}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 7), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 3), ('source_identity_ambiguous_or_unresolved', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_579a10c207b9e79d40a0 | FCR-MINT | mintToken(address,uint256) | main |


## RQ1_c80f7a639e42

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 3 条，最终有 2 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×2。指定类义务 {'excluded': 34}。

该例有 2 次原答、72 条调查动作和 24 条查询记录。求解结果分布 `{'sat': 24}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 11), ('source_identity_ambiguous_or_unresolved', 4)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_1ea6369add2d6d7c5ccb | FCR-MINT | mintToken(address,uint256) | main |
| finding_1c4f82937604bd1f2540 | FCR-DESTROY | lock(address,uint256,uint256) | main |
| finding_c394bf3242678743d212 | FCR-MINT | lock(address,uint256,uint256) | main |


## RQ1_c9626779c857

**FCR · FCR-DESTROY · alarm**

主预测实际入口 burnFrom(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 2}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、10 条调查动作和 11 条查询记录。求解结果分布 `{'sat': 11}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_1ddfdc0af18a503a3553 | FCR-DESTROY | burnFrom(address,uint256) | main |
| finding_dd44e0c9161e590b2daa | FCR-DESTROY | burnFrom(address,uint256) | main |
| finding_f1959ddaf736c9012906 | FCR-FREEZE | UserLock(address,bool) | main |


## RQ1_cb8c3fafbda1

**FCR · FCR-MINT · alarm**

主预测实际入口 mintToken(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i2）。

该例有 1 次原答、18 条调查动作和 48 条查询记录。求解结果分布 `{'sat': 33, 'unsat': 15}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 6), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1), ('property_task_meaning_unresolved', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_33dbbe5b1767f3ef4478 | FCR-MINT | mintToken(address,uint256) | main |


## RQ1_cd39ae0d15a5

**FCR · FCR-PAUSE · alarm**

主预测实际入口 stop()；与最终支持项关联的探针 {'financial_block/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、28 条调查动作和 18 条查询记录。求解结果分布 `{'sat': 12, 'unsat': 6}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 4), ('financial_property_conditions_not_established', 2), ('property_task_meaning_unresolved', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_a2c8e2ae9fe4195cc1ef | FCR-PAUSE | stop() | main |


## RQ1_cd47d22b26a9

**FCR · FCR-FREEZE · unsupported**

指定类规范化提案 1 条，最终有 2 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×1, financial_property_conditions_not_established×1。指定类义务 {'excluded': 31, 'open': 3}。

该例有 2 次原答、15 条调查动作和 43 条查询记录。求解结果分布 `{'sat': 30, 'unknown': 13}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 9), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。

