# VERIFY_REPORT — ITER-0051

> 2026-07-17 · P5 自审 · 结论：AC1–AC9 全部通过，R1 可收口。

## 验收结果

| AC | 结果 | 证据 |
|---|---|---|
| AC1 | ✅ 通过 | 仓根 `AGENTS.md` 存在；真实 `codex exec --ephemeral --sandbox read-only` 能复述“规则仓而非业务仓”、首读文件和验证命令，证明原生发现生效。 |
| AC2 | ✅ 通过 | `AGENTS.md` 明列地图→台账→断点→当前四件套→`Coder/` 的固定读序，并禁止自动全读历史；结构脚本逐项断言。 |
| AC3 | ✅ 通过 | `templates/AGENTS.md.template` 含版本、规则卡、仓路径三个占位符和 user-managed 保护区；自检脚本核对两模板共同深读指针。 |
| AC4 | ✅ 通过 | `docs/codex-compatibility.md` 划清共同内核、Claude 适配层、Codex 适配层，并把入口薄壳、算法归共同真源写成维护红线。 |
| AC5 | ✅ 通过 | 文档明确 R1–R4 边界，并点明现有 gate 只认 `Edit/Write/MultiEdit` + `file_path`，Codex `apply_patch` 在 R3 前没有机械门禁。 |
| AC6 | ✅ 通过 | README、Coder README、HUMAN_GUIDE 均只做短注册并回指共同说明；自动检查通过。 |
| AC7 | ✅ 通过 | `git diff --exit-code -- CLAUDE.md .claude templates/hooks templates/settings.hooks-snippet.json scripts/setup.sh` 无输出；`uv run --with pytest pytest templates/hooks/tests -q` 为 109 passed。 |
| AC8 | ✅ 通过 | 自检脚本在仓根与 `/tmp` 两处均 PASS；`bash -n` 和 `git diff --check` 均通过。 |
| AC9 | ✅ 通过 | `VERSION`、CHANGELOG 顶条、`migrations/v2.12.0.md` 与本地 `v2.12.0` tag 四方一致。 |

## 自动验证记录

- `bash scripts/verify-codex-foundation.sh` → PASS。
- 从 `/tmp` 以绝对路径调用同一脚本 → PASS，证明不依赖 cwd。
- `bash -n scripts/verify-codex-foundation.sh` → PASS。
- `uv run --with pytest pytest templates/hooks/tests -q` → 109 passed in 0.66s。
- Claude 入口、命令、hook、setup 定向 diff → 无变化。
- 真实 Codex 只读探测准确回答仓库定位、第一冷启动文件 `.ai/project/00_INDEX.md`、验证命令。

## 自审结论

- Must Fix：无。
- Should Fix：无 R1 阻断项。
- 独立复核：未触发；本迭代是 Markdown 入口、模板和零依赖检查，没有高风险算法或运行时 hook 改动，客观回归与真实 Codex 探测已覆盖新面。

## 剩余风险 / 延后事项

- R2 的 8 个 skills/plugin、R3 的 Codex hooks 与 `apply_patch` 适配、R4 的目标项目部署/升级双入口仍未完成；因此 v2.12.0 只能称“兼容地基”，不能称“全面兼容”。
- `AGENTS.md.template` 尚未接入 `setup.sh` 或目标项目升级流程，这是冻结范围内的有意延后，不是 R1 缺陷。
