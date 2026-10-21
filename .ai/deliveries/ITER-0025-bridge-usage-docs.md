# 人测桥收尾：部署侧调用文档 + 人类使用说明 + 真样例端到端 dogfood

> ITER-0025 · 迭代交付（小版本）· 收口 2026-07-02 · 所属 MILE-0002（R5，收尾）· /dangerous 危险模式自治执行（P2/P3 用户 ACK，P4→收口自治）

## 本次交付目标

- MILE-0002 收尾 R5：前四项把交付自测桥（R3）和它的 SOP 闭环协议（R4）都造好了，但**"外面怎么用"是空的**——部署项目的 AI 不知道怎么定位/调用 butler 驻留桥，人也不知道弹出来的页面是什么；且桥从没按"外部调用形态"真跑过一遍。R5 收这个尾。
- scope 对账：R5 原列的"无人异步入账 + 准入闸"已由 R2（`dangerous-engine §7.4`）交付，本轮**只交叉引用、不重复实现**。

## 已完成内容

- **部署侧文档**：`mcv-deployment.md` 新增 §6「butler 驻留工具调用」——定义驻留工具类别（存 butler 仓、不拷进目标项目、按 `$BUTLER` 路径传参调用，与 hook 副本方向相反）+ 桥的具体调用形态 + `.ai/human-test/` 落点（建议 gitignore）+ 无人岔口指 §7.4；路径发现复用 §0，字段/语义只引用三处真源不重抄。
- **人类侧文档**：`HUMAN_GUIDE.md §5` 新增「人测回环（交付自测桥）」——人类视角讲清何时弹浏览器页面、四态（通过/未通过/延后处理/跳过）各自含义与 AI 后续动作、提交即续跑、无人值守下不弹页面而记欠债不假绿。
- **真 dogfood**：按外部 CLI 形态起桥（`node bridge.js example/manifest.json --no-open --port 0 --out …`）→ POST 四态 → 桥 exit 0 自退 → 读 results → 四态路由分派，**DOGFOOD PASS**；样例 `example/manifest.json` 补齐为 4 项（四态齐全），兼作 fixture 与使用示例，README 补外部调用样例指引。
- **注册 + 收尾**：`Coder/README.md` 登记 §6；PROJECT 前滚；MILESTONE R5→closed。

## 关键变更 / 用户可感知变化

- 部署项目的 AI 现在有明确文档知道**怎么调用 butler 驻留桥**（传 manifest 路径、不拷副本），不再是"协议有、用法空"。
- 人类用户能在 HUMAN_GUIDE 读到**那个弹出来的页面是什么、四态怎么选**，不再一脸懵。
- 桥第一次按真实"外部调用形态"端到端跑通并留证据，闭环从"规则正文断言"升级为"真跑验证"。
- 向后兼容：全是文档新增 + 样例数据补一项，未动桥体代码、四态机器码、SOP 语义、hook、状态机、四件套 schema、根 CHANGELOG/VERSION。

## 高层影响范围

- 新增（章节）：`mcv-deployment.md §6`、`HUMAN_GUIDE.md §5 人测回环`。
- 改：`tools/delivery-selftest/example/manifest.json`（补 MT-4）、`tools/delivery-selftest/README.md`（外部调用样例）、`Coder/README.md`（登记 §6）。
- 收口机制：PROJECT 前滚、MILESTONE R5→closed、ITERATIONS 翻转。
- 没碰：`bridge.js`/`render.js` 代码、四态机器码、`human-test-bridge.md` SOP 语义、`dangerous-engine §7.4`（只引用）、hook、四件套 schema、状态机、根 CHANGELOG/VERSION。

## 验证方式与结果摘要

- **9/9 AC 通过**。危险模式 §7.3：P5 升格完整审查 + **独立复核**（fresh-context 子 agent，验证者≠实现者），自写驱动**独立复跑 dogfood**（端口 49907、exit 0、summary{pass:1,fail:1,defer:1,skip:1}），**0 Must Fix**。
- dogfood：外部 CLI 形态四态齐全回路 DOGFOOD PASS；工具自测 `test/bridge.test.js` **8/8**（补 MT-4 无回归）。
- scope 守恒复核：diff 仅 7 文件，§7.4 / 桥代码 / 机器码 / SOP 语义 / hook / schema / VERSION 均未改——无越界。

## 已知剩余风险 / 延后事项

- Should Fix（不阻断）：样例落点偏离已 ACK 的 P3——计划 `sample/manifest.sample.json`，实现复用工具既有 `example/manifest.json`（DRY、避免目录双份漂移）。冻结 TECH_PLAN 按纪律不改、仅留痕，不影响任一 AC。
- dogfood 是 headless 程序化提交（本环境无真人浏览器），真人点选层由 R3 Playwright 弱档覆盖，二者互补。
- 桥调用依赖部署项目能解析 `$BUTLER` + 有 Node 运行时（文档已明写前置）。
- 本轮按用户指令只自治到收口、**未提交推送 / 未切版**；MILE-0002 五路线项全 closed，聚合发布（v1.7.0 + 根 CHANGELOG 聚合 ITER-0021~0025 + 里程碑级交付）留作后续。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 切片：`.ai/iterations/ITER-0025/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 改动：`Coder/20_Workflow_Lifecycle/mcv-deployment.md`（§6）、`HUMAN_GUIDE.md`（§5 人测回环）、`tools/delivery-selftest/example/manifest.json`、`tools/delivery-selftest/README.md`、`Coder/README.md`
- 审计轨迹：`.ai/RUN_LOG.md` ITER-0025
- 里程碑：`.ai/MILESTONE.md`（MILE-0002 R5，收尾路线项）
