# Verification Summary

> ⚠️ 危险模式：本迭代 P2/P3 由**用户显式 ACK**，ACK 后开 `/dangerous`，P4→P5→收口自治执行，P5 已跑独立复核（见下）。审计轨迹见 `RUN_LOG.md` ITER-0025。

- ITER-0025 R5（MILE-0002 收尾）：给交付自测桥补"外面怎么用"——`mcv-deployment.md §6` 新增 butler 驻留工具调用节、`HUMAN_GUIDE.md §5` 新增人测桥使用说明、按外部调用形态真 dogfood 四态齐全回路、样例固化 + 注册 + 收口前滚。
- 总体结论：**9/9 AC 通过**，可收口。文档类 AC=读文件确认（`auto·可靠`），dogfood AC=真跑外部调用回路（`auto·可靠`）。scope 守恒：§7.4（无人异步入账+准入闸）R2 已交付，本迭代仅交叉引用未重实现；桥体代码 / 四态机器码 / SOP 语义 / hook / 状态机 / 四件套 schema / 根 CHANGELOG / VERSION 均未动。

# AC Status
- [x] AC1 (auto·可靠) ✓ `mcv-deployment §6` 三点齐全：驻留工具类别（不拷副本、传参调用）+ 桥调用形态（`node $BUTLER/tools/delivery-selftest/bridge.js …`）+ `.ai/human-test/` 落点（建议 gitignore）；§6.1 复用 §0 路径发现不另造
- [x] AC2 (auto·可靠) ✓ §6 只引用三处真源（工具 README 契约 / human-test-bridge 语义 / dangerous §7.4 无人岔口），无 manifest/results 字段与四态机器码重抄
- [x] AC3 (auto·可靠) ✓ `HUMAN_GUIDE §5 人测回环` 覆盖何时弹 / 四态含义表 / 提交即续跑 / 无人不弹页面，人类用户视角
- [x] AC4 (auto·可靠) ✓ 新节位于 §5 扩展模式末、§6 常见问题前；既有子节未移位、无版本/里程碑段冲突
- [x] AC5 (auto·可靠) ✓ 按外部 CLI 形态真跑：起桥（端口 64928）→ POST 四态 → 桥 exit 0 自退 → 读 results.json → 路由分派 DOGFOOD PASS；证据本报告 Verification Results
- [x] AC6 (auto·可靠) ✓ results summary{pass:1,fail:1,defer:1,skip:1} 四态各≥1、state 全合法（独立复核复跑复现）
- [x] AC7 (auto·可靠) ✓ fixture `example/manifest.json`（4 项合法、自测契约校验过）+ 工具 README 补"外部项目调用样例"指引（落点偏离见 Remaining Risks）
- [x] AC8 (auto·可靠) ✓ `Coder/README.md` mcv-deployment 描述补登记 §6 驻留工具调用；§6 为已注册文件内部加节、无新文件隐式依赖
- [x] AC9 (auto·可靠) ✓ PROJECT 前滚 + MILESTONE R5→closed + 范围演进 + ITERATIONS 翻转 + 收口自检 5 不变量全绿（原子收口仪式步①-⑤，见 RUN_LOG close 条）

（无 `human·待人` 档 AC → 人测道小结整段省略。本迭代 9 条全 `auto·可靠`。）

# Verification Results
- AC1-AC4 / AC8：读 mcv-deployment §6（§6/§6.1/§6.2/§6.3）+ HUMAN_GUIDE §5 新节 + Coder/README L124 逐处确认；核对 §6 无字段级重抄、路径发现引 §0。
- AC5/AC6（dogfood·可靠）：`node tools/delivery-selftest/bridge.js example/manifest.json --no-open --port 0 --out /tmp/r5-results.json` **按外部 CLI 形态起子进程**（非 require 模块）→ 抓监听端口 64928 → `POST /submit` 四态（MT-1 pass / MT-2 fail / MT-3 defer / MT-4 skip）→ 桥进程 **exit 0** 自退 → 读 results.json `summary={pass:1,fail:1,defer:1,skip:1}` → 按四态路由表演示 pass=计入收口 / fail=进纠错 / defer=入账不阻塞 / skip=N/A 各归位，**DOGFOOD PASS**。工具自测 `test/bridge.test.js` **8/8**（含 example/manifest.json 契约校验，补 MT-4 无回归）。
- AC7：`example/manifest.json` 4 项合法（dogfood 已解析、自测第 8 项契约校验通过）；README「用法」后有"外部项目调用样例" + 指向 mcv-deployment §6 / human-test-bridge。
- AC9：见 Independent Review + RUN_LOG close 条；收口自检 5 不变量全绿。

# Gate Coverage
- 通用质量门禁：自动化优先——dogfood 用真跑证明（外部 CLI 形态 + POST 四态 + exit 0 + 读回 + 路由断言），不停在"文档写了就算"；无 UI 交互残余需人测（真人点选层 R3 Playwright 弱档已覆盖）。
- Active Profiles：无（规则仓文档 + 复用 R3 Node 工具），N/A。
- Tech Plan Alignment：DD1-DD8 兑现——§6 独立成节非塞 §5（DD1）、tools 抽象为驻留工具类别（DD2）、单一来源引用（DD3）、HUMAN_GUIDE 落 §5 人类视角（DD4）、dogfood 外部形态机械闭环（DD6）、Coder/README 按需微调（DD7）、发布延后（DD8）。**DD5 偏离**：样例落点由计划的 `sample/manifest.sample.json` 改为复用既有 `example/manifest.json`（DRY、避免目录增殖），偏离已记 Remaining Risks（冻结 TECH_PLAN 不改、留痕）。
- References Compliance：本轮无 `.ai/references/`，N/A。

# Independent Review
- 复核方式：fresh-context 子 agent（general-purpose，agentId a7122cd5560759a2d，验证者≠实现者），spec-only 逐 AC + 多维（一致性 / scope 守恒 / 单一来源 / 人类视角 / 文档-代码一致）+ 对抗探测（假绿 / 越界 / 文档不符）+ **自写驱动独立复跑 dogfood**（未用实现者脚本）。
- 独立复跑结论：端口 49907、POST 200、桥 **exit 0**、results `summary={pass:1,fail:1,defer:1,skip:1}`、工具自测 8/8——**DOGFOOD PASS**，非走过场非假绿。
- 逐 AC 裁决：**confirm 8 / refute 1**——refute=AC9（复核时 PROJECT/MILESTONE/ITERATIONS 尚零改动）；复核判定其为"P5 通过后的收口整仪式步"、非实现缺陷（同 ITER-0024 AC8 模式）。已于原子收口仪式步①-⑤补齐 → AC9 转 confirm，**9/9**。
- scope 守恒复核：diff 仅 7 文件，§7.4 / bridge.js / render.js / 四态机器码 / human-test-bridge SOP 语义 / hook / 四件套 schema / 根 CHANGELOG / VERSION **均未改**（example/manifest.json 系 fixture 数据、在 AC6/AC7 授权内）——**无越界**。
- 结论：**可收口**，0 Must Fix、1 Should Fix（DD5 落点偏离，已留痕）、2 Nit（README 样例省略 --port/--no-open 对真部署反而正确；fixture 用虚构项目名合理）。

# Remaining Risks
- **Should Fix（不阻断，按 §7.3 记此）**：样例 fixture 落点偏离已 ACK 的 P3——TECH_PLAN `DD5`/`Files to Change` 定 `tools/delivery-selftest/sample/manifest.sample.json`，实现改为复用工具既有 `example/manifest.json`（该文件早于本迭代存在但未文档化）。偏离动机=DRY、避免 `sample/` 与 `example/` 目录双份漂移，且 dogfood + 使用示例复用同一份更诚实。冻结 TECH_PLAN 按纪律不改，仅此留痕；不影响任一 AC 达成。
- dogfood 是程序化 POST（headless 模拟人提交），非真人点浏览器——本环境无真人交互，真人点选层由 R3 Playwright 弱档覆盖，二者互补不冲突。
- 桥调用依赖部署项目能正确解析 `$BUTLER`（§0 路径发现）+ 有 Node 运行时；文档已明写前置，跨环境 Node 缺失为已知外部依赖。

# Handoff / Next Step
- 本迭代闭合，进原子收口。北极星=ITER-0025 R5（单迭代）达成。
- 收口后 **MILE-0002 三路线项 R1/R2/R3/R4/R5 全 closed**，方向达成、可聚合发布（切版 v1.7.0 + 根 CHANGELOG 聚合 ITER-0021~0025 + 里程碑级交付）——本次按用户指令只自治到收口、**未提交推送 / 未切版**，发布节奏待用户拍板。
