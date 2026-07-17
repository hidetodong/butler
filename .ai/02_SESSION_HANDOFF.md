# Session Handoff

## 任务断点

危险模式会话正在连续推进 MILE-0006。R2 / ITER-0052 已收口为 v2.13.0；应立即开 R3 / ITER-0053，不等待用户 ACK。

## 已交付

- `plugins/butler/` + `.agents/skills/` 8 skills 单一实体源。
- `scripts/install-codex-plugin.sh` 与 `verify-codex-workflows.sh`。
- 本机 `butler@personal` 已安装，当前缓存版本带 `2.13.0+codex.*`。

## R3 边界

- 只做 Codex PreToolUse/PostToolUse、`apply_patch` 输入适配、共享规则复用与端到端拒绝/提醒验证。
- 不做 R4 的 setup、MCV、目标项目双入口部署/升级和里程碑收官。
- 注意：最新 manual 支持 plugin hooks，但当前本机 plugin validator 拒绝 manifest `hooks` 字段；必须以实际 CLI 可加载配置为准并如实记录差异。

## 状态指针

- `.ai/MILESTONE.md`
- `.ai/project/frontier.md`
- `.ai/RUN_LOG.md`
