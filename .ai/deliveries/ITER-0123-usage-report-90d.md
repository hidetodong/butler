# ITER-0123 · usage 报告：90 天分档替代手工回忆

- 交付级别：迭代交付（小版本）
- 收口日期：2026-10-19
- 所属里程碑：MILE-0016（Butler 瘦身与重造）

## 本次交付目标

一条命令按时间窗口把全部入口分成 A、B、C、D。人看完自己决定砍不砍。工具不自动淘汰。

## 已完成内容

- 新建 `tools/usage-report/`。默认窗口 90 天，stdout 一份 JSON。
- A 是窗口内用过，B 是更早用过，C 是名单里没记下时间，D 是记录里有、名单已经没有的残留。
- 缺文件或坏文件仍能出完整名单，退出码 0，坏文件一个字节都不改。
- `usage-report` 进了产品工具名单。`debt.md` 里「运行时观测缺位」那条删了。

## 关键变更 / 用户可感知变化

- `python3 tools/usage-report/usage_report.py report --project-root .` 打出四档。
- C 档只表示没有调用记录。工作流大多没有进程钩，会长期停在 C。
- 报告先读调用前的记录，打完之后才给自己记一笔。

## 高层影响范围

- 新增：`tools/usage-report/`。
- 改动：`tools/usage/usage.py` 的产品名单、持续集成、全貌里的工具清单、`debt.md`。
- 不算：不改采集格式，不补次数，不自动砍命令，不切版本。

## 验证方式与结果摘要

9 条验收全部通过。usage-report 测试 6 passed，usage 测试 8 passed。持续集成第三次退出码 0。收口前完成裁决 `eligible`。独立复核未开。

前两次持续集成失败：本机没有 Codex plugin-creator；补上脚本后，任务状态里的未闭合信号又让活文件测试失败。信号改成已解决后第三趟绿。审计 0 条 DRIFT、2 条未发布。

## 已知剩余风险 / 延后事项

- C 档不能当成「已经证实没人用」。
- 真实会话里有没有人看这份报告，本轮不证明。
- 给人读的三份文档里，工作流个数仍然靠手改。
- 本轮不切版、不提交。
- 本机 Codex 技能目录里补进了仓库锁定提交上的四个官方脚本，当前那份新技能仍在另一条路径。

## 引用

- 四件套：`.ai/iterations/ITER-0123/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 变更流：`.ai/iterations/ITER-0123/CHANGELOG.md`
- 证据：`.ai/iterations/ITER-0123/evidence/`（7 条记录）
