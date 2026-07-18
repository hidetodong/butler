# Session Handoff

## 当前状态

- 当前无 active 迭代/里程碑；ITER-0067 已归档并双格式交付。
- ITER-0067 从 `feat/mile-0008-goal-assurance` 收口；用户已授权合并并推送到 `github/main`，实际同步状态以 Git refs 实时核验。
- 发布真相为 v2.17.0；MILE-0007 已聚合切版并合入/push `main`，tag 为 `v2.17.0`。
- 危险模式仍为 ON；只有用户显式要求才关闭。

## 已交付

- Butler 对无法归属项目的真实外部路径退出流程判定，由宿主权限接管；坏输入继续 fail-closed。
- Claude/Codex 按目标真实 Butler/Git 根校验；Codex patch 支持多个项目根逐根门禁。
- 危险模式每次任务启动冻结宿主已预授权的范围上限，上限内可动态施工，上限外隔离或诚实交还。

## 验证与证据

- `final-hook-tests`：147 passed。
- `final-codex-wrapper` 与 `final-full-ci`：passed。
- 强审修复 2 个 Must Fix，最终 Must Fix 0、Should Fix 0；Goal adjudicator 十项全绿、verdict=`eligible`。
- 六份 evidence 已整包归档到 `.ai/iterations/ITER-0067/evidence/`。

## 下一步边界

- 外部旧项目要获得新 hook 行为，仍需后续切版并走 migration/upgrade；本轮不假报已分发。
- 宿主权限范围是真实授权上限，Butler 不维护第二套权限文件，也不把正常跨目录写入变成 bypass。
- 本次只合并迭代提交，不切新版本；外部项目获得新行为仍需后续切版与升级。
- 后续普通改动从 v2.17.0 继续；未形成新发布前，状态审计会因 VERSION tag 不指向 HEAD 明确亮 `UNRELEASED`。
- 若用户要求远端保护：需先解决私有仓库套餐/可见性，再推 workflow 并核验 required check。
