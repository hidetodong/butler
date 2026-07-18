# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：发布真相仍为 v2.16.0；MILE-0007 的 R1–R5 已在隔离分支实现、验证并收口，尚未切版或推送。
- **工程化加固**：安全安装、证据/状态审计、固定 CI 合同、可执行升级器与八工作流 registry 全部闭环；本地 Darwin/arm64 完整矩阵有机器证据。
- **双宿主治理**：33 个入口元数据投影由 registry 生成/校验；个人 Butler plugin 已刷新，team/public distribution 明确未配置。
- **远端保护**：workflow 尚未推送；required API 返回 403，当前私有仓库需升级 GitHub Pro 或改公开，状态为 `pending external capability`。

## 活跃战线

- 当前无 active 迭代或里程碑；危险模式仍为 ON，直到用户显式关闭。

## 下一个瓶颈

- 把已收口的 MILE-0007 按 MINOR 聚合发布，需要单独执行 VERSION/CHANGELOG/migration/release commit/tag/push 仪式；本次未把“完成里程碑”扩大解释为发布。
- 若要让 `Butler required checks` 成为远端合并门禁，需用户授权套餐/可见性变化，并在 workflow 推送后配置和核验保护规则。
- 可执行升级器仍缺一份真实外部老项目的受监督 dogfood；首次使用保留 backup/journal 并人工审阅 diff。
