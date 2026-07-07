---
状态: ack-frozen
ACK 日期: 2026-07-07
迭代: ITER-0032
里程碑: MILE-0003 R6
---

# AC_LIST — ITER-0032（MILE-0003 R6 部署种子 + 文件夹化迁移配方）

> 监督态自驱（用户"继续接下来的迭代"委托，非 /dangerous）。验收脊柱贯穿 P4→P5；全为规则文档改动，验证=读正文确认 + `git`/`grep` 核守恒，确定性可复现（auto·可靠）。

## 块1 · 部署种子

- **AC1**：`mcv-deployment §2` 的项目全貌产物条**两态化**——明写新项目采用 `.ai/project/` 知识文件夹（`00_INDEX` + 主题按需产生于首次收口前滚、回指本 schema 折叠机制）、单文件 `.ai/PROJECT.md` 标为遗留/暂态形态（老项目 + R8 前 butler 自身）。旧的"仅 PROJECT.md"单态描述被取代，非并列冗余。
- **AC2**：`mcv-deployment §2` 明确部署时创建**空** `.ai/project/` 目录（列入部署即建的目录集、与 `origin/` 同档），并显式说明它是**唯一在部署时即建的 `.ai/` 子目录例外**（`references/`/`iterations/`/`milestones/` 仍按需产生），例外理由=全貌产物之家、标记文件夹采用。守 §2"仅创建目录、不预置任何 `.md` 内容"——空目录不含 `00_INDEX` stub。
- **AC3**：`mcv-deployment §2` 写明 `00_INDEX` **不在部署时 stub**、首次收口前滚才生；空目录到首收口的暂态由冷启动**入口文件键控**兜底（不误触"读不存在的 00_INDEX"），与"单文件项目首收口前"同类暂态。`mcv-deployment` line 45 老项目升级补建指针指向 R6 文件夹化迁移配方（`migration-schema`），不再只指 `versioning §5` 的单文件回填。

## 块2 · 文件夹化迁移配方

- **AC4**：`migration-schema §4` 新增 typed 标签 **`[split]`**——定义=把 `.ai/` 下单文件产物按主题拆成文件夹（首例 `PROJECT.md → .ai/project/`），带**起始态校验**（旧单文件存在且目标文件夹未成形才动）+ **冲突即停退 ACK**（不覆盖），显式归入 §4"所有标签必须幂等"与 §5"漂移即停"契约。
- **AC5**：文档化 `PROJECT.md → .ai/project/` 迁移配方**形态**（`[rename]` + `[split]` + `[restamp]` 三步骨架）作为 R8 模板，附**条件式前向指针**指 R8/v2.0.0 切版时产出实例——**不硬编版本号**、不出现已成型的 `migrations/v2.0.0.md` 路径断言为"已存在"。
- **AC6**：**不写** `migrations/v2.0.0.md` 实例文件（`migrations/` 目录内容零新增）；规则内以"配方在切版时产出（`versioning-schema §6.3 步4`）、R8 落实例"表述，边界清晰不悬空引用未打 tag。

## 指针 / 守恒

- **AC7**：接线状态指针如实翻——`project-digest-schema §9` R6 路线项 待→已（规则层已备、注明 `v2.0.0.md` 实例仍 R8）、§9 header `R3/R5 已接线` → `R3/R5/R6 已接线`、§150 `[split]` 表述与 §4 新定义一致（不再是"未定义"隐含）；`.ai/PROJECT.md` 收口前滚 R6 指针 待→已（R8 仍待）。`README §读取顺序` 部署目录清单补 `.ai/project/` 空种子（与 §2 一致）。
- **AC8**：scope 守恒——改动集限于 `mcv-deployment.md` / `migration-schema.md` / `project-digest-schema.md`（§9+§150）/ `Coder/README.md` + `.ai/` 台账与 `.ai/PROJECT.md` 前滚；**无** `migrations/v2.0.0.md` 新增、**无** butler 自身实体迁移、**无** `VERSION`/`CHANGELOG` 切版改动、**无** R3 折叠必做/第 6 不变量语义改动、**无** R5 读序第一读改动、**无** hook 改动、**无** rename。
