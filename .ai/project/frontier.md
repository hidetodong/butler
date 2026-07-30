# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **MILE-0010 / MILE-0011 已随 v3.1.0 发布**：可信 handoff、有界状态分片和确定性五件套结构/生成/校验/迁移全部完成；当前 live 五件套已 dogfood 为 strict v1。

- **版本**：v3.3.0；已聚合发布 MILE-0013 项目级配置结构化（ITER-0093～ITER-0095）。
- **三宿主**：Claude Code / Codex / Pi 三宿主适配全部落地——Pi 由 TypeScript 扩展（`plugins/butler-pi/`）拦截 write/edit 调 Python 门禁，setup.sh 一键安装。
- **工程化加固**：安全安装、证据/状态审计、固定 CI 合同、可执行升级器与 12 工作流 registry 全部闭环；本地 Darwin/arm64 完整矩阵有机器证据。
- **双宿主治理**：49 个入口元数据投影由 registry 生成/校验；个人 Butler plugin 的仓内真源已刷新，team/public distribution 明确未配置。
- **远端保护**：workflow 尚未推送；required API 返回 403，当前私有仓库需升级 GitHub Pro 或改公开，状态为 `pending external capability`。

## 活跃战线

- MILE-0013 已关闭：项目级机器设置进入扁平 `.ai/butler.config.json`，严格内核、新部署、legacy 事务迁移、全部消费端、双宿主入口与 v3.3.0 迁移链均已接通。
- MILE-0009 已形成 origin/inbox → 日期化 PRD 集合 → 多需求钉版 → migration/split/status/update → workspace scope/plan/hook/diff 的完整链路。
- 真实 `WorkCode.nosync/apps` 已以只读源 + 临时副本验证 28 个 workspace、legacy plan/apply/verify/resolve/rollback 与原仓双 hash 不变；没有替用户升级外部仓。
- 危险模式仍为 ON；当前没有 active 迭代或里程碑路线项。
- ITER-0096 已关闭：旁路执行者可用 `.ai/sidework/` 短回执把代码与调研混合成果交还，用户显式给路径后主 Agent 定向续接；无审批状态、索引或自动扫描。

## 下一个瓶颈
- MILE-0009 已随 v3.0.0 发布；外部旧项目获得新结构仍需显式 upgrade/migration，不能把发布写成目标项目已部署。
- milestone backlog 当前有 5 个独立候办，包括 PRD future route 兑现、状态转换可信门、TDD 证据增强，以及两项并行执行方向。
- 若要让 `Butler required checks` 成为远端合并门禁，需用户授权套餐/可见性变化，并在 workflow 推送后配置和核验保护规则。
- 可执行升级器仍缺一份真实外部老项目的受监督 dogfood；首次使用保留 backup/journal 并人工审阅 diff。
- 危险模式规则真源仍把 P4 与 `/butler:loop` 自动绑定，但用户已明确两者正交；需要独立纠偏迭代统一 dangerous engine、logic protocol 和相关入口，避免再次误触发 Loop。
