# 01_CHANGELOG

> ITER-0055 · 基地车展开边界加固。

## ADD

- `templates/hooks/lib/project_root.py` + `scripts/resolve-project-root.py`：无副作用项目根单一算法与 CLI 薄壳（AC1–4）。
- `scripts/test-resolve-project-root.py`：7 个显式目标/Butler/Git/聚合目录/软链场景（AC2/3/6）。
- `migrations/v2.16.0.md`：全局刷新、双入口重生成、hook 同步与重戳配方（AC5/6）。

## EDIT

- `mcv-deployment.md` / `butler-upgrade.md` / `rule-card.md`：用户点名优先、歧义零写入、历史迁移队列键控 `PROJECT_ROOT`（AC1–5）。
- 8 Claude commands + 8 Codex skills：项目级读写共用 MCV 根目录契约（AC4/5）。
- `templates/hooks/lib/io.py` + hook tests/wrapper：绝对 patch target 按实际项目根校验，跨根 patch/聚合目录相对写入 fail-closed（AC3–6）。
- renderer、README/HUMAN/Codex 兼容说明、Coder/AGENTS 入口、项目知识与回归脚本：登记新边界与现状（AC1–7）。

## DELETE

- `/Users/cyborgno2/Documents/research/.ai/iterations/ITER-0051` 及其空父目录：删除误展开残留，未删除文件（AC7）。
