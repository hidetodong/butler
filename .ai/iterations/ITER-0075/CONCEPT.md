> 分流: 完整 | 命中升级信号: 需求有歧义、多文件改动、契约变更、跨模块影响、设计取舍 | 2026-07-22

# 一句话

- 现有 PRD 文件夹只能代表一份持续改版的项目规格，第二份独立需求进入后会与第一份的模块、版本和归档混在一起。R1 先把“项目里有多份需求、每份需求各自有身份和版本”定成稳定契约，后续收件箱、引用、更新和门禁才能对准同一个对象。

# Goal

- 定义项目级 PRD 需求集合、日期化稳定 `prd_id`、单需求内部目录与“全新需求 / 已有需求新版”的身份判定边界。

# Current Understanding

- 当前 `.ai/references/prd/00_INDEX.md` 同时承担“这是哪份 PRD”和“这份 PRD 有哪些模块”，根目录的 `.archive/vN/` 也只能服务一个版本序列。
- 新模型需要两层地图：项目级总索引回答“有哪些需求”，`prd/<prd_id>/00_INDEX.md` 回答“这份需求有哪些模块”；每份需求拥有独立 `.archive/vN/`。
- `prd_id` 的日期表示需求首次进入当前项目 Butler 体系的日期，不是源文档创建日、版本发布日期或最近更新时间；标题、slug 文案与版本变化都不能改掉已分配身份。
- “已有需求新版”必须先命中一个既有 `prd_id`；只有证据不足或互相冲突时才停下来确认，不能为了省事新建重复需求，也不能把不同需求硬并到旧目录。

# Constraints

- R1 只定声明式结构与身份契约；不改 `prd-split`、`prd-update`、AC/TECH_PLAN/VERIFY 引用格式、命令、迁移器或 hook，这些分别由 R5–R8 承接。
- 继续保留 `.ai/references/` 的非 PRD 扁平资料，不把小任务或无 PRD 项目强制纳入需求集合。
- 稳定身份必须可由人读、可机械校验，并在跨版本、改标题和目录搬迁场景保持不变。
- 旧单 PRD 结构在迁移能力落地前仍是 legacy 可读态；R1 不静默搬迁任何项目数据。
- 危险模式的自主 ACK 不降低自审要求；写入范围仅限 Butler 仓。

# Impact Scope

- 修改 `Coder/40_Context_Management/references-schema.md`，把 PRD 知识文件夹契约升级为项目级需求集合 + 单需求子目录。
- 更新 `Coder/README.md` 的导航摘要，补一份聚焦结构和身份不变量的标准库测试。
- 更新本迭代 `.ai/` 状态、证据、归档与交付。
- 不修改 `prd-split.md`、`prd-update.md`、P1–P5 schema、双宿主命令、registry、hook、migration 与目标项目模板。

# Project Type / Active Profiles

- Markdown 规则仓 + Python/Bash 工具 + Claude/Codex 双宿主适配。
- 未命中领域 profile，仅按通用 SOP；危险模式 ON。

# Open Questions

- 首切与改版动作如何消费新 `prd_id`、旧路径如何迁移、多份 PRD 如何在 AC 中分别钉版，已明确留给 R5–R7，不阻塞 R1 契约落地。
