> 分流: 完整 | 命中升级信号: 契约变更、状态机、跨入口影响、多文件改动 | 2026-07-22

# 一句话

- `origin/` 目前只是“放文件给 /milestone 读”的目录，系统回答不了某份材料是否处理过、后来变了没有、派生出了什么。R3 建一份只存回执和关系、不复制原文的 `.ai/INBOX.md`，让文件、对话和外部文档都有稳定来源身份与处理状态。

# Goal

- 定义可恢复、幂等、尊重用户原稿所有权的需求收件箱数据契约。

# Current Understanding

- 来源身份不能用内容 hash 代替：同一文件改版后 hash 会变，但仍是同一来源；需要稳定 `source_id` + 当前/已处理双指纹。
- 同内容从两个位置进入可能是重复候选，但不能自动合并来源；相反，同一 locator 内容变化应保留 source_id 并置 `source-changed`。
- `.ai/INBOX.md` 是处理回执，不是原文仓库；它只存定位、摘要、hash、状态和派生指针。
- 一份原稿可派生多个 PRD/里程碑/脑暴产物，多个来源也可共同支撑一个产物，因此关系必须是独立多对多表。

# Constraints

- `origin/` 用户自管，AI 永远只读：不新增、改写、移动、重命名、归档或删除其中内容。
- 收件箱可选；对话快速路径和直接 `/milestone` 继续合法。
- R3 只定义数据契约，不实现扫描、分类、确认和路由命令；R4 承接行为。
- ledger 不复制完整原文、凭据、长摘要或敏感内容；只保留最小回执。
- 内容指纹采用 SHA-256 且必须定义输入字节，不能用 mtime/大小冒充。

# Impact Scope

- 新增 `Coder/40_Context_Management/inbox-schema.md`。
- 更新 `mcv-deployment.md`、`Coder/README.md` 和 HUMAN_GUIDE 的 origin 定位指针。
- 新增结构合同测试；更新本迭代状态、证据与交付。
- 不创建/修改 `origin/`，不实现命令、registry 或 hook。

# Project Type / Active Profiles

- Markdown 规则仓 + Python/Bash 工具 + Claude/Codex/Pi 适配。
- 未命中领域 profile，仅按通用 SOP；危险模式 ON。

# Open Questions

- R4 如何交互确认批量路由、R7 如何复用 receipt，留给各自迭代；不阻塞 R3 数据层。
