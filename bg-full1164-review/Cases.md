# 代表成员的实际机制与不利结果

选择覆盖新增、丢失、撤回未决、修复端误报、明确排除与技术失败。以下引用均为已冻结的结构化判断。

## RQ1_a4f43feac855 · AC

相对上次全量，有效未检出 → 报警。本次接纳了 source_role_reassignment；逐条位置与证据编号见 findings。 作者根新增 1、丢失 0。对应根的作用窗口与最早可见断点见 Roots。

各阶段 {'checkpoint_basic': 'alarm', 'checkpoint_feedback': 'alarm', 'checkpoint_initial': 'alarm', 'report': 'alarm'}。相关义务理由 no_effect_in_scope, policy_missing, effect_range_decided, nominee_acceptance, external_dependency。

当前指定类报告证据 finding_90225e8e550cffeda3dc(source_role_reassignment), finding_ccc81e4fc87a47e04a7e(source_role_reassignment)。

## RQ1_0fa374173417 · AC

相对上次全量，报警 → 未决。未取得足以导出指定判断的依据。已定位检查登记 expected_authorization_not_established。 作者根新增 0、丢失 1。对应根的作用窗口与最早可见断点见 Roots。

各阶段 {'checkpoint_basic': 'unsupported', 'checkpoint_feedback': 'unsupported', 'checkpoint_initial': 'unsupported', 'report': 'unsupported'}。相关义务理由 no_effect_in_scope, policy_missing, source_task_reading, external_dependency。

当前无本类主报警。

## RQ1_12eee489708e · AC

相对上次全量，有效未检出 → 报警。本次接纳了 scoped_semantic_conflict；逐条位置与证据编号见 findings。 作者根新增 1、丢失 0。对应根的作用窗口与最早可见断点见 Roots。

各阶段 {'checkpoint_basic': 'alarm', 'checkpoint_initial': 'alarm', 'report': 'alarm'}。相关义务理由 effect_range_decided, external_dependency, no_effect_in_scope。

当前指定类报告证据 finding_7dfa2192ae4f64a77953(scoped_semantic_conflict)。

## RQ1_31450a049444 · AC

相对上次全量，报警 → 技术失败。没有最终投影。失败阶段与两种模型后处理异常、一个输入展开上限见 Failures；该成员留在评价分母。 作者根新增 0、丢失 1。对应根的作用窗口与最早可见断点见 Roots。

各阶段 {}。相关义务理由 。

当前无本类主报警。

## RQ1_dadf1b436e9d · AC

相对上次全量，报警 → 报警。本次接纳了 scoped_semantic_conflict；逐条位置与证据编号见 findings。 作者根新增 0、丢失 1。对应根的作用窗口与最早可见断点见 Roots。

各阶段 {'checkpoint_basic': 'alarm', 'checkpoint_feedback': 'alarm', 'checkpoint_initial': 'alarm', 'report': 'alarm'}。相关义务理由 source_task_reading, no_effect_in_scope, external_dependency, policy_missing, effect_range_decided。

当前指定类报告证据 finding_0e2f52f8d660d71e880b(scoped_semantic_conflict), finding_415e6ca4910b3dcb4f16(scoped_semantic_conflict)。

## RQ1_58de46f081ec · FCR-FREEZE

相对上次全量，有效未检出 → 有效未检出。实际读取后允许本类阴性；局部排除的作用范围见 scoped_obligation_bases。

各阶段 {'checkpoint_basic': 'not_detected', 'checkpoint_initial': 'not_detected', 'report': 'not_detected'}。相关义务理由 no_effect_in_scope, necessary_effect_absent, detached_local_holder_switch。

当前无本类主报警。

## RQ1_81a85f242b60 · FCR-MINT

相对上次全量，未决 → 报警。本次接纳了 program_support；逐条位置与证据编号见 findings。

各阶段 {'checkpoint_basic': 'unsupported', 'checkpoint_initial': 'alarm', 'report': 'alarm'}。相关义务理由 no_effect_in_scope, source_task_reading, necessary_effect_absent, effect_range_decided, ordinary_paid_credit。

当前指定类报告证据 finding_c0cefe9cd03affe5dbef(program_support)。

## RQ1_db11e3e08742 · FCR-DESTROY

相对上次全量，未决 → 未决。未取得足以导出指定判断的依据。已定位检查登记 financial_property_conditions_not_established。

各阶段 {'checkpoint_basic': 'not_detected', 'checkpoint_feedback': 'unsupported', 'checkpoint_initial': 'unsupported', 'report': 'unsupported'}。相关义务理由 necessary_effect_absent, holder_consent_basis_unresolved, no_effect_in_scope, source_task_reading。

当前无本类主报警。

## RQ1_7d7240a2af90 · FCR-TRANSFER

相对上次全量，未决 → 报警。本次接纳了 existing_rights_moved；逐条位置与证据编号见 findings。

各阶段 {'checkpoint_basic': 'alarm', 'checkpoint_initial': 'alarm', 'report': 'alarm'}。相关义务理由 source_task_reading, no_effect_in_scope。

当前指定类报告证据 finding_b4557005816f4b8b6ff8(existing_rights_moved)。

## RQ1_8456d2957fff · FCR-DESTROY

相对上次全量，未决 → 未决。未取得足以导出指定判断的依据。已定位检查登记 financial_property_conditions_not_established。

各阶段 {'checkpoint_basic': 'unsupported', 'checkpoint_feedback': 'unsupported', 'checkpoint_initial': 'unsupported', 'report': 'unsupported'}。相关义务理由 no_effect_in_scope, source_unit_missing, necessary_effect_absent。

当前无本类主报警。

## RQ1_353a9b0b5006 · FCR-DESTROY

相对上次全量，有效未检出 → 未决。未取得足以导出指定判断的依据。已定位检查登记 financial_property_conditions_not_established。

各阶段 {'checkpoint_basic': 'not_detected', 'checkpoint_feedback': 'unsupported', 'checkpoint_initial': 'unsupported', 'report': 'unsupported'}。相关义务理由 necessary_effect_absent, holder_consent_basis_unresolved, no_effect_in_scope, source_task_reading。

当前无本类主报警。
