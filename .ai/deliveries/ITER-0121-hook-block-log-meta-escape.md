# ITER-0121 · hook 拦截日志与仓根 meta 逃生舱

- 交付级别：迭代交付（小版本）
- 收口日期：2026-09-14
- 所属里程碑：MILE-0016（Butler 瘦身与重造）

## 本次交付目标

拦下来的 hook 事后能翻到原因；没有进行中的迭代时，仓根那几份说明书能直接改，不用先开一轮迭代凑齐四件套。改 hook 源文件不再因为「摘要必须等于当前版本 tag」让 CI 立刻红。

## 已完成内容

- **拦截日志**：最终 deny 往 `.ai/.hook-blocks.log` 追加一行。bypass 成功仍只写 `.ai/RUN_LOG.md`。写日志失败继续 deny。文件进 gitignore，上限 256KB，超了丢最旧的完整行。
- **逃生舱**：没有 active 迭代时，`README.md` / `CHANGELOG.md` / `.gitignore` / `VERSION` / `LICENSE` 不被 `phase_gate` 和 `workspace_scope` 拦。有迭代时仍走原门禁。不扩到入口文件。
- **摘要 CI**：工作区 hook 树摘要等于当前 tag，或已登记进 `known_hook_tree_digests`。本轮新摘要已登记。历史 tag 仍必须在白名单里。
- **欠账**：删掉「hook 树一改就必须跟切版绑在一起」。v4.0.0 必须含 hook 同步。

## 关键变更 / 用户可感知变化

- 被门禁拦住之后，项目里会多一份本地拦截日志，能看出是哪条规则、拦了哪个文件。这份日志不进 git。
- 没有进行中的迭代时，改 README、CHANGELOG、版本号这类仓根文件不再被「先写四件套」拦住。
- 以后改 hook 不必跟切版绑在同一批，把新树摘要登记进白名单即可。

## 高层影响范围

- 新增：`templates/hooks/lib/block_log.py`、`templates/hooks/lib/iteration_state.py`。
- 改动：dispatcher、`phase_gate`、`workspace_scope`、升级器摘要测试、`migrations/manifest.json`、hook README、本仓 `.gitignore`。
- 台账：里程碑范围演进记录、欠账清单。
- 目标项目侧：下次切版同步 hook 才会拿到新 dispatcher；应忽略 `.ai/.hook-blocks.log`。

## 验证方式与结果摘要

10 条验收全部通过。hook pytest 211 passed，升级器测试 22 passed，CI 退出码 0。状态审计 0 漂移、2 条未发布标记。收口前完成裁决 `eligible`。独立复核未跑。

前三次取证把环境变量当成了命令，重录后绿。审计第一次失败是交接文件陈旧，同步后再录通过。

## 已知剩余风险 / 延后事项

- butler 仓自己不跑 live hook，行为只在测试里锁着。
- 已部署项目要等到 v4.0.0 同步 hook 才拿得到新 dispatcher。
- 用户原件只读这条纪律仍没有机器兜底。
- 本轮不切版、不提交。

## 引用

- 四件套：`.ai/iterations/ITER-0121/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 变更流：`.ai/iterations/ITER-0121/CHANGELOG.md`
- 证据：`.ai/iterations/ITER-0121/evidence/`（10 条记录）
