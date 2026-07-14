# 01_CHANGELOG

> **ITER-0049 已收口**（MILE-0005 R3·`/butler:preference` 最宽参数命令）。对象级变更流（ADD/EDIT/DELETE），绑 AC、文件+章节级粒度，仅承载**当前开放迭代**的热数据。开新迭代时整体覆写；本迭代收口时归档至 `iterations/ITER-0049/CHANGELOG.md`。
>
> 上一迭代 ITER-0048 已收口，变更流见 `iterations/ITER-0048/CHANGELOG.md`。

## ADD

- `.claude/commands/butler/preference.md`（AC1/AC2/AC4/AC5）——全批**参数面最宽**的薄壳路由器命令：4 子命令（`on`/`off` 隐私总开关、`reback on|off` 影响回路〔**二级嵌套参数**〕、`distill` 手动蒸馏）+ 空参只读状态回声。含薄壳三件事声明 + DRY 红线、跨 cwd 路径约定段（数据落外置 `$PREF`）、第 0 步优雅降级、`$ARGUMENTS` 六路径分派、收尾回声状态。委托真源 `70_Extension_Preference/preference-probe-engine.md` §2.2/§2.3/§2.4/§6/§7 不复述算法。
- `migrations/v2.9.0.md`（AC9）——区间 `v2.8.0→v2.9.0`，部署面 `[no-op]`+`[restamp]`；新命令由 R1 整目录软链自动托管、无需重跑 `setup.sh`；触发名迁移刻意不碰 `templates/` → 无 `[regen-claude]`。

## EDIT

- `Coder/70_Extension_Preference/preference-probe-engine.md`（AC3）——作命令引用的 `/preference`→`/butler:preference`（11 处，含 §2.4 同意披露用户可见「怎么关」文案）+ §2.3 命令表主行加旧名注（旧名 `/preference` 仍作触发被识别、留空=只读回声）。**引擎 §1、§3–§10 算法一字未动**。
- `Coder/00_System_Prompt/logic-protocol.md`（AC3）——Pass A/B 命令名迁移 + 偏好模式激活段补自然语言触发描述 + 旧名识别保留。
- `Coder/65_Extension_Dangerous/dangerous-engine.md` / `Coder/20_Workflow_Lifecycle/local-constraints-schema.md` / `Coder/README.md`（AC3）——命令引用触发名迁移。
- `HUMAN_GUIDE.md` / `README.md`（AC3/AC7）——触发名迁移 + `README.md` `butler/` 目录树补 `preference.md`、扩展模式表 + Coder 目录 `70_Extension_Preference` 行迁 `/butler:preference`。
- `.ai/project/capabilities.md`（AC7）——命令表 `/preference` 行转换为 `/butler:preference` 一等入口（真源指命令文件 + 引擎章节、注参数面最宽·唯一二级参数·只管全局层）。
- `.ai/project/architecture.md` / `.ai/project/frontier.md`（AC3/知识前滚）——命令引用迁移 + frontier 前滚 R3 收口/版本 v2.9.0/成员 6。
- `VERSION`（AC9）——`2.8.0`→`2.9.0`；`CHANGELOG.md` 顶条 `[2.9.0] - 2026-07-14`（MINOR、聚合 ITER-0049）。

## DELETE

- 无——R3 纯新增，不删文件。**`templates/`（`rule-card.md`、`templates/preference/*`）的 `/preference` 刻意保留不迁**（DD5 边界：命令不下发目标项目，目标项目侧靠散文旧名兜底）。
