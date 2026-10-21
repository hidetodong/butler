# ITER-0090 · Butler setup 机器级安装命令

## 本次交付目标

让用户通过 `/butler:setup` 或 `$butler-setup` 安装/刷新 Butler，不再记忆脚本路径。

## 已完成内容

- 新增 setup 规则真源、Claude 命令、Codex skill/metadata 和仓库发现软链。
- workflow registry 扩为 12 项，并自动生成双宿主投影与人读能力表。
- init 改为委托 setup 规则；安装机械逻辑继续只存在于 `scripts/setup.sh`。
- 临时 HOME 覆盖宿主缺失、安装成功和部分失败，完整 CI 通过。

## 关键变更 / 用户可感知变化

首次 bootstrap 仍从仓库运行 `bash scripts/setup.sh`；已有 Butler 发现面后，直接调用 setup 命令即可刷新 Claude、Codex 和 Pi。

## 高层影响范围

workflow registry、双宿主入口、安装/初始化规则、Codex plugin 和用户文档。

## 验证方式与结果摘要

setup 双宿主矩阵、skill/plugin validator、registry 9 项、200 hooks 和完整 CI 全绿。

## 已知剩余风险 / 延后事项

Pi TypeScript 本机缺少可选类型依赖，沿用既有 warning skip；首次 Codex hook trust 仍需用户审阅。

## 引用

- `.ai/iterations/ITER-0090/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0090/evidence/`
- `Coder/20_Workflow_Lifecycle/butler-setup.md`
