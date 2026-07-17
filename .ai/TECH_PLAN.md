# TECH_PLAN — ITER-0055 · 基地车展开边界加固

## 方案摘要

新增一个标准库项目根解析器，把“施工到哪里”从散文猜测收敛成一个可测试的决策。规则真源定义优先级，Claude/Codex 入口和工作流只回指该契约；所有展开命令都使用解析后的绝对路径，不再直接使用 `$(pwd)`。

## 根目录决策

`scripts/resolve-project-root.py` 按以下顺序决定，命中即停：

1. **用户点名目标**：`--user-target <path>`。解析软链后必须是已存在、可写的目录；不要求已初始化 Git。
2. **最近的已部署 Butler 根**：从 `--start` 向上查找，候选必须同时有 `.ai/` 和含 Butler 签名/管理区的 `CLAUDE.md` 或 `AGENTS.md`。
3. **VCS 根**：若不在已部署 Butler 项目中，用 `git -C <start> rev-parse --show-toplevel` 确定当前仓库根。
4. **拒绝**：上述都不成立时退出码 2，提示用户点名项目；不扫描子目录猜候选，不创建任何文件。

解析成功时 stdout 只输出可供 shell 捕获的绝对路径，stderr 回声证据类型和根目录。调用方在任何写入前向用户显示该结果。

## 实现落点

- **单一真源**：在 `mcv-deployment.md` 新增“施工项目根解析”前置门，定义上述决策、回声与零写入约束。
- **可执行真源**：新增 `scripts/resolve-project-root.py`；只用 Python 标准库与本机 Git，实现无副作用解析。
- **部署接线**：MCV 例子先得到 `PROJECT_ROOT`，后续侦察、展开、双入口渲染、hook 验证全部显式使用该路径。
- **渲染防误用**：`render-project-entrypoints.py` 保持 `--target` 显式参数，拒绝不存在/非目录/不可写目标；文档只传 `PROJECT_ROOT`。
- **全局规则注入**：`templates/rule-card.md` 的基地车段压缩为“先解根、再写入”的硬规则；两入口模板继续内联同一 rule-card，不双写算法。
- **工作流路由**：8 个 Claude 命令与 8 个 Codex skills 中涉及项目读写的“当前项目”描述，统一改为“先按 MCV 项目根契约解析，然后以该根为基准”；只加路由指针，不复制判定算法。
- **文档与迁移**：README/HUMAN_GUIDE/兼容说明登记聚合目录边界；如版本判定为 MINOR，产出迁移说明，既有项目结构不需搬迁。

## 验证设计

`scripts/test-resolve-project-root.py` 覆盖：

1. 显式目标在 cwd 之外，仍返回显式目标。
2. 显式无 Git 目录可用。
3. 显式目标不存在/非目录时拒绝。
4. Git 仓子目录定位到顶层。
5. 非 Git 的已部署 Butler 项目从子目录定位到最近根。
6. 包含多仓子目录的聚合父目录拒绝，整棵临时树零新增。
7. 软链路径解析为真实绝对路径。
8. 渲染器对非法目标零写入，对解析后外部目标只写双入口。

交付前复跑 `bash scripts/verify-dual-host.sh`、`python3 -m pytest templates/hooks/tests -q`、plugin validator、`git diff --check`，并绝对路径确认 `research/.ai` 不存在。

## 变更顺序

1. 先写 resolver 失败/成功场景测试，再实现最小解析逻辑。
2. 把 MCV 真源从 `pwd` 切到 `PROJECT_ROOT`，同步规则卡。
3. 更新 Claude/Codex 薄路由指针，保持两宿主语义一致。
4. 更新渲染器边界、文档和统一验证脚本。
5. 跑完整回归，P5 强审后再收口。

## 风险与回退

- **取舍**：无 Git/无 Butler 标记且用户未点名的目录会多一次确认；这是拒绝误展开的有意代价。
- **误认风险**：既有 Butler 根必须验证入口签名，不只看 `.ai/` 目录名。
- **回退**：resolver 是无副作用前置层；若发现兼容性问题，可回退调用接线，不需搬迁任何已部署 `.ai` 数据。

## Execution Steps

- [ ] T1：新增 resolver 及单元/隔离测试（AC1–4/6）。
- [ ] T2：接线 MCV、rule-card 与 renderer 目标验证（AC1–5）。
- [ ] T3：更新 8 Claude 命令 + 8 Codex skills 的单一根契约指针（AC4/5）。
- [ ] T4：更新文档、回归入口和迁移/版本面（AC5/6）。
- [ ] T5：完整回归、事故路径检查与 P5 强审（AC6/7）。
