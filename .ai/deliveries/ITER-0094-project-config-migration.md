# ITER-0094 · Butler 配置部署与 legacy 迁移

## 本次交付目标

让新项目直接采用 JSON 配置，并让旧项目能在不丢开关、profile 或人类约束正文的前提下事务迁移到新结构。

## 已完成内容

- project-config 新增 legacy 严格解析、JSON 优先兼容读取、冲突报告和纯迁移计划。
- upgrader 新增有限的 `migrate_config` action，把 JSON 与 Markdown 两项变更纳入既有 backup/restore/journal。
- 新部署改为生成 `.ai/butler.config.json`；`local-constraints.md` 只保留人类可读项目差异。
- 当前版本项目会按已发布 action 检测配置被删、未迁或冲突，不被 `already-current` 静默隐藏。

## 关键变更 / 用户可感知变化

新项目不再把持久开关和 Active Profiles 写进 Markdown。旧项目在 JSON 缺失时仍可回退读取；迁移遇到模糊 Markdown、损坏/冲突 JSON 或 symlink 会在首写前停止。

## 高层影响范围

project-config、butler-upgrade、新项目部署协议、本地约束 schema、共同 rule-card 与 init 双宿主入口。

## 验证方式与结果摘要

project-config 27 项、upgrader 18 项、完整 CI（含 200 个 hook 测试和全部行为组）与 `git diff --check` 通过；Goal 裁决为 `eligible`。

## 已知剩余风险 / 延后事项

- `migrate_config` 真实版本链 action 留给 R3 与发布接线统一登记；R2 未冒称现有 3.2.0 项目已会自动触发。
- 本轮危险模式强审修复 1 个 Must Fix 后最终清零；未执行 fresh-context 独立复核。

## 引用

- `.ai/iterations/ITER-0094/AC_LIST.md`
- `.ai/iterations/ITER-0094/TECH_PLAN.md`
- `.ai/iterations/ITER-0094/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0094/evidence/`
- `tools/project-config/README.md`
- `tools/butler-upgrade/README.md`
