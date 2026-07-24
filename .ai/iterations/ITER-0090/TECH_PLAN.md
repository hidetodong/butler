<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0090

方案状态: pass

## Design Decisions

- 新建 `Coder/20_Workflow_Lifecycle/butler-setup.md` 作为语义真源；`scripts/setup.sh` 继续是机械执行真源。
- 新增 registry workflow `setup`，由同步器维护两宿主 frontmatter、agents metadata、软链和 `docs/workflows.md`。
- Claude/Codex 薄入口只做路径预检、影响说明、确认、执行和结果汇报；不内嵌安装步骤。
- `init` 的第 3 步改为委托 setup 规则，保持项目部署和机器安装分层。

## Failure Paths

- Butler 根不可信、脚本缺失/不可执行、用户未确认时零写退出。
- setup 非零退出时原样报告退出码和脚本的部分完成边界；不重试、不修改脚本判定。
- Codex/Pi 不存在沿用 setup.sh 的明确降级语义，不把跳过说成安装成功。

## Test Strategy

- quick_validate 新 skill；registry 12 工作流/投影/软链/策略回归；setup 临时 HOME stub；完整 CI、artifact/state/handoff/audit。

## References Compliance

- N/A
