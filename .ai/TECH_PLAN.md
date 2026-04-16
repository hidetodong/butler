# Goal

- 按 E-1（平台检测 if/else）与 E-2 方案 β（skill 失败直接问用户，不越权网络请求），对 Bucket E 2 条 Should Fix 执行最小范围修复。

# Files / Modules to Change

| # | 文件 | 涉及 AC | 改动点 |
|---|---|---|---|
| 1 | `scripts/setup.sh` | E-1 | 1（`sed -i` 改为 `$OSTYPE` 分支） |
| 2 | `Coder/00_System_Prompt/logic-protocol.md` | E-2 | 1（§ 4.2 末尾追加 Fallback 段） |

共 2 个文件，2 处 edit。

# Interface / Contract

- E-1：脚本行为不变（更新语义一致），只修复 Linux 下的兼容性。
- E-2：规则新增 **Fallback 段落**，明确 skill 失败时 AI **必须**转向用户手动提供而非越权访问网络。属于行为约束增强，不改已有存储路径 / 命名前缀。

# State / Boundary

- 不动 `templates/`、`.ai/references/` 命名约定、其他规则文件。
- 不重构 setup.sh 的 awk 段（已跨平台）、CLAUDE_GLOBAL_MD 处理、shell rc 检测逻辑。

# Design Decisions

1. **E-1 使用 `$OSTYPE` 判断**：macOS 下 `$OSTYPE == "darwin20"` 等，统一 `darwin*` glob 匹配；Linux 下多为 `linux-gnu`。其他平台（WSL、Cygwin、FreeBSD）默认走 Linux 分支（GNU sed 语法）。
2. **E-2 β 方案落地位置**：作为新段放在 § 4.2 末尾（"处理规则"列表之后、`## 5. 流程总调度`之前），保留表格与处理规则的原有结构；不引入新的 H3 子标题，降低目录层级复杂度。
3. **E-2 提示语示例采用 `confluence-api-extractor` 作为占位**，便于读者直接套用；MasterGo 等其他 skill 失败时替换名字即可。

# Execution Steps

## Edit 1 — `scripts/setup.sh` L22-25

将 `sed -i '' "..."` 单行调用扩展为 `$OSTYPE` 分支：

```bash
  if grep -q 'BUTLER_PATH' "$SHELL_RC" 2>/dev/null; then
    # 更新已有的 BUTLER_PATH（macOS/BSD 与 Linux sed -i 语法不同）
    if [[ "$OSTYPE" == "darwin"* ]]; then
      sed -i '' "s|export BUTLER_PATH=.*|export BUTLER_PATH=\"$BUTLER_DIR\"|" "$SHELL_RC"
    else
      sed -i "s|export BUTLER_PATH=.*|export BUTLER_PATH=\"$BUTLER_DIR\"|" "$SHELL_RC"
    fi
    echo "[更新] $SHELL_RC 中的 BUTLER_PATH 已更新"
```

## Edit 2 — `logic-protocol.md` § 4.2 末尾追加 Fallback 段

在当前 L103 "若参考资料在执行过程中被更新..."之后、L105 `## 5. 流程总调度` 之前插入：

```markdown
Fallback（skill 不可用或调用失败时）：

- 若目标 skill 未安装、认证失败或调用超时，**不得**自行使用 WebFetch 等工具越权访问外部资源。
- 应主动提示用户手动提取参考资料内容并粘贴到对话，例如："`confluence-api-extractor` skill 不可用，请将 <URL> 页面内容粘贴到对话，我将落盘到 `.ai/references/api-<name>.md`"。
- 收到用户粘贴的文本后，按上表"存储位置"约定落盘，命名前缀保持一致（`api-` / `design-` / `insight-` / 无前缀）。
- Fallback 路径产出的参考资料，在 `AC_LIST.md` / `TECH_PLAN.md` 的 `External References` 中必须标注"用户手动提供"，以便审计区分 skill 自动化产物与人工产物。
```

# Verification Plan

- **E-1**：
  - `bash -n scripts/setup.sh` 语法检查通过。
  - `grep -nE 'OSTYPE|sed -i' scripts/setup.sh` 显示 `$OSTYPE` 分支结构存在且 sed 调用在分支内。
- **E-2**：
  - `grep -n 'Fallback' Coder/00_System_Prompt/logic-protocol.md` 命中。
  - `grep -n '不得.*WebFetch' Coder/00_System_Prompt/logic-protocol.md` 命中，关键约束"不越权"明确落地。
  - 通读 § 4.2，确认 fallback 规则与表格"存储位置"口径一致（命名前缀不变）。
- `git diff --stat` 应显示仅 2 个文件变更。

# Risks / Open Questions

- **风险 1**：本地无 Linux 真机，E-1 的 Linux 分支只能靠代码评审。缓解：`$OSTYPE == "darwin"*` 之外即走 GNU sed 标准语法（`sed -i "..."`），这是 GNU sed 通用用法，代码评审足以确认正确性。
- **风险 2**：`$OSTYPE` 在极少数非标准 shell 环境（老版 POSIX sh）可能未定义。setup.sh shebang 是 `#!/usr/bin/env bash` 且全文依赖 `[[`、`|=` 等 bash 特性，因此 `$OSTYPE` 在本脚本执行环境中总是可用。
- **开放问题**：无。
