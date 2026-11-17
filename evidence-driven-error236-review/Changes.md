# 逐根变化、误报与剩余问题

[主报告](WorkReview.md) · [全部根](Roots.md) · [FCR](FCR.md)

## AC新增与丢失

| 变化 | 根 | 函数 | 成员 | 本次可见理由 |
|---|---|---|---|---|
| gained | D2:67:author:1 | MyTestWallet7 | [RQ1_281f3b161467](Cases-02.md#rq1_281f3b161467) | source_role_reassignment,policy_missing |
| lost | D2:290:S1 | task | [RQ1_9f051c86ed67](Cases-05.md#rq1_9f051c86ed67) | policy_missing |
| lost | D2:303:S1 | Own | [RQ1_341058e186b5](Cases-05.md#rq1_341058e186b5) | policy_missing,local_bookkeeping |
| lost | D2:307:S1 | Ownables | [RQ1_371f33f7ff6f](Cases-05.md#rq1_371f33f7ff6f) | local_bookkeeping |
| lost | D2:521:S1 | init | [RQ1_f694e40ffba2](Cases-08.md#rq1_f694e40ffba2) | policy_missing,local_bookkeeping |
| lost | D2:534:S1 | owned | [RQ1_254bfee03840](Cases-08.md#rq1_254bfee03840) | local_bookkeeping |
| gained | D2:574:S1 | initVault | [RQ1_7fcdff67fecb](Cases-09.md#rq1_7fcdff67fecb) | policy_missing,program_support,local_bookkeeping |
| gained | D2:72:original:2 | StartRoulette | [RQ1_3dba1c8c9669](Cases-10.md#rq1_3dba1c8c9669) | source_role_reassignment,policy_missing |
| gained | D2:450:original:1 | StartRoulette | [RQ1_7623b2a26a25](Cases-10.md#rq1_7623b2a26a25) | source_role_reassignment,policy_missing |
| gained | D2:421:original:1 | StartRoulette | [RQ1_771e49570272](Cases-10.md#rq1_771e49570272) | policy_missing,source_role_reassignment |
| gained | D2:523:original:2 | StartRoulette | [RQ1_999f460049c5](Cases-10.md#rq1_999f460049c5) | policy_missing,source_role_reassignment |
| gained | D2:427:original:1 | setOwner | [RQ1_d639862f5b71](Cases-11.md#rq1_d639862f5b71) | policy_missing,local_bookkeeping,source_role_reassignment |
| lost | D2:37:original:1 | RegisterDevice | [RQ1_e6f04047bff4](Cases-11.md#rq1_e6f04047bff4) | local_bookkeeping |

## AC参考外发生点（51）

| 成员 | 作用 | 字节 | 决定 | 明细 |
|---|---|---|---|---|
| RQ1_01900f3f9b7c | mintToken | 4284 | unbacked_source_issuance | [逐例](Cases-03.md#rq1_01900f3f9b7c) |
| RQ1_0930870e6f17 | doAirdrop | 3515 | unbacked_source_issuance | [逐例](Cases-04.md#rq1_0930870e6f17) |
| RQ1_0a67a2a6aa84 | doAirdrop | 3541 | unbacked_source_issuance | [逐例](Cases-07.md#rq1_0a67a2a6aa84) |
| RQ1_0bcbefea1890 | mintToken | 4226 | unbacked_source_issuance | [逐例](Cases-10.md#rq1_0bcbefea1890) |
| RQ1_0cd685c505a3 | doAirdrop | 3528 | unbacked_source_issuance | [逐例](Cases-05.md#rq1_0cd685c505a3) |
| RQ1_1007b4fc52ca | mintToken | 4224 | unbacked_source_issuance | [逐例](Cases-04.md#rq1_1007b4fc52ca) |
| RQ1_116d8aeb4b40 | doAirdrop | 3559 | unbacked_source_issuance | [逐例](Cases-08.md#rq1_116d8aeb4b40) |
| RQ1_18f20020e22b | doAirdrop | 3549 | unbacked_source_issuance | [逐例](Cases-05.md#rq1_18f20020e22b) |
| RQ1_224d9bccba32 | doAirdrop | 3505 | unbacked_source_issuance | [逐例](Cases-03.md#rq1_224d9bccba32) |
| RQ1_235a30b99277 | mintToken | 4015 | unbacked_source_issuance | [逐例](Cases-01.md#rq1_235a30b99277) |
| RQ1_277940cef55d | doAirdrop | 3538 | unbacked_source_issuance | [逐例](Cases-05.md#rq1_277940cef55d) |
| RQ1_298ee75a547f | doAirdrop | 3560 | unbacked_source_issuance | [逐例](Cases-01.md#rq1_298ee75a547f) |
| RQ1_2ab8786fb079 | doAirdrop | 3625 | unbacked_source_issuance | [逐例](Cases-02.md#rq1_2ab8786fb079) |
| RQ1_309938a2bbb9 | doAirdrop | 3519 | unbacked_source_issuance | [逐例](Cases-02.md#rq1_309938a2bbb9) |
| RQ1_3daa3272da3f | mintToken | 4226 | unbacked_source_issuance | [逐例](Cases-09.md#rq1_3daa3272da3f) |
| RQ1_409f227124c6 | doAirdrop | 3526 | unbacked_source_issuance | [逐例](Cases-07.md#rq1_409f227124c6) |
| RQ1_42449480aa59 | doAirdrop | 3541 | unbacked_source_issuance | [逐例](Cases-07.md#rq1_42449480aa59) |
| RQ1_4325a2042776 | doAirdrop | 3524 | unbacked_source_issuance | [逐例](Cases-03.md#rq1_4325a2042776) |
| RQ1_43b9baf37b44 | doAirdrop | 3575 | unbacked_source_issuance | [逐例](Cases-01.md#rq1_43b9baf37b44) |
| RQ1_4c2921d39474 | AuthorizePayments | 2703 | unguarded_governed_effect | [逐例](Cases-08.md#rq1_4c2921d39474) |
| RQ1_52d5c754a744 | addString | 329 | scoped_semantic_conflict | [逐例](Cases-09.md#rq1_52d5c754a744) |
| RQ1_52d5c754a744 | setOwner | 417 | program_support | [逐例](Cases-09.md#rq1_52d5c754a744) |
| RQ1_52d5c754a744 | destroy | 557 | scoped_semantic_conflict | [逐例](Cases-09.md#rq1_52d5c754a744) |
| RQ1_57506af34f24 | doAirdrop | 3505 | unbacked_source_issuance | [逐例](Cases-04.md#rq1_57506af34f24) |
| RQ1_671ac389b102 | doAirdrop | 3709 | unbacked_source_issuance | [逐例](Cases-03.md#rq1_671ac389b102) |
| RQ1_6d7db4fbefe5 | doAirdrop | 3551 | unbacked_source_issuance | [逐例](Cases-01.md#rq1_6d7db4fbefe5) |
| RQ1_701182c88214 | mintToken | 4224 | unbacked_source_issuance | [逐例](Cases-04.md#rq1_701182c88214) |
| RQ1_742a666ba5fe | doAirdrop | 3555 | unbacked_source_issuance | [逐例](Cases-06.md#rq1_742a666ba5fe) |
| RQ1_8b881d18ff63 | mintToken | 4560 | unbacked_source_issuance | [逐例](Cases-09.md#rq1_8b881d18ff63) |
| RQ1_8f44e59cd670 | doAirdrop | 3550 | unbacked_source_issuance | [逐例](Cases-01.md#rq1_8f44e59cd670) |
| RQ1_947273fa2eef | mintToken | 4332 | unbacked_source_issuance | [逐例](Cases-01.md#rq1_947273fa2eef) |
| RQ1_98079f94c997 | doAirdrop | 3581 | unbacked_source_issuance | [逐例](Cases-07.md#rq1_98079f94c997) |
| RQ1_991cdff3e261 | doAirdrop | 3516 | unbacked_source_issuance | [逐例](Cases-09.md#rq1_991cdff3e261) |
| RQ1_affea7f70c2f | doAirdrop | 3546 | unbacked_source_issuance | [逐例](Cases-07.md#rq1_affea7f70c2f) |
| RQ1_bbf6634a1913 | mintToken | 4224 | unbacked_source_issuance | [逐例](Cases-01.md#rq1_bbf6634a1913) |
| RQ1_bc14311821a2 | mintToken | 4332 | unbacked_source_issuance | [逐例](Cases-09.md#rq1_bc14311821a2) |
| RQ1_be17ecaef698 | endBetPeriod | 3242 | unguarded_governed_effect | [逐例](Cases-09.md#rq1_be17ecaef698) |
| RQ1_c29ef00e048d | doAirdrop | 3557 | unbacked_source_issuance | [逐例](Cases-04.md#rq1_c29ef00e048d) |
| RQ1_c9b9d9ecb7bb | AuthorizePayments | 2737 | unguarded_governed_effect | [逐例](Cases-09.md#rq1_c9b9d9ecb7bb) |
| RQ1_d05efb1718e4 | doAirdrop | 3562 | unbacked_source_issuance | [逐例](Cases-02.md#rq1_d05efb1718e4) |
| RQ1_d80631993985 | doAirdrop | 3518 | unbacked_source_issuance | [逐例](Cases-01.md#rq1_d80631993985) |
| RQ1_dadf1b436e9d | mintToken | 4332 | unbacked_source_issuance | [逐例](Cases-07.md#rq1_dadf1b436e9d) |
| RQ1_dee4a75fd1b4 | acceptOwnership | 1073 | source_role_reassignment | [逐例](Cases-10.md#rq1_dee4a75fd1b4) |
| RQ1_dee4a75fd1b4 | transferOwnership | 926 | source_role_reassignment | [逐例](Cases-10.md#rq1_dee4a75fd1b4) |
| RQ1_e02b882a516b | doAirdrop | 3527 | unbacked_source_issuance | [逐例](Cases-07.md#rq1_e02b882a516b) |
| RQ1_e3be5dad4539 | doAirdrop | 3528 | unbacked_source_issuance | [逐例](Cases-10.md#rq1_e3be5dad4539) |
| RQ1_e88cd683cd73 | doAirdrop | 3541 | unbacked_source_issuance | [逐例](Cases-08.md#rq1_e88cd683cd73) |
| RQ1_e97f2d279ad9 | mintToken | 3979 | unbacked_source_issuance | [逐例](Cases-02.md#rq1_e97f2d279ad9) |
| RQ1_f09f7b47307f | doAirdrop | 3559 | unbacked_source_issuance | [逐例](Cases-07.md#rq1_f09f7b47307f) |
| RQ1_f82d8856631a | doAirdrop | 3505 | unbacked_source_issuance | [逐例](Cases-05.md#rq1_f82d8856631a) |
| RQ1_f91e2b168fdf | doAirdrop | 3549 | unbacked_source_issuance | [逐例](Cases-07.md#rq1_f91e2b168fdf) |

## FCR逐项

| 成员 | 类别 | 旧→新 | 变化 | 证据 |
|---|---|---|---|---|
| RQ1_7cc11a697bd2 | FCR-MINT | alarm→unsupported | FP_withdrawn_still_unknown | [逐例](Cases-11.md#rq1_7cc11a697bd2) |
| RQ1_81a85f242b60 | FCR-MINT | alarm→unsupported | FP_withdrawn_still_unknown | [逐例](Cases-11.md#rq1_81a85f242b60) |
| RQ1_cbb6e67b8b81 | FCR-MINT | alarm→unsupported | FP_withdrawn_still_unknown | [逐例](Cases-12.md#rq1_cbb6e67b8b81) |
| RQ1_328c13393c2c | FCR-DESTROY | unsupported→unsupported | still_FN | [逐例](Cases-11.md#rq1_328c13393c2c) |
| RQ1_33d48945207e | FCR-DESTROY | unsupported→unsupported | still_FN | [逐例](Cases-11.md#rq1_33d48945207e) |
| RQ1_353a9b0b5006 | FCR-DESTROY | unsupported→technical_error | still_FN | [逐例](Cases-12.md#rq1_353a9b0b5006) |
| RQ1_440857b3df3c | FCR-DESTROY | unsupported→unsupported | still_FN | [逐例](Cases-12.md#rq1_440857b3df3c) |
| RQ1_4b4775267823 | FCR-DESTROY | unsupported→unsupported | still_FN | [逐例](Cases-11.md#rq1_4b4775267823) |
| RQ1_55a1e2ef0f09 | FCR-DESTROY | unsupported→unsupported | still_FN | [逐例](Cases-11.md#rq1_55a1e2ef0f09) |
| RQ1_5b3469baa447 | FCR-DESTROY | not_detected→alarm | recovered_FN | [逐例](Cases-11.md#rq1_5b3469baa447) |
| RQ1_6eeaddaeac8f | FCR-DESTROY | unsupported→unsupported | still_FN | [逐例](Cases-12.md#rq1_6eeaddaeac8f) |
| RQ1_8e4c324fa1c9 | FCR-DESTROY | unsupported→unsupported | still_FN | [逐例](Cases-12.md#rq1_8e4c324fa1c9) |
| RQ1_b472a9a0647e | FCR-DESTROY | unsupported→unsupported | still_FN | [逐例](Cases-11.md#rq1_b472a9a0647e) |
| RQ1_eb22e4884871 | FCR-DESTROY | unsupported→unsupported | still_FN | [逐例](Cases-12.md#rq1_eb22e4884871) |
| RQ1_eb30c6dee989 | FCR-DESTROY | unsupported→unsupported | still_FN | [逐例](Cases-11.md#rq1_eb30c6dee989) |
| RQ1_f922252cd038 | FCR-DESTROY | unsupported→unsupported | still_FN | [逐例](Cases-11.md#rq1_f922252cd038) |
| RQ1_185a84436c18 | FCR-PAUSE | unsupported→unsupported | still_FN | [逐例](Cases-12.md#rq1_185a84436c18) |
| RQ1_e390407a4c29 | FCR-PAUSE | unsupported→unsupported | still_FN | [逐例](Cases-12.md#rq1_e390407a4c29) |
| RQ1_0c8823eed851 | FCR-FREEZE | not_detected→not_detected | still_FN | [逐例](Cases-11.md#rq1_0c8823eed851) |
| RQ1_23abf434df32 | FCR-FREEZE | unsupported→unsupported | still_FN | [逐例](Cases-12.md#rq1_23abf434df32) |
| RQ1_32e1e7ce1240 | FCR-FREEZE | unsupported→unsupported | still_FN | [逐例](Cases-12.md#rq1_32e1e7ce1240) |
| RQ1_39fb6e7197c4 | FCR-FREEZE | not_detected→not_detected | still_FN | [逐例](Cases-12.md#rq1_39fb6e7197c4) |
| RQ1_58de46f081ec | FCR-FREEZE | not_detected→not_detected | still_FN | [逐例](Cases-11.md#rq1_58de46f081ec) |
| RQ1_5ab05cf437b3 | FCR-FREEZE | unsupported→unsupported | still_FN | [逐例](Cases-11.md#rq1_5ab05cf437b3) |
| RQ1_5b3c7cbe3d9d | FCR-FREEZE | unsupported→unsupported | still_FN | [逐例](Cases-11.md#rq1_5b3c7cbe3d9d) |
| RQ1_6239598c387b | FCR-FREEZE | unsupported→unsupported | still_FN | [逐例](Cases-12.md#rq1_6239598c387b) |
| RQ1_65379f53b3ab | FCR-FREEZE | unsupported→unsupported | still_FN | [逐例](Cases-11.md#rq1_65379f53b3ab) |
| RQ1_6a278772c4f3 | FCR-FREEZE | unsupported→unsupported | still_FN | [逐例](Cases-11.md#rq1_6a278772c4f3) |
| RQ1_8921e5cc1831 | FCR-FREEZE | unsupported→unsupported | still_FN | [逐例](Cases-11.md#rq1_8921e5cc1831) |
| RQ1_95cf7213c86a | FCR-FREEZE | unsupported→not_detected | still_FN | [逐例](Cases-12.md#rq1_95cf7213c86a) |
| RQ1_abb48ccfac75 | FCR-FREEZE | unsupported→unsupported | still_FN | [逐例](Cases-12.md#rq1_abb48ccfac75) |
| RQ1_b7fd0e26135f | FCR-FREEZE | unsupported→unsupported | still_FN | [逐例](Cases-12.md#rq1_b7fd0e26135f) |
| RQ1_c80f7a639e42 | FCR-FREEZE | not_detected→not_detected | still_FN | [逐例](Cases-12.md#rq1_c80f7a639e42) |

## 源码身份与未实施事项

相对上次完整实跑2e0共7个方法文件变化；相对直接父fb2只有financial_value.py定点返修。当前仅做只读结果审阅，不改方法、标签、历史评分或真实协议。未运行的8旧AC FP与其它正确保护不能宣称无退化。
