# 逐例审阅

## RQ1_c9a2d9b618a7

证据目录 run/members/RQ1_c9a2d9b618a7/attempt_1/，报告哈希 2c9a69cbd88a83ff63f46c54470cb3379679d056c68db18deea130d05e64fda2

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:93:author:1",
    "last1164 丢失根因 D2:93:author:1",
    "prev200 丢失根因 D2:93:author:1",
    "decision_only 丢失根因 D2:93:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,invalid_semantic_row,semantic_answer_outside_sent_scope,category_ambiguous_or_outside_supported_task",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_c9a2d9b618a7",
        "reference": "D2:93:author:1",
        "function": "FirstBloodToken",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_7eaf4d7b9db420c51abb"
        ],
        "decision_only_findings": [
          "finding_503409a2a41dcf6060eb"
        ],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:93:author:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:93:author:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:93:author:1"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:93:author:1"
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "23a6538a9ed5b2f61822e0e7b5063a3598a192d13fc88c7a9ac1328ad4db6f82"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "3e7fa87176cfe502a18032a71e51c370af5daba9e41823bd3e38d457c96859ac"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "640696f8c31a46ef4008c1bdf3ee5462c600219d346fb6124f9cc672390e80c5",
          "issue": "issue_1bccabbcdfc4e6ebf8d8"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "911964605f585c9591f272bb796449144323cebcdae27e4a1271aa82747b9892",
          "issue": "issue_1bccabbcdfc4e6ebf8d8"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "2d9de34b651044ccce55c8dfe68c1b693ae48919feec69add90e5c097f30203e",
          "issue": "issue_eae6b1c61495995fe3c3"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1ca889cdf90bd5abfb3b34e08d0bd061b36cd2d179fa9f23db4f9ec07e44d874",
          "issue": "issue_eae6b1c61495995fe3c3"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "8ad5ff16c17a9b18c6882bcbfb5a656e6b874a81e7426757da8b38d3e346be1e",
          "issue": "issue_e4e6b9ee7e4b36420c18"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "a3c0ff116d3905396c67ee30475fffa7286ccac01a61cb69a5e40442f884b65d",
          "issue": "issue_e4e6b9ee7e4b36420c18"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "79adeba3e109248d14baf7eef16ab62850ec030d425057424795c2f009fccd8e",
          "issue": "issue_4c55422ceb4fd259b2bf"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "5171e82bbdcaf02458b36e3de7a664b0bb5103fbc98523e99a1961eb46c59a61",
          "issue": "issue_4c55422ceb4fd259b2bf"
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
          "detail_sha256": "463e59323616d457beb3d7f4386be080c074091a12b7f44d85eb14dbb2bdc8fe",
          "issue": "issue_11d0ccb636e7c4c7a078"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ac8494b00defc88e54f4a60de4fee6ea93d5da78ef4c72234f796ea9fca4c268",
          "issue": "issue_11d0ccb636e7c4c7a078"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "a450b611b985d1568d2829c1258ad0d6bcc7b252c9244f6255333532f74b464e",
          "issue": "issue_f8c642f6797b6a5c2075"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "16f066dd84d6fd1191ce28be6f988de7bf1410fe09e8250dfdb3fbe7fb7d41a9",
          "issue": "issue_f8c642f6797b6a5c2075"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "3cdad311bc7555f2c801e64779642822732382c6f7b5522ae79d15184785f6a9",
          "issue": "issue_3ff91f281464a017f8d9"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "47212c126234e4681d765cc1a1996b338e21d2eb075c5c1914ba76082e727aa0",
          "issue": "issue_3ff91f281464a017f8d9"
        }
      ]
    }
  ],
  "FP_review": {
    "disappeared": [
      1530
    ],
    "new": [],
    "disappeared_to_unknown": true,
    "warning": "位置用于导航；同位置仍需根因判断。消失至unknown不算有效误报纠正。"
  },
  "mechanism": {
    "supports": [
      {
        "support": "support_85b6f9d0f79630fbfad0",
        "fact": "fact_be6b99f619f4d7c654cc",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_9bd44807adeeb7e74067",
        "fact": "fact_424b5ec4eebf6ac67573",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_b2e92eb5bcf37eb2d994",
        "fact": "fact_a6363271ba5cda1e2309",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_f8a3ed0bb6c7f718c26e",
        "fact": "fact_5c58c05b4025be1667c7",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_00bdebf9159937bae2dc",
        "object_or_effect": "w_d6b75f820771dd051e85",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_d6b75f820771dd051e85",
        "grounded": true
      },
      {
        "id": "fact_00edd4d98ccdd16ba45a",
        "object_or_effect": "w_3c070c8dc98e14e6f4b1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_3c070c8dc98e14e6f4b1",
        "grounded": true
      },
      {
        "id": "fact_0c834c5297ea406bd0ad",
        "object_or_effect": "w_4e2669109ca626cb2013",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_4e2669109ca626cb2013",
        "grounded": true
      },
      {
        "id": "fact_13db91c8429e28b91525",
        "object_or_effect": "w_79b0be99e02cfda27cee",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_79b0be99e02cfda27cee",
        "grounded": true
      },
      {
        "id": "fact_1f1f0714952b51d3fab9",
        "object_or_effect": "w_3bde77db9ecd6b3fcb30",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_3bde77db9ecd6b3fcb30",
        "grounded": true
      },
      {
        "id": "fact_2773a723afada6ab40d4",
        "object_or_effect": "w_eb2c11f494326cab9fa9",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_eb2c11f494326cab9fa9",
        "grounded": true
      },
      {
        "id": "fact_288c9fd13dfb58587210",
        "object_or_effect": "w_5e090337eb169899f4e7",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_5e090337eb169899f4e7",
        "grounded": true
      },
      {
        "id": "fact_32d901da5222bafe6559",
        "object_or_effect": "w_42119a372b2b85775e95",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_42119a372b2b85775e95",
        "grounded": true
      },
      {
        "id": "fact_403f2a4aaad169d5637d",
        "object_or_effect": "w_c9b9ca1efcf982e068ab",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_c9b9ca1efcf982e068ab",
        "grounded": true
      },
      {
        "id": "fact_424b5ec4eebf6ac67573",
        "object_or_effect": "o_157a5b41ac0b8c9fa194",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_5659e8e498c1e6c49192",
        "object_or_effect": "w_574b1e387659de42f4c8",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_574b1e387659de42f4c8",
        "grounded": true
      },
      {
        "id": "fact_5c58c05b4025be1667c7",
        "object_or_effect": "o_92e0ee70e3d7e7dc2f8f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_734bf504f69dfa5e9c81",
        "object_or_effect": "w_61170669140bb15becfe",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_61170669140bb15becfe",
        "grounded": true
      },
      {
        "id": "fact_8feec45882bbade55ff7",
        "object_or_effect": "w_ff6e279e69acd2abcd27",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_ff6e279e69acd2abcd27",
        "grounded": true
      },
      {
        "id": "fact_a6363271ba5cda1e2309",
        "object_or_effect": "o_2b5a857d6ed301b50cd3",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_acd1fabb61b3909b5075",
        "object_or_effect": "w_4ef726cbc09b7169687c",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4ef726cbc09b7169687c",
        "grounded": true
      },
      {
        "id": "fact_be6b99f619f4d7c654cc",
        "object_or_effect": "o_1d5b2a1788fb5aeb3c83",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_c25cda01659b1956b541",
        "object_or_effect": "w_b60c21a17ebac739ee29",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_b60c21a17ebac739ee29",
        "grounded": true
      },
      {
        "id": "fact_c67e0eae533821cb2d63",
        "object_or_effect": "w_4a8d8dbc2ac2676b2dfe",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_4a8d8dbc2ac2676b2dfe",
        "grounded": true
      },
      {
        "id": "fact_d23c63595843d3716a03",
        "object_or_effect": "w_cc3a36a736cc2b19256a",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_cc3a36a736cc2b19256a",
        "grounded": true
      },
      {
        "id": "fact_dbc08aaee037011893bd",
        "object_or_effect": "w_57fb562ab04b3c8724c1",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_57fb562ab04b3c8724c1",
        "grounded": true
      },
      {
        "id": "fact_e5c4a25c781106ccaacc",
        "object_or_effect": "w_78fe2f9a256ef41105c3",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_78fe2f9a256ef41105c3",
        "grounded": true
      },
      {
        "id": "fact_e94c17fb53a87c6c9d58",
        "object_or_effect": "w_54286cc554f593cd20ff",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_54286cc554f593cd20ff",
        "grounded": true
      },
      {
        "id": "fact_ed349bd4cd8d8e98aed8",
        "object_or_effect": "w_2dbc0f8276f847d8770f",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2dbc0f8276f847d8770f",
        "grounded": true
      },
      {
        "id": "fact_ff67335f20762e40192b",
        "object_or_effect": "w_19a9a963b50d92837823",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_19a9a963b50d92837823",
        "grounded": true
      }
    ],
    "query_summary": [
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 22
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 16
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 22
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 2
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 11,
      "category_ambiguous_or_outside_supported_task": 7,
      "unknown_assessment_vocabulary": 7,
      "semantic_answer_outside_sent_scope": 10,
      "no_locatable_source": 7,
      "unbound_or_inapplicable_seed": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 14
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 34,
      "source_task_reading": 2,
      "policy_missing": 10,
      "external_dependency": 2
    }
  }
}
```

## RQ1_cb8c3fafbda1

证据目录 run/members/RQ1_cb8c3fafbda1/attempt_1/，报告哈希 1169c6cfebf176a689a58d85cd7338ccfc52e4cee12fe0317de2f56f6aea8d17

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
    "已确认消费/覆盖诊断 invalid_semantic_row,action_slice_exhausted,unknown_assessment_vocabulary,program_investigation_seconds",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-MINT",
    "positive": true,
    "paired_id": "RQ1_7bfd58ffb1ae",
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
          "detail_sha256": "9a930c630ededdf6b66435f82b533dd6abb2cb9f2d229cf4a5aece150cd02c54",
          "issue": "issue_cc5b7ae3a9e473541de2"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f16597a5faf0fb22e95bded8e8708ebb7ff7622a7964bbb81ad188a15b15e555",
          "issue": "issue_66ee1201d866c2e821ba"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "9b49a1c35274dc4e4d20b183ac605e10809447e6af8cc5a9bf17e00cb314a1f4",
          "issue": "issue_30723afa7a68b2f3a2a6"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "857b9b0de86de95f502f951f5266a9923c7d62eef4df8003da0fa68c40491a3a",
          "issue": "issue_30723afa7a68b2f3a2a6"
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
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 15
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 15
      },
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 11
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 36
      },
      {
        "label": "financial_block",
        "answer": "unsat",
        "count": 19
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 21
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 12
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "financial_consent_unresolved",
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
      "invalid_semantic_row": 5,
      "unknown_assessment_vocabulary": 3,
      "category_ambiguous_or_outside_supported_task": 1,
      "semantic_answer_outside_sent_scope": 1,
      "action_slice_exhausted": 5,
      "program_investigation_budget_exhausted": 1,
      "program_investigation_seconds": 2
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
      "source_task_reading": 39,
      "no_debit_in_scope": 1,
      "new_entitlement": 1,
      "program_support": 2,
      "external_dependency": 6
    }
  }
}
```

## RQ1_cd39ae0d15a5

证据目录 run/members/RQ1_cd39ae0d15a5/attempt_1/，报告哈希 99f080a68a393f5448240a408cbfe74daad12d1556edc1b3ec5588d8c5cdd152

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
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": true,
    "paired_id": "RQ1_b649070a92c3",
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
      "no_effect_in_scope": 109,
      "model_phase_missing": 16
    }
  }
}
```

## RQ1_cd47d22b26a9

证据目录 run/members/RQ1_cd47d22b26a9/attempt_1/，报告哈希 ac413270210bdfd759f40e59c29c9910156e90f7f29493f7ea4432116fdb49d5

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
    "已确认消费/覆盖诊断 invalid_semantic_row,action_slice_exhausted,unknown_assessment_vocabulary,program_investigation_seconds",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-FREEZE",
    "positive": true,
    "paired_id": "RQ1_fa2207747d01",
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
          "detail_sha256": "1f681b6588345d454d714c3400b5b19df4d7c8866c6875e619316b1383827cbe",
          "issue": "issue_fedf2ac2cc4ba5e2bd40"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "e7c4b5162b6a88791857a6571be03403e953bbb313a6bcdec0f2f81baf54dc6f",
          "issue": "issue_4f4093aad434b8a1231b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "06e5761da1571037ddf3a5172a1fcf61fb1a8d012c9b42270e250a3584b044c1",
          "issue": "issue_4f4093aad434b8a1231b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "531fc1074245f7a92636bccf4d87a67b99580f3b6092b183fe1687b3fc570c4f",
          "issue": "issue_8a5d55a7c1b62bd205d5"
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "cb9c903ead13b1473ba98cff14431958b10a241cf3c99f74e207a38babe338c5",
          "issue": "issue_4f4093aad434b8a1231b"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "771fa30ad879793dda7e3a0e0ef487e945c9f0add94924f2770026d68f42fe8a",
          "issue": "issue_4f4093aad434b8a1231b"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [],
    "facts": [],
    "query_summary": [
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "control_transition_preservation",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 12
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 12
      },
      {
        "label": "financial_block",
        "answer": "unknown",
        "count": 31
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 9,
      "unknown_assessment_vocabulary": 4,
      "category_ambiguous_or_outside_supported_task": 2,
      "semantic_answer_outside_sent_scope": 1,
      "action_slice_exhausted": 5,
      "program_investigation_budget_exhausted": 1,
      "program_investigation_seconds": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "scope_missing": 9,
      "no_effect_in_scope": 120,
      "source_task_reading": 29,
      "no_debit_in_scope": 2,
      "new_entitlement": 1,
      "covered_holder_grant": 2,
      "external_dependency": 6,
      "program_support": 1
    }
  }
}
```

## RQ1_cda3df36df22

证据目录 run/members/RQ1_cda3df36df22/attempt_1/，报告哈希 f757a8179e7b4efbd3398b19bc3351cf429cce83ef557491b67fbb2eecc91fdf

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "not_detected",
    "FCR-MINT": "unsupported",
    "FCR-DESTROY": "unsupported",
    "FCR-PAUSE": "alarm",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": true,
    "paired_id": "RQ1_35f857af5c9e",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "c88528d7fe5cd09271c3f4718696f92f8bb42921eb298c3fd25113da1bf6cbbe",
          "issue": "issue_c533be28c2eeac68f8f4"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "783be0bfad612e093c1aae83e67d21f1db41b27d5bb0a74e8db6db0c29549807",
          "issue": "issue_c533be28c2eeac68f8f4"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "ea630cce5409a49d8a0f6347f00a5cf90580d20df27c9c0f999390a1ed85e075",
          "issue": "issue_cd8a59ad24bbafd08b09"
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
          "detail_sha256": "c88528d7fe5cd09271c3f4718696f92f8bb42921eb298c3fd25113da1bf6cbbe",
          "issue": "issue_c533be28c2eeac68f8f4"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "0b426e5720923d0ed69114199716da7d8f624f95b43dba35199900116a6e5096",
          "issue": "issue_c533be28c2eeac68f8f4"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_a1eaad3920976b8b7084",
        "fact": "fact_51c4f9dfae166e612069",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_51c4f9dfae166e612069",
        "object_or_effect": "o_04be86c3ee13db6b79fe",
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
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "financial_block",
        "answer": "sat",
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
        "label": "control_transition_preservation",
        "answer": "unsat",
        "count": 2
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 7,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 3,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 1,
      "invalid_semantic_row": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE",
      "FCR-TRANSFER"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 54,
      "program_support": 1,
      "source_task_reading": 11,
      "covered_holder_grant": 1,
      "scope_missing": 3
    }
  }
}
```

## RQ1_ce214e96568d

证据目录 run/members/RQ1_ce214e96568d/attempt_1/，报告哈希 562b2d57ce1d4dcd43bb3b8f273aa7d80a60fee427f6709af4c3485038dcb33d

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:157:author:1",
    "last1164 丢失根因 D2:157:author:1",
    "prev200 丢失根因 D2:157:author:1",
    "decision_only 丢失根因 D2:157:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope,invalid_semantic_row",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_ce214e96568d",
        "reference": "D2:157:author:1",
        "function": "Constructor",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "TP",
        "decision_only": "TP",
        "prev200_findings": [
          "finding_754e8da8667b4fe513fb",
          "finding_121477e90165e4402cbe",
          "finding_28c4c85a7b2c2c6b1a96"
        ],
        "decision_only_findings": [
          "finding_dda6bc704eee09289988"
        ],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:157:author:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:157:author:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": [
          "D2:157:author:1"
        ]
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:157:author:1"
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
        "support": "support_b3cf64b1c6f225eaa18d",
        "fact": "fact_9ae1363c1088acca8f78",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_9ae1363c1088acca8f78",
        "object_or_effect": "o_60c031bd9deec4a8344d",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 5,
      "invalid_semantic_row": 1,
      "semantic_answer_outside_sent_scope": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "unassessed_role_change": 9,
      "no_effect_in_scope": 21,
      "source_task_reading": 11,
      "external_dependency": 2
    }
  }
}
```

## RQ1_cea156e41c29

证据目录 run/members/RQ1_cea156e41c29/attempt_1/，报告哈希 3eab6cc5d6b8d7bde322df0a0a8b9d96f3f1533c9ba8ce61146906b5eb3c72c3

```json
{
  "task": "FCR",
  "prediction": {
    "FCR-TRANSFER": "not_detected",
    "FCR-MINT": "not_detected",
    "FCR-DESTROY": "not_detected",
    "FCR-PAUSE": "alarm",
    "FCR-FREEZE": "not_detected"
  },
  "changes": [
    "last1164 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": true,
    "paired_id": "RQ1_d695cf0bad2e",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "9cdf9e9262fd16f69773346d46060ad13c84ea5d6725ea044c57b0fb58ed66ae",
          "issue": "issue_b818ef91094ddfa9fcfe"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "e9d35f2892df6f202f076b83d36c96dde3a1849caba0b857b5248aa8b4477d76",
          "issue": "issue_b818ef91094ddfa9fcfe"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_700e05db5a13f8d9129c",
        "fact": "fact_d6c4544ed01b78dd5d65",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_7d5e7a58ad16279869ae",
        "fact": "fact_990e2119e00113c089b1",
        "origin": "verified_service",
        "field": "policies",
        "version": 1
      },
      {
        "support": "support_fb6818f8b6a00c595855",
        "fact": "fact_9bd852b5da306115af31",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_08a990573a71b2f30d67",
        "object_or_effect": "w_f5dd6031228f5c9b3a53",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_f5dd6031228f5c9b3a53",
        "grounded": true
      },
      {
        "id": "fact_6eae917dee306bdf22f9",
        "object_or_effect": "w_b3bd5c8f0df4b0888b09",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b3bd5c8f0df4b0888b09",
        "grounded": true
      },
      {
        "id": "fact_990e2119e00113c089b1",
        "object_or_effect": "w_8ae31ab65587c5a41a68",
        "meaning": "current_authority_required",
        "role": null,
        "subject": "o_e931f729cb4b45ab338a",
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_9bd852b5da306115af31",
        "object_or_effect": "o_65224a4fdd97a6cbb447",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_d6c4544ed01b78dd5d65",
        "object_or_effect": "o_05b71e2b9bbc5c97d1aa",
        "meaning": "eligibility_state",
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
        "count": 2
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
        "count": 2
      },
      {
        "label": "financial_block",
        "answer": "sat",
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
        "count": 1
      },
      {
        "label": "both_usable",
        "answer": "unsat",
        "count": 1
      }
    ],
    "diagnostics": {
      "category_ambiguous_or_outside_supported_task": 1,
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
      "no_effect_in_scope": 47,
      "program_support": 1,
      "source_task_reading": 1,
      "source_check_excluded": 1
    }
  }
}
```

## RQ1_cf32aac41cf2

证据目录 run/members/RQ1_cf32aac41cf2/attempt_1/，报告哈希 1b5588a6e937193f7a90cb6236dc85d53631d466d697edac7328424a88e9c05a

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope,no_locatable_source",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": true,
    "paired_id": "RQ1_a4c5ecc3c29e",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "cd31b9f8f69fddf59cf2fc4880ebbff8fa5f34f7fca3c1530ac4a3eb144c3142",
          "issue": "issue_7f26e03406d4148fc4b1"
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
          "detail_sha256": "3cb6cbc29e00a39f209ac30f28d62cd839dff597fe59c8fce1056ce53725c157",
          "issue": "issue_f73a1c539131a9bced62"
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
      "unknown_assessment_vocabulary": 2,
      "semantic_answer_outside_sent_scope": 2,
      "no_locatable_source": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 24,
      "model_phase_missing": 1,
      "external_dependency": 5
    }
  }
}
```

## RQ1_cfe97b8f7250

证据目录 run/members/RQ1_cfe97b8f7250/attempt_1/，报告哈希 d315ec500b531ba33b63d1ea7a471fbb6c703962ce1ef19ccf8e30dd5b6a30ca

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_cfe97b8f7250",
        "reference": "D2:43:author:1",
        "function": "bioLock",
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
        "support": "support_83888e2a0a0d33aeb607",
        "fact": "fact_8d5adb689b29c603ef41",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_8d5adb689b29c603ef41",
        "object_or_effect": "o_53a684244748ecd961d4",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "semantic_answer_outside_sent_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 65,
      "source_task_reading": 69,
      "external_dependency": 29
    }
  }
}
```

## RQ1_d4aefd2e1bfc

证据目录 run/members/RQ1_d4aefd2e1bfc/attempt_1/，报告哈希 d5d8e7f6642a78c5dfbb733ec0b278965d2f39a5d4f41356ae443ac57df78699

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope,category_ambiguous_or_outside_supported_task",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_d4aefd2e1bfc",
        "reference": "D2:522:author:1",
        "function": "refundOwner",
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
      "normalization_diagnostics": [
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "b138589739c8a259ec867fffaa91eb4ecde7dfd240acf324021b9c3a4f5a42d2",
          "issue": "issue_a85dd81b3f23aab7a7c3"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "1c8946b0da450ad8ce475665bbb94d3241447993202b8992449590d099b3384f",
          "issue": "issue_3be240341eac5bfb5730"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "36cdc7cc569fee665ef781ffbc2ce64f212962497c6b8dfdd3d733afac14c84b",
          "issue": "issue_3be240341eac5bfb5730"
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
          "detail_sha256": "0ae78b45fbd59c3d6fc0976d76894a0b20d5d3090a6001649065b6a684c25296",
          "issue": "issue_eba46045bdad11e8014c"
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
        "support": "support_fa08605f801daa8dfb21",
        "fact": "fact_479767f6bb0d7a4bcbe7",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_479767f6bb0d7a4bcbe7",
        "object_or_effect": "o_1408cf2cddc592661f7c",
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
        "count": 5
      },
      {
        "label": "callback_influence",
        "answer": "unsat",
        "count": 5
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
      "unbound_or_inapplicable_seed": 4,
      "unknown_assessment_vocabulary": 2,
      "category_ambiguous_or_outside_supported_task": 1,
      "semantic_answer_outside_sent_scope": 2,
      "unrelated_or_secondary_graph_pairs_deferred": 1,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "policy_missing": 1,
      "external_dependency": 1,
      "no_effect_in_scope": 5,
      "source_task_reading": 2
    }
  }
}
```
