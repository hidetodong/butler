# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：发布真相仍为 v2.16.0；MILE-0007 的 R1–R4 均已实现并收口在隔离分支，尚未整体发布。
- **里程碑**：MILE-0007 active；安装器事务安全、机器证据/状态审计、固定工具链/双 OS CI 合同和可执行升级器已交付，仅 R5 待推进。
- **持续验证**：本地唯一入口与 workflow 合同已成型；Darwin/arm64 固定工具链完整矩阵有机器证据。workflow 尚未推送，真实 GitHub Linux/macOS run 缺失。
- **远端保护**：required API 返回 403；当前私有仓库需升级 GitHub Pro 或改公开，状态为 `pending external capability`。

## 活跃战线

- 当前无 active 迭代；危险模式将自动开启 R5“工作流注册与分发收敛”。

## 下一个瓶颈

- R5 统一 8 个工作流的宿主名称、触发策略、入口生成/校验与团队分发边界，消除 Claude/Codex/文档多处人工同步。
- 若要让 `Butler required checks` 真正成为远端合并门禁，需用户另行授权升级 GitHub 套餐或改变仓库可见性，并在 workflow 推送后配置/核验保护规则。
