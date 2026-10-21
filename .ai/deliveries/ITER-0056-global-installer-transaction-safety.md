# 全局安装器先验安全与真实结果

> ITER-0056 · MILE-0007 R1 · 用户双 ACK · P5 完整审查 · 2026-07-18

## 本次交付目标

修复 Butler 全局安装时可能丢失 Claude 用户配置、误判 shell 文本和接管用户命令目录的问题，让异常输入零破坏停机，正常安装保持幂等。

## 已完成内容

- 新增零依赖 Python helper，先规划并校验 shell、Claude 配置和命令软链，再逐对象原子应用。
- marker 只接受 0 个或完整一对；有效 `BUTLER_PATH` export 只接受 0/1 条；命令软链只有可证明归属 Butler 时才迁移。
- 保存用户区原始字节、CRLF、无尾换行和文件权限；计划后状态变化会在暂存前与提交前再次拒绝。
- `setup.sh` 改为薄编排，Codex plugin 失败时返回原退出码并明确报告“部分完成”。
- 新增 16 个隔离 HOME 专项测试，并把它们接入完整双宿主验证矩阵。

## 关键变更 / 用户可感知变化

残缺 marker、重复 export、真实命令目录、无关软链或不可认领断链不再被猜测处理，安装器会说明冲突并保留用户状态。正常首装、重复安装和仓路径迁移仍可直接运行；Codex 安装失败不会掩盖 Claude 侧已经完成的事实。

## 高层影响范围

- 全局安装：`scripts/configure-global-install.py`、`scripts/setup.sh`。
- 自动验证：`scripts/test-configure-global-install.py`、`scripts/verify-dual-host.sh`。
- 人读入口：`HUMAN_GUIDE.md`、`README.md`。
- 未修改 renderer、resolver、hooks、workflow 算法或 Codex plugin installer。

## 验证方式与结果摘要

- 专项 16 tests、renderer 8 tests、resolver 7 tests、hook 127 tests 全绿。
- Codex R1/R2、hook wrapper、官方 plugin validator、Python compile、shell syntax 与 `git diff --check` 全绿。
- P5 完整审查发现并修复 2 个 Must Fix：计划后状态竞态与 CRLF 字节漂移；复审为 0 Must Fix、0 Should Fix。
- 未执行 fresh-context 独立复核，不冒称独立审查。

## 已知剩余风险 / 延后事项

- 多个用户对象不构成跨文件 ACID 事务；真实 I/O 中断时保留已完成对象并准确回声。
- 证据消失的历史断链需要用户人工确认，这是防止误接管的有意边界。
- MILE-0007 后续 R2–R5 不属于本次交付。

## 引用（只引用，不嵌入）

- `.ai/iterations/ITER-0056/AC_LIST.md`
- `.ai/iterations/ITER-0056/TECH_PLAN.md`
- `.ai/iterations/ITER-0056/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0056/CHANGELOG.md`
