# 逐例审阅

## RQ1_4c2921d39474

证据目录 run/members/RQ1_4c2921d39474/attempt_1/，报告哈希 335e50749c5ad4c27c25e6e85ef58823d117bc65715a98485290588756656fbd

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [
    "v32 丢失根因 D2:535:author:1",
    "last1164 丢失根因 D2:535:author:1",
    "decision_only 丢失根因 D2:535:author:1"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unbound_or_inapplicable_seed,semantic_answer_outside_sent_scope",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_4c2921d39474",
        "reference": "D2:535:author:1",
        "function": "init",
        "v32": "TP",
        "last1164": "TP",
        "b5": "TP",
        "ACTaint_DeepSeek": "TP",
        "prev200": "FN",
        "decision_only": "TP",
        "prev200_findings": [],
        "decision_only_findings": [
          "finding_b1c4036b131b8a855004"
        ],
        "current": "FN"
      }
    ],
    "findings": [],
    "changes": {
      "v32": {
        "gained": [],
        "lost": [
          "D2:535:author:1"
        ]
      },
      "last1164": {
        "gained": [],
        "lost": [
          "D2:535:author:1"
        ]
      },
      "prev200": {
        "gained": [],
        "lost": []
      },
      "decision_only": {
        "gained": [],
        "lost": [
          "D2:535:author:1"
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
        "support": "support_1250d3be13b4034fa9f4",
        "fact": "fact_cf77aae411d6ce625483",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_c9eb70d1b10abda872f4",
        "fact": "fact_858235051a554a3328a9",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_f86b27497c6aa7118ce3",
        "fact": "fact_a8a9af558334901e209d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_858235051a554a3328a9",
        "object_or_effect": "o_9a220c5489f0de660de7",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_a8a9af558334901e209d",
        "object_or_effect": "o_f1d0639fd4a532520233",
        "meaning": "nonfinancial_counter",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_cf77aae411d6ce625483",
        "object_or_effect": "o_72e2e13063b438e9461f",
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
      "semantic_answer_outside_sent_scope": 2,
      "invalid_semantic_row": 3
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "source_task_reading": 18,
      "no_effect_in_scope": 9,
      "unassessed_role_change": 5
    }
  }
}
```

## RQ1_4d2acebaa2ff

证据目录 run/members/RQ1_4d2acebaa2ff/attempt_1/，报告哈希 2633f71b93716c1f7c3febd1781208e8c96fcf38246903d102df3717b204597e

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
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,unknown_assessment_vocabulary,no_locatable_source,unbound_or_inapplicable_seed",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": true,
    "paired_id": "RQ1_7a54127ed44c",
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "b78a0807bf1ed9b26ad8edc4fcccab1fb9ba5aad17a6d13aa23dedf303ec267f",
          "issue": "issue_5a8424603a56e7d262df"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "1e2bdfd7668a3cc2837540771eef6442252aab95ae1608d4cf4771cff0540d26",
          "issue": "issue_5a8424603a56e7d262df"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "3fc6de71dbc2f51b6b96955316a47a41f575254e9f1d149d40a45ea8745c71e6",
          "issue": "issue_d03a88cc256d9c88ad15"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "35b199f7028e9d33af48cbaea0dad2727073dce2b22bb7e306498d50971acc8e",
          "issue": "issue_d03a88cc256d9c88ad15"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "80a9a7fd5623b1de50bc75131708690d684ccb6370a0b9f56cf0b46459ca89e1",
          "issue": "issue_3fa1e95a4c6af5f351a2"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c5dd2765efebc50b3eaf29b00a9fb613c78d3e9c2838058f5e7005360bef6d82",
          "issue": "issue_7c8f40eac38891c0fbe0"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "18fafde39f8570ea86925b87c4753bdd67760bc49c3b0cb28043e7c30ad1cd97",
          "issue": "issue_90d85f71b89368fd0534"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "79f86c1a29cce53ed5118c0a3e413a6af4a1a36a2c4ea130a3e1594678e137cb",
          "issue": "issue_90d85f71b89368fd0534"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "7e51d8f5a66632a6d3d77245b29da482c589120a8ebee964e5e7a834fbccbd65",
          "issue": "issue_69e609101a6f57789d0d"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "0bca6191b3d999e4e198f80866300e2a32cfd7184b493690e0e931b581fec71a",
          "issue": "issue_69e609101a6f57789d0d"
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
          "detail_sha256": "cb7f026592cc78d9182faeaedaedfa991fcbfb1fa567ecfea3c515d92249e310",
          "issue": "issue_f3ab74b49677220e4d92"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_08bad7453e2a22d5c98b",
        "fact": "fact_e651b8ad489ce1199974",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_40310a4327cc02522c83",
        "fact": "fact_c26176bbbcf3bc72221a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_99066e2f5bd591883cca",
        "fact": "fact_8342a0b6a83250b53f3d",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_a52e9ff7cc523bafff50",
        "fact": "fact_16642426098e6a3a72b2",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_a8d596ea97418a051420",
        "fact": "fact_1d9b29b8102e2e1bb48a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_b9161438bee807af9f7c",
        "fact": "fact_16642426098e6a3a72b2",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_bd34989748994c83cd09",
        "fact": "fact_c26176bbbcf3bc72221a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_c24de0d7b64ba316c839",
        "fact": "fact_1d9b29b8102e2e1bb48a",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_e0f484a63439610eac38",
        "fact": "fact_fac568a2e39f6e2f6693",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_07f8a41c951246b0c800",
        "object_or_effect": "w_c9a6639e83616330938c",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c9a6639e83616330938c",
        "grounded": true
      },
      {
        "id": "fact_16642426098e6a3a72b2",
        "object_or_effect": "o_2a40541358bcd1d0a77b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_1ada48e203520864095b",
        "object_or_effect": "w_438caf8e3becc694623f",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_438caf8e3becc694623f",
        "grounded": true
      },
      {
        "id": "fact_1d9b29b8102e2e1bb48a",
        "object_or_effect": "o_5131df8b91340f4d4f9b",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_1f23e9c7f15de4f22584",
        "object_or_effect": "w_76a24ac8c07ee80e068d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_76a24ac8c07ee80e068d",
        "grounded": true
      },
      {
        "id": "fact_207e78fe75a04a3b0473",
        "object_or_effect": "w_330a0c84abd59c737885",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_330a0c84abd59c737885",
        "grounded": true
      },
      {
        "id": "fact_259393140b141bfc8a29",
        "object_or_effect": "w_2a7da4eeba8adcd4ebda",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2a7da4eeba8adcd4ebda",
        "grounded": true
      },
      {
        "id": "fact_2e691c19c01816ff07bc",
        "object_or_effect": "w_181db23a48d8730ef7c4",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_181db23a48d8730ef7c4",
        "grounded": true
      },
      {
        "id": "fact_34cb3b796073b00da8b6",
        "object_or_effect": "w_6c98046e5eacb1bb4ef4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6c98046e5eacb1bb4ef4",
        "grounded": true
      },
      {
        "id": "fact_3581b937243af0689eb6",
        "object_or_effect": "w_76a24ac8c07ee80e068d",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_76a24ac8c07ee80e068d",
        "grounded": true
      },
      {
        "id": "fact_3d5d08389f8b8341cdef",
        "object_or_effect": "w_3b182c132bb1dacf9cd1",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_3b182c132bb1dacf9cd1",
        "grounded": true
      },
      {
        "id": "fact_42076571e1bc6fe2b116",
        "object_or_effect": "w_c9a6639e83616330938c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c9a6639e83616330938c",
        "grounded": true
      },
      {
        "id": "fact_437cf89b9b240d5dccc9",
        "object_or_effect": "w_330a0c84abd59c737885",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_330a0c84abd59c737885",
        "grounded": true
      },
      {
        "id": "fact_45a5dc8d6adf64178b7f",
        "object_or_effect": "w_c0fb157a62f8606ce3fe",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c0fb157a62f8606ce3fe",
        "grounded": true
      },
      {
        "id": "fact_488c144ecca5bf2b8611",
        "object_or_effect": "w_d4cdd79ddc11a5551f99",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d4cdd79ddc11a5551f99",
        "grounded": true
      },
      {
        "id": "fact_4b0446157469a01d3e16",
        "object_or_effect": "w_c75a23bba0c9f82eadac",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c75a23bba0c9f82eadac",
        "grounded": true
      },
      {
        "id": "fact_4e5eefe6a54cbd38e8a9",
        "object_or_effect": "w_d50f1d625e0c57410479",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d50f1d625e0c57410479",
        "grounded": true
      },
      {
        "id": "fact_4ec98c4ae3bee7f02900",
        "object_or_effect": "w_3b182c132bb1dacf9cd1",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_3b182c132bb1dacf9cd1",
        "grounded": true
      },
      {
        "id": "fact_516634a6882e3a268057",
        "object_or_effect": "w_5711cee39111628463cf",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_5711cee39111628463cf",
        "grounded": true
      },
      {
        "id": "fact_51aed856ec5040bbd504",
        "object_or_effect": "w_a1f44f20964c52ebc2dd",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_a1f44f20964c52ebc2dd",
        "grounded": true
      },
      {
        "id": "fact_56042d143addf4e7a8cb",
        "object_or_effect": "w_d50f1d625e0c57410479",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_d50f1d625e0c57410479",
        "grounded": true
      },
      {
        "id": "fact_5b57fb37e89233ff25fd",
        "object_or_effect": "w_1419aeb3ae1d4ce97cf3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_1419aeb3ae1d4ce97cf3",
        "grounded": true
      },
      {
        "id": "fact_5f28b545c011ae5b4b60",
        "object_or_effect": "w_e377c97244c7c40cb42d",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_e377c97244c7c40cb42d",
        "grounded": true
      },
      {
        "id": "fact_5f35876a8ad460791d1b",
        "object_or_effect": "w_2a7da4eeba8adcd4ebda",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_2a7da4eeba8adcd4ebda",
        "grounded": true
      },
      {
        "id": "fact_63f6313633868c4a2d53",
        "object_or_effect": "w_78e3bda79870790d4dc7",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_78e3bda79870790d4dc7",
        "grounded": true
      },
      {
        "id": "fact_63f983e0b606ecc9a8a2",
        "object_or_effect": "w_30570076a5ca8dae1aaf",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_30570076a5ca8dae1aaf",
        "grounded": true
      },
      {
        "id": "fact_6488d56bbdeb6d58f51f",
        "object_or_effect": "w_1419aeb3ae1d4ce97cf3",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_1419aeb3ae1d4ce97cf3",
        "grounded": true
      },
      {
        "id": "fact_68aab74b47ce6f285067",
        "object_or_effect": "w_e1673d674be655b345c5",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_e1673d674be655b345c5",
        "grounded": true
      },
      {
        "id": "fact_731715e73b25175828ad",
        "object_or_effect": "w_438caf8e3becc694623f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_438caf8e3becc694623f",
        "grounded": true
      },
      {
        "id": "fact_73982ac5c714fdd20b7c",
        "object_or_effect": "w_181db23a48d8730ef7c4",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_181db23a48d8730ef7c4",
        "grounded": true
      },
      {
        "id": "fact_753eadf165ce1a9531a8",
        "object_or_effect": "w_757b343e4234d98abffe",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_757b343e4234d98abffe",
        "grounded": true
      },
      {
        "id": "fact_7b7b18e899fd6c2d633d",
        "object_or_effect": "w_d61a0bf24d8ff103791e",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_d61a0bf24d8ff103791e",
        "grounded": true
      },
      {
        "id": "fact_7efc350aa90b9d8b719f",
        "object_or_effect": "w_aa7bf09d20435930acc3",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_aa7bf09d20435930acc3",
        "grounded": true
      },
      {
        "id": "fact_7f46c754012466c9c2f3",
        "object_or_effect": "w_c0221cfb792c94b14748",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c0221cfb792c94b14748",
        "grounded": true
      },
      {
        "id": "fact_8342a0b6a83250b53f3d",
        "object_or_effect": "o_ec302165a8dc4e4986f6",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_859e8bc7f01b8dd884ca",
        "object_or_effect": "w_68ee2d0670ce909d9bf6",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_68ee2d0670ce909d9bf6",
        "grounded": true
      },
      {
        "id": "fact_8b2d531ea55456ce0fa7",
        "object_or_effect": "w_e1673d674be655b345c5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e1673d674be655b345c5",
        "grounded": true
      },
      {
        "id": "fact_8f756ee79876da7cfbfb",
        "object_or_effect": "w_124c82605c0eea7ef28f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_124c82605c0eea7ef28f",
        "grounded": true
      },
      {
        "id": "fact_97c1d2b146632fe25d62",
        "object_or_effect": "w_49cc3ba41d861842c528",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_49cc3ba41d861842c528",
        "grounded": true
      },
      {
        "id": "fact_98e7944d56a77093044c",
        "object_or_effect": "w_fe5982faee7296cc0649",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_fe5982faee7296cc0649",
        "grounded": true
      },
      {
        "id": "fact_a29ae71ae6df6f1bbc4f",
        "object_or_effect": "w_08d8b260b09d23d4f2d5",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_08d8b260b09d23d4f2d5",
        "grounded": true
      },
      {
        "id": "fact_a948a7d137520481c0c4",
        "object_or_effect": "w_472d2f1b10f03a7c958c",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_472d2f1b10f03a7c958c",
        "grounded": true
      },
      {
        "id": "fact_ad53368f6dc49819b5fb",
        "object_or_effect": "w_754323a5aec644464d00",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_754323a5aec644464d00",
        "grounded": true
      },
      {
        "id": "fact_b12c9934fe2fca66c179",
        "object_or_effect": "w_08b1fa2d691ff1f1a175",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_08b1fa2d691ff1f1a175",
        "grounded": true
      },
      {
        "id": "fact_b2e85b737f5b6d0676a5",
        "object_or_effect": "w_6b5545c678c50839c48a",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_6b5545c678c50839c48a",
        "grounded": true
      },
      {
        "id": "fact_b400d0d94801f92131d4",
        "object_or_effect": "w_68ee2d0670ce909d9bf6",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_68ee2d0670ce909d9bf6",
        "grounded": true
      },
      {
        "id": "fact_b4092f85d7e07863fc14",
        "object_or_effect": "w_2d2ddb6b0f033ae596b5",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_2d2ddb6b0f033ae596b5",
        "grounded": true
      },
      {
        "id": "fact_b5adbbe87edf1b6fe6b3",
        "object_or_effect": "w_b4fc983d2f42fd5545fd",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_b4fc983d2f42fd5545fd",
        "grounded": true
      },
      {
        "id": "fact_b65e2294159e5fae6d07",
        "object_or_effect": "w_d93a44216a4f94f90f0f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d93a44216a4f94f90f0f",
        "grounded": true
      },
      {
        "id": "fact_b691fef5cf77b6d3d605",
        "object_or_effect": "w_c0221cfb792c94b14748",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c0221cfb792c94b14748",
        "grounded": true
      },
      {
        "id": "fact_b76a0755271c25718dc0",
        "object_or_effect": "w_9ab7e9c76fcd0f18641d",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_9ab7e9c76fcd0f18641d",
        "grounded": true
      },
      {
        "id": "fact_bd6d2226e0d79bfbca97",
        "object_or_effect": "w_fc9b10e93686780ea805",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_fc9b10e93686780ea805",
        "grounded": true
      },
      {
        "id": "fact_be017e48570811197616",
        "object_or_effect": "w_754323a5aec644464d00",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_754323a5aec644464d00",
        "grounded": true
      },
      {
        "id": "fact_c0e0180a9f5ca0cc73f2",
        "object_or_effect": "w_aa7bf09d20435930acc3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_aa7bf09d20435930acc3",
        "grounded": true
      },
      {
        "id": "fact_c1ed23d35fe1cab3f63e",
        "object_or_effect": "w_30570076a5ca8dae1aaf",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_30570076a5ca8dae1aaf",
        "grounded": true
      },
      {
        "id": "fact_c26176bbbcf3bc72221a",
        "object_or_effect": "o_45b9deb9ac9b3dcf12a3",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_c40d7ebc8ded86f5db38",
        "object_or_effect": "w_2c15d4a312cd1cc90709",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_2c15d4a312cd1cc90709",
        "grounded": true
      },
      {
        "id": "fact_c610985a13e7eb7f5519",
        "object_or_effect": "w_a1f44f20964c52ebc2dd",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_a1f44f20964c52ebc2dd",
        "grounded": true
      },
      {
        "id": "fact_c824d33a6aa52712f07d",
        "object_or_effect": "w_d4cdd79ddc11a5551f99",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_d4cdd79ddc11a5551f99",
        "grounded": true
      },
      {
        "id": "fact_c856d44b1360368e5d6f",
        "object_or_effect": "w_9ab7e9c76fcd0f18641d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_9ab7e9c76fcd0f18641d",
        "grounded": true
      },
      {
        "id": "fact_d22e0da3c34e45f42e34",
        "object_or_effect": "w_6c98046e5eacb1bb4ef4",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_6c98046e5eacb1bb4ef4",
        "grounded": true
      },
      {
        "id": "fact_d591834bb049b6ea3b8d",
        "object_or_effect": "w_fe5982faee7296cc0649",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_fe5982faee7296cc0649",
        "grounded": true
      },
      {
        "id": "fact_db077a6ed96b1a6ac302",
        "object_or_effect": "w_c0fb157a62f8606ce3fe",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c0fb157a62f8606ce3fe",
        "grounded": true
      },
      {
        "id": "fact_db51ac9f6f31f666edfb",
        "object_or_effect": "w_124c82605c0eea7ef28f",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_124c82605c0eea7ef28f",
        "grounded": true
      },
      {
        "id": "fact_dd7dfd486cfd20d2f4f9",
        "object_or_effect": "w_472d2f1b10f03a7c958c",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_472d2f1b10f03a7c958c",
        "grounded": true
      },
      {
        "id": "fact_dedaebeb849d03b6c8d7",
        "object_or_effect": "w_fb35d06150d553a63853",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_fb35d06150d553a63853",
        "grounded": true
      },
      {
        "id": "fact_e168989ed0f97ab8f70d",
        "object_or_effect": "w_d93a44216a4f94f90f0f",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_d93a44216a4f94f90f0f",
        "grounded": true
      },
      {
        "id": "fact_e651b8ad489ce1199974",
        "object_or_effect": "o_0ffa7bb5ffce630a55c7",
        "meaning": "financial_right",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_e6bd705b4f75e64d5a3c",
        "object_or_effect": "w_5711cee39111628463cf",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_5711cee39111628463cf",
        "grounded": true
      },
      {
        "id": "fact_e702aeda68f5f8be9c44",
        "object_or_effect": "w_c48374fa1344a14c9de3",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_c48374fa1344a14c9de3",
        "grounded": true
      },
      {
        "id": "fact_e85b3977ba58f790011c",
        "object_or_effect": "w_08b1fa2d691ff1f1a175",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_08b1fa2d691ff1f1a175",
        "grounded": true
      },
      {
        "id": "fact_ea84084349458e3ad0bf",
        "object_or_effect": "w_7a9fa11cb133d31808a4",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_7a9fa11cb133d31808a4",
        "grounded": true
      },
      {
        "id": "fact_ec33935a8288c2983ff7",
        "object_or_effect": "w_e377c97244c7c40cb42d",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_e377c97244c7c40cb42d",
        "grounded": true
      },
      {
        "id": "fact_ecf46c863c1af4626d6d",
        "object_or_effect": "w_520c7bb459a0d6632219",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": "w_520c7bb459a0d6632219",
        "grounded": true
      },
      {
        "id": "fact_f28b9c67416ff4b5b2c4",
        "object_or_effect": "w_2d2ddb6b0f033ae596b5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_2d2ddb6b0f033ae596b5",
        "grounded": true
      },
      {
        "id": "fact_f3cff8014069b1e39d50",
        "object_or_effect": "w_c75a23bba0c9f82eadac",
        "meaning": "authorization_quantity",
        "role": null,
        "subject": null,
        "scope": "w_c75a23bba0c9f82eadac",
        "grounded": true
      },
      {
        "id": "fact_f5ad3f2e0dd9c37c4159",
        "object_or_effect": "w_b4fc983d2f42fd5545fd",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_b4fc983d2f42fd5545fd",
        "grounded": true
      },
      {
        "id": "fact_fac568a2e39f6e2f6693",
        "object_or_effect": "o_0dc7d2dfa76a48ae3e48",
        "meaning": "management_role",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_fe016e6d96dd5b55b6fc",
        "object_or_effect": "w_d61a0bf24d8ff103791e",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_d61a0bf24d8ff103791e",
        "grounded": true
      }
    ],
    "query_summary": [],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 4,
      "category_ambiguous_or_outside_supported_task": 4,
      "unknown_assessment_vocabulary": 6,
      "semantic_answer_outside_sent_scope": 2,
      "no_locatable_source": 5,
      "unrelated_or_secondary_graph_pairs_deferred": 7,
      "yield_to_source_bound_semantic_review": 2,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "revision_outside_actual_feedback_scope": 1,
      "noncached_action_limit": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 145,
      "source_task_reading": 35,
      "scope_missing": 12,
      "external_dependency": 7,
      "covered_holder_grant": 1
    }
  }
}
```

## RQ1_4f19278de7d5

证据目录 run/members/RQ1_4f19278de7d5/attempt_1/，报告哈希 7580e25ca0be86aa432bdebd733271f04727dd6495bc758e4a7901d41fec34be

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
        "member": "RQ1_4f19278de7d5",
        "reference": "D2:181:author:1",
        "function": "init",
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
          "detail_sha256": "f9b561bfad17d25bc5cb9194fdf276943b985c21716d36d8c33a0b0736be7738",
          "issue": "issue_2a94df5fe026c0a9e92f"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c50fa71a640a3111e3247a111887475558924fc5dc66d3ad0e97f446ec7139de",
          "issue": "issue_2a94df5fe026c0a9e92f"
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
        "count": 2
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 1
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
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "invalid_semantic_row": 6,
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
      "no_effect_in_scope": 15,
      "external_dependency": 12,
      "source_task_reading": 7,
      "policy_missing": 1
    }
  }
}
```

## RQ1_4f9f1ce04ed8

证据目录 run/members/RQ1_4f9f1ce04ed8/attempt_1/，报告哈希 3473be50c8aa174c789654c26313f4da520afdd015c444dce21d5e3560b5b5d6

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
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed,category_ambiguous_or_outside_supported_task",
    "未决类别 FCR-PAUSE"
  ],
  "evaluation": {
    "target": "FCR-PAUSE",
    "positive": true,
    "paired_id": "RQ1_b0a696b11b0a",
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
          "detail_sha256": "c01069903c561c9649f80cc60606524033d67e3eeb54d9179c51f4dd8e98e51a"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "d35fc156eb6f3632b6da2fc19c27668fb33acab62e15313c1443ddfd255d4bbe"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "663982c8155fa840331c101147f235a908428f2cad0a13a839fb6435f16fdffa",
          "issue": "issue_16288d5ca44b640f055d"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "c88b4b6c717eefae400b8f98fba6c1f12ae4353df6684dac27841c39e030f427",
          "issue": "issue_16288d5ca44b640f055d"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "f0d71f0a2b0592b4ecb2a52b2acf88c702a248d8509d8a27a7987c47c44ff394",
          "issue": "issue_fb4272c8e332922f4aec"
        },
        {
          "reason": "negated_or_ambiguous_confirmation_not_a_risk_judgment",
          "detail_sha256": "09fb4d9059fc061e13788b3d92d88ee93862c433cebf03e38fd1629dfdb83bc5",
          "issue": "issue_fb4272c8e332922f4aec"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_5d138b2a570223aaf73f",
        "fact": "fact_448d92c712b2f2009620",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      },
      {
        "support": "support_c451001aa48dbd93ae3c",
        "fact": "fact_cb22b91fdce077e8a580",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_448d92c712b2f2009620",
        "object_or_effect": "o_18367577a3c1179af6d5",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": null,
        "grounded": true
      },
      {
        "id": "fact_992f1f63695ed1a0cb9b",
        "object_or_effect": "w_eb8349fe13324fadbf0f",
        "meaning": "eligibility_state",
        "role": null,
        "subject": null,
        "scope": "w_eb8349fe13324fadbf0f",
        "grounded": true
      },
      {
        "id": "fact_cb22b91fdce077e8a580",
        "object_or_effect": "o_d2a1e3c10de3c4e78204",
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
        "count": 5
      },
      {
        "label": "blocked_by_change",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 4
      },
      {
        "label": "two_distinct_holders_blocked_same_change",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "prefix_reachability",
        "answer": "unsat",
        "count": 2
      },
      {
        "label": "prefix_reachability",
        "answer": "sat",
        "count": 2
      },
      {
        "label": "control_transition_preservation",
        "answer": "unsat",
        "count": 1
      },
      {
        "label": "financial_block",
        "answer": "sat",
        "count": 1
      }
    ],
    "diagnostics": {
      "unbound_or_inapplicable_seed": 2,
      "invalid_semantic_row": 7,
      "category_ambiguous_or_outside_supported_task": 2,
      "unknown_assessment_vocabulary": 1,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 3,
      "negated_or_ambiguous_confirmation_not_a_risk_judgment": 1,
      "revision_outside_actual_feedback_scope": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-DESTROY",
      "FCR-FREEZE",
      "FCR-MINT",
      "FCR-TRANSFER"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 37,
      "program_support": 1,
      "scope_missing": 1,
      "source_check_excluded": 1
    }
  }
}
```

## RQ1_4febca8bfe3b

证据目录 run/members/RQ1_4febca8bfe3b/attempt_1/，报告哈希 2d58f9196717704daa7c50fca2a2e738f00bd768fdc45b3c2e2be4dd9acfb2df

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
    "last1164 新增指定类命中",
    "decision_only 新增指定类命中"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,no_locatable_source,category_ambiguous_or_outside_supported_task"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": true,
    "paired_id": "RQ1_49db443acf1d",
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
        "before": "unsupported",
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
          "detail_sha256": "5605f88e791cdfdfae23d156e2d8dd78cdf7a23399483fcd698526fa10f56d2d",
          "issue": "issue_49aea9f9b18199244d9d"
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
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "559ac0865bf57b406d122e15bf471d89659ee146bfd778898d818ddfb84b4c36",
          "issue": "issue_53ebfd9520874a0a210e"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "83dec84d7994f3aac42853356fa599a361afa52cc78257a9e22feeb6814f43ab",
          "issue": "issue_53ebfd9520874a0a210e"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_6dbdb6520b2026a77edb",
        "fact": "fact_a5639e9827e170c107d2",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_a5639e9827e170c107d2",
        "object_or_effect": "o_92bfca5069e99798f9ed",
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
      "invalid_semantic_row": 10,
      "unknown_assessment_vocabulary": 2,
      "no_locatable_source": 2,
      "category_ambiguous_or_outside_supported_task": 1
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
      "program_support": 1
    }
  }
}
```

## RQ1_4feeb0c21e60

证据目录 run/members/RQ1_4feeb0c21e60/attempt_1/，报告哈希 bb8374f4ce104d37dc0b207bff49f8e18a5729ffc9d20bdaa050098feee89201

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
    "已确认消费/覆盖诊断 invalid_semantic_row,unknown_assessment_vocabulary,category_ambiguous_or_outside_supported_task,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": true,
    "paired_id": "RQ1_0e202076b336",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "2787680d4555d40138a9db70d1d79fd12c8ad92acda1e36a9f97f147c8acea3c",
          "issue": "issue_e8f1034347f3c3922f29"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "7a1dd90b32f755d1428091c3f83172a5d02bcc25e7033e98bd125843a062384c",
          "issue": "issue_3413ba126198adaa89e1"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "5c13a83c98315596b09ffe913f96516e0eed11f72047888a829c313a43470651",
          "issue": "issue_3413ba126198adaa89e1"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_7f5feca9e70c59f28a5f",
        "fact": "fact_921cd32ad55531f7c3eb",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_921cd32ad55531f7c3eb",
        "object_or_effect": "o_2c644b1d4cad654ac89f",
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
        "count": 1
      },
      {
        "label": "baseline_usable",
        "answer": "sat",
        "count": 1
      },
      {
        "label": "blocked_by_change",
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
      "invalid_semantic_row": 4,
      "unknown_assessment_vocabulary": 2,
      "category_ambiguous_or_outside_supported_task": 1,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 1
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 48,
      "external_dependency": 11,
      "source_task_reading": 1
    }
  }
}
```

## RQ1_511b9f30f4b7

证据目录 run/members/RQ1_511b9f30f4b7/attempt_1/，报告哈希 6e73fc410be8925b7530a9e76da97831636284f5f05b5f8d18727ccd4c09eda5

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 unbound_or_inapplicable_seed,unknown_assessment_vocabulary,no_locatable_source,invalid_semantic_row",
    "未决类别 AC"
  ],
  "evaluation": {
    "roots": [
      {
        "member": "RQ1_511b9f30f4b7",
        "reference": "D2:38:author:1",
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
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "6a61ad1caa2ad86ea0907a0a2f950e5de7740ef598ee88c74c74e961d6ef403b",
          "issue": "issue_21dedc5d9ba00e6476c9"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "6aa1f4b3dc1d0c7dcceccef542f85f05d8615a07227be3b0f199ba2fe33549f9",
          "issue": "issue_d37c729a2681ff05223e"
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
          "detail_sha256": "5469ef98c43079965006bd7ef2a3114a7a11a6fff935f71adbd4e1888b7c8888",
          "issue": "issue_ad191c5267a550760e29"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "f118acf09e3997552b412446077c73d674ea2099482771257d63ffc692424c26",
          "issue": "issue_ad191c5267a550760e29"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "bf4b98617d433683336c9b520c6c51eb3333c082c25dbd7193d2ca4c5e5233c9",
          "issue": "issue_3b8be705cfbb0028daa9"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "0bace6614653ff2a77dc224b348f8fadd8463d164c272e6b0be9990952cae9c9",
          "issue": "issue_3b8be705cfbb0028daa9"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "2029f8e2c3786f69bea65ece5ef6a5907b90c5bd8e2fc8c01dae67477146bcb3",
          "issue": "issue_df547e2ca6bd6095dfca"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "4356ef0518417d224031064f5f62df1a3073adf6777f2a84ef5880c21afab148",
          "issue": "issue_df547e2ca6bd6095dfca"
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
      "unbound_or_inapplicable_seed": 15,
      "unknown_assessment_vocabulary": 5,
      "no_locatable_source": 5,
      "invalid_semantic_row": 3,
      "category_ambiguous_or_outside_supported_task": 3,
      "semantic_answer_outside_sent_scope": 3
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

## RQ1_51a9713a1934

证据目录 run/members/RQ1_51a9713a1934/attempt_1/，报告哈希 72b73f08d4bdc17f55413423fa573024b0b8b5e9963e30b0522d49ee31acd0a1

```json
{
  "task": "AC",
  "prediction": {
    "AC": "unsupported"
  },
  "changes": [],
  "reason_review": [
    "结果不变；内部语义支持、查询及覆盖记录仍单独保留。",
    "已确认消费/覆盖诊断 invalid_semantic_row,semantic_answer_outside_sent_scope",
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
      "invalid_semantic_row": 10,
      "semantic_answer_outside_sent_scope": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [],
    "obligation_bases": {
      "no_effect_in_scope": 38,
      "external_dependency": 6,
      "source_context_missing": 4,
      "model_phase_missing": 17
    }
  }
}
```

## RQ1_53f9777ccdf6

证据目录 run/members/RQ1_53f9777ccdf6/attempt_1/，报告哈希 af8fc3c054325378b89cadd12d8dc2faab5c62684a17e5a356dea9083cdd5432

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
    "decision_only 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 invalid_semantic_row,category_ambiguous_or_outside_supported_task,unknown_assessment_vocabulary,semantic_answer_outside_sent_scope",
    "未决类别 FCR-DESTROY,FCR-FREEZE,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-TRANSFER",
    "positive": true,
    "paired_id": "RQ1_a7d72c1e4129",
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
          "reason": "invalid_semantic_row",
          "detail_sha256": "23a6538a9ed5b2f61822e0e7b5063a3598a192d13fc88c7a9ac1328ad4db6f82"
        },
        {
          "reason": "invalid_semantic_row",
          "detail_sha256": "3e7fa87176cfe502a18032a71e51c370af5daba9e41823bd3e38d457c96859ac"
        },
        {
          "reason": "category_ambiguous_or_outside_supported_task",
          "detail_sha256": "b45895c8460d75caf2a9da754b85f55d9f55ebc1bbe17b7cfca1ccf1168f75cb",
          "issue": "issue_804601c2a74b562f7e6e"
        },
        {
          "reason": "unknown_assessment_vocabulary",
          "detail_sha256": "35521322ba67ae119e4a0d66c047187704f57485df2838321ffcc90a64d38192",
          "issue": "issue_804601c2a74b562f7e6e"
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
      "invalid_semantic_row": 8,
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
      "no_effect_in_scope": 44,
      "external_dependency": 15,
      "source_task_reading": 1
    }
  }
}
```

## RQ1_55a1e2ef0f09

证据目录 run/members/RQ1_55a1e2ef0f09/attempt_1/，报告哈希 8211d2c870629690d03f80a8f8fcd93d1b29413c7829fae2374e128be2fce846

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
    "v32 退为未知，不能当作纠正",
    "last1164 退为未知，不能当作纠正"
  ],
  "reason_review": [
    "实际记录确认结果变化；缺少逐字原答，无法唯一归因模型原始业务解释。",
    "已确认消费/覆盖诊断 unrelated_or_secondary_graph_pairs_deferred,unbound_or_inapplicable_seed,noncached_action_limit,invalid_seed_fields",
    "未决类别 FCR-DESTROY,FCR-MINT,FCR-PAUSE,FCR-TRANSFER"
  ],
  "evaluation": {
    "target": "FCR-DESTROY",
    "positive": true,
    "paired_id": "RQ1_fe4ace2cd8e5",
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
          "reason": "invalid_seed_fields",
          "detail_sha256": "303a9aa6a1bacf281bb4c27501cc9890b6d69631c6e3efd90f79661a98149611"
        }
      ]
    }
  ],
  "mechanism": {
    "supports": [
      {
        "support": "support_b36cd10410d911be94aa",
        "fact": "fact_09cc6df727b09b0963d3",
        "origin": "verified_service",
        "field": "annotations",
        "version": 1
      }
    ],
    "facts": [
      {
        "id": "fact_09cc6df727b09b0963d3",
        "object_or_effect": "o_8ecda1ad460f101da6cf",
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
        "count": 9
      },
      {
        "label": "opened_by_change",
        "answer": "sat",
        "count": 7
      },
      {
        "label": "both_usable",
        "answer": "sat",
        "count": 9
      },
      {
        "label": "opened_by_change",
        "answer": "unsat",
        "count": 4
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
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "unsat",
        "count": 22
      },
      {
        "label": "same_request_amount_change",
        "answer": "unsat",
        "count": 22
      },
      {
        "label": "financial_value",
        "answer": "unsat",
        "count": 32
      },
      {
        "label": "financial_consent_unresolved",
        "answer": "unsat",
        "count": 6
      },
      {
        "label": "financial_value_post_exclusion",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "financial_value",
        "answer": "sat",
        "count": 3
      },
      {
        "label": "local_premises_feasible",
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
      "unbound_or_inapplicable_seed": 2,
      "invalid_seed_fields": 1,
      "semantic_answer_outside_sent_scope": 1,
      "unrelated_or_secondary_graph_pairs_deferred": 6,
      "noncached_action_limit": 2
    }
  },
  "coverage_summary": {
    "whole_reading_eligible": false,
    "negative_eligible_categories": [
      "FCR-FREEZE"
    ],
    "obligation_bases": {
      "no_effect_in_scope": 162,
      "source_task_reading": 8,
      "scope_missing": 16,
      "covered_holder_grant": 1,
      "external_dependency": 3
    }
  }
}
```
