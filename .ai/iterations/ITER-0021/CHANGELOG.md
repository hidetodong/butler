> ITER-0021（MILE-0002 R1）· active · —

本文件是**当前活跃迭代 ITER-0021** 的对象级变更流（ADD/EDIT/DELETE）。

## ADD
- 无

## EDIT
- `Coder/30_Quality_Gate/testing-strategy.md` §2「测试分层建议」→「自动化优先（硬纪律）」：措辞由建议升级为"凡机器能测的必须自动化"，UI / 交互纳入自动道（浏览器自动化 / 可编程视觉断言）→ AC1
- `Coder/30_Quality_Gate/testing-strategy.md` 新增 §3「分道口径」：自动道 / 人测道判定 + 默认归自动道 + 人测道类目锚点清单（主观审美 / 物理设备 / 真人感知 / 外部人工闸）；原 §3-6 顺移 §4-7 → AC2
- `Coder/30_Quality_Gate/testing-strategy.md` §4（原 §3）最小验证集合"关键路径手动验证"→"默认自动验证"；§5 验收映射 + §7 回写要求补分道结论 → AC1
- `Coder/30_Quality_Gate/testing-strategy.md` frontmatter scope 补"自动化优先纪律 + 分道口径" → AC2
- `Coder/20_Workflow_Lifecycle/verify-schema.md` §2 交付约定加条件字段「人测道小结」 → AC3
- `Coder/20_Workflow_Lifecycle/verify-schema.md` §3 模板 AC Status 加 `(auto)` / `(human)` lane 标记 + 新增「人测道小结」段 → AC3
- `Coder/20_Workflow_Lifecycle/verify-schema.md` §4 编写规则加"分道回填"要求（自动道给可复现证据 / 人测道说明为何不可测）；既有 6 必填字段不变 → AC4, AC5
- `templates/rule-card.md` 执行纪律段加"自动化优先"一句 → AC7
- `Coder/README.md` 规则目录说明（30_Quality_Gate 群组）+ schema 描述（verify 分道回填）同步 → AC6
- `HUMAN_GUIDE.md` 目录树 testing-strategy / verify-schema 两注释同步 → AC6

## DELETE
- 无
