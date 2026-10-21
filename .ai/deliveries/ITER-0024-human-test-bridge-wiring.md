# 等待-回收-续跑接线：交付自测桥接进 P5 闭环（新增 human-test-bridge 协议 + 四态路由 + 机械跑通）

> ITER-0024 · 迭代交付（小版本）· 收口 2026-07-02 · MILE-0002 R4 · ⚠️ 危险模式（P2/P3 自审门 self-ACK，P4 自治 + P5 独立复核）

## 本次交付目标

- MILE-0002 第四个路线项 R4（扁平原子）。承 R1（分道）R2（置信）R3（桥体）——前三项备齐了"哪些要人测 / 多大把握 / 人测完怎么回传"，唯独**回传后 butler 怎么接**还悬空。
- 缺口：R3 的桥能自退、能写 `results.json`，但没有规则告诉 butler 何时起桥、起完怎么等、四态怎么分派。
- 目标：新增一份**等待-回收-续跑闭环协议**，把桥接进 P5 / 纠错 / 无人降级，定四态路由，并**机械跑通一遍**证明协议可执行——补上 R1-R3 一直缺的最后一环：结论真正流回 butler、闭环真正合上。

## 已完成内容

- **新增** `Coder/20_Workflow_Lifecycle/human-test-bridge.md`（等待-回收-续跑闭环协议 SSOT，§1-§7）：
  - §2 触发条件：P5 存在 `human·待人` 残余 **且** 有人在场（两条件与）。
  - §3 闭环五步：生成 manifest → `run_in_background` 起桥 → 阻塞等桥进程自退 → 读 `results.json` → 四态路由回填 `VERIFY_REPORT`；异常退出（无 results.json）不假绿、诚实停。
  - §4 四态路由表：`pass`=收口 / `fail`=进 `correction-contract` 纠错 / `defer`=入账不阻塞 / `skip`=N/A，**逐条镜像工具 README**、补 SOP 侧落点。
  - §5 无人降级：`/dangerous` 无人不起桥（否则永久阻塞）、走 `dangerous §7.4` 准入闸。
  - §6 调用形态：butler 传 manifest 路径调驻留工具、不拷副本；部署登记 defer R5。
- **接线**（增量追加、文件名互引、不 renumber）：`verify-schema.md §4`（人测道回传闭环）、`testing-strategy.md §3`（人测道残余走桥协议）、`correction-contract.md §3`（人测 `fail` 进纠错闭环）、`dangerous-engine.md §7.4/§8`（有人起桥 / 无人走准入闸，与协议双向锁死）。
- **注册 + 前滚**：`Coder/README.md`（目录 + 文件说明）、`templates/rule-card.md`（一句口径）、`tools/delivery-selftest/README.md`（R4 已完成 + 指向协议）、`.ai/PROJECT.md`（现行约束 + 架构图前滚）。

## 关键变更 / 用户可感知变化

- 人测闭环**真正合上**：P5 遇到人测残余（有人场次）→ 生成清单 → 后台起桥弹页面 → 人勾四态 → 桥自退 → butler 读回 → 四态各自续跑。R1-R3 的通道到 R4 才接通下游。
- **一处岔口写死**：有人 → 起桥走四态路由；无人（`/dangerous`）→ 不起桥走 `§7.4` 准入闸。两条路互斥、双向一致，杜绝"无人下误起桥永久阻塞"。
- **四态各有确定动作**：通过收口 / 未通过进纠错 / 延后入账不阻塞 / 跳过记 N/A——人无论选哪个 butler 都能续跑，且红线绝不假绿（无 `results.json` 不算通过）。
- 不造新工具：R4 只写规则协议 + 复用 R3 桥；桥代码零改动。

## 高层影响范围

- 新增：`Coder/20_Workflow_Lifecycle/human-test-bridge.md`。
- 改（接线）：`verify-schema.md` / `testing-strategy.md` / `correction-contract.md` / `dangerous-engine.md` / `Coder/README.md` / `templates/rule-card.md` / `tools/delivery-selftest/README.md` / `.ai/PROJECT.md`。
- 没碰：桥工具代码（`bridge.js` / `render.js`）、hook、四件套 schema、状态机、四态机器码、R5 部署 / dogfood。

## 验证方式与结果摘要

- 9 条 AC 全满足，全 `auto·可靠`。主体为规则协议接线（读规则确认存在且自洽），叠一条机械验证真跑桥回路。
- **机械跑通闭环**（AC9）：后台起桥 → `GET /health` 200 → `POST /submit` 四态 → 桥进程 **exit 0**（自退）→ 读 `results.json` summary `{pass:1,fail:1,defer:1,skip:1}` → node 路由脚本按协议表分派四态各归位、ASSERT PASS。真实 butler 以 `run_in_background` 退出通知替代 `wait`，机制等价。
- **一致性五不变量全 PASS**：两处四态表逐条一致 / 有人无人双向一致不死锁 / verify §4 未移位（changelog-schema §4 引用不破）/ 全增量无悬挂引用 / 单一来源不重抄。
- **危险模式 P5 §7.3 独立复核**：fresh-context 子 agent 实读规则 + 独立复跑 AC9 + 对抗探测（假绿 / 路由完整性 / 崩溃无 results.json / 越界 R5）。结论：**9/9 confirm（AC8 前滚收口步④补齐后）、0 Must Fix、1 Should Fix（已补）、1 Nit**；无假绿路径、无越界 R5。

## 已知剩余风险 / 延后事项

- `run_in_background` 的"进程退出即续跑"依赖 harness 后台能力；本 harness 已机械证明可行，跨 harness 后台语义差异为已知风险（协议描述机制、不绑定具体 harness）。
- 机械验证是程序化 POST（模拟人提交），非真人点页面；真人交互层由 R3 Playwright 弱档覆盖，本迭代不重复。
- 部署路径解析 / `mcv-deployment` / `HUMAN_GUIDE` 登记 + 真实项目 dogfood + 长程无人准入闸落地留 **R5**。本迭代只到"协议成文 + 接线 + 机械跑通"。

## 引用

- 归档四件套 + 切片：`.ai/iterations/ITER-0024/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 新增协议：`Coder/20_Workflow_Lifecycle/human-test-bridge.md`
- 桥体契约真源：`tools/delivery-selftest/README.md`
- 接线：`verify-schema.md` / `testing-strategy.md` / `correction-contract.md` / `dangerous-engine.md` / `Coder/README.md` / `templates/rule-card.md`；前滚：`.ai/PROJECT.md`
- 危险模式审计：`.ai/RUN_LOG.md`（ITER-0024 段）
