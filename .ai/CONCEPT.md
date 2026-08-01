<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0101 · 修复 Butler 插件刷新运行时与错误码回声

## Current Understanding

- ITER-0100 推送后执行 setup，Claude Router 软链成功，但 Codex plugin 校验因系统 Python 缺少 PyYAML 失败，随后 setup 的未加边界 rc 引用在当前 locale 下触发 unbound variable。
- 已确认：修复错误并重新执行 Butler setup
- 已确认：继续使用官方 plugin validator，不跳过验证
- 建议（未确认）：优先复用仓库锁定且具备 PyYAML 的 .venv Python，并保留 uv 与系统 Python 回退

## Scope

- 修复 install-codex-plugin.sh 的 validator Python 选择
- 修复 setup.sh 的退出码变量边界
- 增加回归验证并重新安装插件

## Open Questions / Risks

- N/A
