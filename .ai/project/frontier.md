# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：v2.15.0。MILE-0006 R1–R4 已完成：统一 setup、双入口部署/升级、8 skills 和 apply_patch hooks 组成完整双宿主工作流。
- **里程碑**：MILE-0006 closed；四条路线均完成，交付与回归矩阵已归档。
- **分发**：`scripts/install-codex-plugin.sh` 使用个人 marketplace、官方 cachebuster/validator 和 `codex plugin add`；当前本机 `butler@personal` 已安装。
- **边界**：Claude 能力保持；Codex hooks 已实测 phase/protected deny、allow 和 advisory。PreToolUse 不是完整安全边界，首次 trust 仍需用户操作。

## 活跃战线

- 当前无活跃路线；等待下一项明确需求或新里程碑。

## 下一个瓶颈

- hook trust 需要用户首次审阅；自动 E2E 只能用测试态 trust bypass 证明行为，不能代替日常信任动作。
- shell/MCP 写路径不在当前机械保护声明内；若 Codex canonical 工具协议变化，须重跑真实 E2E 并更新 adapter。
