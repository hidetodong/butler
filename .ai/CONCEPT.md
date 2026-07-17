# CONCEPT — ITER-0054 · 双宿主部署升级收官

> ⚠️ 危险模式：本迭代由模型自治推进；P2/P3 经强制自审门后自主 ACK。

## 一句话目标

把已经分别可用的 Claude 与 Codex 能力接进同一条安装、首次部署和既有升级链，并用隔离回归证明用户内容不会被覆盖。

## 问题

R1–R3 已分别交付发现入口、8 skills/plugin 和 apply_patch hooks，但用户仍要手动串两套安装步骤，目标项目首次部署只生成 CLAUDE.md，升级协议也只维护 CLAUDE.md。能力已经存在，最后的缺口是“能稳定装上、能生成双入口、以后能安全更新”。

## 目标

- G1：`setup.sh` 保留 Claude 安装行为，同时检测 Codex CLI 并安装/刷新 Butler plugin；无 Codex 时明确跳过、不破坏 Claude 安装。
- G2：提供单一渲染器，从同一 rule-card/template 生成或更新 CLAUDE.md 与 AGENTS.md，保留 user-managed 内容和既有非 Butler 内容。
- G3：MCV 首次部署与 butler-upgrade 都调用同一渲染契约，migration schema 能表达双入口重生成与全局 plugin 刷新。
- G4：隔离 HOME 与隔离目标项目覆盖首次生成、重复执行、老文件追加、用户区保真、版本重戳、Claude hooks 与 Codex plugin 结构回归。
- G5：更新使用说明、兼容矩阵、迁移配方并收口 MILE-0006。

## 非目标

- 不自动替用户确认 hook trust，不绕过 Codex sandbox/审批。
- 不把 plugin 文件复制进每个目标项目；plugin 仍是机器级分发，AGENTS.md 与 `.ai/` 才随项目走。
- 不重写 P1–P5、skills 或 hook 判定算法。
- 不推远端、不合 main、不发布公共 marketplace。

## 方案取舍

选“标准库渲染器 + 协议共同调用”，避免让 MCV 与 upgrade 各自手工拼两份入口。代价是新增一个小型维护脚本和 managed markers；收益是双入口可幂等验证，用户区保护从文字纪律升级为确定性工具行为。
