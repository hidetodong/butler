# ITER-0110 · 最小可执行领域合同与双冲突试点（MILE-0015 R4）

- 交付级别：迭代交付（小版本）
- 收口日期：2026-08-13
- 所属里程碑：MILE-0015（Butler 领域模型治理）

## 本次交付目标

把 R1–R3 已讲清的高风险领域边界变成能自动抓回归的最小机器合同，并用两个现存冲突验证合同真能约束实现——解除 Dangerous Mode 与 Convergence Loop 的错误包含，统一 VERIFY「人测道小结」的结构所有权。

## 已完成内容

- 新增最小领域合同工具 `tools/domain-contract/`：只登记「身份—上下文—种类—唯一所有者—真源」+ 关系与断言，fail-closed 校验重复/悬空/越界/复制型载荷。
- 新增共享「有界 P4 收敛策略」`Coder/30_Quality_Gate/bounded-convergence.md`，Dangerous 与 Loop 并列引用、互不激活。
- 解除 5 个规则文件的 Dangerous/Loop 耦合措辞。
- 把「人测道小结」结构所有权写回 artifact manifest/template，verify-schema 只解释触发/回填。
- 给 strict VERIFY 补确定性迁移（缺段插入 + 幂等 + 拒绝诊断）。
- 补 11 例领域合同 fixture + 5 例迁移 fixture，接入完整 CI。
- 还掉 `debt.md` 里两条欠债。

## 关键变更 / 用户可感知变化

- `/butler:dangerous` 不再被写成「自动复用 Loop」：两者是并列模式，各自显式触发、互不激活。
- VERIFY 报告新增固定「人测道小结」段（缺省 N/A），结构由机器清单统一，不再出现「写进去被判错、不写又违规」。
- 旧的 strict VERIFY 报告可通过确定性迁移补段，重复/错位/未知 marker 会被拒绝并给路径诊断。

## 高层影响范围

- 新增 `tools/domain-contract/`、`Coder/30_Quality_Gate/bounded-convergence.md`。
- 修改 `Coder/` 下 5 个规则文件、`tools/artifact-pipeline/`（manifest/template/migration）、`scripts/verify-ci.sh`、`.ai/project/debt.md`。
- 不触碰 MILE-0014 的 Decision Map / Work / Promotion / Router 状态机。

## 验证方式与结果摘要

- 完整 `verify-ci.sh` 退出码 0（含 MILE-0014 三 Module + Router、context-budget、artifact contract、markdown 链接、state audit、全量单测）。
- 证据见 `.ai/iterations/ITER-0110/evidence/`（6 条 record，outcome 全 passed）。
- 8/8 AC 全绿（auto·可靠），裁决 `eligible`。

## 已知剩余风险 / 延后事项

- `tech_plan` 的 manifest（4 段）与 `tech-plan-schema.md`（10 段）仍漂移，建议另开迭代对齐。
- 各宿主运行时实际加载领域文件的遥测留 R5。

## 引用

- `.ai/iterations/ITER-0110/AC_LIST.md`
- `.ai/iterations/ITER-0110/TECH_PLAN.md`
- `.ai/iterations/ITER-0110/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0110/evidence/`
