# VERIFY_REPORT — ITER-0047（butler 命令命名空间系统地基 · MILE-0005 R1）

> ⚠️ 危险模式：本迭代 P2 为用户显式 ACK，P3 起由自审门替代 ACK、P4→P5→收口自治执行；P5 升格独立复核（`dangerous-engine §7.3`）。审计轨迹见 `RUN_LOG.md` ITER-0047。

# Verification Summary
- 覆盖：新建 `.claude/commands/butler/` 命名空间目录、`/butler-prd`→`/butler:prd` 破坏性迁移（`git mv` 正文零改）、新落 `/butler:review` 薄壳范本、`setup.sh` 逐文件软链→命名空间目录软链（含旧软链迁移清理）、4 活文档引用更新、`[rename]` 迁移配方、MINOR 切版三载体。
- 总体结论：**AC1–AC8 全过**。P4 实测：隔离假 HOME 实跑 `setup.sh` ×3 场景 **16/16 断言全绿**、`git mv` 后 grep 确认 prd 无自引用、`git diff --stat` 边界守恒。
- **P5 独立复核（升格）确认全绿**：fresh-context 子 agent 自写隔离 HOME 压测 **18/18**、byte-level diff 确认 prd 等价、真源锚点逐一核无捏造——confirm 8 / refute 0 / **0 Must Fix / 0 Should Fix**。

# AC Status（道 + 置信档）
- [x] AC1 (auto·可靠): 命名空间成立 ✓（`butler/` 目录 + `prd.md`+`review.md` 在、旧 `butler-prd.md` 已删，子目录＝冒号前缀映射正确）
- [x] AC2 (auto·可靠): 旧命令干净移除 ✓（活文档 grep `butler-prd`：Coder/README/HUMAN_GUIDE 零命中；`.ai/project` 仅 2 处「原名」历史陈述合法；旧全局软链经隔离 HOME 实跑确认被清；冻结归档未动）
- [x] AC3 (auto·可靠): prd 功能等价 ✓（`git show dc6fa11:...butler-prd.md` 与现 `butler/prd.md` **byte-identical**；原文从不自称命令名，三分支路由一字未改）
- [x] AC4 (auto·可靠): setup.sh 目录软链 ✓（隔离 HOME 实跑：旧扁平软链清理、`~/.claude/commands/butler` 指向仓库命名空间目录、prd+review 经软链可达、幂等重跑无 `butler/butler` 套娃、`-L` 守卫不误删用户真文件）
- [x] AC5 (auto 结构核 + 人读): review 薄壳范本 ✓（委托 `review-engine §5`/`independent-review`/`overview §3` 并声明不复述〔DRY〕、第 0 步优雅降级、frontmatter 两行说人话、`$ARGUMENTS` 分派默认自检/independent；与 prd.md 同构，真源锚点全部真实）
- [x] AC6 (auto·可靠): 迁移配方 ✓（`migrations/v2.7.0.md` 含个人命令层 `[rename]`〔清旧软链+重跑 setup.sh〕+ 部署面 `[no-op]`+`[restamp]` + `[global-install]` 机器动作）
- [x] AC7 (auto·可靠): 切版三载体对齐 ✓（VERSION=2.7.0、CHANGELOG 顶条 `[2.7.0]`、`migrations/v2.7.0.md` 区间 `v2.6.1→v2.7.0` 一致；MINOR 语义自洽；git tag 于发布提交时打——见 Handoff）
- [x] AC8 (auto·可靠): 边界守恒 ✓（`git diff dc6fa11 --stat` 仅命令层 2 + setup.sh + migrations + VERSION/CHANGELOG + 4 活文档 + RUN_LOG；`Coder/**` 算法/状态机、`templates/**`、schema、hook 一行未动）

# Verification Results
- AC1/AC3：`ls .claude/commands/butler/` 见 prd.md+review.md；`git show dc6fa11:.claude/commands/butler-prd.md` diff 现 `butler/prd.md` 退出 0（byte-identical）。
- AC2：`rtk proxy grep -rn butler-prd` 活文档——残留仅 capabilities/frontier 各 1 处「原名 `/butler-prd`」历史陈述、setup.sh 迁移清理代码（引用旧名必须），均合法。
- AC4：隔离假 HOME `HOME=<tmp> bash scripts/setup.sh` ×3（旧软链迁移 / 幂等重跑 / 全新装）16/16；P5 复核独立自写测试 18/18 复现。
- AC5：读 `butler/review.md` 核四要点 + 真源 section 锚点（overview §3/G1/G2、independent-review §5、`insight-independent-review.md`、VERIFY_REPORT `Independent Review` 字段）逐字对上、无捏造路径。
- AC6/AC7：读 `migrations/v2.7.0.md` + `cat VERSION` + CHANGELOG 顶条，三载体版本号一致、标签齐备。
- AC8：`git diff dc6fa11 --stat` 逐文件核，无越界。

# Gate Coverage
- 通用质量门禁：不破坏分层（命令层改动不入 Coder/templates）+ 新命令 README 目录树注册（无隐式依赖）+ 文件名互引不写绝对路径 + review.md frontmatter 两行说人话 ✓
- Active Profiles：无（规则仓，未命中 domain profile）。
- Tech Plan Alignment：DD1–DD6 全兑现（命名空间映射 / prd git mv 零改 / setup.sh 目录软链+迁移清理 / review 薄壳 / MINOR 三载体 / 边界守恒）；T1–T8 全落。
- References Compliance：N/A（无外部参考资料）。

# Independent Review（P5 强制完整审查升格，dangerous §7.3）
- 复核方式：fresh-context 子 agent（general-purpose，验证者≠实现者，agentId ab402c531621f2ace），spec-only 逐 AC + 自写隔离 HOME 压测（18/18）+ byte-level diff + 全树对抗 grep + 真源锚点逐一核。
- 逐 AC 裁决：**confirm 8 / refute 0 / 未能验证 0**。
- 结论：**可收口**——**0 Must Fix、0 Should Fix、3 Nice-to-Have**（均不阻断）。

# Remaining Risks
- 命令菜单「可见性」无法在 headless 实敲——用「文件/软链存在 + 命名空间结构正确 + 经软链可达」作可靠代理（命名空间机制经 claude-code-guide 查证 + 隔离 HOME 实跑，同 ITER-0044 验法）。
- 独立复核 3 条 Nice-to-Have（均不阻断，不改）：
  - N-1：`[rename]` 标签语义轻微过载——`migration-schema §4` 正典义是「重命名 `.ai/` 下过时文件」，v2.7.0 复用其描述「个人命令别名」改名。实现者已隔离处理（`[rename]` 只在明标「与目标项目无关」的说明段、未混进执行器消费的迁移步骤列表〔步骤里只有 `[global-install]`+`[restamp]`〕），且 AC6 点名要该标签，非缺陷。
  - N-2：git tag `v2.7.0` 需在发布提交时补打，才算含 tag 的三载体完全闭合——当前文档三载体已齐。
  - N-3：review.md `argument-hint` 用「fresh 子 agent」「验证者≠作者」略带术语，已算内联可读，可更白话，非必改。

# Handoff / Next Step
- 独立复核通过（0 Must Fix）→ 进原子收口五步（归档四件套 + 交付 md/html + 台账/路线图 + PROJECT 前滚 + 收口自检）+ 切版 git 仪式（本地 tag v2.7.0）。
- 北极星（MILE-0005 R1 单迭代）达成即交还；R2–R4 设计未锁、不擅自连跑。按用户「危险模式 ACK」授权：本轮自治到收口 + 提交 + 推分支 + draft PR；**不合并 main、不推 tag 到远端**（待用户授权）。
