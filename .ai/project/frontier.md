# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：v2.14.0。MILE-0006 R1–R3 已完成：Codex 能从 `AGENTS.md` 发现规则、通过 plugin 使用 8 个 skills，并对 canonical `apply_patch` 运行共享门禁/提醒。
- **里程碑**：MILE-0006 active；R1/R2/R3 closed，R4 planned；R3 收口后危险模式将自动开启 R4。
- **分发**：`scripts/install-codex-plugin.sh` 使用个人 marketplace、官方 cachebuster/validator 和 `codex plugin add`；当前本机 `butler@personal` 已安装。
- **边界**：Claude 能力未变。Codex hooks 已实测 phase/protected deny、allow 和 advisory；PreToolUse 不是完整安全边界。目标项目双入口和统一 setup/upgrade 尚未接线。

## 活跃战线

- 下一项 R4：setup / MCV / upgrade / migration 双宿主接线，并跑 Claude+Codex 回归矩阵后收 MILE-0006。

## 下一个瓶颈

- `scripts/setup.sh` 与 `mcv-deployment` 仍以 Claude 为主，尚未把 `AGENTS.md`、plugin 安装/信任说明和双端验证纳入一个幂等升级路径。
- hook trust 需要用户首次审阅；自动 E2E 只能用测试态 trust bypass 证明行为，不能代替日常信任动作。
