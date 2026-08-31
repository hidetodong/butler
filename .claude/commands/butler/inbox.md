---
description: 记闪念、看闪念口与孵化区、执行一次已经定好的处置（孵化 / 做掉 / 不做 / 提升 / 开迭代 / 撤回）
argument-hint: "[add <一句话> | list | handle]"
---

你正在执行 Butler 需求录入动作。本入口是薄壳，不复制契约字段、状态机与动作边界。

1. 从 `$BUTLER_PATH` 解析 Butler 仓库；未设置或缺少 `Coder/README.md` 时停止，不猜规则位置。
2. 按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1` 解析唯一 `PROJECT_ROOT`；所有 `.ai/` 写入都相对它。
3. 完整读取 `$BUTLER_PATH/Coder/40_Context_Management/intake-schema.md`（数据形态与合法转移）与 `intake-workflow.md`（动作边界）。
4. 按 `$ARGUMENTS` 选 add / list / handle；留空按 list 的只读列出处理。
5. 结构性写盘只经 `$BUTLER_PATH/tools/intake/intake.py`，传 `--project-root <PROJECT_ROOT>`：闪念表的行、待办区索引行、草稿顶部标记与段落骨架，**不得**用编辑器直接改。唯一由你用编辑器写的是孵化区草稿的正文，把工具留下的占位标记换成真内容。
6. 处置的**决定**由你先问用户，不交给工具猜：孵化还是丢、规模哪一档、暂缓或撤回的原因，都要先问出来再翻译成参数。纯中文闪念推不出短英文键时，回来问用户要一个，不得自己音译。

收尾把工具回执讲成人话：新键是什么、现在什么状态、哪几个文件被写了。被 `current` 挡住时如实说「有一个 active 占着，这条得等」，不得擅自收口去腾位置。
