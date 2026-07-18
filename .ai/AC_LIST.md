---
状态: ack-frozen
ACK 日期: 2026-07-18
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 `dangerous-engine.md §5.1` 自审门），未经用户逐项确认（ITER-0059，2026-07-18）。

# Goal

交付一个由机器台账驱动的 Butler 升级器：默认只生成确定性计划，显式执行时保护目标项目、遇漂移先停、失败可恢复，并用历史 fixture 和机器证据证明跨版本与幂等行为。

# In Scope

- 机器可读迁移台账及其 schema/完整性检查，人读 `migrations/v*.md` 与机器记录的覆盖关系。
- 目标项目 inspect、dry-run、apply、decision/resume 状态、运行 journal 与项目内恢复点。
- 入口重生成、hook/settings 同步、显式 rename/add-field、restamp/no-op 等确定性项目动作。
- `[split]`、无戳首次升级和机器级 global install 的明确边界与非假成功状态。
- v1.x、v2.0、v2.14、v2.15 等代表性历史 fixture、跨版本 E2E、故障注入和现有 CI/evidence 接线。
- Claude `/butler:upgrade` 与 Codex `butler-upgrade` skill 改为调用同一程序，不再让模型解释散文后直接写。

# Out of Scope

- 不让程序自动理解并拆分任意 `.ai/PROJECT.md` 语义内容；`[split]` 仍遵守 opt-in 两态契约。
- 默认不运行会改用户 HOME 的 `setup.sh`；不把机器级安装纳入目标项目回滚承诺。
- 不删除历史 Markdown 配方，不重写历史 deliveries/迭代归档，不修改 `origin/`。
- 不为所有未来动作提前造通用脚本语言；只实现已登记的有限 action schema，未知类型必须拒绝。
- 不发布新版本、不提交/推送、不处理 R5 工作流注册表或 GitHub 远端 required checks。

# Acceptance Checklist

- [ ] **AC1（机器台账完整且唯一驱动）**：仓库提供有 schema/version 的机器可读迁移台账；每条记录含 source/target 版本、稳定 action ID、类型、执行域、参数和前置条件。校验器证明当前全部 `migrations/v*.md` 都有且仅有对应记录、版本区间无断链、action 类型/参数合法；升级程序不得从 Markdown 正文正则提取执行动作。
- [ ] **AC2（inspect 与 dry-run 零写入）**：对显式目标根运行 inspect/dry-run，会输出确定排序的旧版→当前版队列、逐动作域/状态/理由、预计文件变化和阻塞项，并提供机器可读输出；执行前后目标项目、Butler 仓和测试 HOME 的内容摘要一致。无戳、双入口版本不一、目标版本超前或未知版本均返回稳定非零/needs-decision 状态和可操作诊断。
- [ ] **AC3（路径、所有权与漂移 fail-closed）**：升级器拒绝 Butler 仓自身、非唯一/不存在目标、路径穿越及软链逃出项目根；不写 `origin/`、`deliveries/`、历史归档或未登记路径。入口 marker 重复/残缺、hook 副本手工漂移、部分成形目标或前置 hash/shape 不符时，在首个项目写入前停止并列出冲突。
- [ ] **AC4（事务化项目 apply 与恢复）**：显式 apply 在加锁后先完成全队列预检，再于目标 `.ai/` 受控运行区生成带路径、原摘要、目标摘要的恢复 manifest/journal；只对登记的项目文件原子替换。任一注入故障或意外异常会自动恢复所有已触及项目文件到执行前逐字节状态并记录失败；不得用 `git reset/checkout` 或覆盖用户其他未提交改动完成回滚。
- [ ] **AC5（有限动作确定执行）**：程序至少确定性支持历史 `[regen-claude]`→双入口重生成、`regen-entrypoints`、`sync-hooks`（含 settings 幂等合并）、参数化 `rename`、参数化 `add-field`、`restamp` 与 `no-op`；入口外原文和两份 user-managed 区逐字保留。未知 action/参数立即拒绝；同一成功 apply 重跑为零内容变化且 journal 明确标记 already-current/no-op。
- [ ] **AC6（人工与机器级动作不假绿）**：`split`、无戳 manual-bootstrap 和 `global-install` 在 plan 中与项目机械动作分域。未给 `[split]` 决定时零项目写入并返回 needs-decision；显式 defer 后保留 `.ai/PROJECT.md` 并可继续机械升级，显式“现在迁”若仍需语义处理则停在可恢复人工交接点。默认 apply 不修改 HOME；机器级安装只能经单独显式命令/确认执行，失败不得把项目报告为 fully-complete。
- [ ] **AC7（历史兼容与跨版本 E2E）**：隔离 fixture 至少覆盖 v1.x 单入口、v2.0 split 边界、v2.14 旧部署、v2.15 双入口和当前版；逐例验证 dry-run→apply→rerun，最终入口同戳当前 VERSION、hooks/settings 对齐、受保护内容不变。另覆盖缺 AGENTS、无 stamp、断链 manifest、异常 marker、漂移 hook、并发锁和中途故障恢复。
- [ ] **AC8（宿主接线与文档单源）**：Claude command 与 Codex skill 都只负责解析 Butler/项目根、调用同一升级 CLI、呈报 plan 和收集显式决定；`butler-upgrade.md`、`migration-schema.md`、MCV 文档及人类指南明确程序真源、退出状态、dry-run/apply/恢复/全局动作边界，旧“模型逐条解释并直接执行”口径被删除或改成兼容说明。
- [ ] **AC9（证据化非回归）**：机器台账校验、升级器单测、历史 E2E、故障恢复、幂等、dry-run 摘要不变、`git diff --check`、active state audit 和完整 `bash scripts/verify-ci.sh` 均生成本迭代 evidence record；P5 每条 AC 引用真实 record，失败首跑保留，不以口头复核或静态文档替代执行证据。

# Verification Method

- AC1：运行 manifest schema/覆盖测试；故意删版本、造断链、重复 ID、未知 action 和坏参数，均应非零；静态断言升级器不读取 Markdown 步骤作为执行输入。
- AC2：在只读摘要夹具上运行 inspect/dry-run JSON 与人读输出，比较目标、Butler 和隔离 HOME 前后哈希；逐项断言错误状态码和诊断字段。
- AC3：用临时仓构造 self-target、`..`/绝对越界、外指 symlink、残缺 marker、漂移 hook、部分目录，断言零写入与冲突清单。
- AC4：在每个写入边界注入失败，比较执行前后文件集合、内容和 mode；核 journal/restore manifest 摘要，确认不调用破坏性 git 回滚。
- AC5：对每类 action 跑正常、已完成、冲突 fixture；逐字节比较入口外部文本/user-managed，第二次执行内容摘要不变。
- AC6：隔离 HOME 断言默认命令零 HOME 写入；分别测试 split 未决/defer/now 和 global install 未授权/显式执行失败，核最终完成状态不假绿。
- AC7：参数化历史 fixture 做完整跨版本 E2E；并发两个 apply 断言只有一个持锁执行，故障恢复后可安全重跑。
- AC8：运行 Claude/Codex workflow validator 与文档链接/契约检查；静态核两宿主入口只路由同一 CLI，不复制迁移算法。
- AC9：用 verification-evidence runner 捕获专项、完整 CI、本地状态审计和负向复核，逐 AC 校验 record outcome/log/hash。

# Open Questions / Risks

- 历史 Markdown 本身不完全符合现有 schema；本轮应修其结构并让机器台账成为执行真源，但不能篡改历史发布意图。
- `[split]` 的内容路由本质上需要语义判断；验收要求是诚实阻塞/暂缓/恢复，不以低质量自动拆分换“全自动”标签。
- global install 跨越项目事务边界；即使提供单独显式执行，也只能报告自己的结果，不能承诺与项目文件原子提交。
- 当前工作树叠加未提交的 ITER-0056～0058；实现与测试必须保留并正确归属这些增量。
