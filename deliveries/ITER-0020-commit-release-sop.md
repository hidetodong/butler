# 提交与切版 SOP：提交规约成文 + 切版 git 仪式补全

> ITER-0020 · 迭代交付（小版本）· 收口 2026-07-02 · 独立迭代（所属 milestone —）· 有监督标准模式

## 本次交付目标

- 用户诉求：在仓库内做一份"提交切版"的 SOP。
- 现状两处缺口：① 提交约定**有实践、无规则**——全仓零成文，但 git 历史高度一致（`type(scope): 描述 (ITER-NNNN)` + `chore(release)` + `Co-Authored-By`）；② 切版流程 `versioning-schema §5` 只到语义层（定 bump / 改 VERSION / 加 CHANGELOG / 写 migration / 打 tag），**没落到 git 操作层**。
- 目标：把"日常提交规约 + 切版 git 仪式"补成一份可照做的 SOP，就地扩写进 `versioning-schema.md`。

## 已完成内容

- `versioning-schema.md` 新增 §5「提交规约」：commit message 格式 `type(scope): 中文描述 (ITER-NNNN)`（7 类 type + scope 口径 + 中文描述 + 迭代号尾注）、发布专用 `chore(release): vX.Y.Z — 聚合 ITER-A~B (级别)`、何时提交 / 一次装什么、`Co-Authored-By` 署名 trailer、并显式声明**非 hook 机械门禁**。
- 原 §5 切版流程顺移 §6 并扩到 git 操作层：§6.1「提交 ≠ 切版」两路径、§6.2 切版前预检（复用冷启动一致性自检 5 不变量）、§6.3 语义 5 步 + git 精确序列（add→commit→tag→push）、§6.4 切版后自检（VERSION==tag==CHANGELOG 顶条）；里程碑发布引用 `milestone-schema`。
- 原 §6-8（部署戳 / 升级 gap / 边界）顺移 §7-9，内部 §引用同步修正。
- frontmatter title 改「提交与版本治理协议」、scope 扩含提交规约 + 切版仪式。
- 指针同步：`Coder/README §139` / `CLAUDE.md` VERSION 行 / `HUMAN_GUIDE`；外部 §引用顺移修正 `migration-schema` / `butler-upgrade` / `mcv-deployment`。

## 关键变更 / 用户可感知变化

- 现在有一份可照做的提交规约：每次 commit 该写什么格式、release 该用什么形态，从"看历史模仿"变成"照规则写"。
- 切版从"知道要改哪些文件"升级为"知道每一步敲什么 git 命令 + 切版前后各自检一遍"，降低发版漂移。
- 明确"提交 ≠ 切版"——日常迭代收口只 commit+push（不切 tag），发版是按需聚合动作，不再混淆。
- 向后兼容：纯规则正文扩写 + 指针同步，未动 hook 代码 / 四件套字段 / 状态机 / VERSION 数值 / 根 CHANGELOG 已有条目。

## 高层影响范围

- 改（核心）：`Coder/20_Workflow_Lifecycle/versioning-schema.md`（新增 §5 + 扩写 §6 + 顺移 §7-9 + frontmatter）。
- 改（顺移引用）：`migration-schema.md`、`butler-upgrade.md`、`mcv-deployment.md`（versioning-schema §编号引用修正）。
- 改（指针）：`Coder/README.md`、`CLAUDE.md`、`HUMAN_GUIDE.md`。
- 前滚：`.ai/PROJECT.md` 现行约束。
- 没碰：`templates/rule-card.md`（裁决不收录）、`CLAUDE.md.template`、四件套 schema、hook 体系、`VERSION`、根 `CHANGELOG.md`。

## 验证方式与结果摘要

- 11 条 AC 全部满足（逐项见 VERIFY_REPORT）。
- AC4 抽 6 条历史提交逐条套规约，全含 `Co-Authored-By` trailer、零冲突。
- `git diff --name-only` 核对不变量：VERSION / 根 CHANGELOG / rule-card / CLAUDE.md.template / 四件套 schema / hook 全部未碰。
- 全仓 `versioning-schema.md §N` 引用复查：外部 6 处已正确指向 §6/§7/§8，无旧指向残留；versioning-schema §1-9 编号连续。
- rule-card 裁决=不改（提交规约属纪律类，非产物链硬门 / 非封闭枚举，收录会稀释 rule-card 定位）。

## 已知剩余风险 / 延后事项

- Should Fix（不阻断）：提交规约作用域限 butler 仓自身，目标项目提交规约推广未做（已在 §9 边界声明，留后续按需）。
- 提交规约非机械门禁，靠纪律 + 收口自检兜底（与"会话起始必读""切版靠纪律"同源同险，非新增风险）。
- 本迭代只写 SOP，未实际切版；MILE-0001 聚合发布仍待定，与本迭代解耦。

## 引用

- 归档四件套 + 切片：`.ai/iterations/ITER-0020/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 核心改动：`Coder/20_Workflow_Lifecycle/versioning-schema.md`（§5 提交规约 / §6 切版流程）
- 联动改动：`Coder/20_Workflow_Lifecycle/migration-schema.md`、`butler-upgrade.md`、`mcv-deployment.md`、`Coder/README.md`、`CLAUDE.md`、`HUMAN_GUIDE.md`
- 前滚：`.ai/PROJECT.md`
