# Goal Assurance

只读完成资格裁决器：`python3 tools/goal-assurance/goal.py evaluate --project-root <PROJECT_ROOT>`。

- stdout 始终为 JSON；`eligible` exit 0，`ineligible` exit 1，项目输入不可解析 exit 2。
- `eligible` 只允许进入收口仪式，不等于 `complete`；complete 仍由 closed 台账、归档、交付和状态审计派生。
- 工具不写任何文件，不读取宿主 Goal/Task 或 Execution Steps。
