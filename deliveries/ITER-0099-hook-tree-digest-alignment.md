# 升级器 hook 树摘要与部署文件集对齐

## 本次交付目标

修复已部署项目执行 `sync_hooks` 时被错误判定为 hook 树遭篡改的问题。升级器现在用“实际会部署到项目里的文件集”计算摘要，既允许干净的历史 Butler hook 继续升级，也保留对真实内容修改和项目独有文件的拒绝保护。

## 已完成内容

- 在 `tools/butler-upgrade/upgrade.py` 增加统一过滤函数，让源模板和目标项目共同排除测试目录、缓存、字节码以及顶层 pytest 脚手架。
- 按新口径重算 `migrations/manifest.json` 的历史摘要白名单，得到 10 个可追溯值，并覆盖此前缺失的 v2.18.0、v3.0.0 和 v3.1.0。
- 在 `scripts/test-butler-upgrade.py` 增加三组回归：过滤口径一致性、历史 tag 摘要可复算、真实篡改继续拒绝。
- 解决远端同步造成的 ITER-0096 编号碰撞，将本地工作完整迁移为 ITER-0099，并重新生成全部验证证据。

## 关键变更 / 用户可感知变化

- 干净的旧项目不会再因为未部署 `conftest.py` 或 `pytest.ini` 而被误判为冲突。
- `tests/`、缓存和 `.pyc` 在源侧与目标侧采用同一套规则，不再有两份条件逐渐漂移。
- 项目真正修改 Butler hook 内容，或在受管 hook 树里加入自有文件时，升级器仍会拒绝覆盖。
- butler-radar 当前只读计划为 `already-current` 且无冲突；本次没有对任何外部项目执行写入。

## 高层影响范围

实现改动限于升级器过滤逻辑、迁移 manifest 和升级器回归测试。没有修改 hook 运行时判定、`split`、配置迁移、事务备份或 journal 行为。

迭代产物与证据归档在 `.ai/iterations/ITER-0099/`；对象级变更见 `.ai/iterations/ITER-0099/CHANGELOG.md`。

## 验证方式与结果摘要

- `upgrader-tests`：22 项通过，覆盖统一过滤、历史摘要和两类篡改拒绝。
- `deployed-hook-matrix-final`：本机六项目只读矩阵精确符合预期，五项命中白名单，`claude-skills` 因项目自有 hook 保持拒绝。
- `radar-plan`：butler-radar 返回 `already-current`、`conflicts=[]`。
- `full-ci`：使用 uv 0.9.28 与 Python 3.12.12 完整运行 `bash scripts/verify-ci.sh` 并通过。
- 第一次矩阵诊断因 Python 3.14 动态导入方式错误失败，失败 record 与最终绿色 record 一并归档，未被隐去。

## 已知剩余风险 / 延后事项

- 本机六个样本不能证明其他机器不存在不同的历史部署裁剪；如果出现新变体，应考虑让部署侧维护机械文件清单。
- v1.0.0 时代缺少原始部署凭据，旧项目与历史 tag 的一致性属于事后内容比对。
- `claude-skills` 的项目自有 hook 与 Butler 受管目录冲突属于独立兼容性需求，本轮没有放宽守门器。
- 项目配置未开启独立复核，本次采用同上下文 P5 简评。

## 引用

- 验收清单：`.ai/iterations/ITER-0099/AC_LIST.md`
- 技术方案：`.ai/iterations/ITER-0099/TECH_PLAN.md`
- 验证报告：`.ai/iterations/ITER-0099/VERIFY_REPORT.md`
- 对象级变更流：`.ai/iterations/ITER-0099/CHANGELOG.md`
- 证据目录：`.ai/iterations/ITER-0099/evidence/`
