# G 与 R4-Simple 的实际源码差异

两臂运行相同的冻结输入、模型首答、分词器、配置和评价规则。Simple 改变的是对一类额度授权意见的程序处理；本轮比较覆盖这一整组变更。 [冻结身份](Freeze.json) · [方法和每文件摘要](Versions.json)

| 原方法文件 | 实际差异 |
|---|---|
| `investigation/property_model.py` | `compose()` 在源依据读取后调用 `effect_consumption.assess()`，保留返回的作用核查回执。 [G](Code/G/property_model.py#L522) · [Simple](Code/Simple/property_model.py#L522) |
| `investigation/effect_consumption.py` | Simple 新增 `assess()`，对实际余额扣减核对该额度条件是否覆盖每条相关路径。 [源码](Code/Simple/effect_consumption.py#L7) |
| `investigation/transfer_scope.py` | Simple 新增 `bind_transfers()` 等逻辑，用同操作、目标、声明、有序键和数量对齐余额作用与额度使用。 [源码](Code/Simple/transfer_scope.py#L91) |

额度条件匹配后，消费者还检查原判断是否允许该正常解释、是否已有程序性质证书、是否存在另一个位置上的独立已验证正证。作用不能绑定、授权来源不全、额度界限没有覆盖所有扣减路径的候选保留原处理。这是同作用的授权核对，结果的实际影响见证据页。 [完整三文件差异](Code/G_to_Simple.diff) · [共用配置](Code/full_expanded_900s_20s.json) · [实际证据](Evidence.md)

网页列出的四份源码和共用配置均逐字节核对了原 ZIP 及方法文件 SHA-256。组合变更已有对照；作用绑定和随后的正常证明各自贡献仍待单独消融。 [包身份](Freeze.json) · [源码哈希](Versions.json)
