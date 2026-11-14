# 逐例审阅

## RQ1_d695cf0bad2e

证据目录 run/members/RQ1_d695cf0bad2e/attempt_1/，报告哈希 a8be5319d0466ca2ce9e67fef43fdfab1548d2a361f8e01ff97c17bbb240ef97

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
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": false,
    "paired_id": "RQ1_cea156e41c29",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "75c900eda095b1c40214492fd7e9677f862db3679580ff566010ad2103cd9004",
          "issue": "issue_39fae2a73f10935e6206"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_02fbbd06a38c32183e23",
        "fact": "fact_e293e3a40049b7acca09",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_245c67f1c81d93189596",
        "fact": "fact_bcbe50902d5c761d3c77",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_e9aafada77e4557f28fe",
        "fact": "fact_6bf43e748c43be7c52ca",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_6bf43e748c43be7c52ca",
        "object_or_effect": "o_71dd50f2ed72fcc31fa7",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_bcbe50902d5c761d3c77",
        "object_or_effect": "o_d540ea3fc0cd9476373f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_e293e3a40049b7acca09",
        "object_or_effect": "o_e01843be1f057ce0c81e",
        "meaning": "nonfinancial_counter",
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
        "count": 1
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 2,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 3
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
      "no_effect_in_scope": 43,
      "source_check_excluded": 2
    }
  }
}
```

## RQ1_da88771c652e

证据目录 run/members/RQ1_da88771c652e/attempt_1/，报告哈希 d57e6ed8ab113cb2154cb375f20c31a3585f10336d66594ed91cef08659089d0

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:139:original:2",
    "prev200 丢失根因 D2:139:original:2",
    "decision_only 丢失根因 D2:139:original:2"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,invalid_semantic_row,unknown_assessment_vocabulary",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_da88771c652e",
        "reference": "D2:139:original:1",
        "function": "fallback / delegatedFwd",
        "v32": "FN",
        "last1164": "FN",
        "b5": "FN",
        "ACTaint_DeepSeek": "FN",
        "prev200": "FN",
        "decision_only": "FN",
        "prev200_findings": [],
        "decision_only_findings": [],
        "current": "FN"
      },
      {
        "member": "RQ1_da88771c652e",
        "reference": "D2:139:original:2",
        "function": "upgrade",
        "v32": "TP",
        "last1164": "FN",
        "b5": "FN",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_dd7fb2b9f575ec87fe9e"
        ],
        "decision_only_findings": [
          "finding_da280ca74a78522bd300",
          "finding_f1e39ae4838d7e3aa649"
        ],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:139:original:2"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": []
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:139:original:2"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:139:original:2"
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1dd4267f951609687107193357719b095f636d6b1217709e58422eb00d9dbed9",
          "issue": "issue_d3e405ba3564a5a603d3"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "66f765d97bc133f309c4ad549bc7b9d944cfc5b31ad63e5758e82c5d93579817",
          "issue": "issue_02c403f3f2833de4ba35"
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
      "unbound_or_inapplicable_seed": 2,
      "invalid_semantic_row": 2,
      "unknown_assessment_vocabulary": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 2,
      "external_dependency": 4
    }
  }
}
```

## RQ1_dadf1b436e9d

证据目录 run/members/RQ1_dadf1b436e9d/attempt_1/，报告哈希 78494d66d4418812189caac7982dac4695baafe4c7dbcd26d5b8c5cabd85c109

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_dadf1b436e9d",
        "reference": "D2:484:S1",
        "function": "selfdestructs",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_83aa57b9980248df37e9"
        ],
        "decision_only_findings": [
          "finding_5c2061c0d3da5a11a865"
        ],
        "current": "TP"
      }
    ],
    "findings": [
      {
        "idx": 24,
        "member": "RQ1_dadf1b436e9d",
        "finding": "finding_d2ff3747e3893a64ab4e",
        "function": "fallback()",
        "location": {
          "file": "units/program.sol",
          "start": 5202,
          "length": 135,
          "ast_id": 636
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_dadf1b436e9d', 'units/program.sol', 5202)",
        "source_excerpt": "function () payable public {\n    \t\tuint amount = msg.value * buyPrice;               \n    \t\t_transfer(owner, msg.sender, amount);\n    }",
        "source_sha256": "946be02ddab6982899fcc12d927dbdcc5de6ce797862fc2e9c82c68dd9dd8e5d",
        "note": "实际报警入口或影响与作者参考不同，不能抵销该独立根因漏检。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 5202. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 5202,
              "length": 135,
              "ast_id": 636
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
          "E4"
        ]
      },
      {
        "idx": 25,
        "member": "RQ1_dadf1b436e9d",
        "finding": "finding_6d606fafc7803e11a87b",
        "function": "selfdestructs()",
        "location": {
          "file": "units/program.sol",
          "start": 5342,
          "length": 74,
          "ast_id": 644
        },
        "result": "TP",
        "reference": "D2:484:S1",
        "group": "D2:484:S1",
        "source_excerpt": "function selfdestructs() payable public {\n    \t\tselfdestruct(owner);\n    }",
        "source_sha256": "946be02ddab6982899fcc12d927dbdcc5de6ce797862fc2e9c82c68dd9dd8e5d",
        "note": "实际入口及源码效果与作者独立根因对应，保留程序证据可审计性限制。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 5342. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 5342,
              "length": 74,
              "ast_id": 644
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "7aa1d5655650a34e9b5fc7b5071b6399111d5d19b1c0062c88e44a34b01bb19e",
          "issue": "issue_af218738b347532b6854"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d92b6eb9505a0aa8a3ad61c12dd753c5b9f6be7f0f44b80613bec4092dca7f0b",
          "issue": "issue_649b2f39c32932380139"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "af0b3e98cc22b4e68525fc6e41876a1e1aafb5c7f2e80d39bf5d591c89f24863",
          "issue": "issue_ccf0ef4199fb6e66a77a"
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
        "support": "support_b41ad7a59c2916ff36d9",
        "fact": "fact_bb34f489ad9e6bfaed15",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_bb34f489ad9e6bfaed15",
        "object_or_effect": "o_f0fefc0dc7d73703dbf5",
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
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 3,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "source_task_reading": 18,
      "no_effect_in_scope": 17,
      "program_support": 2,
      "external_dependency": 3
    }
  }
}
```

## RQ1_db11e3e08742

证据目录 run/members/RQ1_db11e3e08742/attempt_1/，报告哈希 267185c97bc7749edc999e8f7215ab1285dfd577d1159beaf10049f531296bfc

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "not_detected",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "alarm",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "v32 退为未知，不能当作纠正",
    "prev200 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,semantic_answer_outside_sent_scope,unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task",
    "未决类别 FCR-DESTROY,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": false,
    "paired_id": "RQ1_353a9b0b5006",
    "state": "unsupported",
    "changes": {
      "v32": {
        "before": "alarm",
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
      "normalization_diagnostics": [
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "246c15ecea240cd740e6dcd9a45e0a7c1fb3efafbbada1bd5770c0a102fb85a4",
          "issue": "issue_3904f8f13a17bb91390f"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "2418ea795a5517f140a9a72e74d6c829e60e9c544797d53a3c49d7e9ee2898ef",
          "issue": "issue_3904f8f13a17bb91390f"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "3ac9aa218acfdf3b4673c83eb3e7476e5a1b6c6a35f84a2ea42aa0a20198dc6d",
          "issue": "issue_e17450cba6ca0e4229cb"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "841996e3ca7986eba268c477e77af2a2222f7f2dea4e24fb446ec5babad30efb",
          "issue": "issue_e17450cba6ca0e4229cb"
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
          "detail_sha256": "02a534b609b02460d4581e08339f3da1dadfa5c1a9c7d715434ae0b8ebd9dae9",
          "issue": "issue_976c1072f3e234e6a1f1"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "b1cd43fb902c720e1193e03f92a4c5f041a068903b13aa7bf612c7af1fef0e4a",
          "issue": "issue_976c1072f3e234e6a1f1"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_295159bb2c3a4f383355",
        "fact": "fact_1f4521faeeee30a739f9",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_299c2c0e4dcbff1fa484",
        "fact": "fact_1f77f8a95274bbce6795",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_8da54c2be2982eecb85f",
        "fact": "fact_ca6508fb59572661cea7",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_91ed8773181ce169b139",
        "fact": "fact_ca6508fb59572661cea7",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_d10a9082ad10067efa62",
        "fact": "fact_3635341e3e1a8a4da6e8",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_eed0a967f1bd4fd686b2",
        "fact": "fact_9431f46c16d3965f03b3",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_f2ea542ac00451a1d5fe",
        "fact": "fact_821642de4ca9418eb953",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_041112de13ca845086bd",
        "object_or_effect": "w_d10bb63c3e35fc4c2491",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d10bb63c3e35fc4c2491",
        "grounded": true
      },
      {
        "id": "fact_071f4962666fe494e1cc",
        "object_or_effect": "w_48a7b04236a61ec85ecc",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_48a7b04236a61ec85ecc",
        "grounded": true
      },
      {
        "id": "fact_18e69d07bf6a2776fe78",
        "object_or_effect": "w_b4a11817a1d84e21fa94",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_b4a11817a1d84e21fa94",
        "grounded": true
      },
      {
        "id": "fact_1f4521faeeee30a739f9",
        "object_or_effect": "o_4ff559dc5f534bc95b5f",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_1f77f8a95274bbce6795",
        "object_or_effect": "o_13b0b03d5988e47ccd23",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_25ebc2a436c4cd793cfe",
        "object_or_effect": "w_5da1fd69d9ab19a3017d",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_5da1fd69d9ab19a3017d",
        "grounded": true
      },
      {
        "id": "fact_3127b0a601938b3d26dd",
        "object_or_effect": "w_a27bde0cb7c06eac1471",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_a27bde0cb7c06eac1471",
        "grounded": true
      },
      {
        "id": "fact_318a06be96b7a4a0f723",
        "object_or_effect": "w_27ad13b82ee5fdae5015",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_27ad13b82ee5fdae5015",
        "grounded": true
      },
      {
        "id": "fact_322410c0b5d041b2a94c",
        "object_or_effect": "w_8f26451f23699bc7b5e3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8f26451f23699bc7b5e3",
        "grounded": true
      },
      {
        "id": "fact_341809c1369579e80251",
        "object_or_effect": "w_b3f26948c98f5435bce6",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_b3f26948c98f5435bce6",
        "grounded": true
      },
      {
        "id": "fact_3635341e3e1a8a4da6e8",
        "object_or_effect": "o_8918291da3767aeefb60",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_3f89034a53d452a1e13d",
        "object_or_effect": "w_864e76c88b429d006bab",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_864e76c88b429d006bab",
        "grounded": true
      },
      {
        "id": "fact_432af9c31abda7a1fd2c",
        "object_or_effect": "w_e9cae1db45b4630c76ad",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_e9cae1db45b4630c76ad",
        "grounded": true
      },
      {
        "id": "fact_47ab45ebb55dfeed50ee",
        "object_or_effect": "w_bf374db51dc35da8d84e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_bf374db51dc35da8d84e",
        "grounded": true
      },
      {
        "id": "fact_5687bc25fc3a2af7f21d",
        "object_or_effect": "w_ef2a1505b6ab71e74869",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_ef2a1505b6ab71e74869",
        "grounded": true
      },
      {
        "id": "fact_5a677ab493869a9f129c",
        "object_or_effect": "w_62ea900c53961236d0f7",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_62ea900c53961236d0f7",
        "grounded": true
      },
      {
        "id": "fact_5e06a39af78f9872ca0c",
        "object_or_effect": "w_b383716db264765936a8",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b383716db264765936a8",
        "grounded": true
      },
      {
        "id": "fact_5ec6b14620ad1f577ef7",
        "object_or_effect": "w_1a4db32091cb561de0a7",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_1a4db32091cb561de0a7",
        "grounded": true
      },
      {
        "id": "fact_61341864916ab0d866d6",
        "object_or_effect": "w_c75a76c65528e31478a1",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c75a76c65528e31478a1",
        "grounded": true
      },
      {
        "id": "fact_689fd52fd4109792b8de",
        "object_or_effect": "w_74ca0ac56ddbbd1eff9d",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_74ca0ac56ddbbd1eff9d",
        "grounded": true
      },
      {
        "id": "fact_7e32a782d8efead22be6",
        "object_or_effect": "w_05f251fafe5e990b4b1c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_05f251fafe5e990b4b1c",
        "grounded": true
      },
      {
        "id": "fact_821642de4ca9418eb953",
        "object_or_effect": "o_25a23e23ae7f8ba95ccb",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_9431f46c16d3965f03b3",
        "object_or_effect": "o_153d4bd9eb9b57a2cc46",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_9e067ef8973a0f6bafac",
        "object_or_effect": "w_9df2b7629a3763a8cee6",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_9df2b7629a3763a8cee6",
        "grounded": true
      },
      {
        "id": "fact_a1efa74219beada35b79",
        "object_or_effect": "w_fc1a0ff6c350f0e62ced",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_fc1a0ff6c350f0e62ced",
        "grounded": true
      },
      {
        "id": "fact_b4e85af014776b6da890",
        "object_or_effect": "w_23d1d7d8d87c824fe2e2",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_23d1d7d8d87c824fe2e2",
        "grounded": true
      },
      {
        "id": "fact_c1ef8875fbec10f75e61",
        "object_or_effect": "w_08557df6b74aa3bf05cc",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_08557df6b74aa3bf05cc",
        "grounded": true
      },
      {
        "id": "fact_ca6508fb59572661cea7",
        "object_or_effect": "o_7665cd22d5f6eaec7bce",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_de8b49657d4df40740d4",
        "object_or_effect": "w_aa8e00d9f561b0f86b22",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_aa8e00d9f561b0f86b22",
        "grounded": true
      },
      {
        "id": "fact_e6e9bc2b233cba55da78",
        "object_or_effect": "w_56da90dc095f4b7f35a8",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_56da90dc095f4b7f35a8",
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 26
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 23
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 19
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
      },
      {
        "label": "same_request_amount_change",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "prefix_reachability",
        "answer": "unsat",
        "count": 30
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 6
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 12
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "financial_consent_unresolved",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "financial_consent_unresolved",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "control_transition_preservation",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 3,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 5,
      "unrelated_or_secondary_graph_pairs_deferred": 10,
      "action_slice_exhausted": 2,
      "yield_to_source_bound_semantic_review": 1,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "revision_outside_actual_feedback_scope": 1,
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
      "no_effect_in_scope": 125,
      "scope_missing": 8,
      "source_task_reading": 16,
      "program_support": 1
    }
  }
}
```

## RQ1_db73c28a69c2

证据目录 run/members/RQ1_db73c28a69c2/attempt_1/，报告哈希 d9b5bca3f0635c5176b71638c1d5219e421b6480aa3da23418459e1fd91dd1f9

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
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": false,
    "paired_id": "RQ1_1844e5d3d18e",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "959b824b9c77a5346bc5e0bd3b1dc935ebe7d72cf42bfde75226a5cdf3fcb38d",
          "issue": "issue_4e2bd742cf688e646501"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b5cbb3007436962a4e5b4dbef9cd89e476f4e8adb8efe8226d63903daec7dad6",
          "issue": "issue_4e2bd742cf688e646501"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "9ac9de52d866f4b8935a13f4d6981add008d4c0ecd3afd31d58e8c2e8f09c7ce",
          "issue": "issue_211b69dbe38c39d750bb"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "0163c289ca2a29d07d70322243b1c8f3dea116be8d1cc3f26b0ac186e114d8ed",
          "issue": "issue_211b69dbe38c39d750bb"
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
          "detail_sha256": "a3d957534703fdb506caf2abf588a2df0827cf0943994c96b7a24ee7eaba9458",
          "issue": "issue_9828991b4f5fa4654ba3"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d02d79fb9442078a7e255241d7711d265d61be8c97cf1629677945e90584b518",
          "issue": "issue_9828991b4f5fa4654ba3"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_2e880006b8c94930ce5a",
        "fact": "fact_ce392fb8fe1c2f03bb51",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_44eab38c7810e76f8cd4",
        "fact": "fact_799d16e67e6833f03741",
        "origin": "verified_service",
        "field": "policies",
        "version": 1
      },
      {
        "support": "support_51c378cb587acd34c1eb",
        "fact": "fact_c9344e7aa9883a45ac7e",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_e6d3a22950fa6a8bfa5c",
        "fact": "fact_a48dc31533ddcf165503",
        "origin": "verified_service",
        "field": "policies",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_799d16e67e6833f03741",
        "object_or_effect": "w_ab00bd875e9e11d66461",
        "meaning": "initialization_stage",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_a48dc31533ddcf165503",
        "object_or_effect": "w_ab00bd875e9e11d66461",
        "meaning": "current_authority_required",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_c9344e7aa9883a45ac7e",
        "object_or_effect": "o_934f81693ceaf1ca1497",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_ce392fb8fe1c2f03bb51",
        "object_or_effect": "o_a8aa727ecf8e7d0e79d7",
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
      "invalid_semantic_row": 5,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 2,
      "no_locatable_source": 1,
      "unbound_or_inapplicable_seed": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 85,
      "external_dependency": 20
    }
  }
}
```

## RQ1_dc06d7bad0d8

证据目录 run/members/RQ1_dc06d7bad0d8/attempt_1/，报告哈希 9f1dd70a920d4b511473b4524be2b9cbb52c8098103dba7fb5fb51705be35366

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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unrelated_or_secondary_graph_pairs_deferred,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": false,
    "paired_id": "RQ1_9c365cb18f95",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "82386450a883c374e1ca6e98070b80d094f58b7b6844995a39fe1cd6fd795e2d",
          "issue": "issue_b3cc0894c809d1a50a82"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f8f7fc0dd53f8fca8e11b90e5ca85628a55725e34b23de29b52e72af328f8a49",
          "issue": "issue_b3cc0894c809d1a50a82"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "58a92268e5994b6fe6c5ec97619db337cd53eb73d30892851a9f718387c96e3c",
          "issue": "issue_bcb7bad43f73e99a5b30"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "863c5ca11b26357ef8d6c5d52cf3da5aa2a790c063395c942327355678bb29ed",
          "issue": "issue_bcb7bad43f73e99a5b30"
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
          "detail_sha256": "813352cf5ede1201f84c8cf343d99cb5cedd0073e41f10a5a3ee9748d3afffef",
          "issue": "issue_b3cc0894c809d1a50a82"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_047d81a88bb0477c5ee7",
        "fact": "fact_1b6d4164b4bfe2931c86",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_3a23e5c151867a18316d",
        "fact": "fact_0afd90dadc8aac79004d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_489e8857e3ff14cb95df",
        "fact": "fact_1142d07f8052a0273dd4",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_49d279581e25b73cc623",
        "fact": "fact_3fe2e542588d333a3574",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_680be54105c783cfafad",
        "fact": "fact_6f484e813251166bcf4a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_7c299a49355e27d83cc4",
        "fact": "fact_1b6d4164b4bfe2931c86",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_84f50764efce70c31ce8",
        "fact": "fact_0afd90dadc8aac79004d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_ce45d743ab2dca0d1141",
        "fact": "fact_f61afbd447555507d10e",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_ef14d3f46a9cf22ca441",
        "fact": "fact_1142d07f8052a0273dd4",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_030fe29acfb6404683b6",
        "object_or_effect": "w_06d20771d686646f0b06",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_06d20771d686646f0b06",
        "grounded": true
      },
      {
        "id": "fact_033b79ed665df1ecebd9",
        "object_or_effect": "w_2b7de8030f7ef853c35d",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_2b7de8030f7ef853c35d",
        "grounded": true
      },
      {
        "id": "fact_04772f6f09d9933704cf",
        "object_or_effect": "w_ed92ee8294b80afd0576",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ed92ee8294b80afd0576",
        "grounded": true
      },
      {
        "id": "fact_04dad1b1caf204b81685",
        "object_or_effect": "w_2cdebf2f92450e4ed58b",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_2cdebf2f92450e4ed58b",
        "grounded": true
      },
      {
        "id": "fact_064c020f16dbe3634e7d",
        "object_or_effect": "w_e07bd267dd79db7bc95c",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_e07bd267dd79db7bc95c",
        "grounded": true
      },
      {
        "id": "fact_0afd90dadc8aac79004d",
        "object_or_effect": "o_9e65d62823d80e118b3e",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_0b4b4abcc6fef8dae30d",
        "object_or_effect": "w_abb812f6745476dc98f9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_abb812f6745476dc98f9",
        "grounded": true
      },
      {
        "id": "fact_0d6664534cefc55634bc",
        "object_or_effect": "w_e20deb95760f1a32fbfe",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_e20deb95760f1a32fbfe",
        "grounded": true
      },
      {
        "id": "fact_0d949b6f736f1fceba6f",
        "object_or_effect": "w_40885578c510734cc26b",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_40885578c510734cc26b",
        "grounded": true
      },
      {
        "id": "fact_0dc7df4ce87d41d68663",
        "object_or_effect": "w_cce8fc487aeccf579906",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_cce8fc487aeccf579906",
        "grounded": true
      },
      {
        "id": "fact_0f44dc291ccfcafce269",
        "object_or_effect": "w_3e881308d4548eb203a3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3e881308d4548eb203a3",
        "grounded": true
      },
      {
        "id": "fact_0f960adc04d603814ce0",
        "object_or_effect": "w_24b3e9953f822c65da33",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_24b3e9953f822c65da33",
        "grounded": true
      },
      {
        "id": "fact_1142d07f8052a0273dd4",
        "object_or_effect": "o_94092d4ac28777573c91",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_1254e3ed1f1e9453d52d",
        "object_or_effect": "w_b78ae722fdbc5121ed91",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_b78ae722fdbc5121ed91",
        "grounded": true
      },
      {
        "id": "fact_12f4134ae43a011c4545",
        "object_or_effect": "w_64392feb5d35d5690c9a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_64392feb5d35d5690c9a",
        "grounded": true
      },
      {
        "id": "fact_14c9a1c4f7288b2a49a7",
        "object_or_effect": "w_df2866643646d3aa368b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_df2866643646d3aa368b",
        "grounded": true
      },
      {
        "id": "fact_158950b83e196afd4995",
        "object_or_effect": "w_12ff2a7dda891e0e9085",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_12ff2a7dda891e0e9085",
        "grounded": true
      },
      {
        "id": "fact_1625a36e80314d119fdd",
        "object_or_effect": "w_6115fca3bd15a8476ad5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6115fca3bd15a8476ad5",
        "grounded": true
      },
      {
        "id": "fact_166da226cdb05c18f989",
        "object_or_effect": "w_64380128275b46bbb988",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_64380128275b46bbb988",
        "grounded": true
      },
      {
        "id": "fact_183ddd2869db403ee47e",
        "object_or_effect": "w_d8cf7a55d20154849817",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d8cf7a55d20154849817",
        "grounded": true
      },
      {
        "id": "fact_1aeae19e94818f678a78",
        "object_or_effect": "w_f958692dc6b6a74fa00f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f958692dc6b6a74fa00f",
        "grounded": true
      },
      {
        "id": "fact_1b6d4164b4bfe2931c86",
        "object_or_effect": "o_33d8b88cd829f5343f48",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_1c82e13bd8d6e986e2d1",
        "object_or_effect": "w_88c82d6981ae6a690795",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_88c82d6981ae6a690795",
        "grounded": true
      },
      {
        "id": "fact_1cc0cfccc3a45a1c9611",
        "object_or_effect": "w_cf95146d9a378bab4363",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cf95146d9a378bab4363",
        "grounded": true
      },
      {
        "id": "fact_1d6eda1b8ca61554aa43",
        "object_or_effect": "w_3b271be70f7420ce76f1",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_3b271be70f7420ce76f1",
        "grounded": true
      },
      {
        "id": "fact_1e07371866bc9e84ebc5",
        "object_or_effect": "w_ed92ee8294b80afd0576",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_ed92ee8294b80afd0576",
        "grounded": true
      },
      {
        "id": "fact_1e25c0bc338a493e911c",
        "object_or_effect": "w_5c38670ceeb24f74f2ae",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5c38670ceeb24f74f2ae",
        "grounded": true
      },
      {
        "id": "fact_1e58c3eec434675d978f",
        "object_or_effect": "w_0dde9217bb3a7141057a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0dde9217bb3a7141057a",
        "grounded": true
      },
      {
        "id": "fact_1e7aa6f9402765e92b4d",
        "object_or_effect": "w_3e881308d4548eb203a3",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_3e881308d4548eb203a3",
        "grounded": true
      },
      {
        "id": "fact_1eced0af0ddd61244298",
        "object_or_effect": "w_787cb179a735ddceffc5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_787cb179a735ddceffc5",
        "grounded": true
      },
      {
        "id": "fact_20a5b3f63e7ec0686910",
        "object_or_effect": "w_e30387bf581d3d93b959",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e30387bf581d3d93b959",
        "grounded": true
      },
      {
        "id": "fact_217ca7f7f53f5e21f3c0",
        "object_or_effect": "w_cce8fc487aeccf579906",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cce8fc487aeccf579906",
        "grounded": true
      },
      {
        "id": "fact_24955ef0f0edcea80781",
        "object_or_effect": "w_81d2d2fce417c58aa8b2",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_81d2d2fce417c58aa8b2",
        "grounded": true
      },
      {
        "id": "fact_25452d2e020662b83c04",
        "object_or_effect": "w_354c61d03563ece77e6a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_354c61d03563ece77e6a",
        "grounded": true
      },
      {
        "id": "fact_2755952e4278dbc7f1fe",
        "object_or_effect": "w_725a1492cd80906affc8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_725a1492cd80906affc8",
        "grounded": true
      },
      {
        "id": "fact_2aa607d57a38c23fa1a8",
        "object_or_effect": "w_aa02fe7f7abb2cb6a215",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_aa02fe7f7abb2cb6a215",
        "grounded": true
      },
      {
        "id": "fact_2b912e259c505f16dc1e",
        "object_or_effect": "w_5405b44373d9cd8e983f",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_5405b44373d9cd8e983f",
        "grounded": true
      },
      {
        "id": "fact_2d1bfbef011bb0531fc4",
        "object_or_effect": "w_a6e4c301b720d54bebdc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a6e4c301b720d54bebdc",
        "grounded": true
      },
      {
        "id": "fact_2e2b0aa771f643d24c83",
        "object_or_effect": "w_43a920d924062346a4f9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_43a920d924062346a4f9",
        "grounded": true
      },
      {
        "id": "fact_30e08ae7b86c3a3e71b0",
        "object_or_effect": "w_6e34512c719936accb8b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6e34512c719936accb8b",
        "grounded": true
      },
      {
        "id": "fact_3201802b59c796f35f5d",
        "object_or_effect": "w_ef3c341057b5db3c5fa7",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_ef3c341057b5db3c5fa7",
        "grounded": true
      },
      {
        "id": "fact_33790eb40be25eeecf7f",
        "object_or_effect": "w_a728c5bb62b954e99804",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a728c5bb62b954e99804",
        "grounded": true
      },
      {
        "id": "fact_34eaa644df3d3d5eb530",
        "object_or_effect": "w_cb1676289ee219b0cb18",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_cb1676289ee219b0cb18",
        "grounded": true
      },
      {
        "id": "fact_35fa72b6ba3604ad3b20",
        "object_or_effect": "w_c8ffd0223921843ae8bb",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c8ffd0223921843ae8bb",
        "grounded": true
      },
      {
        "id": "fact_366485ae201afde7306a",
        "object_or_effect": "w_dc50a5d58ec1198ad788",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_dc50a5d58ec1198ad788",
        "grounded": true
      },
      {
        "id": "fact_37212596dac5b8c4b2ec",
        "object_or_effect": "w_81d2d2fce417c58aa8b2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_81d2d2fce417c58aa8b2",
        "grounded": true
      },
      {
        "id": "fact_3a3d5924035ff06013e9",
        "object_or_effect": "w_1cf2cc7781b2e96f361b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1cf2cc7781b2e96f361b",
        "grounded": true
      },
      {
        "id": "fact_3b2c434fb47a9f2a5ff4",
        "object_or_effect": "w_8d4f972c0f18dd40931a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8d4f972c0f18dd40931a",
        "grounded": true
      },
      {
        "id": "fact_3b5dc887df81aa2d3fe7",
        "object_or_effect": "w_70a37a49d6eea8672a02",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_70a37a49d6eea8672a02",
        "grounded": true
      },
      {
        "id": "fact_3fe2e542588d333a3574",
        "object_or_effect": "o_de132558625ac6a4469b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_403d3085606ba0f749cc",
        "object_or_effect": "w_45806f1f431df5108f2c",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_45806f1f431df5108f2c",
        "grounded": true
      },
      {
        "id": "fact_42214c7430a563a15f2e",
        "object_or_effect": "w_e2efd534267eef9dd14c",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_e2efd534267eef9dd14c",
        "grounded": true
      },
      {
        "id": "fact_44130dd5f0752e220ba2",
        "object_or_effect": "w_0749d4cc425f5fcfce29",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_0749d4cc425f5fcfce29",
        "grounded": true
      },
      {
        "id": "fact_461376eb24f32ab5cd8c",
        "object_or_effect": "w_c8ffd0223921843ae8bb",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c8ffd0223921843ae8bb",
        "grounded": true
      },
      {
        "id": "fact_4673dbf760565b6758ce",
        "object_or_effect": "w_6e34512c719936accb8b",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_6e34512c719936accb8b",
        "grounded": true
      },
      {
        "id": "fact_46d5d8f94ab02558010f",
        "object_or_effect": "w_3d451cfa23056fc0501c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3d451cfa23056fc0501c",
        "grounded": true
      },
      {
        "id": "fact_479013621d8cf04cd420",
        "object_or_effect": "w_45806f1f431df5108f2c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_45806f1f431df5108f2c",
        "grounded": true
      },
      {
        "id": "fact_47e7cd33ee90acfd8bda",
        "object_or_effect": "w_df2866643646d3aa368b",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_df2866643646d3aa368b",
        "grounded": true
      },
      {
        "id": "fact_48026c4e11cb28fb0705",
        "object_or_effect": "w_cb1676289ee219b0cb18",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cb1676289ee219b0cb18",
        "grounded": true
      },
      {
        "id": "fact_4a6d61b7b975ca59d5dc",
        "object_or_effect": "w_3b271be70f7420ce76f1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3b271be70f7420ce76f1",
        "grounded": true
      },
      {
        "id": "fact_4a879dd850a34341762c",
        "object_or_effect": "w_43a920d924062346a4f9",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_43a920d924062346a4f9",
        "grounded": true
      },
      {
        "id": "fact_4bb3a2a20c2b390c42fa",
        "object_or_effect": "w_a4c868dd78317c3ffad2",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_a4c868dd78317c3ffad2",
        "grounded": true
      },
      {
        "id": "fact_4d280e41d11ddb4d577d",
        "object_or_effect": "w_3d8cd4b85887c19c2a9c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3d8cd4b85887c19c2a9c",
        "grounded": true
      },
      {
        "id": "fact_4dac5258eee603374ecf",
        "object_or_effect": "w_3e6f37d4eef89f662ac3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3e6f37d4eef89f662ac3",
        "grounded": true
      },
      {
        "id": "fact_4db12046a848c87c981f",
        "object_or_effect": "w_06d20771d686646f0b06",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_06d20771d686646f0b06",
        "grounded": true
      },
      {
        "id": "fact_4f0f92ab41c1233383f3",
        "object_or_effect": "w_bf068bd805baf003140e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_bf068bd805baf003140e",
        "grounded": true
      },
      {
        "id": "fact_50e47919dc524de1582a",
        "object_or_effect": "w_a6f5d4f31a9a3d4f0617",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a6f5d4f31a9a3d4f0617",
        "grounded": true
      },
      {
        "id": "fact_51a2bc384d749503b13d",
        "object_or_effect": "w_f7d775ddd65613cecf18",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_f7d775ddd65613cecf18",
        "grounded": true
      },
      {
        "id": "fact_54013c8fa560bc0d25bb",
        "object_or_effect": "w_e30387bf581d3d93b959",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_e30387bf581d3d93b959",
        "grounded": true
      },
      {
        "id": "fact_60b2d1a14c880de481b1",
        "object_or_effect": "w_db4492aed9eb20cf46ca",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_db4492aed9eb20cf46ca",
        "grounded": true
      },
      {
        "id": "fact_65fe942c1b69d521dd36",
        "object_or_effect": "w_06e96608924a95beddcc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_06e96608924a95beddcc",
        "grounded": true
      },
      {
        "id": "fact_66b31ca80362663719e3",
        "object_or_effect": "w_2b7de8030f7ef853c35d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2b7de8030f7ef853c35d",
        "grounded": true
      },
      {
        "id": "fact_682f61144ed79b5cba6a",
        "object_or_effect": "w_10b5756f22d899c83bda",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_10b5756f22d899c83bda",
        "grounded": true
      },
      {
        "id": "fact_68656c0b5df338bb89f3",
        "object_or_effect": "w_64c5e08cd139a4cc876e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_64c5e08cd139a4cc876e",
        "grounded": true
      },
      {
        "id": "fact_69a193071cd4a8d21e41",
        "object_or_effect": "w_48174cac8188054bb0e3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_48174cac8188054bb0e3",
        "grounded": true
      },
      {
        "id": "fact_6c4fc58316e86545265e",
        "object_or_effect": "w_70bae251cef7dc0231a2",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_70bae251cef7dc0231a2",
        "grounded": true
      },
      {
        "id": "fact_6f1d25365f2e0f7b9a6d",
        "object_or_effect": "w_07eafc1bdb973a6817a1",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_07eafc1bdb973a6817a1",
        "grounded": true
      },
      {
        "id": "fact_6f484e813251166bcf4a",
        "object_or_effect": "o_243cc7ed41a0b8064fcc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_700453cddc8c956f1dc7",
        "object_or_effect": "w_3e6f37d4eef89f662ac3",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_3e6f37d4eef89f662ac3",
        "grounded": true
      },
      {
        "id": "fact_728a1df8061b054f4f90",
        "object_or_effect": "w_10b5756f22d899c83bda",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_10b5756f22d899c83bda",
        "grounded": true
      },
      {
        "id": "fact_72c297ea3fe808b132df",
        "object_or_effect": "w_6e54ad542ff34c595930",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6e54ad542ff34c595930",
        "grounded": true
      },
      {
        "id": "fact_7340f60b5d02966e4c3b",
        "object_or_effect": "w_90148fbc7879ed7eb212",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_90148fbc7879ed7eb212",
        "grounded": true
      },
      {
        "id": "fact_7452e7460bd338b2631d",
        "object_or_effect": "w_cf95146d9a378bab4363",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_cf95146d9a378bab4363",
        "grounded": true
      },
      {
        "id": "fact_753d721bb73c98594134",
        "object_or_effect": "w_e07bd267dd79db7bc95c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e07bd267dd79db7bc95c",
        "grounded": true
      },
      {
        "id": "fact_756b7d2ef95c2ffcb97f",
        "object_or_effect": "w_a6f5d4f31a9a3d4f0617",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_a6f5d4f31a9a3d4f0617",
        "grounded": true
      },
      {
        "id": "fact_76b8ef0614126c5f36a6",
        "object_or_effect": "w_e6d439a2b78513f326b7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e6d439a2b78513f326b7",
        "grounded": true
      },
      {
        "id": "fact_77fd4841f3e7cdbe4059",
        "object_or_effect": "w_63260e9379f3031619f4",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_63260e9379f3031619f4",
        "grounded": true
      },
      {
        "id": "fact_7b3180e4e54a63deea2e",
        "object_or_effect": "w_a03663a484d1c12f54b2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a03663a484d1c12f54b2",
        "grounded": true
      },
      {
        "id": "fact_7c5718d6f33cb74bab13",
        "object_or_effect": "w_6e54ad542ff34c595930",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_6e54ad542ff34c595930",
        "grounded": true
      },
      {
        "id": "fact_7d7d665f9115295a8d65",
        "object_or_effect": "w_24b3e9953f822c65da33",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_24b3e9953f822c65da33",
        "grounded": true
      },
      {
        "id": "fact_7d94d29264bba7651f68",
        "object_or_effect": "w_5c38670ceeb24f74f2ae",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_5c38670ceeb24f74f2ae",
        "grounded": true
      },
      {
        "id": "fact_7dea873ccf2584dcb562",
        "object_or_effect": "w_abb812f6745476dc98f9",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_abb812f6745476dc98f9",
        "grounded": true
      },
      {
        "id": "fact_7eb439e401ed40ca27b1",
        "object_or_effect": "w_3efd5b777471ab5b9abf",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_3efd5b777471ab5b9abf",
        "grounded": true
      },
      {
        "id": "fact_81108fcd05a5e5b1bebb",
        "object_or_effect": "w_354c61d03563ece77e6a",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_354c61d03563ece77e6a",
        "grounded": true
      },
      {
        "id": "fact_81af957d7e238c25a242",
        "object_or_effect": "w_c8a73eabb0611ff136f2",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c8a73eabb0611ff136f2",
        "grounded": true
      },
      {
        "id": "fact_86cd8f91d3bc090888aa",
        "object_or_effect": "w_a5a4dcc88dbfe0fdd5d1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a5a4dcc88dbfe0fdd5d1",
        "grounded": true
      },
      {
        "id": "fact_86e67f9fbb14ab42ed82",
        "object_or_effect": "w_e6d439a2b78513f326b7",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_e6d439a2b78513f326b7",
        "grounded": true
      },
      {
        "id": "fact_87c3ea53d76fd350b5b3",
        "object_or_effect": "w_84741d667a974b561a4e",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_84741d667a974b561a4e",
        "grounded": true
      },
      {
        "id": "fact_87ddbebe7521807054fe",
        "object_or_effect": "w_70a37a49d6eea8672a02",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_70a37a49d6eea8672a02",
        "grounded": true
      },
      {
        "id": "fact_87e4962b026b18d9f6ae",
        "object_or_effect": "w_a4c868dd78317c3ffad2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a4c868dd78317c3ffad2",
        "grounded": true
      },
      {
        "id": "fact_88944135289525df68f3",
        "object_or_effect": "w_12ff2a7dda891e0e9085",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_12ff2a7dda891e0e9085",
        "grounded": true
      },
      {
        "id": "fact_8907e3ed1effeb17f688",
        "object_or_effect": "w_e2efd534267eef9dd14c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e2efd534267eef9dd14c",
        "grounded": true
      },
      {
        "id": "fact_8960c3def7021616bce0",
        "object_or_effect": "w_d658d6b869263e96618e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d658d6b869263e96618e",
        "grounded": true
      },
      {
        "id": "fact_8a47a71bfdcdfc813733",
        "object_or_effect": "w_c2acb1314263b0dacf0e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c2acb1314263b0dacf0e",
        "grounded": true
      },
      {
        "id": "fact_8c2592a4d23242d54dec",
        "object_or_effect": "w_4f015e7963578414317b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4f015e7963578414317b",
        "grounded": true
      },
      {
        "id": "fact_8cdee9f452db7fef8eb7",
        "object_or_effect": "w_53a85741cc77abb56c4b",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_53a85741cc77abb56c4b",
        "grounded": true
      },
      {
        "id": "fact_8db96f9e49e2e6536cbc",
        "object_or_effect": "w_27a5a8f1b64339b7781a",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_27a5a8f1b64339b7781a",
        "grounded": true
      },
      {
        "id": "fact_8ebb893dede17ee27f6a",
        "object_or_effect": "w_6337dfffbbfb46747470",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6337dfffbbfb46747470",
        "grounded": true
      },
      {
        "id": "fact_8f5baceb6bf409d47c0e",
        "object_or_effect": "w_01984b25b779f9444f47",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_01984b25b779f9444f47",
        "grounded": true
      },
      {
        "id": "fact_90d6f1a7870d98dfd4d1",
        "object_or_effect": "w_8d4f972c0f18dd40931a",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_8d4f972c0f18dd40931a",
        "grounded": true
      },
      {
        "id": "fact_91a37d2ccbfe32c4b39f",
        "object_or_effect": "w_a6b989a75be1937aaa45",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a6b989a75be1937aaa45",
        "grounded": true
      },
      {
        "id": "fact_9269d781991204e4f00c",
        "object_or_effect": "w_62abb51f508f57648ce0",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_62abb51f508f57648ce0",
        "grounded": true
      },
      {
        "id": "fact_92d32ce4928a3fd7e66b",
        "object_or_effect": "w_84741d667a974b561a4e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_84741d667a974b561a4e",
        "grounded": true
      },
      {
        "id": "fact_93053df5791b47b0a8ff",
        "object_or_effect": "w_b78ae722fdbc5121ed91",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b78ae722fdbc5121ed91",
        "grounded": true
      },
      {
        "id": "fact_94cda2da603839427318",
        "object_or_effect": "w_a03663a484d1c12f54b2",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_a03663a484d1c12f54b2",
        "grounded": true
      },
      {
        "id": "fact_963c505a6ebf644dede5",
        "object_or_effect": "w_5405b44373d9cd8e983f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5405b44373d9cd8e983f",
        "grounded": true
      },
      {
        "id": "fact_9710b8107c0341ff2999",
        "object_or_effect": "w_e20deb95760f1a32fbfe",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e20deb95760f1a32fbfe",
        "grounded": true
      },
      {
        "id": "fact_9885e27b0eeaa6c756e6",
        "object_or_effect": "w_0b900941043b7a2cff1a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0b900941043b7a2cff1a",
        "grounded": true
      },
      {
        "id": "fact_990409b2b0cfc786a2e9",
        "object_or_effect": "w_ddda453cc8e0caa36d9c",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_ddda453cc8e0caa36d9c",
        "grounded": true
      },
      {
        "id": "fact_a134b41fb50fd7d480dd",
        "object_or_effect": "w_27a5a8f1b64339b7781a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_27a5a8f1b64339b7781a",
        "grounded": true
      },
      {
        "id": "fact_a192e46c9bfbd103f846",
        "object_or_effect": "w_3d8cd4b85887c19c2a9c",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_3d8cd4b85887c19c2a9c",
        "grounded": true
      },
      {
        "id": "fact_a1ad9c3546a4ae4a0003",
        "object_or_effect": "w_54c5339ede15fcb3f663",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_54c5339ede15fcb3f663",
        "grounded": true
      },
      {
        "id": "fact_a2b1634c3c0ffb082388",
        "object_or_effect": "w_90148fbc7879ed7eb212",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_90148fbc7879ed7eb212",
        "grounded": true
      },
      {
        "id": "fact_a4451be28785f436fea5",
        "object_or_effect": "w_e1838eb1aed8cd4c1cb6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e1838eb1aed8cd4c1cb6",
        "grounded": true
      },
      {
        "id": "fact_a4eee63ea462a09ee901",
        "object_or_effect": "w_6115fca3bd15a8476ad5",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_6115fca3bd15a8476ad5",
        "grounded": true
      },
      {
        "id": "fact_a5015f94524719bd2dc2",
        "object_or_effect": "w_06e96608924a95beddcc",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_06e96608924a95beddcc",
        "grounded": true
      },
      {
        "id": "fact_a543edeef4331d708525",
        "object_or_effect": "w_a728c5bb62b954e99804",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_a728c5bb62b954e99804",
        "grounded": true
      },
      {
        "id": "fact_a5a558eca58b23f321de",
        "object_or_effect": "w_dc50a5d58ec1198ad788",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_dc50a5d58ec1198ad788",
        "grounded": true
      },
      {
        "id": "fact_a5ae43897f6f9f99426b",
        "object_or_effect": "w_07eafc1bdb973a6817a1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_07eafc1bdb973a6817a1",
        "grounded": true
      },
      {
        "id": "fact_a854edeb72099020ced9",
        "object_or_effect": "w_7a45acfd5d11b8bc375b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7a45acfd5d11b8bc375b",
        "grounded": true
      },
      {
        "id": "fact_a8cb4d1e8dc8eafa2ee0",
        "object_or_effect": "w_db4492aed9eb20cf46ca",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_db4492aed9eb20cf46ca",
        "grounded": true
      },
      {
        "id": "fact_a8f2b76abd664199993d",
        "object_or_effect": "w_aa02fe7f7abb2cb6a215",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_aa02fe7f7abb2cb6a215",
        "grounded": true
      },
      {
        "id": "fact_a9a5c665ca32ca931f63",
        "object_or_effect": "w_2cdebf2f92450e4ed58b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2cdebf2f92450e4ed58b",
        "grounded": true
      },
      {
        "id": "fact_abe5d9325bf72c9d4c8b",
        "object_or_effect": "w_a6b989a75be1937aaa45",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_a6b989a75be1937aaa45",
        "grounded": true
      },
      {
        "id": "fact_ade19aba33ca09d49b57",
        "object_or_effect": "w_548b4282de0e09a514da",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_548b4282de0e09a514da",
        "grounded": true
      },
      {
        "id": "fact_aec4b50e0a4058951fdb",
        "object_or_effect": "w_a6e4c301b720d54bebdc",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_a6e4c301b720d54bebdc",
        "grounded": true
      },
      {
        "id": "fact_af955dfe952a6ca364f6",
        "object_or_effect": "w_53a85741cc77abb56c4b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_53a85741cc77abb56c4b",
        "grounded": true
      },
      {
        "id": "fact_b95d524bfebfb67a2dc3",
        "object_or_effect": "w_54c5339ede15fcb3f663",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_54c5339ede15fcb3f663",
        "grounded": true
      },
      {
        "id": "fact_b9754c9396cd4f64898f",
        "object_or_effect": "w_3efd5b777471ab5b9abf",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3efd5b777471ab5b9abf",
        "grounded": true
      },
      {
        "id": "fact_b997c5ce1fb80439f677",
        "object_or_effect": "w_4236091efed43e567e24",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4236091efed43e567e24",
        "grounded": true
      },
      {
        "id": "fact_ba746aee0c689ba455f5",
        "object_or_effect": "w_ecc05255d4fa5177cb56",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ecc05255d4fa5177cb56",
        "grounded": true
      },
      {
        "id": "fact_bb7ea2d5aa226b3ebfec",
        "object_or_effect": "w_88c82d6981ae6a690795",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_88c82d6981ae6a690795",
        "grounded": true
      },
      {
        "id": "fact_bbb2a586295099544957",
        "object_or_effect": "w_7a45acfd5d11b8bc375b",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_7a45acfd5d11b8bc375b",
        "grounded": true
      },
      {
        "id": "fact_beabd33db17303255843",
        "object_or_effect": "w_363d09c9d30a9d26d277",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_363d09c9d30a9d26d277",
        "grounded": true
      },
      {
        "id": "fact_bf5b653a576a68429c0a",
        "object_or_effect": "w_cff3b832f9eecfe99f88",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_cff3b832f9eecfe99f88",
        "grounded": true
      },
      {
        "id": "fact_c00c3e9101f8e5ce58f6",
        "object_or_effect": "w_4236091efed43e567e24",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_4236091efed43e567e24",
        "grounded": true
      },
      {
        "id": "fact_c2c8cceac6516d992712",
        "object_or_effect": "w_f958692dc6b6a74fa00f",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_f958692dc6b6a74fa00f",
        "grounded": true
      },
      {
        "id": "fact_c2ef8d5166e1274fc048",
        "object_or_effect": "w_548b4282de0e09a514da",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_548b4282de0e09a514da",
        "grounded": true
      },
      {
        "id": "fact_c3c2b4ebf4770d254cec",
        "object_or_effect": "w_670e36a81e025c0d4ad2",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_670e36a81e025c0d4ad2",
        "grounded": true
      },
      {
        "id": "fact_c575d8c9648092a42df8",
        "object_or_effect": "w_84b092632dcf59e71e76",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_84b092632dcf59e71e76",
        "grounded": true
      },
      {
        "id": "fact_c5c75696fe8f92240dfc",
        "object_or_effect": "w_0b900941043b7a2cff1a",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_0b900941043b7a2cff1a",
        "grounded": true
      },
      {
        "id": "fact_c65606600e53518ce647",
        "object_or_effect": "w_e1838eb1aed8cd4c1cb6",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_e1838eb1aed8cd4c1cb6",
        "grounded": true
      },
      {
        "id": "fact_c786514ed89da983f0dc",
        "object_or_effect": "w_787cb179a735ddceffc5",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_787cb179a735ddceffc5",
        "grounded": true
      },
      {
        "id": "fact_c931e8e3dcb1f78c6eae",
        "object_or_effect": "w_0749d4cc425f5fcfce29",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0749d4cc425f5fcfce29",
        "grounded": true
      },
      {
        "id": "fact_ca355ae109a421ac40a3",
        "object_or_effect": "w_c8a73eabb0611ff136f2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c8a73eabb0611ff136f2",
        "grounded": true
      },
      {
        "id": "fact_cace925b8eaaa3fc7ebe",
        "object_or_effect": "w_ecc05255d4fa5177cb56",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_ecc05255d4fa5177cb56",
        "grounded": true
      },
      {
        "id": "fact_cc05988bbb04c093e517",
        "object_or_effect": "w_62abb51f508f57648ce0",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_62abb51f508f57648ce0",
        "grounded": true
      },
      {
        "id": "fact_cdcf4a4b8844475e968e",
        "object_or_effect": "w_70bae251cef7dc0231a2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_70bae251cef7dc0231a2",
        "grounded": true
      },
      {
        "id": "fact_cec398ebb9b2b8c0db96",
        "object_or_effect": "w_72293b019796bafdaca1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_72293b019796bafdaca1",
        "grounded": true
      },
      {
        "id": "fact_cf2f43e54dac3068405d",
        "object_or_effect": "w_48174cac8188054bb0e3",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_48174cac8188054bb0e3",
        "grounded": true
      },
      {
        "id": "fact_d077ad5bfbfaacf19eec",
        "object_or_effect": "w_f7d775ddd65613cecf18",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f7d775ddd65613cecf18",
        "grounded": true
      },
      {
        "id": "fact_d0d1118d26a33e1b3f0f",
        "object_or_effect": "w_ef3c341057b5db3c5fa7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ef3c341057b5db3c5fa7",
        "grounded": true
      },
      {
        "id": "fact_d17c5e0ed8c3395ca818",
        "object_or_effect": "w_63260e9379f3031619f4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_63260e9379f3031619f4",
        "grounded": true
      },
      {
        "id": "fact_d1baeeffa5e2febae690",
        "object_or_effect": "w_d658d6b869263e96618e",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_d658d6b869263e96618e",
        "grounded": true
      },
      {
        "id": "fact_d25910aec0fd5090c860",
        "object_or_effect": "w_c6d5b45cc91f86f56c47",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c6d5b45cc91f86f56c47",
        "grounded": true
      },
      {
        "id": "fact_d56522d1037860ad512c",
        "object_or_effect": "w_725a1492cd80906affc8",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_725a1492cd80906affc8",
        "grounded": true
      },
      {
        "id": "fact_d6bd3781d9de19651433",
        "object_or_effect": "w_6337dfffbbfb46747470",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_6337dfffbbfb46747470",
        "grounded": true
      },
      {
        "id": "fact_d6d00ed36e2e9f399220",
        "object_or_effect": "w_c6d5b45cc91f86f56c47",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c6d5b45cc91f86f56c47",
        "grounded": true
      },
      {
        "id": "fact_d993bd4fff45b074ade9",
        "object_or_effect": "w_a4bf05e2e0fa3bb62a02",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_a4bf05e2e0fa3bb62a02",
        "grounded": true
      },
      {
        "id": "fact_da6c47aed8ef60ced947",
        "object_or_effect": "w_64392feb5d35d5690c9a",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_64392feb5d35d5690c9a",
        "grounded": true
      },
      {
        "id": "fact_e2f395f3c831dc3afc7b",
        "object_or_effect": "w_2de3fbb2f391db21def5",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_2de3fbb2f391db21def5",
        "grounded": true
      },
      {
        "id": "fact_e34cd9dc04132e4cccac",
        "object_or_effect": "w_2de3fbb2f391db21def5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2de3fbb2f391db21def5",
        "grounded": true
      },
      {
        "id": "fact_e3f38b8187cdb7c570ca",
        "object_or_effect": "w_01984b25b779f9444f47",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_01984b25b779f9444f47",
        "grounded": true
      },
      {
        "id": "fact_e57cb3acfe6ff0ed0d0b",
        "object_or_effect": "w_670e36a81e025c0d4ad2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_670e36a81e025c0d4ad2",
        "grounded": true
      },
      {
        "id": "fact_e62baad076339ee05f60",
        "object_or_effect": "w_ddda453cc8e0caa36d9c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ddda453cc8e0caa36d9c",
        "grounded": true
      },
      {
        "id": "fact_e83e6b198cff19752887",
        "object_or_effect": "w_3d451cfa23056fc0501c",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_3d451cfa23056fc0501c",
        "grounded": true
      },
      {
        "id": "fact_ee3f6f4811428e9fb123",
        "object_or_effect": "w_c2acb1314263b0dacf0e",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c2acb1314263b0dacf0e",
        "grounded": true
      },
      {
        "id": "fact_ee9bed9071dc3a50dbcf",
        "object_or_effect": "w_64380128275b46bbb988",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_64380128275b46bbb988",
        "grounded": true
      },
      {
        "id": "fact_f3b0ac0c2f8f51df5b0a",
        "object_or_effect": "w_84b092632dcf59e71e76",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_84b092632dcf59e71e76",
        "grounded": true
      },
      {
        "id": "fact_f42b6425b8c7e2471f56",
        "object_or_effect": "w_72293b019796bafdaca1",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_72293b019796bafdaca1",
        "grounded": true
      },
      {
        "id": "fact_f4f2e888f85e38924a87",
        "object_or_effect": "w_d8cf7a55d20154849817",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_d8cf7a55d20154849817",
        "grounded": true
      },
      {
        "id": "fact_f61afbd447555507d10e",
        "object_or_effect": "o_1af141754587cc122857",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_f701c629cb85b9673c5a",
        "object_or_effect": "w_1cf2cc7781b2e96f361b",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_1cf2cc7781b2e96f361b",
        "grounded": true
      },
      {
        "id": "fact_f81d563d62e0a3b4cc67",
        "object_or_effect": "w_bf068bd805baf003140e",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_bf068bd805baf003140e",
        "grounded": true
      },
      {
        "id": "fact_fd93f252ad6ee1196171",
        "object_or_effect": "w_0dde9217bb3a7141057a",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_0dde9217bb3a7141057a",
        "grounded": true
      },
      {
        "id": "fact_fd9c2af5b0be2f9111dc",
        "object_or_effect": "w_64c5e08cd139a4cc876e",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_64c5e08cd139a4cc876e",
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
        "count": 1
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "prefix_reachability",
        "answer": "unsat",
        "count": 64
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 5,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 5,
      "yield_to_source_bound_semantic_review": 1,
      "revision_outside_actual_feedback_scope": 1,
      "noncached_action_limit": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 129,
      "source_task_reading": 12,
      "external_dependency": 18,
      "covered_holder_grant": 1,
      "intra_ledger_transfer": 1,
      "scope_missing": 4
    }
  }
}
```

## RQ1_de08a43a1826

证据目录 run/members/RQ1_de08a43a1826/attempt_1/，报告哈希 f0a1f666f7d26914329c6357b9c8a49ea644ff4dd6db191aabbbe08970225743

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unrelated_or_secondary_graph_pairs_deferred,semantic_answer_outside_sent_scope,category_ambiguous_or_outside_supported_task",
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
          "detail_sha256": "34f74cbec81e5db297022f7f80f2b972286ec7e67563f0e807470a1eca93b642",
          "issue": "issue_b0448e0383bbd1d7a21f"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "87a5e1f54244b330730e1e069788b2d9f979ff885ede54f9ef2fd60486d4de30",
          "issue": "issue_b0448e0383bbd1d7a21f"
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
        "label": "original_path_commit",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "baseline_usable",
        "answer": "unsat",
        "count": 60
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 120
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 80
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 60
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 40
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 6,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 2,
      "shared_declaration_in_distinct_applied_contexts": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 5
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 29,
      "external_dependency": 53,
      "policy_missing": 6,
      "source_context_missing": 2,
      "source_task_reading": 7
    }
  }
}
```

## RQ1_e13bb6580d65

证据目录 run/members/RQ1_e13bb6580d65/attempt_1/，报告哈希 429e1764754cf351cdfbcb2296807b51e4dfcb1be1eed6c70c258a89fb5c78fd

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "not_detected",
    "FCR-MINT": "alarm",
    "FCR-DESTROY": "alarm",
    "FCR-PAUSE": "unsupported",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-PAUSE"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": true,
    "paired_id": "RQ1_94d9f2cfc77c",
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
      "FCR-DESTROY"
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "de80dafdf3a06fac15f01ccb52d48b4ffe36a7933bdaf584de61ee71f6bba277",
          "issue": "issue_c3262c68d164c8ef098e"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 2
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
        "answer": "sat",
        "count": 1
      },
      {
        "label": "financial_value",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 7
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 7
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
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 5,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE",
      "FCR-MINT",
      "FCR-TRANSFER"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 98,
      "source_task_reading": 32,
      "scope_missing": 2,
      "program_support": 2,
      "no_debit_in_scope": 1
    }
  }
}
```

## RQ1_e1ce695fff9e

证据目录 run/members/RQ1_e1ce695fff9e/attempt_1/，报告哈希 10282e5d743b611dfa1c4133eb659c5dcbd0947dd88f13a779dbccc884f5e773

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
    "已确认消费/覆盖诊断 category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,unbound_or_inapplicable_seed,no_locatable_source",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": false,
    "paired_id": "RQ1_bcafc7a40ce2",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "56b4ae2a9c5362c757cd0ba1bc3ce2e6d63f57e16660eb3a0052e78403388906",
          "issue": "issue_156faf7cda4af61c38a3"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "720a097727f90054502d4af61638d9c5dae419c5ce7e093435a582a8cba0c5e7",
          "issue": "issue_156faf7cda4af61c38a3"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "77bf7c6ec93a163da0283cfa4603f83cb907e44b309e82465efe3cb4b75ad9e0",
          "issue": "issue_76b0b3caa95fb86acf80"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "70adefb9a9fdcd3aa26abf4485aff1a259e3c18d3e116d96794e71d1659d7b0b",
          "issue": "issue_76b0b3caa95fb86acf80"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "82365d1a03a87979b8f50a44f39aaa894c671c4bd9ab48c3e02ed32477359b0f",
          "issue": "issue_1ebb9413b11f9c6d24e6"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d22ba48f67ddcce444065982795f2eb363320e3c37a98d61a88e5392e922fe93",
          "issue": "issue_1ebb9413b11f9c6d24e6"
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
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 3,
      "no_locatable_source": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 35,
      "external_dependency": 10
    }
  }
}
```

## RQ1_e25d32acc1f7

证据目录 run/members/RQ1_e25d32acc1f7/attempt_1/，报告哈希 b3589cb3b835db37e26281cbc46888be513ac55e100a9dcda82bb605cc9d5ada

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "not_detected",
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
    "已确认消费/覆盖诊断 unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,invalid_semantic_row,revision_outside_actual_feedback_scope",
    "未决类别 FCR-DESTROY,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": false,
    "paired_id": "RQ1_9451d6dac4de",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "520bebdfa7d1e621a05706344f3c53a725c523b13a40d54b6c6b4139c799631c",
          "issue": "issue_c10cabdda9cba77b2f55"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ad5f0fbd45ba5261f0210d970e9a99f09fa4cb320f41cc8967d2eb24f91f254b",
          "issue": "issue_7b4c60a9dfbcb6b22396"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "092d8f35f83e2ff942cc3a80fc69056c6f21082d9e50412f09c218de7cdddb86",
          "issue": "issue_a78ab03de4ea557e2644"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "53370abf3fafeaf514b8319adc7b4bc088cee1a8e3a7c099f74c133a84b08099",
          "issue": "issue_c958f6002bc414d27554"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "2e6d46c1c1b810c9baec94b68310b1f58ad16347bb168d1cce8e14816d607b13",
          "issue": "issue_c958f6002bc414d27554"
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
          "detail_sha256": "07848413d06d731a4914844543a06710f7017ec3e756060567a770f1a7338a2f",
          "issue": "issue_3498ff64efb73e62e8d9"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b9e2d051145e77f7fb480fc7dfd5945e3e52c5fb7b403025df911961eae11636",
          "issue": "issue_3498ff64efb73e62e8d9"
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
        "count": 2
      },
      {
        "label": "direct_callback_influence",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "callback_influence",
        "answer": "unsat",
        "count": 2
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
      "invalid_semantic_row": 1,
      "unknown_assessment_vocabulary": 5,
      "category_ambiguous_or_outside_supported_task": 2,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE",
      "FCR-MINT",
      "FCR-PAUSE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 42,
      "source_check_excluded": 1,
      "external_dependency": 2
    }
  }
}
```
