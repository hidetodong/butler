> R5 部署 / 使用文档 + dogfood（人测桥外部调用方式）· closed · 2026-07-02

本文件是 ITER-0025 收口时归档的对象级变更流切片（ADD/EDIT/DELETE）。

## ADD
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md §6` — 新增「butler 驻留工具调用」节：驻留工具类别（不拷进目标项目、按 `$BUTLER` 传参调用）+ 桥调用形态 + `.ai/human-test/` 落点 + 无人岔口指 §7.4 → AC1 AC2
- `HUMAN_GUIDE.md §5 人测回环（交付自测桥）` — 新增人类视角使用说明：何时弹页面 / 四态含义表 / 提交即续跑 / 无人不弹页面 → AC3 AC4

## EDIT
- `tools/delivery-selftest/example/manifest.json` — 补第 4 项（MT-4 读屏走查），凑齐四态齐全样例，兼作 dogfood fixture 与使用示例 → AC6 AC7
- `tools/delivery-selftest/README.md 用法` — 补「外部项目调用样例」（传路径调 butler 那一份）+ 指向 mcv-deployment §6 / human-test-bridge → AC7
- `Coder/README.md` — mcv-deployment 描述补登记 §6 驻留工具调用（无隐式依赖）→ AC8

## DELETE
- 无
