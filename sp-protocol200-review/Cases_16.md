# 逐例审阅

## RQ1_bcafc7a40ce2

证据目录 run/members/RQ1_bcafc7a40ce2/attempt_1/，报告哈希 b3db32aec83d079344c0c10b974c1e423490b0d085193c4abadf7b0fcfc81ee9

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
    "已确认消费/覆盖诊断 category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,no_locatable_source,invalid_semantic_row",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": true,
    "paired_id": "RQ1_e1ce695fff9e",
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "471b7a198891c7c6afecda6bda1ebeeb0494e6faf7f70fac549a7f386fa5d36e"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "796864c4867767a9fed546ae139ae75e95fcea08a788c410e1433011fa05597f",
          "issue": "issue_7b384299d5526524eea5"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c987347af2f80a6ad7306971af2f60b6a8376a23f08968cf82650c111ff52bff",
          "issue": "issue_7b384299d5526524eea5"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "2e3b110f02aeb33dfe40f9c24ef52da17c2d570bbed6fd20767948b30f7fbd8d",
          "issue": "issue_ec7d03e7ff50b40553b3"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a8c5acffa2c91ad027a9dcf9049cdd2dcaee7e3d4ec2c321445fa155942d0929",
          "issue": "issue_ec7d03e7ff50b40553b3"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "039b1447132f87eeb1f5cda400049d3b201ff76912d0d07a1aef3fbea498812b",
          "issue": "issue_df34b8369d6f79d90331"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "be2087c8b2b5dc4c00fa6a47770fe06a9094ae6c303cf9e6ee5e739bc3ecda79",
          "issue": "issue_df34b8369d6f79d90331"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "b43faae2a4d310e6faec3c8ccfa2abad080200c7fb1fabf3b5144569d5784e29",
          "issue": "issue_43f420b825b92f5ecc49"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ced3bc8fd3ee76309c7458f7ef7e491408579cd01af0de8c5e1047698d131f83",
          "issue": "issue_43f420b825b92f5ecc49"
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
          "detail_sha256": "1493c86dcb9e093ddb04d8f74be14d714fb69fc0034ca6caf5b8f608ecacafad",
          "issue": "issue_7d3ddef7c78633f73c75"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "febf5d31d0b1905393dd1ddf2d198af8c55022b5593bbbe05ba407bd5cbcff75",
          "issue": "issue_7d3ddef7c78633f73c75"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "8090e26a16b7acd775da56b81102969b755f9ee75dbda8a98d23cc0fbdb328cd",
          "issue": "issue_aa78c58234c628fd41a0"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "fb4a1e7813f154ffabe6bbd042883753d6646b96950a552f130fd682887b2f79",
          "issue": "issue_aa78c58234c628fd41a0"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "88d118f96081fc101789b270dc4cfde1139510742f073119a974ff77a18e1d6c",
          "issue": "issue_9811ea1f2b6d61ccb5c4"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1422c21e14ac49b032978a0b2d1584f7f2b585a6aac796d5cd747466672878fa",
          "issue": "issue_9811ea1f2b6d61ccb5c4"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "b5796a64eeb14520ad8b73e3bc9418388ce3651f43c8e0fc7eba50c39d8816f4",
          "issue": "issue_1c72568f61f4f2d155d0"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "6657921aeffb0b9124e123c4b2210ec4f69a2644dc8a611cf4822a03201bb99d",
          "issue": "issue_1c72568f61f4f2d155d0"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_049d9f900720751059ae",
        "fact": "fact_54471e93378e145079d1",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_54471e93378e145079d1",
        "object_or_effect": "o_9844ea69c0236919c3f1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_bfd6211cccb025c59608",
        "object_or_effect": "w_090d4bdf81f4b8d47f0e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_090d4bdf81f4b8d47f0e",
        "grounded": true
      },
      {
        "id": "fact_e12c79356a247b137ef4",
        "object_or_effect": "w_976b031590b61a073cd7",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_976b031590b61a073cd7",
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "invalid_semantic_row": 5,
      "category_ambiguous_or_outside_supported_task": 8,
      "unknown_assessment_vocabulary": 8,
      "no_locatable_source": 8,
      "unbound_or_inapplicable_seed": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 34,
      "external_dependency": 10,
      "source_task_reading": 1
    }
  }
}
```

## RQ1_be17ecaef698

证据目录 run/members/RQ1_be17ecaef698/attempt_1/，报告哈希 dabbf31f0b2770884282905ea64e7504116b8537559011707d79a96919c9b421

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "last1164 丢失根因 D2:597:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope,unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_be17ecaef698",
        "reference": "D2:597:author:1",
        "function": "clearBlockchain",
        "v32": "FN",
        "last1164": "TP",
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
        "lost": [
          "D2:597:author:1"
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
          "detail_sha256": "837760f532aa8833fe5665df554d0ead715d4004b6351c209947afb5a57f7dec",
          "issue": "issue_d6ab2ddf61802815913c"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "3eff81edf9294522524bfb0dd160edddc354d99a31e4af747e1403324ab4f858",
          "issue": "issue_d6ab2ddf61802815913c"
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
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [
      4722
    ],
    "new": [],
    "disappeared_to_unknown": true,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [],
    "facts": [],
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
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 2
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "invalid_semantic_row": 5,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 3,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 14,
      "source_task_reading": 9,
      "policy_missing": 2,
      "external_dependency": 3
    }
  }
}
```

## RQ1_c0ce67b52132

证据目录 run/members/RQ1_c0ce67b52132/attempt_1/，报告哈希 2410fb2c13c60bc6e6882916446eb21d9bf2abc5be70e9b35565775b8868928a

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
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
        "member": "RQ1_c0ce67b52132",
        "reference": "D2:267:author:1",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "c7cd262a4739b000c154c65ff361a03c705ab548ec53bd7aac74316279bacae7",
          "issue": "issue_3c0447fa3c7f07efc643"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1e9be9c9ca2e301799a021bd09124d4e25df37557c412409dc3b8a670fd94bb2",
          "issue": "issue_3c0447fa3c7f07efc643"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ed8a911e9da30867794511f75140c9662e20cd9ae0a5244351ef18f25ebfa8bb",
          "issue": "issue_732aacf40fbb103b526a"
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
        "support": "support_3e7f0d030eeead38a45a",
        "fact": "fact_a774ae0eff9341859efa",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_a774ae0eff9341859efa",
        "object_or_effect": "o_514d8039a5c0a1795075",
        "meaning": "other_source_meaning",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 5,
      "category_ambiguous_or_outside_supported_task": 1,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 1
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

## RQ1_c20b10d094d5

证据目录 run/members/RQ1_c20b10d094d5/attempt_1/，报告哈希 466edda89c5e7ccf343ed014a54c03a681e47ed26853ec086e24b2f8263d885e

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:50:author:1",
    "last1164 丢失根因 D2:50:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,invalid_semantic_row,semantic_answer_outside_sent_scope,unbound_or_inapplicable_seed",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_c20b10d094d5",
        "reference": "D2:50:author:1",
        "function": "ETHERanate",
        "v32": "TP",
        "last1164": "TP",
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
        "lost": [
          "D2:50:author:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:50:author:1"
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
          "detail_sha256": "b36458fabdc42b9ed487b5f74bee6fe0045895890fcfc69dc194b93bf6089d65",
          "issue": "issue_453697cab855b8289a30"
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
        "support": "support_4477462720c157804277",
        "fact": "fact_89037030d1d7e5a62b5f",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_495ea76049e02a8f4d89",
        "fact": "fact_30e8499f66c14352c7e1",
        "origin": "verified_service",
        "field": "policies",
        "version": 1
      },
      {
        "support": "support_c36586f01ca12a0eb7c2",
        "fact": "fact_89037030d1d7e5a62b5f",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_004850c64331adf5418a",
        "object_or_effect": "w_781d930325ad6f398a11",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_781d930325ad6f398a11",
        "grounded": true
      },
      {
        "id": "fact_007e3afaf588b30d5ffc",
        "object_or_effect": "w_a1f636e2ff091c814e5e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a1f636e2ff091c814e5e",
        "grounded": true
      },
      {
        "id": "fact_01497be6c64c2bb47251",
        "object_or_effect": "w_18c59869f93e5349b844",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_18c59869f93e5349b844",
        "grounded": true
      },
      {
        "id": "fact_026e7ed546dc7d2df68c",
        "object_or_effect": "w_cd85d2685ff6bcbb17be",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_cd85d2685ff6bcbb17be",
        "grounded": true
      },
      {
        "id": "fact_02bc95f0f00917457920",
        "object_or_effect": "w_5c83e0f6e3fdba17d0df",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_5c83e0f6e3fdba17d0df",
        "grounded": true
      },
      {
        "id": "fact_035ba1605bd369717423",
        "object_or_effect": "w_4fceb4c6165d137cb307",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4fceb4c6165d137cb307",
        "grounded": true
      },
      {
        "id": "fact_06344264a6052a4229a1",
        "object_or_effect": "w_c8ed13b21d093b62fa65",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c8ed13b21d093b62fa65",
        "grounded": true
      },
      {
        "id": "fact_06e8e2fa543b3dda820a",
        "object_or_effect": "w_fa2c3797a2553e754279",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_fa2c3797a2553e754279",
        "grounded": true
      },
      {
        "id": "fact_079df5848cf236280a1f",
        "object_or_effect": "w_340bd5be940d2691a6c2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_340bd5be940d2691a6c2",
        "grounded": true
      },
      {
        "id": "fact_07dbf97324b3f564e85b",
        "object_or_effect": "w_d432f76b0d44c728dbdc",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d432f76b0d44c728dbdc",
        "grounded": true
      },
      {
        "id": "fact_08a75c688e0f7f0a629b",
        "object_or_effect": "w_b29fe6a8347f75931050",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b29fe6a8347f75931050",
        "grounded": true
      },
      {
        "id": "fact_094a12b2867fa31a8896",
        "object_or_effect": "w_e3749196d3916eefdc57",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_e3749196d3916eefdc57",
        "grounded": true
      },
      {
        "id": "fact_099e753e4f66b7693342",
        "object_or_effect": "w_e097680af0de00e158e5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_e097680af0de00e158e5",
        "grounded": true
      },
      {
        "id": "fact_0ad2eb4c27f45c9f8900",
        "object_or_effect": "w_58a67390de544de47d65",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_58a67390de544de47d65",
        "grounded": true
      },
      {
        "id": "fact_0b59ca6bd4768011752e",
        "object_or_effect": "w_2232c7896beb479c56ed",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2232c7896beb479c56ed",
        "grounded": true
      },
      {
        "id": "fact_0b8143683f5c1a344b41",
        "object_or_effect": "w_4fba2a4392eabb71df35",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4fba2a4392eabb71df35",
        "grounded": true
      },
      {
        "id": "fact_0cdd4d7b464cc6548a86",
        "object_or_effect": "w_24b142a3e1d6b35c2d91",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_24b142a3e1d6b35c2d91",
        "grounded": true
      },
      {
        "id": "fact_0d066448c1b16445788a",
        "object_or_effect": "w_581ef93977760655f274",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_581ef93977760655f274",
        "grounded": true
      },
      {
        "id": "fact_0d9e631d7006bc948976",
        "object_or_effect": "w_6c5631f5db47f1bda0f4",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6c5631f5db47f1bda0f4",
        "grounded": true
      },
      {
        "id": "fact_0ebc736ff6c22d4bdbd7",
        "object_or_effect": "w_5c5e1421604839e1fd34",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_5c5e1421604839e1fd34",
        "grounded": true
      },
      {
        "id": "fact_0fe50f8ed2d6bab68f37",
        "object_or_effect": "w_455dc01d28f10e466fe3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_455dc01d28f10e466fe3",
        "grounded": true
      },
      {
        "id": "fact_0ff7d060f9ef0f62f8a2",
        "object_or_effect": "w_6e78fc008979505a7a33",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6e78fc008979505a7a33",
        "grounded": true
      },
      {
        "id": "fact_10e287c687c8e403da90",
        "object_or_effect": "w_631bde043b02734aafcc",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_631bde043b02734aafcc",
        "grounded": true
      },
      {
        "id": "fact_116866f617c8bcab2a83",
        "object_or_effect": "w_8f55b33dd9a1cd3749c6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8f55b33dd9a1cd3749c6",
        "grounded": true
      },
      {
        "id": "fact_11ee68612251ea0a85c1",
        "object_or_effect": "w_eafe3d36f003307cca89",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_eafe3d36f003307cca89",
        "grounded": true
      },
      {
        "id": "fact_12f359b8baef1edf72cc",
        "object_or_effect": "w_8ae55d9ff0f4dabf8864",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8ae55d9ff0f4dabf8864",
        "grounded": true
      },
      {
        "id": "fact_1454ed953acc53730f97",
        "object_or_effect": "w_c5ed296f28ac08ee5337",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c5ed296f28ac08ee5337",
        "grounded": true
      },
      {
        "id": "fact_155058c82fb4f383cbac",
        "object_or_effect": "w_17034a092f0d8f726166",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_17034a092f0d8f726166",
        "grounded": true
      },
      {
        "id": "fact_159a33f5d967858d1235",
        "object_or_effect": "w_56fe7b586833fbb415d2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_56fe7b586833fbb415d2",
        "grounded": true
      },
      {
        "id": "fact_16457b0ebea45eaffe4c",
        "object_or_effect": "w_c8cae0e41c69810ce3f8",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c8cae0e41c69810ce3f8",
        "grounded": true
      },
      {
        "id": "fact_172bfb615d6176de12e0",
        "object_or_effect": "w_a52678066190601abcd0",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a52678066190601abcd0",
        "grounded": true
      },
      {
        "id": "fact_174f4745b2fe58fff0f6",
        "object_or_effect": "w_745822c374ce961c078f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_745822c374ce961c078f",
        "grounded": true
      },
      {
        "id": "fact_17d20fe009239e7eab7f",
        "object_or_effect": "w_22fc21ad183a7e4f1fe2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_22fc21ad183a7e4f1fe2",
        "grounded": true
      },
      {
        "id": "fact_188cfb47a97402e64819",
        "object_or_effect": "w_d8cbbc181012e71fc4ee",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d8cbbc181012e71fc4ee",
        "grounded": true
      },
      {
        "id": "fact_19e92993e87e61d3eda2",
        "object_or_effect": "w_1054c49c5cf7b5523007",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_1054c49c5cf7b5523007",
        "grounded": true
      },
      {
        "id": "fact_1a167f9ef8d84e9b48ed",
        "object_or_effect": "w_9bcc35da1aca8ab2a017",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_9bcc35da1aca8ab2a017",
        "grounded": true
      },
      {
        "id": "fact_1a4aae9853abc9b38355",
        "object_or_effect": "w_a0ad2d04e74dd6290b2c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a0ad2d04e74dd6290b2c",
        "grounded": true
      },
      {
        "id": "fact_1b22a513b9cc3cbd345a",
        "object_or_effect": "w_20a31fb497bb7947e71b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_20a31fb497bb7947e71b",
        "grounded": true
      },
      {
        "id": "fact_1c4645e97144a6a5e5ee",
        "object_or_effect": "w_1de3e6906407d7389b83",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_1de3e6906407d7389b83",
        "grounded": true
      },
      {
        "id": "fact_1c85207f01f9f4e72d8b",
        "object_or_effect": "w_469d07a5ee6d1df70fc4",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_469d07a5ee6d1df70fc4",
        "grounded": true
      },
      {
        "id": "fact_1cce91ae96197a8b4979",
        "object_or_effect": "w_e1ae99bb19d002fc9038",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_e1ae99bb19d002fc9038",
        "grounded": true
      },
      {
        "id": "fact_1cedcf2244322f49b6f7",
        "object_or_effect": "w_49f7450c99b9f683afc9",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_49f7450c99b9f683afc9",
        "grounded": true
      },
      {
        "id": "fact_1e00288b172973fd31c9",
        "object_or_effect": "w_45bbe9e954f029a8ff89",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_45bbe9e954f029a8ff89",
        "grounded": true
      },
      {
        "id": "fact_1e5e8adf7a63756f0a81",
        "object_or_effect": "w_6dcf37e39014860dc413",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6dcf37e39014860dc413",
        "grounded": true
      },
      {
        "id": "fact_1ecec262b0181cc07d20",
        "object_or_effect": "w_8d4e391445938bf57429",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8d4e391445938bf57429",
        "grounded": true
      },
      {
        "id": "fact_211e78676044d63d77a3",
        "object_or_effect": "w_30b85b028acaac21cfb8",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_30b85b028acaac21cfb8",
        "grounded": true
      },
      {
        "id": "fact_21c71404db8df54a2dde",
        "object_or_effect": "w_9a9a6fd801d064871031",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_9a9a6fd801d064871031",
        "grounded": true
      },
      {
        "id": "fact_21c9440d35356a873655",
        "object_or_effect": "w_c404019914bca86ded3c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c404019914bca86ded3c",
        "grounded": true
      },
      {
        "id": "fact_2242bc78e47b5e2a0178",
        "object_or_effect": "w_ee1beda2ad049fe08431",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_ee1beda2ad049fe08431",
        "grounded": true
      },
      {
        "id": "fact_22dfc2d11962b7f0f2b6",
        "object_or_effect": "w_c6427c0bc4b63e561606",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c6427c0bc4b63e561606",
        "grounded": true
      },
      {
        "id": "fact_22e1a053b2a00fb58bb0",
        "object_or_effect": "w_8c1d24f33785dcec8ff5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8c1d24f33785dcec8ff5",
        "grounded": true
      },
      {
        "id": "fact_230a98695e941af490bf",
        "object_or_effect": "w_629a0f8bffdeb66181f3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_629a0f8bffdeb66181f3",
        "grounded": true
      },
      {
        "id": "fact_23509997f6de737f15a7",
        "object_or_effect": "w_8be3037e674ce8248301",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8be3037e674ce8248301",
        "grounded": true
      },
      {
        "id": "fact_24cc476b9b9eeb5dbb9c",
        "object_or_effect": "w_57d91882da012bb6b1fd",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_57d91882da012bb6b1fd",
        "grounded": true
      },
      {
        "id": "fact_267a7d1c92cb7929aace",
        "object_or_effect": "w_dc10fd35605ae85d1153",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_dc10fd35605ae85d1153",
        "grounded": true
      },
      {
        "id": "fact_2883ecb7d91a505f1206",
        "object_or_effect": "w_32207ec68660baf6aeb6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_32207ec68660baf6aeb6",
        "grounded": true
      },
      {
        "id": "fact_299ce17b7b15636618d5",
        "object_or_effect": "w_b04bd86e4848dc2ca15a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b04bd86e4848dc2ca15a",
        "grounded": true
      },
      {
        "id": "fact_29f44cac2337fa3c1cfe",
        "object_or_effect": "w_b50f4d7c2c820862e844",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b50f4d7c2c820862e844",
        "grounded": true
      },
      {
        "id": "fact_2aebc3562d0e82645b60",
        "object_or_effect": "w_fb938a1f1a18089cc170",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_fb938a1f1a18089cc170",
        "grounded": true
      },
      {
        "id": "fact_2b5368b180bde925297f",
        "object_or_effect": "w_66e16bcd9e62fafc82be",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_66e16bcd9e62fafc82be",
        "grounded": true
      },
      {
        "id": "fact_2bc5058d5f9005ed1aa0",
        "object_or_effect": "w_1a65ec6e5d8b16082828",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_1a65ec6e5d8b16082828",
        "grounded": true
      },
      {
        "id": "fact_2c2680a5e86184a520ea",
        "object_or_effect": "w_f4488637a2b762d3d0ff",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_f4488637a2b762d3d0ff",
        "grounded": true
      },
      {
        "id": "fact_2c67ae3c30a65a184e70",
        "object_or_effect": "w_8252ebb5e791139c23ae",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8252ebb5e791139c23ae",
        "grounded": true
      },
      {
        "id": "fact_2ca106f475d787c7fb70",
        "object_or_effect": "w_59a2252d71190d269674",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_59a2252d71190d269674",
        "grounded": true
      },
      {
        "id": "fact_2ceccd5863ee18216970",
        "object_or_effect": "w_587013dc81eb435daeb1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_587013dc81eb435daeb1",
        "grounded": true
      },
      {
        "id": "fact_2d1ff3e9b47d976f909c",
        "object_or_effect": "w_7b239c2654c61dc6985d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_7b239c2654c61dc6985d",
        "grounded": true
      },
      {
        "id": "fact_2d8ab8fdf9948db939fc",
        "object_or_effect": "w_6d412cd2e0cb9040119e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6d412cd2e0cb9040119e",
        "grounded": true
      },
      {
        "id": "fact_2f12ba7a754e1dcdb399",
        "object_or_effect": "w_0dda966d677d3a716924",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0dda966d677d3a716924",
        "grounded": true
      },
      {
        "id": "fact_303a5fad94c229dc5885",
        "object_or_effect": "w_82a2c7ab97f7305e18ef",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_82a2c7ab97f7305e18ef",
        "grounded": true
      },
      {
        "id": "fact_3068c2021e6f4d818122",
        "object_or_effect": "w_12a12143131cd0c6ba16",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_12a12143131cd0c6ba16",
        "grounded": true
      },
      {
        "id": "fact_30e8499f66c14352c7e1",
        "object_or_effect": "e_02792fd122ac2636d5c2",
        "meaning": "current_authority_required",
        "role": null,
        "subject": "o_f485d321fbf405817bae",
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_314e95e67d59184e0904",
        "object_or_effect": "w_3a606cab48b246b0d2a2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_3a606cab48b246b0d2a2",
        "grounded": true
      },
      {
        "id": "fact_327d300500742266ad88",
        "object_or_effect": "w_0727fec8abae0055519c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0727fec8abae0055519c",
        "grounded": true
      },
      {
        "id": "fact_3415e29e8748c940dc5c",
        "object_or_effect": "w_49b724f69d376f561ff9",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_49b724f69d376f561ff9",
        "grounded": true
      },
      {
        "id": "fact_35426cf5dfa4f4f5a084",
        "object_or_effect": "w_0a2f62176b1b2bf74af2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0a2f62176b1b2bf74af2",
        "grounded": true
      },
      {
        "id": "fact_35bac61e19d7498816a3",
        "object_or_effect": "w_d2398990b53fdfa1e2c9",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d2398990b53fdfa1e2c9",
        "grounded": true
      },
      {
        "id": "fact_3731906cf6d941adecb2",
        "object_or_effect": "w_a0fadd26136915961c99",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a0fadd26136915961c99",
        "grounded": true
      },
      {
        "id": "fact_37e02d58cffced354370",
        "object_or_effect": "w_d0493cb1ef7b72b04a33",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d0493cb1ef7b72b04a33",
        "grounded": true
      },
      {
        "id": "fact_38522a5cd6c7767c5458",
        "object_or_effect": "w_54bcd41f007625804fac",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_54bcd41f007625804fac",
        "grounded": true
      },
      {
        "id": "fact_395131a0956693d1298e",
        "object_or_effect": "w_6f78814de65c8d4defbe",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6f78814de65c8d4defbe",
        "grounded": true
      },
      {
        "id": "fact_3b3593b33b8f764455f8",
        "object_or_effect": "w_19e5f65e69356f5c6aee",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_19e5f65e69356f5c6aee",
        "grounded": true
      },
      {
        "id": "fact_3c2cfd70d54f0f7eeca2",
        "object_or_effect": "w_54c43b1a4fbb50eecd33",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_54c43b1a4fbb50eecd33",
        "grounded": true
      },
      {
        "id": "fact_3d7dd5434986e0705f30",
        "object_or_effect": "w_a6bbd136885cc90626dc",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a6bbd136885cc90626dc",
        "grounded": true
      },
      {
        "id": "fact_3fbd2d47a1e795efe9d1",
        "object_or_effect": "w_2c0ff7106d9347c12dde",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2c0ff7106d9347c12dde",
        "grounded": true
      },
      {
        "id": "fact_4106926c62f83b0e8de8",
        "object_or_effect": "w_17060e494f894bd598b5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_17060e494f894bd598b5",
        "grounded": true
      },
      {
        "id": "fact_434b886d12117ed73e65",
        "object_or_effect": "w_5fd7cf7d7b3bc4e152c5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_5fd7cf7d7b3bc4e152c5",
        "grounded": true
      },
      {
        "id": "fact_440b22a0d5b090db3b8f",
        "object_or_effect": "w_c7fdaa692d24357d8ec3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c7fdaa692d24357d8ec3",
        "grounded": true
      },
      {
        "id": "fact_44159b3bb6892953f6a5",
        "object_or_effect": "w_4c0733da752fa5eef5e2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4c0733da752fa5eef5e2",
        "grounded": true
      },
      {
        "id": "fact_4667122eda420c880761",
        "object_or_effect": "w_8dcf5c79ef7a011e70d4",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8dcf5c79ef7a011e70d4",
        "grounded": true
      },
      {
        "id": "fact_4765c2afa6913244031c",
        "object_or_effect": "w_7e5f284441348f609ea6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_7e5f284441348f609ea6",
        "grounded": true
      },
      {
        "id": "fact_47f5dc2145c72f4041fa",
        "object_or_effect": "w_4d01717980cb97726abf",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4d01717980cb97726abf",
        "grounded": true
      },
      {
        "id": "fact_495f95998d6c888aa7f8",
        "object_or_effect": "w_c8409396bd05a47398ea",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c8409396bd05a47398ea",
        "grounded": true
      },
      {
        "id": "fact_496f409bbb52386c5067",
        "object_or_effect": "w_3df370438b5fa9f34ae7",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_3df370438b5fa9f34ae7",
        "grounded": true
      },
      {
        "id": "fact_49ca612812e1ca938d3f",
        "object_or_effect": "w_4c8313c2e057af111e8c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4c8313c2e057af111e8c",
        "grounded": true
      },
      {
        "id": "fact_4b135fcbed14b84d0a1d",
        "object_or_effect": "w_2a914de11204852bebc7",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2a914de11204852bebc7",
        "grounded": true
      },
      {
        "id": "fact_4be83aa9f294214a7b9a",
        "object_or_effect": "w_246f8747d02f8516c80e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_246f8747d02f8516c80e",
        "grounded": true
      },
      {
        "id": "fact_4d81cf7697ea767d4a28",
        "object_or_effect": "w_bc3d06c6e08e7ea6c0ea",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_bc3d06c6e08e7ea6c0ea",
        "grounded": true
      },
      {
        "id": "fact_4d88a3a749982b07cc11",
        "object_or_effect": "w_a91dd7e51140b0d72649",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a91dd7e51140b0d72649",
        "grounded": true
      },
      {
        "id": "fact_4dbfe69e8f3c3b6552f2",
        "object_or_effect": "w_6bcdc192a4c00e95504b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6bcdc192a4c00e95504b",
        "grounded": true
      },
      {
        "id": "fact_4e00a7b0f3c8d168afa6",
        "object_or_effect": "w_da1fdda4f3b78b6e3014",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_da1fdda4f3b78b6e3014",
        "grounded": true
      },
      {
        "id": "fact_4ee1aace5c49dc0b9b45",
        "object_or_effect": "w_f6f453082012961f7fbb",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_f6f453082012961f7fbb",
        "grounded": true
      },
      {
        "id": "fact_4f39746c5bb0399bab8f",
        "object_or_effect": "w_b47bd8fcb92b9aa8a45e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b47bd8fcb92b9aa8a45e",
        "grounded": true
      },
      {
        "id": "fact_4fc9ea8a8f6f83aa0704",
        "object_or_effect": "w_f3656f7b74a856c758be",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_f3656f7b74a856c758be",
        "grounded": true
      },
      {
        "id": "fact_5261ac7208cb9c418d1d",
        "object_or_effect": "w_22982145e7c8313feb1f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_22982145e7c8313feb1f",
        "grounded": true
      },
      {
        "id": "fact_5303ea329a785bd80662",
        "object_or_effect": "w_aa0ed818f276c7ecb0a5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_aa0ed818f276c7ecb0a5",
        "grounded": true
      },
      {
        "id": "fact_534d65d12fcd0824f05b",
        "object_or_effect": "w_4a8bd26115d21cdd43bf",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4a8bd26115d21cdd43bf",
        "grounded": true
      },
      {
        "id": "fact_53d9747ba621174d0673",
        "object_or_effect": "w_25dc54ac1c67dd5ddef1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_25dc54ac1c67dd5ddef1",
        "grounded": true
      },
      {
        "id": "fact_54777d419092c7bcd4b9",
        "object_or_effect": "w_9bb08481ce404ee08b6d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_9bb08481ce404ee08b6d",
        "grounded": true
      },
      {
        "id": "fact_55e58dcdfddc4da94989",
        "object_or_effect": "w_04338ccebb2703010a1c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_04338ccebb2703010a1c",
        "grounded": true
      },
      {
        "id": "fact_56c992a8a6410499fd52",
        "object_or_effect": "w_d362354fef79086fe408",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d362354fef79086fe408",
        "grounded": true
      },
      {
        "id": "fact_570cf77a142815c52f19",
        "object_or_effect": "w_996910c19df4cec997c5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_996910c19df4cec997c5",
        "grounded": true
      },
      {
        "id": "fact_5755a7017cb3459dcee2",
        "object_or_effect": "w_9b80d14b72772f1623a6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_9b80d14b72772f1623a6",
        "grounded": true
      },
      {
        "id": "fact_58f6006ca8d921a1dd02",
        "object_or_effect": "w_29a14e985c54f42dbe93",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_29a14e985c54f42dbe93",
        "grounded": true
      },
      {
        "id": "fact_59eeaaa37bff1b3b7448",
        "object_or_effect": "w_493981cda8d6e1d9f6f1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_493981cda8d6e1d9f6f1",
        "grounded": true
      },
      {
        "id": "fact_5ab4d98587ea18fd5880",
        "object_or_effect": "w_12b1404fb032ff3236a5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_12b1404fb032ff3236a5",
        "grounded": true
      },
      {
        "id": "fact_5ab641dad8756392934d",
        "object_or_effect": "w_2d4e36656f168bb04d0c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2d4e36656f168bb04d0c",
        "grounded": true
      },
      {
        "id": "fact_5c2296374a87c95203db",
        "object_or_effect": "w_de8d1724188910f6bb8b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_de8d1724188910f6bb8b",
        "grounded": true
      },
      {
        "id": "fact_5c26338aeb60c8a143fb",
        "object_or_effect": "w_841971845b9dd94644f6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_841971845b9dd94644f6",
        "grounded": true
      },
      {
        "id": "fact_5c6840cc2ee67d881a24",
        "object_or_effect": "w_d2c4da21b2479f04334c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d2c4da21b2479f04334c",
        "grounded": true
      },
      {
        "id": "fact_5cec373223c37e508d60",
        "object_or_effect": "w_6674e8a393f9ae067817",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6674e8a393f9ae067817",
        "grounded": true
      },
      {
        "id": "fact_5d0df04daa7aade9ce22",
        "object_or_effect": "w_7cde8f8f728aad00ea82",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_7cde8f8f728aad00ea82",
        "grounded": true
      },
      {
        "id": "fact_5d422a7f95e540c53457",
        "object_or_effect": "w_c402e9b7439d04a3d8c2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c402e9b7439d04a3d8c2",
        "grounded": true
      },
      {
        "id": "fact_5e42ee4564fbb8c64ab1",
        "object_or_effect": "w_720ffa2076fc49c886ac",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_720ffa2076fc49c886ac",
        "grounded": true
      },
      {
        "id": "fact_5fe8f22782643ebd815a",
        "object_or_effect": "w_c7aa7d7bf6f9d91b1431",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c7aa7d7bf6f9d91b1431",
        "grounded": true
      },
      {
        "id": "fact_600e8b987dae5bd6dca5",
        "object_or_effect": "w_42e98503fadba842e0b9",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_42e98503fadba842e0b9",
        "grounded": true
      },
      {
        "id": "fact_607b789e4812a8dfc05e",
        "object_or_effect": "w_0c1adecef9fbca65ac85",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0c1adecef9fbca65ac85",
        "grounded": true
      },
      {
        "id": "fact_618ee18f2ab55fd6ddf7",
        "object_or_effect": "w_7d241ddd53bc0bd68812",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_7d241ddd53bc0bd68812",
        "grounded": true
      },
      {
        "id": "fact_61a6b0a745443515f507",
        "object_or_effect": "w_afda13ff1d3d0aa39f92",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_afda13ff1d3d0aa39f92",
        "grounded": true
      },
      {
        "id": "fact_62d1fd6f18708a9cb236",
        "object_or_effect": "w_04138249b4673e6ea141",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_04138249b4673e6ea141",
        "grounded": true
      },
      {
        "id": "fact_62f18f509833f7866347",
        "object_or_effect": "w_ac60792ff143b7f0ff10",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_ac60792ff143b7f0ff10",
        "grounded": true
      },
      {
        "id": "fact_638e6c6a07a392c0acbe",
        "object_or_effect": "w_9b9610b25b2f0a582ee3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_9b9610b25b2f0a582ee3",
        "grounded": true
      },
      {
        "id": "fact_645e576192cf00efd03f",
        "object_or_effect": "w_2c81c7c72684816b49a5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2c81c7c72684816b49a5",
        "grounded": true
      },
      {
        "id": "fact_66c6543188eee77ddea0",
        "object_or_effect": "w_8a59ff793db124306f49",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8a59ff793db124306f49",
        "grounded": true
      },
      {
        "id": "fact_675ef3a37f8020fce4ef",
        "object_or_effect": "w_09857b417df1977d6555",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_09857b417df1977d6555",
        "grounded": true
      },
      {
        "id": "fact_6762055840f3bb3abe42",
        "object_or_effect": "w_29667a7e577ac64affb3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_29667a7e577ac64affb3",
        "grounded": true
      },
      {
        "id": "fact_67641e7a5009e5bb1d16",
        "object_or_effect": "w_99a396ff7f3039c7130d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_99a396ff7f3039c7130d",
        "grounded": true
      },
      {
        "id": "fact_6a590bf88642a475faa3",
        "object_or_effect": "w_86d9e9177cd9c6f1cc4d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_86d9e9177cd9c6f1cc4d",
        "grounded": true
      },
      {
        "id": "fact_6a89d4ed89b5b686ec5e",
        "object_or_effect": "w_0678eeb4ba12a64837e1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0678eeb4ba12a64837e1",
        "grounded": true
      },
      {
        "id": "fact_6debe1a9187bc1a91ad0",
        "object_or_effect": "w_2e9e98cfb9bd0fe47ca9",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2e9e98cfb9bd0fe47ca9",
        "grounded": true
      },
      {
        "id": "fact_6ea9ed7df95be2bb19dc",
        "object_or_effect": "w_e6bda8a807003a09314c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_e6bda8a807003a09314c",
        "grounded": true
      },
      {
        "id": "fact_6eb317aa1613ade0e18f",
        "object_or_effect": "w_dcb25862bd73511158f8",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_dcb25862bd73511158f8",
        "grounded": true
      },
      {
        "id": "fact_6eea29084fefa30aaeca",
        "object_or_effect": "w_338d3ecb06e346d779b5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_338d3ecb06e346d779b5",
        "grounded": true
      },
      {
        "id": "fact_6fb4ed9ac3e1452cde51",
        "object_or_effect": "w_353529753cc15960ddee",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_353529753cc15960ddee",
        "grounded": true
      },
      {
        "id": "fact_700c50ae94859b48dc2f",
        "object_or_effect": "w_c0093fc468a7c6ca7569",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c0093fc468a7c6ca7569",
        "grounded": true
      },
      {
        "id": "fact_70304c63ab75db97d539",
        "object_or_effect": "w_75ec651f31575fd2027d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_75ec651f31575fd2027d",
        "grounded": true
      },
      {
        "id": "fact_70b5136f74c2dc4df71e",
        "object_or_effect": "w_a52814338ac52bc27c10",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a52814338ac52bc27c10",
        "grounded": true
      },
      {
        "id": "fact_711548fe0be008bf363c",
        "object_or_effect": "w_f710c29c2488fd010c4c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_f710c29c2488fd010c4c",
        "grounded": true
      },
      {
        "id": "fact_7152f841b40f11c44deb",
        "object_or_effect": "w_502e46efc81d88d8192b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_502e46efc81d88d8192b",
        "grounded": true
      },
      {
        "id": "fact_720036b5e63d859fcc82",
        "object_or_effect": "w_0dcfbc3105f1b5da8c56",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0dcfbc3105f1b5da8c56",
        "grounded": true
      },
      {
        "id": "fact_744d13c712ac8c99c63c",
        "object_or_effect": "w_4490244a0980af9261ef",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4490244a0980af9261ef",
        "grounded": true
      },
      {
        "id": "fact_74805629fd9a09185b01",
        "object_or_effect": "w_660da50caeeb5fa8e344",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_660da50caeeb5fa8e344",
        "grounded": true
      },
      {
        "id": "fact_77dd1b1fbe0259d66e10",
        "object_or_effect": "w_87819b809ba5ac5ee4ec",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_87819b809ba5ac5ee4ec",
        "grounded": true
      },
      {
        "id": "fact_7ab035cabcd92093d7ab",
        "object_or_effect": "w_acc29fb1400b0e0cdcee",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_acc29fb1400b0e0cdcee",
        "grounded": true
      },
      {
        "id": "fact_7ac962e9df08d279e9f0",
        "object_or_effect": "w_a9e330d89defdac9085f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a9e330d89defdac9085f",
        "grounded": true
      },
      {
        "id": "fact_7d115431022c80bd81b3",
        "object_or_effect": "w_0bfaf972f1c86d39fe0d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0bfaf972f1c86d39fe0d",
        "grounded": true
      },
      {
        "id": "fact_7da9838114ef1d79dafb",
        "object_or_effect": "w_dfbe124c63bd7ff062db",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_dfbe124c63bd7ff062db",
        "grounded": true
      },
      {
        "id": "fact_7dd13f8e7c0e836fbbca",
        "object_or_effect": "w_8efd64d255276301d719",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8efd64d255276301d719",
        "grounded": true
      },
      {
        "id": "fact_7eb83ba430392b18a4c0",
        "object_or_effect": "w_aec0aae9d46bfc7cf08f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_aec0aae9d46bfc7cf08f",
        "grounded": true
      },
      {
        "id": "fact_7f2cc036fe6251477ece",
        "object_or_effect": "w_3191dc18945a1ba916a4",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_3191dc18945a1ba916a4",
        "grounded": true
      },
      {
        "id": "fact_801b0ae5abdd3aeb0983",
        "object_or_effect": "w_40adc7ae898268ef9e61",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_40adc7ae898268ef9e61",
        "grounded": true
      },
      {
        "id": "fact_830928ce265c1b74952e",
        "object_or_effect": "w_7a56c72fdd9d3c578aad",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_7a56c72fdd9d3c578aad",
        "grounded": true
      },
      {
        "id": "fact_830b2ab6b163cd964e06",
        "object_or_effect": "w_d323e57cc76fbbbea044",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d323e57cc76fbbbea044",
        "grounded": true
      },
      {
        "id": "fact_8398f2bdfbecee4c92d8",
        "object_or_effect": "w_64d1c29fc469d9132f17",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_64d1c29fc469d9132f17",
        "grounded": true
      },
      {
        "id": "fact_83fb4bb87b92ead74843",
        "object_or_effect": "w_e3c6134e18d33800aebf",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_e3c6134e18d33800aebf",
        "grounded": true
      },
      {
        "id": "fact_85381bf166584f53c34e",
        "object_or_effect": "w_a27dd354cf417e81fb55",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a27dd354cf417e81fb55",
        "grounded": true
      },
      {
        "id": "fact_8605e4d780d909090ce2",
        "object_or_effect": "w_4f713fc08e5e0a06906a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4f713fc08e5e0a06906a",
        "grounded": true
      },
      {
        "id": "fact_86180f3cde924a60e3ec",
        "object_or_effect": "w_8723b60a174bd3e0ef7e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8723b60a174bd3e0ef7e",
        "grounded": true
      },
      {
        "id": "fact_86920ce1bfed2515eace",
        "object_or_effect": "w_de02d4977208a0e425e6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_de02d4977208a0e425e6",
        "grounded": true
      },
      {
        "id": "fact_880b81cb97f86f367550",
        "object_or_effect": "w_de6914082a5be78b094a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_de6914082a5be78b094a",
        "grounded": true
      },
      {
        "id": "fact_889d6457e26356ba020b",
        "object_or_effect": "w_2f14a7a0e014c534adf6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2f14a7a0e014c534adf6",
        "grounded": true
      },
      {
        "id": "fact_89037030d1d7e5a62b5f",
        "object_or_effect": "o_f485d321fbf405817bae",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_898eebfe88d0a60a8da9",
        "object_or_effect": "w_bd68468ff9297002bb5b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_bd68468ff9297002bb5b",
        "grounded": true
      },
      {
        "id": "fact_89a977f451f5e0be088c",
        "object_or_effect": "w_694df033135be0fda963",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_694df033135be0fda963",
        "grounded": true
      },
      {
        "id": "fact_8a4453683e1608465c54",
        "object_or_effect": "w_fb4d1da38a771bbccf75",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_fb4d1da38a771bbccf75",
        "grounded": true
      },
      {
        "id": "fact_8a7f84b9da321c61b960",
        "object_or_effect": "w_bfd676547e530dfb7878",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_bfd676547e530dfb7878",
        "grounded": true
      },
      {
        "id": "fact_8a8b60591250c856615f",
        "object_or_effect": "w_0bcf53ef72c81c05d554",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0bcf53ef72c81c05d554",
        "grounded": true
      },
      {
        "id": "fact_8bada20bf0359f9d35fd",
        "object_or_effect": "w_2420e00b1a26ce5c143c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2420e00b1a26ce5c143c",
        "grounded": true
      },
      {
        "id": "fact_8c95f8fe1f958871d1d6",
        "object_or_effect": "w_95ccbfef9716de15a38b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_95ccbfef9716de15a38b",
        "grounded": true
      },
      {
        "id": "fact_8d18e4432f2df7a12df6",
        "object_or_effect": "w_681a949352ad2e4619ca",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_681a949352ad2e4619ca",
        "grounded": true
      },
      {
        "id": "fact_8d29d64f13e06b1f1495",
        "object_or_effect": "w_f1eaa0050f0ab8507224",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_f1eaa0050f0ab8507224",
        "grounded": true
      },
      {
        "id": "fact_8e0b9ef863700930a2fc",
        "object_or_effect": "w_3700607de6a9ed3df3f2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_3700607de6a9ed3df3f2",
        "grounded": true
      },
      {
        "id": "fact_8e2d1763ee94e0df0362",
        "object_or_effect": "w_daa186d875416cf5d135",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_daa186d875416cf5d135",
        "grounded": true
      },
      {
        "id": "fact_8f1340833acf95795f07",
        "object_or_effect": "w_e32f7fd4d36d20c9af5c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_e32f7fd4d36d20c9af5c",
        "grounded": true
      },
      {
        "id": "fact_8f13d4036247c5f6ec47",
        "object_or_effect": "w_0787fa9d472ae620a851",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0787fa9d472ae620a851",
        "grounded": true
      },
      {
        "id": "fact_902dce2476d775c680b7",
        "object_or_effect": "w_1e3af9d59a7691a6718d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_1e3af9d59a7691a6718d",
        "grounded": true
      },
      {
        "id": "fact_9237893d709f8b2d2e8b",
        "object_or_effect": "w_0233e8f6f39bcb636d0d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0233e8f6f39bcb636d0d",
        "grounded": true
      },
      {
        "id": "fact_93788e089868d32a1444",
        "object_or_effect": "w_60ae82a45e66d6fab676",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_60ae82a45e66d6fab676",
        "grounded": true
      },
      {
        "id": "fact_93e47c0f55abe9528e65",
        "object_or_effect": "w_af2e92f6d6a7c7907229",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_af2e92f6d6a7c7907229",
        "grounded": true
      },
      {
        "id": "fact_946c3dc07c4f50a1435f",
        "object_or_effect": "w_b0205d5097df9b85c378",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b0205d5097df9b85c378",
        "grounded": true
      },
      {
        "id": "fact_94bd4e74e95342ed43fb",
        "object_or_effect": "w_30ddde22acc55de56ebf",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_30ddde22acc55de56ebf",
        "grounded": true
      },
      {
        "id": "fact_9573722f8bbc3bde3cc3",
        "object_or_effect": "w_ecafe38a5dcff31eb593",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_ecafe38a5dcff31eb593",
        "grounded": true
      },
      {
        "id": "fact_971a7642c8d408a49f03",
        "object_or_effect": "w_2a434bffe60cd6154566",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2a434bffe60cd6154566",
        "grounded": true
      },
      {
        "id": "fact_978ca7bcd62f266cc06f",
        "object_or_effect": "w_a0d2c029eee565104418",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a0d2c029eee565104418",
        "grounded": true
      },
      {
        "id": "fact_9899756417ffec5aef18",
        "object_or_effect": "w_51f2b409aaffaac72747",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_51f2b409aaffaac72747",
        "grounded": true
      },
      {
        "id": "fact_98afe79936570f434512",
        "object_or_effect": "w_13dcacf2c530e6b2e9c4",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_13dcacf2c530e6b2e9c4",
        "grounded": true
      },
      {
        "id": "fact_98e6d7cb374bcb9d1444",
        "object_or_effect": "w_4ccc620a09f7c1f2e823",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4ccc620a09f7c1f2e823",
        "grounded": true
      },
      {
        "id": "fact_99a4955f5ac79515aa4e",
        "object_or_effect": "w_07dbee0231a02d5aa6a9",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_07dbee0231a02d5aa6a9",
        "grounded": true
      },
      {
        "id": "fact_9b149117ab81c51a7411",
        "object_or_effect": "w_1d667923ef65db7301ce",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_1d667923ef65db7301ce",
        "grounded": true
      },
      {
        "id": "fact_9b40c91c5bcf8d3dcb14",
        "object_or_effect": "w_85e4948ea58fc207e5b2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_85e4948ea58fc207e5b2",
        "grounded": true
      },
      {
        "id": "fact_9d169df4bef845dc96fc",
        "object_or_effect": "w_739eef1dc47792430504",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_739eef1dc47792430504",
        "grounded": true
      },
      {
        "id": "fact_9dc2378aa1c5c2f5aaf7",
        "object_or_effect": "w_ccb99b94430c44fed884",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_ccb99b94430c44fed884",
        "grounded": true
      },
      {
        "id": "fact_a1fe74d8144f726b91b4",
        "object_or_effect": "w_3d965c29ac4adc844f7c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_3d965c29ac4adc844f7c",
        "grounded": true
      },
      {
        "id": "fact_a29aa4e30b4d06c2137d",
        "object_or_effect": "w_0573a7ee0b3a16fbe4f3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0573a7ee0b3a16fbe4f3",
        "grounded": true
      },
      {
        "id": "fact_a2d64cfb53751ae0acfc",
        "object_or_effect": "w_16e490ddd50bd900e363",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_16e490ddd50bd900e363",
        "grounded": true
      },
      {
        "id": "fact_a2d70307e51a02ca8b09",
        "object_or_effect": "w_d34af543c8af0cb75518",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d34af543c8af0cb75518",
        "grounded": true
      },
      {
        "id": "fact_a4935aa59d372ecf6666",
        "object_or_effect": "w_21e03a234065c0cccffb",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_21e03a234065c0cccffb",
        "grounded": true
      },
      {
        "id": "fact_a5261be71370a792ad5d",
        "object_or_effect": "w_1806af68b838bf9cde3b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_1806af68b838bf9cde3b",
        "grounded": true
      },
      {
        "id": "fact_a52ddb5d51e98cd38a49",
        "object_or_effect": "w_63bfed910fb8aa64fc80",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_63bfed910fb8aa64fc80",
        "grounded": true
      },
      {
        "id": "fact_a553c8162f10326c9c6d",
        "object_or_effect": "w_7c2ffca16303d3f5373d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_7c2ffca16303d3f5373d",
        "grounded": true
      },
      {
        "id": "fact_a5f2de329a003dc765ce",
        "object_or_effect": "w_90d5f15aaada22a805b4",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_90d5f15aaada22a805b4",
        "grounded": true
      },
      {
        "id": "fact_a77f019848ff1b92520b",
        "object_or_effect": "w_e84d5a7f8254321169c9",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_e84d5a7f8254321169c9",
        "grounded": true
      },
      {
        "id": "fact_a86ec7235247bc40833c",
        "object_or_effect": "w_9046d6d62e9f178342b1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_9046d6d62e9f178342b1",
        "grounded": true
      },
      {
        "id": "fact_a929689deb20ede67746",
        "object_or_effect": "w_172f80e48c4af8f30ae3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_172f80e48c4af8f30ae3",
        "grounded": true
      },
      {
        "id": "fact_ac771c26f39a65c6e436",
        "object_or_effect": "w_c1a6c337706661ad93b6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c1a6c337706661ad93b6",
        "grounded": true
      },
      {
        "id": "fact_ac97f9891af5da547337",
        "object_or_effect": "w_662e9d031da3f4858af2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_662e9d031da3f4858af2",
        "grounded": true
      },
      {
        "id": "fact_ae14c5c2a6151db6ff67",
        "object_or_effect": "w_ada851b650ab0142ec10",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_ada851b650ab0142ec10",
        "grounded": true
      },
      {
        "id": "fact_aebf34e97e7cb5e40d6c",
        "object_or_effect": "w_b17de977bd3c3737fa45",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b17de977bd3c3737fa45",
        "grounded": true
      },
      {
        "id": "fact_af48761be0b1904f9a9d",
        "object_or_effect": "w_a0c856cfcad90063ab87",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a0c856cfcad90063ab87",
        "grounded": true
      },
      {
        "id": "fact_b06c2bed00e649c8e4c9",
        "object_or_effect": "w_1c0b97ba5d473977bc18",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_1c0b97ba5d473977bc18",
        "grounded": true
      },
      {
        "id": "fact_b17dc7081975c3bf1a6a",
        "object_or_effect": "w_6eb7ba3e33d7f6ec14a8",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6eb7ba3e33d7f6ec14a8",
        "grounded": true
      },
      {
        "id": "fact_b185d329a1de01f3768a",
        "object_or_effect": "w_a7ae1c501a5703bd0dc2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a7ae1c501a5703bd0dc2",
        "grounded": true
      },
      {
        "id": "fact_b1d1279e0410304071c5",
        "object_or_effect": "w_61926416f783dfe0ac42",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_61926416f783dfe0ac42",
        "grounded": true
      },
      {
        "id": "fact_b23e91f389b5f51680af",
        "object_or_effect": "w_bb81fb8ca96897975721",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_bb81fb8ca96897975721",
        "grounded": true
      },
      {
        "id": "fact_b493858240aca454e0d8",
        "object_or_effect": "w_d77a5c621948502055f5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d77a5c621948502055f5",
        "grounded": true
      },
      {
        "id": "fact_b59c243d8a587e401110",
        "object_or_effect": "w_9c8c45708bf40592e5e2",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_9c8c45708bf40592e5e2",
        "grounded": true
      },
      {
        "id": "fact_b65a78881ccffff23396",
        "object_or_effect": "w_cdb54d66348ff9ccc79b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_cdb54d66348ff9ccc79b",
        "grounded": true
      },
      {
        "id": "fact_b6c8ea31ada61d6a01fc",
        "object_or_effect": "w_c3a55968f19d15bed8d9",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c3a55968f19d15bed8d9",
        "grounded": true
      },
      {
        "id": "fact_b90af45961a5176314e9",
        "object_or_effect": "w_0fbbae7464957cdbcfc3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0fbbae7464957cdbcfc3",
        "grounded": true
      },
      {
        "id": "fact_b9b8dfa49b779304fa8a",
        "object_or_effect": "w_73c8da33fcf54c632281",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_73c8da33fcf54c632281",
        "grounded": true
      },
      {
        "id": "fact_b9f34b86e714240a73a7",
        "object_or_effect": "w_5eaf4f3348e5f131e47b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_5eaf4f3348e5f131e47b",
        "grounded": true
      },
      {
        "id": "fact_baf9fffc38d7eae94bf3",
        "object_or_effect": "w_7a1e200237b21044bed7",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_7a1e200237b21044bed7",
        "grounded": true
      },
      {
        "id": "fact_bb03c5cdc192f671dded",
        "object_or_effect": "w_29a7a9d6132b5b1b842f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_29a7a9d6132b5b1b842f",
        "grounded": true
      },
      {
        "id": "fact_bb511367ac6721ef70a2",
        "object_or_effect": "w_07e6b9ca40c14843c927",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_07e6b9ca40c14843c927",
        "grounded": true
      },
      {
        "id": "fact_bb9b29abf72941b9eec4",
        "object_or_effect": "w_b490e69fd7e7277dd584",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b490e69fd7e7277dd584",
        "grounded": true
      },
      {
        "id": "fact_bc4c7f4fde889f7302f1",
        "object_or_effect": "w_bc255b402e9695a1b1dd",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_bc255b402e9695a1b1dd",
        "grounded": true
      },
      {
        "id": "fact_bc745a333b76a731137f",
        "object_or_effect": "w_586f33fde784f6353854",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_586f33fde784f6353854",
        "grounded": true
      },
      {
        "id": "fact_bcb93d44e7184f6739e4",
        "object_or_effect": "w_1e0b25be48cf3081f6e6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_1e0b25be48cf3081f6e6",
        "grounded": true
      },
      {
        "id": "fact_bcf1d8546f9ea60572b6",
        "object_or_effect": "w_83944865af7caef04bda",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_83944865af7caef04bda",
        "grounded": true
      },
      {
        "id": "fact_bda56f9d6da8a6078b54",
        "object_or_effect": "w_51149d7b6161dff21ae8",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_51149d7b6161dff21ae8",
        "grounded": true
      },
      {
        "id": "fact_c1176f009b17413e1d8d",
        "object_or_effect": "w_6ee0518fbe2f0080dff9",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6ee0518fbe2f0080dff9",
        "grounded": true
      },
      {
        "id": "fact_c13a713a9c11f2bf84da",
        "object_or_effect": "w_53e03ae5f5f119a6be95",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_53e03ae5f5f119a6be95",
        "grounded": true
      },
      {
        "id": "fact_c1890265cfce0c8fc935",
        "object_or_effect": "w_b303b3395f6dbbfba0e8",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b303b3395f6dbbfba0e8",
        "grounded": true
      },
      {
        "id": "fact_c2f7df3b6ff222ae2627",
        "object_or_effect": "w_5be52cd8649e08baab92",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_5be52cd8649e08baab92",
        "grounded": true
      },
      {
        "id": "fact_c3668ee8a73fc0e2bd80",
        "object_or_effect": "w_61702eb0924a87529ff4",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_61702eb0924a87529ff4",
        "grounded": true
      },
      {
        "id": "fact_c43b232c6530d30a8bcf",
        "object_or_effect": "w_6364a37be0653859d19c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6364a37be0653859d19c",
        "grounded": true
      },
      {
        "id": "fact_c575f8e9fa5329305eb6",
        "object_or_effect": "w_69f557cfeb0ff5ddcef6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_69f557cfeb0ff5ddcef6",
        "grounded": true
      },
      {
        "id": "fact_c585626a6fb3c3861709",
        "object_or_effect": "w_2dcf49283e34ef64b66f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2dcf49283e34ef64b66f",
        "grounded": true
      },
      {
        "id": "fact_c6ec06a03904a9f28262",
        "object_or_effect": "w_737aa4f2a343375f5f8d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_737aa4f2a343375f5f8d",
        "grounded": true
      },
      {
        "id": "fact_c70a6a8dea46e3d12baf",
        "object_or_effect": "w_56aa769bbc0e4583bba4",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_56aa769bbc0e4583bba4",
        "grounded": true
      },
      {
        "id": "fact_c80cbc0d680d0565533d",
        "object_or_effect": "w_ef6590e8ff2baf4caa8a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_ef6590e8ff2baf4caa8a",
        "grounded": true
      },
      {
        "id": "fact_c9533f80fcdf32fd3cb3",
        "object_or_effect": "w_bba48c68657e4c377e15",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_bba48c68657e4c377e15",
        "grounded": true
      },
      {
        "id": "fact_c9c4d278f21449607aae",
        "object_or_effect": "w_67bd6e005d232e08b611",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_67bd6e005d232e08b611",
        "grounded": true
      },
      {
        "id": "fact_cdd903579d6407885779",
        "object_or_effect": "w_d7ad443e4beac063028c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d7ad443e4beac063028c",
        "grounded": true
      },
      {
        "id": "fact_cdf6874823b0f860ed94",
        "object_or_effect": "w_d00bd5a239ef8a24048a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d00bd5a239ef8a24048a",
        "grounded": true
      },
      {
        "id": "fact_ce176ac316c4fffed687",
        "object_or_effect": "w_c70875f8fa934fba475c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c70875f8fa934fba475c",
        "grounded": true
      },
      {
        "id": "fact_d185e9c15b2c1435afd5",
        "object_or_effect": "w_02e8f032459153823393",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_02e8f032459153823393",
        "grounded": true
      },
      {
        "id": "fact_d1939a85153a8b50d98e",
        "object_or_effect": "w_f98a2a667b00f4bd3608",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_f98a2a667b00f4bd3608",
        "grounded": true
      },
      {
        "id": "fact_d27cfa5bea71cc414c5b",
        "object_or_effect": "w_a6fef1ac40965694c694",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a6fef1ac40965694c694",
        "grounded": true
      },
      {
        "id": "fact_d48e18ce66f0f0b89d2a",
        "object_or_effect": "w_cd87dc6e3a6034877db3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_cd87dc6e3a6034877db3",
        "grounded": true
      },
      {
        "id": "fact_d5d14aa5503211df3963",
        "object_or_effect": "w_0f0f92aed724ec3c57fd",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0f0f92aed724ec3c57fd",
        "grounded": true
      },
      {
        "id": "fact_d706317dbf27fedf3cc8",
        "object_or_effect": "w_3b10f099518bb4b273e6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_3b10f099518bb4b273e6",
        "grounded": true
      },
      {
        "id": "fact_d852ecf1c62088ddbcf7",
        "object_or_effect": "w_14455d2b8380a0b17651",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_14455d2b8380a0b17651",
        "grounded": true
      },
      {
        "id": "fact_d95ae820a31f55d84b00",
        "object_or_effect": "w_9ec27d992131221e381d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_9ec27d992131221e381d",
        "grounded": true
      },
      {
        "id": "fact_d9eb0ce1e9ddab29d776",
        "object_or_effect": "w_b8c90df9aa7b7aace21b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b8c90df9aa7b7aace21b",
        "grounded": true
      },
      {
        "id": "fact_dc0b1cda0d06dc736dff",
        "object_or_effect": "w_8a3121202b10bd5aa8d7",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_8a3121202b10bd5aa8d7",
        "grounded": true
      },
      {
        "id": "fact_ddcd6f6de344eb8363dc",
        "object_or_effect": "w_6f86506968ff33340d6b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_6f86506968ff33340d6b",
        "grounded": true
      },
      {
        "id": "fact_df0d151c0ac558848a82",
        "object_or_effect": "w_7d18baa8e58c829082c1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_7d18baa8e58c829082c1",
        "grounded": true
      },
      {
        "id": "fact_df2c102559e88a09745f",
        "object_or_effect": "w_dfc191d0f21ac5bbc558",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_dfc191d0f21ac5bbc558",
        "grounded": true
      },
      {
        "id": "fact_e01e524e9dfcc0da8cf6",
        "object_or_effect": "w_328e89199da1b2dbef40",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_328e89199da1b2dbef40",
        "grounded": true
      },
      {
        "id": "fact_e0a85f81d13d17f81cb0",
        "object_or_effect": "w_efa30d3263289f05f410",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_efa30d3263289f05f410",
        "grounded": true
      },
      {
        "id": "fact_e2507aab51b6a0950a6e",
        "object_or_effect": "w_13dbce78f6f58a4d7b91",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_13dbce78f6f58a4d7b91",
        "grounded": true
      },
      {
        "id": "fact_e4040f15cf3fb66ec261",
        "object_or_effect": "w_df263f102fbb1eac8a1a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_df263f102fbb1eac8a1a",
        "grounded": true
      },
      {
        "id": "fact_e53f6ef046f06a480db8",
        "object_or_effect": "w_10d5d536f5920af186b6",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_10d5d536f5920af186b6",
        "grounded": true
      },
      {
        "id": "fact_e58d44e3ea214b6c52f8",
        "object_or_effect": "w_ae4135648aea2a7fa259",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_ae4135648aea2a7fa259",
        "grounded": true
      },
      {
        "id": "fact_e8eba76e81326e7d597a",
        "object_or_effect": "w_a093992ea9c7b45d8c5a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a093992ea9c7b45d8c5a",
        "grounded": true
      },
      {
        "id": "fact_e928dafbc84a8aca70e3",
        "object_or_effect": "w_68491a32f8897f733105",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_68491a32f8897f733105",
        "grounded": true
      },
      {
        "id": "fact_e9bef2291e96d4f1a2ee",
        "object_or_effect": "w_3c997dab9c2762b6daba",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_3c997dab9c2762b6daba",
        "grounded": true
      },
      {
        "id": "fact_ea308ada419f79b3490f",
        "object_or_effect": "w_4d0d04c09d592909754e",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4d0d04c09d592909754e",
        "grounded": true
      },
      {
        "id": "fact_eaf934cc9b16e8baa481",
        "object_or_effect": "w_92ea09179eb77887ba2a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_92ea09179eb77887ba2a",
        "grounded": true
      },
      {
        "id": "fact_eeed16e8e320a8cd2bc7",
        "object_or_effect": "w_189cb9df31cba837549d",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_189cb9df31cba837549d",
        "grounded": true
      },
      {
        "id": "fact_f0ab62757f2cb0de64a5",
        "object_or_effect": "w_057047318bf46228bd4f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_057047318bf46228bd4f",
        "grounded": true
      },
      {
        "id": "fact_f0da85d468259d55e815",
        "object_or_effect": "w_e5f7bb72353c2aafc482",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_e5f7bb72353c2aafc482",
        "grounded": true
      },
      {
        "id": "fact_f161b66ae8b6ad7bd450",
        "object_or_effect": "w_92c03784ec0864458e47",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_92c03784ec0864458e47",
        "grounded": true
      },
      {
        "id": "fact_f182c6a5470310ac708e",
        "object_or_effect": "w_a1ffbdbd1f9ee212e09b",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_a1ffbdbd1f9ee212e09b",
        "grounded": true
      },
      {
        "id": "fact_f1995f5847743337ed69",
        "object_or_effect": "w_3c3915612972be0457e3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_3c3915612972be0457e3",
        "grounded": true
      },
      {
        "id": "fact_f28ffd4cff6744dcf8af",
        "object_or_effect": "w_0c4d46cf56d65cb4bdf0",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_0c4d46cf56d65cb4bdf0",
        "grounded": true
      },
      {
        "id": "fact_f2c01d8b10c5f21aee28",
        "object_or_effect": "w_f09b50c472060871dc42",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_f09b50c472060871dc42",
        "grounded": true
      },
      {
        "id": "fact_f3f19ea0848eee3049b2",
        "object_or_effect": "w_37de1d51a6e94817f841",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_37de1d51a6e94817f841",
        "grounded": true
      },
      {
        "id": "fact_f471995b23204a1a10cf",
        "object_or_effect": "w_d5cc3322cc357428afe1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d5cc3322cc357428afe1",
        "grounded": true
      },
      {
        "id": "fact_f4d940c010114992514d",
        "object_or_effect": "w_ce1b694d5a85fe32a550",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_ce1b694d5a85fe32a550",
        "grounded": true
      },
      {
        "id": "fact_f544a043e9354dbc0770",
        "object_or_effect": "w_46ba44877f979fcc36db",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_46ba44877f979fcc36db",
        "grounded": true
      },
      {
        "id": "fact_f5f6a9b0a81b90069428",
        "object_or_effect": "w_740340ab4433066f9a33",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_740340ab4433066f9a33",
        "grounded": true
      },
      {
        "id": "fact_f6a57d3b77538e414411",
        "object_or_effect": "w_5f467d41a0eb508970fd",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_5f467d41a0eb508970fd",
        "grounded": true
      },
      {
        "id": "fact_f707efcc8b519be3a525",
        "object_or_effect": "w_2ced60879e95e041eece",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2ced60879e95e041eece",
        "grounded": true
      },
      {
        "id": "fact_f805422a113bde64791c",
        "object_or_effect": "w_b24cb262538e04f5db31",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b24cb262538e04f5db31",
        "grounded": true
      },
      {
        "id": "fact_f87fcca1a2dff1791e96",
        "object_or_effect": "w_64ad3c321662e684cd01",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_64ad3c321662e684cd01",
        "grounded": true
      },
      {
        "id": "fact_fabd7db785b3efde7534",
        "object_or_effect": "w_5c37c9ac526584ce9987",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_5c37c9ac526584ce9987",
        "grounded": true
      },
      {
        "id": "fact_fc6edf701e0d9ef16243",
        "object_or_effect": "w_52b6d46a794152e2c7de",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_52b6d46a794152e2c7de",
        "grounded": true
      },
      {
        "id": "fact_fd1eb8b0086c35f77d78",
        "object_or_effect": "w_62d45be22aac175dfaaa",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_62d45be22aac175dfaaa",
        "grounded": true
      },
      {
        "id": "fact_fdee19b447e3893bbc6f",
        "object_or_effect": "w_32e618424e50c5063355",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_32e618424e50c5063355",
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
        "label": "authorization_violation",
        "answer": "unsat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 1,
      "invalid_semantic_row": 2,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 3,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 6,
      "policy_missing": 3,
      "guarded_source_effect": 1
    }
  }
}
```

## RQ1_c24c6c95ccbd

证据目录 run/members/RQ1_c24c6c95ccbd/attempt_1/，报告哈希 f188ce3feb5189d6afb2a37b0571d45dd7970611624344c1cd93208a8f8414af

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
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": true,
    "paired_id": "RQ1_32dbc2fa2433",
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
      "semantic_answer_outside_sent_scope": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 48,
      "model_phase_missing": 2,
      "external_dependency": 15
    }
  }
}
```

## RQ1_c29df435681e

证据目录 run/members/RQ1_c29df435681e/attempt_1/，报告哈希 61eeec624f72e9c11726e999bab8d45c73549f7d365657fb0c75914c7c0c8e6a

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "unsupported",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "alarm",
    "FCR-FREEZE": "unsupported"
  },
  "changes": [
    "last1164 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": true,
    "paired_id": "RQ1_ffcaa562a72d",
    "state": "alarm",
    "changes": {
      "v32": {
        "before": "alarm",
        "after": "alarm"
      },
      "last1164": {
        "before": "not_detected",
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
      "normalization_diagnostics": []
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_597781abbfb2517d2348",
        "fact": "fact_644d9af359e95bd4ae27",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_d572676b8884e22ec7c0",
        "fact": "fact_e279d9f01766fee01f2a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_3641b3e3f9ac98a75d21",
        "object_or_effect": "w_f2fadaadd3b2088a73b1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f2fadaadd3b2088a73b1",
        "grounded": true
      },
      {
        "id": "fact_5cbe6d6a5e290aa3f1ce",
        "object_or_effect": "w_d0328f1e93d7f83823f3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d0328f1e93d7f83823f3",
        "grounded": true
      },
      {
        "id": "fact_644d9af359e95bd4ae27",
        "object_or_effect": "o_547e2f30d00e764e2e26",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_e279d9f01766fee01f2a",
        "object_or_effect": "o_545a8bccfcc4b9e601c4",
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
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "prefix_reachability",
        "answer": "unsat",
        "count": 2
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
      },
      {
        "label": "baseline_usable",
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
        "answer": "unsat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 32,
      "program_support": 1,
      "external_dependency": 15,
      "source_task_reading": 1,
      "source_check_excluded": 1
    }
  }
}
```

## RQ1_c75d73e1c482

证据目录 run/members/RQ1_c75d73e1c482/attempt_1/，报告哈希 c1ad7c7b43066b6c0b1ca06bde09cb4c0a18e25a7009e29dff7dadeb8dd11267

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "alarm",
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
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,invalid_semantic_row,action_slice_exhausted,unknown_assessment_vocabulary",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": true,
    "paired_id": "RQ1_35e0e8d95f92",
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
      "FCR-TRANSFER",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "143bd439b779a17f1a84ffb31a1ad53c2618ee4039934e72b8ab00deb83146cc",
          "issue": "issue_512a63b10f3c2bdbe505"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_39081668c7ac84e0d2d4",
        "fact": "fact_1852f78eb4a115079e4a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_1852f78eb4a115079e4a",
        "object_or_effect": "o_3308e4df4b409508e627",
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
        "answer": "sat",
        "count": 42
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 46
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 6
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 1
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
        "label": "financial_block",
        "answer": "unsat",
        "count": 41
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 16
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 14
      },
      {
        "label": "same_request_amount_change",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 9
      },
      {
        "label": "financial_consent_unresolved",
        "answer": "unsat",
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
      "unbound_or_inapplicable_seed": 3,
      "invalid_semantic_row": 2,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "action_slice_exhausted": 2,
      "noncached_action_limit": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 140,
      "source_task_reading": 38,
      "covered_holder_grant": 2,
      "external_dependency": 6,
      "scope_missing": 5,
      "no_debit_in_scope": 1,
      "new_entitlement": 1,
      "program_support": 2
    }
  }
}
```

## RQ1_c772c59e4a76

证据目录 run/members/RQ1_c772c59e4a76/attempt_1/，报告哈希 7e9c412af768a3a85d5f510d35b195597e2180a2d59d38771cd9fae066adc973

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
    "last1164 新增指定类命中",
    "prev200 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,action_slice_exhausted",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": true,
    "paired_id": "RQ1_a7bf9487cc3f",
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
      "FCR-MINT"
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
          "detail_sha256": "1e0bab14feaa79ae357d85ec36f8e31aabc87a1128b93b5e82e0cf97550dcc9f",
          "issue": "issue_9e6455a3e823954bf414"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "e2e8ec11d1c648dd019c293e1641a6a93f60db5bcebdf263c5f9b1054dae0ef9",
          "issue": "issue_9e6455a3e823954bf414"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a7303eb16bbfabe4c63843081bcc373164d6d94169dc657dbcd6421749058c80",
          "issue": "issue_918930a105a2d9068d00"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "1af17ccfd98726afba5a177f7e8a0dda68d4287e757494589e1f42efae0f8af1",
          "issue": "issue_8a3bb098bf4927a143dc"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "03c1f260b2c77e617458f148906c86b09da17854a6b3d425e9c4b5e9be449d58",
          "issue": "issue_8a3bb098bf4927a143dc"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "00ef56862911bc82a763f97a0ea86ca1a3c59986b9e78c4841e56b7da45730cb",
          "issue": "issue_c7e1d10b66355cd53485"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "abea6b46469a5d94468f777d6a514cc10db0a5d2ee9aa4235042338aa3a5aeed",
          "issue": "issue_c7e1d10b66355cd53485"
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
          "detail_sha256": "726e665a6907acb801d454e7661e065b3b118daa1ba5f2c1547497242ed69fb7",
          "issue": "issue_e01aaa1d669a6ce24506"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "139d92e5e642b05fa50d0d3379a6c081b649605f9dfd0917314b0cffdc4888fa",
          "issue": "issue_e01aaa1d669a6ce24506"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_2257130bc3a9d97e427e",
        "fact": "fact_46f4977c7b0bf44f6d88",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_35db395e9052d227e1a6",
        "fact": "fact_9b8a6276ca13116c6049",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_4b1cd7e237c21f86c9f9",
        "fact": "fact_f7a4acba9a0f8c404586",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_4cf55064066cb807068c",
        "fact": "fact_46f4977c7b0bf44f6d88",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_5db0e4a6b5dfae103f85",
        "fact": "fact_b75f0350acc7c7616189",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_024b1aed556b2aa593f5",
        "object_or_effect": "w_d034ec659fc4840a8f66",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_d034ec659fc4840a8f66",
        "grounded": true
      },
      {
        "id": "fact_04a57a97e97271d22393",
        "object_or_effect": "w_5360db3a159d7a4f91c4",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_5360db3a159d7a4f91c4",
        "grounded": true
      },
      {
        "id": "fact_0f2ff0d6db595038ea1a",
        "object_or_effect": "w_511c2033d66a0c743717",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_511c2033d66a0c743717",
        "grounded": true
      },
      {
        "id": "fact_3ac734c64633fb1d603c",
        "object_or_effect": "w_741a7c5ad38f879e88cc",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_741a7c5ad38f879e88cc",
        "grounded": true
      },
      {
        "id": "fact_46f4977c7b0bf44f6d88",
        "object_or_effect": "o_b23a2f2a9cb4c4c38857",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_5047c373bb4d966eda32",
        "object_or_effect": "w_1eb03cb7cf00962f0291",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_1eb03cb7cf00962f0291",
        "grounded": true
      },
      {
        "id": "fact_53519a461a54cec1ab1a",
        "object_or_effect": "w_b77c912b7d8373816eb7",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_b77c912b7d8373816eb7",
        "grounded": true
      },
      {
        "id": "fact_9b8a6276ca13116c6049",
        "object_or_effect": "o_6339c562204fe8d09e89",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_9dfee1e6a948a7231a30",
        "object_or_effect": "w_5560d793c1a1d3840930",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5560d793c1a1d3840930",
        "grounded": true
      },
      {
        "id": "fact_a928b98342841cc620ae",
        "object_or_effect": "w_eb2251d24f3e12a37989",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_eb2251d24f3e12a37989",
        "grounded": true
      },
      {
        "id": "fact_b75f0350acc7c7616189",
        "object_or_effect": "o_e51c7ca8af0ed9176df0",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_bafa73514df6bffa8c24",
        "object_or_effect": "w_0f28b1e473f9017c6fdf",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_0f28b1e473f9017c6fdf",
        "grounded": true
      },
      {
        "id": "fact_c896d3c789e120188617",
        "object_or_effect": "w_a571e54ab4587e54ee2c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a571e54ab4587e54ee2c",
        "grounded": true
      },
      {
        "id": "fact_c999bc15b0813b104e90",
        "object_or_effect": "w_90cf5a6dcec89525c9dc",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_90cf5a6dcec89525c9dc",
        "grounded": true
      },
      {
        "id": "fact_f7a4acba9a0f8c404586",
        "object_or_effect": "o_c932f2ff88e6ba55b85a",
        "meaning": "eligibility_state",
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
        "count": 5
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 4
      },
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 20
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 29
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 20
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 18
      },
      {
        "label": "financial_consent_unresolved",
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
        "count": 1
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "same_request_amount_change",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 6,
      "category_ambiguous_or_outside_supported_task": 4,
      "unknown_assessment_vocabulary": 5,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 3,
      "action_slice_exhausted": 4,
      "program_encoding_budget_exhausted": 1,
      "noncached_action_limit": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "scope_missing": 6,
      "no_effect_in_scope": 125,
      "source_task_reading": 34,
      "covered_holder_grant": 4,
      "no_debit_in_scope": 2,
      "new_entitlement": 1,
      "external_dependency": 7,
      "program_support": 1
    }
  }
}
```

## RQ1_c80f7a639e42

证据目录 run/members/RQ1_c80f7a639e42/attempt_1/，报告哈希 41b588396e8ee33ab75afe8374177ed632a116b54d0dd7a0b3fa3429b558aa2f

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "alarm",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "unsupported",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "decision_only 风险版漏检"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope,shared_declaration_in_distinct_applied_contexts",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": true,
    "paired_id": "RQ1_30177d564271",
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
      "FCR-MINT"
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
          "detail_sha256": "b8fb9117f814302785a4253ceff0d147433df8bf44b4dbbe808eb6e7d56f125f",
          "issue": "issue_24d4225f63a9bc013188"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "8d6bce60d654cfee1b6583cb870a8d9a1bd5444fc177ae882f041c3f3a6c6fa4",
          "issue": "issue_487ca6791ea3d8c1d6e8"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_1c2633a836f59e8fa37c",
        "fact": "fact_cf9a0092d367e387a1e8",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_cf9a0092d367e387a1e8",
        "object_or_effect": "o_1406d0993f09ee4a97f2",
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
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 10
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 10
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 8
      },
      {
        "label": "financial_consent_unresolved",
        "answer": "unsat",
        "count": 2
      },
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
      "unbound_or_inapplicable_seed": 4,
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 1,
      "shared_declaration_in_distinct_applied_contexts": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 126,
      "source_task_reading": 29,
      "scope_missing": 5,
      "program_support": 1,
      "external_dependency": 6,
      "parameter_only": 1,
      "covered_holder_grant": 2
    }
  }
}
```

## RQ1_c9626779c857

证据目录 run/members/RQ1_c9626779c857/attempt_1/，报告哈希 52f33e560c56a2703c3dcfe8c89edc99e68d089b51187c76800fa4e06a8a73f5

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "unsupported",
    "FCR-MINT": "unsupported",
    "FCR-DESTROY": "alarm",
    "FCR-PAUSE": "unsupported",
    "FCR-FREEZE": "alarm"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,no_locatable_source,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": true,
    "paired_id": "RQ1_085aaca2f412",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "aa49ec3f0aedd2899f6ec68577d9a204184342aca6e0580276ff9f6ad2ca7585",
          "issue": "issue_d4ad0939fe6e6190ded5"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ae9de96a5fc55a7cf20a9dbeb3062024e0f8a43d545d1137e07a1d13227142f1",
          "issue": "issue_4cdb9a28352668f82f02"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "90c33faaecec91cb0572e0135be0b956af3c600b0b6d97c6403bfaa2bd6194e5",
          "issue": "issue_bf15a675d81d7b20a1c6"
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
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 2
      },
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
      "invalid_semantic_row": 6,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 1,
      "no_locatable_source": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 117,
      "program_support": 2,
      "source_task_reading": 5,
      "source_check_excluded": 1,
      "external_dependency": 10
    }
  }
}
```
