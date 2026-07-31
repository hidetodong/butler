# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **MILE-0010 / MILE-0011 已随 v3.1.0 发布**：可信 handoff、有界状态分片和确定性五件套结构/生成/校验/迁移全部完成；当前 live 五件套已 dogfood 为 strict v1。

- **版本**：v3.5.1；已聚合发布 MILE-0014 Explore / Decision Map 接入（ITER-0102～ITER-0106），当前领域模型治理作为 MILE-0015 继续推进。
- **三宿主**：Claude Code / Codex / Pi 三宿主适配全部落地——Pi 由 TypeScript 扩展（`plugins/butler-pi/`）拦截 write/edit 调 Python 门禁，setup.sh 一键安装。
- **工程化加固**：安全安装、证据/状态审计、固定 CI 合同、可执行升级器与 schema v2 Router + 13 业务工作流 registry 全部闭环；本地 Darwin/arm64 完整矩阵有机器证据。
- **双宿主治理**：57 个入口元数据投影由 registry 生成/校验；Claude 根命令与命名空间双软链、Codex Router / iteration Skill 已入安装链，个人 plugin 的仓内真源已刷新，team/public distribution 明确未配置。
- **Explore 边界**：MILE-0014 R1 / ITER-0102 已交付。Explore 统一为既有 Ideation 的 opt-in 深化模式，Standard 只能 suggest 零写等待同意；Decision Map 探索期为决策真源，显式 promotion 从 Iteration P1 接回后降为参考。
- **Decision Map 内核**：MILE-0014 R2 / ITER-0103 已交付。结构化 Map 由本地四动作 Module 独占，具备 DAG/Frontier、Fog、Claim Lease、并发幂等和跨进程恢复；模型只提 operation spec，不决定状态转换是否合法。
- **Decision Work 执行合同**：MILE-0014 R3 / ITER-0104 已交付。四类工作共享不可变 Task/Result sidecar；只有 Research 可在显式选择和逐项 claim 后受控并行，候选必须由协调器显式 absorb，helper 无 Map 或项目写权。
- **Decision Promotion 交接桥**：MILE-0014 R4 / ITER-0105 已交付。resolved Decision slice 通过显式 `route-reference` 或 `iteration-start` 接入既有路线 / Iteration P1；digest、不可变 receipt、双层锁与 pending journal 保障幂等和故障可见，不自动选路、建路线或跳 P2。
- **Explore Router 与真实 dogfood**：MILE-0014 R5 / ITER-0106 已交付。唯一 Ideation 入口接入显式 Explore 语料，真实 `DMAP-0001` 可跨进程恢复；Research 实际串行，live promotion 对已占用路线零写拒绝，外部 tracker 裁决为 defer。
- **领域模型治理**：MILE-0015 已完成 R1–R3；五个限界上下文、20 项统一语言审计、四层渐进导航，以及 PRD→AC→TECH_PLAN→Evidence→Goal→Handoff 五段转换合同均已落地，静态预算和关系检查进入完整 CI。
- **语义入口**：共享 Router 和会话转迭代入口已交付；真实 Claude `/butler` UI 共存与 ChatGPT App `@Butler` 隐式注入仍待安装后人测，不宣称平台端到端已证。
- **开源入口**：ITER-0098 已关闭，根 README、Apache-2.0 `LICENSE`、`CONTRIBUTING.md` 与 `SECURITY.md` 已形成发现、上手、协作和安全报告的公开入口基线。
- **升级器摘要口径**：ITER-0099 已把源模板与目标项目的 hook 文件过滤收敛为单一定义，历史白名单按实际部署文件集重算；升级器 22 项与完整 CI 通过。
- **远端保护**：workflow 尚未推送；required API 返回 403，当前私有仓库需升级 GitHub Pro 或改公开，状态为 `pending external capability`。

## 活跃战线

- MILE-0013 已关闭：项目级机器设置进入扁平 `.ai/butler.config.json`，严格内核、新部署、legacy 事务迁移、全部消费端、双宿主入口与 v3.3.0 迁移链均已接通。
- MILE-0009 已形成 origin/inbox → 日期化 PRD 集合 → 多需求钉版 → migration/split/status/update → workspace scope/plan/hook/diff 的完整链路。
- 真实 `WorkCode.nosync/apps` 已以只读源 + 临时副本验证 28 个 workspace、legacy plan/apply/verify/resolve/rollback 与原仓双 hash 不变；没有替用户升级外部仓。
- MILE-0014 已关闭，R1–R5 与 ITER-0102～ITER-0106 全部完成。
- 危险模式仍为 ON；MILE-0015 active，R1/ITER-0107、R2/ITER-0108、R3/ITER-0109 已关闭，等待按用户指令开启 R4；当前无 active Iteration。
- ITER-0098 已关闭：开源 README 与社区治理文档已完成并通过本地完整 CI；GitHub Private Vulnerability Reporting 是否实际启用仍待仓库管理员在外部设置中核验。

## 下一个瓶颈
- MILE-0009 已随 v3.0.0 发布；外部旧项目获得新结构仍需显式 upgrade/migration，不能把发布写成目标项目已部署。
- MILE-0015 下一瓶颈是 R4：只结构化高风险身份、状态和引用，解除 dangerous/loop 错绑并统一人测 schema/manifest 所有权；R2/R3 尚无运行时读取与转换遥测，只有观察到宿主偏离时才评估补追踪。
- milestone backlog 当前有 7 个独立候办，包括结构化提问卡片、AI 用户体验迭代、PRD future route 兑现、状态转换可信门、TDD 证据增强，以及两项并行执行方向。
- 若要让 `Butler required checks` 成为远端合并门禁，需用户授权套餐/可见性变化，并在 workflow 推送后配置和核验保护规则。
- 项目自有 hook 与 Butler 受管 `.claude/hooks/` 仍缺安全共存合同；在明确目录所有权前继续 fail-closed。
- 危险模式规则真源仍把 P4 与 `/butler:loop` 自动绑定，但用户已明确两者正交；需要独立纠偏迭代统一 dangerous engine、logic protocol 和相关入口，避免再次误触发 Loop。
