> 分流: 完整 | 命中升级信号: 跨文件·流程语义·新工具·持久状态 | 2026-07-22

# 一句话
- 把 handoff 从“AI 记得时手写的一段话”改成由当前权威状态确定性生成的入口。状态一变，旧 handoff 会被识别为陈旧；下次读取前必须拒绝旧内容并从真源重建。

# Goal
- 建立跨宿主可用的 handoff 生成、检查与恢复闭环，解决经常未按时落盘和内容不可信两个实际问题。

# Current Understanding
- `.ai/02_SESSION_HANDOFF.md` 目前只有格式规范和人工维护时机，没有可执行生成器、来源指纹或陈旧判定。
- AI 直接写 handoff 会临场选择段落和摘要内容；即使迭代号没变，task-state、阶段、AC、方案、验证或里程碑状态变化后也可能继续沿用旧内容。
- handoff 不应成为新的权威状态。它应从 task-state、迭代/里程碑当前指针、当前阶段产物和必要的项目前沿信息读取一个有界状态快照，再渲染为固定结构。
- 宿主不一定提供可靠的 stop/compact hook，因此不能承诺捕获尚未落入任何项目状态文件的纯对话内容。可实现的可靠边界是：权威状态变化后可检查陈旧；显式暂停/compact/交接时同步；冷启动消费前强制检查并自愈。

# Constraints
- 保持 `.ai/02_SESSION_HANDOFF.md` 为人类可读入口，不把完整历史、日志或四件套全文复制进去。
- handoff 正文完全由工具生成；人工补充先写入现有权威状态，不允许直接编辑生成区冒充真源。
- 生成和检查默认只读输入；更新 handoff 必须原子写入、可重复执行、相同状态产生相同结果。
- 指纹只覆盖决定 handoff 语义的有界来源，不把整个仓库或全部历史纳入计算。
- Claude、Codex、Pi 共享同一 Python 真源；宿主层只负责触发或提醒。
- 本迭代不提前实现五位编号和双台账分片；读取层须隔离文件布局，给 R2/R3 留稳定适配边界。

# Impact Scope
- 影响：handoff/context persistence 规则、维护边界、冷启动读序、状态审计、部署/升级、共享 hook 或宿主入口、一个新的确定性工具及其测试。
- 可能涉及：`.ai/02_SESSION_HANDOFF.md`、`.ai/task-state.md`、当前台账与四件套的读取适配。
- 不影响：历史 handoff 归档（不存在此类真源）、PRD/inbox/workspace scope 业务语义、五件套固定化候办、MILE-0010 R2–R4 的具体实现。

# Project Type / Active Profiles
- Markdown 规则仓 + Python/Bash 工具 + Claude/Codex/Pi 宿主适配。
- 无 Domain / Stack Profile，仅按通用 SOP、危险模式自审和完整 P5 审查推进。

# Open Questions
- 无阻塞问题。设计阶段需决定指纹 sidecar/内嵌位置、固定结构、状态快照字段和各触发点的 fail-open/fail-closed 边界。

