---
description: 安装或刷新 Butler 机器级能力——统一配置 Claude 全局命令、Codex plugin 与 Pi 扩展
argument-hint: "[可选：Butler 仓绝对路径]"
---

你正在执行 Butler 机器级安装。完整语义以 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/butler-setup.md` 为真源，机械执行只允许调用 `$BUTLER_PATH/scripts/setup.sh`。

1. 按规则真源 §2 解析并回声唯一 `BUTLER_PATH`；路径不唯一或合同文件不全时零写退出。
2. 按 §3 说明用户目录影响并判断本次输入是否已经构成显式安装确认；未确认时等待，不执行。
3. 确认后以独立 argv 执行 `bash "$BUTLER_PATH/scripts/setup.sh"`，保留真实输出和退出码。
4. 按 §4 分组件汇报 installed/refreshed/skipped/failed；不伪报成功，不自动接受 hook trust，不初始化或升级当前项目。
