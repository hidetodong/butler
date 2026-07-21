# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：v2.18.0；MILE-0008 全部收口，v2.18.0 聚合 ITER-0068–0071 已发布。
- **三宿主**：Claude Code / Codex / Pi 三宿主适配全部落地——Pi 由 TypeScript 扩展（`plugins/butler-pi/`）拦截 write/edit 调 Python 门禁，setup.sh 一键安装。
- **工程化加固**：安全安装、证据/状态审计、固定 CI 合同、可执行升级器与十工作流 registry 全部闭环；本地 Darwin/arm64 完整矩阵有机器证据。
- **双宿主治理**：41 个入口元数据投影由 registry 生成/校验；个人 Butler plugin 已刷新，team/public distribution 明确未配置。
- **远端保护**：workflow 尚未推送；required API 返回 403，当前私有仓库需升级 GitHub Pro 或改公开，状态为 `pending external capability`。

## 活跃战线

- MILE-0008"目标可信闭环"closed；R1–R6 全部交付。
- ITER-0072 closed：`/butler:init` 命令上线——三宿主可用的项目初始化入口。
- ITER-0073 closed：`/butler:progress` 命令上线——三宿主可用的结构化进度查看。
- ITER-0072 和 ITER-0073 已收口但未切版（待下次 MINOR/PATCH 聚合发布）。
- 危险模式仍为 ON，但当前无 active 里程碑/迭代。

## 下一个瓶颈
- ITER-0072–0073 待切版聚合发布；外部旧项目获得新命令/hook 仍需正式版本 migration。
- 若要让 `Butler required checks` 成为远端合并门禁，需用户授权套餐/可见性变化，并在 workflow 推送后配置和核验保护规则。
- 可执行升级器仍缺一份真实外部老项目的受监督 dogfood；首次使用保留 backup/journal 并人工审阅 diff。
