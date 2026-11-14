# 逐例审阅

## RQ1_024b9da10799

证据目录 run/members/RQ1_024b9da10799/attempt_1/，报告哈希 81549f4c2ade87a28bb8fc733840bb9e41aef427811b1110c7cd3ecfd9156ea2

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope,category_ambiguous_or_outside_supported_task",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": false,
    "paired_id": "RQ1_73b13298e227",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "82b50cb54ed784bf3d92f571dd0ca54c55baeebc91edd3b05be40da9ada74baf",
          "issue": "issue_118435a65b5c8ef709fd"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "419a650d5bd96f61b643c6a862334a7d7b2eac9e2cbf42edcd8eb1760dac243b",
          "issue": "issue_118435a65b5c8ef709fd"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 3,
      "semantic_answer_outside_sent_scope": 2,
      "invalid_semantic_row": 4,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "no_locatable_source": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 164,
      "model_phase_missing": 36
    }
  }
}
```

## RQ1_0267e2a8ebb2

证据目录 run/members/RQ1_0267e2a8ebb2/attempt_1/，报告哈希 65928dc5ff06fb6674624112947456a9d823868d056bd22add4dacc88f7ff6c2

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "alarm",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "unsupported",
    "FCR-FREEZE": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,action_slice_exhausted,unbound_or_inapplicable_seed,unknown_assessment_vocabulary",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": true,
    "paired_id": "RQ1_3b4d9f6eb96f",
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
          "detail_sha256": "af3447c571b34f76aa9e3568638b1dbe9c51759a7f137ba7615c292f9bab8c1c",
          "issue": "issue_05ab27cb4cde8f96915a"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "20b4dd858cd5651b0120eb681a2775c5576054aecc5583c080fb025d48b2cd8b",
          "issue": "issue_a9cd7c88167040fce78b"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "87773ef5a22389dbbefbfe219f2a4d910fffade09f80a53569f608596e0b82d1",
          "issue": "issue_b03f96f4a8a5b18242c0"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "381cb9059ccfa0c65d5bfe6d9ffbd73e3a3a24c1e012c9c655809f2f7bd7f6d4",
          "issue": "issue_b03f96f4a8a5b18242c0"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "3c90554f4ebe1616c46c64fcb1dd74c96310d727ee76674daac6c702fb652184",
          "issue": "issue_40558facb59b75815b35"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "1b41befbf45883c2d346df9b4c2579eb98639e31b6010b847fe65dcd9a88bb1d",
          "issue": "issue_40558facb59b75815b35"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_1e32f18a6d85609a079e",
        "fact": "fact_4028e17412d07547706d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_bdeb8458424e4cd8b88b",
        "fact": "fact_4028e17412d07547706d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_4028e17412d07547706d",
        "object_or_effect": "o_3ed9f0f34434de90c7ab",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "financial_consent_unresolved",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 39
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
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 8
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 7
      },
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 16
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 37
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 10
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "same_request_amount_change",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 3,
      "invalid_semantic_row": 7,
      "unknown_assessment_vocabulary": 3,
      "category_ambiguous_or_outside_supported_task": 2,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 1,
      "action_slice_exhausted": 4,
      "noncached_action_limit": 2,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "scope_missing": 5,
      "no_effect_in_scope": 125,
      "source_task_reading": 37,
      "covered_holder_grant": 2,
      "no_debit_in_scope": 2,
      "new_entitlement": 1,
      "external_dependency": 7,
      "program_support": 1
    }
  }
}
```

## RQ1_0526c008875c

证据目录 run/members/RQ1_0526c008875c/attempt_1/，报告哈希 359c8a7e7d00ba751417f0ac68a3d6988ef6cc22d72a63568dbf948e849754ff

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,unknown_assessment_vocabulary,no_locatable_source",
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
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "8bbfa704866c1bec506347e3462db5d6a25be92577a267d6cf30f074b9d20a7c",
          "issue": "issue_70a62d3843fad8154d3c"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "94455a110c654fdcd1b57711c1cf4974949eb9e18b1e824f25c029d5de6f7c86",
          "issue": "issue_7281b62c27fb21ea99b5"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "092314133a5e64c818e5a0f197c7df91e19d119b6b1a502e216013d92a998ca7",
          "issue": "issue_7281b62c27fb21ea99b5"
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
      "invalid_semantic_row": 13,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 4,
      "no_locatable_source": 2,
      "category_ambiguous_or_outside_supported_task": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "model_phase_missing": 2,
      "no_effect_in_scope": 1
    }
  }
}
```

## RQ1_053265dda42e

证据目录 run/members/RQ1_053265dda42e/attempt_1/，报告哈希 7ba99f99a05ef41450595484bc5c53614167d8cc9d4d089784dd2560612e8687

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [],
    "findings": [
      {
        "idx": 0,
        "member": "RQ1_053265dda42e",
        "finding": "finding_05c025f97b2920bbf86d",
        "function": "fallback()",
        "location": {
          "file": "units/program.sol",
          "start": 649,
          "length": 714,
          "ast_id": 159
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_053265dda42e', 'units/program.sol', 649)",
        "source_excerpt": "function () payable{\n        if (block.number - period >= blockheight){ \n            bool isSuccess=false; \n            var nextStake = this.balance * WINNERTAX_PRECENT/100;  \n            if (isSuccess == false) \n                isSuccess = whale.send(this.balance - nextStake); \n            MatthewWon(\"Matthew won\", whale, this.balance, block.number);\n            setFacts();\n            if (mustBeDestroyed) selfdestruct(whale); \n            return;\n        }else{ \n            if (msg.value < this.balance + DELTA) throw; \n            bool isOtherSuccess = msg.sender.send(this.balance); \n            setFacts(); \n            StakeIncreased(\"stake increased\", whale, this.balance, blockheight);\n        }\n    }",
        "source_sha256": "fd0090415eb98ee048de2fee8083d61743a02237e32ce21967fd34573aa416cf",
        "note": "冻结参考无该根因，按参考外报警记录；未据此证明其业务上错误。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 649. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 649,
              "length": 714,
              "ast_id": 159
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
          "E5"
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
          "detail_sha256": "89d190b6f9691719b403442d7c245edbe3fe7725f0f268efecd9e8489266826e",
          "issue": "issue_30d384edfeaafc4b49e3"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ff4678882b4adc0875ada71c9d0a2debe59c39c297c7954b2a4cba91c7d2b0d3",
          "issue": "issue_30d384edfeaafc4b49e3"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "c69cae07522dc69daa1f65c02f1c3c67454393f6224e72cad8873a3956568a4e",
          "issue": "issue_3b7e05024b1badc3c9c4"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f34c67e3d63133efaaf557b4988f86c00f76c930954ada6715012e46b6228889",
          "issue": "issue_3b7e05024b1badc3c9c4"
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
        "label": "direct_callback_influence",
        "answer": "sat",
        "count": 7
      },
      {
        "label": "callback_influence",
        "answer": "sat",
        "count": 7
      },
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
      "invalid_semantic_row": 6,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 2,
      "source_task_reading": 2,
      "policy_missing": 1
    }
  }
}
```

## RQ1_085aaca2f412

证据目录 run/members/RQ1_085aaca2f412/attempt_1/，报告哈希 2993fc0a7eeb1d63520d84f226f9636607527e13d863648f91bf9c0067f07b05

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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": false,
    "paired_id": "RQ1_c9626779c857",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d061fa383be4a97c57331868d79d20b4f9d5fa412eaf2e06b9c02019e8d83f8a",
          "issue": "issue_f926535bda25e05e98b2"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f5a4572eb02266338ace139bfab329fb6b34e8bb04bcc8d1d9d952378613b7bd",
          "issue": "issue_d9393baa986966d0fa39"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_8c733867ebac1e764021",
        "fact": "fact_06c60a47323f6a9f2632",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_06c60a47323f6a9f2632",
        "object_or_effect": "o_e0b92a8edb52ace97307",
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
      "unbound_or_inapplicable_seed": 5,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 119,
      "scope_missing": 2,
      "source_task_reading": 4,
      "external_dependency": 10
    }
  }
}
```

## RQ1_0bcbefea1890

证据目录 run/members/RQ1_0bcbefea1890/attempt_1/，报告哈希 56895f85bf2d9430f19715bc4859bda0bf4c66ceb838a035766e744729d1da50

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:614:S1",
    "last1164 丢失根因 D2:614:S1",
    "prev200 丢失根因 D2:614:S1",
    "decision_only 丢失根因 D2:614:S1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 semantic_answer_outside_sent_scope,unknown_assessment_vocabulary,unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_0bcbefea1890",
        "reference": "D2:614:S1",
        "function": "selfdestructs",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_834feeae84ec36968872"
        ],
        "decision_only_findings": [
          "finding_5c47f77e1815994c23a4"
        ],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:614:S1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:614:S1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:614:S1"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:614:S1"
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
          "detail_sha256": "fbdfe3ca8972fc1e6861699ffd67baaab3f4c278bde4c72006c6e100080541ef",
          "issue": "issue_403e7e2babad6b781bda"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "193f3d8425853c6c7319f7dab1e18b8454a84ff4fd41f6aec2ac5b4571a558e4",
          "issue": "issue_403e7e2babad6b781bda"
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
          "detail_sha256": "795cd229c3b64ba10f8a4ca7bccc9b6c92440650118a8b1a982f55959630914a",
          "issue": "issue_b554eb6d41d7912bf95e"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [
      4814
    ],
    "new": [],
    "disappeared_to_unknown": true,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_21bcc34e9557cb88d306",
        "fact": "fact_d374f31adf5f7a5c23ba",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_d374f31adf5f7a5c23ba",
        "object_or_effect": "o_fe75de25fd4846c5b4a9",
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
        "answer": "sat",
        "count": 2
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "requester_opens_other_holders_gate",
        "answer": "unsat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 1,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 4,
      "unrelated_or_secondary_graph_pairs_deferred": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 17,
      "source_task_reading": 17,
      "policy_missing": 2,
      "external_dependency": 2
    }
  }
}
```

## RQ1_0bf6f8bce8d9

证据目录 run/members/RQ1_0bf6f8bce8d9/attempt_1/，报告哈希 c8959d93a5c6f0b348776daf9a264f29d0a7436b375fe2fb9661c241210ec3a8

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,unrelated_or_secondary_graph_pairs_deferred",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": false,
    "paired_id": "RQ1_196284e657b0",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ff19c089d897d826271c892df84ff8e657ccc9e0f893277a7a5e4e4274416e30",
          "issue": "issue_31b3af5db467ae5cb2cf"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f435b2d57dc47e4f381871570e0abf0ec642a10c680d866bb01412815dfd6bed",
          "issue": "issue_a475ae202fa5b463b3b8"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "b58828575c61cb8bd44ddcf957647484a87233377fed45e17549f40e6b98bd5d",
          "issue": "issue_502acaa90c051ee20692"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ecf98353a8986a7e0e5bbfe50c3943f7229847431a220b9b6e8bdf032979a9bf",
          "issue": "issue_502acaa90c051ee20692"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "72a351729f8aad7a361cf4fc0f17734d2c334a30e2591ea41eddacf63b78fd45",
          "issue": "issue_a9f3737318f8be85f42f"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "5d83759d7f70ff7d7966924f36335c1f3199e89c7f244fbda7420165c13bec1d",
          "issue": "issue_a9f3737318f8be85f42f"
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
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "0ecbc9ed262d24418f1ccd84d115e23a1a54c1bdaaacbb5f3ed953fd4463d502"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "bba0f5a014e3a100c5853280420587964aedcc57cf53e14e15eb91bb4d50fcff",
          "issue": "issue_924c88bd5124032d6877"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "e164b2da29bb004afc38b6b9dc7c1a2ed479465a62cf4a9470ac5d5036df1980",
          "issue": "issue_924c88bd5124032d6877"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [
      {
        "label": "original_path_commit",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 10,
      "unknown_assessment_vocabulary": 5,
      "category_ambiguous_or_outside_supported_task": 3,
      "unrelated_or_secondary_graph_pairs_deferred": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 28,
      "external_dependency": 15,
      "source_check_excluded": 2
    }
  }
}
```

## RQ1_0c666ce785e8

证据目录 run/members/RQ1_0c666ce785e8/attempt_1/，报告哈希 915f4fc3cc69781d5701d5b71ad0feb36f49068a09934184696c04f9a238e055

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "alarm",
    "FCR-MINT": "unsupported",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "unsupported",
    "FCR-FREEZE": "unsupported"
  },
  "changes": [
    "last1164 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unknown_assessment_vocabulary,no_locatable_source,unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": true,
    "paired_id": "RQ1_3455b6a9ba4f",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "af6ba0fceca2f5543a6242d9088be3ccb94971c0cf7c6a58c2a40d01927e7f93",
          "issue": "issue_d62756471f1395ed0ba6"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "385b337e7a80d267c8a2eed64137283e3aed656e6d000e4148f8337cdb882483",
          "issue": "issue_900039121939209255c0"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "6ff271be0be9c17da6c248799ceaafda93f5885ed2bde05d442b3deff58058e5",
          "issue": "issue_64fc6ca41f58e812bd0d"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "91863a86197bc5fbed46f8e8766fcdec72421cb91b7baab4e05a846a5c24061b",
          "issue": "issue_97143034d22173aa61d9"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "7d3b1cab6c177f9946544655853ebc11529f5b2b705d9773489b378128ee14b1",
          "issue": "issue_97143034d22173aa61d9"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_2ff08af300ca27b89321",
        "fact": "fact_338acb30a8bb6ff7ea0e",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_647ffcc9009948bf5f08",
        "fact": "fact_240377b0832362343cc2",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_b5ed959ad4ffed72dea6",
        "fact": "fact_9829d5f60a8f899a6893",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_cc52e7e1e033d68c364c",
        "fact": "fact_c391951f0a6366f9e9f3",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_f4fc61f39960ecee7f3a",
        "fact": "fact_257cd60f34d886872195",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_f745f2ddcc88b2704899",
        "fact": "fact_98b2c0205f2c52eee3d1",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_240377b0832362343cc2",
        "object_or_effect": "o_afe29c81daae5afc0a76",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_257cd60f34d886872195",
        "object_or_effect": "o_54ad95ced9b66a4ebf48",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_338acb30a8bb6ff7ea0e",
        "object_or_effect": "o_7d210bb2d5d78236d319",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_45db1f83f81d667c3ea8",
        "object_or_effect": "w_6e8a5bfa83b05b834872",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6e8a5bfa83b05b834872",
        "grounded": true
      },
      {
        "id": "fact_4c6393ad1f24c08d2899",
        "object_or_effect": "w_5a1b84e5fd6a6a67acb6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_5a1b84e5fd6a6a67acb6",
        "grounded": true
      },
      {
        "id": "fact_9829d5f60a8f899a6893",
        "object_or_effect": "o_d0905fb600641ba8fdd5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_98b2c0205f2c52eee3d1",
        "object_or_effect": "o_9613a006b877ebcf5b9a",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_c391951f0a6366f9e9f3",
        "object_or_effect": "o_1c00526a2ab577a26d47",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "original_path_commit",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "direct_effect",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "direct_effect",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 3,
      "unknown_assessment_vocabulary": 4,
      "category_ambiguous_or_outside_supported_task": 1,
      "no_locatable_source": 4,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 34,
      "program_support": 1,
      "external_dependency": 10
    }
  }
}
```

## RQ1_0e202076b336

证据目录 run/members/RQ1_0e202076b336/attempt_1/，报告哈希 a3f3b660417ee3e4a4937265341d7283754209f9afe64a3e9fcc3716108ff1c9

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": false,
    "paired_id": "RQ1_4feeb0c21e60",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "7ceb6b1d5596ee086dffc7924682477887f4f70aafd99d0a8ba944f40dce26e5",
          "issue": "issue_754ffcda68383ee9ec80"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d2015e8847e7cd38a7b9fa4b91e0cbb47b4829334c2038ab31e707bec2fe2e19",
          "issue": "issue_a5180c968effba48ac7a"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_4ec89f15f916aa6cbf68",
        "fact": "fact_bb4048432cc39b50f664",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_95edf268b3249b254833",
        "fact": "fact_475c7303a5be9aaf8c00",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_475c7303a5be9aaf8c00",
        "object_or_effect": "o_fb3edcf2dab4707eb8e7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_62252fe8efea7273f3ba",
        "object_or_effect": "w_923e5d9d11f258db8a18",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_923e5d9d11f258db8a18",
        "grounded": true
      },
      {
        "id": "fact_99772d85a9d30ecc869a",
        "object_or_effect": "w_0c928823161a93a6fd49",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0c928823161a93a6fd49",
        "grounded": true
      },
      {
        "id": "fact_bb4048432cc39b50f664",
        "object_or_effect": "o_a66f7cb725e8dc19c10b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "original_path_commit",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 3
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
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 2
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 1,
      "invalid_semantic_row": 2,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 48,
      "external_dependency": 11,
      "source_check_excluded": 1
    }
  }
}
```

## RQ1_0f3c3f400f6f

证据目录 run/members/RQ1_0f3c3f400f6f/attempt_1/，报告哈希 7689fcc015b4fc810e1c583d1d4d98e015ffad4a149f27eb275d957a024692dc

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
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
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,invalid_semantic_row,semantic_answer_outside_sent_scope,category_ambiguous_or_outside_supported_task",
    "未决类别 FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": false,
    "paired_id": "RQ1_5b3c7cbe3d9d",
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
          "detail_sha256": "dc5ed3bbdbfaa8fd0f457006374f6b0625142619263d17f422f280cec6f0cbb5",
          "issue": "issue_11a8778b421d65edbb0e"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "e33cbb9140236e7d6a736aad853f4f0d0d18ef3293313b1accd2a1df3f87748b",
          "issue": "issue_11a8778b421d65edbb0e"
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
  "mechanism": {
    "supports": [
      {
        "support": "support_294e8d1f5c1b5a9ec374",
        "fact": "fact_9343373260c398d53cf0",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_efd7eb0f16b70f095a4f",
        "fact": "fact_0e42380a7f9e0431eff6",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_0e42380a7f9e0431eff6",
        "object_or_effect": "o_28b16a308727536f2d99",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_9343373260c398d53cf0",
        "object_or_effect": "o_6166c82c5104cb75b8e0",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_9bc9d2baf1c4cf550c29",
        "object_or_effect": "w_29b3b4bf4c447398a976",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_29b3b4bf4c447398a976",
        "grounded": true
      },
      {
        "id": "fact_a006a99f85966fc2c895",
        "object_or_effect": "w_d6c6171ae8b1205a5bac",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d6c6171ae8b1205a5bac",
        "grounded": true
      },
      {
        "id": "fact_b29a7189e1c97229a0ad",
        "object_or_effect": "w_505406e3daa0059eb02e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_505406e3daa0059eb02e",
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
        "count": 5
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 5
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 3,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 4
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-DESTROY",
      "FCR-FREEZE",
      "FCR-MINT",
      "FCR-PAUSE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 284,
      "source_task_reading": 20,
      "scope_missing": 1
    }
  }
}
```
