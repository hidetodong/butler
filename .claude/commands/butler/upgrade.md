---
description: 安全升级已部署 Butler 项目——先由仓库升级器 dry-run，再经显式决定事务 apply；不解析 Markdown 散文写项目
argument-hint: "[留空=计划并升级当前项目]"
---

你正在执行 Butler 主动升级。本命令是薄壳路由器，执行真源是 `$BUTLER_PATH/tools/butler-upgrade/upgrade.py`；动作台账是 `migrations/manifest.json`。不要自行解析 `migrations/v*.md` 后手工写项目。

1. 按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1` 解析并回声唯一 `PROJECT_ROOT`。用户点名优先；歧义、未部署或目标是 Butler 仓自身时停止。
2. 阅读 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/butler-upgrade.md`，运行：

   ```bash
   python3 "$BUTLER_PATH/tools/butler-upgrade/upgrade.py" plan \
     --project-root "$PROJECT_ROOT" --json
   ```

3. 呈报版本 gap、项目动作、split 决策、冲突和 `external_pending`。标准模式等用户 ACK；危险模式走其自审门。
4. 若 split 需决定：暂缓用 `--split defer`；现在迁用 `--split now`，程序返回人工语义交接时不得假装完成。
5. 放行后显式执行 `apply --project-root "$PROJECT_ROOT" --split <决定> --json`。冲突/锁/恢复诊断按原状态呈报，不删除保护 marker、用户内容或锁来换绿。
6. `global-install` 修改 HOME，项目 apply 不执行。只有用户另行确认（危险模式也须独立审计）才运行 `global-install ... --confirm`。
7. 最后重跑 plan，报告 run ID、最终版本、幂等状态、split 结果和仍待机器级动作。
