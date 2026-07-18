# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：发布真相仍为 v2.16.0；MILE-0007 的 ITER-0056/R1、ITER-0057/R2、ITER-0058/R3 均已收口但尚未提交/发布。
- **里程碑**：MILE-0007 active；安装器事务安全、机器证据/状态审计、固定工具链/双 OS CI 合同已交付，R4–R5 planned。
- **持续验证**：本地唯一入口与 workflow 合同已成型；Darwin/arm64 固定工具链完整矩阵有机器证据。workflow 尚未推送，真实 GitHub Linux/macOS run 缺失。
- **远端保护**：required API 返回 403；当前私有仓库需升级 GitHub Pro 或改公开，状态为 `pending external capability`。

## 活跃战线

- 当前无 active 迭代；MILE-0007 等待开启 R4“可执行升级器”。

## 下一个瓶颈

- `/butler:upgrade` 仍由模型解释 Markdown 迁移配方；R4 要提供机器可读动作、dry-run、冲突停机、幂等执行和历史版本 fixture。
- R5 再统一 8 个工作流的宿主名称、触发策略、入口生成/校验与团队分发边界。
- 若要让 `Butler required checks` 真正成为远端合并门禁，需用户另行授权升级 GitHub 套餐或改变仓库可见性，并在 workflow 推送后配置/核验保护规则。
