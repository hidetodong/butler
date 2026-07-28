<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0093 · Butler 项目配置合同与统一读写内核

分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-07-28

> ⚠️ 危险模式：本产物由模型自主确认问题理解，未经用户逐项确认（ITER-0093，2026-07-28）

## Current Understanding

- 当前项目级持久开关和 Active Profiles 由模型从 `.ai/local-constraints.md` 的 Markdown 段落读取与回写，缺少稳定的数据合同、类型校验和原子写入。
- 本迭代先建立 `.ai/butler.config.json` 的最小扁平合同和统一读写内核；部署生成、旧 Markdown 迁移与消费端切换由 R2/R3 承接。
- 第一版字段固定为 `schema_version`、`dangerous`、`independent_review`、`preference`、`profiles`，不增加 `features` 或 `settings` 分组。

## Scope

- 新增版本化 JSON Schema 和 Python 标准库读写工具，支持校验、读取、初始化与单字段安全更新。
- 配置存在但损坏时 fail-closed 并返回可操作诊断；危险模式不得因缺字段、错误类型或未知结构被误开。
- 写入采用同目录临时文件加原子替换，保留未知项目文件，不依赖 PyYAML 或宿主 cwd。
- 本迭代不读取旧 Markdown、不修改部署流程、不切换现有命令消费端，保证 R1 可独立验证。

## Open Questions / Risks

- `preference` 当前缺字段语义是默认 on，但一个已存在且损坏的新配置不应静默套默认值；两者需区分为“配置缺失”和“配置非法”。
- `profiles` 来自原 Markdown 的自然语言列表，迁移规则需要在 R2 单独处理，R1 只定义字符串数组合同。
