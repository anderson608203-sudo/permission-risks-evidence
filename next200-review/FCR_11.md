# FCR 逐例核查

## RQ1_cda3df36df22

**FCR · FCR-PAUSE · alarm**

主预测实际入口 stop()；与最终支持项关联的探针 {'financial_block/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 1 次原答、24 条调查动作和 15 条查询记录。求解结果分布 `{'sat': 9, 'unsat': 6}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 5), ('property_task_meaning_unresolved', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_7c5989eab424698e8a6e | FCR-PAUSE | stop() | main |


## RQ1_cea156e41c29

**FCR · FCR-PAUSE · alarm**

旧记录有管理员改变开关的描述，新版调查的是持有人的金融请求能否被阻断。模型保留部署疑点，程序在条件性能力域接受对应结论。 主预测实际入口 disableTransfers(bool)；与最终支持项关联的探针 {'financial_block/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、17 条调查动作和 15 条查询记录。求解结果分布 `{'unsat': 3, 'sat': 12}`。问题处理原因中最常见的三项为 `[('property_task_meaning_unresolved', 2), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2), ('financial_property_conditions_not_established', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_0b979353eaecd9119066 | FCR-PAUSE | disableTransfers(bool) | main |


## RQ1_cf32aac41cf2

**FCR · FCR-TRANSFER · alarm**

主预测实际入口 zero_fee_transaction(address,address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、6 条调查动作和 4 条查询记录。求解结果分布 `{'sat': 3, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('property_task_meaning_unresolved', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_77475cd5480196d91fda | FCR-TRANSFER | zero_fee_transaction(address,address,uint256) | main |


## RQ1_d695cf0bad2e

**FCR · FCR-PAUSE · not_detected**

指定类规范化提案 0 条，最终有 0 个同类提示或性质的问题。指定类义务 {'excluded': 9}。

该例有 2 次原答、6 条调查动作和 0 条查询记录。求解结果分布 `{}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2), ('financial_property_conditions_not_established', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_db11e3e08742

**FCR · FCR-DESTROY · not_detected**

指定 DESTROY 的旧 FP 按冻结口径变 TN。但本例模型仍提出销毁风险，程序将该线索映成 PAUSE；其配对风险版也未命中。不能声称方法已分清该修复的业务差异。 指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 30}。

该例有 1 次原答、10 条调查动作和 53 条查询记录。求解结果分布 `{'unsat': 44, 'sat': 6, 'unknown': 3}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 4), ('property_task_meaning_unresolved', 3), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_db73c28a69c2

**FCR · FCR-TRANSFER · not_detected**

指定类规范化提案 5 条，最终有 5 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×4, source_identity_ambiguous_or_unresolved×1。指定类义务 {'excluded': 21}。

该例有 2 次原答、34 条调查动作和 21 条查询记录。求解结果分布 `{'sat': 17, 'unsat': 4}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 8), ('source_identity_ambiguous_or_unresolved', 2), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_e7ef35d20e05f9364705 | FCR-DESTROY | WitdrawTokenToHolder(address,address,uint256) | main |


## RQ1_dc06d7bad0d8

**FCR · FCR-FREEZE · not_detected**

指定类规范化提案 1 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 33}。

该例有 1 次原答、32 条调查动作和 124 条查询记录。求解结果分布 `{'unsat': 121, 'sat': 3}`。问题处理原因中最常见的三项为 `[('property_task_meaning_unresolved', 5), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 4), ('financial_property_conditions_not_established', 4)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_e13bb6580d65

**FCR · FCR-MINT · alarm**

主预测实际入口 mint(address,uint256)；与最终支持项关联的探针 {'direct_effect/sat': 1}。旧版也在该入口形成对应问题（i1）。

该例有 2 次原答、19 条调查动作和 8 条查询记录。求解结果分布 `{'sat': 8}`。问题处理原因中最常见的三项为 `[('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 5), ('financial_property_conditions_not_established', 1)]`。

最终发现（含附加类别）

| 编号 | 类别 | 入口 | 范围 |
| --- | --- | --- | --- |
| finding_3689f37cd23bfe42923a | FCR-MINT | mint(address,uint256) | main |


## RQ1_e1ce695fff9e

**FCR · FCR-DESTROY · not_detected**

指定类规范化提案 2 条，最终有 2 个同类提示或性质的问题。记录的终止原因 matched_direct_effect_impossible_on_all_applicable_positions_and_paths×2。指定类义务 {'excluded': 9}。

该例有 2 次原答、17 条调查动作和 5 条查询记录。求解结果分布 `{'sat': 4, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 3), ('matched_direct_effect_impossible_on_all_applicable_positions_and_paths', 2)]`。

本例没有导出的 finding。有效覆盖见逐例表。


## RQ1_e25d32acc1f7

**FCR · FCR-TRANSFER · not_detected**

指定类规范化提案 2 条，最终有 1 个同类提示或性质的问题。记录的终止原因 financial_property_conditions_not_established×1。指定类义务 {'excluded': 9}。

该例有 2 次原答、10 条调查动作和 5 条查询记录。求解结果分布 `{'sat': 4, 'unsat': 1}`。问题处理原因中最常见的三项为 `[('financial_property_conditions_not_established', 3), ('property_task_meaning_unresolved', 1)]`。

本例没有导出的 finding。有效覆盖见逐例表。

