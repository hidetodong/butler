# ITER-0067 · 项目外写入授权边界

## 本次交付目标

- 让 Butler 只拦能归属项目的流程违规，不再抢在宿主权限之前拒绝真实项目外写入。
- 让危险模式能在预授权范围内无人值守跨项目施工，同时不能自行扩大权限。

## 已完成内容

- 拆开“坏输入”和“真实项目外目标”：坏输入继续拒绝，项目外目标交宿主决定。
- Claude 与 Codex 统一按目标文件的真实 Butler / Git 根执行门禁。
- Codex patch 支持多个项目根逐一校验，任一项目拒绝则整次拒绝。
- 危险模式新增启动冻结授权上限、范围内动态追加施工项目和范围外依赖路由。

## 关键变更 / 用户可感知变化

- 用户明确要求修改 `~/.codex/config.toml` 等项目外文件时，Butler 不再要求 `BUTLER_BYPASS`；宿主仍会按自身权限决定是否允许。
- 从聚合目录或项目子目录工作时，目标若属于某个项目，会使用那个项目自己的 `.ai/` 状态校验，不会因 cwd 不同而误放或误拦。
- 危险模式不会因后来发现授权范围内的兄弟项目而停机；真正超出上限的关键依赖仍会诚实交还。

## 高层影响范围

- 共享 hook 的路径分类、项目根解析和 Codex 多目标分派。
- 危险模式协议、部署说明、Coder 入口、规则卡和 hook 贡献者说明。
- Codex wrapper E2E、147 项 hook 回归和完整双宿主 CI。

## 验证方式与结果摘要

- `final-hook-tests`：147 项通过，覆盖外部/未知目标、项目子目录、兄弟项目、多项目 patch 与全部既有门禁。
- `final-codex-wrapper`：真实 plugin wrapper 路径通过。
- `final-full-ci`：固定 uv/Python 工具链、双宿主、plugin/skills、Markdown、Goal 与 hook 矩阵全部通过。
- Goal adjudicator 十项检查全部通过，裁决 `eligible` 后进入收口。

## 已知剩余风险 / 延后事项

- 本轮无未关闭实现风险。
- 实际文件权限仍取决于宿主配置；若用户预授权范围过宽，Butler 不另建第二套权限系统兜底。
- 本轮不切版本、不发布、不推送，也未同步外部项目里的旧 hook 副本。

## 引用

- `.ai/iterations/ITER-0067/AC_LIST.md`
- `.ai/iterations/ITER-0067/TECH_PLAN.md`
- `.ai/iterations/ITER-0067/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0067/CHANGELOG.md`
- `.ai/iterations/ITER-0067/evidence/`
