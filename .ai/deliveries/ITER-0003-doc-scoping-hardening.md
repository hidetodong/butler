# ITER-0003 · 文档 scoped 有界硬约束

## 本次交付目标
- 堵死增量迭代中文档纵向堆积、越来越长不可控的风险：把"每个迭代文档只承载本迭代内容、有界"从软指令升级为硬约束。

## 已完成内容
- **Fix 1 工作区 overwrite-only**：`iteration-schema.md` §5.1 明文规定开新迭代时工作区四件套必须整体覆写，严禁保留/续写/追加上一迭代内容；§1 新增"文档有界，历史横向归档"不变量。
- **Fix 2 CHANGELOG 收口归档**：`01_CHANGELOG.md` 作用域收敛为当前活跃迭代热数据，收口时切片归档进 `iterations/ITER-NNNN/CHANGELOG.md`，全局文件不跨迭代累积；`mcv-update.md §5.1` 相应改为"主分片随迭代自动发生、体积分片退化兜底"。
- **Fix 3 deliveries 引用不嵌入**：`delivery-summary.md §4.7` 升级为硬约束——产物只能以路径/链接引用，不得全文嵌入交付总结。
- `lifecycle.md` P1/P5、`mcv-deployment.md §2` 同步接入上述三条。
- dogfood：本迭代工作区四件套整体覆写为 ITER-0003（清掉了 ITER-0002 僵尸残留），收口归档 + 交付 + 台账三层一致。

## 关键变更 / 用户可感知变化
- 以后每开一个新迭代，工作区四件套会被**整体覆写**为新迭代内容，老内容只在 `.ai/iterations/ITER-NNNN/` 归档里；单份文档体量恒定，历史靠迭代目录横向铺开。
- 交付总结永远是高层摘要，不会把验收清单/技术方案全文塞进去——只给指针。

## 高层影响范围
- 规则层：`Coder/20_Workflow_Lifecycle/` 下 5 个文件（iteration-schema / lifecycle / delivery-summary / mcv-deployment / mcv-update）。
- hook 体系零改动；工作区固定路径不变。

## 验证方式与结果摘要
- grep 交叉核对 CHANGELOG 口径在 iteration-schema / mcv-deployment / mcv-update 三处一致；overwrite-only 与"引用不嵌入"落点齐全。
- dogfood 自洽：工作区已覆写为 ITER-0003 无残留、归档/台账/交付三层对齐、本交付文件中产物仅以路径出现（无全文嵌入）。
- 结论：AC1–AC7 全绿，迭代闭合。

## 已知剩余风险 / 延后事项
- `mcv-update.md §3` 结构图仍以"最近一段时间"泛述 CHANGELOG 热数据，与 §5.1 精确口径属泛/精关系、不矛盾，后续重写可一并收口。
- overwrite-only / 引用不嵌入靠规则强制，hook 未校验；机制兜底 linter 列为后续候选。

## 可选引用
- `.ai/iterations/ITER-0003/AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md`
- `Coder/20_Workflow_Lifecycle/iteration-schema.md`
