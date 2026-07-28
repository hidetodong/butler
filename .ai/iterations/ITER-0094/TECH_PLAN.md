<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0094

方案状态: pass
方案审查日期: 2026-07-28
方案审查方式: dangerous-self-review

> ⚠️ 危险模式：本方案由模型完成 Plan Admission 后自主 ACK，未经用户确认（ITER-0094，2026-07-28）

## Design Decisions

- `config.py` 增加纯函数 legacy parser、兼容 `resolve` 和迁移计划。迁移计划只返回目标 bytes，不自行做双文件写入；这样升级器可复用既有事务，不另造第二套 journal。
- legacy 分段只认 H1 heading。Active Profiles 仅接受明确“无”或单值 profile 标识；开关只接受 on/off。旧 Review Policy 仅作为 `independent_review` 回退，任何歧义都拒绝。
- JSON 存在时必须先通过 R1 严格校验，并作为返回真源；仍存在 legacy 配置时逐字段比较，把冲突字段列入结构化输出。JSON 不存在才回退 Markdown。
- 升级器新增无参数 `migrate_config` action 和固定前置条件，动态加载 project-config 内核生成两项 Change；两文件继续由 upgrade backup/restore/journal 原子编排。
- R2 更新部署与 local constraints 规则，但不改当前消费端。manifest 的真实版本 action 留给 R3 与版本接线一起登记。

## Failure Paths

- legacy 段含无法确定的 profile/开关值、重复 heading 或坏 UTF-8：退出 2，零写。
- 已有 JSON 损坏或与 legacy 冲突：拒绝迁移，不删除 Markdown 段。
- `.ai/butler.config.json`、`local-constraints.md` 或父路径为 symlink/非普通文件：升级器所有权校验拒绝。
- apply 中任一文件写入失败：既有事务恢复两文件，journal 留下 `failed-restored`。

## Test Strategy

- 扩展 project-config 专项覆盖解析、优先级、冲突和 bytes-preserving strip；扩展 upgrader unittest 覆盖 action contract、plan/apply/幂等与注入失败。
- 完成后运行两组专项、artifact/state/handoff 检查、完整 CI 与 diff check。

## References Compliance

- N/A
