# ITER-0077 · 收件箱数据契约

## 本次交付目标

让需求材料具备稳定来源身份、内容变化检测和派生追踪，同时保持 `origin/` 用户原稿零写入。

## 已完成内容

- 定义 `.ai/INBOX.md` Sources 与 Derivations 两张表。
- 定义 `SRC-NNNN`、observed/processed 双 SHA-256 和七态状态机。
- 定义同源幂等、同源变化、跨源重复候选及失败原子性。
- 接入部署、Coder 导航和 HUMAN_GUIDE，新增 7 项结构测试。

## 关键变更 / 用户可感知变化

- 系统可区分“同一来源的新内容”和“不同来源的相同内容”。
- 一份原稿能追到多个派生产物，多个来源也能共同支撑一个产物。
- AI 不会为处理收件箱而移动、归档或修改用户原稿。

## 高层影响范围

- 新增 `Coder/40_Context_Management/inbox-schema.md`。
- 更新部署协议、Coder README、HUMAN_GUIDE 与结构测试。
- 未实现扫描/分类/路由命令；R4 承接。

## 验证方式与结果摘要

- 专项 7/7、完整 CI exit 0、167 hooks 通过。
- Goal adjudicator 十项全绿；强审最终 Must Fix 0。

## 已知剩余风险 / 延后事项

- 行为幂等和路由事务仍需 R4 fixture 证明。
- 未执行 fresh-context 独立复核。

## 引用

- `.ai/iterations/ITER-0077/`
- `.ai/iterations/ITER-0077/evidence/`
