<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0112 变更流

> 退役项目知识文件夹与折叠机制（MILE-0016 R1） · closed · 2026-08-18

## ADD

- `.ai/debt.md`「`/butler:upgrade` 从未在真实已部署项目上跑过」：自 `.ai/project/architecture.md` 成熟度段迁出的唯一无真源欠债，全仓别处不存在 → AC2

## EDIT

- `.ai/project/debt.md` → `.ai/debt.md`：`git mv` 迁位，正文除新增上述一条外未改 → AC1

## DELETE

- `.ai/project/00_INDEX.md`：知识文件夹自身的地图与主题登记表，随文件夹机制退役 → AC1
- `.ai/project/identity.md`：定位 / 目的 / 使用者 / 边界，全文指向仓根 `CLAUDE.md` / `README.md` / `HUMAN_GUIDE.md` / `Coder/README.md` / `CONTRIBUTING.md` / `SECURITY.md` / `LICENSE` → AC1
- `.ai/project/constraints.md`：9 条现行约束，逐条已在真源存在——写作面向 AC 与 audience 标注在仓根 `CLAUDE.md`、注册即真源在 `Coder/README.md`、兼容诚实在 `docs/codex-compatibility.md §87`、开源治理在 `README.md` / `CONTRIBUTING.md` / `SECURITY.md`、高风险 skill 显式在 `workflows/registry.json`、semver 与提交规约在 `versioning-schema.md §5/§6`、测试自动化在 `testing-strategy.md §3`、最小实现在 `implementation-discipline.md`、无人残余在 `dangerous-engine §7.4`；仅「新增知识主题必须在 `00_INDEX.md` 登记」一条随机制消亡 → AC1/AC2
- `.ai/project/architecture.md`：模块地图段与 `Coder/README.md`「目录结构」「规则目录说明」重复（该文件自己开篇即声明"此处不抄"）；决策驻留 Modules 段在 `Coder/README.md` 第 174–177 行有同等或更详细描述；成熟度段落后 9 个里程碑（只写到 MILE-0007，当前 MILE-0016）已确认失真；唯一无真源的「`/butler:upgrade` 从未真跑」已迁入 `.ai/debt.md` → AC1/AC2
- `.ai/project/capabilities.md`：22 个小节逐条核查，全部可弃——开源协作 / 项目配置 / TDD 配对 / 五件套产物链 / handoff 与台账 / 旁路回执 / 双宿主适配 / Codex 工作流 hooks / 工作流注册 / Decision Map R1–R5 五节 / 持续验证 / 可执行升级 / P1–P5 SOP / 命令表 / 部署维护 / 驻留工具 / 领域治理接线 / 帮手，真源分别为对应 `Coder/` 规则、`tools/*/README.md`、`workflows/registry.json`、`docs/workflows.md`、`docs/codex-compatibility.md`、`migrations/manifest.json` 与各驻留工具本身；`Coder/README.md` 第 172–217 行的驻留工具描述比本文件更详；「远端 required check 未启用」这条诚实声明在 `HUMAN_GUIDE.md §119`、`docs/codex-compatibility.md §126`、`README.md §354` 三处均有且更精确 → AC1/AC2
- `.ai/project/fold-state.json`：折叠回执，随折叠机制退役；历史迭代的折叠参与记录与 hash 自此不可机器验证 → AC1/AC10
- `Coder/62_Extension_Agents/knowledge-fold.md`：更新说明帮手，其唯一职责是把迭代 delta 折进 `.ai/project/` → AC3
- `Coder/62_Extension_Agents/drift-check.md`：查过时帮手，其唯一职责是查知识文件夹漂移 → AC3
- `Coder/40_Context_Management/project-digest-schema.md`：知识文件夹结构契约，同时拥有文件夹态与单文件 `.ai/PROJECT.md` legacy 态，两态一并停支持 → AC5
- **保留（本轮不删，留待 R3）** `.ai/project/invariants.md`：47 条不变量、其中 38 条带 `*为什么*` 理由，纯追加式维护、无漂移、别处无真源。
- **保留（本轮不删，留待 R3）** `.ai/project/frontier.md`：每次收口整体覆写，覆盖至 MILE-0015、一直准确。
- **保留（不属本机制）** `.ai/project/workspaces.md`（部署项目侧，butler 仓无此文件）：workspace-scope 的项目工作区地图，由 PreToolUse hook 实际消费，与知识文件夹机制无关。
