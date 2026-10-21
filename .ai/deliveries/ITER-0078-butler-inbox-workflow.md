# ITER-0078 · `/butler:inbox` 命令与分类路由

## 本次交付目标

让项目能确定性发现需求材料、保留来源身份，并在不覆盖活工作区的前提下把每项材料送到正确的 Butler 动作。

## 已完成内容

- 交付 `tools/inbox/inbox.py`：零写 plan、原子 apply、status、原始字节 hash、幂等/变化/缺失检测和稳定 JSON。
- 交付 managed INBOX parser/renderer，严格保留管理块外内容，损坏 marker/ledger fail-closed。
- 交付分类、确认、危险模式自审、八类委托路由和批量冲突隔离协议。
- 新增 Claude `/butler:inbox` 与 Codex `$butler-inbox`，registry 和 repo discovery 从 10 扩到 11 项。
- 新增 scanner、workflow、registry 隔离回归并接入完整 CI。

## 关键变更 / 用户可感知变化

- `origin/` 中的新文件现在可以被扫描登记，而不会被改写、移动或删除。
- 同一路径内容变化会沿用原 `SRC-NNNN` 并亮出 `source-changed`，不会重复造来源。
- standard 模式先确认路由；dangerous 模式也必须先自审留痕。冲突项等待时，无依赖 sibling 可以继续。
- 双宿主都能通过统一 inbox 入口发现这套能力。

## 高层影响范围

- 新增 scanner、动作协议、双宿主入口和第 11 项工作流注册。
- 更新 inbox 数据契约、Codex plugin/validator、README/HUMAN_GUIDE 与当前能力口径。
- 不改写 legacy PRD 动作内部算法；多 PRD 引用、迁移、split/update 适配仍由 R5–R7 承接。

## 验证方式与结果摘要

- scanner 专项 11/11、registry 8/8、协议结构 5/5、完整 CI exit 0、170 hooks 和 diff check 通过。
- Goal adjudicator 十项全绿；强审最终 Must Fix 0、Should Fix 0。
- 一条系统 Python 缺 pytest 的失败 record 按证据纪律保留，随后用仓库锁定 uv 环境 reproduced 通过。

## 已知剩余风险 / 延后事项

- AI 分类质量将在 R8 用代表性需求材料做端到端验证。
- 多 PRD 首切/更新的真实目录与事务能力仍待 R5–R7；当前入口不会把待确认或未支持动作冒充完成。
- 未执行 fresh-context 独立复核。

## 引用

- `.ai/iterations/ITER-0078/`
- `.ai/iterations/ITER-0078/evidence/`
- `Coder/40_Context_Management/inbox-workflow.md`
- `tools/inbox/`
