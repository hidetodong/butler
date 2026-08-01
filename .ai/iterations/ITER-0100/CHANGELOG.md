<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0100 变更流

## ADD

- `Coder/00_System_Prompt/workflow-router.md`：新增四态语义路由、安全退路和一次一个主工作流合同（AC1、AC5–AC7）。
- `Coder/20_Workflow_Lifecycle/iteration-intake.md`、`tools/iteration-intake/`：新增会话结晶、零写 plan、事务 apply、active 拒绝、里程碑绑定和回滚测试（AC8–AC11）。
- `.claude/commands/butler.md`、`.claude/commands/butler/iteration.md`、`plugins/butler/skills/butler-router/`、`plugins/butler/skills/butler-iteration/`：新增双宿主薄入口及仓内发现链接（AC3、AC4、AC8）。
- `workflows/router-examples.json`：新增覆盖 13 个业务工作流与四种 Router 状态的共享语义样例（AC5–AC7）。

## EDIT

- `workflows/registry.json`、`scripts/sync-workflow-registry.py`、`docs/workflows.md`：升级 schema v2，加入 Router 元入口、routing 元数据、iteration 工作流和严格校验 / 幂等投影（AC2、AC5–AC8、AC12）。
- `scripts/configure-global-install.py` 与双宿主 / 安装 / registry / validator 测试：安全管理 Claude 根命令文件软链，并把 Router + 13 个业务 Skill 纳入完整回归（AC3、AC12）。
- `Coder/README.md`、`HUMAN_GUIDE.md`、`docs/codex-compatibility.md`、plugin manifest：登记共享内核、宿主边界和新能力（AC1、AC4、AC12）。

## DELETE

- N/A
