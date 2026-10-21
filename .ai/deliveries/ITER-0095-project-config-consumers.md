# ITER-0095 · Butler 配置全链路接线与 3.3.0 发布准备

## 本次交付目标

让危险模式、独立复核、偏好、进度和双宿主入口共享同一份项目配置语义，并把 MILE-0013 准备成可升级、可验证的 v3.3.0 本地候选。

## 已完成内容

- 所有活消费端统一通过 project-config `resolve` 读取，坏配置 fail-closed，source 与 legacy 冲突显式报告。
- 项目开关统一通过 `set` 回写 JSON；legacy/missing 项目先 upgrade/init，不再改 Markdown。
- 当前 Butler 仓保值迁移到 `.ai/butler.config.json`，并从 local constraints 清除机器段。
- v3.3.0 manifest 登记 `migrate_config`，VERSION、插件、README badge 和根 CHANGELOG 对齐为 UNRELEASED 候选。
- 配置与升级专项正式接入完整 CI；新增消费矩阵防止命令、skills 与规则真源再次漂移。

## 关键变更 / 用户可感知变化

项目的危险模式、独立复核、偏好抑制和 Active Profiles 现在由扁平 JSON 稳定承载。旧项目仍能兼容读取，但写操作会明确要求先升级；`/butler:preference project on|off` 可单独控制当前项目。

## 高层影响范围

project-config、butler-upgrade、会话调度、危险/复核/偏好引擎、Claude commands、Codex skills、rule-card、人类指南、workflow registry、CI 与版本迁移链。

## 验证方式与结果摘要

project-config 32 项、upgrader 19 项、200 个 hook 测试、双宿主/registry/链接/状态矩阵、两次修复后完整 CI 与 `git diff --check` 通过；Goal 裁决为 `eligible`。

## 已知剩余风险 / 延后事项

- v3.3.0 尚无发布提交、tag 或 push，只是本地 UNRELEASED 候选。
- Pi 可选 tsc 因本机缺宿主模块/Node types 只报告既有警告；核心 Pi 契约验证通过。
- 危险模式完整强审最终 Must Fix 0、Should Fix 0；`independent_review=false`，未执行 fresh-context 独立复核。

## 引用

- `.ai/iterations/ITER-0095/AC_LIST.md`
- `.ai/iterations/ITER-0095/TECH_PLAN.md`
- `.ai/iterations/ITER-0095/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0095/evidence/`
- `tools/project-config/README.md`
- `migrations/v3.3.0.md`
