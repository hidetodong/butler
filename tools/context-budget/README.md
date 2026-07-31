# context-budget

确定性检查 Butler 的 L0–L3 渐进上下文合同与主交付链上下文映射。它只使用 Python 标准库，以 UTF-8 bytes、行数、Markdown 指针数和固定结构作为跨模型稳定代理；不假装测量模型真实 token，也不证明模型运行时一定遵守了读取指令。

## 命令

```bash
python3 tools/context-budget/context_budget.py check --project-root .
python3 -m unittest discover -s tools/context-budget/tests
```

退出码：

- `0`：合同通过。
- `1`：项目存在预算或结构违约。
- `2`：输入、文件布局、编码或表格结构非法。

## 合同边界

- L0：唯一标记块，检查 bytes、非空行、指针数和三类路由语义。
- L1：检查全文预算、五上下文、四读取路径、六字段扇出升级回执和禁止模式。
- L2：检查恰好 20 项术语、必填列、唯一概念、合法所有者和真实定义真源。
- 主链映射：检查四类事实层级、五段转换、九个必填字段、上下文方向、修复真源、每段 1–3 份仓内直接真源、体量与禁止递归护栏。
- 运行时：静态工具不能观察真实读取行为；短任务用用户可见的进度回执，跨会话任务再同步 `.ai/task-state.md`。

`butler-min:` 当前使用 Markdown 固定表头和轻量行解析；若表格开始需要转义竖线、多行单元格或机器迁移，再升级为正式 Markdown AST/registry。
