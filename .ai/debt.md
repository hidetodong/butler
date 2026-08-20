# debt（已知长期欠债）

> 只放悬着没还的账。还掉的删除、不留历史（历史归 `ITERATIONS` / `deliveries`）。

- **butler 仓自身不 dogfood 运行自己的 hook**：live 机械门禁（含双 active 迭代拦截 `single_active_iteration`）在 butler 仓内不触发——规则仓非部署项目，不装自己的 PreToolUse hook。改由 pytest 验证 hook 逻辑 + prompt 级一致性自检兜底 butler 侧。MILE-0001 R2 已补执行门禁 hook + 自检探针；"butler 侧不 live 化"仍是**已知设计约束**，非待修 bug。
- **项目自有 hook 与 Butler 受管目录不能共存**：若项目把自有文件放进 `.claude/hooks/`，升级器会把它视为受管树漂移并拒绝覆盖；`claude-skills` 已证明守门行为正确，但尚无安全的共存或目录所有权合同。解决前不得用扩大白名单绕过。
- **`/butler:upgrade` 从未在真实已部署项目上跑过**：升级器（`tools/butler-upgrade/`）有 16 项历史 / 负向 / 事务专项进 CI，但全部跑在临时 fixture 上；真实老项目跨多个版本升级的端到端回归一次没做过。MILE-0016 R15 计划补这次回归。本条自 ITER-0112 从已删除的 `.ai/project/architecture.md` 成熟度段迁出。
- **运行时观测缺位**：所有门禁只能证明文件结构一致，证明不了任何宿主在真实会话里按规矩读过——L0 分层导航、冷启动读序、新建的 `.ai/OVERVIEW.md` 都一样，改得再准也没有一条数据说明它被打开过。缺的是每个入口记录最后调用时间的 usage instrumentation，归 MILE-0016 R11。本条于 2026-08-20（ITER-0114）从已删除的 `.ai/project/frontier.md`「下一个瓶颈」节迁出。
- **远端 required check 未启用**：`Butler required checks` 要成为远端合并门禁，需要用户先授权套餐或可见性变化——workflow 尚未推送，required API 返回 403，当前私有仓库需升级 GitHub Pro 或改公开；GitHub Private Vulnerability Reporting 是否实际启用也仍待仓库管理员在外部设置里核验。本地 `scripts/verify-ci.sh` 全绿不等于远端有门禁，不得口头打绿。本条于 2026-08-20（ITER-0114）从已删除的 `.ai/project/frontier.md` 迁出，合并原「当前形态·远端保护」与「下一个瓶颈·远端 required check」两条重复表述，并收编「活跃战线」里 Private Vulnerability Reporting 待核验那半句。
- **双宿主语义入口未经真实安装人测**：共享 Router 与会话转迭代入口已交付并有本地机器证据，但真实 Claude `/butler` UI 共存、ChatGPT App `@Butler` 隐式注入都还没在装好的环境里由人验过，不得宣称平台端到端已证。本条于 2026-08-20（ITER-0114）从已删除的 `.ai/project/frontier.md` 迁出。
- **危险模式规则真源仍把 P4 与 `/butler:loop` 自动绑定**：用户已明确两者正交（`Coder/65_Extension_Dangerous/dangerous-engine.md` 与 `Coder/00_System_Prompt/logic-protocol.md` 口径不一致），需要一次独立纠偏迭代统一 dangerous engine、logic protocol 与相关入口，避免再次误触发 Loop。本条于 2026-08-20（ITER-0114）从已删除的 `.ai/project/frontier.md` 迁出。
- **`.ai/invariants.md` 有 16 条不带真源指针**：这批条目复述了机制的具体形状却没给可核对的出处，正是最容易悄悄变假的一类（实测已有两条假掉，ITER-0114 修好）。当前由 `scripts/sync-project-overview.py --check` 上棘轮卡住不许再增，**但 16 这个基线是欠账不是允许额度**，逐条补真源指针的活儿没做。
- **`iteration-schema.md §5.3` 的修订记录要求与产物合同冲突**：§5.3 要求 amend 时「在 `AC_LIST.md` 顶部『修订记录』追加一行」，但 `tools/artifact-pipeline/artifacts.v1.json` 的 acceptance 清单只允许固定七个二级标题，`## 修订记录` 加进去就 drift。ITER-0112 的 amend 直接改 AC 正文没留记录，ITER-0114 改把它写进 frontmatter——两次绕法不一致。要么放宽产物合同，要么改 §5.3 的落点措辞，本轮未定。
