---
状态: ack-frozen
ACK 日期: 2026-07-18
---

# Goal

让 Butler 全局安装器在用户配置正常时保持幂等，在配置残缺、重复或所有权不明时零破坏停下，并准确报告实际结果。

# In Scope

- Claude 全局配置 managed marker 的完整性校验、用户原文保护和安全更新。
- `.zshrc` / `.bashrc` 中 `BUTLER_PATH` 有效 export 的精确识别与更新。
- `~/.claude/commands/butler` 的所有权判断、路径迁移和冲突处理。
- 用户文件逐对象原子更新，以及跨组件失败时的真实结果回声。
- 隔离 HOME 下的缺陷回归、原有安装路径和完整双宿主矩阵。
- 必要的人读冲突修复说明。

# Out of Scope

- 不重构 Codex plugin installer 或建立公共/team marketplace。
- 不要求 shell、Claude、commands、plugin 四个独立组件组成可自动回滚的全局事务。
- 不修改目标项目部署、升级迁移、renderer、hook 或工作流算法。
- 不建立 GitHub Actions；持续集成属于 MILE-0007 R3。

# Acceptance Checklist

- [x] **AC1（marker 零丢失）**：Claude 全局配置只有 0 个 marker 时可安全追加，恰好一对时只替换 Butler 管理区；marker 单个、重复块或数量异常时非零退出，原文件内容与权限保持不变。
- [x] **AC2（用户区保真）**：成功更新 Claude 全局配置后，管理区前后所有用户原文逐字保留；新管理区恰好一对 marker，重复运行内容和 marker 数量不漂移。
- [x] **AC3（环境变量精确更新）**：只把有效的 `export BUTLER_PATH=...` 当作现存配置；0 条时追加 1 条，1 条时原位更新，多条时拒绝修改。注释、普通文本或其他变量包含 `BUTLER_PATH` 时不得造成假命中或假成功。
- [x] **AC4（命令目录所有权）**：目标不存在时建立 Butler 命名空间软链；现存软链可证明指向 Butler 命令源时允许幂等刷新或仓路径迁移；真实文件/目录、断链或无关软链一律不删除、不覆盖，并以非零状态报告冲突。
- [x] **AC5（逐对象原子与真实回声）**：每个用户配置文件先完整校验再写临时文件并原子替换，失败不留截断文件或临时垃圾；某个独立组件失败时，日志明确哪些步骤已完成、哪一步失败，不输出笼统“安装完成”。
- [x] **AC6（隔离缺陷回归）**：自动化稳定复现并锁住三个已知缺陷——单 marker 内容丢失、注释伪命中、真实命令目录下误建内部软链；每个场景都验证退出码、文件内容和目标树零意外变化。
- [x] **AC7（现有路径非回归）**：隔离 HOME 验证空环境首装、重复安装、仓路径迁移、无 Codex CLI 和 fake Codex installer 五类成功/部分成功路径；真实用户 HOME 不参与测试。
- [x] **AC8（总回归与说明）**：`bash scripts/verify-dual-host.sh`、相关专项测试和 `git diff --check` 全绿；安装输出或人读文档能告诉用户如何处理 marker、重复 export 和命令目录冲突，改动不越出 R1。

# Verification Method

- AC1–5：隔离 HOME 文件/权限/软链树断言，并核对 `setup.sh` 退出码和日志内容。
- AC6：为三个已复现缺陷建立固定测试夹具，验证修复前会失败、修复后通过。
- AC7：扩展现有 setup 双分支和幂等矩阵，加入旧仓路径迁移场景。
- AC8：运行 setup 专项测试、`bash scripts/verify-dual-host.sh`、`git diff --check`，并检查 Git diff 作用域。

# Open Questions / Risks

- Bash 在 macOS 与 Linux 的 `sed`、`mv` 和软链行为存在差异；实现应减少平台分支，并把可移植性留给自动测试证明。
- “可证明为 Butler 所有的旧软链”需要足够严格，不能只凭目录名猜；P3 必须给出所有权证据和断链处理方案。
- Codex plugin 安装属于后续独立组件，失败后不回滚已经安全完成的 Claude 配置；但必须非零退出并如实报告部分完成。
