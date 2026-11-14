# 逐例审阅

## RQ1_b61f163309a1

证据目录 run/members/RQ1_b61f163309a1/attempt_1/，报告哈希 b5f6484cff4ee86c0b8e4e86a4a8ad1bf6661b5585f633d36b6dbddd7d776651

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "alarm",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "not_detected",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "decision_only 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,unrelated_or_secondary_graph_pairs_deferred,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": true,
    "paired_id": "RQ1_81a85f242b60",
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
        "before": "unsupported",
        "after": "alarm"
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "5c400205dc463daa9ac4216d21e07b321cb67f7e98b943b9c52c1e491309757f",
          "issue": "issue_674cef7acc2aaa56f106"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b7f484f3c3dab8ea4e3ada70c5889f4cf80f5b777de800fb68deb0502798ce54",
          "issue": "issue_64e3f14724ba14e60cc8"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_1253f5f79de5d9295a49",
        "fact": "fact_0b6a1566374dfde9b567",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_1d4860f927a79eecfd0a",
        "fact": "fact_871f783636e663042eda",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_0b6a1566374dfde9b567",
        "object_or_effect": "o_f1c0cbc23d1d63b3f88f",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_0ca603b3300e0ce0268b",
        "object_or_effect": "w_c622c7b6295d1a625a78",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c622c7b6295d1a625a78",
        "grounded": true
      },
      {
        "id": "fact_7848855a5a45ad0a9182",
        "object_or_effect": "w_b81976afd4448e9c469f",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_b81976afd4448e9c469f",
        "grounded": true
      },
      {
        "id": "fact_871f783636e663042eda",
        "object_or_effect": "o_c65487046fc1cbf4ed84",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_8b7cf40c7be87bda8a76",
        "object_or_effect": "w_a07152700dac6d357231",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_a07152700dac6d357231",
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "direct_callback_influence",
        "answer": "sat",
        "count": 5
      },
      {
        "label": "callback_influence",
        "answer": "sat",
        "count": 5
      },
      {
        "label": "direct_callback_influence",
        "answer": "unsat",
        "count": 3
      },
      {
        "label": "callback_influence",
        "answer": "unsat",
        "count": 3
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 11
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 11
      },
      {
        "label": "baseline_usable",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "direct_effect",
        "answer": "sat",
        "count": 3
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 2,
      "noncached_action_limit": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE",
      "FCR-PAUSE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 150,
      "source_task_reading": 22,
      "scope_missing": 2,
      "program_support": 1,
      "covered_holder_grant": 2,
      "external_dependency": 3
    }
  }
}
```

## RQ1_b649070a92c3

证据目录 run/members/RQ1_b649070a92c3/attempt_1/，报告哈希 c0e1b6c4f0d8d499433bb9e0679af4eae7c93d93c0c94f8fb8c9e1a38c56aea4

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "not_detected",
    "FCR-MINT": "unsupported",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "not_detected",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "decision_only 未知转有效阴性"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope,unrelated_or_secondary_graph_pairs_deferred",
    "未决类别 FCR-DESTROY,FCR-MINT"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": false,
    "paired_id": "RQ1_cd39ae0d15a5",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ae746bfa4fdf6907fd045a07bf8a12bb18d84f477858232cc0c6f249c5f2ff1d",
          "issue": "issue_62edd36debd5610f7a3d"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_c408438c1af57366f32b",
        "fact": "fact_6aa7ef2dc61fb7d009d8",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_6aa7ef2dc61fb7d009d8",
        "object_or_effect": "o_6bec2419524a7ccff194",
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
      "unbound_or_inapplicable_seed": 1,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE",
      "FCR-PAUSE",
      "FCR-TRANSFER"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 112,
      "parameter_only": 1,
      "source_task_reading": 9,
      "covered_holder_grant": 1,
      "scope_missing": 2
    }
  }
}
```

## RQ1_b6fc6e31e760

证据目录 run/members/RQ1_b6fc6e31e760/attempt_1/，报告哈希 68d7003af51486a3e9082c088a9912dab10d34799cc59d2f2e77388ea5407b32

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:537:original:1",
    "last1164 丢失根因 D2:537:original:1,D2:537:original:2"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope,invalid_semantic_row,unknown_assessment_vocabulary",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_b6fc6e31e760",
        "reference": "D2:537:original:1",
        "function": "payout",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "FN",
        "decision_only": "FN",
        "prev200_findings": [],
        "decision_only_findings": [],
        "current": "FN"
      },
      {
        "member": "RQ1_b6fc6e31e760",
        "reference": "D2:537:original:2",
        "function": "payoutSelf",
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
          "D2:537:original:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:537:original:1",
          "D2:537:original:2"
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "3e7fa87176cfe502a18032a71e51c370af5daba9e41823bd3e38d457c96859ac"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c7c79550ff2ac3388bdb42031e45047dc94f9e2aacdf9e3bbc4f50fdce18e7c4",
          "issue": "issue_d832445a500b7071b98e"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "a97856862a85057e4d226f2fe988beec465b6b341181849b28bdfdd436b13b0f",
          "issue": "issue_553698827c4d03e9dac4"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "9f2c5a41818b6a9e03da6908596c764e1d729f4516787877a5002d818e563188",
          "issue": "issue_553698827c4d03e9dac4"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "dcd6a9fdc767219cddf83cb2840967f07c39a0afbb885cc00aea40f723e7dd08",
          "issue": "issue_825830c543c2076dae7f"
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
    "supports": [],
    "facts": [],
    "query_summary": [
      {
        "label": "original_path_commit",
        "answer": "sat",
        "count": 5
      },
      {
        "label": "source_quantity_debit",
        "answer": "unsat",
        "count": 11
      },
      {
        "label": "same_holder_native_settlement_counterexample",
        "answer": "unsat",
        "count": 3
      },
      {
        "label": "actual_debit_exists",
        "answer": "unsat",
        "count": 3
      },
      {
        "label": "source_quantity_debit",
        "answer": "sat",
        "count": 6
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 10
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 10
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 10
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 5,
      "invalid_semantic_row": 4,
      "unknown_assessment_vocabulary": 3,
      "category_ambiguous_or_outside_supported_task": 1,
      "semantic_answer_outside_sent_scope": 5,
      "unrelated_or_secondary_graph_pairs_deferred": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 11,
      "policy_missing": 1,
      "source_task_reading": 4,
      "external_dependency": 2
    }
  }
}
```

## RQ1_b731957fa974

证据目录 run/members/RQ1_b731957fa974/attempt_1/，报告哈希 6d86f16c0b976797b066267e24b2da32e7f6d0731e07bc384f303a4015a6fb0e

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "alarm",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "alarm",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "last1164 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": true,
    "paired_id": "RQ1_4968e56244c9",
    "state": "alarm",
    "changes": {
      "v32": {
        "before": "alarm",
        "after": "alarm"
      },
      "last1164": {
        "before": "unsupported",
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
      "normalization_diagnostics": []
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_df176813ee7009e21208",
        "fact": "fact_a2e438b59d8b18a42cec",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_a2e438b59d8b18a42cec",
        "object_or_effect": "o_69bffa551a4c0ce70e71",
        "meaning": "financial_right",
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
        "count": 4
      },
      {
        "label": "direct_effect",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "control_transition_preservation",
        "answer": "unsat",
        "count": 4
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
        "count": 4
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 4
      }
    ],
    "diagnostics": {
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 217,
      "new_entitlement": 4,
      "source_task_reading": 31,
      "scope_missing": 2,
      "external_dependency": 8,
      "program_support": 2,
      "covered_holder_grant": 1
    }
  }
}
```

## RQ1_b809aa517821

证据目录 run/members/RQ1_b809aa517821/attempt_1/，报告哈希 7a8fe58227aee772879aa84218b23517a8447cb71c5b5a46235fc6b5c1667369

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [
    "v32 丢失根因 D2:416:author:1",
    "last1164 丢失根因 D2:416:author:1",
    "prev200 丢失根因 D2:416:author:1",
    "decision_only 丢失根因 D2:416:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,unrelated_or_secondary_graph_pairs_deferred,invalid_semantic_row",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_b809aa517821",
        "reference": "D2:416:author:1",
        "function": "mintTo",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_ad50b4825175d76bb0ee"
        ],
        "decision_only_findings": [
          "finding_082f5c9ea23d87a23129"
        ],
        "current": "FN"
      }
    ],
    "findings": [
      {
        "idx": 21,
        "member": "RQ1_b809aa517821",
        "finding": "finding_9a09dbbce47ddaa9699e",
        "function": "killContract()",
        "location": {
          "file": "units/program.sol",
          "start": 1561,
          "length": 184,
          "ast_id": 161
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_b809aa517821', 'units/program.sol', 1561)",
        "source_excerpt": "function killContract () payable external\n    {\n        if (msg.sender==owner || msg.value >=howManyEtherInWeiToKillContract)\n        {\n            selfdestruct(owner);\n        }\n    }",
        "source_sha256": "c9511ccccf05235aefe1f0f59b7acf00a3c7450a5f9936ceabffe0c095010c80",
        "note": "实际报警入口或影响与作者参考不同，不能抵销该独立根因漏检。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 1561. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 1561,
              "length": 184,
              "ast_id": 161
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
          "E10"
        ]
      }
    ],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:416:author:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:416:author:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:416:author:1"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:416:author:1"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "36ee6bf99273648f25dc3956915340fbe07099daba809e5451ce6450c81dafbf",
          "issue": "issue_8f179caa0054e4ca169c"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b728a1f784c64919610574c7cb21e15b93aa87ca828f78a19eb4da94d1813ec6",
          "issue": "issue_8f179caa0054e4ca169c"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "2a395fd663cb0288d32df9d71714cb4b77c5151663ce1cbeb81d923be45a9d3f",
          "issue": "issue_9e151788ea5adff99da1"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "83b371443e037517df8e9f558a02f0d3543f6a226509a372f55688c466c386fc",
          "issue": "issue_9e151788ea5adff99da1"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "e2e2e373ead8bd099cc3954594c6479b99eaca3c58a338fb54f6a7520d5c3cbf",
          "issue": "issue_4af4d93f9085f462546c"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "36ee68cb34b0ce3f967d45f8d62c6942ce00942dba06df231f6460c874d45786",
          "issue": "issue_4af4d93f9085f462546c"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "b7f47317a31ecc3e6c82389ef72fc397c4940f99fabbdbcc3076d527434cb05e",
          "issue": "issue_af8b1477c082b76fa53b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "079ed9924192a3138bde0fc7d4a8254db75d06e32fc65b4e2a70a84cf3cc135b",
          "issue": "issue_af8b1477c082b76fa53b"
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c43472dceaabb87cdfc1e2685582335359cbfbb0309eb5e23b8a0f08ec0c71aa",
          "issue": "issue_838337893b194391393a"
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
        "support": "support_2d5cadb2eb41efccaa5a",
        "fact": "fact_266741567a5bc63044ef",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_30d74f125bbbc6f6ca18",
        "fact": "fact_0d851b34ee9346e6ad61",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_4b244eb9c307266f6229",
        "fact": "fact_3da438667bfaff315c6c",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_6358bf06015cc2621180",
        "fact": "fact_c4ced5f9a7bb7839c1e1",
        "origin": "verified_service",
        "field": "policies",
        "version": 1
      },
      {
        "support": "support_a56f6a1963e9f3c8871b",
        "fact": "fact_3da438667bfaff315c6c",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_bc96f4f788747de04c91",
        "fact": "fact_5277156557b4f2d42828",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_edfb9e04d3fb14ce8ad3",
        "fact": "fact_5277156557b4f2d42828",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_0d851b34ee9346e6ad61",
        "object_or_effect": "o_6d1f81f02213ec957f0e",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_266741567a5bc63044ef",
        "object_or_effect": "o_62dd6c2af0b66a9a592d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_3da438667bfaff315c6c",
        "object_or_effect": "o_cdb3e4676af23c1b6630",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_4c40ee65b1710cde5874",
        "object_or_effect": "w_7cd8cad407dd81a0d1cd",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_7cd8cad407dd81a0d1cd",
        "grounded": true
      },
      {
        "id": "fact_5277156557b4f2d42828",
        "object_or_effect": "o_4cf05f22e6e0cb37b692",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_54a9ea830aaa092f5068",
        "object_or_effect": "w_8fb1430a9e012ab60ab0",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_8fb1430a9e012ab60ab0",
        "grounded": true
      },
      {
        "id": "fact_5ac4adc9ab5b781d75c6",
        "object_or_effect": "w_05d18213362a7be7f390",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_05d18213362a7be7f390",
        "grounded": true
      },
      {
        "id": "fact_9c566698f41e27ef2c72",
        "object_or_effect": "w_6e01b361b6e23a2e979d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6e01b361b6e23a2e979d",
        "grounded": true
      },
      {
        "id": "fact_a19e85027077570502dc",
        "object_or_effect": "w_3b70dfc577ba32c19f01",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_3b70dfc577ba32c19f01",
        "grounded": true
      },
      {
        "id": "fact_c4ced5f9a7bb7839c1e1",
        "object_or_effect": "w_3b70dfc577ba32c19f01",
        "meaning": "holder_authorization_applies",
        "role": null,
        "subject": "o_cdb3e4676af23c1b6630",
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 6
      },
      {
        "label": "authorization_violation",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "authorization_violation",
        "answer": "unsat",
        "count": 5
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 12
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 12
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 8
      },
      {
        "label": "direct_callback_influence",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "callback_influence",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "direct_callback_influence",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "callback_influence",
        "answer": "unsat",
        "count": 6
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 1,
      "category_ambiguous_or_outside_supported_task": 4,
      "unknown_assessment_vocabulary": 5,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 4,
      "invalid_semantic_row": 3,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 11,
      "policy_missing": 4,
      "program_support": 1,
      "external_dependency": 1,
      "source_task_reading": 2
    }
  }
}
```

## RQ1_b84042e6eefd

证据目录 run/members/RQ1_b84042e6eefd/attempt_1/，报告哈希 8b085190edca7dbce58a217ee691d36c61f5be4acbadabdb037d787565d2ff4d

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "not_detected",
    "FCR-MINT": "not_detected",
    "FCR-DESTROY": "not_detected",
    "FCR-PAUSE": "alarm",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "last1164 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": true,
    "paired_id": "RQ1_475c7d9ec738",
    "state": "alarm",
    "changes": {
      "v32": {
        "before": "alarm",
        "after": "alarm"
      },
      "last1164": {
        "before": "unsupported",
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
          "detail_sha256": "251fafc5c1783105f6cd151fb3167e5b29b83a62707bb0148547c074386a7f43",
          "issue": "issue_7e7637e180df1df573ad"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [
      {
        "label": "control_transition_preservation",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "prefix_reachability",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 6,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1
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
      "no_effect_in_scope": 26,
      "program_support": 1,
      "source_task_reading": 1,
      "intra_ledger_transfer": 1,
      "source_check_excluded": 1
    }
  }
}
```

## RQ1_bb9523a9c423

证据目录 run/members/RQ1_bb9523a9c423/attempt_1/，报告哈希 7aac8b173d3b28937a51801824db225752bb04b295a7f4bfcb86aad22345de2f

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_bb9523a9c423",
        "reference": "D2:364:author:1",
        "function": "reward",
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
          "detail_sha256": "5aa111c1afd10848a5e52c802f9c8ce386f0bf8c5885aaaf63b3283f2666f124"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "71aaecf09473ca67a37d1897264df5c27d14770059a2632c3940f4c1a10c5cfc"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "164ea7a2833778f09e2c35225d22bd74721d2149edce4cc141d777887ab88e7e"
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
          "detail_sha256": "40e96a676c039349c3383b4e70f38cf5c74b8b2992f3bc078fa992a9cc93df3e",
          "issue": "issue_5bac2d92797105eb4ee4"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c35f7f1aaeee2b427901312c25e79d31bf19850c0b9303c80d92ffe258ebd74d",
          "issue": "issue_5bac2d92797105eb4ee4"
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
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 11,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 9,
      "policy_missing": 1,
      "source_task_reading": 1,
      "external_dependency": 2
    }
  }
}
```

## RQ1_bbf6634a1913

证据目录 run/members/RQ1_bbf6634a1913/attempt_1/，报告哈希 16366be92bd20e8b16a47dff6990174f707a8713b88c4fe7d406a326fcfe9cbb

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [
    "last1164 新增根因 D2:3:S1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_bbf6634a1913",
        "reference": "D2:3:S1",
        "function": "selfdestructs",
        "v32": "TP",
        "last1164": "FN",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_81558456e6f50e72e626"
        ],
        "decision_only_findings": [
          "finding_057078307213d2893cfb"
        ],
        "current": "TP"
      }
    ],
    "findings": [
      {
        "idx": 22,
        "member": "RQ1_bbf6634a1913",
        "finding": "finding_a26c9b344a58c3fbe523",
        "function": "fallback()",
        "location": {
          "file": "units/program.sol",
          "start": 4812,
          "length": 135,
          "ast_id": 594
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_bbf6634a1913', 'units/program.sol', 4812)",
        "source_excerpt": "function () payable public {\n    \t\tuint amount = msg.value * buyPrice;               \n    \t\t_transfer(owner, msg.sender, amount);\n    }",
        "source_sha256": "ce5d74bd65908863282d67fb34be8d88b5434b933e07a56321648e0369db6eb3",
        "note": "实际报警入口或影响与作者参考不同，不能抵销该独立根因漏检。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 4812. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 4812,
              "length": 135,
              "ast_id": 594
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
          "E2",
          "E7"
        ]
      },
      {
        "idx": 23,
        "member": "RQ1_bbf6634a1913",
        "finding": "finding_d3903f68d06f341b598f",
        "function": "selfdestructs()",
        "location": {
          "file": "units/program.sol",
          "start": 4952,
          "length": 74,
          "ast_id": 602
        },
        "result": "TP",
        "reference": "D2:3:S1",
        "group": "D2:3:S1",
        "source_excerpt": "function selfdestructs() payable public {\n    \t\tselfdestruct(owner);\n    }",
        "source_sha256": "ce5d74bd65908863282d67fb34be8d88b5434b933e07a56321648e0369db6eb3",
        "note": "实际入口及源码效果与作者独立根因对应，保留程序证据可审计性限制。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 4952. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 4952,
              "length": 74,
              "ast_id": 602
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
          "E3",
          "E8"
        ]
      }
    ],
    "changes": {
      "v32": {
        "gained": [],
        "lost": []
      },
      "last1164": {
        "gained": [
          "D2:3:S1"
        ],
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "39993f5a25f5f1435ca8f7612ee9a6babc7bd96a50875888ef1c633b39bd3611",
          "issue": "issue_72dad2d8cd4e712b1523"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "3a8d904a8bb536a311d7ca4daa93260778b916ccb8fc7b121d1f675806b1ce5a",
          "issue": "issue_72dad2d8cd4e712b1523"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "57db6c844bc1d6a4c7068633c9975382ff03a92b2f65b8adb818d16aef7bdcaa",
          "issue": "issue_c385ce3dc098b8e861d2"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ff539df207483c1e5d4dede87b99802b006f3a9536f5047dec8215932eaa1ab6",
          "issue": "issue_c385ce3dc098b8e861d2"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "00da389696b883deccaa8c9937f270f0a6a1dcb69e23c66a88ba9d4677f462cf",
          "issue": "issue_17f6eb8b9437f18d2d38"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c554eeb3f67f1cc5d38ffb3ff63b52762d4c0c8eb0fd532c9ed740cfcb2428a1",
          "issue": "issue_17f6eb8b9437f18d2d38"
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
          "reason": "invalid_seed_fields",
          "detail_sha256": "303a9aa6a1bacf281bb4c27501cc9890b6d69631c6e3efd90f79661a98149611"
        },
        {
          "reason": "invalid_seed_fields",
          "detail_sha256": "316a0a58c45ced27d54780d99899c0ff00fe36bbd6ca904427ca27a63f9b62ce"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "3d37b1e591fbfc9aafa3c9ac6a64afa51a1c23631df61bbacb80faaeab713167",
          "issue": "issue_1b7a1c6662f75cb88b1a"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [
      2834
    ],
    "new": [],
    "disappeared_to_unknown": false,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_2f31b2c3890697ff6143",
        "fact": "fact_421e3308e7bf5b58c209",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_463ee939dfe978458636",
        "fact": "fact_89814802d78333da1ab8",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_60bbfd09f84474b14e9f",
        "fact": "fact_421e3308e7bf5b58c209",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_db9ff53d8f5705247e51",
        "fact": "fact_3c92a585781f64beea0b",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_3c92a585781f64beea0b",
        "object_or_effect": "o_ac587de2c770b825326a",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_421e3308e7bf5b58c209",
        "object_or_effect": "o_1d37ddf778cb1e7b8311",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_73b16b1dc4004aab3059",
        "object_or_effect": "w_d7f673a1cd4b75c73947",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d7f673a1cd4b75c73947",
        "grounded": true
      },
      {
        "id": "fact_89814802d78333da1ab8",
        "object_or_effect": "o_8f3af6369f58a43c26ce",
        "meaning": "financial_right",
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
        "count": 2
      },
      {
        "label": "authorization_violation",
        "answer": "sat",
        "count": 2
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 5,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 4,
      "semantic_answer_outside_sent_scope": 2,
      "invalid_seed_fields": 2,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 17,
      "source_task_reading": 16,
      "program_support": 2,
      "external_dependency": 2,
      "policy_missing": 1
    }
  }
}
```

## RQ1_bc34a2568a3c

证据目录 run/members/RQ1_bc34a2568a3c/attempt_1/，报告哈希 845ed8f850319cbda95b470149f8b0a6b87cc17f35e2caecf6c78b11f2261c2a

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:173:author:1",
    "last1164 丢失根因 D2:173:author:1",
    "prev200 丢失根因 D2:173:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unrelated_or_secondary_graph_pairs_deferred,semantic_answer_outside_sent_scope,category_ambiguous_or_outside_supported_task",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_bc34a2568a3c",
        "reference": "D2:173:author:1",
        "function": "TokenERC20",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "FN",
        "prev200_findings": [
          "finding_ef5d1380b8eace2e22f2"
        ],
        "decision_only_findings": [],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:173:author:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:173:author:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:173:author:1"
        ]
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "23a6538a9ed5b2f61822e0e7b5063a3598a192d13fc88c7a9ac1328ad4db6f82"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "1516dc3f640c645b3ea0999a24da549d3751773f3dc30f9f7364edc778f927fe",
          "issue": "issue_5a4cc9586d7b07998e83"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "5ca0ce84f6c7cc6ef9a0664faa58bad44443eaa70e44861f6cb7fba791828476",
          "issue": "issue_5a4cc9586d7b07998e83"
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
        "support": "support_d26338bdd6fe9dddcb1b",
        "fact": "fact_521482cec950b4c104f5",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_00955a8173aa4de27dbd",
        "object_or_effect": "w_5b40945356c101d36f2b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5b40945356c101d36f2b",
        "grounded": true
      },
      {
        "id": "fact_0204e24d2cc100b28e5b",
        "object_or_effect": "w_2949296ca8121bb69ca0",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2949296ca8121bb69ca0",
        "grounded": true
      },
      {
        "id": "fact_05159ae2e49dc8ff8296",
        "object_or_effect": "w_36d9376d313380f79c51",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_36d9376d313380f79c51",
        "grounded": true
      },
      {
        "id": "fact_0a3871fbac138a53ed48",
        "object_or_effect": "w_24bca91e81851dad5aa9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_24bca91e81851dad5aa9",
        "grounded": true
      },
      {
        "id": "fact_0af7f9c8d3ed03057a7b",
        "object_or_effect": "w_a6426c123b3e92d6425c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a6426c123b3e92d6425c",
        "grounded": true
      },
      {
        "id": "fact_0e9a443577b782749b3f",
        "object_or_effect": "w_1da7681bb9d97188f135",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1da7681bb9d97188f135",
        "grounded": true
      },
      {
        "id": "fact_0f89a0ae5130e9415986",
        "object_or_effect": "w_5db3b343293f8ed7c2c0",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5db3b343293f8ed7c2c0",
        "grounded": true
      },
      {
        "id": "fact_1260974d93bf6b2a26c6",
        "object_or_effect": "w_9e7756bead03da4ef529",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9e7756bead03da4ef529",
        "grounded": true
      },
      {
        "id": "fact_151e6fb28c3326285418",
        "object_or_effect": "w_f8184e5cd8fc9150f3fc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f8184e5cd8fc9150f3fc",
        "grounded": true
      },
      {
        "id": "fact_16e2ec4b74c04589c05a",
        "object_or_effect": "w_e6514f2c18906dafe6eb",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e6514f2c18906dafe6eb",
        "grounded": true
      },
      {
        "id": "fact_1c3a3877570bb40fcf7e",
        "object_or_effect": "w_b85f6a867a7cf39aad59",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b85f6a867a7cf39aad59",
        "grounded": true
      },
      {
        "id": "fact_1cabc30aafc0b18ca114",
        "object_or_effect": "w_556df7d9a21f906be86a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_556df7d9a21f906be86a",
        "grounded": true
      },
      {
        "id": "fact_279defda31787bbef277",
        "object_or_effect": "w_1e6a147e6817df127f4f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1e6a147e6817df127f4f",
        "grounded": true
      },
      {
        "id": "fact_2c844d50403e28ad71b0",
        "object_or_effect": "w_2caa7ab3fb3e05ec19fa",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2caa7ab3fb3e05ec19fa",
        "grounded": true
      },
      {
        "id": "fact_2e6375c72b2636270c2f",
        "object_or_effect": "w_59fdd432235ed64c8e61",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_59fdd432235ed64c8e61",
        "grounded": true
      },
      {
        "id": "fact_31466149a81f8e557e44",
        "object_or_effect": "w_0ad6c3191cdd8a5092b7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0ad6c3191cdd8a5092b7",
        "grounded": true
      },
      {
        "id": "fact_38bb60a270bc0bab6e86",
        "object_or_effect": "w_cb55c22e9e2acec12bb8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cb55c22e9e2acec12bb8",
        "grounded": true
      },
      {
        "id": "fact_3b000b31417d4f768562",
        "object_or_effect": "w_1bcf102eab540ee1c859",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1bcf102eab540ee1c859",
        "grounded": true
      },
      {
        "id": "fact_48048a2f2b2681e44be7",
        "object_or_effect": "w_79bd58595f14e4e9735b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_79bd58595f14e4e9735b",
        "grounded": true
      },
      {
        "id": "fact_4cff74d41e37a0ea042f",
        "object_or_effect": "w_322788d41d36f27d048e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_322788d41d36f27d048e",
        "grounded": true
      },
      {
        "id": "fact_4f3d6366809b1ed6463b",
        "object_or_effect": "w_b27583419544c9b756b7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b27583419544c9b756b7",
        "grounded": true
      },
      {
        "id": "fact_521482cec950b4c104f5",
        "object_or_effect": "o_084665c879187d2cf698",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_527454d03216392345e1",
        "object_or_effect": "w_2fe9e730d565505602f3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2fe9e730d565505602f3",
        "grounded": true
      },
      {
        "id": "fact_5c0855735cb734b1c384",
        "object_or_effect": "w_5f7821571ce2e37cdc7a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5f7821571ce2e37cdc7a",
        "grounded": true
      },
      {
        "id": "fact_5e43fac5a0a9499ba414",
        "object_or_effect": "w_d7e7af53aa8e1e932e70",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d7e7af53aa8e1e932e70",
        "grounded": true
      },
      {
        "id": "fact_5ef9a96b64802e906de5",
        "object_or_effect": "w_286c69495ba5a89ca4f1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_286c69495ba5a89ca4f1",
        "grounded": true
      },
      {
        "id": "fact_655af62b54048f693045",
        "object_or_effect": "w_2b73c7e7fdb3ae18b635",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2b73c7e7fdb3ae18b635",
        "grounded": true
      },
      {
        "id": "fact_6644dac1cf159381d0d5",
        "object_or_effect": "w_4f07808dc1241df1bdb7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4f07808dc1241df1bdb7",
        "grounded": true
      },
      {
        "id": "fact_6b87b478216e739d0f90",
        "object_or_effect": "w_a1fa2f38af962105c0c6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a1fa2f38af962105c0c6",
        "grounded": true
      },
      {
        "id": "fact_704af5136fe658dab332",
        "object_or_effect": "w_3802cc0b8ef7a780cc0f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3802cc0b8ef7a780cc0f",
        "grounded": true
      },
      {
        "id": "fact_714be11353208efe3ae2",
        "object_or_effect": "w_e5e42cda0ac7fe9a403d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e5e42cda0ac7fe9a403d",
        "grounded": true
      },
      {
        "id": "fact_7a0f6566e989d89519bf",
        "object_or_effect": "w_1fd1a7083b46ee29fea3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1fd1a7083b46ee29fea3",
        "grounded": true
      },
      {
        "id": "fact_7cddddaf11a10f4f03e6",
        "object_or_effect": "w_c62a3840a524b0a08bb4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c62a3840a524b0a08bb4",
        "grounded": true
      },
      {
        "id": "fact_7d46b9c8a11ce87850bc",
        "object_or_effect": "w_d745ddb951c30e07edaa",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d745ddb951c30e07edaa",
        "grounded": true
      },
      {
        "id": "fact_83a99fe25856bbad32f4",
        "object_or_effect": "w_f20da3bbc01d62a60eee",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f20da3bbc01d62a60eee",
        "grounded": true
      },
      {
        "id": "fact_84971a4fb7f28bf65210",
        "object_or_effect": "w_26a53a7db422b54f64e7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_26a53a7db422b54f64e7",
        "grounded": true
      },
      {
        "id": "fact_8f158ed7d7b64f9863c4",
        "object_or_effect": "w_03875e3617cc8d83eccb",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_03875e3617cc8d83eccb",
        "grounded": true
      },
      {
        "id": "fact_912d7c6aa0e3e8ee456d",
        "object_or_effect": "w_517cbad231b4fa7754f1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_517cbad231b4fa7754f1",
        "grounded": true
      },
      {
        "id": "fact_914920efdadc16331397",
        "object_or_effect": "w_ff34d6a2c0b4c78b85da",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ff34d6a2c0b4c78b85da",
        "grounded": true
      },
      {
        "id": "fact_940361065bad3138672d",
        "object_or_effect": "w_b3dbc4d9a518b81935ed",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b3dbc4d9a518b81935ed",
        "grounded": true
      },
      {
        "id": "fact_94bf86f923aa669d3fa2",
        "object_or_effect": "w_b2eb00c45cf796a3383d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b2eb00c45cf796a3383d",
        "grounded": true
      },
      {
        "id": "fact_9f66afd0544977eb0302",
        "object_or_effect": "w_c93808a04b100807cf9f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c93808a04b100807cf9f",
        "grounded": true
      },
      {
        "id": "fact_a16c81ebbbe339096a75",
        "object_or_effect": "w_e43b2068edd996191ac6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e43b2068edd996191ac6",
        "grounded": true
      },
      {
        "id": "fact_a24c7face5ffc8f405c1",
        "object_or_effect": "w_74463993b1c0b14c734b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_74463993b1c0b14c734b",
        "grounded": true
      },
      {
        "id": "fact_a2627497029f0d1cc88d",
        "object_or_effect": "w_db80a19c8bf3c55c96d6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_db80a19c8bf3c55c96d6",
        "grounded": true
      },
      {
        "id": "fact_a4cebeb5e5628746a136",
        "object_or_effect": "w_28150b784e6494ec7292",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_28150b784e6494ec7292",
        "grounded": true
      },
      {
        "id": "fact_ae6cbccbf5b32a36c9f3",
        "object_or_effect": "w_5144f70662149d02bc12",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5144f70662149d02bc12",
        "grounded": true
      },
      {
        "id": "fact_ae9ccf2badcc04ed9deb",
        "object_or_effect": "w_9be0fa0669ebeb050fbf",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9be0fa0669ebeb050fbf",
        "grounded": true
      },
      {
        "id": "fact_b336fabb6a110790988a",
        "object_or_effect": "w_058977b4a75e9ae43f1c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_058977b4a75e9ae43f1c",
        "grounded": true
      },
      {
        "id": "fact_b4820a8bb8f7d15ddf8f",
        "object_or_effect": "w_f8c9f6fbc47c3283d336",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f8c9f6fbc47c3283d336",
        "grounded": true
      },
      {
        "id": "fact_b62025eb0fd9879066fa",
        "object_or_effect": "w_d8b032e34a117eae30ef",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d8b032e34a117eae30ef",
        "grounded": true
      },
      {
        "id": "fact_b88119d67de0382110a9",
        "object_or_effect": "w_ecd12effee8b0f5c1cd8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ecd12effee8b0f5c1cd8",
        "grounded": true
      },
      {
        "id": "fact_c839947414826b82bb11",
        "object_or_effect": "w_ed5dc5553dbcb47d694c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ed5dc5553dbcb47d694c",
        "grounded": true
      },
      {
        "id": "fact_c85ffbca3e97d14cc631",
        "object_or_effect": "w_e85f0c69e887fd2d9d00",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e85f0c69e887fd2d9d00",
        "grounded": true
      },
      {
        "id": "fact_cb832a0b70a32b8306b6",
        "object_or_effect": "w_d77e5c5f32f47f22d485",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d77e5c5f32f47f22d485",
        "grounded": true
      },
      {
        "id": "fact_cbcc724933b26e32dd44",
        "object_or_effect": "w_e784c295f0cacd103c4f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e784c295f0cacd103c4f",
        "grounded": true
      },
      {
        "id": "fact_d39bef2d502a31e33856",
        "object_or_effect": "w_fd9a1c065cb954ab1522",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_fd9a1c065cb954ab1522",
        "grounded": true
      },
      {
        "id": "fact_d3d711ad5408802fa3b9",
        "object_or_effect": "w_6164eb86b126bda4f2c2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6164eb86b126bda4f2c2",
        "grounded": true
      },
      {
        "id": "fact_d417ec8bfc3f21f75f05",
        "object_or_effect": "w_b3a3374833f1ae818fc0",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b3a3374833f1ae818fc0",
        "grounded": true
      },
      {
        "id": "fact_d488ce1771d0e9591874",
        "object_or_effect": "w_010b7d9c3c248f8fe9e7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_010b7d9c3c248f8fe9e7",
        "grounded": true
      },
      {
        "id": "fact_d512a068bc5c46a12ae1",
        "object_or_effect": "w_3d8a384e9a3e37710276",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3d8a384e9a3e37710276",
        "grounded": true
      },
      {
        "id": "fact_d6b6512ed1fa702fbe8e",
        "object_or_effect": "w_28d182d1d3dc32edb5df",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_28d182d1d3dc32edb5df",
        "grounded": true
      },
      {
        "id": "fact_db579c163077177c3598",
        "object_or_effect": "w_dff6d72c6053979b2823",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_dff6d72c6053979b2823",
        "grounded": true
      },
      {
        "id": "fact_dca7cc1b443d7224f852",
        "object_or_effect": "w_7f5165178eb6aa651048",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7f5165178eb6aa651048",
        "grounded": true
      },
      {
        "id": "fact_dd3a7e23263783000f07",
        "object_or_effect": "w_5426b8d371a8e715829e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5426b8d371a8e715829e",
        "grounded": true
      },
      {
        "id": "fact_dec25b6d102ffded4709",
        "object_or_effect": "w_fd5a943b6ce4140243ad",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_fd5a943b6ce4140243ad",
        "grounded": true
      },
      {
        "id": "fact_e9989044c8dca3f38402",
        "object_or_effect": "w_98c7a1b183d89c77bb79",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_98c7a1b183d89c77bb79",
        "grounded": true
      },
      {
        "id": "fact_ed7ae8b93ab02d6f5a1c",
        "object_or_effect": "w_4d3630e7b7f7edd7d76a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4d3630e7b7f7edd7d76a",
        "grounded": true
      },
      {
        "id": "fact_f13ff0df4050b6b7ed4c",
        "object_or_effect": "w_e65b33fd7940701e7131",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e65b33fd7940701e7131",
        "grounded": true
      },
      {
        "id": "fact_f2a041604c84e280b389",
        "object_or_effect": "w_96881e258072c2062e22",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_96881e258072c2062e22",
        "grounded": true
      },
      {
        "id": "fact_f4422f82ab96297aa8a4",
        "object_or_effect": "w_4eb404a85009aca2a3a3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4eb404a85009aca2a3a3",
        "grounded": true
      },
      {
        "id": "fact_f8536e767d248196cb5a",
        "object_or_effect": "w_83b33b5d3d877cb9cf9d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_83b33b5d3d877cb9cf9d",
        "grounded": true
      },
      {
        "id": "fact_fc9771d7385a2ed43e2a",
        "object_or_effect": "w_103477d4f9051341101d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_103477d4f9051341101d",
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
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 4
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 8,
      "semantic_answer_outside_sent_scope": 2,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 14,
      "source_task_reading": 5,
      "policy_missing": 2,
      "external_dependency": 3
    }
  }
}
```

## RQ1_bc5855a83e2d

证据目录 run/members/RQ1_bc5855a83e2d/attempt_1/，报告哈希 31b4fd6d800b8ebe4b0f339aa1ecc5bda534cd961472b98bb1e6bd1ae3fe29f5

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
    "prev200 退为未知，不能当作纠正",
    "decision_only 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,unknown_assessment_vocabulary,no_locatable_source",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": true,
    "paired_id": "RQ1_770ae395781c",
    "state": "unsupported",
    "changes": {
      "v32": {
        "before": "alarm",
        "after": "unsupported"
      },
      "last1164": {
        "before": "alarm",
        "after": "unsupported"
      },
      "prev200": {
        "before": "alarm",
        "after": "unsupported"
      },
      "decision_only": {
        "before": "alarm",
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
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "cd7c280669406dad401aacafae9281acff4e3f9782583979a58d6d14067ae7e3",
          "issue": "issue_a4d98da69963ee4183cf"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 5,
      "semantic_answer_outside_sent_scope": 2,
      "unknown_assessment_vocabulary": 1,
      "no_locatable_source": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 97,
      "model_phase_missing": 33
    }
  }
}
```
