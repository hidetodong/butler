# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：**v2.1.0 已发布**（MILE-0004 收尾切版，MINOR·向后兼容能力新增；聚合 ITER-0035~0041，含 MILE-0004 收口）。前一版 v2.0.0 是 MILE-0003 的 MAJOR。
- **无活跃里程碑 / 无活跃迭代**（`MILESTONES.current: none`、`ITERATIONS.current: none`）。MILE-0004"PRD 先行 + references 版本化改版同步"已收口，路线图 R1–R6 六块齐。
- **PRD 全生命周期子系统成型（v2.1.0 落地、未端到端踩过）**：`references-schema`(R1 契约 + §9 非回归门) + `prd-split`(R2 首切) + `/milestone` 大 PRD 并进(R3) + AC 钉版 `prd_version`(R4) + `prd-update` 改版同步 `/prd update`(R5 主流程 + R6 §4.2 认亲松边)。opt-in 加层，非 PRD 流全程未动。

## 活跃战线

- **无进行中战线**——MILE-0004 已收口 + 切版，等下一个方向（新里程碑 / 独立迭代由用户发起）。
- **PRD 全链首次端到端实战仍悬**：R1–R6 全靠执行遵从守，命门红线（切片逐字无损、绝不切碎、映射/版本单一真源、亮牌不自动改已冻结、松边不硬认、非回归门 git diff 为空）都还没在真实"拿一份大 PRD 开里程碑 + 改一次版"里检验过——R4 钉版回溯、R5 冻快照的首次兑付点。

## 下一个瓶颈

- **无既定下一步**：待用户给方向。候选——PRD 全链真实 dogfood（拿一份真 PRD 走导入→改版全程）可一并还上"从未真跑"的欠账。
- **两笔历史欠债仍悬着**（见 `debt.md`）：hook 在 butler 侧不 live、`/butler-upgrade` 从未真跑（`[split]` 迁移接线已于 ITER-0035 补齐，就差真实老项目端到端跑一遍——v2.1.0 的 `migrations/v2.1.0.md` 是 `[no-op]`+`[restamp]`、不新增结构迁移风险）。
