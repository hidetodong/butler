# CONCEPT — ITER-0024

> 分流：完整路径 | 命中升级信号：新增规则文件（P5 子协议）、跨文件接线（verify / testing / correction / dangerous）、关键路径（人测闭环收口判定）| 2026-07-02 | MILE-0002 R4 | ⚠️ 危险模式（P2 起自审门自 ACK；P4 自治）

## 一句话

R3 造好了桥（能起、能测、能回传、能自退），但桥的**下游还没接**——butler 不知道何时起桥、起完怎么等、结果回来怎么按四态续跑。R4 把桥接进 SOP：新增一份**等待-回收-续跑闭环协议**（`human-test-bridge.md`），定清"P5 存在人测残余 + 有人在场 → 生成 manifest → `run_in_background` 起桥 → 阻塞等进程退出 → 读 `results.json` → 四态路由（通过=收口 / 未通过=纠错 / 跳过=N/A / 延后=入账不阻塞）"，并把它接进 P5（verify-schema / testing-strategy）、纠错（correction-contract）、无人降级（dangerous §7.4），补上 R1/R2/R3 一直缺的最后一环：**结论真正流回 butler、闭环真正合上**。

## 背景与判断

- 里程碑归属：MILE-0002 路线项 **R4**（扁平原子）。承 R1（分道）R2（置信）R3（桥体）——前三项把"哪些要人测 / 多大把握 / 人测完怎么回传"都备齐了，唯独**回传后 butler 怎么接**还悬空。
- 缺口：R3 交付时明说"把桥接进 P5 / 纠错闭环、后台等待续跑是 R4"（见 `tools/delivery-selftest/README.md` 及其交付）。桥能自退、能写 `results.json`，但没有规则告诉 butler 何时起、怎么等、四态怎么分派。
- 本迭代**只接线 + 定协议 + 机械跑通闭环**；部署 / 使用文档注册（mcv-deployment / HUMAN_GUIDE）+ 真实项目 dogfood = R5。
- 与 R2 无人处置的分工要厘清：桥是**有人场次**工具（弹页面等人勾）；`/dangerous` **无人**场次桥会永久阻塞，故无人场次**不起桥**、走 `dangerous-engine §7.4` 依赖感知准入。R4 要把这条"有人起桥 / 无人走准入闸"的岔口写死，两边一致、不矛盾。

## 目标（Goal）

- G1：**闭环协议成文**——新增 `Coder/20_Workflow_Lifecycle/human-test-bridge.md`，定义触发条件（P5 存在 `human·待人` 残余 + 有人在场）、等待-回收-续跑五步（生成 manifest → `run_in_background` 起桥 → 阻塞等进程退出 → 读 `results.json` → 四态路由回填）、调用形态（butler 传 manifest 路径调 butler 驻留工具、不拷副本）。
- G2：**四态路由口径**——`pass`=计入收口 / `fail`=进 `correction-contract` 纠错（备注当线索）/ `defer`=入欠债账不阻塞收口 / `skip`=记 N/A；结论回填 `VERIFY_REPORT.md`。与工具 README 路由表逐条一致。
- G3：**P5 接线**——`verify-schema.md`（人测道回填）+ `testing-strategy.md §3`（人测道界定）指向桥协议为回传通道。
- G4：**纠错接线**——`correction-contract.md` 明确人测 `fail`（经桥回传）进本契约纠错闭环。
- G5：**无人降级接线**——`dangerous-engine.md §7.4/§8` 厘清"桥属有人场次、无人不起桥走准入闸"，与桥协议双向一致。
- G6：**注册 + 前滚**——`Coder/README.md` 目录 + 读序注册新文件；工具 `README.md` 把"接线=R4"改为已完成并指向协议；`rule-card.md` 收录一句；`.ai/PROJECT.md` 前滚。
- G7：**机械跑通闭环**——真跑一遍 butler 侧回路：样例 manifest → `run_in_background` 起 `bridge.js`（`--no-open`）→ 程序化 POST 四态 → 后台进程 exit 0 → 读 `results.json` 解析 → 演示四态路由分派，证明协议可执行（非仅规则正文）。

## 约束（Constraints）

- **接线不造新工具**：桥体 R3 已成，R4 只写规则协议 + 复用现有 `bridge.js`，不改工具代码（若机械验证暴露桥体缺陷，另记欠债 / 视严重度决定，不在本迭代顺手改契约）。
- **有人 / 无人岔口清晰**：桥只在有人场次跑；无人场次（`/dangerous`）不起桥，走 §7.4。协议与 dangerous-engine 不得互相矛盾。
- **文件名互引**：接线一律用文件名引用（不写脆弱的 §行号），符合本仓写作约定。
- 只接线、定协议、机械验证；**不写**部署注册文档（mcv-deployment / HUMAN_GUIDE）、**不做**真实项目 dogfood（R5）。
- 不改 P1-P5 状态机、四件套脊柱、hook、四态机器码。

## 影响范围（Impact Scope）

- 新增：`Coder/20_Workflow_Lifecycle/human-test-bridge.md`（等待-回收-续跑闭环协议 SSOT）。
- 改（接线）：`verify-schema.md`、`testing-strategy.md`、`correction-contract.md`、`dangerous-engine.md`、`Coder/README.md`、`templates/rule-card.md`、`tools/delivery-selftest/README.md`、`.ai/PROJECT.md`。
- 不影响：桥工具代码（`bridge.js` / `render.js`）、hook、四件套 schema、状态机、R5 部署 / dogfood。

## 项目类型与 Profiles

butler 规则仓（编辑规则本身）。R4 主体是规则协议（新增一份 20_ 层子协议 + 多处接线），叠一次机械验证（真跑桥回路）。无 active profile；验证遵循 R1 自动化优先——闭环用真跑证明（`auto·可靠`），不停在"读规则存在"。

## 待澄清（Open Questions）

- Q1：新协议落 `20_Workflow_Lifecycle/` 还是 `30_Quality_Gate/`？倾向 20_——它是 P5 生命周期子流程（等待-回收-续跑），非质量门禁判据。（P3 定）
- Q2：文件名 `human-test-bridge.md` vs `human-test-loop.md`？倾向 `human-test-bridge.md`——与工具"交付自测桥"呼应、涵盖回环。（P3 定）
- Q3：manifest / results 落点？倾向 `.ai/human-test/`（manifest.json + results.json），与四件套隔离、可 gitignore。（P3 定）
- Q4：机械验证用 `curl` 还是 node `http` 客户端 POST？倾向复用桥自带 `test/` 思路或 `curl`，只为证明 run_in_background→exit→read 回路，不新增测试文件。（P3 定）
