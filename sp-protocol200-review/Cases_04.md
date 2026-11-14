# 逐例审阅

## RQ1_2be3e9b98fac

证据目录 run/members/RQ1_2be3e9b98fac/attempt_1/，报告哈希 7da0e2b929e60e3f5471edfff8759c412c95fbb2172baab5034278e12208525f

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [
    "prev200 新增根因 D2:30:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_2be3e9b98fac",
        "reference": "D2:30:author:1",
        "function": "IstriumToken",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "FN",
        "decision_only": "TP",
        "prev200_findings": [],
        "decision_only_findings": [
          "finding_51df9e11ea8ff618d0ad"
        ],
        "current": "TP"
      }
    ],
    "findings": [
      {
        "idx": 5,
        "member": "RQ1_2be3e9b98fac",
        "finding": "finding_a9ea7ba44fa7aadfc90f",
        "function": "IstriumToken(address)",
        "location": {
          "file": "units/program.sol",
          "start": 755,
          "length": 18,
          "ast_id": 71
        },
        "result": "TP",
        "reference": "D2:30:author:1",
        "group": "D2:30:author:1",
        "source_excerpt": "owner = msg.sender",
        "source_sha256": "38adbb5e3f84bace1ea40d1788615289615a4f78aa5e08a65e78c32fc736f795",
        "note": "公开资格写入位于作者标定入口，实际语义支持与资格/下游检查对应。",
        "decision": {
          "status": "risk",
          "reason": "source_role_reassignment",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 755 under management_role. An office established by the source controls a separate protected effect. The replacement of that office lacks the corresponding qualification.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 755,
              "length": 18,
              "ast_id": 71
            }
          ],
          "effects": [
            "w_2b213285ebbc50c812a3"
          ],
          "rules": [],
          "supports": [
            "support_0d3dbdc867b2ff81bdbd"
          ],
          "facts": [
            "fact_1d2252dbc0e50206b264"
          ],
          "meanings": [
            "management_role"
          ],
          "origins": [
            "source_observation",
            "verified_service"
          ]
        },
        "evidence_refs": [
          "E1",
          "E10"
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
        "gained": [
          "D2:30:author:1"
        ],
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
          "detail_sha256": "dd83895f69656be636e4d0b592e18019531c14dffeb85517da414bdfe60e0e87",
          "issue": "issue_7a435648ce8ef9f3fecc"
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
          "detail_sha256": "e8db7284583e5a453473b81ef0a648b118315da727e3ce3b12a2ac6458e91f49",
          "issue": "issue_d781c0a113c471ea38d8"
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
        "support": "support_0d3dbdc867b2ff81bdbd",
        "fact": "fact_1d2252dbc0e50206b264",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_1d3c342b6e27f055aaf7",
        "fact": "fact_f3fac5ca89ba24614722",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_d263a2ccc06de38b2b87",
        "fact": "fact_1d2252dbc0e50206b264",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_1621a1ccb84edc360b04",
        "object_or_effect": "w_59496ea46a193e24162f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_59496ea46a193e24162f",
        "grounded": true
      },
      {
        "id": "fact_1d2252dbc0e50206b264",
        "object_or_effect": "o_be63fc36ce15ceeded11",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_ad609b0c2d2bd32fda51",
        "object_or_effect": "w_fa3ab0cce934c2c05889",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_fa3ab0cce934c2c05889",
        "grounded": true
      },
      {
        "id": "fact_c78cad831e5488aaf650",
        "object_or_effect": "w_344eff6ee755f9a4ee9a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_344eff6ee755f9a4ee9a",
        "grounded": true
      },
      {
        "id": "fact_f3fac5ca89ba24614722",
        "object_or_effect": "o_9c6285bba30423e7bd92",
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
      "unbound_or_inapplicable_seed": 2,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 3,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 7,
      "policy_missing": 3,
      "source_task_reading": 4,
      "source_role_reassignment": 1
    }
  }
}
```

## RQ1_2c07fdcf80d4

证据目录 run/members/RQ1_2c07fdcf80d4/attempt_1/，报告哈希 5b10fdc8d21c515f4cd9af1e073b423d4ab80857d0c0375b5b06124e2edb9c35

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:458:author:1",
    "last1164 丢失根因 D2:458:author:1",
    "prev200 丢失根因 D2:458:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_2c07fdcf80d4",
        "reference": "D2:458:author:1",
        "function": "setAllowedAddress",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "FN",
        "prev200_findings": [
          "finding_3b348068a0c65a391561"
        ],
        "decision_only_findings": [],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:458:author:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:458:author:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:458:author:1"
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a9bf4faeba866a66ce1611006a910acb5f6e04684079072bcfd6e42b377adcf5",
          "issue": "issue_9d5d33c5f801bee980b7"
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
          "detail_sha256": "8cafef1f40a876089df7c636bfd90ad3afd472db764a617a44e56c4acc8d6db1",
          "issue": "issue_b83ef85353aeefafcd42"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [
      2544
    ],
    "new": [],
    "disappeared_to_unknown": true,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_310e38956cb32d03efac",
        "fact": "fact_93f17b3c5fbaab57459b",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_3e9ace84822ad831dbe6",
        "fact": "fact_9646902c28b68256b51a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_afa225fe7d4fd166640c",
        "fact": "fact_f2f5295c9148c273c4ae",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_b68903582da864738807",
        "fact": "fact_93f17b3c5fbaab57459b",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_05b7c7cef7e97d86de8d",
        "object_or_effect": "w_5a35031f2b7a3e1d8db3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5a35031f2b7a3e1d8db3",
        "grounded": true
      },
      {
        "id": "fact_141bc73702051c56a139",
        "object_or_effect": "w_2e619ffa8d96e8a010bb",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2e619ffa8d96e8a010bb",
        "grounded": true
      },
      {
        "id": "fact_7982ac5274105168aa72",
        "object_or_effect": "w_ef0cf1059bdb66ecacdc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ef0cf1059bdb66ecacdc",
        "grounded": true
      },
      {
        "id": "fact_93f17b3c5fbaab57459b",
        "object_or_effect": "o_9473dea584ebaa8c80a3",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_9646902c28b68256b51a",
        "object_or_effect": "o_3fdb5948dbe873230c3c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_f2f5295c9148c273c4ae",
        "object_or_effect": "o_f536dfe521837b8c80ff",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_f4677492af669aebb723",
        "object_or_effect": "w_9e198b91a5c1d220dcff",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9e198b91a5c1d220dcff",
        "grounded": true
      },
      {
        "id": "fact_f68667df2cfbe60129fd",
        "object_or_effect": "w_40e6170ac269a2930fb6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_40e6170ac269a2930fb6",
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 6
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 5
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 6
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 2
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 3,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 6,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 17,
      "source_task_reading": 9,
      "policy_missing": 5,
      "external_dependency": 2
    }
  }
}
```

## RQ1_2d22977434b5

证据目录 run/members/RQ1_2d22977434b5/attempt_1/，报告哈希 25793b818de9b9bee62f0a5f87294f2e3f1400c36838cb076e25d3694169750a

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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,no_locatable_source",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": false,
    "paired_id": "RQ1_4169c528c5e4",
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
          "detail_sha256": "59effd625d070d18d0c3f824764238df3a31fa363242b9db49f7a565743cfbea",
          "issue": "issue_96e82b099fce92a85f2b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c037dc089a461783fa74fa8c5ee511f42cb95092411e2335e5762683c1efb816",
          "issue": "issue_96e82b099fce92a85f2b"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "c5360081ec74343df0d89278a2af66aecd2f12eccf577f5837887e954cbb0a2c",
          "issue": "issue_85da55fd1a0401fa24a3"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "461fe6ec5ef47fcd61642ac3440be0f3d30563feda69fc2b59fa7d8fede785e3",
          "issue": "issue_85da55fd1a0401fa24a3"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_2e873517cbffd6152c04",
        "fact": "fact_b4d8df0d704add2ccc4a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_7bf8a59f1e181efadd90",
        "fact": "fact_41f14f1f5e4810311a1d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_41f14f1f5e4810311a1d",
        "object_or_effect": "o_3a47c406840d6b2301b6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_b4d8df0d704add2ccc4a",
        "object_or_effect": "o_6a1914ce99e5ed3eaeb6",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_f8eac1f68cfa0be29f01",
        "object_or_effect": "w_bdc287844c6de2f9e26f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_bdc287844c6de2f9e26f",
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 36
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
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 25
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 30
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 5
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
      "unbound_or_inapplicable_seed": 3,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "no_locatable_source": 2
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

## RQ1_2e5ccd7b4bd2

证据目录 run/members/RQ1_2e5ccd7b4bd2/attempt_1/，报告哈希 aec6f0a4ac23e9b4054c9f16eecca2f6fe667929d5f4ef8bd798a7c8897111b6

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "prev200 丢失根因 D2:363:original:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 semantic_answer_outside_sent_scope,unbound_or_inapplicable_seed,unknown_assessment_vocabulary,revision_outside_actual_feedback_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_2e5ccd7b4bd2",
        "reference": "D2:363:original:1",
        "function": "fallback",
        "v32": "FN",
        "last1164": "FN",
        "b5": "FN",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "pending",
        "prev200_findings": [
          "finding_5faca06b709dc38d7a77"
        ],
        "decision_only_findings": [
          "finding_7cbbe6ff9454bbfb5665"
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
          "D2:363:original:1"
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
      "normalization_diagnostics": [
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "23ff4bd8be2d5794f9ce44142a5101a0ec9c2dbfef7ac8a946461c9b9349cd3a",
          "issue": "issue_2e5eaa44eda8e361b1bd"
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
        "support": "support_1643554b2b173ad7ac75",
        "fact": "fact_a8a7b2eaaffba373a37f",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_fbafa0346d3fb539c4b6",
        "fact": "fact_f4c642ad03b700812871",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_a8a7b2eaaffba373a37f",
        "object_or_effect": "o_599f16a74243cae7170b",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_f4c642ad03b700812871",
        "object_or_effect": "o_53576bf73c900eb56133",
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
        "count": 3
      },
      {
        "label": "source_quantity_debit",
        "answer": "unsat",
        "count": 8
      },
      {
        "label": "source_quantity_debit",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "net_state_change",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 3
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 1,
      "semantic_answer_outside_sent_scope": 2,
      "unknown_assessment_vocabulary": 1,
      "revision_outside_actual_feedback_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 17,
      "source_task_reading": 11,
      "external_dependency": 1
    }
  }
}
```

## RQ1_30177d564271

证据目录 run/members/RQ1_30177d564271/attempt_1/，报告哈希 af5f35684b7b7e38ebad7c2211a104e7c16e742482912d218e26564094933d4f

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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": false,
    "paired_id": "RQ1_c80f7a639e42",
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
          "detail_sha256": "92056a209e0ec3da358533ae2ccd56f602c96b3d893ca2c299954a063ab1ef4d",
          "issue": "issue_a98c02dc7452b2171124"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "36fd75244fea894205fbe7192adf32996e7b6af988dcda70801569cd5d4c2b36",
          "issue": "issue_debbd8bbb8b2d5b414dc"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ef46966763c89430c633fca814819be9d28633cc002c69dbc9c2b61f0fe93e7e",
          "issue": "issue_debbd8bbb8b2d5b414dc"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_00019f81aac585dbd5e3",
        "fact": "fact_605f2e87782b9d871289",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_605f2e87782b9d871289",
        "object_or_effect": "o_1d1134cd9e6d2056cde8",
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
        "count": 3
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 3
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "unknown_assessment_vocabulary": 2,
      "category_ambiguous_or_outside_supported_task": 1,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE",
      "FCR-PAUSE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 126,
      "source_task_reading": 28,
      "scope_missing": 2,
      "external_dependency": 6,
      "parameter_only": 1,
      "covered_holder_grant": 2
    }
  }
}
```

## RQ1_30c29cd44cad

证据目录 run/members/RQ1_30c29cd44cad/attempt_1/，报告哈希 70c48d17c6e34e904d8eba9ee7e36268dbc3bca70cadbfd689a20a4e7fa4b59a

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
    "decision_only 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unrelated_or_secondary_graph_pairs_deferred,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": true,
    "paired_id": "RQ1_329e0d0d7a11",
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
        "before": "unsupported",
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
          "detail_sha256": "8db701b9d18b35bed3139a4944fcc2b65e622375dd28cb493b909f03c9f83def",
          "issue": "issue_8bbeea519c8166f70a17"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "3e4bc6b819678de93f97817365e8b74f03280775d83511460b4b8e25ac92f464",
          "issue": "issue_8bbeea519c8166f70a17"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_5d495df8d3e4ad9b0729",
        "fact": "fact_a9823af82b0718a4c9b2",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_7e549daa86d625c6bdd9",
        "fact": "fact_333a31e0eeb6fa6a95c8",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_333a31e0eeb6fa6a95c8",
        "object_or_effect": "o_10ded92b986eaf369b34",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_3ef2b75b5c7d79f656c6",
        "object_or_effect": "w_4642e60400dbba6b9b33",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4642e60400dbba6b9b33",
        "grounded": true
      },
      {
        "id": "fact_a9823af82b0718a4c9b2",
        "object_or_effect": "o_27e3dd838313b9bd662a",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_d845d36cac20d513a875",
        "object_or_effect": "w_717cd877fb3012d10a61",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_717cd877fb3012d10a61",
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
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 2
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 3,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 44,
      "external_dependency": 15,
      "source_task_reading": 1
    }
  }
}
```

## RQ1_31450a049444

证据目录 run/members/RQ1_31450a049444/attempt_1/，报告哈希 e5382aef1a46b1d1a7cd87e471ebeb667e16b807cf85ac143a392411470b2ccc

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_31450a049444",
        "reference": "D2:360:original:1",
        "function": "fin",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_ffbeb81b7e7545c4faf5"
        ],
        "decision_only_findings": [
          "finding_9f69cbec6ac769365aec"
        ],
        "current": "TP"
      },
      {
        "member": "RQ1_31450a049444",
        "reference": "D2:360:original:2",
        "function": "pay",
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
    "findings": [
      {
        "idx": 6,
        "member": "RQ1_31450a049444",
        "finding": "finding_f9f7dee69ef2ed684e44",
        "function": "fin()",
        "location": {
          "file": "units/program.sol",
          "start": 248,
          "length": 106,
          "ast_id": 44
        },
        "result": "TP",
        "reference": "D2:360:original:1",
        "group": "D2:360:original:1",
        "source_excerpt": "function fin() public {\n        if (tx.origin == O) {\n            selfdestruct(tx.origin);\n        }\n    }",
        "source_sha256": "c2a2caa3407ab77f8ad8ee572bc16ddc2820b2b5490b1cff016a15450530d21f",
        "note": "实际入口及源码效果与作者独立根因对应，保留程序证据可审计性限制。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 248. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 248,
              "length": 106,
              "ast_id": 44
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
          "detail_sha256": "97fcfa70239aa7d9eb6c94170979d4225f109b805d899a49c0a4cff6af62aa93",
          "issue": "issue_9bae1827e27fcd32720e"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "75868286c7121c4fc51ffdfe17f4ed6f4c183f43e0e4688b036764ae1960a97e",
          "issue": "issue_dc142845c9016062841d"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ad34a8611a04278aaff4634c59715b95b6b6b446f314be67b8e9e5a423362143",
          "issue": "issue_dc142845c9016062841d"
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
        "support": "support_48946511ae9b26669318",
        "fact": "fact_1560be5df2bad0775fc1",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_9ee5020ce86ce41b514b",
        "fact": "fact_b50a8792da35d5ac0ee4",
        "origin": "verified_service",
        "field": "policies",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_1560be5df2bad0775fc1",
        "object_or_effect": "o_6aba4726777aed7f43b3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_b50a8792da35d5ac0ee4",
        "object_or_effect": "e_76909c123acc9f3643d8",
        "meaning": "holder_authorization_applies",
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
        "count": 1
      },
      {
        "label": "authorization_violation",
        "answer": "unsat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 4,
      "unknown_assessment_vocabulary": 2,
      "category_ambiguous_or_outside_supported_task": 1,
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "program_support": 1,
      "external_dependency": 1,
      "no_effect_in_scope": 1
    }
  }
}
```

## RQ1_329e0d0d7a11

证据目录 run/members/RQ1_329e0d0d7a11/attempt_1/，报告哈希 e2b676379b3f439ae173728ab1648f24058b940af648123ba3e0ef11efc1f806

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
    "已确认消费/覆盖诊断 unknown_assessment_vocabulary,invalid_semantic_row,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": false,
    "paired_id": "RQ1_30c29cd44cad",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "670b6c00aceb315973a0fe3f1d140dd0f9207365763daa1fa6908d93fe93094f",
          "issue": "issue_fb6f0eb6ac9782efe1aa"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "2f5a32d1ffe9bb8b120b17b0c4dc7ab68bedf042a73ed09eaebd03cd4d218a55",
          "issue": "issue_6d79738f14c9b3038906"
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
      "invalid_semantic_row": 1,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1
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

## RQ1_32dbc2fa2433

证据目录 run/members/RQ1_32dbc2fa2433/attempt_1/，报告哈希 bf8871b1da41bd2d74936aee03a73772e7c9145a86885e1edb1e6d2670af9965

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
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,unrelated_or_secondary_graph_pairs_deferred",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": false,
    "paired_id": "RQ1_c24c6c95ccbd",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "4575b29d8f5ea627c4f2e85219b55732b9537e898da9fd56ab01bb49b0b81ba5",
          "issue": "issue_881c4a51540b4c574785"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "4948517942fcdd413a133743c6b83b732853cad77a1306692951ee97b4a4e776",
          "issue": "issue_881c4a51540b4c574785"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "8865a235591d390a4e7c49b96ecbda7a3eeb99bfc545bce0f7d4d79e9bb27f97",
          "issue": "issue_3449602ec494c5f32936"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "7833eeb88455efe0dcd0663611b601c505f0e78c22a4758cb5534c839cb1663b",
          "issue": "issue_3449602ec494c5f32936"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "75cf4e935eb41c11a371cfc601ea399254f1dd6d82278114d4c0aa9ad77b5a84",
          "issue": "issue_9fed695df126cafc7032"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "e0b7e0f1bd319ee02c87ae01c013c466982a247e725325807e0f51759b75d131",
          "issue": "issue_9fed695df126cafc7032"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "1229516d01749a65da128558283e94a0cce0dc25f6333a74c4b6e9f1aa6b2cfc",
          "issue": "issue_3b424c596a9fa29e80e5"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a0e802a63c4cb26bd1efa0bea76ff7879730484fe5b9ddb4bcd56c5d017bee0d",
          "issue": "issue_3b424c596a9fa29e80e5"
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
          "detail_sha256": "95932ac317a746b7867d4b5f0a2a41eaca083eaaa09c78dd8ea2dca7dfe6054e",
          "issue": "issue_d849b8407827e687106a"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "f9d78e58db5762defcf8c80994a02941bff08962db05016bf2b91c830d50d017",
          "issue": "issue_d849b8407827e687106a"
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
      },
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
      "invalid_semantic_row": 7,
      "category_ambiguous_or_outside_supported_task": 5,
      "unknown_assessment_vocabulary": 4,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 2,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 45,
      "external_dependency": 15
    }
  }
}
```

## RQ1_33d48945207e

证据目录 run/members/RQ1_33d48945207e/attempt_1/，报告哈希 788e16f6e10336d1eef15bed4cf35c7910dd85f47e5a48728b7ab9293211bd9b

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
    "已确认消费/覆盖诊断 Unsupported:source_semantics_unavailable:path_85b2849dece1deace263,unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope,unrelated_or_secondary_graph_pairs_deferred",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": true,
    "paired_id": "RQ1_6ca2b0aeda43",
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
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_40021c2225d3c865daf3",
        "fact": "fact_8f499ca44475051d05b1",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_fefbaad3fe44d95e723b",
        "fact": "fact_5c3f6cc0347d7043e0a2",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_1e4536ff4e749bce274e",
        "object_or_effect": "w_56353990d4ed75f1c3b5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_56353990d4ed75f1c3b5",
        "grounded": true
      },
      {
        "id": "fact_561bd7dfb6bdda717ecc",
        "object_or_effect": "w_1dddde09d98421e55bee",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1dddde09d98421e55bee",
        "grounded": true
      },
      {
        "id": "fact_5c3f6cc0347d7043e0a2",
        "object_or_effect": "o_dc69f2f23bae78cf6302",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_606fb7feeffce93efe92",
        "object_or_effect": "w_0f42398ce8c03e28ea1e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0f42398ce8c03e28ea1e",
        "grounded": true
      },
      {
        "id": "fact_6c108e44a096730c1db6",
        "object_or_effect": "w_7178ec18011c95fe657c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7178ec18011c95fe657c",
        "grounded": true
      },
      {
        "id": "fact_72ba5710a4b8dd460922",
        "object_or_effect": "w_9ad08c2c7bdeb60804a8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9ad08c2c7bdeb60804a8",
        "grounded": true
      },
      {
        "id": "fact_85962efe9d14f69120d2",
        "object_or_effect": "w_66a9511c73596363b6a5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_66a9511c73596363b6a5",
        "grounded": true
      },
      {
        "id": "fact_8f499ca44475051d05b1",
        "object_or_effect": "o_44cdfe67f909b28fe66b",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_9fec235c38068c0d096f",
        "object_or_effect": "w_8eab9dcf421b74a9fc9e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8eab9dcf421b74a9fc9e",
        "grounded": true
      },
      {
        "id": "fact_a618c91488d61f8bf3f1",
        "object_or_effect": "w_2ad82ac4774d32c92a15",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2ad82ac4774d32c92a15",
        "grounded": true
      },
      {
        "id": "fact_acd579393a054cff71cf",
        "object_or_effect": "w_f531fa54841577490dad",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f531fa54841577490dad",
        "grounded": true
      },
      {
        "id": "fact_b03aa9f6e8a4717c7c1c",
        "object_or_effect": "w_d85231e623851c224566",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d85231e623851c224566",
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 1,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 1,
      "Unsupported:source_semantics_unavailable:path_85b2849dece1deace263": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 209,
      "source_task_reading": 12,
      "external_dependency": 17,
      "covered_holder_grant": 1,
      "scope_missing": 1
    }
  }
}
```
