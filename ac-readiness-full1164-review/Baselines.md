# Baseline来源与可比较范围

本轮未追加任何baseline运行。下表沿用已经保存的公开作者表或历史实跑台账。实际成员、预处理、版本与预算差异见Versions及历史来源，作者公开成绩与本批结果分别保留。

| AC来源 | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|
| ACTaint 历史DeepSeek实跑 | 448 | 258 | 33 | 63.46% | 93.14% | 75.48% |
| AChecker 作者表 | 369 | 315 | 112 | 53.95% | 76.72% | 63.35% |

ACTaint沿用历史608＋16份运行与原映射，模型检查点和旧输出上限未证为与本轮完全一致。AChecker采用作者SmartBug表。v32是219方法文件的同成员历史Full；本轮没有重新执行v32或−LLM。

| FCR指定类 | Total | Pied-Piper作者FP/FN | Tokeer作者FP/FN | JANUS作者FP/FN |
|---|---|---|---|---|
| TRANSFER | 80 | 0/3 | 0/0 | 0/0 |
| MINT | 70 | 1/4 | 27/5 | 0/0 |
| DESTROY | 116 | 4/3 | 14/7 | 1/0 |
| PAUSE | 124 | 7/3 | N/A | 0/0 |
| FREEZE | 150 | 56/4 | 6/14 | 0/0 |

这些行不补造未知/失败分布，不自动建立严格同预算公平性。保存的项目来源为research_execution_20261111_r1/rel_revision_full1164_review_r1的Baselines、evaluation_only/PaperRows、ACTaIndex及Tools，和research_execution_20261110_r1/mech_compare_r1/Versions。
