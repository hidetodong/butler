---
状态: ack-frozen
ACK 日期: 2026-07-05
迭代: ITER-0026
里程碑: MILE-0003 R1
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 `dangerous-engine §5.1` 验收自审门），未经用户确认（ITER-0026，2026-07-05）。

# Goal

- 给 butler 帮手立名册：新建 `Coder/62_Extension_Agents/`（总述 + 复核完整定义），通用规矩 G1–G4 单源化，复核帮手三拆，注册进 `Coder/README`。目标细节见 `CONCEPT.md`，不重述。

# In Scope

- 新建 `Coder/62_Extension_Agents/overview.md`（总述）与 `independent-review.md`（复核完整定义）。
- 通用规矩 G1–G4 提炼进总述当唯一真源。
- 复核三拆：`60_review` 按性质分家（共享流程留原地 / 通用规矩上提总述 / 复核专有进 `independent-review`）+ 原地留指针。
- `dangerous §7.3` / `verify-schema §4` 的 G2 引用改指总述。
- `Coder/README.md` 注册新目录（目录结构 + 目录说明 + 读取顺序判断）。
- 顺手改准两处事实错：`AGENTS.md` 起源、Agent Skills 采用数加时间点。

# Out of Scope

- 不落"更新说明""查过时"两帮手的完整定义（R4）——但名册表先列占位。
- 不做工具层硬拦权限（留后续）。
- 不改 `/review` 触发方式与产出行为、不改 P1–P5 状态机 / 四件套字段 / hook。
- 不动知识文件夹本体（R2 起）。

# Acceptance Checklist

- [ ] AC1（功能·总述）: `62_Extension_Agents/overview.md` 存在，含帮手定义（帮手是什么）+ 通用规矩 G1–G4 + 名册表（列全三帮手，"更新说明""查过时"标 R4 待落）+ 触发式加载说明。
- [ ] AC2（功能·复核定义）: `independent-review.md` 存在，是一份中立定义（角色 / 输入 / 输出 / 禁止 / 隔离 / 权限），含复核专有内容（触发 / 隔离形态 / Checker 契约 / 断言核对 / 输出衔接），共享审查流程指回 `60_review`、不重抄。
- [ ] AC3（结构·三拆无丢无重）: `60_review` 按 CONCEPT 三拆清单分家——共享流程留原地、通用规矩上提总述、复核专有进 `independent-review`；每处留指针，无内容丢失、无两处并存正文。
- [ ] AC4（结构·G2 单源）: G2"叫不起来如实说"正文只在总述一处；`review-engine §6.4` 原正文改为回指总述；`dangerous §7.3`、`verify-schema §4` 引用目标从 `review §6.4` 改指总述；全仓 grep 无漏网仍指 `review §6.4` 的 G2 引用。
- [ ] AC5（结构·注册）: `Coder/README.md` 目录结构树 + 目录说明含 `62_Extension_Agents/`；读取顺序按"触发式加载、不进冷启动必读"处理（与其它扩展模块一致）。
- [ ] AC6（质量·分层合规）: 新增两文件 frontmatter 标 audience/scope；落点 `62`（非 `00` 层）；夹内文件零数字前缀；不破坏 SOP Core / Domain / Business 三层分工。
- [ ] AC7（质量·事实校准）: `AGENTS.md` 起源改为 Sourcegraph 的 Amp 团队发起（非 OpenAI）；Agent Skills 采用数加"截至 2026 上半年"时间点。
- [ ] AC8（质量·功能等价）: `/review` 的触发条件、Checker 契约、输出衔接、诚实 fallback 语义在重组后不变——逐条比对搬家前后语义无丢失、无行为改动。

# Verification Method

- AC1/AC2/AC5: 读新建 / 改动文件正文确认字段与内容齐全、指针可解析（确定性可复现）。
- AC3/AC4: grep 全仓核对——三拆各段落在目标文件、原地有指针；搜 `§6.4` / `review-engine §6.4` 确认 G2 引用无漏网、正文单源。
- AC6: 读 frontmatter + 目录层级确认；对照 `CLAUDE.md` 分层约束。
- AC7: grep `AGENTS` / `Skills` 确认措辞已改准。
- AC8: 搬家前后语义逐条对照（P5 独立复核重点核 refute）。

# Open Questions / Risks

- 风险：三拆是"带地址搬家"，butler 无机器手段发现两处写岔——靠 grep 对账 + P5 独立复核兜底。
- 风险：复核定义与 `60_review` 边界若切不干净，可能重复或丢失——AC3 专项核。
- 已定（承 CONCEPT 两默认）：总述只进 README 目录说明、不进冷启动必读；名册表先列全三帮手。
