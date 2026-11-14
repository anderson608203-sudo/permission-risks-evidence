# 逐例审阅

## RQ1_6a278772c4f3

证据目录 run/members/RQ1_6a278772c4f3/attempt_1/，报告哈希 44ac3ecdd02ca86e0b9f019c4a15d8e8bdff2f68fea62681320b58dabbee0cd5

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
    "已确认消费/覆盖诊断 category_ambiguous_or_outside_supported_task,noncached_action_limit,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": true,
    "paired_id": "RQ1_980e04c92f4d",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "4ea635915faf98827326e7d50db00cd7f192f74e95138ad2785b0acf222b437c",
          "issue": "issue_27525788ab729bd977b1"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "cfb773fe5135df5e3531b4d012388b7630b66b48f1c832f786dd4d8d55225984",
          "issue": "issue_27525788ab729bd977b1"
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
          "detail_sha256": "f3a978c65a5ee0124d8b5e90fe4d60b65c18ef50e062cb6b5766bb51a8e1b972",
          "issue": "issue_4c7c0ffc86ebbcf5369c"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "dd24704d7261a8e09f642358bc6068cfaa4e5d5525a65a683598f01eac70c852",
          "issue": "issue_4c7c0ffc86ebbcf5369c"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_7f2578e53c9258fb8409",
        "fact": "fact_024c4e5b02dde10f261e",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_024c4e5b02dde10f261e",
        "object_or_effect": "o_0c988d790aaeed70f65e",
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
        "count": 16
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 17
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
        "count": 5
      },
      {
        "label": "financial_block",
        "answer": "sat",
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
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "noncached_action_limit": 2,
      "unbound_or_inapplicable_seed": 1,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "semantic_meaning_or_explanation_polarity_unresolved": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE",
      "FCR-MINT"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 242,
      "source_task_reading": 22,
      "scope_missing": 9,
      "program_support": 7
    }
  }
}
```

## RQ1_6be1f4b67f6f

证据目录 run/members/RQ1_6be1f4b67f6f/attempt_1/，报告哈希 e1e58cd944712d3c36d95a8ce03a5e59f377f74e1a2f5347220b649f4aa69822

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
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
          "detail_sha256": "32813565496e7cd594377c1251b844565dff5573119c55393fa1875eb1024eca",
          "issue": "issue_998dfb26d4275653390b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "08a60cbafd61b5bf7ac1d34f386f39c2e84922f68fa5f788f2b7888c23178d46",
          "issue": "issue_998dfb26d4275653390b"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "049b96b101c56bde3bdeca6bd6bf37373d65c8b4445f05773e485617dcfa80f7",
          "issue": "issue_03202ccd9996787b951a"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "89dd30bae144c1ac558e0b778b1a47bf024a861472f7526cf3630cb92fd99860",
          "issue": "issue_03202ccd9996787b951a"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "17b0402f6c1532e80f1aa1af359ca513259095817d46f1fea240a19166bf1df6",
          "issue": "issue_0a0aaa9d6585c06d6448"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "cbdb589d78147ad0c3ea7ad523d732817bcbb97441df5384dba372f758b7ba21",
          "issue": "issue_0a0aaa9d6585c06d6448"
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
    "supports": [],
    "facts": [],
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
      "invalid_semantic_row": 9,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 3,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "policy_missing": 1,
      "external_dependency": 2,
      "source_task_reading": 1,
      "no_effect_in_scope": 1
    }
  }
}
```

## RQ1_6c3522e11e92

证据目录 run/members/RQ1_6c3522e11e92/attempt_1/，报告哈希 2587c10bbca14f446e9d84efbd0c5cfbd052d46f1e4e55f614ab0b2ed6acd7ac

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
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
    "已确认消费/覆盖诊断 unknown_assessment_vocabulary,shared_declaration_in_distinct_applied_contexts,unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": false,
    "paired_id": "RQ1_9a61667124cf",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "465bb4080542c52d2f8bd3a7e2140bb8d6e260c0d3d53154c420bdd3fab2e49e",
          "issue": "issue_d371d595cefd1a1fb71e"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d38b2ff8ab7b248bc005e7f9d9d372056a9b7d8dca1a51dec062ec2c051b2edf",
          "issue": "issue_e49282190b63f6aae182"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "85276018732ea0532c35580b6774bc700ac6ea7e8ee0c1a55838146aedaab1e2",
          "issue": "issue_37eb40cb6f1124101b91"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_076762f37cbeaec3e6cc",
        "fact": "fact_6c8f9fcc70c3c72c5256",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_6381c95748726cf9698f",
        "fact": "fact_2085bb360b4f8dee2158",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_f516b8945430d630f749",
        "fact": "fact_912738f36981f75335b1",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_2085bb360b4f8dee2158",
        "object_or_effect": "o_83c5e8ebdbc658dfd4a0",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_6c8f9fcc70c3c72c5256",
        "object_or_effect": "o_76214d4ba48d75d16ae1",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_912738f36981f75335b1",
        "object_or_effect": "o_31fdc1e62d59a35822c7",
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
      "unbound_or_inapplicable_seed": 1,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 225,
      "source_check_excluded": 4,
      "source_task_reading": 25,
      "external_dependency": 6,
      "scope_missing": 4,
      "covered_holder_grant": 1
    }
  }
}
```

## RQ1_6ca2b0aeda43

证据目录 run/members/RQ1_6ca2b0aeda43/attempt_1/，报告哈希 2bbf4c69898715090d90f8e0a46fc04f6b9ac6514d1c06da821fabc492b03097

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
    "positive": false,
    "paired_id": "RQ1_33d48945207e",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "ae2ba840e799ec063dcc44b8d9f787e57ccf83e8040459b7c2cd3a7bd6e6d51e",
          "issue": "issue_72bf8b0b95175e16af92"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "4a13c1a6f3ce2bcc7e4bccf67d05eac1ad4866d67645eb72fc0ecfa7bf1ac80a",
          "issue": "issue_72bf8b0b95175e16af92"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_9f320a00f859f5bf1588",
        "fact": "fact_e98306ac7e46f6708b7d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_e98306ac7e46f6708b7d",
        "object_or_effect": "o_2720ce07bdfe177f82c5",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 4,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "Unsupported:source_semantics_unavailable:path_85b2849dece1deace263": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 209,
      "source_task_reading": 10,
      "external_dependency": 20,
      "scope_missing": 1
    }
  }
}
```

## RQ1_72c6b8c6b605

证据目录 run/members/RQ1_72c6b8c6b605/attempt_1/，报告哈希 07ba2b99f00583a2aa876e03ef6c40bc3ee52e3e6446ea67c2a8832773a00200

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope,category_ambiguous_or_outside_supported_task",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": false,
    "paired_id": "RQ1_b5217318672e",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b78dac214e0d52fa60a7b6b2a49afe7ad33b062f5fb82baefab04f32ff314c3b",
          "issue": "issue_62551d0415da2f3b17cd"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "923918d29101d0b6019f99c7b0c7f9e6eba8caaff8a9e9a51fd24c9daa001179",
          "issue": "issue_101308b751c8efe938b0"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "bc3f7b457385c8f950c7e1c13f2e3c5428d529f439555901218848244c60b545",
          "issue": "issue_34061b4063fa7b6de8d8"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "20083ecb62dedbef1bf8ac58e3def5a615828c9deb44cf80ec55e94354068556",
          "issue": "issue_34061b4063fa7b6de8d8"
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
          "detail_sha256": "8d7305beec0c2aa5093658630f6993f00cf72499c78bedc0e88753e10464058c",
          "issue": "issue_1bf203a31663a656cae7"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "d429f9b0b2ce02840664aa00ae08fe38f19785dbe4c7813d1f20eb7f494babde",
          "issue": "issue_1bf203a31663a656cae7"
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
      "invalid_semantic_row": 7,
      "unknown_assessment_vocabulary": 3,
      "category_ambiguous_or_outside_supported_task": 2,
      "semantic_answer_outside_sent_scope": 3,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 38,
      "source_check_excluded": 1,
      "external_dependency": 6
    }
  }
}
```

## RQ1_73b13298e227

证据目录 run/members/RQ1_73b13298e227/attempt_1/，报告哈希 0b1dc80c29de04a673135ff7c5088217bc67a5f08627a97a37509155d9ce7512

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": true,
    "paired_id": "RQ1_024b9da10799",
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
      "unbound_or_inapplicable_seed": 2,
      "invalid_semantic_row": 4,
      "semantic_answer_outside_sent_scope": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 170,
      "model_phase_missing": 42,
      "external_dependency": 3
    }
  }
}
```

## RQ1_7405f0959142

证据目录 run/members/RQ1_7405f0959142/attempt_1/，报告哈希 2ac2b277e942916d18db7ae7549b54f87c2a167a851f9e34da7d193caa4c3cf2

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
    "target": "FCR-PAUSE",
    "positive": false,
    "paired_id": "RQ1_afb609e0053e",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "751280102b1447a42033f9246d523f278ad48ceedf8e5fa825aade9828f3a6f8",
          "issue": "issue_4ec2809fd4c9ab1742c1"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "15bf016b93b2c22c922625c39728713282d8e4933da687be6b3358f9893af29f",
          "issue": "issue_4ec2809fd4c9ab1742c1"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "7a550e2da2a415f416a0f92c30e77f7e2e2234079627cc7dfd90f0fcb7d4c621",
          "issue": "issue_700d20535c8ffa45a9b8"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "56a44ce8074e57163263746becf634af30fa9d373b23d98f5db26ff52a96e709",
          "issue": "issue_700d20535c8ffa45a9b8"
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
          "detail_sha256": "921ba7d43dcbfb864b357497b43710bd942f88a393f9836f0a051c620009ece3",
          "issue": "issue_11559957d0858502bd68"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "12f415af8cf13caf9676548f598f48af805630cf3c173faf0e348b6f8649037e",
          "issue": "issue_11559957d0858502bd68"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 3,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 44,
      "external_dependency": 5,
      "source_check_excluded": 1
    }
  }
}
```

## RQ1_7450d39da940

证据目录 run/members/RQ1_7450d39da940/attempt_1/，报告哈希 c0e6f9aa38bb9f5248f9e0b468b09b70d262f612a0e53756ef443392006180ba

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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": false,
    "paired_id": "RQ1_39fb6e7197c4",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "ab276067a467c20c3b90c403487ddf83249a5e5aeab9ea102e3606a59b2f0f72",
          "issue": "issue_8721ffa621b2c3661efe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1c1fd601430a7d7207530d1b3d626085fe3e7dca2d231c7786050607ff482202",
          "issue": "issue_8721ffa621b2c3661efe"
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
          "detail_sha256": "04982c9d9622601ee525fdf23fa64d000c7feaaa240f073831cb34bcee9ddc9a",
          "issue": "issue_e596448fb25cdfd1855d"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "8d7f8990795235b06207fa0f6bc267bb10786ef3452ac93074c6e9b0d3011e58",
          "issue": "issue_e596448fb25cdfd1855d"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_5bde7e030d00fe76c6b9",
        "fact": "fact_c3bda691a7e253f71673",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_95aca4301b6e29a3fca3",
        "fact": "fact_aa18b394b6ef58e7e264",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_2d02916609527ddda877",
        "object_or_effect": "w_4f8bbde0d1ef351898a3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4f8bbde0d1ef351898a3",
        "grounded": true
      },
      {
        "id": "fact_aa18b394b6ef58e7e264",
        "object_or_effect": "o_bdddd932af64a27387b9",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_c3bda691a7e253f71673",
        "object_or_effect": "o_abb0d4dbd8c6c130017d",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_f1af3c6190d756b6af6a",
        "object_or_effect": "w_59c0bc3873d6040f2fe3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_59c0bc3873d6040f2fe3",
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
      "unbound_or_inapplicable_seed": 2,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 116,
      "external_dependency": 34
    }
  }
}
```

## RQ1_770ae395781c

证据目录 run/members/RQ1_770ae395781c/attempt_1/，报告哈希 40d9aabe8357bd0a458a7ce17238db24e0bff8a5f2177bfd9c17bd99b71b6323

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
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": false,
    "paired_id": "RQ1_bc5855a83e2d",
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
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_75736c7c70bb89f6bdb6",
        "fact": "fact_95f7d0bb9040cbe270e1",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_95f7d0bb9040cbe270e1",
        "object_or_effect": "o_2995d159bd9a98812a8c",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 2,
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
      "no_effect_in_scope": 95,
      "source_task_reading": 29,
      "covered_holder_grant": 1
    }
  }
}
```

## RQ1_770b64940b4d

证据目录 run/members/RQ1_770b64940b4d/attempt_1/，报告哈希 e31ad19ea18f26ccfd09a1df636835483d878eee40c8b2ce00f63ffb1392e6ec

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,invalid_semantic_row,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_770b64940b4d",
        "reference": "D2:293:author:1",
        "function": "withdrawTokens",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c6f29ee66d15fb505d70b7a8059f2d95d58163ae332e2f04a560607787be50f4",
          "issue": "issue_d4d5fc1be147c4227617"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "3d8a272173a49c42e2f5c7b2ebf82cf2e9844a9bfd8be92d39ae6e43820e715a",
          "issue": "issue_671319066ecba4898951"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "5a169cd369337915298f47c122bb21718359ccc11950b777f27bcabd04553eea",
          "issue": "issue_671319066ecba4898951"
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
      "unbound_or_inapplicable_seed": 5,
      "invalid_semantic_row": 2,
      "unknown_assessment_vocabulary": 2,
      "category_ambiguous_or_outside_supported_task": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "external_dependency": 3,
      "no_effect_in_scope": 8
    }
  }
}
```
