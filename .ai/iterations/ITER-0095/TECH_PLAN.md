<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0095

方案状态: pass
方案审查日期: 2026-07-28
方案审查方式: dangerous-self-review

> ⚠️ 危险模式：本方案由模型完成 Plan Admission 后自主 ACK，未经用户确认（ITER-0095，2026-07-28）

## Design Decisions

- 把 `python3 "$BUTLER_PATH/tools/project-config/config.py" resolve --project-root "$PROJECT_ROOT"` 定为所有活入口的唯一读取协议。调用方只消费 stdout JSON；非零退出、`status!=ok` 或 JSON 损坏均 fail-closed，`legacy_conflicts` 必须显式展示。
- 把 `set <field> <value>` 定为三个项目布尔开关与 profiles 的唯一回写协议。命令先 resolve；只有 `source=config` 才允许 set，legacy/missing 返回升级或初始化指引，禁止直接改 Markdown。
- 新增标准库 unittest 扫描受控 consumer matrix，既断言必须出现的命令/语义，也禁止 `.ai/local-constraints.md` 机器开关旧指引；纳入完整 CI，避免未来文档漂移。
- 本仓 dogfood 用 `plan_migration` 的真实投影作为依据，但通过 `apply_patch` 同步落 JSON 与收窄 Markdown，保留危险模式 true；写后以 resolve 和专项测试验证。
- 先增加未来 `3.2.0 -> 3.3.0` migration recipe/manifest，使 upgrader 专项可验证真实 action；R3/里程碑关闭、交付文件存在后，再把 VERSION、插件 manifest、README badge、根 CHANGELOG 一次对齐并跑关闭态 CI。

## Failure Paths

- `resolve` 非零、坏 JSON、未知 schema 或冲突：消费端停止动作并回报诊断；危险模式按 off 处理，但不得把该推断写回配置。
- `set` 遇到 source=legacy/missing：零写并要求 `/butler:upgrade` 或 `/butler:init`；不自动跨两文件迁移。
- 本仓迁移后值不一致或 Markdown 残留机器段：专项失败，停在 P4 修复，不进入发布元数据。
- 未来 migration action 顺序或版本一致性失败：upgrader/发布审计阻断；不以手工绕过宣称发布成功。
- 无 tag/远端授权：最终版本只可称本地 UNRELEASED 候选，交付中保留该限制。

## Test Strategy

- 定点：project-config unittest、upgrader unittest、consumer contract unittest、真实本仓 resolve/迁移检查。
- 集成：命令/skill registry、artifact contract、migration manifest/version consistency、Markdown links。
- 收口：`bash scripts/verify-ci.sh`、Goal/state auditor、evidence integrity、`git diff --check`；版本元数据对齐后再跑一次关闭态完整 CI。

## References Compliance

- 只改 Butler 仓授权根内的规则、命令、skills、工具测试、当前 `.ai/` 状态与发布材料；历史迭代/旧 migration 正文不追溯改写。
