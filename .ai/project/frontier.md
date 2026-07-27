# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **MILE-0010 / MILE-0011 已随 v3.1.0 发布**：可信 handoff、有界状态分片和确定性五件套结构/生成/校验/迁移全部完成；当前 live 五件套已 dogfood 为 strict v1。

- **版本**：v3.1.0；ITER-0090 setup 命令与 MILE-0012 轻量 TDD 配对证据已收口但尚未提交/发布。
- **三宿主**：Claude Code / Codex / Pi 三宿主适配全部落地——Pi 由 TypeScript 扩展（`plugins/butler-pi/`）拦截 write/edit 调 Python 门禁，setup.sh 一键安装。
- **工程化加固**：安全安装、证据/状态审计、固定 CI 合同、可执行升级器与 12 工作流 registry 全部闭环；本地 Darwin/arm64 完整矩阵有机器证据。
- **双宿主治理**：49 个入口元数据投影由 registry 生成/校验；个人 Butler plugin 的仓内真源已刷新，team/public distribution 明确未配置。
- **远端保护**：workflow 尚未推送；required API 返回 403，当前私有仓库需升级 GitHub Pro 或改公开，状态为 `pending external capability`。

## 活跃战线

- 当前无 active 里程碑或迭代；MILE-0012 的 R1 配对检查与 R2 P5/Goal 接线、pytest dogfood 均已收口。
- MILE-0009 已形成 origin/inbox → 日期化 PRD 集合 → 多需求钉版 → migration/split/status/update → workspace scope/plan/hook/diff 的完整链路。
- 真实 `WorkCode.nosync/apps` 已以只读源 + 临时副本验证 28 个 workspace、legacy plan/apply/verify/resolve/rollback 与原仓双 hash 不变；没有替用户升级外部仓。
- 危险模式仍为 ON；当前没有待自动续跑的 active 路线项。

## 下一个瓶颈
- MILE-0009 已随 v3.0.0 发布；外部旧项目获得新结构仍需显式 upgrade/migration，不能把发布写成目标项目已部署。
- milestone backlog 当前有 3 个独立候办：PRD future route 兑现、状态转换可信门、TDD 证据增强。
- 若要让 `Butler required checks` 成为远端合并门禁，需用户授权套餐/可见性变化，并在 workflow 推送后配置和核验保护规则。
- 可执行升级器仍缺一份真实外部老项目的受监督 dogfood；首次使用保留 backup/journal 并人工审阅 diff。
