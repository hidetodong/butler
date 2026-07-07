> 活跃迭代 ITER-0032（MILE-0003 R6，部署种子 + 文件夹化迁移配方）· active · 2026-07-07

本文件是**当前活跃迭代**的对象级变更流（ADD/EDIT/DELETE）。收口时归档至 `iterations/ITER-0032/CHANGELOG.md`。上一迭代 ITER-0031 的切片见 `iterations/ITER-0031/CHANGELOG.md`。

## ADD

- `migration-schema.md §4`：新增 `[split]` typed 标签（把 `.ai/` 单文件产物按主题拆成知识文件夹，首例 `PROJECT.md → .ai/project/`；起始态校验 + 冲突即停退 ACK）（AC4）。
- `migration-schema.md §6`：新增"文件夹化配方形态（R6 备、R8 产实例）"条——`[rename]`+`[split]`+`[restamp]` 三步形态 + 实例 `migrations/v2.0.0.md` 留 R8 切版产、R6 不预落（AC5/6）。
- `mcv-deployment.md §2`：新增部署即建**空** `.ai/project/` 知识文件夹种子说明（唯一部署即建的 `.ai/` 子目录例外、00_INDEX 不 stub·键控入口文件兜底）（AC2/3）。

## EDIT

- `mcv-deployment.md §2` 全貌产物条：从单态"仅 PROJECT.md"改写为**两态**（新项目 `.ai/project/` 文件夹 / 单文件 `.ai/PROJECT.md` 遗留暂态）+ line 45 老项目升级指针指 R6 文件夹化配方（`migration-schema §4`）、实例产于切版（`versioning §6.3 步4`）（AC1/3）。
- `project-digest-schema.md §9` header：`R3/R5 已接线` → `R3/R5/R6 已接线`；R6 路线项 待→已（规则层已备，注明 `v2.0.0.md` 实例仍 R8）（AC7）。
- `Coder/README.md` 部署目录清单行：补空 `.ai/project/` 知识文件夹种子（与 §2 一致）（AC7）。
- `context-persistence.md §冷启动读序`（P5 MF-1 驱动）：line 124 文件夹分支补**入口文件 `00_INDEX.md` 存在性判据守卫**（空种子暂态→缺全貌产物倒推、不读空 00_INDEX）+ line 130 兜底句点名"空 `.ai/project/` 种子"为缺全貌产物一种。**为 R6 新引入的空种子暂态补冷启动安全守卫，不改 R5 两态语义**（见 VERIFY_REPORT §边界校正）。
- `.ai/PROJECT.md`（收口前滚，收口步④落）：知识文件夹条 R6 指针 待→已（R8 仍待）（AC7）。

## DELETE

- 无（无删除 / 无 rename；`migrations/` 零新增，AC6/8）。
