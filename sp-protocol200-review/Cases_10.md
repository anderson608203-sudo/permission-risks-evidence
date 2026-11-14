# 逐例审阅

## RQ1_776a6b98d18f

证据目录 run/members/RQ1_776a6b98d18f/attempt_1/，报告哈希 b136e9adde2d866860daa0eb2144a46477db2e3066ab3cb7cb14192695f974fe

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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,invalid_semantic_row"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": false,
    "paired_id": "RQ1_8456d2957fff",
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
          "detail_sha256": "e46772664e815b372652949c57b81b627064e1fc39f8419389a0d29f5b50f64b",
          "issue": "issue_9b94f947fc53106f3323"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "e60dcb1b10a80b56d4a65fd6e1876e3554f3411ddaa1a560fdc9c7f4240ce90b",
          "issue": "issue_73e1b581365221e5c0ee"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1bf425eb1b932d8e5d42fda80298588e328ee18074b1face521c558db0fa188d",
          "issue": "issue_73e1b581365221e5c0ee"
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
          "detail_sha256": "88c99684a70a0b5b6d8354011faaa0f3f805791f32177917b6abafdc2ab3a2bc",
          "issue": "issue_73e1b581365221e5c0ee"
        },
        {
          "reason": "ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "b133d1892db30bcd1d365301b83bd4dcbddefb36638a9581fa00352faadc1720",
          "issue": "issue_73e1b581365221e5c0ee"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 4,
      "unknown_assessment_vocabulary": 2,
      "category_ambiguous_or_outside_supported_task": 2,
      "invalid_semantic_row": 2,
      "ambiguous_confirmation_not_a_risk_judgment": 1
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
      "source_check_excluded": 1
    }
  }
}
```

## RQ1_7a54127ed44c

证据目录 run/members/RQ1_7a54127ed44c/attempt_1/，报告哈希 f6a2a330b4cdc23d23710ba1940171a04f4bc95ddda12efef7a5bacd1e776c19

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
    "last1164 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": false,
    "paired_id": "RQ1_4d2acebaa2ff",
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
        "before": "unsupported",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "7a44995e10483cc70b90db97d7614785fec8047087ad7e027170fbb153964060",
          "issue": "issue_e4d1ed7c1bde0070084b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ffd496063a8f14ebd211d5f63f0c0f349abdbca3c8b480f19d95bd5472261cec",
          "issue": "issue_e4d1ed7c1bde0070084b"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "665c1dce76c17b84079b7a8d0e9c10b5459cf319d92ee2b3d5f8afa2ba41abf9",
          "issue": "issue_27736dc327f4969aaa98"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f170960ec8cbcaaee9442f2cdd81c64106754073c379262277fbe466a54a646b",
          "issue": "issue_27736dc327f4969aaa98"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "4f0a21ab2b244966a8f03341225bb3fb996768786d0e0af4986933942a73a684",
          "issue": "issue_7e13d45fc2895c72a827"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f7c5db5d2216c13781fe481560c5c47887f75994a5427c151964d32a08a6992c",
          "issue": "issue_7e13d45fc2895c72a827"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 8,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 5,
      "unrelated_or_secondary_graph_pairs_deferred": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 132,
      "source_task_reading": 31,
      "external_dependency": 7
    }
  }
}
```

## RQ1_7bfd58ffb1ae

证据目录 run/members/RQ1_7bfd58ffb1ae/attempt_1/，报告哈希 e124c4c4a736cb0844a21460df9639990dfe3b5205f48a98975714b245e9c5ea

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
    "已确认消费/覆盖诊断 invalid_semantic_row,action_slice_exhausted,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": false,
    "paired_id": "RQ1_cb8c3fafbda1",
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "3e7fa87176cfe502a18032a71e51c370af5daba9e41823bd3e38d457c96859ac"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "d052a4b38fbe704fc643a9c96300333862ced0127412dff35b2fa1e5ad088b0d",
          "issue": "issue_c860bcc1db7fbf31fe12"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ae0a5171ae34fa212a68e0589c66c8b72d207d73322bc9e5546e727a695963a0",
          "issue": "issue_c860bcc1db7fbf31fe12"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a49f2dfb78f4c181679737cf1566a8d80de69544a2b41d815cf6ad483c6f7cba",
          "issue": "issue_95f18d6a0f0d3fd2a43a"
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
        "count": 40
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
        "label": "financial_consent_unresolved",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 13
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 5
      },
      {
        "label": "same_request_amount_change",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 3
      },
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 19
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 26
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 19
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
      "invalid_semantic_row": 7,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "action_slice_exhausted": 5,
      "program_investigation_budget_exhausted": 1,
      "program_investigation_seconds": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "scope_missing": 4,
      "no_effect_in_scope": 128,
      "program_support": 1,
      "source_task_reading": 40,
      "external_dependency": 6,
      "parameter_only": 1
    }
  }
}
```

## RQ1_7d7240a2af90

证据目录 run/members/RQ1_7d7240a2af90/attempt_1/，报告哈希 fded602b3b475a2ebfb7c27c1b446d829eb2dc0a01d37c8a69c1ef6fe707d035

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,no_locatable_source",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": true,
    "paired_id": "RQ1_8d60a47186e2",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "9c5ddcc964664d286a8ea4da36d3510bc726bca87ce74f183b83a94cbca3b8c6",
          "issue": "issue_a45bc1249b6d0b882ec3"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "51f76cc6c994c6622831a452f0dd6004ce4bd2d2cde1fb73a0e080305a17747d",
          "issue": "issue_4c46b07210995dc611ae"
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
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a33e8822c076ef86153af208e3528fe2cbda08323318ade61468f11f65534d53",
          "issue": "issue_36b4a2138d7671716d92"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 14,
      "unknown_assessment_vocabulary": 3,
      "no_locatable_source": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 19,
      "model_phase_missing": 1
    }
  }
}
```

## RQ1_7dd1efe175e6

证据目录 run/members/RQ1_7dd1efe175e6/attempt_1/，报告哈希 5fc58c2f2ef42df267333244e65d8916e3f7ceacf30c6815bad19476a504efa4

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
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
          "detail_sha256": "62656b6025068c4784f3809fb77ead977791e39e33eb10ae33aee3821192cb7b",
          "issue": "issue_457194939020697781b1"
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
        "count": 2
      },
      {
        "label": "authorization_violation",
        "answer": "unsat",
        "count": 2
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 6,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 15,
      "source_task_reading": 6,
      "source_context_missing": 1,
      "external_dependency": 2,
      "source_check_excluded": 1
    }
  }
}
```

## RQ1_81a85f242b60

证据目录 run/members/RQ1_81a85f242b60/attempt_1/，报告哈希 7f1ae87962101814bd0a046667db8c8c8b121e9ed6bbdf9c250f61db7d7d12fb

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
    "v32 修复版新增误报",
    "last1164 修复版新增误报",
    "prev200 修复版新增误报"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": false,
    "paired_id": "RQ1_b61f163309a1",
    "state": "alarm",
    "changes": {
      "v32": {
        "before": "not_detected",
        "after": "alarm"
      },
      "last1164": {
        "before": "unsupported",
        "after": "alarm"
      },
      "prev200": {
        "before": "not_detected",
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
      "normalization_diagnostics": []
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_1f8571ac11aee98a6906",
        "fact": "fact_96a021d8d1d7a6f01015",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_39ceb98772f98cc81754",
        "fact": "fact_2a1d924cf705b1ead071",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_b3edb1334bf6c8beb62f",
        "fact": "fact_bfd5cc55fc63b1906d23",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_08ea08181eb0f50c4b54",
        "object_or_effect": "w_116349a03356c7812082",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_116349a03356c7812082",
        "grounded": true
      },
      {
        "id": "fact_20dc72649d42381db3c8",
        "object_or_effect": "w_9469912b3eec41c540cf",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_9469912b3eec41c540cf",
        "grounded": true
      },
      {
        "id": "fact_2a1d924cf705b1ead071",
        "object_or_effect": "o_41ba1d2b1d59753dc0fe",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_4dc2a480def84d113f08",
        "object_or_effect": "w_bcebbee10994152dc747",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_bcebbee10994152dc747",
        "grounded": true
      },
      {
        "id": "fact_6e91b3372c71cf0ea2e5",
        "object_or_effect": "w_6a204353fdd7487e0e0f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6a204353fdd7487e0e0f",
        "grounded": true
      },
      {
        "id": "fact_75522dc7f73a7ddcd250",
        "object_or_effect": "w_024ac9d0405c918197b1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_024ac9d0405c918197b1",
        "grounded": true
      },
      {
        "id": "fact_94d4a6de8bc868533251",
        "object_or_effect": "w_e4f929c4d5450c19cc43",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_e4f929c4d5450c19cc43",
        "grounded": true
      },
      {
        "id": "fact_96a021d8d1d7a6f01015",
        "object_or_effect": "o_7f709a009fdc8f9ea7ce",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_aefd89a413731aa0fcc1",
        "object_or_effect": "w_664ccf2beb290e12537c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_664ccf2beb290e12537c",
        "grounded": true
      },
      {
        "id": "fact_b8a4e272dde609c2475d",
        "object_or_effect": "w_bde748e1b531e6f2ff54",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_bde748e1b531e6f2ff54",
        "grounded": true
      },
      {
        "id": "fact_bfd5cc55fc63b1906d23",
        "object_or_effect": "o_07533ad427ea53d5b1b2",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_c4a5cb557af405f8b560",
        "object_or_effect": "w_388371dd0839d7b7cadd",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_388371dd0839d7b7cadd",
        "grounded": true
      },
      {
        "id": "fact_c96b72a72101811c682d",
        "object_or_effect": "w_ea31a4a480512d9eea91",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_ea31a4a480512d9eea91",
        "grounded": true
      },
      {
        "id": "fact_d4dc22cc3df5fa32605c",
        "object_or_effect": "w_68deb1cbddca5b7f005a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_68deb1cbddca5b7f005a",
        "grounded": true
      },
      {
        "id": "fact_effe39374fdb59ab2ce4",
        "object_or_effect": "w_bfd6844efd8900e4be97",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_bfd6844efd8900e4be97",
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 10
      },
      {
        "label": "financial_consent_unresolved",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "baseline_usable",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 6
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 8
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 3
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 8
      },
      {
        "label": "prefix_reachability",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
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
      "unbound_or_inapplicable_seed": 1,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 7
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
      "no_effect_in_scope": 146,
      "source_task_reading": 19,
      "covered_holder_grant": 2,
      "scope_missing": 2,
      "program_support": 1
    }
  }
}
```

## RQ1_8400be2dc985

证据目录 run/members/RQ1_8400be2dc985/attempt_1/，报告哈希 c7b0852eb291fb7295648a51a100327880c87ebfad236bab5c418ca85d47d7e0

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,no_locatable_source,unbound_or_inapplicable_seed",
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
          "detail_sha256": "b55b823b8c463f87c0ab99e73dfcddfdb3b4a832b816983790ac84502921e036",
          "issue": "issue_e8bf41bf35118a6ec211"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1131e6ab42086e9a76db87c02463fb2eb8112448b48e590b5a10a629443ec78f",
          "issue": "issue_e8bf41bf35118a6ec211"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "c8458d710ba78b6d52f689f6112b26a2a8abe4480b5b30c9f0bbc61975ca6792",
          "issue": "issue_d8da778cf3aa648b0d4b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a80b056aa256884f1cb35584850a21598916e56902632bbbe18c5e2b07a65db0",
          "issue": "issue_d8da778cf3aa648b0d4b"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "9361e43f578bc2fe3ac9439732f0d236e514182884dabadb3e69b66b33e181e4",
          "issue": "issue_8b7a3462b43de838c119"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "93c6a71d4f0297c131e7f89880ed25c45b16d5cf45f01aecae8e03dc342cb765",
          "issue": "issue_8b7a3462b43de838c119"
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "9a7075c643ea2e255859bc3bfa49962aa6d76c61b769c2a99fe4ccf5a424251d",
          "issue": "issue_c9ed155ab649f3bc7149"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d5de837c5ae3aa438efbd235d795f87110cc4cd5d10b27bf857ad9e8b3a27212",
          "issue": "issue_f32e4c60738bf2f216b8"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f928d30be2b86268da6c7624548c44b21f7842078def1c23c253efd8cb3188a7",
          "issue": "issue_6134664a6c63235a9db5"
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
        "support": "support_b5780efaa9dd8b7699cf",
        "fact": "fact_0157f1c563afaabf3453",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_cb85589f14b22b0962ea",
        "fact": "fact_cb640736e5b926e95c4b",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_d859c8b8aacbe9abc4e9",
        "fact": "fact_790ef139c617277787cb",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_0157f1c563afaabf3453",
        "object_or_effect": "o_d4ea6739271f96571ae6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_156413ab73192176a08e",
        "object_or_effect": "w_1397abc0273d658874bc",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_1397abc0273d658874bc",
        "grounded": true
      },
      {
        "id": "fact_23c0b10d80eab66bd3d0",
        "object_or_effect": "w_60a64ed923aec90a870d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_60a64ed923aec90a870d",
        "grounded": true
      },
      {
        "id": "fact_49014333d3799e82ed09",
        "object_or_effect": "w_88864dd7a4c78b86a019",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_88864dd7a4c78b86a019",
        "grounded": true
      },
      {
        "id": "fact_6360bc881544ee0b81fd",
        "object_or_effect": "w_1b0e24058424c1dfe1a1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_1b0e24058424c1dfe1a1",
        "grounded": true
      },
      {
        "id": "fact_790ef139c617277787cb",
        "object_or_effect": "o_9645e2e6d38392be98d1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_cb640736e5b926e95c4b",
        "object_or_effect": "o_d1082d78478da3611c75",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_d21e1d2023810c6af868",
        "object_or_effect": "w_0af3524b369a2f71876c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0af3524b369a2f71876c",
        "grounded": true
      },
      {
        "id": "fact_f1815c532d9fec8c497e",
        "object_or_effect": "w_d5221744f6df3cb721fe",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d5221744f6df3cb721fe",
        "grounded": true
      },
      {
        "id": "fact_f42f99e5a873baff6649",
        "object_or_effect": "w_cfaa740ea87b82dbaa20",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cfaa740ea87b82dbaa20",
        "grounded": true
      },
      {
        "id": "fact_fb9ffe644dc7adc9208c",
        "object_or_effect": "w_a973a99fa1383e942a2d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a973a99fa1383e942a2d",
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
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 8
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 6
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 6,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 6,
      "no_locatable_source": 6,
      "unbound_or_inapplicable_seed": 6,
      "unrelated_or_secondary_graph_pairs_deferred": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "policy_missing": 4,
      "no_effect_in_scope": 137,
      "source_task_reading": 127,
      "source_context_missing": 4,
      "external_dependency": 29,
      "unassessed_role_change": 1
    }
  }
}
```

## RQ1_8456d2957fff

证据目录 run/members/RQ1_8456d2957fff/attempt_1/，报告哈希 fd8eb6ecedb2ce07ba2915060c992378b7ffa31c1bc46b065263ad80ae3cd225

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "not_detected",
    "FCR-MINT": "not_detected",
    "FCR-DESTROY": "alarm",
    "FCR-PAUSE": "not_detected",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "last1164 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,no_locatable_source,category_ambiguous_or_outside_supported_task"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": true,
    "paired_id": "RQ1_776a6b98d18f",
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
          "detail_sha256": "e3e945bbdca44656848875ac31aede69ebc7d36a750c14500c35e6e12e005137",
          "issue": "issue_897603750a6550fc2fa1"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "2302d2c33808ba5295a58ad48a176ddf08c6205db7ae76bb7c60d84b13f06b82",
          "issue": "issue_332bdcb8b280bc4eac0f"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "46b49c11e4e890d684079f062cf24900ae3b21f80f64bcd967273d7c7869abd9",
          "issue": "issue_332bdcb8b280bc4eac0f"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_44286048cf7a02ba376c",
        "fact": "fact_b6677a999303a7244efa",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_5b9c72706310b4d49853",
        "fact": "fact_88776b2df886b4171637",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_67e990b1bd18b77ce88a",
        "fact": "fact_5d583b62c6507421b009",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_fb0a504989eb314f7da0",
        "fact": "fact_9e8998530b8f44cb3fe2",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_5d583b62c6507421b009",
        "object_or_effect": "o_d5e4aa422ab337a8ba7e",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_6efbf1405b1b59f745de",
        "object_or_effect": "w_27d31623886cf2ab24f8",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_27d31623886cf2ab24f8",
        "grounded": true
      },
      {
        "id": "fact_88776b2df886b4171637",
        "object_or_effect": "o_f6fca82be02e49a438f4",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_9e8998530b8f44cb3fe2",
        "object_or_effect": "o_12e84c228e2805b7b4bd",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_b6677a999303a7244efa",
        "object_or_effect": "o_08495af89bff9c0aa312",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_db702879479d436297e4",
        "object_or_effect": "w_300b815dbe040900eb34",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_300b815dbe040900eb34",
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
        "label": "direct_effect",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 3,
      "unknown_assessment_vocabulary": 2,
      "category_ambiguous_or_outside_supported_task": 1,
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
      "no_effect_in_scope": 19,
      "uncompensated_debit": 1
    }
  }
}
```

## RQ1_84ed7052a606

证据目录 run/members/RQ1_84ed7052a606/attempt_1/，报告哈希 4a06f26a2d1a3ec2e455467ed0f2180c0c8e15b434177a38558216843bc79051

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_84ed7052a606",
        "reference": "D2:418:author:1",
        "function": "init",
        "v32": "TP",
        "last1164": "TP",
        "b5": "FN",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_abdb81b05f23df9e4eae"
        ],
        "decision_only_findings": [
          "finding_2d9bc50515585acfac27"
        ],
        "current": "TP"
      }
    ],
    "findings": [
      {
        "idx": 14,
        "member": "RQ1_84ed7052a606",
        "finding": "finding_ab0f2a2e94eee33891a7",
        "function": "init()",
        "location": {
          "file": "units/program.sol",
          "start": 1558,
          "length": 56,
          "ast_id": 180
        },
        "result": "TP",
        "reference": "D2:418:author:1",
        "group": "D2:418:author:1",
        "source_excerpt": "function init()\n    {\n        Holder = msg.sender;\n    }",
        "source_sha256": "5508c1c2fdd37ff8679263626af7420ce7dfc2e8c6c5b92b6ef3c66c48a35b03",
        "note": "实际入口及源码效果与作者独立根因对应，保留程序证据可审计性限制。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 1558. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 1558,
              "length": 56,
              "ast_id": 180
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
      },
      {
        "idx": 15,
        "member": "RQ1_84ed7052a606",
        "finding": "finding_06f43f445ef724350d39",
        "function": "Close()",
        "location": {
          "file": "units/program.sol",
          "start": 2661,
          "length": 118,
          "ast_id": 330
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_84ed7052a606', 'units/program.sol', 2661)",
        "source_excerpt": "function Close() public\n    {\n        if (msg.sender == Ho1der)\n        {\n            suicide(Ho1der);\n        }\n    }",
        "source_sha256": "5508c1c2fdd37ff8679263626af7420ce7dfc2e8c6c5b92b6ef3c66c48a35b03",
        "note": "实际报警入口或影响与作者参考不同，不能抵销该独立根因漏检。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 2661. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 2661,
              "length": 118,
              "ast_id": 330
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
          "E9"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "2e1c3b3f9d2c36fff1b25721e73450d13c2c4bf5c37dc30bfcaffc21886dcab7",
          "issue": "issue_67d61823292733b09452"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "02de170f3803ac8a629192a371beb329c0eeb41e08c5decace5e689b57dec862",
          "issue": "issue_67d61823292733b09452"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "181c5e0c656d804d8dcd33d92fc60d408d337e19b0c57ff3e87c090f9e0a56af",
          "issue": "issue_4e5c32311f3397c3e4f8"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "817ea6b9344289dc4c684b4a2d865debf0140f111326aaec362ffdbdb6531546",
          "issue": "issue_4e5c32311f3397c3e4f8"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "e7d7d0fa5f4cb952cba58a575a8fbeae5f669638f4c66dc9b38fb0ea76bbefdb",
          "issue": "issue_dbb1012e344ff2ee1af7"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "7597f36551fbb5621bba37e1d00db3f05cfac504e7f9e3aba857232f22ea3615",
          "issue": "issue_dbb1012e344ff2ee1af7"
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
      1768
    ],
    "new": [
      2661
    ],
    "disappeared_to_unknown": false,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_2fcac980cbc8b7e1f702",
        "fact": "fact_0ccf49d7a2888cb276b7",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_72b80ba06dd7ee871088",
        "fact": "fact_36f40a265ba702090f5a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_76e0ab0f93404a2dd0ed",
        "fact": "fact_0ccf49d7a2888cb276b7",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_816dd9cb41c1a13db16d",
        "fact": "fact_c46ac8e1dae612ed4c7d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_95c358be5b6e22c6da50",
        "fact": "fact_e02282674aa06a9eb4df",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_c7b37409e952f147f535",
        "fact": "fact_e02282674aa06a9eb4df",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_0ccf49d7a2888cb276b7",
        "object_or_effect": "o_cce3dd1c641a1fc4b407",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_36f40a265ba702090f5a",
        "object_or_effect": "o_c9a6a7f59df481013797",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_c02f5260138603d1de63",
        "object_or_effect": "w_d0c4f45285c613e8528d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d0c4f45285c613e8528d",
        "grounded": true
      },
      {
        "id": "fact_c46ac8e1dae612ed4c7d",
        "object_or_effect": "o_17bb8c7224f9c8ad9443",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_e02282674aa06a9eb4df",
        "object_or_effect": "o_a22afba67b6dcc9375ed",
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
        "label": "authorization_violation",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "authorization_violation",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 8
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 8
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 8
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 1,
      "invalid_semantic_row": 3,
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
      "no_effect_in_scope": 7,
      "source_task_reading": 3,
      "policy_missing": 2,
      "program_support": 2
    }
  }
}
```

## RQ1_852d7abd1772

证据目录 run/members/RQ1_852d7abd1772/attempt_1/，报告哈希 b52e23d4b88255fb3b136e8e14b08b0ad755cf4b66a5734f37c35655670d8ed9

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_852d7abd1772",
        "reference": "D2:321:author:1",
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "23a6538a9ed5b2f61822e0e7b5063a3598a192d13fc88c7a9ac1328ad4db6f82"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "3e7fa87176cfe502a18032a71e51c370af5daba9e41823bd3e38d457c96859ac"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "c5faa851e2e73c4d43c12729559b48a7b457d735cd91983375ee5feb06d9d02a",
          "issue": "issue_93aae26ccdc34501dc8f"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "e30cdb84ffead9873b604c8e041b11a952895b22f2f5283e55e221761bd96bde",
          "issue": "issue_93aae26ccdc34501dc8f"
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
      "unbound_or_inapplicable_seed": 6,
      "invalid_semantic_row": 4,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "external_dependency": 3,
      "no_effect_in_scope": 6
    }
  }
}
```
