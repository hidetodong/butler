# Verification Summary

- 覆盖范围：`/butler-upgrade` 新 feature 的 5 个 AC，涉及 1 新文件 + 4 个修改文件，共 6 处改动。
- 总体结论：**全部通过**。butler 规则仓进入"可被目标项目主动升级"的新阶段。

# AC Status

- [x] **U-1** 保护区标记方向（方案 2：`<!-- user-managed -->` 标记用户区）— 已满足
- [x] **U-2** 老项目首次升级策略（方案 b：备份 + 交互 ACK）— 已满足
- [x] **U-3** `.ai/` 升级范围粒度（方案 ii：命名 + schema 字段补齐）— 已满足
- [x] **U-4** 新建 `butler-upgrade.md` 包含完整 8 段结构 — 已满足
- [x] **U-5** `CLAUDE.md.template` 加入保护区标记 — 已满足
- [x] **U-6** `mcv-deployment.md § 3` 部署步骤生成保护区标记 — 已满足
- [x] **U-7** `logic-protocol.md § 4` 注册新命令与语义触发词 — 已满足
- [x] **U-8** `Coder/README.md` 目录结构 + "其中："说明双处注册 — 已满足

# Verification Results

- **U-4**：`butler-upgrade.md` 8 段完整（L9/15/24/45/62/75/104/120：目标 / 触发条件 / 侦察 / 首次升级 / 常规升级 / `.ai/` 结构升级 / 验证与回退 / 边界说明）；frontmatter 2 行；6792 字节。
- **U-5**：`templates/CLAUDE.md.template` L33（`<!-- user-managed -->`）+ L42（`<!-- /user-managed -->`）包裹"项目特定约束"整个章节。
- **U-6**：`mcv-deployment.md § 3` L70 第 4 步明确引用 `<!-- user-managed -->` 保护区，并声明"保护区标记由 `CLAUDE.md.template` 骨架提供，部署时原样保留，作为后续 `butler-upgrade.md` 协议的升级契约起点"。
- **U-7**：`logic-protocol.md § 4` L80 注册 `Butler Upgrade (/butler-upgrade)` 触发项，含语义触发词"升级 butler / 同步到新版 / 同步 butler 规则"；明确标注"非持久 Mode，执行一次后返回 Standard Mode"。
- **U-8**：`Coder/README.md` L55 目录结构加入 `butler-upgrade.md`（位于 `mcv-update.md` 与 `maintenance-boundaries.md` 之间，构成生命周期三阶段的中间环节）；L108 "其中："说明加一行，明确命令入口 `/butler-upgrade`。

# Gate Coverage

- **通用质量门禁**：改动聚焦；6 处可全部映射回 8 条 AC；frontmatter 完整；HTML 注释语法兼容 Markdown 渲染。
- **Active Profiles**：本轮无命中。
- **Tech Plan Alignment**：
  - Design Decisions 1（协议位置 `20_Workflow_Lifecycle/`）→ 实际放置位置 ✅
  - Design Decisions 2（HTML 注释作标记）→ `<!-- user-managed -->` 就位 ✅
  - Design Decisions 3（保护区包裹整个"项目特定约束"章节）→ L33-L42 覆盖整章节 ✅
  - Design Decisions 4（首次升级永远交互 ACK）→ § 4 流程中第 4 步明确强制 ACK ✅
  - Design Decisions 5（`.ai/` 升级不动 CHANGELOG / BUG_LOG / 任务产物）→ § 6.3 显式声明不纳入 ✅
  - Design Decisions 6（注册到 § 4 Semantic Triggers，非独立目录）→ 已在 logic-protocol.md § 4 注册 ✅
- **References Compliance**：N/A（本轮无外部参考资料）。

# Remaining Risks

## 已在协议中显式记录的风险

- **保护区标记识别容错**：§ 3 侦察阶段明确要求 AI 容错识别（忽略空白/大小写），若完全无法识别退化为首次升级流程。风险已嵌入规则。
- **butler 自身 `CLAUDE.md`（仓根）未加保护区标记**：本轮显式不做（避免自指复杂度），作为 follow-up。butler 自身演进由 audit 流程管理，不走 butler-upgrade。
- **协议首次实跑待验证**：本 feature 尚无实际老项目升级 dogfooding。协议文档化按最高清晰度标准，减少首次执行歧义。

## 可选 follow-up（本轮 out of scope）

- butler 仓根 `CLAUDE.md` 也可加 `<!-- user-managed -->` 保护区（但按 § 8 边界说明，butler 自身演进不走 butler-upgrade 协议，所以没必要）。
- 未来新加的重命名场景（例如某个 schema 改名）需要同步更新 `butler-upgrade.md § 6.1` 的"已知重命名清单"。属规则维护日常，不需要独立工单。

# Handoff / Next Step

- 本轮任务已完整闭合。
- 产物链：`.ai/CONCEPT.md` → `.ai/AC_LIST.md` → `.ai/TECH_PLAN.md` → 本文件。
- 交付总结：`deliveries/2026-04-17-feature-butler-upgrade.md`（feature 类型，区别于 audit 清理类）。
- 后续可选：
  - 打新 milestone（如 `v0.1.1-upgrade-protocol`），标志 butler 进入"支持主动升级"阶段。
  - 找一个老项目实际跑一次 `/butler-upgrade`，完成首次 dogfooding。
