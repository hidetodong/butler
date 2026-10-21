# MILE-0013 · 项目级 Butler 配置结构化

## 本次交付目标

把 Butler 需要稳定读写的项目级设置从人类散文约束中拆出，形成严格、可迁移、双宿主一致的扁平 JSON 配置链路。

## 已完成内容

- R1 建立五字段 schema、严格 reader/writer、默认/损坏/路径安全与原子发布合同。
- R2 建立新部署生成、legacy 兼容投影和 upgrader 双文件事务迁移。
- R3 统一危险模式、独立复核、偏好、进度、双宿主入口与文档，完成本仓 dogfood、真实 migration action 和 v3.3.0 候选验证。

## 关键变更 / 用户可感知变化

新项目直接生成 `.ai/butler.config.json`；旧项目升级时保留现有开关/profile 与人类约束。所有入口共享 `resolve/set`，坏 JSON 不再被散文默认值掩盖，机器配置也不再与 Markdown 长期双写。

## 高层影响范围

项目配置内核、部署与升级器、会话冷启动、扩展模式、Claude/Codex 工作流、人类文档、CI、版本元数据与迁移配方。

## 验证方式与结果摘要

三个迭代均已完成专项、完整 CI、证据校验、危险模式 P5 强审与 Goal 裁决；R3 最终配置专项 32 项、upgrader 19 项，完整 CI 通过。

## 已知剩余风险 / 延后事项

- v3.3.0 尚未 commit、tag 或 push，必须保持 UNRELEASED 口径；真正发布仍需用户显式授权并按版本协议执行 Git 仪式。
- legacy 回退本版保留；彻底移除需未来破坏性版本单独评估。
- 三个迭代均未执行 fresh-context 独立复核，均如实保留在各自 VERIFY 与交付风险中。

## 引用

- `.ai/milestones/MILE-0013/MILESTONE.md`
- `deliveries/ITER-0093-project-config-core.md`
- `deliveries/ITER-0094-project-config-migration.md`
- `deliveries/ITER-0095-project-config-consumers.md`
- `migrations/v3.3.0.md`

## 拆分路线图回填

| 路线项 | 迭代 | 结果 | 交付 |
|---|---|---|---|
| R1 配置合同与统一读写内核 | ITER-0093 | closed | `deliveries/ITER-0093-project-config-core.md` |
| R2 部署与 legacy 事务迁移 | ITER-0094 | closed | `deliveries/ITER-0094-project-config-migration.md` |
| R3 全链路接线与发布验证 | ITER-0095 | closed | `deliveries/ITER-0095-project-config-consumers.md` |
