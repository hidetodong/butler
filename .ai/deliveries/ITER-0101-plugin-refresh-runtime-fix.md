# Butler 插件刷新运行时与错误码回声修复

## 本次交付目标

让缺少全局 uv 或 PyYAML 的开发机仍能使用仓库锁定环境完成 Butler plugin 官方校验与刷新，并保证 setup 在 UTF-8 中文文案旁准确保留子安装器退出码。

## 已完成内容

- 保留 uv 为首选 validator 路径；无 uv 时依次尝试仓库 `.venv` 和可导入 PyYAML 的系统 Python。
- 所有 validator runtime 都不可用时明确失败，不跳过官方校验。
- 修复 Codex 失败回声和 Pi 成功回声中的 shell 变量边界。
- 补齐无 uv、无 runtime、C.UTF-8 错误码、Pi 安装成功和 iteration-intake 状态结构回归。

## 关键变更 / 用户可感知变化

- `scripts/setup.sh` 已在真实机器上整体 exit 0。
- Codex Butler plugin 已安装启用为 `3.3.0+codex.20260801061356`。
- Claude 根命令、命名空间命令与 Pi 扩展软链均已刷新到当前仓库。
- 新 Codex 会话会加载这次刷新后的 plugin；当前已打开会话不会热替换 Skill。

## 高层影响范围

改动限于机器级 setup、Codex plugin 安装器、双宿主安装验证，以及 ITER-0100 新增 iteration-intake 生成状态的结构修复；未改变 Router 业务语义或高风险工作流边界。

## 验证方式与结果摘要

- 双宿主安装矩阵通过，覆盖仓库 venv 回退、无 runtime 拒绝、Codex exit 7 回声与 Pi UTF-8 成功回声。
- 固定 uv 0.9.28 / Python 3.12.12 的完整 `scripts/verify-ci.sh` 最终通过；两次诊断失败证据保留在归档中。
- 真实 `scripts/setup.sh` 整体 exit 0，`codex plugin list` 显示 Butler installed/enabled。
- 证据索引与完整命令记录见 `.ai/iterations/ITER-0101/VERIFY_REPORT.md` 和 `.ai/iterations/ITER-0101/evidence/`。

## 已知剩余风险 / 延后事项

本轮无剩余已知风险。插件刷新需要新开 Codex 会话才会加载，这是宿主生命周期边界，不是安装失败。

## 引用

- `.ai/iterations/ITER-0101/AC_LIST.md`
- `.ai/iterations/ITER-0101/TECH_PLAN.md`
- `.ai/iterations/ITER-0101/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0101/CHANGELOG.md`
- `.ai/iterations/ITER-0101/evidence/`
