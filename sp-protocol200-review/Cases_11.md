# 逐例审阅

## RQ1_868007cf433c

证据目录 run/members/RQ1_868007cf433c/attempt_1/，报告哈希 7a049464ce2911208ea364da618a080afaec3f056f1e2f06637934ef66ca36a5

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "prev200 丢失根因 D2:222:original:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_868007cf433c",
        "reference": "D2:222:original:1",
        "function": "fallback",
        "v32": "FN",
        "last1164": "FN",
        "b5": "FN",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "pending",
        "prev200_findings": [
          "finding_d2dad93ac9ee93c50ea0"
        ],
        "decision_only_findings": [
          "finding_f86e69b76e2c09a625e6"
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
        "lost": []
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:222:original:1"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "e0b9d0ce7678ff53b3a4e5ef2913fd77766cf6025803d54224237975dd7bfeec",
          "issue": "issue_0b8c6b5291f087102865"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "51f3e4f16c357c7b37890f2bbe1d8d446b4c34d092a69550ca816886537f479b",
          "issue": "issue_0b8c6b5291f087102865"
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
        "support": "support_3d1617275d1ef614566c",
        "fact": "fact_97728ad33599183420e8",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_f3b5505bb09f90e0994c",
        "fact": "fact_3f1e358c66803844080d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_3f1e358c66803844080d",
        "object_or_effect": "o_18b79c65b03d81d1643f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_97728ad33599183420e8",
        "object_or_effect": "o_651a33f08c51280234f2",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_c3df0f49dbadab2db790",
        "object_or_effect": "w_1c3a566608121f372136",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1c3a566608121f372136",
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
        "count": 4
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 5
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 6,
      "semantic_answer_outside_sent_scope": 2,
      "unbound_or_inapplicable_seed": 1,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 6,
      "policy_missing": 1
    }
  }
}
```

## RQ1_86a0269d7608

证据目录 run/members/RQ1_86a0269d7608/attempt_1/，报告哈希 50230fd26b0b98eed553d5b7a25f82c3f619811c2ce59c2d9245a6c59d97bb3b

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
    "v32 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": false,
    "paired_id": "RQ1_a0facbcc1e38",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "9bfa11af7f356ba3d3cb25a7566bad4419b927c129eae2547d9b19463bfcca4d",
          "issue": "issue_6ccd6ce012390845797e"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d31f54023132c1c1616c3d1fa8f7fe9a8dc1370d42883def6e014725ce17cf6e",
          "issue": "issue_4cc9f932590864aebbcd"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_322ce80d7ae99bb4e148",
        "fact": "fact_1ffd5eefbbfeb0da266b",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_1ffd5eefbbfeb0da266b",
        "object_or_effect": "o_2a9b55f2deadd65bad36",
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
        "answer": "unsat",
        "count": 3
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "baseline_usable",
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
      "invalid_semantic_row": 5,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE",
      "FCR-PAUSE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 184,
      "source_task_reading": 26,
      "external_dependency": 9,
      "scope_missing": 1
    }
  }
}
```

## RQ1_8d60a47186e2

证据目录 run/members/RQ1_8d60a47186e2/attempt_1/，报告哈希 a10f63f6e3c5b8f5ab68fe528dc239b60a92eade4f5cf21eb8c0fbfe312af8d4

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
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,no_locatable_source"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": false,
    "paired_id": "RQ1_7d7240a2af90",
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
        "before": "not_detected",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a80026ef0676a6e509956a78bc1b03fb1d98dd3b50e8cd7919cf826ac5e0ba4e",
          "issue": "issue_f7ab83bc83ac16aad412"
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "81d106cdd5f963be0e49ce2781bd730002c17bdc887f15d0480908b1b14e4f31",
          "issue": "issue_c7a7dbb72f372c2ec77f"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 6,
      "unknown_assessment_vocabulary": 2,
      "no_locatable_source": 1
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

## RQ1_8e8598bb724e

证据目录 run/members/RQ1_8e8598bb724e/attempt_1/，报告哈希 b2d0e8103b3c9324b2f0c0b31571ee19cf795c60035256285594190a7eb5944b

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
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,unknown_assessment_vocabulary,no_locatable_source",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": true,
    "paired_id": "RQ1_fbd0377ce541",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "bbcba920cbe50d5e61c33385579d8fe9c3bc2bdd94c8f2f924e4641a9ad4f976",
          "issue": "issue_75f4a6fdc9a5309a39e5"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 12,
      "semantic_answer_outside_sent_scope": 3,
      "unknown_assessment_vocabulary": 1,
      "no_locatable_source": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 99,
      "model_phase_missing": 6
    }
  }
}
```

## RQ1_94187f5625cc

证据目录 run/members/RQ1_94187f5625cc/attempt_1/，报告哈希 56ae60442b60953a833e7b5b40f63ab2e94f6b800683b59b606a024ff4ae9b36

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task,semantic_answer_outside_sent_scope",
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
          "detail_sha256": "aa28467a3390bd5783d5f15e18012b7e62e7b853dfcc5a6275c64a663fd6537f",
          "issue": "issue_007bbf09836ed8e3052d"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "96c3a2653d5cc974f9cf9d0026d67604b19de0dfe51dd6d72f3698656ae29403",
          "issue": "issue_007bbf09836ed8e3052d"
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
          "detail_sha256": "4269f79e5a362337022bdb1b4b008f9c75a46c31edfcbc3940164bf7c2782dbb",
          "issue": "issue_41623d914427cf1afa93"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "bcf86db962b9cf5de0f453573f7326f25163693acf9fc609a6f3bbda8d71cec2",
          "issue": "issue_41623d914427cf1afa93"
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
        "support": "support_0ccf0bab5221a9f3385c",
        "fact": "fact_83f20854f25f13c5387d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_1af3d957b99dff9bfd3c",
        "fact": "fact_e5189be666a09c270a5e",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_1f01eb929d3974c09922",
        "fact": "fact_34ee1b0a81b3c509db5a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_4b2a5d51a88710889b78",
        "fact": "fact_eb05d1c474426e14d20a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_7d8b6e74bee2f9d248bb",
        "fact": "fact_30c4cea7799c3f37954c",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_a2fcd5e1263256bae1a5",
        "fact": "fact_30c4cea7799c3f37954c",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_0576d38cf10ec53c7dcb",
        "object_or_effect": "w_866fb61c6370c7b55c8a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_866fb61c6370c7b55c8a",
        "grounded": true
      },
      {
        "id": "fact_2e59cc5242e98140407d",
        "object_or_effect": "w_8d4f73123fc0a9419d26",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8d4f73123fc0a9419d26",
        "grounded": true
      },
      {
        "id": "fact_30c4cea7799c3f37954c",
        "object_or_effect": "o_3676ba7df8bdf9602d04",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_34ee1b0a81b3c509db5a",
        "object_or_effect": "o_c9d69d37eb15e759f5c0",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_7d6ba66fdead9c796616",
        "object_or_effect": "w_b09d86b8841afe1e63d3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b09d86b8841afe1e63d3",
        "grounded": true
      },
      {
        "id": "fact_83f20854f25f13c5387d",
        "object_or_effect": "o_eb7b56353021c8a4c9e8",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_aab4bef5316e8884d4c0",
        "object_or_effect": "w_745b297e1e1aa22def35",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_745b297e1e1aa22def35",
        "grounded": true
      },
      {
        "id": "fact_ad63ca7d1a51d4f4b117",
        "object_or_effect": "w_52aa91395caad205b9ca",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_52aa91395caad205b9ca",
        "grounded": true
      },
      {
        "id": "fact_b1c9074b4d39f6f70d49",
        "object_or_effect": "w_d2a2d83eaca2b62212d9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d2a2d83eaca2b62212d9",
        "grounded": true
      },
      {
        "id": "fact_e5189be666a09c270a5e",
        "object_or_effect": "o_84b3100fcfb142a55d30",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_e5451f91935604901e82",
        "object_or_effect": "w_bba15a83d537823c0e73",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_bba15a83d537823c0e73",
        "grounded": true
      },
      {
        "id": "fact_eb05d1c474426e14d20a",
        "object_or_effect": "o_95856e449010d6e0fb94",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 4,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 30,
      "external_dependency": 11,
      "source_task_reading": 7,
      "policy_missing": 1
    }
  }
}
```

## RQ1_9451d6dac4de

证据目录 run/members/RQ1_9451d6dac4de/attempt_1/，报告哈希 f94f483a2970fc1f13b3c54d02cd5bce4231f8b31ddaeaaad1edc8d935edc0e9

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,no_locatable_source,category_ambiguous_or_outside_supported_task",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": true,
    "paired_id": "RQ1_e25d32acc1f7",
    "state": "unsupported",
    "changes": {
      "v32": {
        "before": "alarm",
        "after": "unsupported"
      },
      "last1164": {
        "before": "not_detected",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "431f52e190cbd98e578546ea31f7611b950ae3876574081337cf38efa5b3aff3",
          "issue": "issue_b5243541b93f0d0c330e"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d1700e93c5aebfb28320b5485aca09fe30e8b74e901626b8418a3fcd5a6ec558",
          "issue": "issue_b5243541b93f0d0c330e"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "9141d5a4b5a853617874e31612fa9b1e60e4d47c2d491a43ea5e3d6040eefbf0",
          "issue": "issue_0c0272c5698d88478a5b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a842aeedc8e474c17b85035afebc999316d2d88a277d27aaba99e827b67b8db0",
          "issue": "issue_0c0272c5698d88478a5b"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "7b4357441eeaf5fa8d370ab8cfa8d53c752476d807c20e50333bc48a64f2a0b5",
          "issue": "issue_5eb48e7900b628a4e48b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d33308a66541b75fa84717cb2199fc82332d01e7ab8b8fdac499faa598245a8f",
          "issue": "issue_5eb48e7900b628a4e48b"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "0e1f7db4d5c3632349bfd234ae64932aac19bdfc1c2c5aae44b3d0b65f1d550e",
          "issue": "issue_2ad0fdc511f4525b9529"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ae0f162bca24ce96473e99c168362550297c7c4eea4d38fd43ca7d2950b648b6",
          "issue": "issue_2ad0fdc511f4525b9529"
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
          "detail_sha256": "7bae47e4bb22a5d623f95e53d41f3ad9356286ec70d5808148d45c78deed76e5",
          "issue": "issue_fa436b52f5cff8e3db57"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1f4a4f62a0b6848fc94ff98d70be6213fa50b088c078dade614141eab35ea5d9",
          "issue": "issue_fa436b52f5cff8e3db57"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "cce83e7a9dd099a222453b055e3001701aa4690c041831c7efc1a762c0b7069e",
          "issue": "issue_e459890e1b5dd7c8f55e"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "bb865656be72decafe694dd58ca548657ceca9c6f3b3811251e298d0dd72960f",
          "issue": "issue_7bc7d33bd41ded430d79"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c705e3289e805089d5464c54d6d9a47cdeeba50f274d9d9e1463f03e012fb91a",
          "issue": "issue_7bc7d33bd41ded430d79"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "31fa9ad459a8562e151d198aae27a583ceacee58364c02530adbab4800d5c927",
          "issue": "issue_745b85c6aea9b755d2ba"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "e0e5d4635843ad9893e5be12d8432afb0f9a62c033ca48db0cb5dc1638ba4448",
          "issue": "issue_745b85c6aea9b755d2ba"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_d227c6b271518b3c9902",
        "fact": "fact_99cb1b6fe29e37270b32",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_08cf10c2ae8101c681aa",
        "object_or_effect": "w_d926150e87c27f56aeaa",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d926150e87c27f56aeaa",
        "grounded": true
      },
      {
        "id": "fact_8dac8c8ed393d9e0f278",
        "object_or_effect": "w_09fc1bb60ae73c631bcc",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_09fc1bb60ae73c631bcc",
        "grounded": true
      },
      {
        "id": "fact_99cb1b6fe29e37270b32",
        "object_or_effect": "o_8a5882246de2118dd4e6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 8,
      "category_ambiguous_or_outside_supported_task": 7,
      "unknown_assessment_vocabulary": 8,
      "no_locatable_source": 8,
      "unbound_or_inapplicable_seed": 4
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 34,
      "source_task_reading": 1,
      "external_dependency": 10
    }
  }
}
```

## RQ1_947273fa2eef

证据目录 run/members/RQ1_947273fa2eef/attempt_1/，报告哈希 00e39a5f500147941d191e3671030851b8143186d395ce2e72f0692bdc42851a

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [
    "last1164 新增根因 D2:20:S1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_947273fa2eef",
        "reference": "D2:20:S1",
        "function": "selfdestructs",
        "v32": "TP",
        "last1164": "FN",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_84153239c8059e672825"
        ],
        "decision_only_findings": [
          "finding_df09bcbc711b0e290922"
        ],
        "current": "TP"
      }
    ],
    "findings": [
      {
        "idx": 16,
        "member": "RQ1_947273fa2eef",
        "finding": "finding_a0c14dde9c1846e03a32",
        "function": "selfdestructs()",
        "location": {
          "file": "units/program.sol",
          "start": 5342,
          "length": 74,
          "ast_id": 644
        },
        "result": "TP",
        "reference": "D2:20:S1",
        "group": "D2:20:S1",
        "source_excerpt": "function selfdestructs() payable public {\n    \t\tselfdestruct(owner);\n    }",
        "source_sha256": "5858aa841b01556733b6d06756cafe3a3e49090aeaeabd79d7f88b533eadce9e",
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
          "E3",
          "E7"
        ]
      },
      {
        "idx": 17,
        "member": "RQ1_947273fa2eef",
        "finding": "finding_1c0ea6b73399a23fb90e",
        "function": "fallback()",
        "location": {
          "file": "units/program.sol",
          "start": 5201,
          "length": 135,
          "ast_id": 636
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_947273fa2eef', 'units/program.sol', 5201)",
        "source_excerpt": "function () payable public {\n    \t\tuint amount = msg.value * buyPrice;               \n    \t\t_transfer(owner, msg.sender, amount);\n    }",
        "source_sha256": "5858aa841b01556733b6d06756cafe3a3e49090aeaeabd79d7f88b533eadce9e",
        "note": "实际报警入口或影响与作者参考不同，不能抵销该独立根因漏检。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 5201. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 5201,
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
          "E2",
          "E6"
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
          "D2:20:S1"
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
          "detail_sha256": "0bf540b48d73164d0d777bf679b45a04e5434b1eb8af29e57bd4feea15d755ef",
          "issue": "issue_12fc2dbda4aa8bd1806b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "0f151519b9110c703d9379be5413a773b77762e44ca82364f6833a5b39efb572",
          "issue": "issue_12fc2dbda4aa8bd1806b"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "351558aa9bf917678aa9d833480025963d30625a5f364f67a6e74ba8596646d4",
          "issue": "issue_bb41720467ced6a0c099"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "fde286076fa7ee44376c590fc15e1abc4bd66297786eec431a6d451f40225892",
          "issue": "issue_bb41720467ced6a0c099"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "daab32dbcb3e0f9dd865518810a4b958c9ae5184f8bbf706efbdec14333a2806",
          "issue": "issue_b8ec17a10e19f33844db"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "84f0f2a1e6d87eaadd1231ad57c21a61782b3f7cf8cdfb26214af96baf7f032a",
          "issue": "issue_b8ec17a10e19f33844db"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "826eca3625dd7432adff4ee6609b589dabb8468bcc2b5d008c21579b74d04373",
          "issue": "issue_f73f3763f0435e9921aa"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "83c22cc2635c7b810f1aa0d8935c916f1481fb5072c0683bf707dfad83163c77",
          "issue": "issue_f73f3763f0435e9921aa"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [
      4977
    ],
    "new": [],
    "disappeared_to_unknown": false,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_3271848e3fbc52d50cb7",
        "fact": "fact_7f0c1384bffcc30136ac",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_7f0c1384bffcc30136ac",
        "object_or_effect": "o_019026fc603f1aef1a25",
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
      "invalid_semantic_row": 8,
      "category_ambiguous_or_outside_supported_task": 4,
      "unknown_assessment_vocabulary": 4,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "source_task_reading": 16,
      "no_effect_in_scope": 17,
      "program_support": 2,
      "external_dependency": 3,
      "policy_missing": 1
    }
  }
}
```

## RQ1_94d9f2cfc77c

证据目录 run/members/RQ1_94d9f2cfc77c/attempt_1/，报告哈希 428b3f5befb032ee0d9be79e6234e7090bb3472cd82cb34810fb1b923f03aecd

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "not_detected",
    "FCR-MINT": "not_detected",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "not_detected",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "decision_only 未知转有效阴性"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": false,
    "paired_id": "RQ1_e13bb6580d65",
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
          "detail_sha256": "c2069420e62a8d129eb503ed8732d6938e830c1167a28212606e180009426cec",
          "issue": "issue_f7f9e784ab8f4682f0a5"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_a2d80af67f388aaf5d4a",
        "fact": "fact_6c998ec941ebaca1fdb8",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_6c998ec941ebaca1fdb8",
        "object_or_effect": "o_6588b630f05d8e03684d",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE",
      "FCR-MINT",
      "FCR-PAUSE",
      "FCR-TRANSFER"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 97,
      "source_task_reading": 32,
      "scope_missing": 1
    }
  }
}
```

## RQ1_96012699cf50

证据目录 run/members/RQ1_96012699cf50/attempt_1/，报告哈希 8ccbc3da085427c29acd54adb153b4f22ab41ce8a2f056050832007b33cffa29

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary",
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "bd2ef726f6bec6c651c83acf60a26fedb9ee044bceb8216e282eab5fbcd06b97"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "2e9d70fd202072f5ed992249b60036c32cc6306870c0e796cb62614b1c75f9dc",
          "issue": "issue_d9f738e9df8956b691c8"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "5b3fdf46e124f8b5cf73a59076117dce25d9ba86538a06b0922275e707cdba17",
          "issue": "issue_d9f738e9df8956b691c8"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "1a87552c84cb38fb6999d41a231103c450f9daf0f4a39cce86bc450340f880c4",
          "issue": "issue_ee13083fa7cc382ba4d2"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "52940e497e34a10f624cc1deb8a984b8d4fe0980b851853818c2f166e574308a",
          "issue": "issue_ee13083fa7cc382ba4d2"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "adfa3a01502f6bd7d979d2fc804d49310a0060db0f9c27f6276f2523808c7cb5",
          "issue": "issue_4897c99a5d99b6de47ad"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ca51f361cf0b083e498aacb44b90d4018166cd22b7159b3bdad97003899404dd",
          "issue": "issue_4897c99a5d99b6de47ad"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "4db220f29711f8c2d2e7a27a2dca0ad795864cf17a9823ec50db1003947d7aff",
          "issue": "issue_9af688f50759fadf9859"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a523529535bf8ab350a1947963fdefe537f41f52c83ccf943bb0a4888b915ab8",
          "issue": "issue_9af688f50759fadf9859"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "2ee721fc7ab63a1524da4d03f1fff1ea2037f58b1e6e81c892261ee4ffc85dfe",
          "issue": "issue_fd74ae751a9cb98b0b3c"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "81052cea2cfd55f1cd59dd8a146f824898ee2590b86bd79c700ef51ee47c2cda",
          "issue": "issue_fd74ae751a9cb98b0b3c"
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
        "support": "support_64d5ff845682f2b4251f",
        "fact": "fact_c884ae0c963e4c3dfd01",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_80088b760be31ab5a942",
        "fact": "fact_c884ae0c963e4c3dfd01",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_0f438d8ef18e01e1aa23",
        "object_or_effect": "w_cee071a4abfd03183660",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cee071a4abfd03183660",
        "grounded": true
      },
      {
        "id": "fact_1948cccafd5f85918d46",
        "object_or_effect": "w_a9e979bd0fe1e6886e84",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a9e979bd0fe1e6886e84",
        "grounded": true
      },
      {
        "id": "fact_2fef02eb0527661e7b02",
        "object_or_effect": "w_0ad205fc161f091578ac",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0ad205fc161f091578ac",
        "grounded": true
      },
      {
        "id": "fact_4a3a9fd927c459cd506f",
        "object_or_effect": "w_6ef8b1912de66886742b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6ef8b1912de66886742b",
        "grounded": true
      },
      {
        "id": "fact_5af0c265a2197458715d",
        "object_or_effect": "w_fcb53baaaf7e9035fe4e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_fcb53baaaf7e9035fe4e",
        "grounded": true
      },
      {
        "id": "fact_60ef3a0ba8bd3705516e",
        "object_or_effect": "w_22c13e6dc2f633a7dd30",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_22c13e6dc2f633a7dd30",
        "grounded": true
      },
      {
        "id": "fact_7596f8dfed7b22c378b6",
        "object_or_effect": "w_b981bf2573db8aa1a9e3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b981bf2573db8aa1a9e3",
        "grounded": true
      },
      {
        "id": "fact_7a40238c752426043df0",
        "object_or_effect": "w_cc7dbf2c8489fda14d98",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cc7dbf2c8489fda14d98",
        "grounded": true
      },
      {
        "id": "fact_86eca0e6b8060d1d950b",
        "object_or_effect": "w_a6c1b0bd1b8717a72461",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a6c1b0bd1b8717a72461",
        "grounded": true
      },
      {
        "id": "fact_87afef317e1bb22f400c",
        "object_or_effect": "w_24b57a1d573ef3994566",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_24b57a1d573ef3994566",
        "grounded": true
      },
      {
        "id": "fact_9c491eaa5d612d773443",
        "object_or_effect": "w_b905f5e8dd1288505670",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b905f5e8dd1288505670",
        "grounded": true
      },
      {
        "id": "fact_ae7159988bbcfd9f2781",
        "object_or_effect": "w_675441836854a5cf2da9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_675441836854a5cf2da9",
        "grounded": true
      },
      {
        "id": "fact_afd145adf19ba98dccd8",
        "object_or_effect": "w_d25003f8b8ea7d301e50",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d25003f8b8ea7d301e50",
        "grounded": true
      },
      {
        "id": "fact_b3e6f2e182c9be9153d3",
        "object_or_effect": "w_d60f6857fc2eb4163769",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d60f6857fc2eb4163769",
        "grounded": true
      },
      {
        "id": "fact_b85fd31bc7ab7f5d124e",
        "object_or_effect": "w_b2ef57cb0dc13f68da91",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b2ef57cb0dc13f68da91",
        "grounded": true
      },
      {
        "id": "fact_bca6add0d9fbdecccb44",
        "object_or_effect": "w_808bdba43eba9df70902",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_808bdba43eba9df70902",
        "grounded": true
      },
      {
        "id": "fact_c7a054749f1e516a6cf8",
        "object_or_effect": "w_0b1c5ae8091e367d49b4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0b1c5ae8091e367d49b4",
        "grounded": true
      },
      {
        "id": "fact_c884ae0c963e4c3dfd01",
        "object_or_effect": "o_55da584e27fd66d28d23",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_d3b885673585e692431d",
        "object_or_effect": "w_fb8e9408d3315102a6b8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_fb8e9408d3315102a6b8",
        "grounded": true
      },
      {
        "id": "fact_d4f6a944fa1681d57d0f",
        "object_or_effect": "w_e0d85bd84c9e14b3af61",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e0d85bd84c9e14b3af61",
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 4,
      "invalid_semantic_row": 5,
      "category_ambiguous_or_outside_supported_task": 5,
      "unknown_assessment_vocabulary": 5,
      "semantic_answer_outside_sent_scope": 2,
      "shared_declaration_in_distinct_applied_contexts": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 9
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 19,
      "policy_missing": 3,
      "external_dependency": 8,
      "source_task_reading": 1
    }
  }
}
```

## RQ1_980e04c92f4d

证据目录 run/members/RQ1_980e04c92f4d/attempt_1/，报告哈希 eadbc2442947f5215acd8525ca0bccea17548228db8e2795bc6afef950418631

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
    "target": "FCR-FREEZE",
    "positive": false,
    "paired_id": "RQ1_6a278772c4f3",
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
          "detail_sha256": "7f0e23ea5872499192f8fa61f4c97bd00cc3e89c842058930f00ebcfb357cfeb",
          "issue": "issue_b0e67e1a41d6a43147c9"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "65d77a221f553d53358a3819ef965dbf51128d8413254c1d8e3b367cef0ee2c0",
          "issue": "issue_b0e67e1a41d6a43147c9"
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
          "detail_sha256": "c487b4b7fd32af05400700fe04d85f645e72859e1db98e1021969a53cfa254f7",
          "issue": "issue_5308ccd945215d4e4dec"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "15bfb37e84a88ef3c371ab4cb93087f4b428b4c3f0cc25885fa18c5b50ebe0bb",
          "issue": "issue_5308ccd945215d4e4dec"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 10,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 2,
      "no_locatable_source": 1,
      "core_unresolved_retained_for_investigation": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 247,
      "model_phase_missing": 18
    }
  }
}
```
