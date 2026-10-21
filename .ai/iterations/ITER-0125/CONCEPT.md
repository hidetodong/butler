<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0125 · 升级器补上删除与移动

> 分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-10-20

## Current Understanding

- 这是 MILE-0016 的 R14。升级器现在写不出「删掉一个目录」和「把仓根路径移进 `.ai/`」。本轮把这两类动作补上，以后的 v4.0.0 配方才写得出来。
- 用户在 2026-10-20 说「继续吧」，确认上面的理解。`--split` 和 `project-knowledge-shape-valid` 本轮不动，留到 R15 写配方时再处理。
- 标签写成 `[delete]` 与 `[move]`，程序里的类型用 `delete` 与 `move`，接进现有三张动作表。
- 删除在目标已经不存在时再跑仍成功。移动允许源在仓根、目标在 `.ai/` 下；源和目标都在时停下，不覆盖。源和目标都不在时也停下，不当成已经搬完。
- 历史 `[split]` 标签定义保留。`apply` 仍必须带 `--split`。
- 测试只用临时夹具。本轮不写 `migrations/v4.0.0.md`，不在真实已部署项目上跑升级，不切版。

## Scope

- `migration-schema.md` §4 增加 `[delete]` 与 `[move]`，写明起始态、幂等和冲突即停。
- `upgrade.py` 的动作域、字段、前置条件和路径校验接上这两类。
- 临时夹具测试覆盖：重复执行、目标冲突、失败回滚。
- 若 manifest 要求新标签能被校验器认识，只让校验器认识这两类，不写 v4.0.0 配方实例。

## Open Questions / Risks

- 没有待确认问题。已部署项目里的 `origin/`、旧收件箱和仓根 `deliveries/` 要等 R15 的配方才会真的被删或被搬。
