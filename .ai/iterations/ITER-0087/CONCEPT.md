# CONCEPT — ITER-0087 · 五件套阶段生成器

## Current Understanding

- R2 在 R1 contract 上实现 CLI；生成仅作用于当前 live 工作区。
- `init` 只创建缺失骨架；`reset` 必须显式且默认拒绝覆盖非模板正文；`upgrade` 保留已识别段正文。

## Scope

- render/init/reset、阶段边界、原子写、dry-run、幂等与正文保护测试。

## Open Questions / Risks

- N/A
