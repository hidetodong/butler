# Goal

- 修复 Butler Should Fix Bucket E（平台与回退健壮性）2 条问题：`scripts/setup.sh` 的 `sed -i ''` 仅 macOS/BSD 可用，在 Linux 会报错；`logic-protocol.md` 的参考资料注入规则依赖外部 skill，但未定义 skill 不可用时的回退路径。

# Current Understanding

- 本任务是 Butler 规则仓维护的第三轮。上一轮 Bucket A 已随 commit `d266acf` 落地，本轮覆写 `.ai/` 产物作为新任务决策链。
- Bucket E 2 条彼此独立：
  - E-1 是脚本健壮性问题（pure technical）。
  - E-2 是规则文本补丁（需要设计 fallback 层级）。
- 改动文件少（2 个）、无契约变更，但 E-2 存在 3 个候选方案需要用户拍板。

# Constraints

- 显性约束：
  - `scripts/setup.sh` 只能用 POSIX shell 能力，不引入 Python/Node 新依赖。
  - `logic-protocol.md` 的参考资料表格结构保留，fallback 作为新增段落或表格列。
- 隐性约束：
  - setup.sh 修复不破坏现有 macOS 用户的既有行为。
  - fallback 规则与 mcv-deployment `.ai/references/` 目录约定（存储路径、命名）保持一致。

# Impact Scope

预计修改文件：
- `scripts/setup.sh`（E-1：sed 平台兼容）
- `Coder/00_System_Prompt/logic-protocol.md`（E-2：补 fallback 段）

不影响：其他所有规则文件、templates/、Coder/ 下其他内容。

# Project Type / Active Profiles

- 项目类型：Markdown 规则仓库（setup.sh 是附属 POSIX shell 脚本）。
- 未命中任何 Domain Profile。

# Open Questions

- **E-2** 参考资料 skill 不可用时的 fallback 策略需要用户拍板（见 AC_LIST）。
