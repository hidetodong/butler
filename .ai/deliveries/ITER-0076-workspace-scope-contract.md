# ITER-0076 · Monorepo 工作区地图与需求级范围契约

## 本次交付目标

让每份需求能用稳定工作区键声明允许修改的包，而不把易变目录路径写进历史 PRD。

## 已完成内容

- 新增 `.ai/project/workspaces.md` 地图契约与稳定 `workspace_key`。
- 定义 primary/supporting/read-only/excluded 四类范围、默认拒绝与模块子集。
- 定义路径移动、异常 fail-closed、越界扩张重审和单包 `root` 退化态。
- 接入 references/README，并新增 7 项结构合同测试。

## 关键变更 / 用户可感知变化

- 目录移动只改地图，不改历史需求身份。
- 未声明工作区不再被理解为默认可写。
- 模块不能借局部声明扩大整份需求写范围。

## 高层影响范围

- 新增 `Coder/40_Context_Management/workspace-scope-schema.md`。
- 更新 references schema、Coder 导航与结构测试。
- 未实现实际 diff/hook 门禁；该行为由 R8 承接。

## 验证方式与结果摘要

- 专项 7/7、完整 CI exit 0、160 项 hooks 通过。
- Goal adjudicator 十项全绿，强审最终 Must Fix 0。

## 已知剩余风险 / 延后事项

- 自动发现、生成文件归属和真实改动对账仍待 R8。
- 未执行 fresh-context 独立复核。

## 引用

- `.ai/iterations/ITER-0076/`
- `.ai/iterations/ITER-0076/evidence/`
