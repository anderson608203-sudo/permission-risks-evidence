# 逐例审阅

## RQ1_a4c5ecc3c29e

证据目录 run/members/RQ1_a4c5ecc3c29e/attempt_1/，报告哈希 0c75bdbff887dad85dce45e97a4649fa344166cd7f84ce363adeeec62f114ad0

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,no_locatable_source",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": false,
    "paired_id": "RQ1_cf32aac41cf2",
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
      "response_kind": "invalid_protocol",
      "usable": false,
      "status": "protocol_diagnostic",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "909e751cf631c1e398fa6e1a3a9ca594f2a85301bb2b84ad177976f1b6136350",
          "issue": "issue_a20cc3b481b774d78ced"
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
      "unknown_assessment_vocabulary": 1,
      "no_locatable_source": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 20,
      "external_dependency": 5
    }
  }
}
```

## RQ1_a533300b98f5

证据目录 run/members/RQ1_a533300b98f5/attempt_1/，报告哈希 6a3fb7749e7c0a508ecf572e217b23178fc5c6159ee96822f4d8498a4b3ff6be

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
    "roots": [
      {
        "member": "RQ1_a533300b98f5",
        "reference": "D2:539:author:1",
        "function": "die",
        "v32": "FN",
        "last1164": "FN",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "b0c67f76f0f42a39094b4458cf302a6ed656398ccb0e47f966953920cc0881d5",
          "issue": "issue_62ac6b9a88d5b9b84034"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "0750cb2cbc765686288da884557f70fe33a0ffc8ebfae8f7f816fb3a6dd91457",
          "issue": "issue_62ac6b9a88d5b9b84034"
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
      "invalid_semantic_row": 1,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "policy_missing": 1
    }
  }
}
```

## RQ1_a69a455c4a25

证据目录 run/members/RQ1_a69a455c4a25/attempt_1/，报告哈希 a383c8be2a8a89e2f28ee06bda14dd5434329f6986195656b54c463404ad505e

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": false,
    "paired_id": "RQ1_adf28b957352",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "9e11d6d2c166ff16987be53ef6fa976cd69232b8cf4d221a2360e68d8e8acdf3",
          "issue": "issue_451f241341f1eac6b3a4"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "6b8065b1d2f8b2311584628cc5b94f1e94f72dafddc76ab2d6f15fc5f65f8de1",
          "issue": "issue_ce61cab8e347fb5caa6f"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "745c78d349233e159dff8444824a38d2a45e310bc9d176adb1527cbd60811ccf",
          "issue": "issue_ce61cab8e347fb5caa6f"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_9499fd911db468c04709",
        "fact": "fact_3c80f6e88e7639030218",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_3c80f6e88e7639030218",
        "object_or_effect": "o_81ad02bebc600a58ae8f",
        "meaning": "financial_right",
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
      "category_ambiguous_or_outside_supported_task": 1,
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
      "no_effect_in_scope": 127,
      "source_task_reading": 36,
      "external_dependency": 6,
      "parameter_only": 1
    }
  }
}
```

## RQ1_a7bf9487cc3f

证据目录 run/members/RQ1_a7bf9487cc3f/attempt_1/，报告哈希 0d6452d4e93ddb527cd71030eb092d313bcb12772ab756b94bb8019912581df5

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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,invalid_semantic_row",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": false,
    "paired_id": "RQ1_c772c59e4a76",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "f01575133c9436278e90f70666310f0105adf76b25c268b8f0149adf27d360d4",
          "issue": "issue_2db92d580c7e77eb56be"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "bd1fe43002b39a9fdfa9c4173a173792fbfd5b7f07ae085be364e27dbba84d0c",
          "issue": "issue_2db92d580c7e77eb56be"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "ad7ac4f4e6bd410878e376b1cb474a2720e9ef793b63ab18cf161967988a7aa6",
          "issue": "issue_9f35c62f4141a82de2d6"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "bc59aefdb32d222d0434be9c4990fdbcbba9cd3517e85074d95788b6e577a718",
          "issue": "issue_9f35c62f4141a82de2d6"
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
          "detail_sha256": "65fdde435dc330a40467240970ad238f6d973ca518f5f3e6b233a595ccb8d74b",
          "issue": "issue_cfdeb15dbd03301ffa5a"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c16ac29587636be60def6bd8bc118160ba28a922543726c413d24b02d5a038fb",
          "issue": "issue_cfdeb15dbd03301ffa5a"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_cd4393aa700d3ce117dd",
        "fact": "fact_d801a0fb5e759bb0cb90",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_d801a0fb5e759bb0cb90",
        "object_or_effect": "o_7d6c2b9fdbd623aaeaf7",
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
      "invalid_semantic_row": 1,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 3,
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
      "no_effect_in_scope": 128,
      "source_task_reading": 33,
      "covered_holder_grant": 2,
      "external_dependency": 7
    }
  }
}
```

## RQ1_a7d72c1e4129

证据目录 run/members/RQ1_a7d72c1e4129/attempt_1/，报告哈希 e335e270e3ce3013eeb2736339377a1881587abdd4c847e08fe66d8f47b72a9e

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
    "已确认消费/覆盖诊断 category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,unrelated_or_secondary_graph_pairs_deferred,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": false,
    "paired_id": "RQ1_53f9777ccdf6",
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
          "detail_sha256": "90bc67bacfbe6f286c92f61c8c545c3d818b2a3f60b3623bb5e9c33ecaacc606",
          "issue": "issue_f98291d717541c164339"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "7ad3b742c0fa08633cc7ad74bc4290c9abd79fe8333754adb3436efdcae44cc4",
          "issue": "issue_f98291d717541c164339"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "80b6ae102c88a785fa655bd060a164ee98b1c2ac97942c5f65a4a31c1385fc94",
          "issue": "issue_9f8155de3b8ec13c1bf6"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "cfb4137bb72ecf3418d4d47ae3572c5abdd30b84eb4fbb240b69eea9ed6bf965",
          "issue": "issue_9f8155de3b8ec13c1bf6"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "8588108e4744cf97fc23ff42341489b2ee56ab127d23333041321e49c80071c6",
          "issue": "issue_7d7c229b3ee5dba24790"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "06636f7d1badb0710c48d72b2b94cf8c17a88b91f48d9abac37d4646230db5e3",
          "issue": "issue_7d7c229b3ee5dba24790"
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
          "detail_sha256": "9cac0c0e88385554e6dea16d58443cda1220ced88d260eec3d763ebcbe2c72fb",
          "issue": "issue_7d7c229b3ee5dba24790"
        },
        {
          "reason": "ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "20f037ba1c7aa0f488841d2ccda8d0825a0c33eef209772a83f417d8691ed68e",
          "issue": "issue_7d7c229b3ee5dba24790"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_26ecdbc01ee2b559e2ce",
        "fact": "fact_908c4e5a6f26e6583014",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_2d6bc8d76750e6f41a40",
        "fact": "fact_3724731856b3197fed57",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_3724731856b3197fed57",
        "object_or_effect": "o_8d224b68e9146cf93a50",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_4bb381c785a594c84bbe",
        "object_or_effect": "w_de09ff57d58e4e45437a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_de09ff57d58e4e45437a",
        "grounded": true
      },
      {
        "id": "fact_5e1873de8e28ddbb0bf2",
        "object_or_effect": "w_b2b685d2b32a108ec217",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b2b685d2b32a108ec217",
        "grounded": true
      },
      {
        "id": "fact_908c4e5a6f26e6583014",
        "object_or_effect": "o_1a982714af5255bbbb24",
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
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "both_usable",
        "answer": "unsat",
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
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 2
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 1,
      "category_ambiguous_or_outside_supported_task": 4,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 3,
      "ambiguous_confirmation_not_a_risk_judgment": 1
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

## RQ1_a906c0b62c0b

证据目录 run/members/RQ1_a906c0b62c0b/attempt_1/，报告哈希 820cbfbf1ba0ebb39f690c5f3ad4dd7d92d531578ac7b2506d82a1d7ceeadca9

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
    "已确认消费/覆盖诊断 category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": false,
    "paired_id": "RQ1_1a94f7866801",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "65f52e608c84d9bb515cfed5e6eee526ac807eb3df0353fcb2c7bd72d431a3f4",
          "issue": "issue_eb16eaaa0920684af99a"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a794749f03777ae8724d5fb1f4200f89027440539769a3d75c0f11fa9914ad03",
          "issue": "issue_eb16eaaa0920684af99a"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "df9489fe5465d2adde23bba9b3ad5fa329e418cdf44ad87b8d7701470051166c",
          "issue": "issue_56b876ed37ece288b9dd"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "5dcba10ce30aa9572cccfee6ff1e24f1c382c152f1fd203f75d94169b240e6e4",
          "issue": "issue_56b876ed37ece288b9dd"
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
          "detail_sha256": "2f3a37ae31a7beed920d3ffcbb0710021a967a634342f1a585aba99401a07536",
          "issue": "issue_e894770790422930eeab"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "e65e158172d0f748ff8fedbd1fe1b656ffc0a6ee1890884790e01b265edbef13",
          "issue": "issue_e894770790422930eeab"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_1d25ae869a06f0c3ae41",
        "fact": "fact_7c5b14e84da6ce0909d5",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_7c5b14e84da6ce0909d5",
        "object_or_effect": "o_67b3a82a324ff2668ded",
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
      "unbound_or_inapplicable_seed": 2,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 1,
      "core_unresolved_retained_for_investigation": 1,
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
      "no_effect_in_scope": 303,
      "source_task_reading": 49,
      "covered_holder_grant": 3
    }
  }
}
```

## RQ1_aaeb3f57cfd0

证据目录 run/members/RQ1_aaeb3f57cfd0/attempt_1/，报告哈希 7ddccee931da951e6fe7d1396ba1d54686386dae05f8375fe0eeb7530d90d6e0

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
    "last1164 未知转有效阴性",
    "decision_only 未知转有效阴性"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary",
    "未决类别 FCR-DESTROY,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": false,
    "paired_id": "RQ1_20dfd0c54b94",
    "state": "not_detected",
    "changes": {
      "v32": {
        "before": "not_detected",
        "after": "not_detected"
      },
      "last1164": {
        "before": "unsupported",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "bf37a4920b3965c758b529663cb892205e13d490233e45097e4b15b5139bd964",
          "issue": "issue_5233576fdc89700efc41"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1509106288842285b8b4e32d12f3229c81de6745707cfae2b790a18d40f1a968",
          "issue": "issue_5233576fdc89700efc41"
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
          "detail_sha256": "93f341c66e9c3fb94e9484fbc982242e137b446e8ca7601aa5e1ab840e94e226",
          "issue": "issue_5b13ecd929115d6c5af1"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "47b57af32bd5a5e842ff5452478f078104d95a07c1d6acee5585bcc8175baa52",
          "issue": "issue_5b13ecd929115d6c5af1"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_085ef8a80b70e343ca16",
        "fact": "fact_3bfedba6c4e7ed6044cf",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_7b013651deee8f327954",
        "fact": "fact_76ec3d60f013a4090faf",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_9bd54d72b42253f39a94",
        "fact": "fact_7fdc1013cbda4ef8c4d8",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_bb4aeb7f123fc0293fc4",
        "fact": "fact_568003f946c85dfaf2a4",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_d42bc17b1d23b23b70d0",
        "fact": "fact_26f9530e8fd7e7701b22",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_037133f859b5a56c9183",
        "object_or_effect": "w_48ac4a637031a7c45091",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_48ac4a637031a7c45091",
        "grounded": true
      },
      {
        "id": "fact_146c37b4f4906e599613",
        "object_or_effect": "w_d89b11e8992409804f52",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_d89b11e8992409804f52",
        "grounded": true
      },
      {
        "id": "fact_2138de2c72571483ccbd",
        "object_or_effect": "w_22c5a5a499272c691611",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_22c5a5a499272c691611",
        "grounded": true
      },
      {
        "id": "fact_26f9530e8fd7e7701b22",
        "object_or_effect": "o_cf183eff7b8eb37bf425",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_3bfedba6c4e7ed6044cf",
        "object_or_effect": "o_cec6e9f82fd25143866b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_568003f946c85dfaf2a4",
        "object_or_effect": "o_619608534ff36ad4c141",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_623fd94bc7bb1636fd27",
        "object_or_effect": "w_e6bf05681237713dadcf",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_e6bf05681237713dadcf",
        "grounded": true
      },
      {
        "id": "fact_76ec3d60f013a4090faf",
        "object_or_effect": "o_265034e734799d0bf4bc",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_77557806adf09fbf3eb0",
        "object_or_effect": "w_56f9a71c8790b1416e54",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_56f9a71c8790b1416e54",
        "grounded": true
      },
      {
        "id": "fact_7fdc1013cbda4ef8c4d8",
        "object_or_effect": "o_9dc17c47722d69feb41e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_9147fa9600577f162d5d",
        "object_or_effect": "w_063549443a3a720d4d88",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_063549443a3a720d4d88",
        "grounded": true
      },
      {
        "id": "fact_94bdb60dc06862d28abf",
        "object_or_effect": "w_c0bcaca0c954cea38316",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c0bcaca0c954cea38316",
        "grounded": true
      },
      {
        "id": "fact_983ad876abf3ec55e6b2",
        "object_or_effect": "w_ce61a8d3c56728e8489e",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_ce61a8d3c56728e8489e",
        "grounded": true
      },
      {
        "id": "fact_bba04894d74ff1779911",
        "object_or_effect": "w_591406b3b830de0030cd",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_591406b3b830de0030cd",
        "grounded": true
      },
      {
        "id": "fact_d68c1060e4dc99970773",
        "object_or_effect": "w_9a59687fb7f0fd4d4f88",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_9a59687fb7f0fd4d4f88",
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 13
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 14
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 13
      },
      {
        "label": "baseline_usable",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 12
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 12
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 5
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
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 12
      },
      {
        "label": "prefix_reachability",
        "answer": "unsat",
        "count": 6
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 6,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
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
      "no_effect_in_scope": 177,
      "source_task_reading": 12,
      "scope_missing": 2,
      "covered_holder_grant": 4
    }
  }
}
```

## RQ1_ad46f524b21d

证据目录 run/members/RQ1_ad46f524b21d/attempt_1/，报告哈希 f1b05fe97e9e7ddd712c2f0bd323114627ff5d8f342009f0fdd3873c40448692

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed",
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
      "normalization_diagnostics": [
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "2afe6b64dac47cd2225df41bec0066b0afe894b573b544478972bbc6839c5bfd",
          "issue": "issue_78c822aa9e43ee34afd5"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "12be4efbc6208a5f74582ff81a0135b93518c259ceccf6afdf60c7702c6c1e2d",
          "issue": "issue_78c822aa9e43ee34afd5"
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
        "support": "support_2a467744c60206181f75",
        "fact": "fact_20cdfc0eca4e8461c647",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_33d55a16e1d23b9a9566",
        "fact": "fact_cc65f26e928792f63aaa",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_ba30d09ad910d58c7e14",
        "fact": "fact_13d983973da3acbc578d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_00009d0cc3c64098c4d1",
        "object_or_effect": "w_60a4d7c9b784f6c1258b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_60a4d7c9b784f6c1258b",
        "grounded": true
      },
      {
        "id": "fact_00508a38fbfb6e7d52dd",
        "object_or_effect": "w_4bafd88b9c2a3239d9de",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4bafd88b9c2a3239d9de",
        "grounded": true
      },
      {
        "id": "fact_026e1bca6a4cb6c14f64",
        "object_or_effect": "w_b7599dbd3f34b3ecbd00",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b7599dbd3f34b3ecbd00",
        "grounded": true
      },
      {
        "id": "fact_027d77edcc651ea8f4b9",
        "object_or_effect": "w_d81e0d2f1dfb5d11098e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d81e0d2f1dfb5d11098e",
        "grounded": true
      },
      {
        "id": "fact_02ecc0338e9c92db4aec",
        "object_or_effect": "w_1effff7e5054ff4b2825",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1effff7e5054ff4b2825",
        "grounded": true
      },
      {
        "id": "fact_0309e7f7ef55bec1d06c",
        "object_or_effect": "w_82e40b3a85ab58a28173",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_82e40b3a85ab58a28173",
        "grounded": true
      },
      {
        "id": "fact_04d0d42dc4525ca80ce6",
        "object_or_effect": "w_d8bf2bf546a9db19e25d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d8bf2bf546a9db19e25d",
        "grounded": true
      },
      {
        "id": "fact_05759beeea9b3edf3aa4",
        "object_or_effect": "w_75eb4f549108d1d75373",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_75eb4f549108d1d75373",
        "grounded": true
      },
      {
        "id": "fact_05cd97958ea4b94a776e",
        "object_or_effect": "w_9fbcc13a14d7aa74ddc9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9fbcc13a14d7aa74ddc9",
        "grounded": true
      },
      {
        "id": "fact_067a264308526e7dc82f",
        "object_or_effect": "w_1a0518ab2864e8c0c3ba",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1a0518ab2864e8c0c3ba",
        "grounded": true
      },
      {
        "id": "fact_073723616f244beca13a",
        "object_or_effect": "w_8bb7211e5c2d83996d9d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8bb7211e5c2d83996d9d",
        "grounded": true
      },
      {
        "id": "fact_086ed27db92a3cfcd54b",
        "object_or_effect": "w_aeef294865c6f5e0052f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_aeef294865c6f5e0052f",
        "grounded": true
      },
      {
        "id": "fact_089989c1cae2e264137b",
        "object_or_effect": "w_032a4d3c6cf3170dd4b1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_032a4d3c6cf3170dd4b1",
        "grounded": true
      },
      {
        "id": "fact_09b761c7c66ac15016cc",
        "object_or_effect": "w_3cea2e3f9281f4545c15",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3cea2e3f9281f4545c15",
        "grounded": true
      },
      {
        "id": "fact_0aa0cc8b4cdaeea78622",
        "object_or_effect": "w_5b926a2d4ecef00a4a68",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5b926a2d4ecef00a4a68",
        "grounded": true
      },
      {
        "id": "fact_0aaf256c8396353c636a",
        "object_or_effect": "w_277864f58d06fcc35439",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_277864f58d06fcc35439",
        "grounded": true
      },
      {
        "id": "fact_0acc5e1c76cce3d7950b",
        "object_or_effect": "w_5cdef172dd666b985a19",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5cdef172dd666b985a19",
        "grounded": true
      },
      {
        "id": "fact_0cdbbf82534a73ee4eda",
        "object_or_effect": "w_2662f2a7b5e41a8e6612",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2662f2a7b5e41a8e6612",
        "grounded": true
      },
      {
        "id": "fact_0df5a0e5d0d12f3ccd49",
        "object_or_effect": "w_c138c7101ab43bff7990",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c138c7101ab43bff7990",
        "grounded": true
      },
      {
        "id": "fact_0e6dcd9a4975b1bdafcb",
        "object_or_effect": "w_f399e5852b300e3408a2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f399e5852b300e3408a2",
        "grounded": true
      },
      {
        "id": "fact_0f24dcad5c282736f363",
        "object_or_effect": "w_1b4852116ced872c78ac",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1b4852116ced872c78ac",
        "grounded": true
      },
      {
        "id": "fact_10d223b393da760c2a55",
        "object_or_effect": "w_342c3bf9c698e040e9b3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_342c3bf9c698e040e9b3",
        "grounded": true
      },
      {
        "id": "fact_111af28ebc001f80b0b6",
        "object_or_effect": "w_5c8c7ba55162d04a3f72",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5c8c7ba55162d04a3f72",
        "grounded": true
      },
      {
        "id": "fact_12eca3adf0fdc59002c2",
        "object_or_effect": "w_b560b101d138d73800b4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b560b101d138d73800b4",
        "grounded": true
      },
      {
        "id": "fact_13d983973da3acbc578d",
        "object_or_effect": "o_38fd94858812b7aacefc",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_148a14631bb06c932d7a",
        "object_or_effect": "w_d2b274d0ca9594986bd9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d2b274d0ca9594986bd9",
        "grounded": true
      },
      {
        "id": "fact_152c31f6089f8e646a00",
        "object_or_effect": "w_95856fe69dc71497c570",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_95856fe69dc71497c570",
        "grounded": true
      },
      {
        "id": "fact_17553021bf312754f9cb",
        "object_or_effect": "w_09dc7312911b2d001540",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_09dc7312911b2d001540",
        "grounded": true
      },
      {
        "id": "fact_19a052766a50b215128d",
        "object_or_effect": "w_79b3aaa17f1688c82ec1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_79b3aaa17f1688c82ec1",
        "grounded": true
      },
      {
        "id": "fact_1a9e18d41cf654dde425",
        "object_or_effect": "w_373325d74b5bdd3a5e93",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_373325d74b5bdd3a5e93",
        "grounded": true
      },
      {
        "id": "fact_1c441d76edc0126ef23f",
        "object_or_effect": "w_9888d93def3ca05915a0",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9888d93def3ca05915a0",
        "grounded": true
      },
      {
        "id": "fact_1d3b7548479b61a48a9e",
        "object_or_effect": "w_e2c4452b2456e9a1d169",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e2c4452b2456e9a1d169",
        "grounded": true
      },
      {
        "id": "fact_1ed0f8aefb739ce5c0c5",
        "object_or_effect": "w_783a304706d58149fd72",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_783a304706d58149fd72",
        "grounded": true
      },
      {
        "id": "fact_1f75d87ef18b656ee65a",
        "object_or_effect": "w_223cd6d67d119c88554f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_223cd6d67d119c88554f",
        "grounded": true
      },
      {
        "id": "fact_1fe183e73bc86259573b",
        "object_or_effect": "w_f8fd02a576ddafe759f2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f8fd02a576ddafe759f2",
        "grounded": true
      },
      {
        "id": "fact_1fe740e5b69209575b37",
        "object_or_effect": "w_569b18182a6d5a9154dc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_569b18182a6d5a9154dc",
        "grounded": true
      },
      {
        "id": "fact_20cdfc0eca4e8461c647",
        "object_or_effect": "o_bd44957b22192ce20e6c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_23f9140763db39332dbf",
        "object_or_effect": "w_62e8b934b038b3c90006",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_62e8b934b038b3c90006",
        "grounded": true
      },
      {
        "id": "fact_245c4885b98a0cc1c879",
        "object_or_effect": "w_4f42a4e3c8406eeea544",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4f42a4e3c8406eeea544",
        "grounded": true
      },
      {
        "id": "fact_25dde6921d5f220b172d",
        "object_or_effect": "w_b322d8beb8129dbb4873",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b322d8beb8129dbb4873",
        "grounded": true
      },
      {
        "id": "fact_276126571064887fedfb",
        "object_or_effect": "w_34ffe8f135f95be4a3e5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_34ffe8f135f95be4a3e5",
        "grounded": true
      },
      {
        "id": "fact_27f75b3196273b9d639a",
        "object_or_effect": "w_b7acc5a7b9ac5d3af772",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b7acc5a7b9ac5d3af772",
        "grounded": true
      },
      {
        "id": "fact_28332f787ef226318f83",
        "object_or_effect": "w_2e01b9406a778a373606",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2e01b9406a778a373606",
        "grounded": true
      },
      {
        "id": "fact_2881e71c9210d1af5d1e",
        "object_or_effect": "w_88d11d3194bbfc199a9c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_88d11d3194bbfc199a9c",
        "grounded": true
      },
      {
        "id": "fact_28c130c613bbe3d3a209",
        "object_or_effect": "w_1463903bef5bc4dec72b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1463903bef5bc4dec72b",
        "grounded": true
      },
      {
        "id": "fact_2b0ce683161b1f2cb768",
        "object_or_effect": "w_85c2aad1b53903218bc2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_85c2aad1b53903218bc2",
        "grounded": true
      },
      {
        "id": "fact_2b67391299d6520c7393",
        "object_or_effect": "w_a8c6cb0426f96cdb2724",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a8c6cb0426f96cdb2724",
        "grounded": true
      },
      {
        "id": "fact_2c1287deb86f3945166f",
        "object_or_effect": "w_e09fee65d085a31afac2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e09fee65d085a31afac2",
        "grounded": true
      },
      {
        "id": "fact_2c924818deb48d280f76",
        "object_or_effect": "w_7d7b78719776a8df6fe8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7d7b78719776a8df6fe8",
        "grounded": true
      },
      {
        "id": "fact_2db0ad370ad3dd4b6f99",
        "object_or_effect": "w_42b7469109c5bfbaf664",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_42b7469109c5bfbaf664",
        "grounded": true
      },
      {
        "id": "fact_2e04bfaa2010d6e18f27",
        "object_or_effect": "w_7521355ccd1f8779b1d7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7521355ccd1f8779b1d7",
        "grounded": true
      },
      {
        "id": "fact_2e2d3e83f66d338f775c",
        "object_or_effect": "w_f4ff63e6c9d2bb141bbc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f4ff63e6c9d2bb141bbc",
        "grounded": true
      },
      {
        "id": "fact_2e60f37d791cc56d3290",
        "object_or_effect": "w_5bcd8f0fd6680c4fad2d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5bcd8f0fd6680c4fad2d",
        "grounded": true
      },
      {
        "id": "fact_2e9ae0411bf48ad7da76",
        "object_or_effect": "w_e0d2fe27371507a8c1d7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e0d2fe27371507a8c1d7",
        "grounded": true
      },
      {
        "id": "fact_2ee407066f506b8bb772",
        "object_or_effect": "w_807b4eef59313735e02b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_807b4eef59313735e02b",
        "grounded": true
      },
      {
        "id": "fact_2f29e71c9d2fe7fa1ecf",
        "object_or_effect": "w_43a0f0d0a42e4ec3a09f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_43a0f0d0a42e4ec3a09f",
        "grounded": true
      },
      {
        "id": "fact_3209eb181e736e7754c0",
        "object_or_effect": "w_d195c23f4699d8fbe6e3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d195c23f4699d8fbe6e3",
        "grounded": true
      },
      {
        "id": "fact_32390f05393035294a88",
        "object_or_effect": "w_d17daf2ffaa762206628",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d17daf2ffaa762206628",
        "grounded": true
      },
      {
        "id": "fact_3276a36104ce47cdd5fa",
        "object_or_effect": "w_628fbf7d68f798c96209",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_628fbf7d68f798c96209",
        "grounded": true
      },
      {
        "id": "fact_3364746af80c6b03ab8e",
        "object_or_effect": "w_35e1db210a3b13f3239e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_35e1db210a3b13f3239e",
        "grounded": true
      },
      {
        "id": "fact_33e267f5dfe74e4ea3f9",
        "object_or_effect": "w_8eadd979969eda3ab3dd",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8eadd979969eda3ab3dd",
        "grounded": true
      },
      {
        "id": "fact_341ea90be71204a6984c",
        "object_or_effect": "w_aa8375f2af580b21dc7c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_aa8375f2af580b21dc7c",
        "grounded": true
      },
      {
        "id": "fact_382e2b7ce0ebdca21068",
        "object_or_effect": "w_e2214f819c7e35f56f07",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e2214f819c7e35f56f07",
        "grounded": true
      },
      {
        "id": "fact_395c2953452eda152c11",
        "object_or_effect": "w_f0e05cc476cb9ec70463",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f0e05cc476cb9ec70463",
        "grounded": true
      },
      {
        "id": "fact_3ac3bfb126b1509ac4fc",
        "object_or_effect": "w_3937b8fdfe44cac2be8b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3937b8fdfe44cac2be8b",
        "grounded": true
      },
      {
        "id": "fact_3b60ef6eeb4d4707f171",
        "object_or_effect": "w_f1e390092f39a1145e61",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f1e390092f39a1145e61",
        "grounded": true
      },
      {
        "id": "fact_3c673d45d0d4446cc940",
        "object_or_effect": "w_7eb9410b131bb698da8b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7eb9410b131bb698da8b",
        "grounded": true
      },
      {
        "id": "fact_3c7acdd4ebe95b94b3fc",
        "object_or_effect": "w_43af086816db193aea88",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_43af086816db193aea88",
        "grounded": true
      },
      {
        "id": "fact_3d231c5ab5d3f8f65a31",
        "object_or_effect": "w_4629aaa4770a79d5eeca",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4629aaa4770a79d5eeca",
        "grounded": true
      },
      {
        "id": "fact_3d2cf63c8043df76a230",
        "object_or_effect": "w_5a5ddfda1f99c262f8b1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5a5ddfda1f99c262f8b1",
        "grounded": true
      },
      {
        "id": "fact_3d80f4ff83e5e764e432",
        "object_or_effect": "w_3454fc6ff6fd63b907d4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3454fc6ff6fd63b907d4",
        "grounded": true
      },
      {
        "id": "fact_3e758325c31754164149",
        "object_or_effect": "w_8ee03aad66bd44477ae5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8ee03aad66bd44477ae5",
        "grounded": true
      },
      {
        "id": "fact_3e853c991b4c2fc2bb8f",
        "object_or_effect": "w_be680dcc24bd9dfa6aaf",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_be680dcc24bd9dfa6aaf",
        "grounded": true
      },
      {
        "id": "fact_3f136af4c101b63738e5",
        "object_or_effect": "w_f656106b3cbf37f2ac95",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f656106b3cbf37f2ac95",
        "grounded": true
      },
      {
        "id": "fact_40da6687a556c6906b3d",
        "object_or_effect": "w_1f078b20653616c2df64",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1f078b20653616c2df64",
        "grounded": true
      },
      {
        "id": "fact_40e9eb01445005dd8e1d",
        "object_or_effect": "w_10ccba25d99ff7f57932",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_10ccba25d99ff7f57932",
        "grounded": true
      },
      {
        "id": "fact_416b701a78c8f7b32869",
        "object_or_effect": "w_331624a45ed315a97d41",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_331624a45ed315a97d41",
        "grounded": true
      },
      {
        "id": "fact_418d10cb19e72da9f734",
        "object_or_effect": "w_107eefe4164db56f5618",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_107eefe4164db56f5618",
        "grounded": true
      },
      {
        "id": "fact_424e8d3c0fdbecf9b4b6",
        "object_or_effect": "w_6680047b429fedfa6794",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6680047b429fedfa6794",
        "grounded": true
      },
      {
        "id": "fact_43bd4796a1e1d3980393",
        "object_or_effect": "w_ed8e46230fcdaca60942",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ed8e46230fcdaca60942",
        "grounded": true
      },
      {
        "id": "fact_44074e35da3c3b34d6b1",
        "object_or_effect": "w_426632da707f3514b470",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_426632da707f3514b470",
        "grounded": true
      },
      {
        "id": "fact_4422155c6373392af5aa",
        "object_or_effect": "w_a1a3167dea44b84facd5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a1a3167dea44b84facd5",
        "grounded": true
      },
      {
        "id": "fact_457eda5b33a1da55bae6",
        "object_or_effect": "w_c4074918b84164103e2b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c4074918b84164103e2b",
        "grounded": true
      },
      {
        "id": "fact_458dade49ebaac7c353d",
        "object_or_effect": "w_45b1d9382852ea28fa69",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_45b1d9382852ea28fa69",
        "grounded": true
      },
      {
        "id": "fact_458f95d0fe9b364978e0",
        "object_or_effect": "w_a448f4cfa3dda020f359",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a448f4cfa3dda020f359",
        "grounded": true
      },
      {
        "id": "fact_463ede4535bb314adbda",
        "object_or_effect": "w_80679e85f340854a5d6b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_80679e85f340854a5d6b",
        "grounded": true
      },
      {
        "id": "fact_4664483f13cc269283a1",
        "object_or_effect": "w_a98e93f35e574b803af6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a98e93f35e574b803af6",
        "grounded": true
      },
      {
        "id": "fact_46c71250d379ca64dc76",
        "object_or_effect": "w_15874ee07d95a59d9042",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_15874ee07d95a59d9042",
        "grounded": true
      },
      {
        "id": "fact_46e486ab9d646564bcf6",
        "object_or_effect": "w_1a15fb4f94c91f5ad3ad",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1a15fb4f94c91f5ad3ad",
        "grounded": true
      },
      {
        "id": "fact_47b49bb77fc705267e81",
        "object_or_effect": "w_4028c433cb84d7070bc9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4028c433cb84d7070bc9",
        "grounded": true
      },
      {
        "id": "fact_48be1dfc1e6a76121cf7",
        "object_or_effect": "w_4d91b702de2a51264de7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4d91b702de2a51264de7",
        "grounded": true
      },
      {
        "id": "fact_4a022c709b1bcd5e5592",
        "object_or_effect": "w_ee86cbc96e6a69f7a148",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ee86cbc96e6a69f7a148",
        "grounded": true
      },
      {
        "id": "fact_4a66712b66662a1579ce",
        "object_or_effect": "w_031df5605dff5e3a0ff4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_031df5605dff5e3a0ff4",
        "grounded": true
      },
      {
        "id": "fact_4ac56afe752d5be77c41",
        "object_or_effect": "w_6e2910f4f7f314523f4e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6e2910f4f7f314523f4e",
        "grounded": true
      },
      {
        "id": "fact_4b7bb71f9e865395b0bb",
        "object_or_effect": "w_73cf19b2f0f4eef7fc14",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_73cf19b2f0f4eef7fc14",
        "grounded": true
      },
      {
        "id": "fact_4d6fbe3fda75cf5fde51",
        "object_or_effect": "w_d9024b919720d7231acb",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d9024b919720d7231acb",
        "grounded": true
      },
      {
        "id": "fact_4f4a23fc049919fb0801",
        "object_or_effect": "w_32496545b5a57698bfc9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_32496545b5a57698bfc9",
        "grounded": true
      },
      {
        "id": "fact_553a7efb5bd4639d692b",
        "object_or_effect": "w_dec89001ed48da3c9ab9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_dec89001ed48da3c9ab9",
        "grounded": true
      },
      {
        "id": "fact_554c0af3860cb9e97f21",
        "object_or_effect": "w_a5b1bcb06af0c73a0295",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a5b1bcb06af0c73a0295",
        "grounded": true
      },
      {
        "id": "fact_55a18ee8c38543187b28",
        "object_or_effect": "w_1faafcedd30f6d6f0197",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1faafcedd30f6d6f0197",
        "grounded": true
      },
      {
        "id": "fact_55f7dbad070e86c50cdd",
        "object_or_effect": "w_2999313ccb1445c4fe33",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2999313ccb1445c4fe33",
        "grounded": true
      },
      {
        "id": "fact_5796b4671e8d96762c9d",
        "object_or_effect": "w_44f23ac5f84a61910eb4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_44f23ac5f84a61910eb4",
        "grounded": true
      },
      {
        "id": "fact_585ae222992b758599e0",
        "object_or_effect": "w_d03f3a52dfbc6d94a248",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d03f3a52dfbc6d94a248",
        "grounded": true
      },
      {
        "id": "fact_58b1e338d5883df9f11c",
        "object_or_effect": "w_a2aa714248ecdf0de52b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a2aa714248ecdf0de52b",
        "grounded": true
      },
      {
        "id": "fact_59468093559653209a89",
        "object_or_effect": "w_a30d0e2927f43c769c27",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a30d0e2927f43c769c27",
        "grounded": true
      },
      {
        "id": "fact_5a170146bfff8811fdbf",
        "object_or_effect": "w_c6d6776c859c3f842285",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c6d6776c859c3f842285",
        "grounded": true
      },
      {
        "id": "fact_5a968a8b94b28c2b3ece",
        "object_or_effect": "w_c6e8d2d148b893678170",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c6e8d2d148b893678170",
        "grounded": true
      },
      {
        "id": "fact_5aece032410c7d42999d",
        "object_or_effect": "w_1edcd55dad0f7e2817a3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1edcd55dad0f7e2817a3",
        "grounded": true
      },
      {
        "id": "fact_5b2c361fb2c7180427a9",
        "object_or_effect": "w_b21615af6223040b4ab8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b21615af6223040b4ab8",
        "grounded": true
      },
      {
        "id": "fact_5c0ff12cb2416e11b69a",
        "object_or_effect": "w_5590ef6b76d7e551242a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5590ef6b76d7e551242a",
        "grounded": true
      },
      {
        "id": "fact_5c529292605a09bf4dd7",
        "object_or_effect": "w_70167daab51e70bcf751",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_70167daab51e70bcf751",
        "grounded": true
      },
      {
        "id": "fact_5c5ef299dd95f1877665",
        "object_or_effect": "w_b1ec1c12cfef0216671e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b1ec1c12cfef0216671e",
        "grounded": true
      },
      {
        "id": "fact_5d475e3e379b9cd673c7",
        "object_or_effect": "w_6efbd26e4b48b7fde6eb",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6efbd26e4b48b7fde6eb",
        "grounded": true
      },
      {
        "id": "fact_5df4cd54b0553e580cfd",
        "object_or_effect": "w_780ceacaa07f7b5dad41",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_780ceacaa07f7b5dad41",
        "grounded": true
      },
      {
        "id": "fact_5e5fa12f00bbd2c6302e",
        "object_or_effect": "w_7ce163b6973fedca19c3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7ce163b6973fedca19c3",
        "grounded": true
      },
      {
        "id": "fact_5f518917a3dce417a0e4",
        "object_or_effect": "w_89b0580bbccc40ec0ee6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_89b0580bbccc40ec0ee6",
        "grounded": true
      },
      {
        "id": "fact_6054b06c6c35392124e4",
        "object_or_effect": "w_25351a49322da55cd636",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_25351a49322da55cd636",
        "grounded": true
      },
      {
        "id": "fact_608d5b7d4f4abfa16a7b",
        "object_or_effect": "w_83a510dba4bc9800ccf3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_83a510dba4bc9800ccf3",
        "grounded": true
      },
      {
        "id": "fact_6109160600044781b6dd",
        "object_or_effect": "w_38d7ff5f093bc0d08bab",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_38d7ff5f093bc0d08bab",
        "grounded": true
      },
      {
        "id": "fact_6118990dedea7b87ab88",
        "object_or_effect": "w_cf512d8be8f3a8d8721c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cf512d8be8f3a8d8721c",
        "grounded": true
      },
      {
        "id": "fact_6147dc84d9e0209e2502",
        "object_or_effect": "w_32b52f44445cddb4ac1c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_32b52f44445cddb4ac1c",
        "grounded": true
      },
      {
        "id": "fact_61ff99dae907f18018f3",
        "object_or_effect": "w_9cdfb5dd31e005e54215",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9cdfb5dd31e005e54215",
        "grounded": true
      },
      {
        "id": "fact_622ff7e85f5bcc6f47d0",
        "object_or_effect": "w_3682a61d969aaaa9815c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3682a61d969aaaa9815c",
        "grounded": true
      },
      {
        "id": "fact_633012737528cf84cefc",
        "object_or_effect": "w_e031bb25e0ca7df0ca89",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e031bb25e0ca7df0ca89",
        "grounded": true
      },
      {
        "id": "fact_64dd8eadc7743f8755a8",
        "object_or_effect": "w_10cca445e5292626ec7b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_10cca445e5292626ec7b",
        "grounded": true
      },
      {
        "id": "fact_6836267e652b3d012033",
        "object_or_effect": "w_21ead9b60d8a17eefd6d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_21ead9b60d8a17eefd6d",
        "grounded": true
      },
      {
        "id": "fact_6912e18b44e530b3aa9a",
        "object_or_effect": "w_997ebc39dacaed8359bd",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_997ebc39dacaed8359bd",
        "grounded": true
      },
      {
        "id": "fact_69cedf6f2ea8998ed3d8",
        "object_or_effect": "w_4b17e72a6e0b84d69597",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4b17e72a6e0b84d69597",
        "grounded": true
      },
      {
        "id": "fact_6a128f4e74bd01da1dd5",
        "object_or_effect": "w_32f04b0dab4f30e4c2ac",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_32f04b0dab4f30e4c2ac",
        "grounded": true
      },
      {
        "id": "fact_6b875b07eb93bb1debb7",
        "object_or_effect": "w_697e7a44ba810d4e89d0",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_697e7a44ba810d4e89d0",
        "grounded": true
      },
      {
        "id": "fact_6be83d3c3bacc6af42dc",
        "object_or_effect": "w_722bc226546d1e575b0a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_722bc226546d1e575b0a",
        "grounded": true
      },
      {
        "id": "fact_6e6adda0dcca8261b7ff",
        "object_or_effect": "w_ddb303c37dd58c55c42b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ddb303c37dd58c55c42b",
        "grounded": true
      },
      {
        "id": "fact_6eaf387fdbebefe2eb3f",
        "object_or_effect": "w_6dad06f50d7668c6609b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6dad06f50d7668c6609b",
        "grounded": true
      },
      {
        "id": "fact_70fa897daa499343e30f",
        "object_or_effect": "w_9360d5883d47137a798f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9360d5883d47137a798f",
        "grounded": true
      },
      {
        "id": "fact_7100bf347f73d3147a1a",
        "object_or_effect": "w_a896507585ab501276bc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a896507585ab501276bc",
        "grounded": true
      },
      {
        "id": "fact_712f760d81ce2111a69c",
        "object_or_effect": "w_6afe6e2fcb345066065f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6afe6e2fcb345066065f",
        "grounded": true
      },
      {
        "id": "fact_718125da042e77f8e9b4",
        "object_or_effect": "w_2fdce23ded3a8b9624d2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2fdce23ded3a8b9624d2",
        "grounded": true
      },
      {
        "id": "fact_71a7ff7f7e09019350ae",
        "object_or_effect": "w_3d8a24f705a1efed6824",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3d8a24f705a1efed6824",
        "grounded": true
      },
      {
        "id": "fact_71f3fe66882448500a4d",
        "object_or_effect": "w_6038a6d0b99f366f688b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6038a6d0b99f366f688b",
        "grounded": true
      },
      {
        "id": "fact_72528822f2ae8d45a03a",
        "object_or_effect": "w_b4f3278f9408b0439137",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b4f3278f9408b0439137",
        "grounded": true
      },
      {
        "id": "fact_742565d11efeacf071d3",
        "object_or_effect": "w_d332f3765b5c73ca4e70",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d332f3765b5c73ca4e70",
        "grounded": true
      },
      {
        "id": "fact_74d4107cd51616c3f3bd",
        "object_or_effect": "w_3f05dc0365ae0276c42d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3f05dc0365ae0276c42d",
        "grounded": true
      },
      {
        "id": "fact_75219ca6c96e3a697850",
        "object_or_effect": "w_de972ee4f460ab400310",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_de972ee4f460ab400310",
        "grounded": true
      },
      {
        "id": "fact_75a4a51e5c9c840e7e5f",
        "object_or_effect": "w_9ea0583ba3786cb44b5a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9ea0583ba3786cb44b5a",
        "grounded": true
      },
      {
        "id": "fact_75ded21ef85e3c6be92f",
        "object_or_effect": "w_c3702099ffb606519a9a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c3702099ffb606519a9a",
        "grounded": true
      },
      {
        "id": "fact_7702eb2d8c4f4b341ebc",
        "object_or_effect": "w_ea33cad31493607c5260",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ea33cad31493607c5260",
        "grounded": true
      },
      {
        "id": "fact_77def10f08b3473911f7",
        "object_or_effect": "w_e6b299da9cb209963c58",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e6b299da9cb209963c58",
        "grounded": true
      },
      {
        "id": "fact_7811e9a14b2440832ac9",
        "object_or_effect": "w_db806aeba43c3aa68f3a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_db806aeba43c3aa68f3a",
        "grounded": true
      },
      {
        "id": "fact_78b304ad1f4cda506019",
        "object_or_effect": "w_01e06d5612f9f54351ba",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_01e06d5612f9f54351ba",
        "grounded": true
      },
      {
        "id": "fact_78d0a13e9bb6c97ea0e3",
        "object_or_effect": "w_be09ea089502e3db0a17",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_be09ea089502e3db0a17",
        "grounded": true
      },
      {
        "id": "fact_79c6a4d2ea2d7b8e581e",
        "object_or_effect": "w_f581cac174dcef4c65aa",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f581cac174dcef4c65aa",
        "grounded": true
      },
      {
        "id": "fact_7b648054727ffd7c1f17",
        "object_or_effect": "w_38c664d07435da66c2a3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_38c664d07435da66c2a3",
        "grounded": true
      },
      {
        "id": "fact_7d988da0af5ccd4ad742",
        "object_or_effect": "w_ebe75706a1d12e8c8964",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ebe75706a1d12e8c8964",
        "grounded": true
      },
      {
        "id": "fact_7f10aa848394ad8e4880",
        "object_or_effect": "w_a34b99a5890977ece793",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a34b99a5890977ece793",
        "grounded": true
      },
      {
        "id": "fact_7f994147d005251f40ca",
        "object_or_effect": "w_357144fe425b68673828",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_357144fe425b68673828",
        "grounded": true
      },
      {
        "id": "fact_801e9f40ab88ada95db8",
        "object_or_effect": "w_7660c48a27c6a02a692d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7660c48a27c6a02a692d",
        "grounded": true
      },
      {
        "id": "fact_81f395a14c19e39dd5e0",
        "object_or_effect": "w_46a6acb9b4bce08c33cb",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_46a6acb9b4bce08c33cb",
        "grounded": true
      },
      {
        "id": "fact_8232457bb27e49b25464",
        "object_or_effect": "w_72a5b3fe05c26f07245f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_72a5b3fe05c26f07245f",
        "grounded": true
      },
      {
        "id": "fact_82a34099e3628a169b81",
        "object_or_effect": "w_758b8f3e656c0bf3d174",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_758b8f3e656c0bf3d174",
        "grounded": true
      },
      {
        "id": "fact_833b0b82476489466e68",
        "object_or_effect": "w_078800ff14e30ec79636",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_078800ff14e30ec79636",
        "grounded": true
      },
      {
        "id": "fact_847e336fa3f4ef278798",
        "object_or_effect": "w_812acd70eb1aee04901d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_812acd70eb1aee04901d",
        "grounded": true
      },
      {
        "id": "fact_86c8539e97eec8f6d26b",
        "object_or_effect": "w_3a0d459d3abf935abb7e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3a0d459d3abf935abb7e",
        "grounded": true
      },
      {
        "id": "fact_8935313154c049295421",
        "object_or_effect": "w_852bb121cb4cac6d4f48",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_852bb121cb4cac6d4f48",
        "grounded": true
      },
      {
        "id": "fact_8bf8cde43126b21c38ca",
        "object_or_effect": "w_dbc2cf39637deecd1af4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_dbc2cf39637deecd1af4",
        "grounded": true
      },
      {
        "id": "fact_8c001ab204b75522ee37",
        "object_or_effect": "w_f1549e56628f950a0044",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f1549e56628f950a0044",
        "grounded": true
      },
      {
        "id": "fact_8e36f9e6e5f4d660d223",
        "object_or_effect": "w_7c4804fa4469451d304a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7c4804fa4469451d304a",
        "grounded": true
      },
      {
        "id": "fact_8e6b3c48a01529b1afb7",
        "object_or_effect": "w_6f5d970b45c90057e961",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6f5d970b45c90057e961",
        "grounded": true
      },
      {
        "id": "fact_8f9a5c934f607f387ca7",
        "object_or_effect": "w_4daccd2501ebdcfc3cd8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4daccd2501ebdcfc3cd8",
        "grounded": true
      },
      {
        "id": "fact_8ffb370cb4868b4bbfe5",
        "object_or_effect": "w_1b0e6bb9a381453dfeed",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1b0e6bb9a381453dfeed",
        "grounded": true
      },
      {
        "id": "fact_91800509d0a96a6b5eeb",
        "object_or_effect": "w_6fe1bdcfb47e15647e9e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6fe1bdcfb47e15647e9e",
        "grounded": true
      },
      {
        "id": "fact_9225f33bf4fb900eea37",
        "object_or_effect": "w_2cb391fb9f870adb7f20",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2cb391fb9f870adb7f20",
        "grounded": true
      },
      {
        "id": "fact_9265247fd2160fda1db9",
        "object_or_effect": "w_1d4f0f4790a14d2c0b74",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1d4f0f4790a14d2c0b74",
        "grounded": true
      },
      {
        "id": "fact_95419755d347f811eb15",
        "object_or_effect": "w_998d34062b01cb5a5790",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_998d34062b01cb5a5790",
        "grounded": true
      },
      {
        "id": "fact_9616ba6ff6684684500c",
        "object_or_effect": "w_649702ecb141128f99a0",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_649702ecb141128f99a0",
        "grounded": true
      },
      {
        "id": "fact_971da533ef77b7eef47d",
        "object_or_effect": "w_ab7c84f6a80754aeef23",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ab7c84f6a80754aeef23",
        "grounded": true
      },
      {
        "id": "fact_98042828bf6475520567",
        "object_or_effect": "w_296f015885aaef17ad53",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_296f015885aaef17ad53",
        "grounded": true
      },
      {
        "id": "fact_9807ba9be9188d64ce7f",
        "object_or_effect": "w_a6c19a1b35761c62ce99",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a6c19a1b35761c62ce99",
        "grounded": true
      },
      {
        "id": "fact_98d26fcde5600a8bcde3",
        "object_or_effect": "w_be92dbeb9c8d5e0999d3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_be92dbeb9c8d5e0999d3",
        "grounded": true
      },
      {
        "id": "fact_990c04bf2d1bd5f907b9",
        "object_or_effect": "w_c10778437fc76320f708",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c10778437fc76320f708",
        "grounded": true
      },
      {
        "id": "fact_99a9ec02fa33e7c0d7b6",
        "object_or_effect": "w_f01f478c957519624791",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f01f478c957519624791",
        "grounded": true
      },
      {
        "id": "fact_99fa6a27d797573b0e9b",
        "object_or_effect": "w_46a244809cd6313ded82",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_46a244809cd6313ded82",
        "grounded": true
      },
      {
        "id": "fact_9a741b6b21c77e1bd4a6",
        "object_or_effect": "w_58f6f674dce1a5a9d009",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_58f6f674dce1a5a9d009",
        "grounded": true
      },
      {
        "id": "fact_9b1fd2f81ad14c92e256",
        "object_or_effect": "w_6a8beee22ceaa3cca554",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6a8beee22ceaa3cca554",
        "grounded": true
      },
      {
        "id": "fact_9b64a8faa27413b853cd",
        "object_or_effect": "w_94add54c63aa702be689",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_94add54c63aa702be689",
        "grounded": true
      },
      {
        "id": "fact_9bef82e515faa65e1b98",
        "object_or_effect": "w_0c7a614744d4d0e04ba7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0c7a614744d4d0e04ba7",
        "grounded": true
      },
      {
        "id": "fact_9c966519384f10ad6305",
        "object_or_effect": "w_eef7d909fb587102916b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_eef7d909fb587102916b",
        "grounded": true
      },
      {
        "id": "fact_9d39b3d6d4512ee804bb",
        "object_or_effect": "w_fbf64fb795922e569748",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_fbf64fb795922e569748",
        "grounded": true
      },
      {
        "id": "fact_9db7710fd5793ff1477c",
        "object_or_effect": "w_17cdcfcc86f2a005082a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_17cdcfcc86f2a005082a",
        "grounded": true
      },
      {
        "id": "fact_9e1fa7056fd87238219e",
        "object_or_effect": "w_3f5b91912644c8024f49",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3f5b91912644c8024f49",
        "grounded": true
      },
      {
        "id": "fact_9f13f4592f13ac51372e",
        "object_or_effect": "w_3fd9b1aaf87e721ffdf5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3fd9b1aaf87e721ffdf5",
        "grounded": true
      },
      {
        "id": "fact_9f5d60f303c37e4a58ad",
        "object_or_effect": "w_293e3f4d297b9c057402",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_293e3f4d297b9c057402",
        "grounded": true
      },
      {
        "id": "fact_9fc6a672732931187e64",
        "object_or_effect": "w_b74ddd06c05b2532d4d1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b74ddd06c05b2532d4d1",
        "grounded": true
      },
      {
        "id": "fact_a024707f13b7f885fce5",
        "object_or_effect": "w_2ec174a5beb1ab42f1c5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2ec174a5beb1ab42f1c5",
        "grounded": true
      },
      {
        "id": "fact_a0c803ac29574ffa6955",
        "object_or_effect": "w_c5bcebb2fc40d6c0b54f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c5bcebb2fc40d6c0b54f",
        "grounded": true
      },
      {
        "id": "fact_a2010c781e3df5895d68",
        "object_or_effect": "w_99266a501c07e18d2d5e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_99266a501c07e18d2d5e",
        "grounded": true
      },
      {
        "id": "fact_a3720a575a86c56f3379",
        "object_or_effect": "w_4dc6e8ff8ea7bccc1f47",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4dc6e8ff8ea7bccc1f47",
        "grounded": true
      },
      {
        "id": "fact_a376777cafc11e586be1",
        "object_or_effect": "w_9e0effb45aeae7096f96",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9e0effb45aeae7096f96",
        "grounded": true
      },
      {
        "id": "fact_a4440826622fee5317ae",
        "object_or_effect": "w_8baee0cb61d2cf7372c1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8baee0cb61d2cf7372c1",
        "grounded": true
      },
      {
        "id": "fact_a6621f657024d42c045b",
        "object_or_effect": "w_28c863bbc0d7c8fc9552",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_28c863bbc0d7c8fc9552",
        "grounded": true
      },
      {
        "id": "fact_a6c3eaa616b1c16a2b9a",
        "object_or_effect": "w_b26e5822106b97d2e0da",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b26e5822106b97d2e0da",
        "grounded": true
      },
      {
        "id": "fact_a76adfff2a40b6aeb87f",
        "object_or_effect": "w_a5aa5f3c576a0390f0ac",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a5aa5f3c576a0390f0ac",
        "grounded": true
      },
      {
        "id": "fact_a85d25dffd0e31185100",
        "object_or_effect": "w_f15c0680ffd1529b2015",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f15c0680ffd1529b2015",
        "grounded": true
      },
      {
        "id": "fact_a8bf8b3b66f1bcaf5bf4",
        "object_or_effect": "w_d31f0491d40bc76a3312",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d31f0491d40bc76a3312",
        "grounded": true
      },
      {
        "id": "fact_a8ca16f83ef0e3fe7742",
        "object_or_effect": "w_24755dd2a7965f6384d2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_24755dd2a7965f6384d2",
        "grounded": true
      },
      {
        "id": "fact_a9b9f5e98e0f58329438",
        "object_or_effect": "w_27800381556de0f90bce",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_27800381556de0f90bce",
        "grounded": true
      },
      {
        "id": "fact_a9d6cfe5bb422af69a72",
        "object_or_effect": "w_67bea62fe55ad329d4aa",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_67bea62fe55ad329d4aa",
        "grounded": true
      },
      {
        "id": "fact_aa171c027c43ec5c9bbe",
        "object_or_effect": "w_3b26b9e311045fd4e838",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3b26b9e311045fd4e838",
        "grounded": true
      },
      {
        "id": "fact_aa21ed8359d1a0a8bb6b",
        "object_or_effect": "w_25eb4a1e2e8d7e970401",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_25eb4a1e2e8d7e970401",
        "grounded": true
      },
      {
        "id": "fact_aa43562792ec78c50070",
        "object_or_effect": "w_7f153485ab3eb87d5880",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7f153485ab3eb87d5880",
        "grounded": true
      },
      {
        "id": "fact_aace13a08a7ff9484bdf",
        "object_or_effect": "w_1e6ae7b034239e46728b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1e6ae7b034239e46728b",
        "grounded": true
      },
      {
        "id": "fact_aace6fd76915f24915a8",
        "object_or_effect": "w_6ce9ed95ac38634c42fc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6ce9ed95ac38634c42fc",
        "grounded": true
      },
      {
        "id": "fact_ac8283deadfc4f5a4dc0",
        "object_or_effect": "w_479da52c94c8f8c07c72",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_479da52c94c8f8c07c72",
        "grounded": true
      },
      {
        "id": "fact_acb75da3acec7a2890c9",
        "object_or_effect": "w_031c3cd3be5d0f3d6bf4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_031c3cd3be5d0f3d6bf4",
        "grounded": true
      },
      {
        "id": "fact_acf3f915db42d90262a7",
        "object_or_effect": "w_1287b6a481c32b9ec0d4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1287b6a481c32b9ec0d4",
        "grounded": true
      },
      {
        "id": "fact_ad49a19577f66d2641e4",
        "object_or_effect": "w_5d71ad9be931dd79aae7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5d71ad9be931dd79aae7",
        "grounded": true
      },
      {
        "id": "fact_ae6283ffa20ab5fae609",
        "object_or_effect": "w_6e8ac6293dc4f49a1a08",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6e8ac6293dc4f49a1a08",
        "grounded": true
      },
      {
        "id": "fact_af4fc93c3743c804efea",
        "object_or_effect": "w_9bb9ab9df715092484f8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9bb9ab9df715092484f8",
        "grounded": true
      },
      {
        "id": "fact_af542ee79540977e20b9",
        "object_or_effect": "w_8586263431e7c75944de",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8586263431e7c75944de",
        "grounded": true
      },
      {
        "id": "fact_b01df04ee5e646ba8f63",
        "object_or_effect": "w_59879065baa67dbd0d86",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_59879065baa67dbd0d86",
        "grounded": true
      },
      {
        "id": "fact_b1cacaf739bf99d37e5e",
        "object_or_effect": "w_983c31b29c35354be838",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_983c31b29c35354be838",
        "grounded": true
      },
      {
        "id": "fact_b31c07eb16f485ef244a",
        "object_or_effect": "w_5a101339ec67d81df64c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5a101339ec67d81df64c",
        "grounded": true
      },
      {
        "id": "fact_b32b55234491d00a4ebb",
        "object_or_effect": "w_86afe2db6ad27811cd07",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_86afe2db6ad27811cd07",
        "grounded": true
      },
      {
        "id": "fact_b37c12b65edb5eabfe1f",
        "object_or_effect": "w_b94c909eeec3a876aefd",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b94c909eeec3a876aefd",
        "grounded": true
      },
      {
        "id": "fact_b3dc32a1640e1e08052d",
        "object_or_effect": "w_3881c42b4dd607f51e38",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3881c42b4dd607f51e38",
        "grounded": true
      },
      {
        "id": "fact_b3f9133f9c9c78a67363",
        "object_or_effect": "w_53176dc4605b885d00dc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_53176dc4605b885d00dc",
        "grounded": true
      },
      {
        "id": "fact_b4e912e04bd108c15402",
        "object_or_effect": "w_e6ec90c6a42a031c9cd3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e6ec90c6a42a031c9cd3",
        "grounded": true
      },
      {
        "id": "fact_b533ad33625f35d3a1e3",
        "object_or_effect": "w_12c3c3cbf090c3775c3c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_12c3c3cbf090c3775c3c",
        "grounded": true
      },
      {
        "id": "fact_b5862cf5536d74d6ffdf",
        "object_or_effect": "w_c2dc09445b6dcf6d9699",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c2dc09445b6dcf6d9699",
        "grounded": true
      },
      {
        "id": "fact_b5d6d1847fb57bece275",
        "object_or_effect": "w_db01415809d1ee40ee2c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_db01415809d1ee40ee2c",
        "grounded": true
      },
      {
        "id": "fact_b5ffeb316bdd45f36a7c",
        "object_or_effect": "w_5d2abaceaba652529dcb",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5d2abaceaba652529dcb",
        "grounded": true
      },
      {
        "id": "fact_b6136e87e7680e16956b",
        "object_or_effect": "w_919ff8bf50d0c9a69029",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_919ff8bf50d0c9a69029",
        "grounded": true
      },
      {
        "id": "fact_b6728ae79addbb13313e",
        "object_or_effect": "w_9667182ac0b24c21dbb7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9667182ac0b24c21dbb7",
        "grounded": true
      },
      {
        "id": "fact_b683f72ed11ed013a3ca",
        "object_or_effect": "w_b2455f2b0166bed77047",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b2455f2b0166bed77047",
        "grounded": true
      },
      {
        "id": "fact_b72f1e2ebb24daa8503e",
        "object_or_effect": "w_c9a24914549c72397ffa",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c9a24914549c72397ffa",
        "grounded": true
      },
      {
        "id": "fact_b74c964421b54f692192",
        "object_or_effect": "w_c1b94f2940a28070fa9e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c1b94f2940a28070fa9e",
        "grounded": true
      },
      {
        "id": "fact_b8e2de308f72acc0e422",
        "object_or_effect": "w_1bcb78991604288c47dd",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1bcb78991604288c47dd",
        "grounded": true
      },
      {
        "id": "fact_b9ab3f2984b89dcdc48b",
        "object_or_effect": "w_1accb5477a726dacb877",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1accb5477a726dacb877",
        "grounded": true
      },
      {
        "id": "fact_b9ba2c3091c93a1a7ce2",
        "object_or_effect": "w_a5ad5ac5e85603ad3752",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a5ad5ac5e85603ad3752",
        "grounded": true
      },
      {
        "id": "fact_ba3d61a5430e97dda04c",
        "object_or_effect": "w_1db58ec82b897b4efaa5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1db58ec82b897b4efaa5",
        "grounded": true
      },
      {
        "id": "fact_ba71af385a018d1a05c3",
        "object_or_effect": "w_1137cc74c6083313ce6d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1137cc74c6083313ce6d",
        "grounded": true
      },
      {
        "id": "fact_baa414460fad47bc5c8f",
        "object_or_effect": "w_63bf9850c9827d6e40de",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_63bf9850c9827d6e40de",
        "grounded": true
      },
      {
        "id": "fact_bcba68d40e030b1de8d5",
        "object_or_effect": "w_cb03f017c6df712d81d1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cb03f017c6df712d81d1",
        "grounded": true
      },
      {
        "id": "fact_bce10cfa06b5fd0c7685",
        "object_or_effect": "w_3337777ec477514d0027",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3337777ec477514d0027",
        "grounded": true
      },
      {
        "id": "fact_bd22cf33140c22158c46",
        "object_or_effect": "w_341ea4dcbebf25125993",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_341ea4dcbebf25125993",
        "grounded": true
      },
      {
        "id": "fact_bd82f1c73dbc7564d390",
        "object_or_effect": "w_d432e5bd7f22b38005c2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d432e5bd7f22b38005c2",
        "grounded": true
      },
      {
        "id": "fact_c02e1459751e7458b61c",
        "object_or_effect": "w_9bb0bce8518110398b4e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9bb0bce8518110398b4e",
        "grounded": true
      },
      {
        "id": "fact_c0705e3b8ff2400b050b",
        "object_or_effect": "w_2bde3fb129d33d6dda39",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2bde3fb129d33d6dda39",
        "grounded": true
      },
      {
        "id": "fact_c07e1d3a37651b022af4",
        "object_or_effect": "w_b09fa341ba567cfd6f83",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b09fa341ba567cfd6f83",
        "grounded": true
      },
      {
        "id": "fact_c12bf3676e9a71c6a8b0",
        "object_or_effect": "w_9dca703eee8bdfe66f51",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9dca703eee8bdfe66f51",
        "grounded": true
      },
      {
        "id": "fact_c4e4956b3f615ea86ede",
        "object_or_effect": "w_1c9912685664f6d8e62e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1c9912685664f6d8e62e",
        "grounded": true
      },
      {
        "id": "fact_c6e3b3fa7155bf709b34",
        "object_or_effect": "w_b1ec52e2866d26cdb2ab",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b1ec52e2866d26cdb2ab",
        "grounded": true
      },
      {
        "id": "fact_c74d6c04d26a625bf995",
        "object_or_effect": "w_23c020f049b4cc323fb5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_23c020f049b4cc323fb5",
        "grounded": true
      },
      {
        "id": "fact_c82868b310b948d36f0b",
        "object_or_effect": "w_5cedf4f3c4f4e61f2328",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5cedf4f3c4f4e61f2328",
        "grounded": true
      },
      {
        "id": "fact_c8e6ac6a9d3dc6f20a58",
        "object_or_effect": "w_5556a11e599cc2769038",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5556a11e599cc2769038",
        "grounded": true
      },
      {
        "id": "fact_ca8ea25732e093ce1924",
        "object_or_effect": "w_e2aec28412be34c16877",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e2aec28412be34c16877",
        "grounded": true
      },
      {
        "id": "fact_cb016d0621e5a4831c9c",
        "object_or_effect": "w_cda1f906432d58e071f5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_cda1f906432d58e071f5",
        "grounded": true
      },
      {
        "id": "fact_cc65f26e928792f63aaa",
        "object_or_effect": "o_efe6245127bdf12a1f5b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_cc904db437095999bb11",
        "object_or_effect": "w_784444366e699c23fe41",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_784444366e699c23fe41",
        "grounded": true
      },
      {
        "id": "fact_ccc8f1455e6ea54f2106",
        "object_or_effect": "w_dbae4c9874cf737f969f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_dbae4c9874cf737f969f",
        "grounded": true
      },
      {
        "id": "fact_cccee894e21c0b83bf40",
        "object_or_effect": "w_6698bbab13d3845c0870",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6698bbab13d3845c0870",
        "grounded": true
      },
      {
        "id": "fact_cce0406afaa0ac4f7187",
        "object_or_effect": "w_edab3114c181477aba20",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_edab3114c181477aba20",
        "grounded": true
      },
      {
        "id": "fact_cd624330eaf512851ea8",
        "object_or_effect": "w_78efc158ea24a8828ccc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_78efc158ea24a8828ccc",
        "grounded": true
      },
      {
        "id": "fact_cf238ee84ce18de6feea",
        "object_or_effect": "w_2de657a3a126359a5b52",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2de657a3a126359a5b52",
        "grounded": true
      },
      {
        "id": "fact_cf976a31428c91e44cc7",
        "object_or_effect": "w_5507bd3f54333463d9ef",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5507bd3f54333463d9ef",
        "grounded": true
      },
      {
        "id": "fact_d0873c2a8fa03cb21a50",
        "object_or_effect": "w_4510a54e13f4631cc98a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4510a54e13f4631cc98a",
        "grounded": true
      },
      {
        "id": "fact_d103d5b98cdbd26cb515",
        "object_or_effect": "w_10e982f63c41eb459ea9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_10e982f63c41eb459ea9",
        "grounded": true
      },
      {
        "id": "fact_d31ac4dd5dd7f2fdcd9a",
        "object_or_effect": "w_dfa366a96c74cf197363",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_dfa366a96c74cf197363",
        "grounded": true
      },
      {
        "id": "fact_d473a9edadeb0970f066",
        "object_or_effect": "w_7cba56f46276f18f7bfd",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7cba56f46276f18f7bfd",
        "grounded": true
      },
      {
        "id": "fact_d4dc44906977c203cce2",
        "object_or_effect": "w_29aa0ec31d770cdd4eb7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_29aa0ec31d770cdd4eb7",
        "grounded": true
      },
      {
        "id": "fact_d55286b5747bd651cf2a",
        "object_or_effect": "w_fb9584455e5d76a427f7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_fb9584455e5d76a427f7",
        "grounded": true
      },
      {
        "id": "fact_d5a129ad0f37885217c3",
        "object_or_effect": "w_4d19d77e5491226165b1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_4d19d77e5491226165b1",
        "grounded": true
      },
      {
        "id": "fact_d696c36f188ed016d0e8",
        "object_or_effect": "w_0b16b2dbf5ca3966e8b8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0b16b2dbf5ca3966e8b8",
        "grounded": true
      },
      {
        "id": "fact_d7041267fa86aa6022cc",
        "object_or_effect": "w_5fda3dd58e7cef67d0c2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5fda3dd58e7cef67d0c2",
        "grounded": true
      },
      {
        "id": "fact_d720ce336b6942341f09",
        "object_or_effect": "w_19bc7a2d665a29966e51",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_19bc7a2d665a29966e51",
        "grounded": true
      },
      {
        "id": "fact_d72be8f9e6b64519a3d0",
        "object_or_effect": "w_0ac8515c4080b194c615",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0ac8515c4080b194c615",
        "grounded": true
      },
      {
        "id": "fact_d7b71643338598461af3",
        "object_or_effect": "w_415132009d8847773d42",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_415132009d8847773d42",
        "grounded": true
      },
      {
        "id": "fact_d8887fa4965bc6b1f928",
        "object_or_effect": "w_8392fce92753fbb2970e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_8392fce92753fbb2970e",
        "grounded": true
      },
      {
        "id": "fact_d9f4da6a314102ca0ffb",
        "object_or_effect": "w_0750fc5778314488ca60",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0750fc5778314488ca60",
        "grounded": true
      },
      {
        "id": "fact_da2bd0e8206f9781ec62",
        "object_or_effect": "w_7dc53de6c73f10cf8720",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7dc53de6c73f10cf8720",
        "grounded": true
      },
      {
        "id": "fact_da2cb9fe16775a3279b2",
        "object_or_effect": "w_5c987a8bcdf17ed6e090",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5c987a8bcdf17ed6e090",
        "grounded": true
      },
      {
        "id": "fact_dcbcdccb7229d1f6e151",
        "object_or_effect": "w_0e17af780a376ba5a1e2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0e17af780a376ba5a1e2",
        "grounded": true
      },
      {
        "id": "fact_dda38d140541824708ab",
        "object_or_effect": "w_aa0efcb40280ba4adc9d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_aa0efcb40280ba4adc9d",
        "grounded": true
      },
      {
        "id": "fact_df937fd695988281b88e",
        "object_or_effect": "w_22ce748e2ed19214d5de",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_22ce748e2ed19214d5de",
        "grounded": true
      },
      {
        "id": "fact_dfb9b3a89fadafcc5ea7",
        "object_or_effect": "w_c044656daa8ebb267b96",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c044656daa8ebb267b96",
        "grounded": true
      },
      {
        "id": "fact_e0b17309dad79bd34b8e",
        "object_or_effect": "w_e8ea7a95099da960f2ac",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e8ea7a95099da960f2ac",
        "grounded": true
      },
      {
        "id": "fact_e105db230934042c62fa",
        "object_or_effect": "w_3df836c1d53a9f096f7e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3df836c1d53a9f096f7e",
        "grounded": true
      },
      {
        "id": "fact_e1ccbc29a8995747e0fe",
        "object_or_effect": "w_12e404b2471bc7481286",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_12e404b2471bc7481286",
        "grounded": true
      },
      {
        "id": "fact_e2d7764d16195ca1de2e",
        "object_or_effect": "w_b48071626bd70dc9dbf5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b48071626bd70dc9dbf5",
        "grounded": true
      },
      {
        "id": "fact_e350e2194b62eea2cb50",
        "object_or_effect": "w_98fea525bb7156d4c932",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_98fea525bb7156d4c932",
        "grounded": true
      },
      {
        "id": "fact_e3659ef4a0248c40be30",
        "object_or_effect": "w_1234fb3164cdc715bb3a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1234fb3164cdc715bb3a",
        "grounded": true
      },
      {
        "id": "fact_e3a3d8cbe01546306e80",
        "object_or_effect": "w_ac38307fc88839edaf00",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ac38307fc88839edaf00",
        "grounded": true
      },
      {
        "id": "fact_e4321c656528766bc3f8",
        "object_or_effect": "w_844f2c5b1117c26852c6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_844f2c5b1117c26852c6",
        "grounded": true
      },
      {
        "id": "fact_e4b2cace2dc6667c4822",
        "object_or_effect": "w_9b711e105ec58e726cde",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9b711e105ec58e726cde",
        "grounded": true
      },
      {
        "id": "fact_e4cad68ac9cc64fafb05",
        "object_or_effect": "w_c8d660a519c86c2e00a3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c8d660a519c86c2e00a3",
        "grounded": true
      },
      {
        "id": "fact_e8635c12b5dbf3e9621a",
        "object_or_effect": "w_157601a91f37cc7c1630",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_157601a91f37cc7c1630",
        "grounded": true
      },
      {
        "id": "fact_e90b385ce90f093b0e2d",
        "object_or_effect": "w_20837be2a40b817ca3ca",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_20837be2a40b817ca3ca",
        "grounded": true
      },
      {
        "id": "fact_e9c926fc28a34d44da27",
        "object_or_effect": "w_b2cad70021b7c8f6ad9e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b2cad70021b7c8f6ad9e",
        "grounded": true
      },
      {
        "id": "fact_ea0e0df7fb898cb2d098",
        "object_or_effect": "w_5ccc0a01a9830ffebe15",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5ccc0a01a9830ffebe15",
        "grounded": true
      },
      {
        "id": "fact_ea9a395b7778da77381f",
        "object_or_effect": "w_5917fd77097dd54bf1d2",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5917fd77097dd54bf1d2",
        "grounded": true
      },
      {
        "id": "fact_ebb7235d2fb1f22a97cc",
        "object_or_effect": "w_9f741aee796de6b436b5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9f741aee796de6b436b5",
        "grounded": true
      },
      {
        "id": "fact_ec0921663de125e12c0d",
        "object_or_effect": "w_b7d217bd59bf0b9e889e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b7d217bd59bf0b9e889e",
        "grounded": true
      },
      {
        "id": "fact_ec17a89b11f17962a294",
        "object_or_effect": "w_565e438faa7a98175dd6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_565e438faa7a98175dd6",
        "grounded": true
      },
      {
        "id": "fact_ec966f3498d544d8aba0",
        "object_or_effect": "w_5f36df43a7317d9c2153",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5f36df43a7317d9c2153",
        "grounded": true
      },
      {
        "id": "fact_ecfc54b08badbc927f35",
        "object_or_effect": "w_2612b198d7484904de45",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2612b198d7484904de45",
        "grounded": true
      },
      {
        "id": "fact_ee420cf7e3987ef223ec",
        "object_or_effect": "w_1995cb4074c97c5cb520",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1995cb4074c97c5cb520",
        "grounded": true
      },
      {
        "id": "fact_ee701862142bf4d44680",
        "object_or_effect": "w_16f2e737868864397d70",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_16f2e737868864397d70",
        "grounded": true
      },
      {
        "id": "fact_eef1d37a12eea791faef",
        "object_or_effect": "w_3bdea1a354ff5a84f7e4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3bdea1a354ff5a84f7e4",
        "grounded": true
      },
      {
        "id": "fact_eef2e6b94d188b8e06a2",
        "object_or_effect": "w_86e77762d1b25cae285e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_86e77762d1b25cae285e",
        "grounded": true
      },
      {
        "id": "fact_ef61d6cad27e07182251",
        "object_or_effect": "w_7f9e0acaff4db425adcd",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7f9e0acaff4db425adcd",
        "grounded": true
      },
      {
        "id": "fact_f1cd1071bc2cc760204a",
        "object_or_effect": "w_e2bee11e502eb1a646e3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e2bee11e502eb1a646e3",
        "grounded": true
      },
      {
        "id": "fact_f35528db00251103c294",
        "object_or_effect": "w_d2bd75e59dcd79ae07d3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d2bd75e59dcd79ae07d3",
        "grounded": true
      },
      {
        "id": "fact_f38397bf8e4c1fca100c",
        "object_or_effect": "w_a01c1c4ec68b8b91f81f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a01c1c4ec68b8b91f81f",
        "grounded": true
      },
      {
        "id": "fact_f4f715f3170e1fe66391",
        "object_or_effect": "w_b2cedfaf7d8f21e35d13",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b2cedfaf7d8f21e35d13",
        "grounded": true
      },
      {
        "id": "fact_f501cb956ad52ee83989",
        "object_or_effect": "w_d62112f699eef0d3e0d0",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d62112f699eef0d3e0d0",
        "grounded": true
      },
      {
        "id": "fact_f579c4d955f82d550d12",
        "object_or_effect": "w_5253d09d10a96b98d62f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5253d09d10a96b98d62f",
        "grounded": true
      },
      {
        "id": "fact_f59866cc8da44094e653",
        "object_or_effect": "w_92800f69e9bab06df7fc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_92800f69e9bab06df7fc",
        "grounded": true
      },
      {
        "id": "fact_f5a8dc937b305934b5db",
        "object_or_effect": "w_7e7fbb87b0cd79f6be6c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_7e7fbb87b0cd79f6be6c",
        "grounded": true
      },
      {
        "id": "fact_f61d1c61982ce6df7b8e",
        "object_or_effect": "w_ab2e118fa6ed72d4d6ac",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ab2e118fa6ed72d4d6ac",
        "grounded": true
      },
      {
        "id": "fact_f62f0bc6ddea9d2d5a3a",
        "object_or_effect": "w_e9d3bba318179fa206d9",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e9d3bba318179fa206d9",
        "grounded": true
      },
      {
        "id": "fact_f8b4a7d3abe4b8f3b12b",
        "object_or_effect": "w_92ee1f8524ef9cffc6f7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_92ee1f8524ef9cffc6f7",
        "grounded": true
      },
      {
        "id": "fact_f9059cbf4b403257832a",
        "object_or_effect": "w_df6ad2283845734afd7b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_df6ad2283845734afd7b",
        "grounded": true
      },
      {
        "id": "fact_f939e6822db8d1c0bcfa",
        "object_or_effect": "w_f828eae272684561c116",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f828eae272684561c116",
        "grounded": true
      },
      {
        "id": "fact_f94021f5571cee36ea75",
        "object_or_effect": "w_5cbf67a2d98c30c563bc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5cbf67a2d98c30c563bc",
        "grounded": true
      },
      {
        "id": "fact_fb05f1d77b39f38f8b34",
        "object_or_effect": "w_df5aeed75c23a12554f6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_df5aeed75c23a12554f6",
        "grounded": true
      },
      {
        "id": "fact_fb65605fa0ac522fad8d",
        "object_or_effect": "w_ad8f4e069f57172bc78f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_ad8f4e069f57172bc78f",
        "grounded": true
      },
      {
        "id": "fact_fbb9abde569de01ecfc7",
        "object_or_effect": "w_dc0564913d383ba8f01a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_dc0564913d383ba8f01a",
        "grounded": true
      },
      {
        "id": "fact_fcd7448b191e8c175aae",
        "object_or_effect": "w_b5f5fb4f9a4c3d93385a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b5f5fb4f9a4c3d93385a",
        "grounded": true
      },
      {
        "id": "fact_feeb18c466d2d2a3579b",
        "object_or_effect": "w_b3439e5e85719a657c9b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b3439e5e85719a657c9b",
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 5,
      "semantic_answer_outside_sent_scope": 4,
      "unbound_or_inapplicable_seed": 1,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 12,
      "policy_missing": 5,
      "source_task_reading": 1
    }
  }
}
```

## RQ1_ad8d0ac6a104

证据目录 run/members/RQ1_ad8d0ac6a104/attempt_1/，报告哈希 47648913c15a0ddcf7523b3f36b950d482e3d7b845d2710a141b6cbb6e28ec0d

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unrelated_or_secondary_graph_pairs_deferred,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_ad8d0ac6a104",
        "reference": "D2:90:original:1",
        "function": "fallback",
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
          "detail_sha256": "63f76e6ff9e0dcd7188762f97457092e6ab52922f7e56b56caa219d5fc80fe5e",
          "issue": "issue_d4ffe0f3a182c33b7581"
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
        "answer": "sat",
        "count": 16
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 16
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 16
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 6,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 4
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 12,
      "external_dependency": 6,
      "policy_missing": 4
    }
  }
}
```

## RQ1_adc795eb2050

证据目录 run/members/RQ1_adc795eb2050/attempt_1/，报告哈希 a8c00f9f18317f4d1f4fd8ddcdd13d89a456251f9f3e2ee67f53338972105548

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope,unrelated_or_secondary_graph_pairs_deferred",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_adc795eb2050",
        "reference": "D2:108:original:1",
        "function": "initialize",
        "v32": "FN",
        "last1164": "FN",
        "b5": "FN",
        "ACTaint_DeepSeek": "TP",
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
        "support": "source_0a6ea2242f18ba64df47",
        "fact": "fact_9bb7e4e382e55429112b",
        "origin": "source_policy_deduction",
        "field": "policies",
        "version": 1
      },
      {
        "support": "source_4e2fb75531742565ad65",
        "fact": "fact_2aad9a40758f32937847",
        "origin": "source_policy_deduction",
        "field": "policies",
        "version": 1
      },
      {
        "support": "source_6126c22416680338578b",
        "fact": "fact_5aac3cb4877a49202060",
        "origin": "source_policy_deduction",
        "field": "policies",
        "version": 1
      },
      {
        "support": "support_40288a675550a5967406",
        "fact": "fact_3123a2da3ca92b8955f9",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_7a6eed217ff3c5092ae1",
        "fact": "fact_fa273086a1a6a3a03552",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_a5646c17c94c01454783",
        "fact": "fact_0b6f046d41a2a0c21273",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_b2d927b2386cb0198112",
        "fact": "fact_0b6f046d41a2a0c21273",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_b90de9ca3c7bfb2b3d6d",
        "fact": "fact_650f24353bbae5dc189d",
        "origin": "verified_service",
        "field": "policies",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_0b6f046d41a2a0c21273",
        "object_or_effect": "o_49d97e5109c0c3ee9885",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_130fdd35ce8770632485",
        "object_or_effect": "w_d213902e3ab465495133",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d213902e3ab465495133",
        "grounded": true
      },
      {
        "id": "fact_2aad9a40758f32937847",
        "object_or_effect": "w_501bb4ef18a7c275cfc0",
        "meaning": "current_authority_required",
        "role": null,
        "subject": "o_49d97e5109c0c3ee9885",
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_3123a2da3ca92b8955f9",
        "object_or_effect": "o_8ef800c6f17e445b5bd8",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_327b51757d46f8e1c7c9",
        "object_or_effect": "w_b896186f48b8e9f13fff",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b896186f48b8e9f13fff",
        "grounded": true
      },
      {
        "id": "fact_34bcf1b2fd0fb2ed32d5",
        "object_or_effect": "w_23905bfd389d267d11f5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_23905bfd389d267d11f5",
        "grounded": true
      },
      {
        "id": "fact_3d19d5581d9a8570701b",
        "object_or_effect": "w_8ae4b74004b11e7746dd",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8ae4b74004b11e7746dd",
        "grounded": true
      },
      {
        "id": "fact_44c147c8dc5dab571396",
        "object_or_effect": "w_30d88094bcd534d5eb47",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_30d88094bcd534d5eb47",
        "grounded": true
      },
      {
        "id": "fact_4bff81920b936f16b7f3",
        "object_or_effect": "w_6596d05483a6e8434a65",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6596d05483a6e8434a65",
        "grounded": true
      },
      {
        "id": "fact_4cade114ac4221e1d9dd",
        "object_or_effect": "w_dbf74a385698f458b0dd",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_dbf74a385698f458b0dd",
        "grounded": true
      },
      {
        "id": "fact_5aac3cb4877a49202060",
        "object_or_effect": "w_0f2d8d433fffe418a684",
        "meaning": "current_authority_required",
        "role": null,
        "subject": "o_49d97e5109c0c3ee9885",
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_5adc20a90272478d31e6",
        "object_or_effect": "w_ba595e52568075cab7e1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_ba595e52568075cab7e1",
        "grounded": true
      },
      {
        "id": "fact_5f300a007e14cf80eafb",
        "object_or_effect": "w_0f2d8d433fffe418a684",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0f2d8d433fffe418a684",
        "grounded": true
      },
      {
        "id": "fact_650f24353bbae5dc189d",
        "object_or_effect": "w_0c90147bf4efb453a067",
        "meaning": "initialization_stage",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_7048756240129da506ee",
        "object_or_effect": "w_0c90147bf4efb453a067",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0c90147bf4efb453a067",
        "grounded": true
      },
      {
        "id": "fact_9bb7e4e382e55429112b",
        "object_or_effect": "w_8ae4b74004b11e7746dd",
        "meaning": "current_authority_required",
        "role": null,
        "subject": "o_49d97e5109c0c3ee9885",
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_bcb1944397ddf598cdfc",
        "object_or_effect": "w_8caebed6a0e8a1e7bcef",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8caebed6a0e8a1e7bcef",
        "grounded": true
      },
      {
        "id": "fact_e259337d20608e15dd36",
        "object_or_effect": "w_3258fb011a41e4cdff63",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_3258fb011a41e4cdff63",
        "grounded": true
      },
      {
        "id": "fact_ee7df0195d5ea173babe",
        "object_or_effect": "w_d168a9338653133ac945",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d168a9338653133ac945",
        "grounded": true
      },
      {
        "id": "fact_f2d538c17454a4a880eb",
        "object_or_effect": "w_501bb4ef18a7c275cfc0",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_501bb4ef18a7c275cfc0",
        "grounded": true
      },
      {
        "id": "fact_fa273086a1a6a3a03552",
        "object_or_effect": "o_6299befe0b52cf0135b7",
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
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "local_premises_feasible",
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
      "unbound_or_inapplicable_seed": 2,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 12,
      "applicable_role_guard": 2,
      "external_dependency": 1,
      "policy_missing": 2,
      "source_task_reading": 1
    }
  }
}
```
