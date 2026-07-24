<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0090 · Setup 机器级安装命令

## Current Understanding

- 用户不应为了刷新 Butler 的机器级能力记住 `bash scripts/setup.sh`；应有独立 `/butler:setup` 与 `$butler-setup` 入口。
- setup 命令只负责全局命令、Codex plugin 与 Pi 扩展安装，不隐式初始化或升级当前项目。
- `scripts/setup.sh` 继续作为唯一执行真源；双宿主入口只解析 Butler 根、亮明机器级影响、取得确认并转交脚本。

## Scope

- 新增 setup 规则真源、Claude/Codex 入口和 registry 元数据。
- 让 `/butler:init` / `$butler-init` 指向 setup 命令，不再各自维护安装步骤。
- 更新工作流数量、分发表与结构回归；隔离验证 setup 成功、失败和宿主缺失分支。

## Open Questions / Risks

- 命令本身来自尚未安装或仓库发现面；完全空白机器仍需首次 clone 后运行脚本，这是不可消除的 bootstrap 边界。
- 机器级写入必须保留显式确认，不能因语义触发就直接执行。
