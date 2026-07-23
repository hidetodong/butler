# TECH_PLAN — ITER-0088

方案状态: pass

# Design Decisions
- check 命令以 marker 为 strict 开关；project 枚举 manifest 五路径。
- hook rule 调驻留 check 内核或共享 Python import，结构坏 deny，legacy N/A。
- auditor/CI 独立调用 CLI，避免 hook 是唯一守门人。

# Failure Paths
- malformed marker、未知版本、结构漂移 exit 1；工具/manifest 错误 exit 2。

# Test Strategy
- CLI、hook、auditor contract 与全量矩阵。

# References Compliance
- N/A
