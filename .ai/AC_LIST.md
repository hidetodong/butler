---
状态: ack-frozen
ACK 日期: 2026-07-30
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0097

修订记录: 2026-07-30 · P3 逐节测算后把 AC5 体积区间由 4400–4900 改为 4100–4700——原区间参照的试压稿只压了「把话说顺」开头一句，未计入该节四条规矩的措辞收紧，下限估高约 300 B。不改变范围、不增删 AC 条目。
修订记录: 2026-07-30 · 撤销上一条，AC5 区间恢复为 4400–4900。上一条的依据「把话说顺非例子部分可再砍一半」在 P4 逐条核查时不成立——该节剩余内容均有独有语义，硬砍会违反 AC4。P4 实测 4753 B，落在原始区间内，且与 P1 拍板时选项里写明的「约 4700 B」相差 53 B。原始区间本就正确，是上一条修订错了。不改变范围、不增删 AC 条目。

## Goal

- 在规矩语义零改动、例子零删改的前提下，去掉仓根 `communication-style.md` 里的冗余表述（元说明、跨节重复、自相矛盾的散文铺垫），并守住它与 `artifact-style.md §2` 的概念对齐。

## In Scope

- 改写 `communication-style.md` 的非例子正文：压缩引言块的元说明；删除基调 / 详略 / 抓重点三节之间重复的规矩表述；重写「把话说顺」开头的散文铺垫；收紧「别急着抛选择菜单」与「结尾决策块」的措辞。
- 保留全部 9 个 H2 小节（含标题文字与顺序），保持三节分立不合并——已在 P1 由用户拍板。
- 修正既有漂移：`.ai/project/capabilities.md:110` 把本文件记作「8 节」，实际自 v2.10.0 加「把话说顺」后已是 9 节。

## Out of Scope

- 不改任何一条规矩的语义，不新增规矩。
- 不删、不改写、不合并任何一组 ❌/✅ 例子。
- 不动 `scripts/setup.sh` 与 `scripts/configure-global-install.py` 的 `@import` 路径，文件名与仓根位置不变。
- 不动 `templates/`，不下发目标项目；目标项目 `.ai/` / `deliveries/` / `origin/` / `CLAUDE.md` / `.claude/hooks/` 零结构变化。
- 不回溯改写 `CHANGELOG.md:139`（ITER-0046 发布史记的是当时事实的 8 节，历史不追溯）。
- 不动 `artifact-style.md` 本身及 butler 体系内其他风格真源。

## Acceptance Checklist

- [ ] AC1: 7 行 ❌/✅ 例子逐字保留——原版第 24/26/28/30/39/40/46 行的例子内容在新版中完全一致（允许行号变化，不允许任何字符增删改）。
- [ ] AC2: 9 个 H2 小节全部保留，标题文字与出现顺序均不变（基调 / 详略 / 抓重点 / 说人话（简短 ≠ 好懂）/ 把话说顺（短 ≠ 碎）/ 别急着抛选择菜单 / 格式 / 结尾决策块（需要我拍板时）/ 边界）。
- [ ] AC3: 与 `artifact-style.md §2` 的 6 条概念映射在新版中逐条可定位——术语先解释↔标准一、掐短词/自造缩写↔标准一、比喻要落地↔标准二、英文/变量裸奔↔标准三、别写翻译腔↔标准四、流畅优先于省字↔§3「反啰嗦 ≠ 砍成电报体」。
- [ ] AC4: 规矩条目零丢失——原版每条具备独有语义的规矩，在新版中都有对应条目；删除的只能是与其他条目重复的表述，逐条对照表列出去向。
- [ ] AC5: 体积下降到 4400–4900 字节区间，且例子行合计字节数不低于原版。
- [ ] AC6: `.ai/project/capabilities.md` 的节数记载与新版实际 H2 数一致；`CHANGELOG.md:139` 保持原样未被改动。
- [ ] AC7: `@import` 链路不变——`scripts/configure-global-install.py:151` 的路径行与 `communication-style.md` 的仓根位置、文件名均未改动；改动文件集合不含 `templates/` 与 `scripts/`。

## Verification Method

- AC1: `grep -n '❌\|✅' communication-style.md` 提取例子行，剔除「格式」节 emoji 说明行与「结尾决策块」推荐标签行，对新旧两版做逐行 diff，要求 7 行内容完全相同。
- AC2: `grep '^## ' communication-style.md` 前后对比，要求 9 行输出逐行完全相同。
- AC3: 对 6 条映射各取一个关键词在新版 grep（术语先解释 / 掐短 / 比喻 / 裸奔 / 翻译腔 / 流畅优先或等义表述），全部命中；再人工确认语义未被弱化。
- AC4: 产出「原版条目 → 新版去向」逐条对照表，标注保留 / 合并到哪条 / 判定为重复删除；表中不得出现「删除且无对应」的独有语义条目。
- AC5: `wc -c communication-style.md` 落在 4400–4900；例子行字节数用 AC1 的提取结果计算，新版 ≥ 原版。
- AC6: `grep -n '节' .ai/project/capabilities.md` 核对记载与 `grep -c '^## '` 实际值一致；`git diff CHANGELOG.md` 为空。
- AC7: `grep -n 'communication-style' scripts/configure-global-install.py` 输出与改动前一致；`git diff --name-only` 结果人工核对无 `templates/` 与 `scripts/` 路径。

## External References

- N/A

## Open Questions / Risks

- "哪句是冗余、哪句是必要的喘息"没有机械判据，AC4 的逐条对照表是人工判断的产物；机械部分（AC1/AC2/AC5/AC6/AC7）只能保证例子、结构与链路不被破坏，保证不了措辞打磨的品味。
- 本迭代净收益约 500–900 字节（≈160–300 token），投入产出比偏低，属用户明确选择的流程档位；若中途改主意可按 `iteration-schema.md §5.6` 废弃 ITER-0097。
- `capabilities.md` 的节数修正属于本迭代顺带修的既有漂移，不是本次改动引入的；若收口时发现还有别处记载节数，一并纳入 AC6 而不另开迭代。
