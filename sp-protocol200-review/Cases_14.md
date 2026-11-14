# 逐例审阅

## RQ1_adf28b957352

证据目录 run/members/RQ1_adf28b957352/attempt_1/，报告哈希 b8a81673d4f9f1101b68b06c8fcaa1cf43eb97ccf086475e71d0e4c61f6e1758

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "alarm",
    "FCR-MINT": "unsupported",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "unsupported",
    "FCR-FREEZE": "alarm"
  },
  "changes": [
    "last1164 新增指定类命中",
    "prev200 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 action_slice_exhausted,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": true,
    "paired_id": "RQ1_a69a455c4a25",
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
        "before": "unsupported",
        "after": "alarm"
      },
      "decision_only": {
        "before": "alarm",
        "after": "alarm"
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
          "detail_sha256": "fb6b7ffc8d4f6d0c68808de310b1b09ff53a83bf84f4c4efdd75fcd6f3644c21",
          "issue": "issue_08288f71ea6108b5077b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "7dd9310031ee54cc3cc7d19122c201a372d19974c3985b1107fa8fddab855151",
          "issue": "issue_08288f71ea6108b5077b"
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
        "count": 4
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 42
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 47
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 10
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 46
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 3
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 8
      },
      {
        "label": "financial_consent_unresolved",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "same_request_amount_change",
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
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "action_slice_exhausted": 3,
      "program_investigation_budget_exhausted": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "scope_missing": 2,
      "no_effect_in_scope": 124,
      "source_task_reading": 41,
      "program_support": 2,
      "external_dependency": 6
    }
  }
}
```

## RQ1_ae0fe8386d33

证据目录 run/members/RQ1_ae0fe8386d33/attempt_1/，报告哈希 39a2207e8bf10a50ddc2ee4f34f9207eab41dd72a78eb6e7b30697b44b1fb13c

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:224:author:1",
    "last1164 丢失根因 D2:224:author:1",
    "prev200 丢失根因 D2:224:author:1",
    "decision_only 丢失根因 D2:224:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,unknown_assessment_vocabulary,no_locatable_source",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_ae0fe8386d33",
        "reference": "D2:224:author:1",
        "function": "LittleCactus",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_fd07ad8b6991f3acb772"
        ],
        "decision_only_findings": [
          "finding_70605449635ee4fde6c6"
        ],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:224:author:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:224:author:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:224:author:1"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:224:author:1"
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "91478c5b2f3272fa28d306a5f0eb46939771351188491c382800d9adfc063103",
          "issue": "issue_a51aa4d01ffee81f6189"
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
      "invalid_semantic_row": 8,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 2,
      "no_locatable_source": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "model_phase_missing": 2,
      "no_effect_in_scope": 5,
      "external_dependency": 2
    }
  }
}
```

## RQ1_af7c473b8cca

证据目录 run/members/RQ1_af7c473b8cca/attempt_1/，报告哈希 965524a5575d9f65e461bfda2c7af3de42a4e260879917186415c487958fe023

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
  "changes": [
    "decision_only 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,action_slice_exhausted,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": true,
    "paired_id": "RQ1_4be3030c4533",
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "3e7fa87176cfe502a18032a71e51c370af5daba9e41823bd3e38d457c96859ac"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "898a9ddc28dfc6acb34314188eacecac7d514dc1ac8ccfc3cff70a968ae72e5e",
          "issue": "issue_f617b20bf94eade96c06"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1685dccc282dc2a10c107245b5d2bce614b8411b500b6a1714ba663c60e43c92",
          "issue": "issue_262dee494b86220f09e0"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "3abcc59054f26c7475c85c568e51a9dc59004c23258b372f255c91c9dd54209b",
          "issue": "issue_48c8cec360e4ec756bb1"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "8c82ce51ae47750c80cd9b2464311278ec5e0460b3d53aec435f7b0f84dad1fd",
          "issue": "issue_48c8cec360e4ec756bb1"
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
          "detail_sha256": "e9395a34a23246a6b0a2a5654fb99c4d679d9ea5d6914f7d9fc91fe43adb32f8",
          "issue": "issue_1276d0ba9ae98068e6cd"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "819d27414c3a64422add1f8d1402715b6eefb462b666c4ff6998e70e2369b174",
          "issue": "issue_1276d0ba9ae98068e6cd"
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
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 9
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 7
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 18
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 40
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 10
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 43
      },
      {
        "label": "same_request_amount_change",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 9,
      "unknown_assessment_vocabulary": 3,
      "category_ambiguous_or_outside_supported_task": 2,
      "semantic_answer_outside_sent_scope": 1,
      "action_slice_exhausted": 5,
      "program_investigation_budget_exhausted": 1,
      "program_investigation_seconds": 2,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1
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
      "source_task_reading": 40,
      "no_debit_in_scope": 2,
      "new_entitlement": 1,
      "external_dependency": 6,
      "program_support": 1
    }
  }
}
```

## RQ1_afa801e14aca

证据目录 run/members/RQ1_afa801e14aca/attempt_1/，报告哈希 e15c3ac3a877771110ad9bd1bcc75e52955bf8037d95e94e17e15c01012e4959

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_afa801e14aca",
        "reference": "D2:393:author:1",
        "function": "QMQCoin",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_b5e5d8e6516561ce02e9"
        ],
        "decision_only_findings": [
          "finding_ccf16bac42a356341a98"
        ],
        "current": "TP"
      }
    ],
    "findings": [
      {
        "idx": 20,
        "member": "RQ1_afa801e14aca",
        "finding": "finding_a4957ac6c3ca03b38333",
        "function": "QMQCoin()",
        "location": {
          "file": "units/program.sol",
          "start": 2806,
          "length": 126,
          "ast_id": 330
        },
        "result": "TP",
        "reference": "D2:393:author:1",
        "group": "D2:393:author:1",
        "source_excerpt": "function QMQCoin () public {\n        owner = msg.sender;\n        value = 5000e8;\n        distr(owner, totalDistributed);\n    }",
        "source_sha256": "f3f6801bd64368d43cccc4ebd3af093530f1598c7a7b5c1218daa3c42eba75a6",
        "note": "实际入口及源码效果与作者独立根因对应，保留程序证据可审计性限制。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 2806. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 2806,
              "length": 126,
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
          "detail_sha256": "f773c4d803450106ee7e16b6a5c6e399c02292fee554be37526009f04550a260",
          "issue": "issue_1e5571fb5c0e22c1fd76"
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
        "label": "direct_callback_influence",
        "answer": "sat",
        "count": 26
      },
      {
        "label": "callback_influence",
        "answer": "sat",
        "count": 26
      },
      {
        "label": "direct_callback_influence",
        "answer": "unsat",
        "count": 8
      },
      {
        "label": "callback_influence",
        "answer": "unsat",
        "count": 8
      },
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 15
      },
      {
        "label": "authorization_violation",
        "answer": "sat",
        "count": 9
      },
      {
        "label": "authorization_violation",
        "answer": "unsat",
        "count": 6
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 7,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 11,
      "source_task_reading": 9,
      "program_support": 1,
      "external_dependency": 8
    }
  }
}
```

## RQ1_afb609e0053e

证据目录 run/members/RQ1_afb609e0053e/attempt_1/，报告哈希 3081327b3b2dfb365eab9c7fbd930df7d29015bee02a2e65abc2d425912145cc

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
    "last1164 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": true,
    "paired_id": "RQ1_7405f0959142",
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "23a6538a9ed5b2f61822e0e7b5063a3598a192d13fc88c7a9ac1328ad4db6f82"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "dc70afa18624ea26813572043ded8bb180a30539620b4f429594479e7b97744c",
          "issue": "issue_455cdcf18302c7c5b503"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "94790419f65a4430d6df6adb6fc7a78952e688ac8f3d6efadf0aff1d05257e0c",
          "issue": "issue_455cdcf18302c7c5b503"
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "160f96cb34480203705ba2e0068eeddeda2953f787cce86bc71d583e0cd3af94",
          "issue": "issue_64319f05f4b52a1f5def"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "026e17f50dc46659ba52ecb7a2b278b6161bee982757ebc4502c12511549bf6b",
          "issue": "issue_64319f05f4b52a1f5def"
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
        "count": 4
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 3
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 8,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 2,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 43,
      "scope_missing": 1,
      "external_dependency": 5,
      "source_task_reading": 1
    }
  }
}
```

## RQ1_b0a696b11b0a

证据目录 run/members/RQ1_b0a696b11b0a/attempt_1/，报告哈希 e305d209c29234a4cbc4412c1c96b51f2653e1ed1a992c9c5858f19323473429

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unrelated_or_secondary_graph_pairs_deferred,semantic_answer_outside_sent_scope,unbound_or_inapplicable_seed"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": false,
    "paired_id": "RQ1_4f9f1ce04ed8",
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
  "mechanism": {
    "supports": [
      {
        "support": "support_49124b144e5fd1dad05b",
        "fact": "fact_3c828ebeb5fb53ab0766",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_7f60994a32fe3de1a500",
        "fact": "fact_f875c73d44803f770f99",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_3c828ebeb5fb53ab0766",
        "object_or_effect": "o_024dd17a9c3ad1a3fbbc",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_b13152e3c2b744a0c2a4",
        "object_or_effect": "w_b5d7765ed2649982ed8e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b5d7765ed2649982ed8e",
        "grounded": true
      },
      {
        "id": "fact_f875c73d44803f770f99",
        "object_or_effect": "o_37ea148939eb98550c1b",
        "meaning": "eligibility_state",
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
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 6,
      "semantic_answer_outside_sent_scope": 2,
      "unbound_or_inapplicable_seed": 2,
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
      "no_effect_in_scope": 40
    }
  }
}
```

## RQ1_b11b4b1e0dc3

证据目录 run/members/RQ1_b11b4b1e0dc3/attempt_1/，报告哈希 50982f341789584c25d4a0ef068528207bb373594991b1507bdbef6c1f1acb8f

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 semantic_answer_outside_sent_scope,unbound_or_inapplicable_seed,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task",
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
          "detail_sha256": "97e17666ca2d548a75bfc945059329652ced5b4aeb0e7650426d558be6bb8330",
          "issue": "issue_f7803992a25fa9b79417"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1aa75e7fb3b1d6380283f58187628534ff80ba76d25583f8c32cc434963ee69a",
          "issue": "issue_f7803992a25fa9b79417"
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
          "detail_sha256": "487e666cc9fd72e18c91f88e52725b804487462bcdca3c717741390a7b218369",
          "issue": "issue_33d22e3bc122ff98e5d3"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [
      3531,
      3618
    ],
    "new": [],
    "disappeared_to_unknown": true,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_1af5d74fb9d08edf1914",
        "fact": "fact_e4667ce8aba2da50f12f",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_e4667ce8aba2da50f12f",
        "object_or_effect": "o_05b73b0f61ee9de4ccd3",
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
        "answer": "sat",
        "count": 2
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 3,
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
      "no_effect_in_scope": 11,
      "source_task_reading": 3,
      "external_dependency": 2,
      "policy_missing": 1,
      "unassessed_role_change": 1
    }
  }
}
```

## RQ1_b2a2fc36e6b8

证据目录 run/members/RQ1_b2a2fc36e6b8/attempt_1/，报告哈希 1f3a19035178866acd08625d5b75020042d2453b9c5a83d0afa024624e48ff2e

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed,invalid_semantic_row,semantic_answer_outside_sent_scope",
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
        "support": "support_6fc5c56c5acac20f58ff",
        "fact": "fact_9a89e72d431291b440c1",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_7857eac6a92107d5f0c4",
        "fact": "fact_8b7c01680b7147fa8886",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_8b7c01680b7147fa8886",
        "object_or_effect": "o_1500d461942e6d8702d9",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_9a89e72d431291b440c1",
        "object_or_effect": "o_0fdf51d35cb93efb9bc5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_cb18cf663edb8c2360b9",
        "object_or_effect": "w_5093d02cefc569d1ecfb",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5093d02cefc569d1ecfb",
        "grounded": true
      },
      {
        "id": "fact_e1d7770e82d01d4e2b84",
        "object_or_effect": "w_d7977526d028c709b647",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d7977526d028c709b647",
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
        "answer": "sat",
        "count": 2
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 3,
      "invalid_semantic_row": 3,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 4
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 7,
      "source_task_reading": 3,
      "policy_missing": 2,
      "external_dependency": 3
    }
  }
}
```

## RQ1_b4fca92c3262

证据目录 run/members/RQ1_b4fca92c3262/attempt_1/，报告哈希 776351170b3df803c9e0927f2bf2552375e32ad8a8339f191d886e6664c723ec

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:97:S1",
    "last1164 丢失根因 D2:97:S1,D2:97:S2",
    "prev200 丢失根因 D2:97:S1,D2:97:S2",
    "decision_only 丢失根因 D2:97:S1,D2:97:S2"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,unknown_assessment_vocabulary,no_locatable_source",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_b4fca92c3262",
        "reference": "D2:97:S1",
        "function": "owned",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_3c9789b3b3313951e558"
        ],
        "decision_only_findings": [
          "finding_76f369ad0c038db70b35"
        ],
        "current": "FN"
      },
      {
        "member": "RQ1_b4fca92c3262",
        "reference": "D2:97:S2",
        "function": "STARTMETADOLLAR",
        "v32": "FN",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_2627e4becfabadc778ca"
        ],
        "decision_only_findings": [
          "finding_4e62dd50b374eac916e8"
        ],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:97:S1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:97:S1",
          "D2:97:S2"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:97:S1",
          "D2:97:S2"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:97:S1",
          "D2:97:S2"
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
          "detail_sha256": "fc760a6cc6a21ac13293c682b937f7f2808b77f0c83d4219187bd8034104e8b3",
          "issue": "issue_deb3c2f8be53d5270010"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [
      9465
    ],
    "new": [],
    "disappeared_to_unknown": true,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 10,
      "semantic_answer_outside_sent_scope": 2,
      "unknown_assessment_vocabulary": 1,
      "no_locatable_source": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 27,
      "model_phase_missing": 18,
      "external_dependency": 3
    }
  }
}
```

## RQ1_b5217318672e

证据目录 run/members/RQ1_b5217318672e/attempt_1/，报告哈希 8f439eeba37daa8edb7c8d9703da51ae9923a2495f95b6a534f82971c986aeb6

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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,invalid_semantic_row",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": true,
    "paired_id": "RQ1_72c6b8c6b605",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "4cc4620765f52f9777ae5c953d72e729c2b4cbd93f5cee107e9f57a1d5f29517",
          "issue": "issue_17689d8861c69fc61841"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "066b35795ca8e3cce810a5b7ffe2cb18a0305887fa275178d6cc3b80082e1ba0",
          "issue": "issue_17689d8861c69fc61841"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "4b1b4be00e29889c5733b66c6f4120201239fa0b60486254f95b2f6e4b12117b",
          "issue": "issue_18575f14863d2304f1cd"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "98fbba587cd0b31ecc41bbdf93a3de1d7148ec5729f4dc12257c1d14a44e28b3",
          "issue": "issue_18575f14863d2304f1cd"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "fc2f72dc072b013c30098e26f6b22d47b75ff980396a4f47149509a601277a7c",
          "issue": "issue_4d5c9d79c69e9960a5e2"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1ce450f6e595637fa094eb29b3b9efee027ded969074a4771246f93b9f785096",
          "issue": "issue_4d5c9d79c69e9960a5e2"
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
          "detail_sha256": "ee7c06caf061b7bdf529ddb0eb57750f27e624ed92990ff94ff8556d0dc24561",
          "issue": "issue_18c7b930dc0287e1dcb9"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "faef3a7d867e54053539699490c3d5b2e013f55c704eba83f2235cc3cba9c886",
          "issue": "issue_18c7b930dc0287e1dcb9"
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
      "unbound_or_inapplicable_seed": 6,
      "category_ambiguous_or_outside_supported_task": 4,
      "unknown_assessment_vocabulary": 3,
      "invalid_semantic_row": 2,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "semantic_answer_outside_sent_scope": 1,
      "revision_outside_actual_feedback_scope": 1
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
