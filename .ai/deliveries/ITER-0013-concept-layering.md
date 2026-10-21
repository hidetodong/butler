# CONCEPT 分层 / 渐进展开：同时对人和 AI 友好

> ITER-0013 · 迭代交付（小版本） · 收口 2026-06-30

## 本次交付目标

- 上一轮（ITER-0012）治好了"臃肿 + 黑话填充"，但还有反过来一种病没治：产物（尤其 CONCEPT）"太挤 + 太省 + 没铺台阶"——信息很精确却糊成一团，人读着累、AI 也得现拆关系才能动手。
- 这次补一条"分层 / 渐进展开"的写法，让同一份文档**既能让人 15 秒看懂要干嘛、又能让 AI 稳定照着干**。

## 已完成内容

- `artifact-style.md` 新增一节「渐进展开与分层」，五条原则：
  - 顶部先放一句话意图（让冷读者先抓意图再看细节）。
  - 一行一个意思，多步列成步骤、别用箭头链。
  - 承重引用第一次出现给一句话解释——不止 butler 黑话，也含项目里的关键符号 / 文件 / 表。
  - 不串层：散文层不夹密集符号、精确引用单独成一层。
  - 明确"不啰嗦 ≠ 极限压缩"，防止上一轮的反啰嗦被误读成"再压一点"。
  - 附了一个分层 CONCEPT 骨架样例 + 一个箭头链反例，可照抄。
- `concept-schema.md` 模板顶部加了「一句话」块，列入必填字段，并写清它和 `Goal` 的分工（一句话是散文意图速览，Goal 是结构化目标项）。
- rule-card 和 README 同步收录这条口径。

## 关键变更 / 用户可感知变化

- 以后新写的 CONCEPT 顶部会有一句话意图，先讲清"干嘛 + 为什么"，不用从一堆目标里自己拼。
- "对人友好"和"对 AI 友好"被明确成同一件事：唯一偏差（AI 更需要精确引用）用"分层"吸收——精度单独成层，人不看也懂意图、AI 要用直接拿。
- 向后兼容：老 CONCEPT 没有"一句话"块按 legacy 放行；hook 不看文档内部结构，不受影响。
- 本迭代自己的 CONCEPT 就是按新结构写的，可当样板。

## 高层影响范围

- 规则层：改 `artifact-style.md`、`concept-schema.md`、rule-card、README。
- 没碰：其它三件套字段结构、lifecycle 分流格式、对话层规则、hook、迭代 / 里程碑 / 版本机制、历史产物。

## 验证方式与结果摘要

- 9 条验收项全部满足：新节五要点 + 骨架样例齐全、concept-schema 加块 + 必填 + legacy、rule-card / README 同步，grep 全中。
- 不冲突核对：ITER-0012 的 §2 / §3 原样保留，"不啰嗦 ≠ 极限压缩"已显式化解误读。
- 本迭代 CONCEPT 自身顶部带"一句话"层（dogfood）。本仓 CLAUDE.md 五约束自检通过。

## 已知剩余风险 / 延后事项

- 分层 / gist 靠 AI 读取并遵守，没有 hook 机械强制——同 ITER-0012，可接受。
- "一句话"和 Goal 有写重的风险，用分工说明 + 样例兜底。
- TECH_PLAN 是否也加一句话 gist：本轮没做，留将来。
- 本轮不切版，ITER-0012 + ITER-0013 一起累积到下次发布，预计 MINOR。

## 引用

- `.ai/iterations/ITER-0013/CONCEPT.md`
- `.ai/iterations/ITER-0013/AC_LIST.md`
- `.ai/iterations/ITER-0013/TECH_PLAN.md`
- `.ai/iterations/ITER-0013/VERIFY_REPORT.md`
- 改动规则：`Coder/20_Workflow_Lifecycle/artifact-style.md`（§4 新增）、`Coder/20_Workflow_Lifecycle/concept-schema.md`
