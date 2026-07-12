# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：**v2.1.0 已发布**；**ITER-0042（PRD 先行触发加固）已收口、待切 v2.2.0**（MINOR·加 PostToolUse hook 属能力新增，切版待用户放行）。前两版：v2.1.0 = MILE-0004 收尾（聚合 ITER-0035~0041）、v2.0.0 = MILE-0003 MAJOR。
- **无活跃里程碑 / 无活跃迭代**（`MILESTONES.current: none`、`ITERATIONS.current: none`）。ITER-0042 独立迭代（MILE-0004 已收）修的是 v2.1.0 PRD 子系统的实战缺陷。
- **PRD 全生命周期子系统成型 + 触发已加固**：`references-schema`(R1 契约 + §9 非回归门) + `prd-split`(R2 首切) + `/milestone` 大 PRD 并进(R3) + AC 钉版 `prd_version`(R4) + `prd-update` 改版同步(R5+R6 认亲松边) + **ITER-0042 触发加固**（注入表内容路由 + §6.4 分类闸前移 + PostToolUse 落盘自检）。opt-in 加层，非 PRD 流全程未动。

## 活跃战线

- **无进行中战线**——ITER-0042 已收口，等下一个方向（切 v2.2.0 / 新里程碑 / 独立迭代由用户发起）。
- **PRD 全链首次端到端实战：部分踩过、仍未走完**。ITER-0042 的实战（Confluence+MCP+`/milestone`）暴露并修掉了**触发漏切**（软触发被绕过），但那次没走到切分/钉版/改版——命门红线（切片逐字无损、绝不切碎、映射/版本单一真源、亮牌不自动改已冻结、松边不硬认、非回归门 git diff 为空）与 R4 钉版回溯、R5 冻快照仍待真"拿一份大 PRD 走导入→改版全程"检验。

## 下一个瓶颈

- **无既定下一步**：待用户给方向。候选——PRD 全链真实 dogfood（拿一份真 PRD 走导入→改版全程）可一并还上"从未真跑"的欠账。
- **两笔历史欠债仍悬着**（见 `debt.md`）：hook 在 butler 侧不 live、`/butler-upgrade` 从未真跑（`[split]` 迁移接线已于 ITER-0035 补齐，就差真实老项目端到端跑一遍——v2.1.0 的 `migrations/v2.1.0.md` 是 `[no-op]`+`[restamp]`、不新增结构迁移风险）。
