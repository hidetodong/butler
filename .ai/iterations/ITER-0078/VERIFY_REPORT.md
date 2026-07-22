# Verification Summary

- ITER-0078 已交付可执行的需求收件箱 scanner、语义路由协议与 Claude/Codex 双宿主入口。
- scanner 专项 11/11、registry 8/8、协议结构 5/5、完整 CI（170 hooks）和 diff check 通过。
- 强审修复 3 个 Must Fix；最终 Must Fix 0、Should Fix 0。

# AC Status

- [x] AC1 (auto·可靠): scan 默认零写 plan，apply 原子维护 managed block 且保留块外内容 ✓
- [x] AC2 (auto·可靠): origin 递归原始字节 hash，symlink/逃逸/控制字符 fail-closed，缺失不创建 ✓
- [x] AC3 (auto·可靠): locator+hash 幂等、内容变化保留 source_id、缺失来源保留历史 ✓
- [x] AC4 (auto·可靠): 稳定 JSON、封闭计数、异常 exit 2 与零部分写入 ✓
- [x] AC5 (auto·可靠): workflow 逐项分类，standard 确认与 dangerous 自审审计门明确 ✓
- [x] AC6 (auto·可靠): 八类分类到 PRD/update/reference/ideation/backlog/record-only 的委托矩阵完整 ✓
- [x] AC7 (auto·可靠): 活工作区保护、按项事务和独立 sibling 继续规则明确 ✓
- [x] AC8 (auto·可靠): `/butler:inbox`、`$butler-inbox`、11 项 registry、repo discovery 与生成投影一致 ✓
- [x] AC9 (auto·可靠): 隔离 fixture、registry、双宿主、完整 CI 与 diff check 全通过 ✓

# Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| inbox-tool-tests | AC1–AC4, AC9 | captured | passed | `.ai/iterations/ITER-0078/evidence/inbox-tool-tests/record.json` |
| inbox-workflow-registry | AC5–AC9 | captured | failed（系统 Python 缺 pytest，保留诊断） | `.ai/iterations/ITER-0078/evidence/inbox-workflow-registry/record.json` |
| inbox-workflow-registry-reproduced | AC5–AC9 | reproduced | passed | `.ai/iterations/ITER-0078/evidence/inbox-workflow-registry-reproduced/record.json` |
| diff-check | AC9 | captured | passed | `.ai/iterations/ITER-0078/evidence/diff-check/record.json` |
| reproduced-full-ci | AC1–AC9 | reproduced | passed | `.ai/iterations/ITER-0078/evidence/reproduced-full-ci/record.json` |

# Verification Results

- AC1–AC4：11 个临时项目 fixture 覆盖 plan/apply、幂等、变更、缺失、symlink/断链、控制字符路径、损坏 ledger、块外逐字保留、subprocess JSON 和 origin 原文 hash 对账。
- AC5–AC7：结构回归核对八类分类、确认/危险自审、RUN_LOG、processed hash、活工作区冲突与 sibling 隔离；动作真源只委托既有 PRD/ideation/milestone 规则。
- AC8：registry 8 个回归、sync --check、11 skills 官方 validator 与相对 discovery symlink 全绿。
- AC9：锁定 uv 环境的完整 CI exit 0，170 个 hooks 测试通过；Pi TypeScript 依赖缺失仍按既有 CI 合同亮警告并跳过，不计失败。

# Goal Calibration

- CAL-001：管理块 parser 起初错误假定标题后无空行 → 改为跳过规范空行并严格校验分隔行 → resolved（inbox-tool-tests）。
- CAL-002：首次接管已有 INBOX 曾 `rstrip` 块外尾随内容，且断链 origin symlink 会被当作缺失 → 保留原始前后缀并先判 symlink → resolved（inbox-tool-tests + reproduced-full-ci）。
- CAL-003：registry 新增首项后，重复 ID fixture 固定改第二项为 `prd` 不再制造重复 → 改为动态复制首项 ID → resolved（inbox-workflow-registry-reproduced）。

# Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

# Gate Coverage

- 通用质量门禁：专项 scanner 11/11、registry 8/8、协议结构 5/5、完整 CI、170 hooks、Markdown、双宿主、Goal 与 diff check 通过。
- Tech Plan Alignment：确定性 CLI 管事实、薄工作流管语义、既有规则管派生；未引入 JSON 第二真源或 CLI 语义分类器。
- References Compliance：N/A；无外部 PRD，scanner 只 hash 原始 bytes，不复制 origin 内容。

# Review

- 危险模式同上下文完整强审；共修复 3 个 Must Fix：managed table 空行解析、块外尾随内容损失/断链 symlink 漏拒绝、registry 重复 ID fixture 漂移。最终 Must Fix 0、Should Fix 0。
- 未执行 fresh-context 独立复核。

# Remaining Risks

- AI 语义分类本身不能由 scanner 单测证明；R8 将用代表性需求材料做端到端路由回归。
- 当前 workflow 能安全委托现有 PRD 动作，但这些动作仍按 legacy 单 PRD 路径运行；R5–R7 完成前，多 PRD 新建/更新不得误报为已全自动。
- Pi TypeScript 依赖缺失继续按既有 CI 规则降级为警告。

# Handoff / Next Step

- Goal eligible 后关闭 ITER-0078，继续 R5 多 PRD 引用、兼容迁移与人类指南。
