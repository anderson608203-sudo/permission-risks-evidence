# 逐例审阅

## RQ1_1f932eab663d

证据目录 run/members/RQ1_1f932eab663d/attempt_1/，报告哈希 3140129f55db0b0102d0519eddeaced5731b99b6ca065e5e69b0eed56c195443

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "not_detected",
    "FCR-DESTROY": "not_detected",
    "FCR-PAUSE": "not_detected",
    "FCR-FREEZE": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,semantic_answer_outside_sent_scope",
    "未决类别 FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": true,
    "paired_id": "RQ1_43103f5773b9",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "407fcf526e333a9b797fdcdc0a426655da01895840250271d6e45863522759b4",
          "issue": "issue_03f6e24ea3376b07d657"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "64c5cee682a9594c74057837e952c0192f8c66a07f0e2d7cbe4c523e285c8511",
          "issue": "issue_d7a25ebe41964c53f776"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d7761d51cb00941972b53fe3d9fc2021a829fcecdce1a0123ad187394769d521",
          "issue": "issue_d7a25ebe41964c53f776"
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
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 3,
      "unknown_assessment_vocabulary": 2,
      "category_ambiguous_or_outside_supported_task": 1,
      "semantic_answer_outside_sent_scope": 1
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
      "no_effect_in_scope": 122,
      "source_task_reading": 31,
      "scope_missing": 1,
      "program_support": 1
    }
  }
}
```

## RQ1_2046acc1c802

证据目录 run/members/RQ1_2046acc1c802/attempt_1/，报告哈希 5817e97ef16806db5c37bf19018e1690c87a0e6f6a064440007f39e41660e661

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
    "decision_only 未知转有效阴性"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unknown_assessment_vocabulary,unbound_or_inapplicable_seed,invalid_semantic_row,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": false,
    "paired_id": "RQ1_58de46f081ec",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "904585fa57246358caca2892f1eb5392ee827d929dc604ca06f2a81f10face48",
          "issue": "issue_5e493154ce96bd37f195"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d72861e8e5b865d271885584ee8037355c727e5f91b4e7047cd5eebb5527b164",
          "issue": "issue_93ca447637a5466e77aa"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_3dfbf088aea7a43eefab",
        "fact": "fact_35bba84ce445dccdc82b",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_64bcdebce23019e04dbc",
        "fact": "fact_5bbb9f818cc4ab23ff2e",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_35bba84ce445dccdc82b",
        "object_or_effect": "o_489f550c22f8ec497bd9",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_5bbb9f818cc4ab23ff2e",
        "object_or_effect": "o_e271f10eabf5b0b63dd5",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_a5224589118d2465853e",
        "object_or_effect": "w_8efe3096d79387e739e6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8efe3096d79387e739e6",
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
      "unbound_or_inapplicable_seed": 1,
      "invalid_semantic_row": 1,
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
      "no_effect_in_scope": 115,
      "source_task_reading": 30,
      "scope_missing": 1,
      "external_dependency": 6,
      "parameter_only": 1,
      "covered_holder_grant": 2
    }
  }
}
```

## RQ1_206d19a8539c

证据目录 run/members/RQ1_206d19a8539c/attempt_1/，报告哈希 1b8e6ee0dc9faf4e343d361d03f15bb8271467831cf55b4ca1b66996f89efd42

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,negated_or_ambiguous_confirmation_not_a_risk_judgment"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": false,
    "paired_id": "RQ1_3a3d833ca142",
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
          "detail_sha256": "57d3133948def3925737f8ce8935e5f6ba1ef18725c93bfdc703008266156584",
          "issue": "issue_5394c45d3d9d89eec555"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "9195f705e4f3ff8e329eb72a6665fb13c3671939f7046bc8ba23152136c144c4",
          "issue": "issue_dc5f4a0e76a5b059e394"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a3d7aab1a3ed3dae32a0cea2880b244cc8bbffb59892183a77dd5c28abf2a1dc",
          "issue": "issue_dc5f4a0e76a5b059e394"
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
          "detail_sha256": "49e4602a9489ecac29d531dffaafe69e0f3c8c3fc452a2589dbc8a612db04849",
          "issue": "issue_7cdaf24b7282a60ea953"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "8b57ad26da10ce4dea74ecf323e3fd94249e1520531296479910a27c6c64178d",
          "issue": "issue_7cdaf24b7282a60ea953"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_be2b25ff481847cdc6d9",
        "fact": "fact_7cd0403468a59049e1ea",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_7cd0403468a59049e1ea",
        "object_or_effect": "o_491e318c2936ac59454d",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 3,
      "unknown_assessment_vocabulary": 2,
      "category_ambiguous_or_outside_supported_task": 2,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
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
      "source_check_excluded": 1,
      "scoped_counter": 1
    }
  }
}
```

## RQ1_20dfd0c54b94

证据目录 run/members/RQ1_20dfd0c54b94/attempt_1/，报告哈希 17f449aeb712d31b69182da71082f76d0498e2b970ba3938d8fba405cf4d9a84

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "not_detected",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "unsupported",
    "FCR-FREEZE": "alarm"
  },
  "changes": [
    "v32 退为未知，不能当作纠正",
    "last1164 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unrelated_or_secondary_graph_pairs_deferred,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": true,
    "paired_id": "RQ1_aaeb3f57cfd0",
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
        "before": "unsupported",
        "after": "unsupported"
      },
      "decision_only": {
        "before": "unsupported",
        "after": "unsupported"
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "7784e0022847be1f40250e8d69864df33252352fd836b22360eb387462acfe61",
          "issue": "issue_b365b6e3c9ac37d096ce"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b7f507cd9516817aa1c2f4c16c48a5ccf3ab564ac20e9870e572d8428b1acf3d",
          "issue": "issue_b365b6e3c9ac37d096ce"
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "57cc1d9ce14ba07aad580c61c3555044c76986e2d71ab514b1233785fd01d2f3",
          "issue": "issue_e0bf61265ffec397db3e"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_fa8a7204f157a32b578b",
        "fact": "fact_8866d32d0542c0790546",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_4f5e7f1e71cccd9d3460",
        "object_or_effect": "w_db0598a51867862e43de",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_db0598a51867862e43de",
        "grounded": true
      },
      {
        "id": "fact_6e1355dc0faa11f8fe7f",
        "object_or_effect": "w_dd5fec5febf86d2b97ef",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_dd5fec5febf86d2b97ef",
        "grounded": true
      },
      {
        "id": "fact_8866d32d0542c0790546",
        "object_or_effect": "o_af52a83e7344a50ba1a1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_8a4fe3299559b3dd9c5f",
        "object_or_effect": "w_ce71aadf413b7ae571b3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ce71aadf413b7ae571b3",
        "grounded": true
      },
      {
        "id": "fact_ac7083b9b8b8baa9ae00",
        "object_or_effect": "w_cebd0c323237b98d08b9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cebd0c323237b98d08b9",
        "grounded": true
      },
      {
        "id": "fact_b91a68c053d88b46e68c",
        "object_or_effect": "w_b8a3210959fa23fce684",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b8a3210959fa23fce684",
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 12
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 24
      },
      {
        "label": "financial_consent_unresolved",
        "answer": "unsat",
        "count": 20
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 8
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 12
      },
      {
        "label": "prefix_reachability",
        "answer": "unsat",
        "count": 291
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "direct_effect",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "control_transition_preservation",
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
      "invalid_semantic_row": 5,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 2,
      "no_locatable_source": 1,
      "core_unresolved_retained_for_investigation": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 4,
      "program_investigation_seconds": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-MINT"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 228,
      "scope_missing": 18,
      "source_task_reading": 21,
      "program_support": 1,
      "covered_holder_grant": 2
    }
  }
}
```

## RQ1_2490e07356b6

证据目录 run/members/RQ1_2490e07356b6/attempt_1/，报告哈希 a0c24c67841087e1e21eebbed1b5da8c32c3593da48d650f49ca7d9537be3b82

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,unknown_assessment_vocabulary",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_2490e07356b6",
        "reference": "D2:19:author:1",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "bfb78772d439bc93c1f4a943b3b659ff156299796bf9be31f9244b96b19e3fe8",
          "issue": "issue_bbb9ad590fe879d7c874"
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
      "invalid_semantic_row": 6,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 7,
      "policy_missing": 1,
      "source_task_reading": 1,
      "external_dependency": 2
    }
  }
}
```

## RQ1_261dcad8364d

证据目录 run/members/RQ1_261dcad8364d/attempt_1/，报告哈希 f9654a428fdf7cad5c5504e5a60a00b951a784ecff43b59f588dc838f7182319

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b13d5edd6385c8190883b77c87e440b1b34ea307c658b8b340f88b591cd2b259",
          "issue": "issue_11097a9719299549b3b0"
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
      "invalid_semantic_row": 7,
      "unknown_assessment_vocabulary": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "external_dependency": 1
    }
  }
}
```

## RQ1_283c96463274

证据目录 run/members/RQ1_283c96463274/attempt_1/，报告哈希 6053d26a1b177aab008ef9458e34591fb83a1a78424be34d49ad5301add214ec

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
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
          "detail_sha256": "0d996e95bcdac70f27cb32912242ab5cd1ee7c53a2fbcd50ab60d49e4a1cae73",
          "issue": "issue_c25f64fe8542447060e6"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "483ba752944d3048a3f23cf0ad09fe28d56207b80cd10f39e59986380a746fb7",
          "issue": "issue_c25f64fe8542447060e6"
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
      "unbound_or_inapplicable_seed": 7,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "source_task_reading": 7,
      "no_effect_in_scope": 21,
      "policy_missing": 1
    }
  }
}
```

## RQ1_28fd11561fa6

证据目录 run/members/RQ1_28fd11561fa6/attempt_1/，报告哈希 1b2428f3f4f9810d788a374b89b53a62ec7706a1e8be03fb84ad4afcc0c54086

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:297:author:1",
    "last1164 丢失根因 D2:297:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_28fd11561fa6",
        "reference": "D2:297:author:1",
        "function": "initialize",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
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
        "lost": [
          "D2:297:author:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:297:author:1"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "d78a1676028b6490975e365add79ff5c590a56f7e87e9649ce8f04d68809a098",
          "issue": "issue_ac52378f5033a1641c7c"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "30366f65fec3f51280ccbff1f83401c9c69f092d06a23ac3d31e401f3c6af628",
          "issue": "issue_ac52378f5033a1641c7c"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "7b0c75aef65c8149a53fd772f84dd0a1e1d9c623b1e76b3f4f66fbe20c6fa82f",
          "issue": "issue_119100f0a455e7e35272"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "4e79ed8ed95fe1f96bf967a01bf37978e5efc19de8bc69e332a87747767658ea",
          "issue": "issue_119100f0a455e7e35272"
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
        "support": "support_0dcaa0e8e124d4a7b610",
        "fact": "fact_9f0a9111a72901e359ae",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_505259a3cf3f0a9e5a86",
        "fact": "fact_7650f82d4242d0efa409",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_d7a84486843f3a52147d",
        "fact": "fact_9f0a9111a72901e359ae",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_33cb9b115233778dcb49",
        "object_or_effect": "w_6a15075cf2e648829e05",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6a15075cf2e648829e05",
        "grounded": true
      },
      {
        "id": "fact_7650f82d4242d0efa409",
        "object_or_effect": "o_c226513e3770f4865fd0",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_8c331533cff1d0dda7f0",
        "object_or_effect": "w_5f52d5b6f7f193d1e791",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_5f52d5b6f7f193d1e791",
        "grounded": true
      },
      {
        "id": "fact_9f0a9111a72901e359ae",
        "object_or_effect": "o_c21bd9e292e6456c10d1",
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
        "count": 2
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 3
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
      "invalid_semantic_row": 3,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 2,
      "no_locatable_source": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "policy_missing": 2,
      "no_effect_in_scope": 4,
      "source_task_reading": 2,
      "external_dependency": 2
    }
  }
}
```

## RQ1_293812debd13

证据目录 run/members/RQ1_293812debd13/attempt_1/，报告哈希 4fce3a2366aa9ea59ab7c45e6b80532d2730c93192c42e8d08579fb1ce7aa7b6

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,semantic_answer_outside_sent_scope,unbound_or_inapplicable_seed,unknown_assessment_vocabulary",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "3efd2b37b7b43e32e46c195f6d540db6a25b33534720b324c887ef8ace1a1883",
          "issue": "issue_bd45f8bb1c789d298a2c"
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
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "12f54db18a279d34edc886f654456f0b1de2cecf41bf714793d56780029aae48",
          "issue": "issue_35667abc83338a871c59"
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
        "support": "support_12fa8891e8d22719fa8b",
        "fact": "fact_dd43b00b08f2e315ffea",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_3a00ce4e77ee1e293040",
        "fact": "fact_28a7db7013af33794d14",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_4a798bf0b0ec3807bbbc",
        "fact": "fact_75a7d2749aa21468a6bb",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_66f0f3227c469c049a53",
        "fact": "fact_cf08c1c67d0450da6063",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_80df10d36a1fc477dedf",
        "fact": "fact_cf08c1c67d0450da6063",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_f143a889bbd07509dd5a",
        "fact": "fact_dd43b00b08f2e315ffea",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_1ce15d983b3d306aa9ed",
        "object_or_effect": "w_5209b00a9775d18f65b2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5209b00a9775d18f65b2",
        "grounded": true
      },
      {
        "id": "fact_28a7db7013af33794d14",
        "object_or_effect": "o_ec3b52724450b717e5eb",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_75a7d2749aa21468a6bb",
        "object_or_effect": "o_0fd02e05cdf89ee93237",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_97d2d48cf3e21a4c9c34",
        "object_or_effect": "w_7eca80c67823f2e80cc1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7eca80c67823f2e80cc1",
        "grounded": true
      },
      {
        "id": "fact_9a9cd64c4f5831094cec",
        "object_or_effect": "w_f010d77f5a79d6430955",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f010d77f5a79d6430955",
        "grounded": true
      },
      {
        "id": "fact_b972e63912ecaa7064e3",
        "object_or_effect": "w_07112c8fc7fb7e574596",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_07112c8fc7fb7e574596",
        "grounded": true
      },
      {
        "id": "fact_bff9b28a75053c39b62f",
        "object_or_effect": "w_29ad8bec81d03aefe641",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_29ad8bec81d03aefe641",
        "grounded": true
      },
      {
        "id": "fact_cf08c1c67d0450da6063",
        "object_or_effect": "o_022c3ea515c2d72b7133",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_dd43b00b08f2e315ffea",
        "object_or_effect": "o_5077328b8fafdb227081",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_debe49ed16aa0daa4149",
        "object_or_effect": "w_c5326d470b4e7942e0c5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c5326d470b4e7942e0c5",
        "grounded": true
      },
      {
        "id": "fact_f367f1e42c27d26ee3fe",
        "object_or_effect": "w_aead487dac5080ab6c79",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_aead487dac5080ab6c79",
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 3,
      "unrelated_or_secondary_graph_pairs_deferred": 4,
      "invalid_semantic_row": 1,
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

## RQ1_2a3f29f582b8

证据目录 run/members/RQ1_2a3f29f582b8/attempt_1/，报告哈希 0b207adb4d552c9a18fe87c8cc01d0c9ab267688d7c5ab1cfb0087da3f72e141

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "last1164 丢失根因 D2:412:author:1",
    "prev200 丢失根因 D2:412:author:1",
    "decision_only 丢失根因 D2:412:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_2a3f29f582b8",
        "reference": "D2:412:author:1",
        "function": "end_redeem_period",
        "v32": "FN",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_dc794c4718246eceaf88",
          "finding_9aebe1f1aba9f5fc7a1c"
        ],
        "decision_only_findings": [
          "finding_84b202d54775c51cce79"
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
        "lost": [
          "D2:412:author:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:412:author:1"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:412:author:1"
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "71aaecf09473ca67a37d1897264df5c27d14770059a2632c3940f4c1a10c5cfc"
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
          "detail_sha256": "bb131b9a06e452364501dd0904b8d7c5e8099cd2f6e13866ae53eaccdf08cba1",
          "issue": "issue_f5ed314f703c517cda91"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "76d530fc9e4a5b24a9455cdc5b3f09ad942e34e358e704ab3db3a204b3274bf6",
          "issue": "issue_f5ed314f703c517cda91"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "c4fd53397fae5b26197de34f271aa09cc9d06e0bd309f90a7930f0e317e969f1",
          "issue": "issue_dcdcd8d7dc45a1015896"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "5e6eaa44bbd2aff2e312559dd3adef71e2b73fcd90a6e06d006f7ac52b3cf0f4",
          "issue": "issue_dcdcd8d7dc45a1015896"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "8da34bef2a7264ac1f7c122cd7198a3021ab01ba6f39b7c3cc040b7b5ee09ff2",
          "issue": "issue_890d7c24a5c0c57689c0"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "0025a9f8b5020c50443fc68db14fd67e6bd8a73ad5e1e491f6e94c32acede908",
          "issue": "issue_890d7c24a5c0c57689c0"
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
      "invalid_semantic_row": 9,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 4,
      "external_dependency": 4,
      "policy_missing": 1
    }
  }
}
```
