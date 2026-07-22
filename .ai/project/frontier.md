# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：v2.18.0；MILE-0009 R1–R8 已交付并收口，尚未切版。
- **三宿主**：Claude Code / Codex / Pi 三宿主适配全部落地——Pi 由 TypeScript 扩展（`plugins/butler-pi/`）拦截 write/edit 调 Python 门禁，setup.sh 一键安装。
- **工程化加固**：安全安装、证据/状态审计、固定 CI 合同、可执行升级器与 11 工作流 registry 全部闭环；本地 Darwin/arm64 完整矩阵有机器证据。
- **双宿主治理**：45 个入口元数据投影由 registry 生成/校验；个人 Butler plugin 的仓内真源已刷新，team/public distribution 明确未配置。
- **远端保护**：workflow 尚未推送；required API 返回 403，当前私有仓库需升级 GitHub Pro 或改公开，状态为 `pending external capability`。

## 活跃战线

- 当前无 active milestone / iteration；MILE-0009 八条路线全部 closed。
- MILE-0009 已形成 origin/inbox → 日期化 PRD 集合 → 多需求钉版 → migration/split/status/update → workspace scope/plan/hook/diff 的完整链路。
- 真实 `WorkCode.nosync/apps` 已以只读源 + 临时副本验证 28 个 workspace、legacy plan/apply/verify/resolve/rollback 与原仓双 hash 不变；没有替用户升级外部仓。
- 危险模式仍为 ON；下一方向须由用户启动现有未编号候办或提出新任务。

## 下一个瓶颈
- MILE-0009 能力尚未切版/发布；外部旧项目获得新结构仍需显式 upgrade/migration，不能把仓内交付写成已部署。
- 未编号候办 `long-horizon-scale-governance` 可按用户决定提升；当前不预占正式号。
- 若要让 `Butler required checks` 成为远端合并门禁，需用户授权套餐/可见性变化，并在 workflow 推送后配置和核验保护规则。
- 可执行升级器仍缺一份真实外部老项目的受监督 dogfood；首次使用保留 backup/journal 并人工审阅 diff。
