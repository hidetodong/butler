# CONCEPT — ITER-0088 · 五件套校验与门禁

## Current Understanding
- strict check 只对带模板 marker 的 live 产物生效，避免把迁移前工作区和历史归档直接打红。
- hook 在受保护五件套写后提示或阻断结构漂移；状态审计与 CI 做最终硬核。

## Scope
- CLI check、项目 check、hook rule、auditor 与 verify-ci 接线、双宿主文档。

## Open Questions / Risks
- N/A
