# 逐例审阅

## RQ1_3f952af67006

证据目录 run/members/RQ1_3f952af67006/attempt_1/，报告哈希 792374d393c6c7587f6a6e01e555c41aad907be449d7312a03845f99e9aacfcd

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope",
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
      "semantic_answer_outside_sent_scope": 4
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "source_context_missing": 4,
      "no_effect_in_scope": 13,
      "model_phase_missing": 7,
      "external_dependency": 6
    }
  }
}
```

## RQ1_403e9f180228

证据目录 run/members/RQ1_403e9f180228/attempt_1/，报告哈希 824020689ddb36e80be601e49f195e8240a218bb67f42eda45ef9dc12e606a62

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 semantic_answer_outside_sent_scope,invalid_semantic_row,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [],
    "findings": [
      {
        "idx": 7,
        "member": "RQ1_403e9f180228",
        "finding": "finding_b3dafe67307522c66ae1",
        "function": "addSignature(uint256)",
        "location": {
          "file": "units/program.sol",
          "start": 1338,
          "length": 694,
          "ast_id": 230
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_403e9f180228', 'units/program.sol', 1338)",
        "source_excerpt": "function addSignature(uint id) {\n        address member = msg.sender;\n        if (documentsCount < id) throw;\n        Document d = documentsIds[id];\n        uint count = d.signsCount;\n        bool signed = false;\n        if (count != 0) {\n            for (uint i = 0; i < count; i++) {\n                if (d.signs[i].member == member) {\n                    signed = true;\n                    break;\n                }\n            }\n        }\n        if (!signed) {\n            d.signs[count] = Sign({\n                    member: member,\n                    date: now\n                });\n            documentsIds[id].signsCount = count + 1;\n            DocumentSigned(id, member);\n        }\n    }",
        "source_sha256": "409f5ad61f213cef73f9e3991bc1d87d409cffc1009d3ffa45451e287552beeb",
        "note": "冻结参考无该根因，按参考外报警记录；未据此证明其业务上错误。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 1338. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 1338,
              "length": 694,
              "ast_id": 230
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b39a5d1fa868db528366799cc8e1eccebfb7b1ff83bcede90a9d86d00c8b8f62",
          "issue": "issue_01b44a67ea6b5e08c326"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "9aa800560e8ebeb4358214e30c01799506cc75cbdbb2633fc4116d97951ae720",
          "issue": "issue_a81deee2ce846db88cf5"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "7dc19d344a0900df47f9ba1ba9c2f710bf537659d294ef6d63d2599188c6a314",
          "issue": "issue_a81deee2ce846db88cf5"
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c6d7ca1e8b848669d1b10427e15b85bc191132b0cf31078cabfa481b833d0b41",
          "issue": "issue_3da83fd0811961a03dd7"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [],
    "new": [
      1338
    ],
    "disappeared_to_unknown": false,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [
      {
        "label": "local_premises_feasible",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 5
      },
      {
        "label": "authorization_violation",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "authorization_violation",
        "answer": "sat",
        "count": 3
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 3,
      "unknown_assessment_vocabulary": 3,
      "category_ambiguous_or_outside_supported_task": 1,
      "semantic_answer_outside_sent_scope": 5,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 5,
      "source_task_reading": 3,
      "program_support": 1,
      "policy_missing": 2
    }
  }
}
```

## RQ1_4169c528c5e4

证据目录 run/members/RQ1_4169c528c5e4/attempt_1/，报告哈希 cc183b731aeb07085176874313437bca51a27f979ecc4f964655205b6879f3b0

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "alarm",
    "FCR-MINT": "alarm",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "unsupported",
    "FCR-FREEZE": "alarm"
  },
  "changes": [
    "decision_only 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,action_slice_exhausted,unknown_assessment_vocabulary,program_investigation_seconds",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": true,
    "paired_id": "RQ1_2d22977434b5",
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
    "extra_category_alarms": [
      "FCR-TRANSFER",
      "FCR-FREEZE"
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "3e7fa87176cfe502a18032a71e51c370af5daba9e41823bd3e38d457c96859ac"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "dba4c6156d578fec83812482de2802154ffe7a2a3c98938a64137936997d3cd1",
          "issue": "issue_9c15915587a63f1eb350"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "5fff3616c73853d6a1da08460c260c50bbe2fe4cf26203a807870caa607d4bc3",
          "issue": "issue_c80f147ea1cb845356c0"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "db7ae2436810193e497360a077edcc540c2cc1a0067b218127f7e886a9b91e9c",
          "issue": "issue_0157ca4d2fc2e8c79a6c"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d10ff269be70a771fb15ec91f904b9c9bbd5d2139a18c42bc6525084b47c7a8a",
          "issue": "issue_0157ca4d2fc2e8c79a6c"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_2257130bc3a9d97e427e",
        "fact": "fact_46f4977c7b0bf44f6d88",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_46f4977c7b0bf44f6d88",
        "object_or_effect": "o_b23a2f2a9cb4c4c38857",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [
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
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 20
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 24
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 35
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 12
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 15
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
        "label": "financial_consent_unresolved",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "financial_value",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 8,
      "unknown_assessment_vocabulary": 3,
      "category_ambiguous_or_outside_supported_task": 1,
      "semantic_answer_outside_sent_scope": 1,
      "action_slice_exhausted": 4,
      "program_investigation_budget_exhausted": 1,
      "program_investigation_seconds": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "scope_missing": 6,
      "no_effect_in_scope": 125,
      "source_task_reading": 39,
      "no_debit_in_scope": 1,
      "new_entitlement": 1,
      "program_support": 2,
      "external_dependency": 6
    }
  }
}
```

## RQ1_43103f5773b9

证据目录 run/members/RQ1_43103f5773b9/attempt_1/，报告哈希 096e3bc904d521cbbac3e2f70de09e92168c8dd6df276c819ae7623f49729ed3

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
    "last1164 未知转有效阴性",
    "decision_only 未知转有效阴性"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": false,
    "paired_id": "RQ1_1f932eab663d",
    "state": "not_detected",
    "changes": {
      "v32": {
        "before": "not_detected",
        "after": "not_detected"
      },
      "last1164": {
        "before": "unsupported",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
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
      "no_effect_in_scope": 119,
      "source_task_reading": 31
    }
  }
}
```

## RQ1_4580c60aec2d

证据目录 run/members/RQ1_4580c60aec2d/attempt_1/，报告哈希 a2aa055ef313953a45133ec5c98574f86f777e182189c41e82ccd7c80a040ba0

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "prev200 丢失根因 D2:619:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unrelated_or_secondary_graph_pairs_deferred,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_4580c60aec2d",
        "reference": "D2:619:author:1",
        "function": "TokenERC20",
        "v32": "FN",
        "last1164": "FN",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "FN",
        "prev200_findings": [
          "finding_15fe46a6f520983e1ad9"
        ],
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
        "lost": [
          "D2:619:author:1"
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
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
        "support": "support_b63c10d50fc4ea3b3d9a",
        "fact": "fact_2ac4d9c3d31adf0e239b",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_eb52441414ff07c7300f",
        "fact": "fact_734c318a2e31b39db703",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_01220bb32396beaca0ad",
        "object_or_effect": "w_4f77037ada15eae6d39a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4f77037ada15eae6d39a",
        "grounded": true
      },
      {
        "id": "fact_025e1d854573fc7584f0",
        "object_or_effect": "w_528a3fb0bc10c5c2a1f0",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_528a3fb0bc10c5c2a1f0",
        "grounded": true
      },
      {
        "id": "fact_0269924dca2e4803db9f",
        "object_or_effect": "w_1a190b72f1bfb52584bd",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1a190b72f1bfb52584bd",
        "grounded": true
      },
      {
        "id": "fact_0b26a9083f436f9a664a",
        "object_or_effect": "w_cb1bbd53cbd58044b39e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cb1bbd53cbd58044b39e",
        "grounded": true
      },
      {
        "id": "fact_0c29368b6e29b3474972",
        "object_or_effect": "w_b14ee91083a4773ed869",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b14ee91083a4773ed869",
        "grounded": true
      },
      {
        "id": "fact_0cc4345ffd58961cf8e4",
        "object_or_effect": "w_8443439c787ee34a93a4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8443439c787ee34a93a4",
        "grounded": true
      },
      {
        "id": "fact_0cf5e4ec067a0881a389",
        "object_or_effect": "w_1cc55062bd96431c7abf",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1cc55062bd96431c7abf",
        "grounded": true
      },
      {
        "id": "fact_0d89658047a8d3f8fe8f",
        "object_or_effect": "w_bb6c16d68fe60b7c44ea",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_bb6c16d68fe60b7c44ea",
        "grounded": true
      },
      {
        "id": "fact_180a96080779ace0842d",
        "object_or_effect": "w_44917fe4fac2ad7cd720",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_44917fe4fac2ad7cd720",
        "grounded": true
      },
      {
        "id": "fact_1826033ef4adece54951",
        "object_or_effect": "w_364ba7709274f6248640",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_364ba7709274f6248640",
        "grounded": true
      },
      {
        "id": "fact_1864740c9e375e21f56a",
        "object_or_effect": "w_3c60e7892b577b741607",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3c60e7892b577b741607",
        "grounded": true
      },
      {
        "id": "fact_1881f43c73b4a2a0c516",
        "object_or_effect": "w_ef738d1767f7e31f1e1f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ef738d1767f7e31f1e1f",
        "grounded": true
      },
      {
        "id": "fact_1b3e19718a6b70e7ed98",
        "object_or_effect": "w_2acc2cfc03b6bdeaa5f5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2acc2cfc03b6bdeaa5f5",
        "grounded": true
      },
      {
        "id": "fact_1cbb4f570f6ca23fc7eb",
        "object_or_effect": "w_7b7f889ab46929b10081",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7b7f889ab46929b10081",
        "grounded": true
      },
      {
        "id": "fact_1e835cbf77e284162b14",
        "object_or_effect": "w_373844c695c28965def0",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_373844c695c28965def0",
        "grounded": true
      },
      {
        "id": "fact_1efce438d9c3e667ef34",
        "object_or_effect": "w_b19555a1bb9438e282b2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b19555a1bb9438e282b2",
        "grounded": true
      },
      {
        "id": "fact_1f11f3bedee543145b69",
        "object_or_effect": "w_c941ee251902da5572a6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c941ee251902da5572a6",
        "grounded": true
      },
      {
        "id": "fact_1fcc5a64d69b3103c3a2",
        "object_or_effect": "w_e242ee20032eb8b61e45",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e242ee20032eb8b61e45",
        "grounded": true
      },
      {
        "id": "fact_207b8d8df9b003ea0bc1",
        "object_or_effect": "w_ae2be8d9f2f2952b0616",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ae2be8d9f2f2952b0616",
        "grounded": true
      },
      {
        "id": "fact_217dae8495f5cd0e47f7",
        "object_or_effect": "w_62385ec58e56228e5408",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_62385ec58e56228e5408",
        "grounded": true
      },
      {
        "id": "fact_224198e975a63fde1214",
        "object_or_effect": "w_f754df93ccc859e71438",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f754df93ccc859e71438",
        "grounded": true
      },
      {
        "id": "fact_2387fe6a835202f8ea57",
        "object_or_effect": "w_1f82cfdc63a9199f33fb",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1f82cfdc63a9199f33fb",
        "grounded": true
      },
      {
        "id": "fact_2718c98f1c0b6df9214b",
        "object_or_effect": "w_1d4900c32747d6c7bb65",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1d4900c32747d6c7bb65",
        "grounded": true
      },
      {
        "id": "fact_283234442448c4a99619",
        "object_or_effect": "w_3a9c50ef0902ecfc4994",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3a9c50ef0902ecfc4994",
        "grounded": true
      },
      {
        "id": "fact_2a4742a106731ba4722c",
        "object_or_effect": "w_d947cc779d031e0128dd",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d947cc779d031e0128dd",
        "grounded": true
      },
      {
        "id": "fact_2ac4d9c3d31adf0e239b",
        "object_or_effect": "o_3c0e4da5c923fa812c31",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_2cdc497745c1fb9331df",
        "object_or_effect": "w_89c73a8ce3c27f6fe71a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_89c73a8ce3c27f6fe71a",
        "grounded": true
      },
      {
        "id": "fact_2ced5fa4a323e479d707",
        "object_or_effect": "w_35091fd86b9397ac05f2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_35091fd86b9397ac05f2",
        "grounded": true
      },
      {
        "id": "fact_312356eeead263753b88",
        "object_or_effect": "w_baaf53b5853c2feffa03",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_baaf53b5853c2feffa03",
        "grounded": true
      },
      {
        "id": "fact_33aa3a8f91fa184df836",
        "object_or_effect": "w_d341a1f27a8766088e28",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d341a1f27a8766088e28",
        "grounded": true
      },
      {
        "id": "fact_33dd666a5bbf09fe26cd",
        "object_or_effect": "w_78282ec433cae005a7b9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_78282ec433cae005a7b9",
        "grounded": true
      },
      {
        "id": "fact_34443fd7430b7101a8b9",
        "object_or_effect": "w_2656be7e8a69db633234",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2656be7e8a69db633234",
        "grounded": true
      },
      {
        "id": "fact_36c917cefd907985928c",
        "object_or_effect": "w_8bdd1edd039117910201",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8bdd1edd039117910201",
        "grounded": true
      },
      {
        "id": "fact_37d0f401803fe5474da4",
        "object_or_effect": "w_aa27e94ba42be932ee12",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_aa27e94ba42be932ee12",
        "grounded": true
      },
      {
        "id": "fact_39849872f524ffafeff4",
        "object_or_effect": "w_512b3ec50f04f9452629",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_512b3ec50f04f9452629",
        "grounded": true
      },
      {
        "id": "fact_3a6e25d814ed13b9ce04",
        "object_or_effect": "w_a0aedde46d531924b6b9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a0aedde46d531924b6b9",
        "grounded": true
      },
      {
        "id": "fact_3a9ebe029f6300400b10",
        "object_or_effect": "w_d3f6898e15650e48eaf6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d3f6898e15650e48eaf6",
        "grounded": true
      },
      {
        "id": "fact_3b09f6b19d11e257bed7",
        "object_or_effect": "w_6cb5396302f49989d75c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6cb5396302f49989d75c",
        "grounded": true
      },
      {
        "id": "fact_3b5812d733adb531c9e4",
        "object_or_effect": "w_9b5efd6d6dc4fd562913",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9b5efd6d6dc4fd562913",
        "grounded": true
      },
      {
        "id": "fact_3ce9fa69f32bd0860e5b",
        "object_or_effect": "w_93b8c6c9f2dd0998a5b2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_93b8c6c9f2dd0998a5b2",
        "grounded": true
      },
      {
        "id": "fact_3e44e625d94f68db071b",
        "object_or_effect": "w_411f80ecc06ae97b1187",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_411f80ecc06ae97b1187",
        "grounded": true
      },
      {
        "id": "fact_41e1dc8285e968414b75",
        "object_or_effect": "w_208a035d47a4b2a07870",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_208a035d47a4b2a07870",
        "grounded": true
      },
      {
        "id": "fact_42612f9b7b329b426359",
        "object_or_effect": "w_c5d41a874a4fd772106c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c5d41a874a4fd772106c",
        "grounded": true
      },
      {
        "id": "fact_45b955064c1590b892cf",
        "object_or_effect": "w_b410fe232d761f40db6d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b410fe232d761f40db6d",
        "grounded": true
      },
      {
        "id": "fact_494f984a96d0cb5c7a1e",
        "object_or_effect": "w_d4b15e385b0c84eb389c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d4b15e385b0c84eb389c",
        "grounded": true
      },
      {
        "id": "fact_499763fe089da3b5b3bd",
        "object_or_effect": "w_c6ed1102c40b7cb7f4a8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c6ed1102c40b7cb7f4a8",
        "grounded": true
      },
      {
        "id": "fact_4b44502594a05ef44040",
        "object_or_effect": "w_96f0f3ee3c51bc12b547",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_96f0f3ee3c51bc12b547",
        "grounded": true
      },
      {
        "id": "fact_4b48a490764538977ff1",
        "object_or_effect": "w_a46eb87f81a5d8f00986",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a46eb87f81a5d8f00986",
        "grounded": true
      },
      {
        "id": "fact_4c7367cae6fe83a36435",
        "object_or_effect": "w_425b61522ad9a5ece962",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_425b61522ad9a5ece962",
        "grounded": true
      },
      {
        "id": "fact_4cfb11fabb7d6f5a1f30",
        "object_or_effect": "w_2ecf48aeffabe7cce8c3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2ecf48aeffabe7cce8c3",
        "grounded": true
      },
      {
        "id": "fact_4d08eab92b17240ab99b",
        "object_or_effect": "w_4c7a4da5db0ebe0940e8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4c7a4da5db0ebe0940e8",
        "grounded": true
      },
      {
        "id": "fact_51e93c2d1b8d8c3e3b9f",
        "object_or_effect": "w_f174bf2ccf2befe4c5a6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f174bf2ccf2befe4c5a6",
        "grounded": true
      },
      {
        "id": "fact_5400ddafb36def5d659d",
        "object_or_effect": "w_499ed20bb4a91125aa97",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_499ed20bb4a91125aa97",
        "grounded": true
      },
      {
        "id": "fact_56cf1590bec2a7315ae5",
        "object_or_effect": "w_3439286351fdea884144",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3439286351fdea884144",
        "grounded": true
      },
      {
        "id": "fact_5722818d776f0c5b5fef",
        "object_or_effect": "w_bdad330c04ec06e45380",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_bdad330c04ec06e45380",
        "grounded": true
      },
      {
        "id": "fact_584e587474beb3ab52b9",
        "object_or_effect": "w_b7dae4d8624c48f253c4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b7dae4d8624c48f253c4",
        "grounded": true
      },
      {
        "id": "fact_5b1be9642c68812dfd3f",
        "object_or_effect": "w_4c75ffc2a01bd606e29a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4c75ffc2a01bd606e29a",
        "grounded": true
      },
      {
        "id": "fact_5f2590d1adb9fbd8f664",
        "object_or_effect": "w_6a3330799d763985fb7f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6a3330799d763985fb7f",
        "grounded": true
      },
      {
        "id": "fact_6042f763698e4ebf394a",
        "object_or_effect": "w_0135370f53ab1fbec0c8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0135370f53ab1fbec0c8",
        "grounded": true
      },
      {
        "id": "fact_60b6966c59539b05dc77",
        "object_or_effect": "w_a32dd4ffce7b9f10bc01",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a32dd4ffce7b9f10bc01",
        "grounded": true
      },
      {
        "id": "fact_60fc5b336b1f0a863505",
        "object_or_effect": "w_7028da305b513f977f91",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7028da305b513f977f91",
        "grounded": true
      },
      {
        "id": "fact_65cc993f3ad8e7310740",
        "object_or_effect": "w_6e5d939446e06030b70f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6e5d939446e06030b70f",
        "grounded": true
      },
      {
        "id": "fact_672832f86fbc2aa64749",
        "object_or_effect": "w_8959c9a1876be1d622c1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8959c9a1876be1d622c1",
        "grounded": true
      },
      {
        "id": "fact_68b8f0fc87d872a42b1b",
        "object_or_effect": "w_a89f1e36a18713fdefef",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a89f1e36a18713fdefef",
        "grounded": true
      },
      {
        "id": "fact_68ffc38a54cc682eade7",
        "object_or_effect": "w_813394bbf28dcf328277",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_813394bbf28dcf328277",
        "grounded": true
      },
      {
        "id": "fact_69632b6a2bb57d16b386",
        "object_or_effect": "w_f1745b269081470cd0d8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f1745b269081470cd0d8",
        "grounded": true
      },
      {
        "id": "fact_6a9e1645f1f02c3121bc",
        "object_or_effect": "w_65270a19a445b5150b5e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_65270a19a445b5150b5e",
        "grounded": true
      },
      {
        "id": "fact_6afc8bb3b324856bf233",
        "object_or_effect": "w_f06c4d21dd637df9a679",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f06c4d21dd637df9a679",
        "grounded": true
      },
      {
        "id": "fact_6c9fcd29703deccb262f",
        "object_or_effect": "w_d0224960e77ae052ed8c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d0224960e77ae052ed8c",
        "grounded": true
      },
      {
        "id": "fact_6e8558ef7c3ae9aea509",
        "object_or_effect": "w_970d5d49b6f5422c1b29",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_970d5d49b6f5422c1b29",
        "grounded": true
      },
      {
        "id": "fact_700e13196b793c9bc45b",
        "object_or_effect": "w_3cd4ce4cd1123fa4beb2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3cd4ce4cd1123fa4beb2",
        "grounded": true
      },
      {
        "id": "fact_7173d4bd72d9f4e09b27",
        "object_or_effect": "w_568b5766e643049665bd",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_568b5766e643049665bd",
        "grounded": true
      },
      {
        "id": "fact_734c318a2e31b39db703",
        "object_or_effect": "o_06c4c2c714b68ccbdd07",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_753b5447421518a1349a",
        "object_or_effect": "w_9ea230d56139e743721a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9ea230d56139e743721a",
        "grounded": true
      },
      {
        "id": "fact_76521cadd80abb840fd5",
        "object_or_effect": "w_38e237e6879bfd36080f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_38e237e6879bfd36080f",
        "grounded": true
      },
      {
        "id": "fact_767a943f99668654045c",
        "object_or_effect": "w_ce2644dc20d8a1d981ac",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ce2644dc20d8a1d981ac",
        "grounded": true
      },
      {
        "id": "fact_76fecfe5f3449d7158ad",
        "object_or_effect": "w_fb5b93d07d62063189c6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_fb5b93d07d62063189c6",
        "grounded": true
      },
      {
        "id": "fact_77da7e5cd642ae2746d3",
        "object_or_effect": "w_75af2558bb6e0b65f955",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_75af2558bb6e0b65f955",
        "grounded": true
      },
      {
        "id": "fact_7800cb4cadf6ea84f03c",
        "object_or_effect": "w_bfb84d5f7ced2b782e02",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_bfb84d5f7ced2b782e02",
        "grounded": true
      },
      {
        "id": "fact_79b57de8a4e832f3dab1",
        "object_or_effect": "w_3a11e7d6f200f7547379",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3a11e7d6f200f7547379",
        "grounded": true
      },
      {
        "id": "fact_7a126b7bc2edfaa87e93",
        "object_or_effect": "w_01135179431a109292e5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_01135179431a109292e5",
        "grounded": true
      },
      {
        "id": "fact_7a2cc938267788ad6a95",
        "object_or_effect": "w_5c5dd4e812a73a5aad69",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5c5dd4e812a73a5aad69",
        "grounded": true
      },
      {
        "id": "fact_7a619329517d10ed2b12",
        "object_or_effect": "w_18124d5bbff47606f231",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_18124d5bbff47606f231",
        "grounded": true
      },
      {
        "id": "fact_7cf2e070537fbaec2017",
        "object_or_effect": "w_312004ac461b49695bc5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_312004ac461b49695bc5",
        "grounded": true
      },
      {
        "id": "fact_7d774df48446cfda9ed8",
        "object_or_effect": "w_890c5ed7de310d46ecb8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_890c5ed7de310d46ecb8",
        "grounded": true
      },
      {
        "id": "fact_82baefa07079627117a9",
        "object_or_effect": "w_23ffd0ac3ecc177a72e7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_23ffd0ac3ecc177a72e7",
        "grounded": true
      },
      {
        "id": "fact_8319450b264c878009cb",
        "object_or_effect": "w_156928f7b5dd429e0ffb",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_156928f7b5dd429e0ffb",
        "grounded": true
      },
      {
        "id": "fact_8449f3f1180c0f81d3b7",
        "object_or_effect": "w_96cf41332e3f921654f4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_96cf41332e3f921654f4",
        "grounded": true
      },
      {
        "id": "fact_8661fe96d665423cca72",
        "object_or_effect": "w_2e85f19900712fe674ba",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2e85f19900712fe674ba",
        "grounded": true
      },
      {
        "id": "fact_881ed86fae190295b1d5",
        "object_or_effect": "w_9ee1310a5d6de7b4fc1f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9ee1310a5d6de7b4fc1f",
        "grounded": true
      },
      {
        "id": "fact_88a048a0a96a2dc49cdd",
        "object_or_effect": "w_c41e0433aa58617b65e6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c41e0433aa58617b65e6",
        "grounded": true
      },
      {
        "id": "fact_8a05e8a80016bddeaa15",
        "object_or_effect": "w_0d8d93d348f1b79b4801",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0d8d93d348f1b79b4801",
        "grounded": true
      },
      {
        "id": "fact_8a28c4f23d21137b3567",
        "object_or_effect": "w_ed0c4146f0525fa67a62",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ed0c4146f0525fa67a62",
        "grounded": true
      },
      {
        "id": "fact_8b6ebef0975a1362a6ee",
        "object_or_effect": "w_14b72aaa9ad58b8a0803",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_14b72aaa9ad58b8a0803",
        "grounded": true
      },
      {
        "id": "fact_90d54cbe42f23e9b0811",
        "object_or_effect": "w_7f97f14a3e1891fa398e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7f97f14a3e1891fa398e",
        "grounded": true
      },
      {
        "id": "fact_9128c43c0a1cdafbe17a",
        "object_or_effect": "w_1239ce51e7dc4d1ec12f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1239ce51e7dc4d1ec12f",
        "grounded": true
      },
      {
        "id": "fact_924e43aca3dbfc4e819b",
        "object_or_effect": "w_c3ab5a9c31919d8e3ac2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c3ab5a9c31919d8e3ac2",
        "grounded": true
      },
      {
        "id": "fact_93030e1c6864052fb92a",
        "object_or_effect": "w_85fdfddb518617f0488e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_85fdfddb518617f0488e",
        "grounded": true
      },
      {
        "id": "fact_935bc1fd491522498946",
        "object_or_effect": "w_15ce37bad2b84e4f0688",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_15ce37bad2b84e4f0688",
        "grounded": true
      },
      {
        "id": "fact_955beff8c8521aad3f60",
        "object_or_effect": "w_1ea8f844c9887e5bca87",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1ea8f844c9887e5bca87",
        "grounded": true
      },
      {
        "id": "fact_95d36fb0603b8979f7df",
        "object_or_effect": "w_9365b76b41f8dba1b87a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9365b76b41f8dba1b87a",
        "grounded": true
      },
      {
        "id": "fact_965211a00ae7389dfb58",
        "object_or_effect": "w_134bc91265ec3891f8ed",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_134bc91265ec3891f8ed",
        "grounded": true
      },
      {
        "id": "fact_967eef23bf423ab0ce34",
        "object_or_effect": "w_f101ac131933f08a5c3b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f101ac131933f08a5c3b",
        "grounded": true
      },
      {
        "id": "fact_97340aec67fac2e91583",
        "object_or_effect": "w_8e5b9d2bcf6465c2d022",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8e5b9d2bcf6465c2d022",
        "grounded": true
      },
      {
        "id": "fact_98440d95a008697fee33",
        "object_or_effect": "w_09482eaafa89c5eab223",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_09482eaafa89c5eab223",
        "grounded": true
      },
      {
        "id": "fact_9bbff48874d992352ac7",
        "object_or_effect": "w_33fc5895404d52d27d5f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_33fc5895404d52d27d5f",
        "grounded": true
      },
      {
        "id": "fact_9c386191abb31b5433ed",
        "object_or_effect": "w_550216453764e84429e7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_550216453764e84429e7",
        "grounded": true
      },
      {
        "id": "fact_9d6c7a969d74da9b8ca3",
        "object_or_effect": "w_ddfc7d22bd6a1435f2c4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ddfc7d22bd6a1435f2c4",
        "grounded": true
      },
      {
        "id": "fact_a479f28379999302a996",
        "object_or_effect": "w_7f49c000f99a33fa0a84",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7f49c000f99a33fa0a84",
        "grounded": true
      },
      {
        "id": "fact_a4e081a2cd7b40fa6f51",
        "object_or_effect": "w_555128389b58dd5d9911",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_555128389b58dd5d9911",
        "grounded": true
      },
      {
        "id": "fact_a51e334ef44d414af1ba",
        "object_or_effect": "w_88939a7ed6d6a0bcc489",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_88939a7ed6d6a0bcc489",
        "grounded": true
      },
      {
        "id": "fact_a541a34f92af6ca996db",
        "object_or_effect": "w_13e0146c12c8e2121064",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_13e0146c12c8e2121064",
        "grounded": true
      },
      {
        "id": "fact_a58cb011d9f861451ad3",
        "object_or_effect": "w_c3815e4c36bc9fe6ac03",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c3815e4c36bc9fe6ac03",
        "grounded": true
      },
      {
        "id": "fact_a5bc635e86221045c447",
        "object_or_effect": "w_7a916b55a3cd1662e7ad",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7a916b55a3cd1662e7ad",
        "grounded": true
      },
      {
        "id": "fact_a6a56a94841476c01de1",
        "object_or_effect": "w_b528ebd86c2265e8e5ed",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b528ebd86c2265e8e5ed",
        "grounded": true
      },
      {
        "id": "fact_a7a1b015c660c19d66ca",
        "object_or_effect": "w_c1c832f82fc9cb8b770d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c1c832f82fc9cb8b770d",
        "grounded": true
      },
      {
        "id": "fact_aa9217a98494f692bade",
        "object_or_effect": "w_04dd0064a21117d2bfce",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_04dd0064a21117d2bfce",
        "grounded": true
      },
      {
        "id": "fact_aad1e7f03ed2239d7f81",
        "object_or_effect": "w_584b8fe84bac4dbc05e0",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_584b8fe84bac4dbc05e0",
        "grounded": true
      },
      {
        "id": "fact_ab5370e341a07650d221",
        "object_or_effect": "w_81e87abd9f3673158ae7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_81e87abd9f3673158ae7",
        "grounded": true
      },
      {
        "id": "fact_ac6b76de75a35288fb9f",
        "object_or_effect": "w_ad24b4e078d6577d5db2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ad24b4e078d6577d5db2",
        "grounded": true
      },
      {
        "id": "fact_add828089ee068155b84",
        "object_or_effect": "w_48b0d6a6ed9eaff444ca",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_48b0d6a6ed9eaff444ca",
        "grounded": true
      },
      {
        "id": "fact_ae71edc8c64c10566030",
        "object_or_effect": "w_3d815973d3f51f6cd836",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3d815973d3f51f6cd836",
        "grounded": true
      },
      {
        "id": "fact_af3590fb25af82187763",
        "object_or_effect": "w_d5d9b77b566060dded05",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d5d9b77b566060dded05",
        "grounded": true
      },
      {
        "id": "fact_b2e8ef155739d36e95b0",
        "object_or_effect": "w_ad86f41d41d1e35a563d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ad86f41d41d1e35a563d",
        "grounded": true
      },
      {
        "id": "fact_b658f518193b21577559",
        "object_or_effect": "w_84a72a79ba815b288b0a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_84a72a79ba815b288b0a",
        "grounded": true
      },
      {
        "id": "fact_b6b6a8383e669f0bd0a5",
        "object_or_effect": "w_04a236b4c7b4567283a6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_04a236b4c7b4567283a6",
        "grounded": true
      },
      {
        "id": "fact_b6ccc042ddafc8a01119",
        "object_or_effect": "w_1f2a528bc5625f84f2f5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1f2a528bc5625f84f2f5",
        "grounded": true
      },
      {
        "id": "fact_ba4cc2300772fdfa21e7",
        "object_or_effect": "w_295311028aba755d694c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_295311028aba755d694c",
        "grounded": true
      },
      {
        "id": "fact_bee216b6d70f0c31af88",
        "object_or_effect": "w_b869d60c5cea2ce41db2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b869d60c5cea2ce41db2",
        "grounded": true
      },
      {
        "id": "fact_c0a65e2db7c0a67348f6",
        "object_or_effect": "w_c07915995edfee4d2058",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c07915995edfee4d2058",
        "grounded": true
      },
      {
        "id": "fact_c30c7446f79e42651b96",
        "object_or_effect": "w_e1603ae7e4db41c994d6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e1603ae7e4db41c994d6",
        "grounded": true
      },
      {
        "id": "fact_c3562621154302491313",
        "object_or_effect": "w_fc893be79d2480493438",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_fc893be79d2480493438",
        "grounded": true
      },
      {
        "id": "fact_c4439f30f38dcf0becde",
        "object_or_effect": "w_b5152bda3828e2cc2600",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b5152bda3828e2cc2600",
        "grounded": true
      },
      {
        "id": "fact_cc9c34d7a91581246d88",
        "object_or_effect": "w_e2a4585c07169a5ca3dc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e2a4585c07169a5ca3dc",
        "grounded": true
      },
      {
        "id": "fact_cd86ac2cb4f4b90c232c",
        "object_or_effect": "w_7f238bc9279e87f527ad",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7f238bc9279e87f527ad",
        "grounded": true
      },
      {
        "id": "fact_ceab42d9ba4e1edab0da",
        "object_or_effect": "w_2304b2342a1c1e31a806",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2304b2342a1c1e31a806",
        "grounded": true
      },
      {
        "id": "fact_cfdf10ae3ee1c006813a",
        "object_or_effect": "w_c0e00edd2a6b1e3ab1a4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c0e00edd2a6b1e3ab1a4",
        "grounded": true
      },
      {
        "id": "fact_d129a7b642e93cb05ee9",
        "object_or_effect": "w_5db2a86e7575a607b119",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5db2a86e7575a607b119",
        "grounded": true
      },
      {
        "id": "fact_d13efb8ea2d0aa697373",
        "object_or_effect": "w_6ed7bdaa2c9146565a5c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6ed7bdaa2c9146565a5c",
        "grounded": true
      },
      {
        "id": "fact_d16c10a16b89e4c80521",
        "object_or_effect": "w_4a31e8b1f5682033a75e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4a31e8b1f5682033a75e",
        "grounded": true
      },
      {
        "id": "fact_d1b6ab53ba2700186a8c",
        "object_or_effect": "w_e11abf4bb329e08a7f7a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e11abf4bb329e08a7f7a",
        "grounded": true
      },
      {
        "id": "fact_d1c2d9d09ad6aeabafe3",
        "object_or_effect": "w_3b7c0616c5a9bf29fb4b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3b7c0616c5a9bf29fb4b",
        "grounded": true
      },
      {
        "id": "fact_d31586eeedfe89c7352b",
        "object_or_effect": "w_40035c8819b0f3f2ead0",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_40035c8819b0f3f2ead0",
        "grounded": true
      },
      {
        "id": "fact_d336473be74e0ef76e22",
        "object_or_effect": "w_37a02aa7a376dabceeb6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_37a02aa7a376dabceeb6",
        "grounded": true
      },
      {
        "id": "fact_d3813921bc7abd19e11f",
        "object_or_effect": "w_e75956b8f5e36f2a6ab4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e75956b8f5e36f2a6ab4",
        "grounded": true
      },
      {
        "id": "fact_d48a95b616c025f3a8c8",
        "object_or_effect": "w_4c9cde30b88f093a1807",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4c9cde30b88f093a1807",
        "grounded": true
      },
      {
        "id": "fact_d5f9b7a0d61bda0d8869",
        "object_or_effect": "w_08a3612940fbcab66568",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_08a3612940fbcab66568",
        "grounded": true
      },
      {
        "id": "fact_d5fc61823e53f81e617e",
        "object_or_effect": "w_50b042ce019613f28c1b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_50b042ce019613f28c1b",
        "grounded": true
      },
      {
        "id": "fact_d83af0848db030592738",
        "object_or_effect": "w_be6d4c781c72c67155c2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_be6d4c781c72c67155c2",
        "grounded": true
      },
      {
        "id": "fact_d927205dc681403a3ca1",
        "object_or_effect": "w_c034539fd7e42b77be34",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c034539fd7e42b77be34",
        "grounded": true
      },
      {
        "id": "fact_db930fd488256fd4d262",
        "object_or_effect": "w_6a5497ca04a0943bfa98",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6a5497ca04a0943bfa98",
        "grounded": true
      },
      {
        "id": "fact_de8d51d213a3fa92f7da",
        "object_or_effect": "w_78d2599eb7d374b6234e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_78d2599eb7d374b6234e",
        "grounded": true
      },
      {
        "id": "fact_dea1c104020bd4bdf2e0",
        "object_or_effect": "w_7980cf3489599d3eed72",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7980cf3489599d3eed72",
        "grounded": true
      },
      {
        "id": "fact_deb72527511c20267c85",
        "object_or_effect": "w_b1af1fecc83d5aa68fcc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b1af1fecc83d5aa68fcc",
        "grounded": true
      },
      {
        "id": "fact_e57a1e5c4dd6848c6eac",
        "object_or_effect": "w_bf009c38ce7fc237c2b9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_bf009c38ce7fc237c2b9",
        "grounded": true
      },
      {
        "id": "fact_e9e64336a3270b145825",
        "object_or_effect": "w_e3584683d4d9ef9b1d02",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e3584683d4d9ef9b1d02",
        "grounded": true
      },
      {
        "id": "fact_e9f48f8815f15435f994",
        "object_or_effect": "w_65d7e3f716936c924147",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_65d7e3f716936c924147",
        "grounded": true
      },
      {
        "id": "fact_eb4be2ef2bb915dac4eb",
        "object_or_effect": "w_21de84b41b2747bfc18d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_21de84b41b2747bfc18d",
        "grounded": true
      },
      {
        "id": "fact_ec5bfa11339585130fc5",
        "object_or_effect": "w_90333f4e5cc54153c163",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_90333f4e5cc54153c163",
        "grounded": true
      },
      {
        "id": "fact_edb2634866392d876b88",
        "object_or_effect": "w_cfcc8ec364f5d9839b95",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cfcc8ec364f5d9839b95",
        "grounded": true
      },
      {
        "id": "fact_f3b57dee91aae7205a04",
        "object_or_effect": "w_dbdcee4398b966077e46",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_dbdcee4398b966077e46",
        "grounded": true
      },
      {
        "id": "fact_f3e5915bfd35f8b31d37",
        "object_or_effect": "w_3a0542fb2e8cdeadc75b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3a0542fb2e8cdeadc75b",
        "grounded": true
      },
      {
        "id": "fact_f55cbea40373c3dfaf6d",
        "object_or_effect": "w_85d08adb02512a89eb22",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_85d08adb02512a89eb22",
        "grounded": true
      },
      {
        "id": "fact_f6324b6c5590e6e9de0d",
        "object_or_effect": "w_bbcd3f63cfff95dcb5c8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_bbcd3f63cfff95dcb5c8",
        "grounded": true
      },
      {
        "id": "fact_f77e6e57cbf1998b6335",
        "object_or_effect": "w_fb1b2fe62cc2c33b5ec6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_fb1b2fe62cc2c33b5ec6",
        "grounded": true
      },
      {
        "id": "fact_f78766429c741dc57b0d",
        "object_or_effect": "w_32f7c8d4afbf3e5ef246",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_32f7c8d4afbf3e5ef246",
        "grounded": true
      },
      {
        "id": "fact_f7d0bd5ba7e6064f0cbd",
        "object_or_effect": "w_c46939ab3a3169a3f3cc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c46939ab3a3169a3f3cc",
        "grounded": true
      },
      {
        "id": "fact_f845eb6cc50405bde6e1",
        "object_or_effect": "w_3479f8de2c5fc8e26ff4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3479f8de2c5fc8e26ff4",
        "grounded": true
      },
      {
        "id": "fact_fee57c04b04c5badc2d3",
        "object_or_effect": "w_24ad8a93b20a37034527",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_24ad8a93b20a37034527",
        "grounded": true
      },
      {
        "id": "fact_ff9977798fe1837e8a75",
        "object_or_effect": "w_8d6b05bcf0a343b38895",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8d6b05bcf0a343b38895",
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 8
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 4,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 12,
      "source_task_reading": 6,
      "policy_missing": 2,
      "external_dependency": 2
    }
  }
}
```

## RQ1_46a031a993c1

证据目录 run/members/RQ1_46a031a993c1/attempt_1/，报告哈希 2c1adc83af235f41caca813d5f6573cc4615be751291a804521749e75479ccee

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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,ambiguous_confirmation_not_a_risk_judgment"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": false,
    "paired_id": "RQ1_985c6fd1d4e4",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "85f7d3a80db78eb792938c5dbbee5b1952e6894a1ee3643e314e964f7f3079a0",
          "issue": "issue_26f1cb10a473bca94a50"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a103835a6cafadf282fd3d1055395939d87d41cb44bee902166244472c125795",
          "issue": "issue_26f1cb10a473bca94a50"
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
          "detail_sha256": "166a35b94ca7fdafd98e190fde27815a8bd86bcedda1835550a116572570a8e6",
          "issue": "issue_5c1bad90bf6f8b6a0729"
        },
        {
          "reason": "ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "43bed725d3928f2ad6839ab2eaf1445fe7dad71be6b9620b12daa0c426488fd6",
          "issue": "issue_5c1bad90bf6f8b6a0729"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 6,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 1,
      "ambiguous_confirmation_not_a_risk_judgment": 1,
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
      "no_effect_in_scope": 44,
      "source_task_reading": 1
    }
  }
}
```

## RQ1_475c7d9ec738

证据目录 run/members/RQ1_475c7d9ec738/attempt_1/，报告哈希 5e0c864704d64307a1c960020a9f140956c377fb850ec6589b7bd0d26ae34c48

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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,no_locatable_source,category_ambiguous_or_outside_supported_task"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": false,
    "paired_id": "RQ1_b84042e6eefd",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "a0e5c7f2afa3b56ca1291e1b5d10282bef47abb32237a6d5100e253dc9d87347",
          "issue": "issue_88e2b6d64ec03eb44e99"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "726b00c6f552e29e8dbe8ee168db1457b85cf64987f0be1346ed3122f02feabd",
          "issue": "issue_88e2b6d64ec03eb44e99"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "2e138343b627e9a8762a591eea3bc7811f6038a5d1a61b802318840f6c76d9d9",
          "issue": "issue_c94ff8d9900cbbb7e6cb"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_63c481b148935b125404",
        "fact": "fact_54a1f1d56c8acec2c158",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_8f249ef02dcf3e810d76",
        "fact": "fact_f931ecf473b699a50fbf",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_f4f5b601450aea79f765",
        "fact": "fact_03495e9279dbb1e5d3d2",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_03495e9279dbb1e5d3d2",
        "object_or_effect": "o_a0a071798e3434f52959",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_1d27a4fbebb21e513238",
        "object_or_effect": "w_0922c68aeb25f15f63f8",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0922c68aeb25f15f63f8",
        "grounded": true
      },
      {
        "id": "fact_54a1f1d56c8acec2c158",
        "object_or_effect": "o_48361f5add0421bc9923",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_f931ecf473b699a50fbf",
        "object_or_effect": "o_a51dfd72aa925e0aa897",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 3,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 2,
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
      "no_effect_in_scope": 29,
      "source_check_excluded": 1
    }
  }
}
```

## RQ1_4968e56244c9

证据目录 run/members/RQ1_4968e56244c9/attempt_1/，报告哈希 de436901e41e7f444c7baf044142bc8df28e051270a55cfecc80625666512fd2

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "unsupported",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "not_detected",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "v32 退为未知，不能当作纠正",
    "last1164 退为未知，不能当作纠正",
    "prev200 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,shared_declaration_in_distinct_applied_contexts,invalid_semantic_row",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": false,
    "paired_id": "RQ1_b731957fa974",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "cb119108baf68a28b81b98b5d708f838e416f4a5e82366862d43417f4cb5715d",
          "issue": "issue_8ea76adf937b69e18dd6"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "17da85d4e5d26867fda954252069b9558d34d3b65fb80024e20ea2fe633a015d",
          "issue": "issue_8ea76adf937b69e18dd6"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "eba1abfa5e0e64899a5942c695c44b80b8a20ff384f758153b111c2f18ba1bdc",
          "issue": "issue_b84a0065d9fd4f848446"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "fac8a872c369be23a3a12b7e97d42498d01a6b0ee4b32f2257e5d1b46b934f2f",
          "issue": "issue_b84a0065d9fd4f848446"
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
          "detail_sha256": "ab289c7b8b503bc6206379f945980659316d7cd15915f628aeae9eb2f3c69dbe",
          "issue": "issue_623b04f305d20e370d07"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "a9ebaf4ec83bf090eb365cbbb6aaa1780c792e104dcfe9775df0be1529679852",
          "issue": "issue_623b04f305d20e370d07"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_134106524f8901cfce70",
        "fact": "fact_4d185ed5d59661188f72",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_15d9c58fdc75aa95ed1a",
        "fact": "fact_468cc1dfa3d20a60685c",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_65dc4bd1846a2e6110a7",
        "fact": "fact_fef3e8ddeba7f500c7ee",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_468cc1dfa3d20a60685c",
        "object_or_effect": "o_af682b752b5360dd9a55",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_4d185ed5d59661188f72",
        "object_or_effect": "o_dec34ac2df965b3caa20",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_fef3e8ddeba7f500c7ee",
        "object_or_effect": "o_1cfb4a14298a7dca9cac",
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
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 1,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 2,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE",
      "FCR-PAUSE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 211,
      "source_task_reading": 25,
      "external_dependency": 6,
      "scope_missing": 2,
      "covered_holder_grant": 1
    }
  }
}
```

## RQ1_49db443acf1d

证据目录 run/members/RQ1_49db443acf1d/attempt_1/，报告哈希 2724644993bd78be402435c054f79f06be851ee22f532fd2a3f1bac5d41a1f5a

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,no_locatable_source"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": false,
    "paired_id": "RQ1_4febca8bfe3b",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ab3e108def06be2be8853bf2db34cb7b237e8a6ee0fc93fe1731b74179c254a5",
          "issue": "issue_94fb905df92abe613237"
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
          "detail_sha256": "843a4a2940d928f1c71a65c73892d563142e4fa6b8cd8b358572067d6b9ce47d",
          "issue": "issue_72e247ad86780c858439"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_5b813f3b50f017a621fa",
        "fact": "fact_4fd13cf90aee55ede357",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_8ec45566dbe21e218c56",
        "fact": "fact_ed7b8106a344ef9d0c0c",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_93ebfab1837e7ba08fa3",
        "fact": "fact_25fe07448e7b79976e04",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_25fe07448e7b79976e04",
        "object_or_effect": "o_f5a1317599cdd6e2d8d9",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_4fd13cf90aee55ede357",
        "object_or_effect": "o_ecc61408093fdfefe761",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_ed7b8106a344ef9d0c0c",
        "object_or_effect": "o_51b6f9d7ca7d4f07eadf",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 4,
      "unknown_assessment_vocabulary": 2,
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
      "no_effect_in_scope": 18,
      "source_check_excluded": 1,
      "scoped_counter": 1
    }
  }
}
```

## RQ1_4be3030c4533

证据目录 run/members/RQ1_4be3030c4533/attempt_1/，报告哈希 d6f70c105b9d810697ae1da2bded93a03043c3c0f9463dce58107789e306d968

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "alarm",
    "FCR-MINT": "unsupported",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "unsupported",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "v32 退为未知，不能当作纠正",
    "last1164 退为未知，不能当作纠正",
    "prev200 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,action_slice_exhausted",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": false,
    "paired_id": "RQ1_af7c473b8cca",
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
    "extra_category_alarms": [
      "FCR-TRANSFER"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "696786ea45779e6fb22f757b3539da18abdeab3cdaf1ec9480e26c5459a13233",
          "issue": "issue_e05f29803805aeea1b06"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "71173855484054782c3d6fa0a39ea7e33f2133890ce9c35ee6037ffc105f1c4f",
          "issue": "issue_e05f29803805aeea1b06"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "f30f3e0904a575a1107792a328184c5ba84ba778cb4ca8af27ece75c2228d7cb",
          "issue": "issue_ecd8ecff73eeac0eeda6"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1bd2ddce3e3b8b564e8a7289ef68caf4b0c3cc17787f51f8faec810a7ed65b48",
          "issue": "issue_ecd8ecff73eeac0eeda6"
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
          "detail_sha256": "dc8bb4e86f13e3eb64c95458a9ff345d8ecb7995824107c2a68cb63ca46dc7b7",
          "issue": "issue_8414482f764b91136b4c"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "93cf6d34d9ba206ebf341d9117cb24e95fff9c8cf211446abc69add483680a2b",
          "issue": "issue_8414482f764b91136b4c"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_1b4cb1a40d45e3dc3d24",
        "fact": "fact_ebee52ca8fef9b835300",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_ebee52ca8fef9b835300",
        "object_or_effect": "o_01bb288a18a77979ceb9",
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
        "count": 23
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "financial_consent_unresolved",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 8
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "same_request_amount_change",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 14
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 20
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 1
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "financial_value",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 4,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 1,
      "action_slice_exhausted": 2,
      "noncached_action_limit": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "scope_missing": 4,
      "no_effect_in_scope": 127,
      "source_task_reading": 34,
      "program_support": 1,
      "covered_holder_grant": 2,
      "external_dependency": 7
    }
  }
}
```
