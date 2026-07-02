> ITER-0024 R4 等待-回收-续跑接线 · active · —

本文件是**当前活跃迭代 ITER-0024**的对象级变更流（ADD/EDIT/DELETE）。绑 AC、文件 + 章节级粒度。格式见 `Coder/20_Workflow_Lifecycle/changelog-schema.md`。

## ADD
- `Coder/20_Workflow_Lifecycle/human-test-bridge.md`：新增等待-回收-续跑闭环协议（§1 定位 / §2 触发条件 / §3 闭环五步 / §4 四态路由表 / §5 无人场次降级 / §6 调用形态 / §7 关系）。(AC1-AC4, AC7)

## EDIT
- `Coder/20_Workflow_Lifecycle/verify-schema.md` §4：编写规则增一条——人测道残余回传闭环见 `human-test-bridge.md`（§4 不移位）。(AC5)
- `Coder/30_Quality_Gate/testing-strategy.md` §3：人测道判定纪律末尾增一句——人测道残余回传走 `human-test-bridge.md`。(AC5)
- `Coder/30_Quality_Gate/correction-contract.md` §3：增关系 bullet——人测 `fail`（经桥回传）进本契约纠错闭环。(AC6)
- `Coder/65_Extension_Dangerous/dangerous-engine.md` §7.4/§8：增句——桥属有人场次工具、无人不起桥走准入闸；补指有人分支走 `human-test-bridge.md`。(AC7)
- `Coder/README.md`：目录结构 + 文件说明注册 `human-test-bridge.md`。(AC8)
- `templates/rule-card.md`：收录一句人测回传闭环口径。(AC8)
- `tools/delivery-selftest/README.md`：把"接进 P5 / 纠错闭环 / 续跑 = R4"改为已完成并指向协议。(AC8)
- `.ai/PROJECT.md`：收口前滚（现行约束 + 架构图按需）。(AC8)

## DELETE
- 无
