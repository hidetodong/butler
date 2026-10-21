# ITER-0122 · usage 采集：CLI 入口记下最后调用时间

- 交付级别：迭代交付（小版本）
- 收口日期：2026-09-14
- 所属里程碑：MILE-0016（Butler 瘦身与重造）

## 本次交付目标

产品驻留 CLI 被调用后，项目本地能读到该入口的最后调用时间。这份数据不进 git。采集失败不能把原命令弄挂。90 天报告不做。

## 已完成内容

- 新建 `tools/usage/`：`record` / `show` / `catalog`，落点 `.ai/.usage.json`。
- 入口身份封闭：`workflow:router`、registry 里 12 个工作流、产品驻留工具目录。未知 id 拒绝写入。
- 产品驻留 Python CLI 的 `main` 打点；工作流薄壳写明调用 `usage.py record workflow:<id>`。
- gitignore 加上 `.ai/.usage.json`。写失败 fail-open。
- `debt.md` 改为采集已落地，报告仍归 R12。

## 关键变更 / 用户可感知变化

- 跑过的产品 CLI 会在项目 `.ai/.usage.json` 留下最后时间。文件进 gitignore，不要提交。
- slash 命令本身没有进程钩。薄壳里有 record 这一步，但不保证每次 `/butler:inbox` 都已经记到。
- 采集挂了不会把原来的命令弄红。

## 高层影响范围

- 新增：`tools/usage/`。
- 改动：19 个产品工具 `main`、工作流薄壳、CI、若干测试的树哈希、workspace-scope check-diff、OVERVIEW 工具清单。
- 不算：vendored 校验器、dogfood 脚本、Node 自测桥。

## 验证方式与结果摘要

10 条验收全部通过。usage 测试 8 passed，CI 退出码 0。收口前完成裁决 `eligible`。独立复核未跑。

CI 前两次失败：升级器零写入测试被 `.usage.json` 污染；OVERVIEW 未重算。修完后第三趟绿。

## 已知剩余风险 / 延后事项

- 工作流打点靠薄壳自觉。
- 已部署项目要自己把 `.ai/.usage.json` 加进 gitignore。
- 90 天报告仍未做（R12）。
- 本轮不切版、不提交。

## 引用

- 四件套：`.ai/iterations/ITER-0122/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 变更流：`.ai/iterations/ITER-0122/CHANGELOG.md`
- 证据：`.ai/iterations/ITER-0122/evidence/`（6 条记录）
