> 分流: 完整 | 命中升级信号: 多文件改动、设计取舍 | 2026-06-30

# 一句话

给四件套（重点是 CONCEPT）补一条"分层 + 渐进展开"的写法，让同一份文档**既能让人 15 秒看懂要干嘛、又能让 AI 稳定照着干**。做法是：顶部先放一句话意图，再列结构化目标，最后才放精确引用——三层各干一件事、不互相串味。起因是一份实战 CONCEPT（ultra-learning ITER-0016）信息很精确却糊成一团，人读着累、AI 也得现拆关系。

# Goal

- 在 ITER-0012 的"讲人话 + 反啰嗦"之上，补"分层 / 渐进展开"原则：顶部一句话 gist、一行一个意思（拆箭头链）、承重引用首次出现给一句话解释、散文层与精度层不串味。
- 显式声明"不啰嗦 ≠ 极限压缩"，避免反啰嗦被误读成"再压一点"。

# Current Understanding

- 上一轮（ITER-0012）治的是"臃肿 + 黑话填充"；这轮治的是反过来那种病——"太挤 + 太省 + 没铺台阶"，典型就是 ultra-learning ITER-0016 那份。
- 想清楚的核心：对人友好和对 AI 友好不是取舍、是同一件事；唯一偏差是 AI 比人更需要精确引用（路径 / 符号 / payload），用"分层"吸收掉——精度单独成层，人不看也懂意图、AI 要用直接拿得到。
- 落点：跨四件套的通用原则进 `artifact-style.md`；CONCEPT 专属的"一句话"顶部块进 `concept-schema` 模板。

# Constraints

- 叠加扩展，不推翻 ITER-0012 的 §2 / §3；新增"不啰嗦 ≠ 极限压缩"消除误读。
- concept-schema 加"一句话"块是新增、向后兼容：老 CONCEPT 没有也按 legacy 放行；hook 只看文件在不在、不看内部结构，不受影响。
- 不改其它三件套字段结构、不改 lifecycle、不改对话层规则。
- 守本仓 CLAUDE.md 五约束。

# Impact Scope

- 会改：
  - `artifact-style.md`：加"渐进展开 / 分层"节 + 分层骨架样例。
  - `concept-schema.md`：模板顶部加"一句话"块 + 必填字段 + 编写规则。
  - `templates/rule-card.md`：产物书写节补 gist-first / 一行一意 / 不串层。
  - `Coder/README.md`：artifact-style 描述行反映分层。
- 不影响：其它三件套字段、lifecycle 分流格式、对话层规则、hook、迭代 / 里程碑 / 版本机制、历史产物。

# Project Type / Active Profiles

- 形态：Markdown 规则仓库（butler 自己），改的是协作 SOP 规则本身。
- Profiles：无，按通用 SOP + 本仓 CLAUDE.md 编辑约束推进。

# Open Questions

- "一句话"块在 concept-schema 设为完整路径必填、简化路径可选——倾向如此，P2 定。
- 是否给 TECH_PLAN 也加一句话 gist——本轮不做、留将来，避免范围膨胀。
