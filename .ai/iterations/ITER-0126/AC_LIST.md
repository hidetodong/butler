---
状态: ack-frozen
ACK 日期: 2026-10-21
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0126

## Goal

- 把 3.6.0 之后欠下的迁移写成 `migrations/v4.0.0.md`，并在临时项目上证明它跑得通。
- 旧收件箱和 `origin/` 遇到就停下，不默默删。
- 版本号保持 `3.6.0`。切版留到里程碑收口。

## In Scope

- `migrations/v4.0.0.md`，以及 `migrations/manifest.json` 里从 3.6.0 到 4.0.0 的那一节。
- 临时项目上的升级回归。临时 butler 根的版本写成 4.0.0，好让这条配方被选中。
- `apply` 不再强制 `--split`。知识文件夹形状检查去掉。历史 `[split]` 定义保留。
- 项目配置的 `preference` 布尔从契约里卸掉。旧配置只去掉这一键。
- `.ai/debt.md` 里被这条配方还清的句子。

## Out of Scope

- 不改 `VERSION`，不写 `CHANGELOG.md` 的发布条，不打标签，不提交，不收口 MILE-0016。
- 不在未点名的真实项目上执行升级，也不升级 butler 仓自己。
- 不改已发布的历史配方。
- 不处理收件箱里那两条旧缺陷，不改 loop，不加排序器。
- 不删仓库外已有的偏好数据，不删 `templates/preference/` 骨架。
- 不重开 ITER-0123、ITER-0124、ITER-0125。

## Acceptance Checklist

- [ ] AC1: `migrations/manifest.json` 有一节 `source` 为 `3.6.0`、`target` 为 `4.0.0`、`recipe` 为 `v4.0.0.md`，并且该文件存在。整份清单仍能通过校验。`VERSION` 仍是 `3.6.0`。用本仓库当 butler 根、项目戳在 3.6.0 时做计划，选中的动作里没有 `4.0.0/` 开头的动作。
- [ ] AC2: 这一节动作包含 `global_install`、`regen_entrypoints`、`sync_hooks`、`restamp`，以及删除 `.ai/project`、删除 `.ai/PROJECT.md`、把仓根 `deliveries` 移到 `.ai/deliveries`。`migration-schema.md` 里 `[split]` 的定义还在，仍写着知识文件夹和退役说明。
- [ ] AC3: 临时项目戳在 3.6.0，里面有带文件的 `.ai/project/`、有 `.ai/PROJECT.md`、仓根有 `deliveries/`，且没有旧收件箱、没有 `origin/`。用版本为 4.0.0 的临时 butler 根执行这条真实配方后：`.ai/project/` 和 `.ai/PROJECT.md` 消失，`deliveries/` 的内容出现在 `.ai/deliveries/` 且字节不变，源路径消失；两个入口的用户区原文还在，版本戳变成 4.0.0；hook 与配方来源一致。再执行一次，退出码 0，不另造一份。这次执行没有调用 `scripts/setup.sh`，也没有改本机插件。
- [ ] AC4: 同一套临时升级里，项目若带有旧收件箱（文件里有 `butler-inbox:managed`）或仓根 `origin/`，退出码非 0，这两处字节和目录都不变，`.ai/project/`、`.ai/PROJECT.md`、`deliveries/` 也不变。新格式闪念口（标题是 `## 闪念`）不会单凭自己让升级停住，文件字节保持原样。
- [ ] AC5: 仓根 `deliveries/` 和 `.ai/deliveries/` 都已经存在时，退出码非 0，两边都不变。
- [ ] AC6: `apply` 不带 `--split` 不再因为缺参数被拒绝。带 `--split defer` 或 `--split now` 仍被接受。项目只有 `.ai/project/`、没有 `00_INDEX.md`、也没有 `.ai/PROJECT.md` 时，不再因为形状检查而停。
- [ ] AC7: 项目配置的字段表、默认值和规则卡不再把 `preference` 当作活字段。人读文档不再写这个布尔还在。旧的 `.ai/butler.config.json` 经过这条升级后只少 `preference` 这一键，`dangerous`、`independent_review`、`profiles` 保持原值。没有这一键的配置仍能读。实验工具还在。没有名为 `reorder_options` 或 `reorder_by_profile` 的函数。
- [ ] AC8: `.ai/debt.md` 不再写「还没有 `migrations/v4.0.0.md`」，也不再写升级不会碰旧收件箱和 `origin/`。旧收件箱和 `origin/` 仍要人处理的那条账留着。「从未在真实已部署项目上跑过」留着。
- [ ] AC9: `python3 scripts/test-butler-upgrade.py` 退出码 0。`bash scripts/verify-ci.sh` 退出码 0。`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，输出里没有 `[DRIFT]`。

## Verification Method

- AC1: 读清单和 `VERSION`，并对着本仓库跑一次计划，确认 4.0.0 的动作没被选中。
- AC2: 读清单动作和 `migration-schema.md` 的 `[split]` 段。
- AC3–AC6: 在 `scripts/test-butler-upgrade.py` 里用临时目录跑。临时 butler 根使用清单里那一节真实动作。不碰本仓库的 `.ai/`，不调用 `scripts/setup.sh`。
- AC7: 读配置契约、规则卡和人读文档；用临时项目跑掉键和读取。全仓检索那两个重排函数名。
- AC8: 读 `.ai/debt.md`。
- AC9: 跑升级器测试、持续集成和审计，审计输出里检索 `[DRIFT]`。

## External References

- N/A

## Open Questions / Risks

- 从还含历史 `[split]` 的老版本一路升上来，并且 `.ai/PROJECT.md` 还在时，形状检查去掉之后，不再用原来的检查拦住。历史 split 仍排在 v4 删除之前。冻结前若要保住「有待拆单文件就停」，说一声，我改 AC6。
- 临时回归还清不了「从未在真实已部署项目上跑过」。那条账留着。
- `preference` 卸掉之后，已经写在仓库外的旧偏好数据留在原处。
