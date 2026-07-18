# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：v2.17.0；MILE-0007 的 R1–R5 已实现、验证、收口并聚合发布。
- **工程化加固**：安全安装、证据/状态审计、固定 CI 合同、可执行升级器与八工作流 registry 全部闭环；本地 Darwin/arm64 完整矩阵有机器证据。
- **双宿主治理**：33 个入口元数据投影由 registry 生成/校验；个人 Butler plugin 已刷新，team/public distribution 明确未配置。
- **远端保护**：workflow 尚未推送；required API 返回 403，当前私有仓库需升级 GitHub Pro 或改公开，状态为 `pending external capability`。

## 活跃战线

- MILE-0008“目标可信闭环”active；R1 已冻结目标载体/权威边界和 8 个假完成负向 oracle，尚未新增 Goal 运行门禁。
- 危险模式仍为 ON；R2 下一步要裁决 Goal 是独立持久对象还是现有产物的派生视图，并定义不覆盖 AC/evidence/review 的最小合同。

## 下一个瓶颈

- Goal 相关事实目前分散在 milestone、iteration、CONCEPT、AC、TECH_PLAN、task-state、VERIFY/review 与宿主投影；缺少统一完成裁决链。
- R2 必须先解决 Goal 存储/派生形态和状态语义，避免为强化目标再造一份与现有 `.ai/` 产物漂移的台账。
- 若要让 `Butler required checks` 成为远端合并门禁，需用户授权套餐/可见性变化，并在 workflow 推送后配置和核验保护规则。
- 可执行升级器仍缺一份真实外部老项目的受监督 dogfood；首次使用保留 backup/journal 并人工审阅 diff。
