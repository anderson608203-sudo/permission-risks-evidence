# 逐例审阅

## RQ1_0fa374173417

证据目录 run/members/RQ1_0fa374173417/attempt_1/，报告哈希 06fe84eb3367077bbd97aeae1a3c341067f7a986cc6313883e20391609957da9

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [
    "v32 丢失根因 D2:311:author:1",
    "last1164 丢失根因 D2:311:author:1",
    "prev200 丢失根因 D2:311:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_0fa374173417",
        "reference": "D2:311:author:1",
        "function": "mintTo",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "FN",
        "prev200_findings": [
          "finding_9875fac5ed71e9cd2668"
        ],
        "decision_only_findings": [],
        "current": "FN"
      }
    ],
    "findings": [
      {
        "idx": 1,
        "member": "RQ1_0fa374173417",
        "finding": "finding_74ed7a154df01398a2c9",
        "function": "killContract()",
        "location": {
          "file": "units/program.sol",
          "start": 1535,
          "length": 184,
          "ast_id": 161
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_0fa374173417', 'units/program.sol', 1535)",
        "source_excerpt": "function killContract () payable external\n    {\n        if (msg.sender==owner || msg.value >=howManyEtherInWeiToKillContract)\n        {\n            selfdestruct(owner);\n        }\n    }",
        "source_sha256": "68bafe295421dbbb94628566ba812d7005c77fbb8adab62263e18c80f5c6f4d6",
        "note": "实际报警入口或影响与作者参考不同，不能抵销该独立根因漏检。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 1535. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 1535,
              "length": 184,
              "ast_id": 161
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
        "lost": [
          "D2:311:author:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:311:author:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:311:author:1"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "a0569f738702b30b37b1c472882d64733fbe1fd34b622e61e2dac1591a626514",
          "issue": "issue_4f4edd19a0bcb63c6ed7"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a26471b29bebefdf320f5b25ce6ba39a84fb0036d07a6c86c20499c7c6cab1de",
          "issue": "issue_4f4edd19a0bcb63c6ed7"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "1826c43c7c2c7776203567d0d85b5105966e896f1dcb1844dd22c3f7f445a360",
          "issue": "issue_b0c8ef69f2f5d227c330"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b6bd14e6ce4df3627e5a0e4bdac2266f702b10d23c4400250785d5552b9018d7",
          "issue": "issue_b0c8ef69f2f5d227c330"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "0fd87ce6219d88fb4e6fe12370c7810dd3711e0582632416a70b300ae34b6805",
          "issue": "issue_ecd33035c6f335b608b1"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b0ce4734f367c74948909a875e2d4a0ecd3f316e99d169ed263f615943a5703f",
          "issue": "issue_ecd33035c6f335b608b1"
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
        "support": "support_f58cfacc876aba17478c",
        "fact": "fact_dbc25599e5cd0dd8aea6",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_dbc25599e5cd0dd8aea6",
        "object_or_effect": "o_c03f798181e7fc90622d",
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
        "answer": "sat",
        "count": 4
      },
      {
        "label": "callback_influence",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "direct_callback_influence",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "callback_influence",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "local_premises_feasible",
        "answer": "sat",
        "count": 5
      },
      {
        "label": "authorization_violation",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "authorization_violation",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 2
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 11,
      "source_task_reading": 5,
      "program_support": 1,
      "policy_missing": 1,
      "external_dependency": 1
    }
  }
}
```

## RQ1_1007b4fc52ca

证据目录 run/members/RQ1_1007b4fc52ca/attempt_1/，报告哈希 2f4b6e8c5477bef08f420066fff5db4b8924a140c4a364be095f67906565548b

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [
    "last1164 新增根因 D2:236:S1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_1007b4fc52ca",
        "reference": "D2:236:S1",
        "function": "selfdestructs",
        "v32": "TP",
        "last1164": "FN",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_7f9516ccd09374339530"
        ],
        "decision_only_findings": [
          "finding_72c4b25968ea0ba2c015"
        ],
        "current": "TP"
      }
    ],
    "findings": [
      {
        "idx": 2,
        "member": "RQ1_1007b4fc52ca",
        "finding": "finding_441ce6286a5c019f5f97",
        "function": "selfdestructs()",
        "location": {
          "file": "units/program.sol",
          "start": 4952,
          "length": 74,
          "ast_id": 602
        },
        "result": "TP",
        "reference": "D2:236:S1",
        "group": "D2:236:S1",
        "source_excerpt": "function selfdestructs() payable public {\n    \t\tselfdestruct(owner);\n    }",
        "source_sha256": "644289eda397c8a2bd67a571d9112c91fb3eaf49542c16002a1ffa690c32da29",
        "note": "实际入口及源码效果与作者独立根因对应，保留程序证据可审计性限制。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 4952. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 4952,
              "length": 74,
              "ast_id": 602
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
        "gained": [
          "D2:236:S1"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "f6859bdac4c486d02228f78012a7b6ad00c5ca44a6bb4156a3f1de418d6402e6",
          "issue": "issue_7a1808c2928dc7595b45"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "975af84d898b513b9771138db9672da53130ae136ecb8838190f6b59177a25de",
          "issue": "issue_7a1808c2928dc7595b45"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [
      4812
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
        "count": 1
      },
      {
        "label": "authorization_violation",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 6,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 17,
      "source_task_reading": 18,
      "program_support": 1,
      "external_dependency": 2
    }
  }
}
```

## RQ1_15346457ba72

证据目录 run/members/RQ1_15346457ba72/attempt_1/，报告哈希 cc888f9c6f365681b3149db35c7bb5056bab857799ea5de6b066cfb6b8fb74dc

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
    "v32 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,no_locatable_source",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": true,
    "paired_id": "RQ1_fe7add810da5",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "fced8f2348fb10693136501e51274d7a104f6caa251c1cc6c7dcf6b65c331772",
          "issue": "issue_37fe60dff1935d0fd054"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "93e18830b06ceff08cf48868f81f9f1cffe173dfd7ae6f078f47e4bdd2aef174",
          "issue": "issue_37fe60dff1935d0fd054"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "ffa038f78b345644a20e884bcdd6bb22eb47e23bd0de8ec2885988f3f8d4ae34",
          "issue": "issue_be91455e898d8868f9c8"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ce900d77a660d202386924a7cdb0be3173dfcef707d142c423e1abd6437b64ca",
          "issue": "issue_be91455e898d8868f9c8"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "04d6b39da6435b54c14d0895d364bfe8e60d02ba75784a6a4532af24d9d7e915",
          "issue": "issue_8fc5529ed7db08172525"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "629814dde07d95b0d9866e937c06b6a06d1c7b7fe8bee5addfff01f0252130dc",
          "issue": "issue_8fc5529ed7db08172525"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 11,
      "category_ambiguous_or_outside_supported_task": 3,
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

## RQ1_1844e5d3d18e

证据目录 run/members/RQ1_1844e5d3d18e/attempt_1/，报告哈希 4f71670e3c69fc4ed3f9258cdd212a2331ee454e3f515867bedf1e9bfd287196

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
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,category_ambiguous_or_outside_supported_task,unbound_or_inapplicable_seed,unknown_assessment_vocabulary",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": true,
    "paired_id": "RQ1_db73c28a69c2",
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
          "detail_sha256": "64165de051193359c82b57e016f3c27041f3e22132b2e89d4b9add52671c65af",
          "issue": "issue_f04e8fd4f01328e79272"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c19bd1ace49eb10a93b206d2952bbe0210a2a09d48c106cd6662a0e60a67aa09",
          "issue": "issue_f04e8fd4f01328e79272"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "7ae67e8cf9b87f5aea4973090f9c184afa401c0fc6429fb5a92c950155bfe143",
          "issue": "issue_2d66ecb2aae1d6852e27"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "6910f75bdb7552c6bacef7a2a253e081681ba5bae3efecfd4d4589041babf965",
          "issue": "issue_2d66ecb2aae1d6852e27"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "4d4c85282112cc77cb085c9a0a73272eb1d01a663e2e84ffcc25cdd8e8a26a2e",
          "issue": "issue_de44652cc081711a0413"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "89717ac4c509951d04a125054a6a0e2c8d706803297853f9dc8821dd2236c8ca",
          "issue": "issue_de44652cc081711a0413"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "d3fe9def751710ff1c27c07a1cdaf795a70ab24cb8c7f793359c73ea6ece9201",
          "issue": "issue_1f36d9c98915f729fdac"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "273f1aa2b0850e4132ba85a76bab8afc2e84406d56e61ecead619a892e32b223",
          "issue": "issue_1f36d9c98915f729fdac"
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
          "detail_sha256": "1eeb5b9f62eba1989a6bd7493280601e31e6cbff3335f927a91a391e4b336004",
          "issue": "issue_92482410dac06df2e8d2"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "b1f5019b181772f8f3b90ef232fc83c5200ae020ad18f2c2f21a133c54e9adba",
          "issue": "issue_92482410dac06df2e8d2"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_89c6cd6cb87cc9062a63",
        "fact": "fact_2034a4f539065e63fe56",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_92d5a8175d9f4eeb6d45",
        "fact": "fact_f55b4d4a9bbbf4618cfb",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_dabad111593afd9ab6a8",
        "fact": "fact_e50b4196a77c3852719c",
        "origin": "verified_service",
        "field": "policies",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_2034a4f539065e63fe56",
        "object_or_effect": "o_dcd82ec85b9843545cb2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_3850daf5d0d68f24e9c7",
        "object_or_effect": "w_81677679ab47e556b732",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_81677679ab47e556b732",
        "grounded": true
      },
      {
        "id": "fact_e50b4196a77c3852719c",
        "object_or_effect": "w_313cd82e6e5fa92b22e0",
        "meaning": "holder_authorization_applies",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_f55b4d4a9bbbf4618cfb",
        "object_or_effect": "o_307fa758d6f347fb1d4e",
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
        "count": 7
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 8
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 5
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 8
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 3
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 4,
      "category_ambiguous_or_outside_supported_task": 5,
      "unknown_assessment_vocabulary": 4,
      "semantic_answer_outside_sent_scope": 1,
      "core_unresolved_retained_for_investigation": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 8,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 82,
      "source_task_reading": 3,
      "external_dependency": 20
    }
  }
}
```

## RQ1_18c85d7f1380

证据目录 run/members/RQ1_18c85d7f1380/attempt_1/，报告哈希 1d38f8ec8fccc2899fb46b840a3ec43247de462f3e9d06c18e3a8096aacea7ac

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
    "paired_id": "RQ1_983137cbe5d6",
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
          "detail_sha256": "3e3c17d50519c312593852e72fb6f374f8a9e51e78ba7b7c09b9b8f5f657a2fa",
          "issue": "issue_6360b932038d7a236e10"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "61a868e72e0171913cdea10c1452b8b7a7e1b7f21a3d283669cbda193897f15e",
          "issue": "issue_567e8c68cf47626f48b0"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "45ba3c683961b0803225389d111de945aa59d8af0846bd998ebd0f203983abcd",
          "issue": "issue_4d624a73bf74e830a00f"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "74c94c9aaaa3013ba884362cdc1341ca66970e4cd4cd83966bee37cd30c5d7b9",
          "issue": "issue_4d624a73bf74e830a00f"
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
          "detail_sha256": "bfe7ad3b81d282b2458d0ee10430ea3133b7b0b13592ff87a749c91de0f7634b",
          "issue": "issue_161e8e79985de8acd0e2"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "12fe7ae59fdbf70abc2f612ba0854b787b0f39a3b4ae19b1aad2df6d847e380c",
          "issue": "issue_161e8e79985de8acd0e2"
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
        "count": 8
      },
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 16
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 38
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 14
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 31
      },
      {
        "label": "same_request_amount_change",
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
      "invalid_semantic_row": 6,
      "unknown_assessment_vocabulary": 4,
      "category_ambiguous_or_outside_supported_task": 2,
      "semantic_answer_outside_sent_scope": 1,
      "action_slice_exhausted": 5,
      "program_investigation_budget_exhausted": 1,
      "program_investigation_seconds": 2,
      "semantic_budget": 1,
      "revision_outside_actual_feedback_scope": 1
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

## RQ1_196284e657b0

证据目录 run/members/RQ1_196284e657b0/attempt_1/，报告哈希 ffbf5418fbe6ad47aefa40a01fda0a500288040b28a5da1c92a0e017ef72c6f9

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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,unrelated_or_secondary_graph_pairs_deferred",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": true,
    "paired_id": "RQ1_0bf6f8bce8d9",
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
          "detail_sha256": "573dbe781f71fa541659fb465f330c65d9c2b3a4241e354c8dd9445ee9a30088",
          "issue": "issue_a72b49ebcf8b4e1f4844"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "23a2d4dd5c4c91017140ce89d000bbb862125662c4f708c6546e85703cdb3e57",
          "issue": "issue_a72b49ebcf8b4e1f4844"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "35b80db8ed17b1c2b4741b9d24a51964db05ca27941f182bdbb171ed42cb1432",
          "issue": "issue_13fea1204f9859e00919"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ebb5efad598d9636c0fb0c782588f2769387230782dcbeafb1ec9628602d0bd7",
          "issue": "issue_13fea1204f9859e00919"
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
      "unbound_or_inapplicable_seed": 4,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 29,
      "external_dependency": 15,
      "source_task_reading": 1
    }
  }
}
```

## RQ1_1a94f7866801

证据目录 run/members/RQ1_1a94f7866801/attempt_1/，报告哈希 499b05244e6a39048587c9e4561f814054cb1c2217a3482fa906300f5dac783c

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope,no_locatable_source",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": true,
    "paired_id": "RQ1_a906c0b62c0b",
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
          "detail_sha256": "dee737db45e5ffcd8ae40ac738e6137736149decf56be0fc7dc6a1fbd38ca719",
          "issue": "issue_95313dea81800edc06b1"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "75829795864b93a5852b1a4e374257d65fb6cf44a651bf04cd7443b0354ee1f0",
          "issue": "issue_95313dea81800edc06b1"
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
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a21737763bcfc5d53b6e88eff4ed78a90e61fef4f95c9043ded5163464812d2b",
          "issue": "issue_099c95415642689cc3fa"
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
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 2,
      "no_locatable_source": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 271,
      "model_phase_missing": 84
    }
  }
}
```

## RQ1_1c6b43b24d4c

证据目录 run/members/RQ1_1c6b43b24d4c/attempt_1/，报告哈希 252177da0a8467c753b38e418d612d7d19ad6c9732008709e2798644f6b6a00c

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
    "paired_id": "RQ1_37d9daf031da",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "eb28752428774389300cb4fac4b122e3218fb51863bfdb43faca621f980729ce",
          "issue": "issue_76d99d92ed2c5b75c2f4"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "9bcf1f46ae8476547cdeeeac3cfe3b2ac555d7923e7aaa58bc77134c4b4727dd",
          "issue": "issue_76d99d92ed2c5b75c2f4"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [
      {
        "label": "direct_callback_influence",
        "answer": "unsat",
        "count": 448
      },
      {
        "label": "callback_influence",
        "answer": "unsat",
        "count": 448
      },
      {
        "label": "direct_callback_influence",
        "answer": "sat",
        "count": 8
      },
      {
        "label": "callback_influence",
        "answer": "sat",
        "count": 8
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 4,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 1,
      "program_investigation_seconds": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 424,
      "external_dependency": 43,
      "source_task_reading": 33
    }
  }
}
```

## RQ1_1f06ce07140f

证据目录 run/members/RQ1_1f06ce07140f/attempt_1/，报告哈希 ed1394f7aea724465a3f0726989e8166b9eee0dee5223e62c88b70826885aa0d

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
    "已确认消费/覆盖诊断 invalid_semantic_row,ambiguous_confirmation_not_a_risk_judgment,core_unresolved_retained_for_investigation,unbound_or_inapplicable_seed",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": false,
    "paired_id": "RQ1_e73c99ca23e5",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "2f25917ab920f403a1e0a8a8f8227bc011800383da21342bf0b6d137e36aead5",
          "issue": "issue_26f0e8a94b5fa7d08295"
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
        "support": "support_20fd07f5d9fd30b6adfa",
        "fact": "fact_1bb6d783020f2ee4c734",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_1bb6d783020f2ee4c734",
        "object_or_effect": "o_9bf4d0e429f7997f395e",
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
      "invalid_semantic_row": 2,
      "ambiguous_confirmation_not_a_risk_judgment": 1,
      "core_unresolved_retained_for_investigation": 1,
      "unbound_or_inapplicable_seed": 1,
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
      "no_effect_in_scope": 207,
      "source_task_reading": 36,
      "external_dependency": 6,
      "covered_holder_grant": 1
    }
  }
}
```

## RQ1_1f156ef466b1

证据目录 run/members/RQ1_1f156ef466b1/attempt_1/，报告哈希 ee26a0610afb9108e357fd9aca1568b478f4f1874ced19f8e5610b85f92bf02b

```json
{
  "task": "AC",
  "prediction": {
    "AC": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,unrelated_or_secondary_graph_pairs_deferred",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [],
    "findings": [
      {
        "idx": 3,
        "member": "RQ1_1f156ef466b1",
        "finding": "finding_ff62190b770207032f6c",
        "function": "freezeAccount(address,bool)",
        "location": {
          "file": "units/program.sol",
          "start": 6069,
          "length": 128,
          "ast_id": 837
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_1f156ef466b1', 'units/program.sol', 6069)",
        "source_excerpt": "function freezeAccount(address _target, bool frozen){\n    frozenAccount[_target] = frozen;\n    FrozenFunds(_target, frozen);\n  }",
        "source_sha256": "bd291db050ad9450ff3b2063b2abb63754ba3e1a57500cf17e6077a67590df4b",
        "note": "冻结参考无该根因，按参考外报警记录；未据此证明其业务上错误。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 6069. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 6069,
              "length": 128,
              "ast_id": 837
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
          "E10",
          "E3"
        ]
      },
      {
        "idx": 4,
        "member": "RQ1_1f156ef466b1",
        "finding": "finding_58e7442d2f2057fdbad7",
        "function": "setPrices(uint256,uint256)",
        "location": {
          "file": "units/program.sol",
          "start": 4516,
          "length": 124,
          "ast_id": 612
        },
        "result": "FP",
        "reference": null,
        "group": "('RQ1_1f156ef466b1', 'units/program.sol', 4516)",
        "source_excerpt": "function setPrices(uint256 newSellPrice, uint256 newBuyPrice){\n    sellPrice = newSellPrice;\n    buyPrice = newBuyPrice;\n  }",
        "source_sha256": "bd291db050ad9450ff3b2063b2abb63754ba3e1a57500cf17e6077a67590df4b",
        "note": "冻结参考无该根因，按参考外报警记录；未据此证明其业务上错误。",
        "decision": {
          "status": "risk",
          "reason": "program_support",
          "explanation": "The assessment concerns the policy governing the protected effect at source offset 4516. A scope-matched program check supports this effect under the recorded analysis domain.",
          "locations": [
            {
              "file": "units/program.sol",
              "start": 4516,
              "length": 124,
              "ast_id": 612
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
          "E13",
          "E8"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "40e10f599a316c2cb8a80a58e491921409e36aa16f33f09148a68b91986807df",
          "issue": "issue_56107eb3338b1a04b065"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "86134676e8ca8e3baf79189c3055f210b907890fa78e8a50c30590e86c825a04",
          "issue": "issue_56107eb3338b1a04b065"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "ef6eb58c61d3c22c6156d3a05009a7c9f2963a3795c5f4ceca5ab3cdbf3b4422",
          "issue": "issue_1735d1f56f9e8e50fcf4"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "d06ccde84e69eb1a5723ebd004d8d43a89ef76c8b1c541ed69579eb20b8bca1e",
          "issue": "issue_1735d1f56f9e8e50fcf4"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "920a30b92528e30bf9bf5b82780e15341c883b19e9c6583b2f574ae67bd46c1b",
          "issue": "issue_9a27c5a956c628c8fe7f"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "10fc393ca8dbf0c4c92a9357966e6a5f1b393aa04c5273a98d1a78bc725ab5a4",
          "issue": "issue_9a27c5a956c628c8fe7f"
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
          "detail_sha256": "63865aa069a6dac899d835513792f072d256c665885fc4b40b88efe175d50717",
          "issue": "issue_b0a330956fc5553dbb6d"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [
      4240,
      5016
    ],
    "new": [],
    "disappeared_to_unknown": false,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_593d9dae0def231ea4ca",
        "fact": "fact_8ec64d2b6f11afe53078",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_5e9f086133bca24ace27",
        "fact": "fact_312f803d8ba8a08664fd",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_c3a930c48914eaba82d1",
        "fact": "fact_d57cf7872f139358b4d2",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_312f803d8ba8a08664fd",
        "object_or_effect": "o_04433e75b2aa2fa6d2bc",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_8ec64d2b6f11afe53078",
        "object_or_effect": "o_b1f4c8fb8fd5814ae048",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_b3e9e374478e6ec09374",
        "object_or_effect": "w_0fcc25d569f6043a8f5f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0fcc25d569f6043a8f5f",
        "grounded": true
      },
      {
        "id": "fact_bbd689575dededb45df1",
        "object_or_effect": "w_665d77fabdfb79b8fe00",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_665d77fabdfb79b8fe00",
        "grounded": true
      },
      {
        "id": "fact_cd8f1aae9a562ebcbd99",
        "object_or_effect": "w_d04ca6299f65573e9ea1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d04ca6299f65573e9ea1",
        "grounded": true
      },
      {
        "id": "fact_d57cf7872f139358b4d2",
        "object_or_effect": "o_974ed0fcb87b80119ad9",
        "meaning": "management_role",
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
        "count": 7
      },
      {
        "label": "authorization_violation",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "authorization_violation",
        "answer": "unsat",
        "count": 4
      },
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
      "unbound_or_inapplicable_seed": 4,
      "category_ambiguous_or_outside_supported_task": 3,
      "unknown_assessment_vocabulary": 4,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 2,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "program_support": 2,
      "no_effect_in_scope": 16,
      "source_task_reading": 7,
      "policy_missing": 2,
      "external_dependency": 1
    }
  }
}
```
