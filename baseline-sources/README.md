# Permission Risks 对比方法源码导航

本页固定了本项目审阅使用的 ACTaint 和 JANUS 源码版本。点击下列链接即可逐文件阅读全文。

## ACTaint

[全部源码](https://github.com/Smart-Contract-Security/ACTaint/tree/02cb5ee9aca44b3a435a19927b1153b0d2cfa32d/src)
｜[分析主入口](https://github.com/Smart-Contract-Security/ACTaint/blob/02cb5ee9aca44b3a435a19927b1153b0d2cfa32d/src/analyze_smart_contract.py)
｜[图构建](https://github.com/Smart-Contract-Security/ACTaint/blob/02cb5ee9aca44b3a435a19927b1153b0d2cfa32d/src/build_cv_graph.py)

本地 `ACTaint源码.zip` 的 17 个文件均已与该提交逐字节核对。
原 ZIP SHA-256：`316e617dd3926840bf88641a07c82d5740e6bc15f9287aa6c9233d9e0f31cbad`

## JANUS

[仓库与作者说明](https://github.com/secwisf/JANUS/tree/3d540eb66c450ad6340a0e69360ba2e559b49ca9)
｜[backdoor 分析代码](https://github.com/secwisf/JANUS/tree/3d540eb66c450ad6340a0e69360ba2e559b49ca9/backdoor)
｜[vpg 模块](https://github.com/secwisf/JANUS/tree/3d540eb66c450ad6340a0e69360ba2e559b49ca9/vpg)
｜[validation 模块](https://github.com/secwisf/JANUS/tree/3d540eb66c450ad6340a0e69360ba2e559b49ca9/validation)

本地 `JANUS.zip` 中除 `node_modules/` 外的 100 个文件均已与该提交逐字节核对。
原 ZIP SHA-256：`65a2a23d7a396351950913b311abe908b831a815eee8511020635fb02fdab217`
