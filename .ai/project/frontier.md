# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：v2.17.0；MILE-0007 的 R1–R5 已实现、验证、收口并聚合发布。
- **工程化加固**：安全安装、证据/状态审计、固定 CI 合同、可执行升级器与八工作流 registry 全部闭环；本地 Darwin/arm64 完整矩阵有机器证据。
- **双宿主治理**：33 个入口元数据投影由 registry 生成/校验；个人 Butler plugin 已刷新，team/public distribution 明确未配置。
- **远端保护**：workflow 尚未推送；required API 返回 403，当前私有仓库需升级 GitHub Pro 或改公开，状态为 `pending external capability`。

## 活跃战线

- MILE-0008“目标可信闭环”closed；R1–R6 全部交付。派生 Goal、方案准入、运行回流、completion adjudicator、双宿主投影/降级与端到端回归闭环；GFC-001–008 全拒绝。
- 危险模式仍为 ON，但当前无 active 里程碑/迭代。

## 下一个瓶颈

- 外部旧项目自动获得本轮规则仍需后续正式版本 migration；本轮未切版、未合并、未推送。review/blocker 输入仍依赖审查真实执行。
- 若要让 `Butler required checks` 成为远端合并门禁，需用户授权套餐/可见性变化，并在 workflow 推送后配置和核验保护规则。
- 可执行升级器仍缺一份真实外部老项目的受监督 dogfood；首次使用保留 backup/journal 并人工审阅 diff。
