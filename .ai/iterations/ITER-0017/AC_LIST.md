---
状态: ack-frozen
ACK 日期: 2026-06-30
---

> ITER-0017（MILE-0001 R1）。P2 已由用户显式 ACK 冻结（2026-06-30），验收范围锁定，进入 P3。

# Goal

- 新增 `.ai/PROJECT.md` 常驻项目摘要（状态取向全貌）+ 其 schema + 接入冷启动读序 + 纳入收口前滚维护 + 部署种子，补"冷启动只有变更流、没有全貌"的缺口。目标背景见 CONCEPT，不重述。

# In Scope

- 定义 `.ai/PROJECT.md` 产物与字段（状态取向、有界、指针化）。
- 新增 schema 文件，定义字段 / 维护触发 / 边界分工。
- 冷启动读序接线（README + context-persistence）。
- 把"前滚 PROJECT.md"加进迭代 / 里程碑收口步。
- mcv-deployment 部署创建种子；butler 自身落一份种子 dogfood。
- 评估并落实 rule-card / 迁移配方联动。

# Out of Scope

- 收口的执行门禁 / hook 规则 / 一致性探针 / 原子收口命令 → 归 R2 / ITER-0018。
- 不改四件套字段结构、AC 脊柱、P1-P5 状态机。
- 不强制 butler 仓 dogfood 运行自己的 hook。

# Acceptance Checklist

- [ ] AC1: 新增 schema 文件，定义 `.ai/PROJECT.md` 必填字段（至少：目的、架构/模块地图、关键长期决策与不变量[带为什么]、现行约束、已知长期欠债、指针），并明确它是状态取向（写"现在是什么"，不是变更日志）。
- [ ] AC2: schema 明确 PROJECT.md 有界（token 上限）+ 指针化（深内容指向代码 / deliveries / architecture 文档，不内嵌）；写作口径引用 `artifact-style.md`，不另定义一套。
- [ ] AC3: schema 明确 PROJECT.md 与 ITERATIONS（变更流）/ 02_SESSION_HANDOFF（瞬时断点）/ MILESTONE（版本范围）四者分工边界，无职责重叠歧义。
- [ ] AC4: 冷启动读序接线——README 读取顺序 + context-persistence 冷启动章节明确 PROJECT.md 为冷启动第一读（是什么/到哪了 → 时间线 → 断点 → 代码）。
- [ ] AC5: README 目录结构注册新 schema 文件（消除隐式依赖，合本仓 CLAUDE.md 约束 3）。
- [ ] AC6: 收口前滚——iteration-schema §5.5（及 milestone §7.4 如适用）新增一步：收口时按需把本迭代的长期决策/欠债折进 PROJECT.md；明确"多数迭代只动 0-2 行或不动"以控维护成本。
- [ ] AC7: 部署落地——mcv-deployment 部署步骤创建 PROJECT.md 种子（含最小骨架）；并定下迁移配方对已部署项目的补建口径。
- [ ] AC8: dogfood——butler 仓自身落一份 `.ai/PROJECT.md` 种子，内容真实反映 butler 当前全貌（验证 schema 可用、非空骨架）。
- [ ] AC9: rule-card 联动评估——判定 PROJECT.md 是否进 rule-card 强制产物集并落实结论（进则补、不进则记录理由），与"不做存在性硬门禁"决策一致。
- [ ] AC10: 不破坏不变量——四件套字段结构未改、AC 脊柱未动、P1-P5 状态机未动、hook 代码未碰；本仓 CLAUDE.md 五约束自检通过。

# Verification Method

- AC1 / AC2 / AC3: 读新 schema，核对字段齐全 + 状态取向声明 + 有界指针化 + 四产物分工边界。
- AC4: 读 README 读序 + context-persistence 冷启动章节，确认 PROJECT.md 第一读。
- AC5: 读 README 目录结构，确认新 schema 已注册。
- AC6: 读 iteration-schema §5.5 / milestone §7.4，确认前滚步 + 维护成本声明。
- AC7: 读 mcv-deployment，确认种子创建步 + 迁移补建口径。
- AC8: 查 `.ai/PROJECT.md` 存在且非空、内容贴合 butler 现状。
- AC9: grep rule-card，确认联动结论已落实。
- AC10: git diff 确认未碰四件套字段 / hook / 状态机；本仓五约束自检。

# Open Questions / Risks

- 命名 / token 上限 / 是否进硬门禁 / 迁移时机——见 CONCEPT Open Questions，P3 定。
- 风险：PROJECT.md 与 architecture-overview / 项目 README 内容重叠 → 靠 AC3 分工边界 + 指针化化解（PROJECT.md 只做 AI 维护的状态脊柱，深内容指针引用）。
- 风险：维护成本累积 → 靠"按需前滚、多数 0-2 行"+ R2 探针兜底。
