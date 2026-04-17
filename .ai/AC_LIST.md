# Goal

- 新增 butler 升级命令：`/butler-upgrade`（及语义触发），基于保护区标记 + 差异检测，把老项目同步到最新版 butler。

# In Scope

- 新建 `Coder/20_Workflow_Lifecycle/butler-upgrade.md`（升级协议）
- 修改 `templates/CLAUDE.md.template` 加保护区标记
- 修改 `mcv-deployment.md § 3` 部署时建立保护区标记
- 修改 `logic-protocol.md § 4` 注册新命令
- 修改 `Coder/README.md` 注册新文件

# Out of Scope

- Bucket H（profile 目录重组）
- 不对已部署项目的 `deliveries/` 历史做任何处理
- 不引入 butler 版本戳（决策 β 已定）

# Acceptance Checklist

- [ ] **U-1** 保护区标记方向，方案待拍板
- [ ] **U-2** 老项目（无保护区标记）首次升级策略，方案待拍板
- [ ] **U-3** `.ai/` 结构升级范围粒度，方案待拍板
- [ ] **U-4** 新建 `butler-upgrade.md` 包含完整 6 段结构（目标 / 触发条件 / 侦察 / 对比与呈报 / 执行 / 验证与回退）
- [ ] **U-5** `CLAUDE.md.template` 加入保护区标记 HTML 注释
- [ ] **U-6** `mcv-deployment.md § 3` 部署步骤生成保护区标记
- [ ] **U-7** `logic-protocol.md § 4` 注册 `/butler-upgrade` 命令与语义触发词
- [ ] **U-8** `Coder/README.md` 目录结构 + "其中："说明 双处注册

# Verification Method

- **U-4**：新 schema-level 文件通读，6 段齐全；frontmatter OK。
- **U-5**：`grep 'butler-managed' templates/CLAUDE.md.template` 命中保护区标记。
- **U-6**：`grep 'butler-managed' mcv-deployment.md` 命中部署步骤说明。
- **U-7**：`grep 'butler-upgrade' logic-protocol.md` 命中 § 4 Semantic Triggers 区；`grep '升级 butler\|同步到新版' logic-protocol.md` 命中语义触发词。
- **U-8**：`grep 'butler-upgrade' Coder/README.md` 命中 2 处。

# Open Questions / Risks

## ❓ 待拍板 - U-1 保护区标记方向

### 方案 1 — `<!-- butler-managed -->` 标记 butler 区

```markdown
<!-- butler-managed -->
# 项目工程协作规则
...（rule-card 内容 + 深度阅读指针）
<!-- /butler-managed -->

## 项目特定约束
- 用户自己加的约束写这里
```

- 升级时：**只替换 butler-managed 区块**内容，外部保留。
- **优点**：butler 区边界明确；用户能清楚看到 "这里是 butler 管的"。
- **缺点**：用户若在 butler 区内部加了自定义内容（例如在"完整规则参考"后加一句备注），升级会覆盖之。

### 方案 2（推荐）— `<!-- user-managed -->` 标记用户区

```markdown
# 项目工程协作规则
...（rule-card 内容 + 深度阅读指针）

<!-- user-managed -->
## 项目特定约束
- 用户自己加的约束写这里
<!-- /user-managed -->
```

- 升级时：**保留 user-managed 区块**原样，外部完全按最新模板覆盖。
- **优点**：语义更清晰 —— "你管你的，我管我的"；用户加内容只需要放到标记区内就不会丢。
- **缺点**：butler 区没有边界标记，升级算法需"删到文件结尾、再把 user-managed 区接回来"。

### 方案 3 — 双向标记（两者都有）

- butler 区和用户区各有标记。
- **缺点**：模板变复杂；对升级算法无额外收益。不推荐。

---

## ❓ 待拍板 - U-2 老项目（无保护区标记）首次升级策略

老项目的 `CLAUDE.md` 部署时还没有保护区标记（这次 feature 之后部署的才有）。首次升级如何处理？

### 方案 a — 按章节识别

- 按章节名识别：`## 项目特定约束` 整章视为用户区；其他全视为 butler 区。
- **优点**：无需用户干预，自动完成。
- **缺点**：若用户改了章节名（如 "## 本项目约束"），识别失败。

### 方案 b（推荐）— 升级前备份 + 交互 ACK

- 升级前自动备份旧文件（`CLAUDE.md.backup-YYYYMMDD`）；
- AI 对比新旧文件，列出差异清单给用户 ACK："原文件的这些段落 butler 不认识，判断是你加的；是否保留？"
- 用户 ACK 后按决策执行。
- **优点**：零损失、用户全掌控；并且本次升级后新文件含标记，下次升级自动走保护区路径。
- **缺点**：需要用户参与一次。

### 方案 c — 完全重建

- 不保留旧文件任何内容，重新跑基地车部署；
- 用户需手工把项目特定约束粘回新文件。
- **优点**：最简单。
- **缺点**：老项目若累积了 local-constraints 等内容，会不便。

---

## ❓ 待拍板 - U-3 `.ai/` 结构升级范围粒度

### 方案 i — 仅命名升级

- 只处理文件重命名（如 `SESSION_HANDOFF.md` → `02_SESSION_HANDOFF.md`）；
- 内容不动。

### 方案 ii（推荐）— 命名 + schema 字段补齐

- 除命名升级外，还对 `.ai/local-constraints.md` 按新 `local-constraints-schema.md` 补齐缺失必填字段（如缺 `Active Profiles` 则提示用户补）；
- CHANGELOG / BUG_LOG 等累积型文件不动。

### 方案 iii — 全面升级（不推荐）

- 连 CHANGELOG / BUG_LOG 格式也升级。
- **缺点**：破坏历史数据。

---

## 风险

- 本 feature 引入后，必须同步升级 butler 自身（因为规则仓自己的部署文件也未用保护区标记）。本轮不做 butler 仓自身的 dogfooding 迁移，作为 follow-up。
- `.ai/local-constraints.md` 按方案 ii 补齐时，若旧文件字段集完全不对，自动补齐可能产生误判。方案 ii 会要求"模糊匹配时交互确认"。
- 老项目升级需用户参与一次（方案 b），不是零人工成本。

---

# 请回复

3 个方案：`U-1: 2, U-2: b, U-3: ii` 就是全部走推荐。或者告诉我你的组合。
