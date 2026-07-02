# 分级置信 + 代理验证 + 依赖感知准入：verify 置信档 + testing 代理验证 + dangerous 无人残余处置

> ITER-0022 · 迭代交付（小版本）· 收口 2026-07-02 · MILE-0002 R2 · ⚠️ 危险模式（P2/P3 自审门 self-ACK，P4 自治 + P5 独立复核）

## 本次交付目标

- MILE-0002 第二个路线项 R2（扁平原子）。承 R1「自动道 / 人测道」二分。
- 现状三处缺口：① R1 的分道只有二值（能自动 / 不能自动），缺"自动到什么程度"的**置信刻度**；② 没给"本来要人看的项怎么用弱自动检查顶上"的手段；③ `/dangerous` 无人值守下**人测残余会永久阻塞或被草率假绿**，没有处置规约。
- 目标：叠**分级置信**（可靠 / 弱 / 待人）+ **代理验证**（把感知项拉回自动道·弱档）+ **依赖感知准入 + 无人残余处置**（不阻塞入账 / 卡下游不硬闯 / 绝不假绿）。

## 已完成内容

- `verify-schema.md`：§4 分道回填升级为**道 + 置信档合并记法** `(auto·可靠)` / `(auto·弱)` / `(human·待人)`，新增「分级置信」bullet 给三档判据 + 红线；§3 模板 `AC Status` 示例改带置信档、「人测道小结」触发条件对齐为"存在 human·待人 档 AC 时"。既有 6 必填字段与 §4 位置不变（护 `changelog-schema §4` 引用）。
- `testing-strategy.md`：§3 新增 **§3.1「代理验证」**——弱自动检查手段清单（截图对基线 diff / VLM 判读截图 / 启发式断言）+ earned `弱` 档留自动道 + 诚实边界（不冒充可靠绿）+ 置信三档统一口径；§3 判定纪律补"归人测道前先问能否造弱检查"。
- `dangerous-engine.md`：§7 新增 **§7.4「无人残余处置与依赖感知准入」**——不阻塞异步入账 / 弱验证顶上 / 准入闸（叶子残余续跑 vs 卡下游残余三处置）/ 红线绝不假绿 + 与 §8 熔断的边界厘清；§8 补"待人残余异步入账、不阻塞自治继续"呼应句闭环。
- 接线：`rule-card.md` 自动化优先行补代理验证 / 弱不假绿半句；`Coder/README.md`（30_Quality_Gate 组描述 + dangerous-engine 描述 + verify-schema 描述）、`HUMAN_GUIDE.md`（两注释）同步；`.ai/PROJECT.md` 现行约束前滚。

## 关键变更 / 用户可感知变化

- 验证结论从"通过 / 未通过"升级为带**置信刻度**：`可靠`（确定性）/ `弱`（代理验证）/ `待人`（机器不可测残余），一眼看清"多大把握"。
- 感知 / UI 项多了条出路：能造弱检查（截图 diff / VLM 判图）就归**自动道·弱档**，进一步压缩人测残余——但**弱不冒充可靠绿**。
- `/dangerous` 长程自治遇人测残余不再僵死：叶子残余记账续跑、卡下游残余走准入闸（弱验证顶 / 砍分支 / 不具准入资格交还），**红线绝不假绿**。
- 向后兼容：纯规则正文增量（新增 §3.1 / §7.4 + 既有节追 bullet），未 renumber、未动状态机 / 四件套脊柱 / hook / correction-contract；R1 分道二分字段不重构。

## 高层影响范围

- 改（核心）：`Coder/20_Workflow_Lifecycle/verify-schema.md`、`Coder/30_Quality_Gate/testing-strategy.md`、`Coder/65_Extension_Dangerous/dangerous-engine.md`。
- 改（接线）：`templates/rule-card.md`、`Coder/README.md`、`HUMAN_GUIDE.md`。
- 前滚：`.ai/PROJECT.md` 现行约束。
- 没碰：P1-P5 状态机、四件套字段脊柱、hook 体系、correction-contract、「交付自测」桥（R3）、等待-回收-续跑（R4）。

## 验证方式与结果摘要

- 8 条 AC 全部满足（逐项见 VERIFY_REPORT），**全属自动道·可靠档**（读文件 / grep 可复现），无弱档、无待人残余 →「人测道小结」按规则省略。这本身即 R2 口径的自证 dogfood。
- **危险模式 P5 §7.3 独立复核**：fresh-context general-purpose 子 agent、spec-only 逐 AC + 多维（一致性 / dogfood 可读性 / 边界 / 范围）、验证者≠实现者。结论：**8/8 confirm、0 Must Fix、0 Should Fix、1 Nit**（TECH_PLAN 把 README 落点误标 §99/§132/§134=行号且易误读，已就地改具名描述项消解）。
- 引用对账：`/usr/bin/grep` 确认 `testing-strategy §3.1`、`dangerous-engine §7.4` 章节号存在；三处对置信三档定义一致；`changelog-schema → verify-schema §4` 引用未失效（§4 未移位）。

## 已知剩余风险 / 延后事项

- 置信档记法叠进 lane 后信息密度略升；独立复核判定仍清晰可读，后续模板若变复杂可再评估。
- 分级置信 / 代理验证 / 准入闸均非 hook 机械门，靠纪律 + 收口自检兜底（与 butler 既有"提交规约 / 自动化优先均非机械门禁"同源，非新增风险）。
- R3-R5 边界：本迭代只定"无人场景"残余处置（异步入账）；有人值守的残余回传桥（交付自测）显式留 R3，其等待-回收-续跑接线留 R4。

## 引用

- 归档四件套 + 切片：`.ai/iterations/ITER-0022/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 核心改动：`Coder/20_Workflow_Lifecycle/verify-schema.md`（§4 置信档 / §3 模板）、`Coder/30_Quality_Gate/testing-strategy.md`（§3.1 代理验证）、`Coder/65_Extension_Dangerous/dangerous-engine.md`（§7.4 无人残余处置 + §8 呼应）
- 接线改动：`templates/rule-card.md`、`Coder/README.md`、`HUMAN_GUIDE.md`
- 前滚：`.ai/PROJECT.md`
- 危险模式审计：`.ai/RUN_LOG.md`（ITER-0022 段）
