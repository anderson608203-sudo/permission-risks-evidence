# 逐例审阅

## RQ1_983137cbe5d6

证据目录 run/members/RQ1_983137cbe5d6/attempt_1/，报告哈希 34a21de1c32136dc55a8fba8e24d7299e0ca7f23c4e63a61e89a142f7e6e9818

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
    "已确认消费/覆盖诊断 action_slice_exhausted,unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": false,
    "paired_id": "RQ1_18c85d7f1380",
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
          "detail_sha256": "1b4207d1c641309ec0b84a1c4ddfdb09cc7874cb9e0e64f57046278eadf232b3",
          "issue": "issue_0cce7b10bf423f74a60d"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a557a924a5979c92e6fa2fae1f074fe4cb6622752d3e63353bcfff2aed4b6db1",
          "issue": "issue_0cce7b10bf423f74a60d"
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
          "detail_sha256": "7291a907fec953af63cb69f71a21ca501da7747561636d0a8e63bd4be1c5aa0c",
          "issue": "issue_2f744e402bbe6e6499c6"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "78a187fab7ec3d1d27d0802bf3960919e8c69470581cb7c5f89c51c81b924ded",
          "issue": "issue_2f744e402bbe6e6499c6"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_36ed7a022e1cfb7b471b",
        "fact": "fact_ae672b43cbf4dc98d7b3",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_ae672b43cbf4dc98d7b3",
        "object_or_effect": "o_3ba5a12afe5c4770e86e",
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
        "count": 30
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
        "count": 3
      },
      {
        "label": "same_request_amount_change",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 19
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 34
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 17
      },
      {
        "label": "baseline_usable",
        "answer": "unknown",
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
        "label": "financial_block",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "action_slice_exhausted": 5,
      "program_investigation_budget_exhausted": 1,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "scope_missing": 2,
      "no_effect_in_scope": 127,
      "source_task_reading": 36,
      "program_support": 1,
      "covered_holder_grant": 2,
      "external_dependency": 7
    }
  }
}
```

## RQ1_985c6fd1d4e4

证据目录 run/members/RQ1_985c6fd1d4e4/attempt_1/，报告哈希 646b4373497e1024a443376806e4e5343cae4ec3f1820d66302d463f5e8a0616

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "not_detected",
    "FCR-MINT": "not_detected",
    "FCR-DESTROY": "not_detected",
    "FCR-PAUSE": "not_detected",
    "FCR-FREEZE": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": true,
    "paired_id": "RQ1_46a031a993c1",
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "23a6538a9ed5b2f61822e0e7b5063a3598a192d13fc88c7a9ac1328ad4db6f82"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "43aed6cb98d2b04effb122d687b5d9ebf4eaf17d0a679ce17a83158cf09b28bd",
          "issue": "issue_77a64e79738cafaaa7a0"
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
        "answer": "sat",
        "count": 1
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
      "invalid_semantic_row": 5,
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
      "no_effect_in_scope": 42,
      "source_task_reading": 2,
      "program_support": 1
    }
  }
}
```

## RQ1_9a61667124cf

证据目录 run/members/RQ1_9a61667124cf/attempt_1/，报告哈希 d64640754cc4ec78c292b57b4b1b8b1b362e0ed965df39e3ef9b8381d5d137e4

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "unsupported",
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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,shared_declaration_in_distinct_applied_contexts,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": true,
    "paired_id": "RQ1_6c3522e11e92",
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
        "before": "alarm",
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "23a6538a9ed5b2f61822e0e7b5063a3598a192d13fc88c7a9ac1328ad4db6f82"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "6f3ca6b185c53d99a51ae83e69076c2919a20a348ab694fd44e2e7aa534082c4",
          "issue": "issue_19141389dba4637d30ed"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "4f5a06dd6f44727857b27cd7a1c2eb17e1573f3b94b87bb32cbb956da9f569ff",
          "issue": "issue_cc6e6c3cc1750604fe8a"
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
        "count": 6
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "baseline_usable",
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
      "invalid_semantic_row": 9,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 217,
      "source_task_reading": 52,
      "scope_missing": 6,
      "external_dependency": 8,
      "program_support": 2
    }
  }
}
```

## RQ1_9aafb6cd1add

证据目录 run/members/RQ1_9aafb6cd1add/attempt_1/，报告哈希 fca2c555a942521fbb2745a1caf7cf97e8666623c98ebf4ce636e874526032b7

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:587:author:1",
    "last1164 丢失根因 D2:587:author:1",
    "prev200 丢失根因 D2:587:author:1",
    "decision_only 丢失根因 D2:587:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_9aafb6cd1add",
        "reference": "D2:587:author:1",
        "function": "Owned2",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_3144b161e4c4bf19eacd"
        ],
        "decision_only_findings": [
          "finding_fee7e6b250f5486184b3",
          "finding_67b662fdbb9501d73806"
        ],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:587:author:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:587:author:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:587:author:1"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:587:author:1"
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
        "support": "support_4b55d38fde2912cde236",
        "fact": "fact_941ceaf76e347e0e0e52",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_c15c3a9b58a58e388978",
        "fact": "fact_f0b389973db2f3faa643",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_c1ab4899dcb62fbe9c18",
        "fact": "fact_587542a91f6daf9ba1cf",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_27d5eb03e00da4db9af6",
        "object_or_effect": "w_9575a773482ab5091ed3",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_9575a773482ab5091ed3",
        "grounded": true
      },
      {
        "id": "fact_3a8caa6d63efbfe7efbe",
        "object_or_effect": "w_3e55d1ccc4e48cec3d5d",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_3e55d1ccc4e48cec3d5d",
        "grounded": true
      },
      {
        "id": "fact_587542a91f6daf9ba1cf",
        "object_or_effect": "o_eadbc33a403d201e5f7f",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_84986a0965e956600463",
        "object_or_effect": "w_2edefb317f1564a33d3f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2edefb317f1564a33d3f",
        "grounded": true
      },
      {
        "id": "fact_941ceaf76e347e0e0e52",
        "object_or_effect": "o_6769f563011fcda0dd4d",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_d6a84ebc5bbbddf1b3cb",
        "object_or_effect": "w_c0d864a3bab8e6f6b60a",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c0d864a3bab8e6f6b60a",
        "grounded": true
      },
      {
        "id": "fact_f0b389973db2f3faa643",
        "object_or_effect": "o_352d283833df92f4e4d8",
        "meaning": "management_role",
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
        "count": 8
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 8
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 8
      },
      {
        "label": "requester_opens_other_holders_gate",
        "answer": "unsat",
        "count": 1
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
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 6
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "policy_missing": 5,
      "no_effect_in_scope": 20,
      "unassessed_role_change": 3,
      "source_task_reading": 1,
      "external_dependency": 2
    }
  }
}
```

## RQ1_9c365cb18f95

证据目录 run/members/RQ1_9c365cb18f95/attempt_1/，报告哈希 26ca743eb9493653d38b7714d25b21b6c0730c9615e1ae037433de2b620fda64

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "unsupported",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "alarm",
    "FCR-FREEZE": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,yield_to_source_bound_semantic_review,invalid_semantic_row,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": true,
    "paired_id": "RQ1_dc06d7bad0d8",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "69e408364aa74736716d73b8264323439e617c1e01ce15790c638206f5013f6f",
          "issue": "issue_b027b5213535a3c17924"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_91f82f946ea0ca4caa87",
        "fact": "fact_99843fb8b2cca361f787",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_b479ad70e1ff5b92bd9e",
        "fact": "fact_99843fb8b2cca361f787",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_99843fb8b2cca361f787",
        "object_or_effect": "o_9cd725b975376b03323e",
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
        "count": 4
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
        "count": 25
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 25
      },
      {
        "label": "local_premises_feasible",
        "answer": "unsat",
        "count": 18
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 12
      },
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "direct_effect",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "unsat",
        "count": 141
      },
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 2
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 1,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 3,
      "yield_to_source_bound_semantic_review": 2,
      "unknown_assessment_vocabulary": 1,
      "financial_consent_meaning_unresolved": 1,
      "revision_outside_actual_feedback_scope": 1,
      "noncached_action_limit": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 159,
      "source_task_reading": 22,
      "external_dependency": 18,
      "covered_holder_grant": 1,
      "scope_missing": 12,
      "program_support": 2,
      "intra_ledger_transfer": 1
    }
  }
}
```

## RQ1_9d9d397fa18e

证据目录 run/members/RQ1_9d9d397fa18e/attempt_1/，报告哈希 7f0ff08059b341dca3a7abb5e2a4484265c269a6415ce011a0760b5ee3a40610

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed,invalid_semantic_row,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_9d9d397fa18e",
        "reference": "D2:310:author:1",
        "function": "Owned2",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_89414f32edbd57af9e78",
          "finding_9ac96bee0cd2337086cb"
        ],
        "decision_only_findings": [
          "finding_a0f074197f4d4e08fc0a",
          "finding_97c3f0d7705e8dd61c41"
        ],
        "current": "TP"
      }
    ],
    "findings": [
      {
        "idx": 18,
        "member": "RQ1_9d9d397fa18e",
        "finding": "finding_fa2a457ddfde37ae3a73",
        "function": "Owned2()",
        "location": {
          "file": "units/program.sol",
          "start": 1508,
          "length": 18,
          "ast_id": 190
        },
        "result": "TP",
        "reference": "D2:310:author:1",
        "group": "D2:310:author:1",
        "source_excerpt": "owner = msg.sender",
        "source_sha256": "6f8800094bb34e63c53a50208626b55ae95600e91fb06768e67416c0daf48bb7",
        "note": "公开资格写入位于作者标定入口，实际语义支持与资格/下游检查对应。",
        "decision": {
          "status": "risk",
          "reason": "source_role_reassignment",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 1508. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 1508,
              "length": 18,
              "ast_id": 190
            }
          ],
          "effects": [
            "w_5fe4775cd76a51c1b03f"
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
          "detail_sha256": "22abad4b4c06993a3b8faef4791517bcde65e718cf1a557993d0dfe873a15204",
          "issue": "issue_6b98b07488b6b6757ba2"
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
      2995
    ],
    "new": [],
    "disappeared_to_unknown": false,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_64a77559788d439a3a91",
        "fact": "fact_4fb26ab6bc01dff870a9",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_aabbf6c2749f53eeb393",
        "fact": "fact_ff8889da88e324495ec5",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_0131e17f565daeb01e09",
        "object_or_effect": "w_b40a851c6fbbed7a3609",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b40a851c6fbbed7a3609",
        "grounded": true
      },
      {
        "id": "fact_4fb26ab6bc01dff870a9",
        "object_or_effect": "o_c4f10ea09b5feea5b5e6",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_ff8889da88e324495ec5",
        "object_or_effect": "o_6cd02be37668c5c2acf8",
        "meaning": "management_role",
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
        "count": 4
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
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 3,
      "invalid_semantic_row": 3,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 3,
      "unrelated_or_secondary_graph_pairs_deferred": 6
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "policy_missing": 3,
      "no_effect_in_scope": 20,
      "source_task_reading": 3,
      "source_role_reassignment": 1,
      "unassessed_role_change": 2,
      "external_dependency": 2
    }
  }
}
```

## RQ1_9fea8632716d

证据目录 run/members/RQ1_9fea8632716d/attempt_1/，报告哈希 846fd079621c54340247251ecdfacd83fd31b6c0bfd0f6492cf4d6ec482a9bb6

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [
    "decision_only 新增根因 D2:510:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unbound_or_inapplicable_seed,unknown_assessment_vocabulary",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_9fea8632716d",
        "reference": "D2:510:author:1",
        "function": "Ballot",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "FN",
        "prev200_findings": [
          "finding_ba912209a9bc4319f9a9"
        ],
        "decision_only_findings": [],
        "current": "TP"
      }
    ],
    "findings": [
      {
        "idx": 19,
        "member": "RQ1_9fea8632716d",
        "finding": "finding_32453ce8cee2f12ad643",
        "function": "Ballot(uint8)",
        "location": {
          "file": "units/program.sol",
          "start": 300,
          "length": 167,
          "ast_id": 46
        },
        "result": "TP",
        "reference": "D2:510:author:1",
        "group": "D2:510:author:1",
        "source_excerpt": "function Ballot(uint8 _numProposals) public {\n        chairperson = msg.sender;\n        voters[chairperson].weight = 1;\n        proposals.length = _numProposals;\n    }",
        "source_sha256": "9999f8d00a6605a7e77310106a8a37abde3b5cca04bf74b0f015ed04d3b07dfc",
        "note": "实际入口及源码效果与作者独立根因对应，保留程序证据可审计性限制。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 300. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 300,
              "length": 167,
              "ast_id": 46
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
        "gained": [
          "D2:510:author:1"
        ],
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
          "detail_sha256": "a1b9b6c6ef9c7c53a5993a8f45d359e6f230b391800e270f1e8188581f1c9c6a",
          "issue": "issue_9154f79380eadd537bc3"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "29d9eddd22ffec5865a7fa1563a01ac79f8500cdd8c358ce2dd4c446bd97a528",
          "issue": "issue_9154f79380eadd537bc3"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "9971f3aa3aa69d10e76a49d350fbea15b9596447403577d2c66b94540ab8aad9",
          "issue": "issue_337c96a5988a5a399dc5"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "efa3d2a5295cdbbd53b07dad27cf9bb1f9fb570e8b84e049afa9073704300024",
          "issue": "issue_337c96a5988a5a399dc5"
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
          "detail_sha256": "40f38a105896baa46b488826e49fbd3a65bfc6ca400238146ee0d8e4e8a52fd8",
          "issue": "issue_337c96a5988a5a399dc5"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "6d3ea4aa73cb669ee3794d55c6ae62674aedcd7fa4b04c266b948789917ce141",
          "issue": "issue_337c96a5988a5a399dc5"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [
      641
    ],
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
        "count": 2
      },
      {
        "label": "authorization_violation",
        "answer": "unsat",
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
        "count": 16
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 16
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 16
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 8
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 6,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 1,
      "unbound_or_inapplicable_seed": 3,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "policy_missing": 1,
      "external_dependency": 1,
      "program_support": 1,
      "source_task_reading": 2
    }
  }
}
```

## RQ1_a0facbcc1e38

证据目录 run/members/RQ1_a0facbcc1e38/attempt_1/，报告哈希 5311f8ed6bc8dd57a5314afa97a71ff56106ac0bb2bed9b2874f79f5277e6ec2

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
    "prev200 退为未知，不能当作纠正",
    "decision_only 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,unbound_or_inapplicable_seed",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": true,
    "paired_id": "RQ1_86a0269d7608",
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
          "detail_sha256": "471b7a198891c7c6afecda6bda1ebeeb0494e6faf7f70fac549a7f386fa5d36e"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "0ecbc9ed262d24418f1ccd84d115e23a1a54c1bdaaacbb5f3ed953fd4463d502"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 4,
      "semantic_answer_outside_sent_scope": 2,
      "unbound_or_inapplicable_seed": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 182,
      "model_phase_missing": 44,
      "external_dependency": 9
    }
  }
}
```

## RQ1_a3aff7048f13

证据目录 run/members/RQ1_a3aff7048f13/attempt_1/，报告哈希 9a62a8fd7d6638fcd771e2fd25aa7af1530bfc3eb83c5d65d328a88054a56244

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,no_locatable_source",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "cc574eea499854c92e4d9f2db383d632ff36d72cd7dfc49affff18d94217c50d",
          "issue": "issue_ff3925b5185a6a0edfc0"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "bf411817104b6f0882de849745553d59865b6e4491a12c038e832618b4e1d172",
          "issue": "issue_ff3925b5185a6a0edfc0"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "52b29aacf6d6f81eb6c47a20382c22c9240888c1e0b8fe526da10f4c67b57ea5",
          "issue": "issue_1ab6811f54f03b950f9d"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "65f0081c260971a22597f98b7fbdd9bffc6a7bdb954f4c8bd2bba84b5a6c909b",
          "issue": "issue_1ab6811f54f03b950f9d"
        }
      ]
    },
    {
      "index": 1,
      "phase": "protocol_recovery",
      "response_kind": "invalid_protocol",
      "usable": false,
      "status": "protocol_diagnostic",
      "normalization_diagnostics": [
        {
          "reason": "truncated_envelope_complete_items_only",
          "detail_sha256": "fb324a79efb432bd3fd0f4dd672240e6b4dd789b0bc0b3abb9c594b6d0607b50"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "471b7a198891c7c6afecda6bda1ebeeb0494e6faf7f70fac549a7f386fa5d36e"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "0ecbc9ed262d24418f1ccd84d115e23a1a54c1bdaaacbb5f3ed953fd4463d502"
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
      "unbound_or_inapplicable_seed": 8,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "no_locatable_source": 2,
      "truncated_envelope_complete_items_only": 1,
      "invalid_semantic_row": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 105,
      "model_phase_missing": 29,
      "external_dependency": 33
    }
  }
}
```

## RQ1_a4bb8d18e79b

证据目录 run/members/RQ1_a4bb8d18e79b/attempt_1/，报告哈希 4a9840431221f79e60787e39f0427789b283949898e758b50f99d765e74af921

```json
{
  "task": "AC",
  "prediction": {
    "AC": "not_detected"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,unbound_or_inapplicable_seed"
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
        "support": "support_03fd83fff0a4f57c1b4c",
        "fact": "fact_2f75457fb31b3379377b",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_2f75457fb31b3379377b",
        "object_or_effect": "o_4bd82ee030bfca262732",
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
      "semantic_answer_outside_sent_scope": 3,
      "unbound_or_inapplicable_seed": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": true,
    "negative_eligible_categories": [
      "AC"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 3,
      "source_task_reading": 3
    }
  }
}
```
