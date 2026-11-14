# 逐例审阅

## RQ1_58de46f081ec

证据目录 run/members/RQ1_58de46f081ec/attempt_1/，报告哈希 9220fc8260d16402074089797c6382fae66206c5cdebbc19add1d765b4b0b360

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "alarm",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "unsupported",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "decision_only 风险版漏检"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unknown_assessment_vocabulary,unbound_or_inapplicable_seed,unrelated_or_secondary_graph_pairs_deferred,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": true,
    "paired_id": "RQ1_2046acc1c802",
    "state": "not_detected",
    "changes": {
      "v32": {
        "before": "not_detected",
        "after": "not_detected"
      },
      "last1164": {
        "before": "not_detected",
        "after": "not_detected"
      },
      "prev200": {
        "before": "not_detected",
        "after": "not_detected"
      },
      "decision_only": {
        "before": "unsupported",
        "after": "not_detected"
      }
    },
    "extra_category_alarms": [
      "FCR-MINT"
    ]
  },
  "attempts": [
    {
      "index": 0,
      "phase": "initial",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d655a2c5e13dbb1de1dde1b49bad54b0a973366adb23f9f48fc538603b82adbd",
          "issue": "issue_ce69faf465e7daf0790b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "3e4ea58350f92e1a657dbc2cd70660172a6ef636de9cf0b92f622bb11bf5e4ad",
          "issue": "issue_0a624bc4c07906c276b8"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b57cad8746246fcd4788f0410afcf33a564e6842755a3ec3afdaf80a598a8620",
          "issue": "issue_4731c5b98888f4989040"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_37a479bde06c2608fc6e",
        "fact": "fact_19f4d98eb2680b709b88",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_55f0786392edf3bd6e8d",
        "fact": "fact_e8ce922e06a04eea9e89",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_59332f311fdee97458ad",
        "fact": "fact_32124e64ef52cd030b29",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_9a9eecd8b98589c39b90",
        "fact": "fact_4a564daa3ab23b456790",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_04ca6df29ce8070c17e3",
        "object_or_effect": "w_32133eb06a95b388bc11",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_32133eb06a95b388bc11",
        "grounded": true
      },
      {
        "id": "fact_19f4d98eb2680b709b88",
        "object_or_effect": "o_6115aaba696f9a0bde8c",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_2be3381b9f6bdb95edbc",
        "object_or_effect": "w_570db84ac56bb403b2fd",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_570db84ac56bb403b2fd",
        "grounded": true
      },
      {
        "id": "fact_32124e64ef52cd030b29",
        "object_or_effect": "o_0c4dfe9ddb848805b2a7",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_4a564daa3ab23b456790",
        "object_or_effect": "o_febe504014356e0d6889",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_5458f39f973df117a0e3",
        "object_or_effect": "w_c3f2590d63bb0b80014f",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c3f2590d63bb0b80014f",
        "grounded": true
      },
      {
        "id": "fact_6f61c30c1e89474f7c98",
        "object_or_effect": "w_215a19416d5933d05710",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_215a19416d5933d05710",
        "grounded": true
      },
      {
        "id": "fact_87ef5280f0a8465bfc4e",
        "object_or_effect": "w_fe40fe4cbcb26203c068",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_fe40fe4cbcb26203c068",
        "grounded": true
      },
      {
        "id": "fact_9372c58187dd5b6726b6",
        "object_or_effect": "w_50bfd03bd9a79d839212",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_50bfd03bd9a79d839212",
        "grounded": true
      },
      {
        "id": "fact_e8ce922e06a04eea9e89",
        "object_or_effect": "o_e1dcefab4a418987f445",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_ee7630818ccc4ffe405a",
        "object_or_effect": "w_f21ef6b70256288b477a",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_f21ef6b70256288b477a",
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 10
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 10
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "baseline_usable",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "direct_effect",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 114,
      "source_task_reading": 27,
      "no_debit_in_scope": 2,
      "new_entitlement": 1,
      "scope_missing": 1,
      "covered_holder_grant": 3,
      "external_dependency": 6,
      "parameter_only": 1
    }
  }
}
```

## RQ1_5add5c765bae

证据目录 run/members/RQ1_5add5c765bae/attempt_1/，报告哈希 c66f5c56889dc368718900fa00710ae9c5e04c4e8fd7a2d0a5d64b3c48de5e51

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "last1164 丢失根因 D2:513:original:2",
    "prev200 丢失根因 D2:513:original:2",
    "decision_only 丢失根因 D2:513:original:2"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope,unknown_assessment_vocabulary,unrelated_or_secondary_graph_pairs_deferred",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_5add5c765bae",
        "reference": "D2:513:original:1",
        "function": "disableContract",
        "v32": "FN",
        "last1164": "FN",
        "b5": "FN",
        "ACTaint_DeepSeek": "TP",
        "prev200": "FN",
        "decision_only": "FN",
        "prev200_findings": [],
        "decision_only_findings": [],
        "current": "FN"
      },
      {
        "member": "RQ1_5add5c765bae",
        "reference": "D2:513:original:2",
        "function": "setupMiniGame",
        "v32": "FN",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_d7f19c3d7377868e3554"
        ],
        "decision_only_findings": [
          "finding_9d55412c229e7382044a"
        ],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": []
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:513:original:2"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:513:original:2"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:513:original:2"
        ]
      }
    }
  },
  "attempts": [
    {
      "index": 0,
      "phase": "initial",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "15ca665059ff98f952183e2874de6e4ea6ca01f21fbe22d506c3e369156fb136",
          "issue": "issue_236a9235c5e107ede072"
        }
      ]
    },
    {
      "index": 1,
      "phase": "focused_revision",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": []
    }
  ],
  "FP_review": {
    "disappeared": [],
    "new": [],
    "disappeared_to_unknown": false,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_bd44274f8b32a7fa066e",
        "fact": "fact_34c6c30053cfcc7deeec",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_c82844a76e9569844453",
        "fact": "fact_002a8eb3e86357e4523a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_f47c94d987c2f4819109",
        "fact": "fact_7f6282bffd570ec3b130",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_002a8eb3e86357e4523a",
        "object_or_effect": "o_c7534baaa6f10876ba63",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_0b1c21633039ab686659",
        "object_or_effect": "w_9fda91e572d8bf79307a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_9fda91e572d8bf79307a",
        "grounded": true
      },
      {
        "id": "fact_34c6c30053cfcc7deeec",
        "object_or_effect": "o_db6ef4c4289df2fefdeb",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_7f6282bffd570ec3b130",
        "object_or_effect": "o_9964067d5780aee0d4f1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 9,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 19,
      "policy_missing": 3,
      "external_dependency": 4
    }
  }
}
```

## RQ1_5b3c7cbe3d9d

证据目录 run/members/RQ1_5b3c7cbe3d9d/attempt_1/，报告哈希 167de12434999045ff8a7f3c81ada0a3c8f62ce9ce44b3b129df19fc10b98486

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "alarm",
    "FCR-DESTROY": "alarm",
    "FCR-PAUSE": "alarm",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "decision_only 风险版漏检"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope,noncached_action_limit",
    "未决类别 FCR-DESTROY,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": true,
    "paired_id": "RQ1_0f3c3f400f6f",
    "state": "not_detected",
    "changes": {
      "v32": {
        "before": "not_detected",
        "after": "not_detected"
      },
      "last1164": {
        "before": "not_detected",
        "after": "not_detected"
      },
      "prev200": {
        "before": "not_detected",
        "after": "not_detected"
      },
      "decision_only": {
        "before": "unsupported",
        "after": "not_detected"
      }
    },
    "extra_category_alarms": [
      "FCR-MINT",
      "FCR-DESTROY",
      "FCR-PAUSE"
    ]
  },
  "attempts": [
    {
      "index": 0,
      "phase": "initial",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "471b7a198891c7c6afecda6bda1ebeeb0494e6faf7f70fac549a7f386fa5d36e"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "0ecbc9ed262d24418f1ccd84d115e23a1a54c1bdaaacbb5f3ed953fd4463d502"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "0d288552602c5a579e99fb7b9c4b853927bc653265d3a6786146e9128d778c16",
          "issue": "issue_9327d6d80719d48f63c8"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 17
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 18
      },
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 5
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "control_transition_preservation",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "financial_value",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "direct_effect",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "direct_effect",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 4,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "noncached_action_limit": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE",
      "FCR-MINT"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 276,
      "parameter_only": 1,
      "source_task_reading": 22,
      "scope_missing": 9,
      "program_support": 7
    }
  }
}
```

## RQ1_5e9adf3cda8c

证据目录 run/members/RQ1_5e9adf3cda8c/attempt_1/，报告哈希 333d26497abf54618c17fc2f109c8aaecac6bf78b49b6dc838957507f7de5e0e

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,invalid_semantic_row,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_5e9adf3cda8c",
        "reference": "D2:625:original:1",
        "function": "constructor",
        "v32": "FN",
        "last1164": "FN",
        "b5": "FN",
        "ACTaint_DeepSeek": "FN",
        "prev200": "FN",
        "decision_only": "FN",
        "prev200_findings": [],
        "decision_only_findings": [],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": []
      },
      "last1164": {
        "gained": [],
        "lost": []
      },
      "prev200": {
        "gained": [],
        "lost": []
      },
      "decision_only": {
        "gained": [],
        "lost": []
      }
    }
  },
  "attempts": [
    {
      "index": 0,
      "phase": "initial",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "471b7a198891c7c6afecda6bda1ebeeb0494e6faf7f70fac549a7f386fa5d36e"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        }
      ]
    },
    {
      "index": 1,
      "phase": "protocol_recovery",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": []
    }
  ],
  "FP_review": {
    "disappeared": [
      2872,
      3425
    ],
    "new": [],
    "disappeared_to_unknown": true,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_71ae9c964206fb76612c",
        "fact": "fact_af2e6a7ebfc32b34bd0e",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_af2e6a7ebfc32b34bd0e",
        "object_or_effect": "o_7ccc7f5f2938c097642f",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 3,
      "semantic_answer_outside_sent_scope": 2,
      "unbound_or_inapplicable_seed": 5
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 11,
      "external_dependency": 4,
      "source_task_reading": 2
    }
  }
}
```

## RQ1_5eee31e70615

证据目录 run/members/RQ1_5eee31e70615/attempt_1/，报告哈希 fc3f9ed905b0da5cac00a342533ae1a95fce8f555bbe1944b51a694becba596b

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "not_detected",
    "FCR-MINT": "not_detected",
    "FCR-DESTROY": "not_detected",
    "FCR-PAUSE": "not_detected",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "v32 风险版漏检",
    "last1164 风险版漏检",
    "prev200 风险版漏检",
    "decision_only 风险版漏检"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,unbound_or_inapplicable_seed"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": true,
    "paired_id": "RQ1_f322b5b8495d",
    "state": "not_detected",
    "changes": {
      "v32": {
        "before": "alarm",
        "after": "not_detected"
      },
      "last1164": {
        "before": "unsupported",
        "after": "not_detected"
      },
      "prev200": {
        "before": "alarm",
        "after": "not_detected"
      },
      "decision_only": {
        "before": "alarm",
        "after": "not_detected"
      }
    },
    "extra_category_alarms": []
  },
  "attempts": [
    {
      "index": 0,
      "phase": "initial",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "471b7a198891c7c6afecda6bda1ebeeb0494e6faf7f70fac549a7f386fa5d36e"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "0ecbc9ed262d24418f1ccd84d115e23a1a54c1bdaaacbb5f3ed953fd4463d502"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "389e49a25607c8aa0b24c6004a8e0e01f7ef86cd9829df21ad0ef4b1cd09a85a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "4456f87a5d8807d5dfb29f23f83417aa5e27829e239f8a3f07400814de290887"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "32bac5b03050321e057de04365dc2a512561a740452e71312c38d517446ea0c1"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "23a6538a9ed5b2f61822e0e7b5063a3598a192d13fc88c7a9ac1328ad4db6f82"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "00638788fa4178ee4b03762ed9848dcc750d2db36501d100c4e4f9e422f5e6db",
          "issue": "issue_5394ed8dbaa32ae29bf9"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a32ac33ee6942607fd733d2e8c556a2d37a9038735f9871d5e64cd9678b236b5",
          "issue": "issue_5394ed8dbaa32ae29bf9"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "54d2524d26a0229c3b95d1041f0b86cf9a959be139defd45f7da8315e83c8380",
          "issue": "issue_673049bf49ebdd42f1c3"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f713ecf66854e6ce7516ab59484d359e8f21d575abe281ee7e8885e76a985876",
          "issue": "issue_673049bf49ebdd42f1c3"
        }
      ]
    },
    {
      "index": 1,
      "phase": "focused_revision",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "cd4f9eb1678c96da89aabb5203d33e010ad6a87c7aec2b448c94514fd3886262",
          "issue": "issue_c3a938f642ba79359dc2"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c8e575e1fde62cea902c5c106342937ce16d628fa2aa3632818a4463c928184e",
          "issue": "issue_c3a938f642ba79359dc2"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_2b61ae4331034e187dc2",
        "fact": "fact_852a16f216f11cf009ae",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_6c9d3dce83567014aaec",
        "fact": "fact_3579b113e9103c5e42d5",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_3579b113e9103c5e42d5",
        "object_or_effect": "o_fe2c4bc38ed74dc11799",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_5950759a458021127004",
        "object_or_effect": "w_dee1585db6da28912da5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_dee1585db6da28912da5",
        "grounded": true
      },
      {
        "id": "fact_852a16f216f11cf009ae",
        "object_or_effect": "o_e20c12ee65d8d0c6880c",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_d32474331078bc893ee2",
        "object_or_effect": "w_d5ef78e25671c76152f3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d5ef78e25671c76152f3",
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 8,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 3,
      "unbound_or_inapplicable_seed": 1,
      "semantic_answer_outside_sent_scope": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": true,
    "negative_eligible_categories": [
      "FCR-DESTROY",
      "FCR-FREEZE",
      "FCR-MINT",
      "FCR-PAUSE",
      "FCR-TRANSFER"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 19,
      "source_task_reading": 1
    }
  }
}
```

## RQ1_62bedd2d4a5a

证据目录 run/members/RQ1_62bedd2d4a5a/attempt_1/，报告哈希 c4ffb7f2445ba70b554c0be82db1a5dff7b34f7e73521de234198b6e17c047e4

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:111:author:1",
    "last1164 丢失根因 D2:111:author:1",
    "prev200 丢失根因 D2:111:author:1",
    "decision_only 丢失根因 D2:111:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,unknown_assessment_vocabulary,no_locatable_source",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_62bedd2d4a5a",
        "reference": "D2:111:author:1",
        "function": "Constructor",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_368bc851b19e000e6620",
          "finding_b72ba58a90c429776a19",
          "finding_107f063ab1963dcd9975",
          "finding_9186570e266caa1f32bd",
          "finding_3aa3d48caea30b1cae83",
          "finding_efd4c267bbe7578f1965"
        ],
        "decision_only_findings": [
          "finding_4ab4f54c5b013e131f62",
          "finding_9f3c81b94565981c2d6c",
          "finding_6ea29a7d5add1ea0fb31"
        ],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:111:author:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:111:author:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:111:author:1"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:111:author:1"
        ]
      }
    }
  },
  "attempts": [
    {
      "index": 0,
      "phase": "initial",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "471b7a198891c7c6afecda6bda1ebeeb0494e6faf7f70fac549a7f386fa5d36e"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "0ecbc9ed262d24418f1ccd84d115e23a1a54c1bdaaacbb5f3ed953fd4463d502"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "389e49a25607c8aa0b24c6004a8e0e01f7ef86cd9829df21ad0ef4b1cd09a85a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "4456f87a5d8807d5dfb29f23f83417aa5e27829e239f8a3f07400814de290887"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f386e3938ce126ea408d7d3ae38f4078acc6fbdc78f38ca7f48f684bb437b44c",
          "issue": "issue_94cb858b4b6e7a72883f"
        }
      ]
    },
    {
      "index": 1,
      "phase": "protocol_recovery",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "471b7a198891c7c6afecda6bda1ebeeb0494e6faf7f70fac549a7f386fa5d36e"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "0ecbc9ed262d24418f1ccd84d115e23a1a54c1bdaaacbb5f3ed953fd4463d502"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "389e49a25607c8aa0b24c6004a8e0e01f7ef86cd9829df21ad0ef4b1cd09a85a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "23a6538a9ed5b2f61822e0e7b5063a3598a192d13fc88c7a9ac1328ad4db6f82"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [],
    "new": [],
    "disappeared_to_unknown": false,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 12,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 2,
      "no_locatable_source": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "model_phase_missing": 20,
      "no_effect_in_scope": 16,
      "external_dependency": 2
    }
  }
}
```

## RQ1_6476444da7e8

证据目录 run/members/RQ1_6476444da7e8/attempt_1/，报告哈希 13fb88ebbc8d7b46a9ffa094d5d751be096d8d13360d2d2b417304e1361dfeac

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "not_detected",
    "FCR-MINT": "not_detected",
    "FCR-DESTROY": "not_detected",
    "FCR-PAUSE": "not_detected",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "decision_only 未知转有效阴性"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,no_locatable_source,semantic_answer_outside_sent_scope"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": false,
    "paired_id": "RQ1_fe11616caf66",
    "state": "not_detected",
    "changes": {
      "v32": {
        "before": "not_detected",
        "after": "not_detected"
      },
      "last1164": {
        "before": "not_detected",
        "after": "not_detected"
      },
      "prev200": {
        "before": "not_detected",
        "after": "not_detected"
      },
      "decision_only": {
        "before": "unsupported",
        "after": "not_detected"
      }
    },
    "extra_category_alarms": []
  },
  "attempts": [
    {
      "index": 0,
      "phase": "initial",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "471b7a198891c7c6afecda6bda1ebeeb0494e6faf7f70fac549a7f386fa5d36e"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "0ecbc9ed262d24418f1ccd84d115e23a1a54c1bdaaacbb5f3ed953fd4463d502"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "389e49a25607c8aa0b24c6004a8e0e01f7ef86cd9829df21ad0ef4b1cd09a85a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "4456f87a5d8807d5dfb29f23f83417aa5e27829e239f8a3f07400814de290887"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "7f799a66ae376aa06c9a36f702733ca5338a0e850479f768cca6d3b3a59e2a0d",
          "issue": "issue_44814d40ea2b9d0e437f"
        }
      ]
    },
    {
      "index": 1,
      "phase": "protocol_recovery",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "087706736892499ae40183f740c86d84dbb87a140ecbc2fee7a730d720d70fde",
          "issue": "issue_2b968ddcaf9d262d5a42"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_4cb5b3fbc26b6289a300",
        "fact": "fact_fc9f2e06edffa54976d6",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_6287a99fd4c466d056e6",
        "fact": "fact_2784777be9a37d8e1707",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_a7e3a1c261ef77547b8d",
        "fact": "fact_da782efe6456915d0b3d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_2784777be9a37d8e1707",
        "object_or_effect": "o_d4e5450de26c4ad12f3a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_da782efe6456915d0b3d",
        "object_or_effect": "o_aa97963f1b0ab83c1bfe",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_fc9f2e06edffa54976d6",
        "object_or_effect": "o_8dd56873d88e669f7211",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 7,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "no_locatable_source": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": true,
    "negative_eligible_categories": [
      "FCR-DESTROY",
      "FCR-FREEZE",
      "FCR-MINT",
      "FCR-PAUSE",
      "FCR-TRANSFER"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 13,
      "scoped_counter": 1,
      "source_check_excluded": 1
    }
  }
}
```

## RQ1_6674f42c37b9

证据目录 run/members/RQ1_6674f42c37b9/attempt_1/，报告哈希 f9bec18284c9ea185a44afb3b633b3ad455fc26b05a121aaa4551e37ca25548f

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 semantic_answer_outside_sent_scope,program_investigation_seconds,invalid_semantic_row,category_ambiguous_or_outside_supported_task",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_6674f42c37b9",
        "reference": "D2:113:author:1",
        "function": "Ownable",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_9705148b237f40aaa764"
        ],
        "decision_only_findings": [
          "finding_74116cd7ada1155dcd3f"
        ],
        "current": "TP"
      }
    ],
    "findings": [
      {
        "idx": 8,
        "member": "RQ1_6674f42c37b9",
        "finding": "finding_52c652b439565c32a476",
        "function": "Ownable()",
        "location": {
          "file": "units/program.sol",
          "start": 3214,
          "length": 18,
          "ast_id": 406
        },
        "result": "TP",
        "reference": "D2:113:author:1",
        "group": "D2:113:author:1",
        "source_excerpt": "owner = msg.sender",
        "source_sha256": "735cd00265b10b7541a98fb75205dbda3295bc529d6d70c4d1f04747bb6f47a4",
        "note": "公开资格写入位于作者标定入口，实际语义支持与资格/下游检查对应。",
        "decision": {
          "status": "risk",
          "reason": "source_role_reassignment",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 3214. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 3214,
              "length": 18,
              "ast_id": 406
            }
          ],
          "effects": [
            "w_d1ef161e98f99ab83f54"
          ],
          "rules": [],
          "supports": [],
          "facts": [],
          "meanings": [],
          "origins": []
        },
        "evidence_refs": []
      }
    ],
    "changes": {
      "v32": {
        "gained": [],
        "lost": []
      },
      "last1164": {
        "gained": [],
        "lost": []
      },
      "prev200": {
        "gained": [],
        "lost": []
      },
      "decision_only": {
        "gained": [],
        "lost": []
      }
    }
  },
  "attempts": [
    {
      "index": 0,
      "phase": "initial",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": []
    },
    {
      "index": 1,
      "phase": "protocol_recovery",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "e401276ecf08e5e461f916aa093c93753271197d35561f3c18d0cff06cd5a99c",
          "issue": "issue_33fd06cfed280c900e5c"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b4ab11e65100d5c8d3426bd403c9ccfa58cb92bcc24ac8a0287eac14d7b1f58e",
          "issue": "issue_33fd06cfed280c900e5c"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "4179eb4db73e0579a9cb9b7f97e97adac0a8528645655c07dce0e89539fdd819",
          "issue": "issue_344423a647fa96da0afc"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f6511df9e08c3cdc098f519bd74553d32e02245c0b763170da886c4d657bdadb",
          "issue": "issue_344423a647fa96da0afc"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [],
    "new": [],
    "disappeared_to_unknown": false,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "semantic_answer_outside_sent_scope": 4,
      "program_investigation_seconds": 2,
      "semantic_budget": 1,
      "invalid_semantic_row": 2,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 12,
      "source_task_reading": 8,
      "external_dependency": 2,
      "policy_missing": 1,
      "source_role_reassignment": 1
    }
  }
}
```

## RQ1_67706b288d9c

证据目录 run/members/RQ1_67706b288d9c/attempt_1/，报告哈希 5b6f1f429c9f31de3f39aa7d79656103732ad62c6acfe4d4a2aa4afbb65daf21

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unrelated_or_secondary_graph_pairs_deferred,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [],
    "findings": [
      {
        "idx": 9,
        "member": "RQ1_67706b288d9c",
        "finding": "finding_a33b5f83f162d402770b",
        "function": "mix(uint256,uint256)",
        "location": {
          "file": "units/program.sol",
          "start": 4246,
          "length": 508,
          "ast_id": 578
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_67706b288d9c', 'units/program.sol', 4246)",
        "source_excerpt": "function mix(uint256 skinAId, uint256 skinBId) public whenNotPaused {\n        require(_isValidSkin(msg.sender, skinAId, skinBId));\n        require(_isNotOnSale(skinAId) && _isNotOnSale(skinBId));\n        require(_isCooldownReady(skinAId, skinBId));\n        require(_isNotMixing(skinAId, skinBId));\n        _setCooldownEndTime(skinAId, skinBId);\n        skins[skinAId].mixingWithId = uint64(skinBId);\n        skins[skinBId].mixingWithId = uint64(skinAId);\n        MixStart(msg.sender, skinAId, skinBId);\n    }",
        "source_sha256": "29b75cc954962d060182e0848048161d0960a18a756a9f9e839845d570286ca0",
        "note": "冻结参考无该根因，按参考外报警记录；未据此证明其业务上错误。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 4246. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 4246,
              "length": 508,
              "ast_id": 578
            }
          ],
          "effects": [],
          "rules": [],
          "supports": [],
          "facts": [],
          "meanings": [],
          "origins": [
            "source_observation",
            "scoped_program_check"
          ]
        },
        "evidence_refs": [
          "E1",
          "E7"
        ]
      },
      {
        "idx": 10,
        "member": "RQ1_67706b288d9c",
        "finding": "finding_bcf11c9fb823d74eb946",
        "function": "mix(uint256,uint256)",
        "location": {
          "file": "units/program.sol",
          "start": 4246,
          "length": 508,
          "ast_id": 578
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_67706b288d9c', 'units/program.sol', 4246)",
        "source_excerpt": "function mix(uint256 skinAId, uint256 skinBId) public whenNotPaused {\n        require(_isValidSkin(msg.sender, skinAId, skinBId));\n        require(_isNotOnSale(skinAId) && _isNotOnSale(skinBId));\n        require(_isCooldownReady(skinAId, skinBId));\n        require(_isNotMixing(skinAId, skinBId));\n        _setCooldownEndTime(skinAId, skinBId);\n        skins[skinAId].mixingWithId = uint64(skinBId);\n        skins[skinBId].mixingWithId = uint64(skinAId);\n        MixStart(msg.sender, skinAId, skinBId);\n    }",
        "source_sha256": "29b75cc954962d060182e0848048161d0960a18a756a9f9e839845d570286ca0",
        "note": "冻结参考无该根因，按参考外报警记录；未据此证明其业务上错误。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 4246. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 4246,
              "length": 508,
              "ast_id": 578
            }
          ],
          "effects": [],
          "rules": [],
          "supports": [],
          "facts": [],
          "meanings": [],
          "origins": [
            "source_observation",
            "scoped_program_check"
          ]
        },
        "evidence_refs": [
          "E15",
          "E5"
        ]
      },
      {
        "idx": 11,
        "member": "RQ1_67706b288d9c",
        "finding": "finding_a139225c8b462a58d2a4",
        "function": "mix(uint256,uint256)",
        "location": {
          "file": "units/program.sol",
          "start": 4246,
          "length": 508,
          "ast_id": 578
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_67706b288d9c', 'units/program.sol', 4246)",
        "source_excerpt": "function mix(uint256 skinAId, uint256 skinBId) public whenNotPaused {\n        require(_isValidSkin(msg.sender, skinAId, skinBId));\n        require(_isNotOnSale(skinAId) && _isNotOnSale(skinBId));\n        require(_isCooldownReady(skinAId, skinBId));\n        require(_isNotMixing(skinAId, skinBId));\n        _setCooldownEndTime(skinAId, skinBId);\n        skins[skinAId].mixingWithId = uint64(skinBId);\n        skins[skinBId].mixingWithId = uint64(skinAId);\n        MixStart(msg.sender, skinAId, skinBId);\n    }",
        "source_sha256": "29b75cc954962d060182e0848048161d0960a18a756a9f9e839845d570286ca0",
        "note": "冻结参考无该根因，按参考外报警记录；未据此证明其业务上错误。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 4246. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 4246,
              "length": 508,
              "ast_id": 578
            }
          ],
          "effects": [],
          "rules": [],
          "supports": [],
          "facts": [],
          "meanings": [],
          "origins": [
            "source_observation",
            "scoped_program_check"
          ]
        },
        "evidence_refs": [
          "E11",
          "E3"
        ]
      }
    ],
    "changes": {
      "v32": {
        "gained": [],
        "lost": []
      },
      "last1164": {
        "gained": [],
        "lost": []
      },
      "prev200": {
        "gained": [],
        "lost": []
      },
      "decision_only": {
        "gained": [],
        "lost": []
      }
    }
  },
  "attempts": [
    {
      "index": 0,
      "phase": "initial",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "471b7a198891c7c6afecda6bda1ebeeb0494e6faf7f70fac549a7f386fa5d36e"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "0ecbc9ed262d24418f1ccd84d115e23a1a54c1bdaaacbb5f3ed953fd4463d502"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "389e49a25607c8aa0b24c6004a8e0e01f7ef86cd9829df21ad0ef4b1cd09a85a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "8369e0e36c9d44ccdbb537ec9a3830028f31505786b0f1745024b8addbd31e75",
          "issue": "issue_bc8d40f0495e32ef441c"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "914b460b381e6523e167ffad8018defd028da7d0e7574cbdb1f57573d2d2d6a0",
          "issue": "issue_bc8d40f0495e32ef441c"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "2e5e06cf845a5fb7180251004c6507bc9e22707271d111fd366fd78cbec491de",
          "issue": "issue_61d11e49aab986442ed1"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "3c44ab33f41806c089266cd24abfd03eea114af48e516185f03e333ef6696b94",
          "issue": "issue_61d11e49aab986442ed1"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [],
    "new": [],
    "disappeared_to_unknown": false,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "authorization_violation",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 6
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 3
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 5,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 51,
      "source_task_reading": 39,
      "external_dependency": 8,
      "program_support": 3
    }
  }
}
```

## RQ1_679bfbe1c927

证据目录 run/members/RQ1_679bfbe1c927/attempt_1/，报告哈希 cde382585d5fead54bdc4fbe448a886a6fcff65a17f8376f192a44943e5826f2

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,invalid_semantic_row,semantic_answer_outside_sent_scope,unbound_or_inapplicable_seed",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_679bfbe1c927",
        "reference": "D2:334:author:1",
        "function": "Constructor",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_eb5b6880bbf2ad1a6e11",
          "finding_4d88817f757c0bf1b069",
          "finding_b8a55ad70ff6ead23371"
        ],
        "decision_only_findings": [
          "finding_2b61a44d19eaead70d8a"
        ],
        "current": "TP"
      }
    ],
    "findings": [
      {
        "idx": 12,
        "member": "RQ1_679bfbe1c927",
        "finding": "finding_848230a6007c154a12d5",
        "function": "Constructor()",
        "location": {
          "file": "units/program.sol",
          "start": 793,
          "length": 18,
          "ast_id": 113
        },
        "result": "TP",
        "reference": "D2:334:author:1",
        "group": "D2:334:author:1",
        "source_excerpt": "owner = msg.sender",
        "source_sha256": "5108c847a2dc4ed5cf5a072eeb5dea89c841310045fb9e35979d15e3569eaf42",
        "note": "公开资格写入位于作者标定入口，实际语义支持与资格/下游检查对应。",
        "decision": {
          "status": "risk",
          "reason": "source_role_reassignment",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 793. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 793,
              "length": 18,
              "ast_id": 113
            }
          ],
          "effects": [
            "w_4868c618d8c5b556404c"
          ],
          "rules": [],
          "supports": [],
          "facts": [],
          "meanings": [],
          "origins": [
            "source_observation"
          ]
        },
        "evidence_refs": [
          "E1",
          "E2"
        ]
      },
      {
        "idx": 13,
        "member": "RQ1_679bfbe1c927",
        "finding": "finding_84d284d3997049a13db8",
        "function": "transferOwnership(address)",
        "location": {
          "file": "units/program.sol",
          "start": 899,
          "length": 100,
          "ast_id": 139
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_679bfbe1c927', 'units/program.sol', 899)",
        "source_excerpt": "function transferOwnership(address _newOwner) public onlyOwner {\n        newOwner = _newOwner;\n    }",
        "source_sha256": "5108c847a2dc4ed5cf5a072eeb5dea89c841310045fb9e35979d15e3569eaf42",
        "note": "实际报警入口或影响与作者参考不同，不能抵销该独立根因漏检。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 899 under current_authority_required, eligibility_state, management_role. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 899,
              "length": 100,
              "ast_id": 139
            }
          ],
          "effects": [],
          "rules": [
            "P03",
            "P05",
            "P06"
          ],
          "supports": [
            "source_692b0230979c5208f834",
            "support_0825e513d4910ad2713c",
            "support_2bf2132bbb725e2ddec5",
            "support_6a77bc0a50c02b2ad8cf"
          ],
          "facts": [
            "fact_08011df7ec0d5196fd5f",
            "fact_433530bd4ce1dada328f",
            "fact_c04ffe1604aaf40ae777"
          ],
          "meanings": [
            "current_authority_required",
            "eligibility_state",
            "management_role"
          ],
          "origins": [
            "source_observation",
            "verified_service",
            "rule_derivation",
            "scoped_program_check"
          ]
        },
        "evidence_refs": [
          "E13",
          "E17"
        ]
      }
    ],
    "changes": {
      "v32": {
        "gained": [],
        "lost": []
      },
      "last1164": {
        "gained": [],
        "lost": []
      },
      "prev200": {
        "gained": [],
        "lost": []
      },
      "decision_only": {
        "gained": [],
        "lost": []
      }
    }
  },
  "attempts": [
    {
      "index": 0,
      "phase": "initial",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": [
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "471b7a198891c7c6afecda6bda1ebeeb0494e6faf7f70fac549a7f386fa5d36e"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "0ecbc9ed262d24418f1ccd84d115e23a1a54c1bdaaacbb5f3ed953fd4463d502"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "23a6538a9ed5b2f61822e0e7b5063a3598a192d13fc88c7a9ac1328ad4db6f82"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "fb769acb9b1ea016bf1b9449491d4f6f38073a6ae1fec58d07a38a07f34efee2",
          "issue": "issue_707a932580a234cc7f98"
        }
      ]
    },
    {
      "index": 1,
      "phase": "focused_revision",
      "response_kind": "substantive",
      "usable": true,
      "status": "analysis_received",
      "normalization_diagnostics": []
    }
  ],
  "FP_review": {
    "disappeared": [
      2337
    ],
    "new": [
      899
    ],
    "disappeared_to_unknown": false,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_0825e513d4910ad2713c",
        "fact": "fact_433530bd4ce1dada328f",
        "origin": "verified_service",
        "field": "policies",
        "version": 1
      },
      {
        "support": "support_2bf2132bbb725e2ddec5",
        "fact": "fact_c04ffe1604aaf40ae777",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_6a77bc0a50c02b2ad8cf",
        "fact": "fact_10b7b33fa28ce90f2632",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_a3ab06314044609098f6",
        "fact": "fact_ce56d9272958f138bb3c",
        "origin": "verified_service",
        "field": "policies",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_0563e57c56aa74e66761",
        "object_or_effect": "w_799311e8184bd8ad246c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_799311e8184bd8ad246c",
        "grounded": true
      },
      {
        "id": "fact_06ff9b6b5c4353336de3",
        "object_or_effect": "w_0da1a6602ff7d5846f50",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0da1a6602ff7d5846f50",
        "grounded": true
      },
      {
        "id": "fact_08011df7ec0d5196fd5f",
        "object_or_effect": "w_d9ef9f52797408795db5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d9ef9f52797408795db5",
        "grounded": true
      },
      {
        "id": "fact_0806471ab804ac74a655",
        "object_or_effect": "w_eb9c4aaf650ebc5481d3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_eb9c4aaf650ebc5481d3",
        "grounded": true
      },
      {
        "id": "fact_10b7b33fa28ce90f2632",
        "object_or_effect": "o_7b47ee53d58784ac0560",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_1a4188df9bf0c08b4acb",
        "object_or_effect": "w_6164490d92c55f2b31b4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6164490d92c55f2b31b4",
        "grounded": true
      },
      {
        "id": "fact_418cd65566bca427f85b",
        "object_or_effect": "w_089a9deb4057e65220b5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_089a9deb4057e65220b5",
        "grounded": true
      },
      {
        "id": "fact_433530bd4ce1dada328f",
        "object_or_effect": "w_d9ef9f52797408795db5",
        "meaning": "current_authority_required",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_bc590a68b39feb0fb4d5",
        "object_or_effect": "w_7a28a26cf45dfbef6ae9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7a28a26cf45dfbef6ae9",
        "grounded": true
      },
      {
        "id": "fact_c04ffe1604aaf40ae777",
        "object_or_effect": "o_725c9a8ab90d57c4fb28",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_ce56d9272958f138bb3c",
        "object_or_effect": "w_7a28a26cf45dfbef6ae9",
        "meaning": "holder_authorization_applies",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "authorization_violation",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 6
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 6
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 6
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 5,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 2,
      "unbound_or_inapplicable_seed": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 6
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "unassessed_role_change": 5,
      "source_role_reassignment": 1,
      "no_effect_in_scope": 21,
      "source_task_reading": 10,
      "external_dependency": 3,
      "policy_missing": 2,
      "program_support": 1
    }
  }
}
```
