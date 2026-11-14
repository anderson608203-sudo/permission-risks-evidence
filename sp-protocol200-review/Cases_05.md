# 逐例审阅

## RQ1_3455b6a9ba4f

证据目录 run/members/RQ1_3455b6a9ba4f/attempt_1/，报告哈希 94fc6153350d8f401469cc1d67400d1f4419a95dc9b702f07b8fa5d19e841f99

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,no_locatable_source",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": false,
    "paired_id": "RQ1_0c666ce785e8",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1345b4138ee79c68e48811c766529450bd43f5edad9497ab85e451e381b7f6a0",
          "issue": "issue_48674546a6c06ff86846"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "f354431bc7026082eb9a0ae48faf54f92dd21185ea829ccf63e79182651d3771",
          "issue": "issue_1f83197991f45283bc00"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "23d4c3ba2ac2342f3462788be71ace5fcbcf64639949437993e3e39145dbae09",
          "issue": "issue_1f83197991f45283bc00"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "3496425ee50c0657b1ec6ceeae6d95e95afce04f07b5b9c46273d767222a6044",
          "issue": "issue_e984756f280e48c052d9"
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "5a73f7b65b41c272061cb65046732185694387b804cc613b3f466320c90fc2e8",
          "issue": "issue_b64d3b0004757d80c74e"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "66d631cdd387fe7b92b17bd2059ad1bfbe1993253c158f9676e97f46ef03a894",
          "issue": "issue_dde8a5ec2af3c33ddf71"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "6e4aaf3699ab2024c0732fcebdd5a04d3e1a3463768ba04f89aa9f5e40b58837",
          "issue": "issue_dde8a5ec2af3c33ddf71"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "a76feaac87f462f62e563f9f0e825d5b1e2a8fbf7eb1e428ef502b35ef5fc478",
          "issue": "issue_f3c8819014f61a5498fb"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "9f54ac5f6071bf226072dd7e764948cec9402ba9740880498c8388173811a74a",
          "issue": "issue_f3c8819014f61a5498fb"
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
      "invalid_semantic_row": 6,
      "unknown_assessment_vocabulary": 6,
      "category_ambiguous_or_outside_supported_task": 3,
      "no_locatable_source": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 34,
      "source_check_excluded": 1,
      "external_dependency": 10
    }
  }
}
```

## RQ1_34ab8e0115aa

证据目录 run/members/RQ1_34ab8e0115aa/attempt_1/，报告哈希 29d610f06d16a5820c69f2931d13a324b973152f9d22cf2c572c1dfa15a1c9e8

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:359:S2",
    "last1164 丢失根因 D2:359:S1,D2:359:S2",
    "prev200 丢失根因 D2:359:S1,D2:359:S2",
    "decision_only 丢失根因 D2:359:S2"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_34ab8e0115aa",
        "reference": "D2:359:S1",
        "function": "PonziTokenV3",
        "v32": "FN",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "FN",
        "prev200_findings": [
          "finding_bd7d7d8f643020010af2"
        ],
        "decision_only_findings": [],
        "current": "FN"
      },
      {
        "member": "RQ1_34ab8e0115aa",
        "reference": "D2:359:S2",
        "function": "destroy",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_12c404df2478348ab521"
        ],
        "decision_only_findings": [
          "finding_04969ba51a757e3588e8"
        ],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:359:S2"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:359:S1",
          "D2:359:S2"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:359:S1",
          "D2:359:S2"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:359:S2"
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
          "detail_sha256": "32bac5b03050321e057de04365dc2a512561a740452e71312c38d517446ea0c1"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "5aa111c1afd10848a5e52c802f9c8ce386f0bf8c5885aaaf63b3283f2666f124"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "2d79424d3d8ea7495c1f18954a91a36b236ae70557a460d0c2471aec8d4f066b",
          "issue": "issue_fba2d6a4560854dd3e63"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "3d6c06f753bf474be631b4c2dbe73ba24c91cd73afa868e08df18849d3f227fc",
          "issue": "issue_fba2d6a4560854dd3e63"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "6f8c80c5c3f27943436bc7a68f9992d7882fa226d4506d6c2af9f38e97d2ff22",
          "issue": "issue_56601258144b7c435edd"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "75683728a1e6adea0ec134ffa851785464ffc74fe6e9008346c2ae9365036802",
          "issue": "issue_56601258144b7c435edd"
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
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "8206f5ce91d4ac3e73b56f9ec24416e07c3acfcdcaabc61418fe2e2b315fa472",
          "issue": "issue_d798eff572a97ae55c6d"
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
      "invalid_semantic_row": 6,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "no_locatable_source": 1,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "changed_property_requires_scoped_evidence": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 9,
      "source_task_reading": 4,
      "source_context_missing": 6,
      "external_dependency": 4,
      "policy_missing": 1
    }
  }
}
```

## RQ1_353a9b0b5006

证据目录 run/members/RQ1_353a9b0b5006/attempt_1/，报告哈希 418f1867b7d5a0a8a11ab20a5d065bd57d9255aa6232ef27226bfda3dd34a5e6

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
    "已确认消费/覆盖诊断 unknown_assessment_vocabulary,invalid_semantic_row,category_ambiguous_or_outside_supported_task,financial_consent_meaning_unresolved",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": true,
    "paired_id": "RQ1_db11e3e08742",
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
          "detail_sha256": "94a2df8792fe6829794d0c9243706575f030468fffde8814299fe6a7d4088f6c",
          "issue": "issue_08cf16a38d4c574a9b2b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "0eb39a936a1dcfa38262999aa503d1cd95c7db70b6ef1e91f037130ac42f804c",
          "issue": "issue_08cf16a38d4c574a9b2b"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "27e1b42dbb41b2e70534c4f40775064fdfb1e5e2325e41d31aaddb3ca0672f1f",
          "issue": "issue_16bcda07977fa91d5c93"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "0d074db45bb46e1c725cfcc9a1fe8001889827f8acd8a0499b4f32f08f5c41f0",
          "issue": "issue_16bcda07977fa91d5c93"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "3fb30226da361dec94d34e2e093dc65c1d9f6714c2f0ab706a5c2ed347f9884e",
          "issue": "issue_b8921d8eec35605ac998"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ae82cec028a7c149d786f98a65af4d65a4c31270eca0cc4995960c98ac1ffd93",
          "issue": "issue_b8921d8eec35605ac998"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "fc24946fc4eb3da9a5a666047bc3991142987428ef3d4d01ff0b40b4eab0d141",
          "issue": "issue_3c1745cf0117c5bde4d3"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "939b0aa44af9a766b6e9c3614778ff4f095d437c76e53f53e119af85e9c07b0f",
          "issue": "issue_3c1745cf0117c5bde4d3"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "a6fe6273b3f411fa01a0b3017a8f91fc9856f2a7660f16f673fd2b475114d7e4",
          "issue": "issue_cd39455091464307e26a"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "3fd95fb319a1ed5e958b6c1f66d6bddfa5c1ecf89e692641a3662fe0005d50c5",
          "issue": "issue_cd39455091464307e26a"
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
          "detail_sha256": "7a294074b7db9358f673cdd2074009e83424bbe7a7a50086f6e7d64839472bf5",
          "issue": "issue_4ce086542fb4e26464fa"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_8c75d0d7d5cfecd84f49",
        "fact": "fact_b3cb73056f18babc3e4a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_bd5a44c425d8d4a87227",
        "fact": "fact_b3cb73056f18babc3e4a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_bf3ba78c6f0cf6d8c1de",
        "fact": "fact_94b672c68be2b2754af8",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_94b672c68be2b2754af8",
        "object_or_effect": "o_4ea2745111cdfc8d9689",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_b3cb73056f18babc3e4a",
        "object_or_effect": "o_427aac5a7f8ea5322db6",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "prefix_reachability",
        "answer": "unsat",
        "count": 85
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 11
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 14
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 36
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 33
      },
      {
        "label": "control_transition_preservation",
        "answer": "unsat",
        "count": 3
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 10
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "financial_consent_unresolved",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "same_request_amount_change",
        "answer": "sat",
        "count": 3
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 5,
      "category_ambiguous_or_outside_supported_task": 5,
      "unknown_assessment_vocabulary": 6,
      "semantic_answer_outside_sent_scope": 1,
      "no_locatable_source": 2,
      "action_slice_exhausted": 2,
      "yield_to_source_bound_semantic_review": 2,
      "unbound_or_inapplicable_seed": 1,
      "financial_consent_meaning_unresolved": 4,
      "revision_outside_actual_feedback_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 1,
      "program_investigation_budget_exhausted": 1,
      "program_investigation_seconds": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 126,
      "scope_missing": 13,
      "source_task_reading": 19,
      "no_debit_in_scope": 2
    }
  }
}
```

## RQ1_35e0e8d95f92

证据目录 run/members/RQ1_35e0e8d95f92/attempt_1/，报告哈希 9241f9cd1cf4a50523a1e803c935a827e4e3016f0e3e20e8e3211a05051eb6ac

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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,action_slice_exhausted,category_ambiguous_or_outside_supported_task",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": false,
    "paired_id": "RQ1_c75d73e1c482",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "cdb96d28d09ce0b12408cb09dd80ce8a7bee4c317d3b08dd7b41974fe2e2313f",
          "issue": "issue_37a8ef0046902d57910e"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "017232ef1b79f62ffd0a2896c4f4eec1e13d2c1c32e883553d8fe10ca6615709",
          "issue": "issue_a5446580e5f137fed7ed"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "e605c54d104a232ffbad10eafb18d272a4304d518b7ab99093bbe1aeddf81611",
          "issue": "issue_d96e99ae528057df7410"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "9a93cbca13521926c6ec9003ab14d84e0d20f98d8d181971c816d2ea9a4ccd1e",
          "issue": "issue_d96e99ae528057df7410"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "ace9fb2dc49cf36323832b89167aac3a4b3ceff4bca6d6c99d3891f54ab8a988",
          "issue": "issue_5627e719a0981c9b4ab0"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "86abc4ae620ef2a1c2b48d88ecef4b9e8456be038b42cae6c7865ed61e9cdaea",
          "issue": "issue_5627e719a0981c9b4ab0"
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
        "support": "support_2cd03281b42c20fd1982",
        "fact": "fact_626c603aae3aa29d9a87",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_854c311f835dd9aef1f4",
        "fact": "fact_725bdb672ea78006eb04",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_d99910f0e2d008affb62",
        "fact": "fact_c04a350384505527954a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_626c603aae3aa29d9a87",
        "object_or_effect": "o_26d6eae0270ddc247c4d",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_725bdb672ea78006eb04",
        "object_or_effect": "o_9a59aaec6139892141d8",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_c04a350384505527954a",
        "object_or_effect": "o_01b0947d9af42a9e5a56",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_d9e2df2bc8f1aa86c133",
        "object_or_effect": "w_66bfe1b211f004b306a1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_66bfe1b211f004b306a1",
        "grounded": true
      }
    ],
    "query_summary": [
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
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 26
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 49
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 50
      },
      {
        "label": "same_request_amount_change",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 8
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
        "label": "financial_block",
        "answer": "unknown",
        "count": 7
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
      "unbound_or_inapplicable_seed": 6,
      "unknown_assessment_vocabulary": 4,
      "category_ambiguous_or_outside_supported_task": 2,
      "semantic_answer_outside_sent_scope": 2,
      "shared_declaration_in_distinct_applied_contexts": 1,
      "action_slice_exhausted": 3,
      "program_investigation_seconds": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 141,
      "source_task_reading": 35,
      "covered_holder_grant": 3,
      "external_dependency": 6,
      "scope_missing": 3,
      "program_support": 1,
      "parameter_only": 1
    }
  }
}
```

## RQ1_35f857af5c9e

证据目录 run/members/RQ1_35f857af5c9e/attempt_1/，报告哈希 c117cd4a859e48e788376a532c4a81d237ef85ebf7789d1659a91d2944cf31ed

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
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": false,
    "paired_id": "RQ1_cda3df36df22",
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
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 9,
      "semantic_answer_outside_sent_scope": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 50,
      "model_phase_missing": 15
    }
  }
}
```

## RQ1_37d9daf031da

证据目录 run/members/RQ1_37d9daf031da/attempt_1/，报告哈希 fe7b71bc3398062b97da096124e70aafe377ed85b8e4b3a0395d69ab6dcc4d6d

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": true,
    "paired_id": "RQ1_1c6b43b24d4c",
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
          "detail_sha256": "2870d110e23bd2032fd4a6415d30257ba22d473b46c99acccaadfb72b7b721ef",
          "issue": "issue_dc2448e46666122e702f"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "2a70072e1b01281c24e68714c37bca6c810abf3ccbf4fd0d882882d840237268",
          "issue": "issue_dc2448e46666122e702f"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "4d965cfca075002b29d5cf9fd71291b4803f7f89c0bc4ebb2fe24588120ad7e6",
          "issue": "issue_3384821912e10de8c447"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "2586858ece8a79814a6877cf4ba4849ca8add8f0fe9842215a1ec08c81b84022",
          "issue": "issue_5997bdc193beb9d5653e"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_20df6978ce509db365bb",
        "fact": "fact_927b9b0903a2763e8062",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_927b9b0903a2763e8062",
        "object_or_effect": "o_c2b0bdd098b38e386f66",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "direct_callback_influence",
        "answer": "unsat",
        "count": 109
      },
      {
        "label": "callback_influence",
        "answer": "unsat",
        "count": 109
      },
      {
        "label": "direct_callback_influence",
        "answer": "sat",
        "count": 60
      },
      {
        "label": "callback_influence",
        "answer": "sat",
        "count": 60
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 5,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 1,
      "program_investigation_budget_exhausted": 1,
      "program_investigation_seconds": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 448,
      "external_dependency": 49,
      "source_task_reading": 33
    }
  }
}
```

## RQ1_39fb6e7197c4

证据目录 run/members/RQ1_39fb6e7197c4/attempt_1/，报告哈希 c34afe8ef1b31f957a525db79423688c3259028ee4cfa8e0d00036654012f959

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope,unrelated_or_secondary_graph_pairs_deferred",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": true,
    "paired_id": "RQ1_7450d39da940",
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "23a6538a9ed5b2f61822e0e7b5063a3598a192d13fc88c7a9ac1328ad4db6f82"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c03ae07492b134610d07ad31a37d64fd91c1d41c2c07d117b70cce2be7a75921",
          "issue": "issue_1efe80652a389c7dddb8"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f7979a44d076f50838022cfca4e85e3d8b299de2ce1f9b64fc33542fe703f574",
          "issue": "issue_eee770c6a6cb36c62759"
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
          "reason": "ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "a7dfb650d337b53c093463a3fb90e798209e8f04761c2d5d148e24a85d771188",
          "issue": "issue_d147137e13bcdd06e3e2"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_2d9773aca8c6c69d36a1",
        "fact": "fact_b3e387decf2b0e0e998c",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_b3e387decf2b0e0e998c",
        "object_or_effect": "o_ccacdd94b6ff05526727",
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
      "invalid_semantic_row": 8,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 2,
      "core_unresolved_retained_for_investigation": 1,
      "ambiguous_confirmation_not_a_risk_judgment": 1,
      "revision_outside_actual_feedback_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 125,
      "external_dependency": 30
    }
  }
}
```

## RQ1_3a3d833ca142

证据目录 run/members/RQ1_3a3d833ca142/attempt_1/，报告哈希 04c0c7f7815e4001e785c0e8a5c70795cc38236f849169f17a741579679cb4d4

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "alarm",
    "FCR-MINT": "not_detected",
    "FCR-DESTROY": "not_detected",
    "FCR-PAUSE": "not_detected",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "last1164 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,revision_outside_actual_feedback_scope"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": true,
    "paired_id": "RQ1_206d19a8539c",
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
          "detail_sha256": "fd229be18bcff9dba6a0a39380c27cd77b37f8c56f028332e7540c740a4493cc",
          "issue": "issue_ec5ef433e9521cce806b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "129fcea0aad3164756fee040b789d99513b3f419160410379a6f9f0bf29c62b0",
          "issue": "issue_ec5ef433e9521cce806b"
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
          "detail_sha256": "f895fba7bcbd1f0b09abf8cf7415856b76bee740c7ab2806f77188686ae79bf0",
          "issue": "issue_d1da204cc58bfe431cd0"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "361d5b4c1d110edbd1a55b96f625e45d3d760bd891119beb06719294269c6a46",
          "issue": "issue_d1da204cc58bfe431cd0"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_02d2e07e04897345df53",
        "fact": "fact_49fd4e2bf0d1502e5857",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_545a3bb143f476f57e63",
        "fact": "fact_4759cb2d4e50c12ceaab",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_9547f1eda893dfda6476",
        "fact": "fact_49fd4e2bf0d1502e5857",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_a1750b3b11c64b4b7339",
        "fact": "fact_c8686ffc9b13f613a600",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_1f225ba1e4123a210526",
        "object_or_effect": "w_57d92a68933cb6acf5ff",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_57d92a68933cb6acf5ff",
        "grounded": true
      },
      {
        "id": "fact_4759cb2d4e50c12ceaab",
        "object_or_effect": "o_097df1ec14924603cc2e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_49fd4e2bf0d1502e5857",
        "object_or_effect": "o_d08a391adff3299bdae2",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_c8686ffc9b13f613a600",
        "object_or_effect": "o_ac7781148fa72d6d3569",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_d800b36b6ee23de1176b",
        "object_or_effect": "w_d84e4181991ecd4bf27a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d84e4181991ecd4bf27a",
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
        "label": "direct_effect",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "direct_effect",
        "answer": "unsat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 3,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 2,
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
      "no_effect_in_scope": 18,
      "program_support": 1,
      "scoped_counter": 1
    }
  }
}
```

## RQ1_3b4d9f6eb96f

证据目录 run/members/RQ1_3b4d9f6eb96f/attempt_1/，报告哈希 9aec5ad8114fea785f49061c5ce4559974a4c1028abc63f348294ef330961514

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
    "已确认消费/覆盖诊断 action_slice_exhausted,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": false,
    "paired_id": "RQ1_0267e2a8ebb2",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "9d157bba022b014b419c4df09ec53ded781500984643df6dc358184c40b16996",
          "issue": "issue_0c6aa20c9e4a3f7767d2"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [
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
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 25
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 41
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 46
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 2
      },
      {
        "label": "financial_block",
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
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "action_slice_exhausted": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "scope_missing": 2,
      "no_effect_in_scope": 126,
      "source_task_reading": 39,
      "program_support": 1,
      "external_dependency": 6,
      "parameter_only": 1
    }
  }
}
```

## RQ1_3b975bee1104

证据目录 run/members/RQ1_3b975bee1104/attempt_1/，报告哈希 98ccfe595f747137b6fb58ae307a831f26b6e513da8360a836061a3649df8f55

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "last1164 丢失根因 D2:44:author:1",
    "prev200 丢失根因 D2:44:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_3b975bee1104",
        "reference": "D2:44:author:1",
        "function": "TokenERC20",
        "v32": "FN",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "FN",
        "prev200_findings": [
          "finding_78c8ab3b687b0790dfc6"
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
        "lost": [
          "D2:44:author:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:44:author:1"
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
        "support": "support_207abb5bbebd950cd646",
        "fact": "fact_13180f75ff66c47f1049",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_c703e17777158045c013",
        "fact": "fact_706f00d22404d046a2aa",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_02d3f3bf921d955fd402",
        "object_or_effect": "w_d944d6c226b6759e92a8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d944d6c226b6759e92a8",
        "grounded": true
      },
      {
        "id": "fact_13180f75ff66c47f1049",
        "object_or_effect": "o_c83504604dc62d6f09ed",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_167062e070edada406d2",
        "object_or_effect": "w_36749388cc436d671e05",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_36749388cc436d671e05",
        "grounded": true
      },
      {
        "id": "fact_28db24441efeb3faadd9",
        "object_or_effect": "w_a56bea49be1af4ba5151",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a56bea49be1af4ba5151",
        "grounded": true
      },
      {
        "id": "fact_40bf5b102a2fadfad682",
        "object_or_effect": "w_696f0216c9c49a933833",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_696f0216c9c49a933833",
        "grounded": true
      },
      {
        "id": "fact_4114a46037699a917381",
        "object_or_effect": "w_e7eb5b874913dd41f0bf",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e7eb5b874913dd41f0bf",
        "grounded": true
      },
      {
        "id": "fact_5adef24251a2608453c8",
        "object_or_effect": "w_f614275896981f39aa2e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f614275896981f39aa2e",
        "grounded": true
      },
      {
        "id": "fact_706f00d22404d046a2aa",
        "object_or_effect": "o_8c0b1f5458e36e9cd3ca",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_8993d670cf4de9ced7af",
        "object_or_effect": "w_d55f737fa1f345863f34",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d55f737fa1f345863f34",
        "grounded": true
      },
      {
        "id": "fact_f318835fd975bb0829d8",
        "object_or_effect": "w_4b561949cdc12029663f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4b561949cdc12029663f",
        "grounded": true
      },
      {
        "id": "fact_f70f1d4cebc1e1bf4440",
        "object_or_effect": "w_28faf9463e5afdc72520",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_28faf9463e5afdc72520",
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
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 12,
      "source_task_reading": 8,
      "policy_missing": 2,
      "external_dependency": 2
    }
  }
}
```
