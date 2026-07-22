# ITER-0079 · 多 PRD 引用、兼容迁移与人类指南

## Problem

- P2/P3/P5 仍只有单值 `prd_version`，无法表达一轮同时钉住需求 A v1.2 与需求 B v2.0。
- legacy PRD 的模块、索引和 `.archive/` 都在 `prd/` 根；目标集合要求它们进入唯一日期化 `prd_id` 子目录，但日期/语义身份不能由工具猜。
- 直接移动会让历史 `references/prd/<slug>.md` 指针失效；直接回写 closed AC 又破坏冻结历史。
- MILE-0009 明确要求人类只看一份指南就能盘点、迁移、验证和失败恢复，不能只留规则散文。

## Goal

- 建立多 PRD 钉版字段与确定性解析器；交付 legacy → collection 的零写 plan、事务 apply、兼容映射/回滚和独立迁移指南。

## In Scope

- `prd_refs` 多值钉版合同：每项含 `prd_id + prd_version + module_slugs`，P3/P5 继承同一真源。
- legacy 单值 `prd_version` 与旧 `references/prd/<slug>.md` 的只读兼容解析；新集合不得继续写 legacy 形态。
- 驻留迁移工具：inspect/plan/apply/verify/rollback，显式 `prd_id` 和标题，原始 bytes hash、事务目录切换、receipt、backup。
- 迁移项目级索引、单需求目录和 legacy 别名映射；扫描 MILESTONE、active/future、closed 迭代引用并分类报告，closed 零回写。
- `docs/prd-migration-guide.md` + HUMAN_GUIDE 入口，覆盖盘点、身份日期、MILESTONE/AC、验证与恢复。
- 隔离 fixture 覆盖 plan 零写、apply、重复执行、故障恢复、历史解析和坏输入。

## Out of Scope

- 不改 `prd-split`/status 的首切动作（R6），不改 `prd-update` 的确定性改版事务（R7）。
- 不自动猜首次进入日期、需求 slug、标题或把多个 legacy PRD 混成一个。
- 不回写 frozen/closed AC、TECH_PLAN、VERIFY 或归档；active 引用是否升级只报告。
- 不在本轮写 `WorkCode.nosync/apps`，真实项目 dogfood 留 R8 的独立授权与验证。

## Key Decisions

- 新集合用 `prd_refs` 列表作为钉版 SSOT；旧 `prd_version` 只作 legacy 单 PRD兼容，不允许两字段并存。
- 迁移身份参数必须由用户/既有证据显式给出；工具只校验日期化语法与冲突，不替用户造历史。
- 目录切换采用同父目录 staging + backup + rename；成功保留 receipt/backup，verify 绿后才允许用户清理备份。
- 历史兼容不靠回写：迁移 receipt 保存 legacy implicit ID 与新 `prd_id` 映射，resolver 结合旧 AC 的 `prd_version` 解析到 live 或 `<prd_id>/.archive/vN/`。
- 迁移按内容 hash 对账，失败恢复只恢复本次事务触及的 PRD 根。

## Risks

- Markdown frontmatter 多行列表需要清晰模板和解析器，不能依赖 PyYAML 才可验证。
- legacy 00_INDEX 格式存在历史变体；解析不确定必须拒绝，不能产生半迁移集合。
- symlink 兼容跨平台脆弱，因此兼容真源采用 receipt/resolver，不把 symlink 当唯一保障。
