> 提交与切版 SOP：提交规约成文 + 切版 git 仪式补全 · closed · 2026-07-02

## ADD
- `versioning-schema.md §5` — 新增「提交规约」节：commit message 格式 `type(scope): 中文描述 (ITER-NNNN)`、发布 `chore(release)` 形态、何时提交 / 一次装什么、非 hook 门禁声明、`Co-Authored-By` 署名 trailer → AC1, AC2, AC3

## EDIT
- `versioning-schema.md` frontmatter — title 改「提交与版本治理协议」、scope 补提交规约 + 切版仪式 → AC8
- `versioning-schema.md §6`（原 §5 切版流程）— 扩到 git 操作层：§6.1 提交≠切版两路径 / §6.2 切版前预检（复用冷启动一致性自检 5 不变量）/ §6.3 语义 5 步 + git 精确序列 / §6.4 切版后自检；里程碑发布引用 `milestone-schema` → AC5, AC6, AC7
- `versioning-schema.md §7-9`（原 §6-8 部署戳 / 升级 gap / 边界）— 顺移编号 + 内部 §引用（§5→§6）修正 + §9 边界补"提交规约靠纪律" → AC11
- `migration-schema.md §47/§51` — versioning-schema §引用顺移修正（§5→§6、§7→§8）→ AC11
- `butler-upgrade.md §45/§77/§145` — versioning-schema §引用顺移修正（§7→§8 ×3）→ AC11
- `mcv-deployment.md §87` — versioning-schema §引用顺移修正（§6→§7）→ AC11
- `Coder/README.md §139` — versioning-schema 一句话描述补提交规约 + 切版 git 仪式 → AC9
- `CLAUDE.md` — VERSION 行引用补提交规约 → AC9
- `HUMAN_GUIDE.md` — versioning-schema 注释补提交规约 + 切版仪式 → AC9
- `.ai/PROJECT.md` 现行约束 — 补提交规约一句（收口前滚）→ AC10

## DELETE
- 无
