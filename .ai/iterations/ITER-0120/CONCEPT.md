<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0120 · 根布局整理：backlog 与 deliveries 迁入 .ai

> 分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-09-11

## Current Understanding

- **R9 要做的事**：把两件现在还露在「项目根 / 带里程碑专名」里的东西收进 `.ai/`。候办草稿目录从 `.ai/milestone-backlog/` 改成 `.ai/backlog/`（因为它已经不只装里程碑那一档）；仓根 `deliveries/` 整树搬进 `.ai/deliveries/`，内部形状不变（迭代交付平铺，里程碑交付仍在 `milestones/` 子目录）。不留兼容软链。
- **已经领号**：本轮是 ITER-0120，不是新开迭代。用户 2026-09-11 说「可以开 R9」，视为确认范围，进入验收起草。
- **规模（开工前清点）**：候办草稿 10 份；交付树 272 个文件，只分两层（根 + `milestones/`）。全仓提到 `milestone-backlog` 的文件里，活规则 8、工具测试 8、活 `.ai/` 9；提到 `deliveries/` 的活规则 20、工具测试 12、活 `.ai/` 7、仓根人读 4、CHANGELOG 1。其余大量命中在冻结快照和交付正文自己里面。
- **两类消费者必须分开，不能一把扫过去全改**：
  - **活指针**（改完还得能找到文件）：规则真源、工具常量、测试夹具、台账「交付」列（热表 + 冷分片）、闪念口去向、待办区索引、冷启动读序投影、部署协议、CHANGELOG 里「详见 `deliveries/…`」这种找文件的链接。
  - **历史记述**（写的是当时的事实，不跟文件搬家）：`.ai/iterations/` 与 `.ai/milestones/` 收口快照、已发布 `migrations/` 配方、`docs/research/` 与 `docs/superpowers/`、以及搬过去之后的交付正文内部叙述。里程碑交付里用的 `../ITER-….md` 相对链接，整树平移后仍然有效，不改。
- **开放问题 1（已定）**：历史归档不改写正文；会 404 的活指针才改。CHANGELOG 按这句话拆——「当时做了什么」的叙述保留旧名，「去哪找这份交付」的路径改新名。
- **开放问题 2（已定）**：本轮只在 butler 仓自己搬家。已部署项目的动作登记给 v4.0.0，本轮不写配方、不跑升级器。候办改名在 `.ai/` 内部，现有 `[rename]` 标签能表达；仓根 `deliveries/` 搬进 `.ai/` 跨出了 `[rename]` 的硬校验（源路径第一段不是 `.ai/`），必须等 R14 补「移动」动作，R15 写进配方。
- **hook 黑名单故意不动**：`templates/hooks/lib/io.py` 里 `deliveries/` 这条豁免是给**还没升级的已部署项目**留的——它们磁盘上仓根还有 `deliveries/`。新路径 `.ai/deliveries/` 已经被 `.ai/` 这条前缀豁免覆盖。动 hook 源文件会撞上「hook 树摘要必须等于当前 VERSION 对应 tag」那条 CI，R8 已经踩过；本轮不碰进摘要的 hook 文件。
- **部署只建 `.ai/`**：现在 init 会在项目根建 `.ai/` 和 `deliveries/` 两个目录。搬家之后 `deliveries` 变成 `.ai/` 的子目录，和其他子目录一样按需产生（第一次收口时建），部署不再在仓根建它。
- **不顺手清 `.ai/project/workspaces.md`**：R3 把这份工作区地图的去留写到过 R9，但它不是本路线项的范围。路径名确实别扭，留给以后，本轮不加第三条搬家。

## Scope

- `git mv` `.ai/milestone-backlog/` → `.ai/backlog/`，10 份草稿文件名不变；同步闪念口去向、待办区索引、`tools/intake/`、审计、规则、测试。
- `git mv` 仓根 `deliveries/` → `.ai/deliveries/`，保留 `milestones/` 子目录和平铺的迭代交付；同步规则、脚本、工具、测试、台账交付列（含冷分片）、CHANGELOG 找文件的链接、冷启动读序投影。
- 部署协议、`/butler:init`、rule-card 改为只建 `.ai/`；`.ai/backlog/` 与 `.ai/deliveries/` 按需产生。
- 冷启动一致性自检第 3 条改为「按台账交付列相对项目根解析文件在不在」，不再写死 `deliveries/<链接>`。
- 改完后用可重跑扫描锁住：活跃面不再出现旧目录名；新路径在规则、工具、台账里都在场。
- 按 `migration-schema.md §5` 把对已部署项目的影响写进 `.ai/MILESTONE.md` 范围演进记录，明确指向 R14 / R15。
- `.ai/OVERVIEW.md` 重算；CI 与项目状态审计全绿。

## Open Questions / Risks

- **~~历史归档改不改~~（已定）**：活指针改、冻结快照不改。见 Current Understanding。
- **~~已部署项目本轮迁不迁~~（已定）**：本轮只登记。候办改名可走现有 `[rename]`；交付搬家等 R14 的移动动作。
- **风险 · 冷分片台账必须一起改**。审计会把热表和 `.ai/history/iterations/` 冷分片拼起来，再按「交付」列当相对路径去找文件。只改热表、不改 ITER-0001～0100 那两片，审计会报一百来条交付丢失。改完分片还要重算 state-ledger 的哈希回执，否则下一轮 `check` 会红。
- **风险 · 漏改一处活引用就是断指针**。交付树 272 个文件、规则和测试几十处。防线是分类扫描 + 审计 + 完整 CI，不是人眼。
- **风险 · 改 rule-card 和两份入口模板会流进已部署项目的 `CLAUDE.md` / `AGENTS.md`**。本轮必须在范围演进记录里写明 v4.0.0 配方要含 `[regen-entrypoints]`，不能靠「以后都写新路径」了事。
- **风险 · 已部署项目在 R15 之前仓根仍有 `deliveries/`**。所以 hook 黑名单那条旧豁免要留着。Butler 仓自己搬家后，这条豁免在本仓不再被用到，但不构成漂移。
