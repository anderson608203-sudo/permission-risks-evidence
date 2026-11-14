# 逐例审阅

## RQ1_e5e40ec6feca

证据目录 run/members/RQ1_e5e40ec6feca/attempt_1/，报告哈希 50290df903947a97840484bfda9d2a6f149f29e4971e4db8a9a13c09b64ffc84

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [
    "v32 新增根因 D2:572:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_e5e40ec6feca",
        "reference": "D2:572:author:1",
        "function": "destroy",
        "v32": "FN",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_b4198815ec171602004d"
        ],
        "decision_only_findings": [
          "finding_9d5de296a4534287cd37"
        ],
        "current": "TP"
      }
    ],
    "findings": [
      {
        "idx": 26,
        "member": "RQ1_e5e40ec6feca",
        "finding": "finding_fdf6996a99c20eacfc9f",
        "function": "destroy()",
        "location": {
          "file": "units/program.sol",
          "start": 194,
          "length": 54,
          "ast_id": 27
        },
        "result": "TP",
        "reference": "D2:572:author:1",
        "group": "D2:572:author:1",
        "source_excerpt": "function destroy(){\n        selfdestruct(owner);\n    }",
        "source_sha256": "2756ed6f4df948c9c34dbf8e57241e05ecc33a5caa1503b3fb1e71e7959e5165",
        "note": "实际入口及源码效果与作者独立根因对应，保留程序证据可审计性限制。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 194. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 194,
              "length": 54,
              "ast_id": 27
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
          "E2"
        ]
      }
    ],
    "changes": {
      "v32": {
        "gained": [
          "D2:572:author:1"
        ],
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a0784858540cc7dd7e7adc3d952ef4b8c43f598a01e90643c7c972b0da67ed0d",
          "issue": "issue_c96a8723f100ed51245f"
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
        "count": 1
      },
      {
        "label": "authorization_violation",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 3,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": true,
    "negative_eligible_categories": [
      "AC"
    ],
    "obligation_bases": {
      "program_support": 1,
      "no_effect_in_scope": 1
    }
  }
}
```

## RQ1_e5f934bea8ec

证据目录 run/members/RQ1_e5f934bea8ec/attempt_1/，报告哈希 479819ed730d27591d73bc83cd1d48669dd7175bb0d19322190cd497f4ac77ee

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 semantic_answer_outside_sent_scope,invalid_semantic_row,unrelated_or_secondary_graph_pairs_deferred",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [],
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "471b7a198891c7c6afecda6bda1ebeeb0494e6faf7f70fac549a7f386fa5d36e"
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
    "supports": [
      {
        "support": "support_c0c8e1e86fb483f921a2",
        "fact": "fact_12d72ba1db44957863ba",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_c42dd8b8c7ce6f9ef696",
        "fact": "fact_7c3cb4310e53c406c2a9",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_12d72ba1db44957863ba",
        "object_or_effect": "o_45911bea898a819f97ba",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_2560406ab565a1d870a4",
        "object_or_effect": "w_d8e77f83b590a3d64f66",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_d8e77f83b590a3d64f66",
        "grounded": true
      },
      {
        "id": "fact_32dc86a2f6628e5d5a5a",
        "object_or_effect": "w_b4ec93b1e93d85c52ad8",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_b4ec93b1e93d85c52ad8",
        "grounded": true
      },
      {
        "id": "fact_54d98aa48911ebce2e0a",
        "object_or_effect": "w_3b747939b3d5c20d21c6",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_3b747939b3d5c20d21c6",
        "grounded": true
      },
      {
        "id": "fact_7c3cb4310e53c406c2a9",
        "object_or_effect": "o_98e2d833b2e63d4dbc45",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_91181f8400422db6b665",
        "object_or_effect": "w_c2686ac667e9e5ed9440",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c2686ac667e9e5ed9440",
        "grounded": true
      },
      {
        "id": "fact_9399fb41d680f22cd228",
        "object_or_effect": "w_4ca08634f6e744c1ce6f",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_4ca08634f6e744c1ce6f",
        "grounded": true
      },
      {
        "id": "fact_bd6f0140b8edddc3fa60",
        "object_or_effect": "w_fbb6d8b65fabcee5a1d9",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_fbb6d8b65fabcee5a1d9",
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 2,
      "semantic_answer_outside_sent_scope": 4,
      "unrelated_or_secondary_graph_pairs_deferred": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 25,
      "external_dependency": 10,
      "source_context_missing": 1,
      "source_task_reading": 11,
      "policy_missing": 2
    }
  }
}
```

## RQ1_e6f04047bff4

证据目录 run/members/RQ1_e6f04047bff4/attempt_1/，报告哈希 9f0097d2be7f0f29dc154afa05f32879b7b68e98a0745116750511c64931ee91

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:37:original:1",
    "last1164 丢失根因 D2:37:original:1",
    "prev200 丢失根因 D2:37:original:1",
    "decision_only 丢失根因 D2:37:original:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope,unrelated_or_secondary_graph_pairs_deferred,invalid_semantic_row",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_e6f04047bff4",
        "reference": "D2:37:original:1",
        "function": "RegisterDevice",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_d01629e724b44c0bca08"
        ],
        "decision_only_findings": [
          "finding_c410e5f24d06aa1b5d55"
        ],
        "current": "FN"
      },
      {
        "member": "RQ1_e6f04047bff4",
        "reference": "D2:37:original:2",
        "function": "CollectMoney",
        "v32": "FN",
        "last1164": "FN",
        "b5": "FN",
        "ACTaint_DeepSeek": "TP",
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
        "lost": [
          "D2:37:original:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:37:original:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:37:original:1"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:37:original:1"
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
      "normalization_diagnostics": []
    },
    {
      "index": 1,
      "phase": "focused_revision",
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
          "detail_sha256": "bd743f7d426b68edf85506e4d09b3da18dc89b3951f4c3e1c243b6ba84170b27",
          "issue": "issue_f6632e95be77a51da6d2"
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
    "supports": [
      {
        "support": "support_5f77e9240b619af78cb5",
        "fact": "fact_8b0e5b928a43c93754a5",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_67ffe9c50fd4b85bd0ce",
        "fact": "fact_5a8788cdd5a05ed16331",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_a809f0e496dc26f52e26",
        "fact": "fact_0933294f71e5b72b6596",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_a8f9f6090eda1eb81049",
        "fact": "fact_0933294f71e5b72b6596",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_b32f3bcd0785cf112dbd",
        "fact": "fact_5a8788cdd5a05ed16331",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_0933294f71e5b72b6596",
        "object_or_effect": "o_e77191c84496e6ce89fa",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_3d5206f13b349404137a",
        "object_or_effect": "w_b7d69a027b60f8a8f78f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b7d69a027b60f8a8f78f",
        "grounded": true
      },
      {
        "id": "fact_5a8788cdd5a05ed16331",
        "object_or_effect": "o_4950729e8d1fbfbfca75",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_8b0e5b928a43c93754a5",
        "object_or_effect": "o_802393c11e93aa0d237b",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_c954040d6bacb82a4e61",
        "object_or_effect": "w_f5f956b18cfa59ff6249",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f5f956b18cfa59ff6249",
        "grounded": true
      },
      {
        "id": "fact_fd8962e78cb3798411ad",
        "object_or_effect": "w_41360f0b0879a189ecdc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_41360f0b0879a189ecdc",
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 2
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 1,
      "invalid_semantic_row": 1,
      "unknown_assessment_vocabulary": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 6,
      "policy_missing": 2,
      "source_task_reading": 2
    }
  }
}
```

## RQ1_e73c99ca23e5

证据目录 run/members/RQ1_e73c99ca23e5/attempt_1/，报告哈希 ffca7596fe30a6edd4fd04d8da9938e5270feb925978d4c2e976df169b61e82e

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "alarm",
    "FCR-MINT": "unsupported",
    "FCR-DESTROY": "alarm",
    "FCR-PAUSE": "alarm",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,shared_declaration_in_distinct_applied_contexts,no_locatable_source",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": true,
    "paired_id": "RQ1_1f06ce07140f",
    "state": "alarm",
    "changes": {
      "v32": {
        "before": "alarm",
        "after": "alarm"
      },
      "last1164": {
        "before": "alarm",
        "after": "alarm"
      },
      "prev200": {
        "before": "alarm",
        "after": "alarm"
      },
      "decision_only": {
        "before": "alarm",
        "after": "alarm"
      }
    },
    "extra_category_alarms": [
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a30fec8de8a9600f09b12cc1b70404f9cac9a233dadf723a8ee42a6f2ba6ce07",
          "issue": "issue_f9a11159c4dc60c5f056"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "0ed878e2f5cb94e9895da7ea57c4c73dbb30d94d3a4693abce762e8e57d73f11",
          "issue": "issue_75524843181c1b446cf5"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_0d9037fabd56e3c52db3",
        "fact": "fact_27196f815c2583ff7ebe",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_27196f815c2583ff7ebe",
        "object_or_effect": "o_b817254c37a071188dc6",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 5
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
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 24
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 24
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 8
      },
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "direct_effect",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "direct_effect",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "baseline_usable",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 2
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
        "label": "financial_block",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "control_transition_preservation",
        "answer": "unsat",
        "count": 4
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "unknown_assessment_vocabulary": 2,
      "shared_declaration_in_distinct_applied_contexts": 1,
      "no_locatable_source": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 1,
      "noncached_action_limit": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 197,
      "source_task_reading": 34,
      "scope_missing": 6,
      "external_dependency": 8,
      "program_support": 4,
      "covered_holder_grant": 1
    }
  }
}
```

## RQ1_e7801f3e61cb

证据目录 run/members/RQ1_e7801f3e61cb/attempt_1/，报告哈希 de7d24249b4939cef54c4b2a64c22433d3dfb03b3accda878a23dcc3b388718c

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,invalid_semantic_row,unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [],
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
    "disappeared": [],
    "new": [],
    "disappeared_to_unknown": false,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_41d59c002f176f03577a",
        "fact": "fact_1b9bb9f3b2ec9cea219b",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_92805bc8f96468ab425f",
        "fact": "fact_b8b4701dd39628c535e1",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_182fd44e787c42fa9d95",
        "object_or_effect": "w_e4ec25d158f4ceffe76c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_e4ec25d158f4ceffe76c",
        "grounded": true
      },
      {
        "id": "fact_1b9bb9f3b2ec9cea219b",
        "object_or_effect": "o_46dd4647127be50eb20e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_3e34d09bdf8fd0046290",
        "object_or_effect": "w_f29a610eb5f3a3be8a56",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_f29a610eb5f3a3be8a56",
        "grounded": true
      },
      {
        "id": "fact_5211e107e1bd2a69f021",
        "object_or_effect": "w_dfe995a96bc52495bdb3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_dfe995a96bc52495bdb3",
        "grounded": true
      },
      {
        "id": "fact_81265fabd77cb68dcd82",
        "object_or_effect": "w_12acfb9ee06c505d13aa",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_12acfb9ee06c505d13aa",
        "grounded": true
      },
      {
        "id": "fact_823b92ebe68fc869d774",
        "object_or_effect": "w_cdd475e43c57b0ba924a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_cdd475e43c57b0ba924a",
        "grounded": true
      },
      {
        "id": "fact_865cebf591994827f0ea",
        "object_or_effect": "w_6624f99d85341da6d184",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6624f99d85341da6d184",
        "grounded": true
      },
      {
        "id": "fact_98671795096c893ad5cd",
        "object_or_effect": "w_d449aeca72b306d765c4",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d449aeca72b306d765c4",
        "grounded": true
      },
      {
        "id": "fact_a421a62b74751ba0b032",
        "object_or_effect": "w_b1567b1c7d90b9f8acdc",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b1567b1c7d90b9f8acdc",
        "grounded": true
      },
      {
        "id": "fact_b5780add485db84a232e",
        "object_or_effect": "w_be555d7d0f33aff1e0de",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_be555d7d0f33aff1e0de",
        "grounded": true
      },
      {
        "id": "fact_b8b4701dd39628c535e1",
        "object_or_effect": "o_13442fb547cf59702bac",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_bfff5f95ba68efbb41fe",
        "object_or_effect": "w_d2ce4fe3e31ae3ceddeb",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d2ce4fe3e31ae3ceddeb",
        "grounded": true
      },
      {
        "id": "fact_edacf78dd7a50b737c54",
        "object_or_effect": "w_269fe2c12dfbcda1eb82",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_269fe2c12dfbcda1eb82",
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 14
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 14
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 14
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 6,
      "semantic_answer_outside_sent_scope": 2,
      "unbound_or_inapplicable_seed": 3,
      "unrelated_or_secondary_graph_pairs_deferred": 8
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "source_task_reading": 17,
      "no_effect_in_scope": 57,
      "unassessed_role_change": 16,
      "external_dependency": 24,
      "source_context_missing": 20,
      "policy_missing": 8
    }
  }
}
```

## RQ1_e85ac4a50ee4

证据目录 run/members/RQ1_e85ac4a50ee4/attempt_1/，报告哈希 4e7d4fa21c1e390ac3ca0874f7e4accee69f3681e5c003ca56938cb77dab7abf

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "last1164 丢失根因 D2:57:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unknown_assessment_vocabulary,semantic_answer_outside_sent_scope,unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_e85ac4a50ee4",
        "reference": "D2:57:author:1",
        "function": "kill",
        "v32": "FN",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
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
        "lost": [
          "D2:57:author:1"
        ]
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "24babd6c940123e676c1d4ca4e74bebffecce2662bf9bfacc9d2f8c116a0f61f",
          "issue": "issue_856ff23c8478bab877bd"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "fb41e4b7a1eb97ac974f47fad899ddfa747d5629f58ced2cbf67470c85bcb4b6",
          "issue": "issue_84a98c14d823608ac4ed"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "611f93834a97cefac3862079314b04391a77a376478bff15385d070aadc7d07f",
          "issue": "issue_84a98c14d823608ac4ed"
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
    "supports": [
      {
        "support": "support_67c89399e974852d2fc6",
        "fact": "fact_200a4c2a4413d05bb157",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_790e98074016d914ddf0",
        "fact": "fact_ffa722f4221c17b040ca",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_200a4c2a4413d05bb157",
        "object_or_effect": "o_6204bdc11c7001356d30",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_ffa722f4221c17b040ca",
        "object_or_effect": "o_6ce0a1a0a8ef6befd502",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 2
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 1,
      "unknown_assessment_vocabulary": 2,
      "category_ambiguous_or_outside_supported_task": 1,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 7,
      "policy_missing": 1,
      "source_task_reading": 2
    }
  }
}
```

## RQ1_e97f2d279ad9

证据目录 run/members/RQ1_e97f2d279ad9/attempt_1/，报告哈希 c086dd8a548a584f57679f53493775b637aa88211c4ac38ce1de88fd567d88e3

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:47:S1",
    "last1164 丢失根因 D2:47:S1,D2:47:S2",
    "prev200 丢失根因 D2:47:S1",
    "decision_only 丢失根因 D2:47:S1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unrelated_or_secondary_graph_pairs_deferred,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_e97f2d279ad9",
        "reference": "D2:47:S1",
        "function": "Prosperity",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_198e21d1c689a9f8503a"
        ],
        "decision_only_findings": [
          "finding_1779233183c27e5e2b1b"
        ],
        "current": "FN"
      },
      {
        "member": "RQ1_e97f2d279ad9",
        "reference": "D2:47:S2",
        "function": "giveBlockReward",
        "v32": "FN",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
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
        "lost": [
          "D2:47:S1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:47:S1",
          "D2:47:S2"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:47:S1"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:47:S1"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "f3123ac6c872a9278452500a4e431f1dc817cf9217a075a77fe6dcd8262b0c11",
          "issue": "issue_fd6153f26e1303f9fcf8"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "4b45c47a92b5e623d24b92e9d9542bed425be336e29f3038593fff9376dcf3eb",
          "issue": "issue_fd6153f26e1303f9fcf8"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "0b030a5385c8f0d91fc5faa055ff58319e7e476155d16f7a9fc491cc5d93c4b6",
          "issue": "issue_12540e1ee620c2e1a027"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "2682743aee6b0954786e9593f5c89c7f2ddb32dd12e7c313737eb69d50126f21",
          "issue": "issue_12540e1ee620c2e1a027"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "6f6c0f204a99162eb322a75b82c7845e978d8c24326a08223554674f472b0e85",
          "issue": "issue_d373ae6d7e7662831ad2"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "5797e05813543d125b6fb8d59ec2778119a7b7c529602a520f0480a994fe3d52",
          "issue": "issue_d373ae6d7e7662831ad2"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [
      1998
    ],
    "new": [],
    "disappeared_to_unknown": true,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 6
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 6
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 4
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 6,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 4
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 16,
      "source_task_reading": 15,
      "policy_missing": 4,
      "external_dependency": 2
    }
  }
}
```

## RQ1_eb30c6dee989

证据目录 run/members/RQ1_eb30c6dee989/attempt_1/，报告哈希 3eccb2d7245643d7f1fa5427480f51263b10b13763d7b7795c455637ca2d8322

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "unsupported",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "unsupported",
    "FCR-FREEZE": "unsupported"
  },
  "changes": [
    "v32 退为未知，不能当作纠正",
    "last1164 退为未知，不能当作纠正",
    "prev200 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": true,
    "paired_id": "RQ1_ee2aa7f32d31",
    "state": "unsupported",
    "changes": {
      "v32": {
        "before": "not_detected",
        "after": "unsupported"
      },
      "last1164": {
        "before": "not_detected",
        "after": "unsupported"
      },
      "prev200": {
        "before": "not_detected",
        "after": "unsupported"
      },
      "decision_only": {
        "before": "unsupported",
        "after": "unsupported"
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "23a6538a9ed5b2f61822e0e7b5063a3598a192d13fc88c7a9ac1328ad4db6f82"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "cee0542d77aa80b2b2e09e869e1228717326d03ce58c727ecb5bd5a5f1b17994",
          "issue": "issue_da4f8d122c04825e3360"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "6f83d616d0f1928481ed9be14c1188a5a68f7c558461e6797c5bb1b0317f7706",
          "issue": "issue_da4f8d122c04825e3360"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "e3a088d8f46279c0665377de0fa760fd7e9747b08cf75de5537c838b8d1ff320",
          "issue": "issue_9c3dc2e01bcd1239e3c4"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "8eb9188b62ccbc082f8dd4cb4d0d31f0478f2f3817473cc6cc33a61c04aea13a",
          "issue": "issue_9c3dc2e01bcd1239e3c4"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 13,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 2,
      "no_locatable_source": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 96,
      "model_phase_missing": 18,
      "external_dependency": 6
    }
  }
}
```

## RQ1_ee2aa7f32d31

证据目录 run/members/RQ1_ee2aa7f32d31/attempt_1/，报告哈希 0b1fa78b322b9325bff2f9c09844fa7e1700f0c64847821f751497ef1be00eec

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "unsupported",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "unsupported",
    "FCR-FREEZE": "unsupported"
  },
  "changes": [
    "v32 退为未知，不能当作纠正",
    "prev200 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": false,
    "paired_id": "RQ1_eb30c6dee989",
    "state": "unsupported",
    "changes": {
      "v32": {
        "before": "not_detected",
        "after": "unsupported"
      },
      "last1164": {
        "before": "unsupported",
        "after": "unsupported"
      },
      "prev200": {
        "before": "not_detected",
        "after": "unsupported"
      },
      "decision_only": {
        "before": "unsupported",
        "after": "unsupported"
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 7,
      "semantic_answer_outside_sent_scope": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 99,
      "model_phase_missing": 15,
      "external_dependency": 6
    }
  }
}
```

## RQ1_f322b5b8495d

证据目录 run/members/RQ1_f322b5b8495d/attempt_1/，报告哈希 3b489c1db1b95e49deddc3fab08204472136919cce0224e184d0faa899633af4

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unbound_or_inapplicable_seed,unknown_assessment_vocabulary"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": false,
    "paired_id": "RQ1_5eee31e70615",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "61bc000bfd734cf2b1a2715b8be10c63ced41925573159e7d9fc25c7f627d636",
          "issue": "issue_3646418f2c0b00b14310"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "2ad9ddad86ff1b944b076ebd8b678ccfda2334e234bae3daab33f3693077c7da",
          "issue": "issue_1de53ebc7c82af7087b8"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "invalid_semantic_row": 4,
      "unknown_assessment_vocabulary": 2
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
      "no_effect_in_scope": 18,
      "source_check_excluded": 2
    }
  }
}
```
