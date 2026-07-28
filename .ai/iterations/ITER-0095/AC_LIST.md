---
状态: ack-frozen
ACK 日期: 2026-07-28
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0095

> ⚠️ 危险模式：本验收清单由模型完成反证、自洽性与可验证性审查后自主 ACK，未经用户确认（ITER-0095，2026-07-28）

修订记录: 2026-07-28 · P5 明确 AC7 验证的是本地 UNRELEASED 发布候选及既定交付路径；迭代/里程碑实体交付属于通过 Goal 后的收口输出，不能反向作为完成资格前置。

## Goal

- 让 Butler 所有活消费端共享 `.ai/butler.config.json` 的确定性读取/回写语义，并以可升级、可验证、未冒充已发布的 v3.3.0 候选收口 MILE-0013。

## In Scope

- `resolve/set` 消费合同、危险/复核/偏好/进度与双宿主接线、当前仓迁移、结构测试、v3.3.0 migration 与发布元数据、完整关闭态验证。

## Out of Scope

- 不删除 legacy 回退解析，不改变外置偏好 consent/data，不迁移任务状态，不提交、打 tag、推送或执行目标项目批量升级。

## Acceptance Checklist

- [ ] AC1: 会话冷启动、危险模式、独立复核、偏好和 Active Profiles 的活规则统一调用 project-config `resolve`，不得自行解析 Markdown；坏 JSON fail-closed，危险模式绝不因错误而开启。
- [ ] AC2: 危险、独立复核和项目偏好回写统一调用 project-config `set` 并只写 JSON；当 `source` 不是 `config` 时明确要求先 init/upgrade，不回写 legacy Markdown、不静默用默认值覆盖旧值。
- [ ] AC3: `/butler:progress` 与两宿主 progress skill/command 使用同一解析结果展示 source、冲突和三开关/profile；Butler 版本改从入口 stamp 或 VERSION 读取，不再假定 local constraints 存在版本字段。
- [ ] AC4: 本仓以迁移前真实值生成 `.ai/butler.config.json`，并只从 `.ai/local-constraints.md` 删除 Active Profiles/Butler 开关/Review Policy 机器段；人类约束正文保真，迁移后 `resolve` 返回 config 且无冲突。
- [ ] AC5: 活 README/HUMAN_GUIDE/Coder/docs/模板/skills/commands 对配置位置、兼容期、写入边界和安全默认描述一致；历史归档与旧 migration 保持历史事实，不追溯改写。
- [ ] AC6: `migrate_config` 登记到 v3.3.0 manifest/recipe，升级计划能从 v3.2.0 包含该 action；当前版本项目若配置漂移仍会被检测，迁移/重生成/重戳顺序和事务边界明确。
- [ ] AC7: v3.3.0 的 VERSION、插件 manifest、README badge、根 CHANGELOG 和既定迭代/里程碑交付路径对齐；状态审计明确显示 UNRELEASED，绝不宣称 commit、tag 或远端发布完成。双格式交付实体在 Goal eligible 后按收口仪式生成并由关闭态审计核对。
- [ ] AC8: 消费合同、project-config、upgrader、文档/registry、完整 CI、关闭态审计与 `git diff --check` 全绿；P5 完整强审无 Must Fix，独立复核关闭状态如实披露。

## Verification Method

- AC1–AC3, AC5：新增消费合同结构测试，逐个扫描活规则、命令与 skills 的 `resolve/set`、错误语义和禁止旧写法。
- AC4：对本仓运行 `resolve` 并核对 JSON/Markdown 内容；迁移算法专项覆盖同值、冲突和正文保真。
- AC6：upgrader 专项从 v3.2.0 生成真实计划并断言 `migrate_config`，验证 current drift 回归。
- AC7–AC8：版本一致性/迁移 manifest、完整 `scripts/verify-ci.sh`、Goal/state auditor、artifact check 与 diff check。

## External References

- N/A

## Open Questions / Risks

- N/A
