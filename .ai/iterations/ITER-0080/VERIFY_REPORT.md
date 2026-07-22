# Verification Summary

- ITER-0080 已把 PRD 首切切换为身份四态 + 日期证据 + `<prd_id>/` 双层索引，并交付确定性只读 status 与双宿主筛选入口。
- status 行为 14/14、规则结构 7/7、registry 45 个投影对账、完整 CI（182 hooks + inbox/migration/status 行为组）和 diff check 通过。
- 强审修复 3 个 Must Fix；最终 Must Fix 0、Should Fix 0。

# AC Status

- [x] AC1 (auto·可靠): 四态身份闸先于写盘，仅 new-requirement 进入首切 ✓
- [x] AC2 (auto·可靠): 首次进入日期要求显式证据，当前日期/mtime/发布日/改版日均禁猜 ✓
- [x] AC3 (auto·可靠): 项目总索引 + 独立需求目录、无损模块与小 PRD 单模块合同完整 ✓
- [x] AC4 (auto·可靠): 身份、模块边界与四类 Workspace Scope 一次 soft 对齐，模块只收窄 ✓
- [x] AC5 (auto·可靠): status 列表、prd_id 下钻、workspace 筛选及跨 PRD 同名 slug 独立通过 ✓
- [x] AC6 (auto·可靠): collection/legacy、零写、混合/重复/漂移/symlink/retired workspace 负向通过 ✓
- [x] AC7 (auto·可靠): 新 milestone 指针使用 prd_id#module_slug，slug-only 仅历史兼容 ✓
- [x] AC8 (auto·可靠): Claude/Codex 参数与同一 status 工具对齐，registry 无漂移，update 必须显式 prd_id ✓
- [x] AC9 (auto·可靠): 专项、完整 CI、diff check、Goal/state audit 通过 ✓

# Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| prd-status-tests | AC5, AC6, AC9 | captured | launch_error（错误地把 env 赋值当 argv；由下一条纠正） | `.ai/iterations/ITER-0080/evidence/prd-status-tests/record.json` |
| reproduced-prd-status-tests | AC5, AC6, AC9 | reproduced | passed | `.ai/iterations/ITER-0080/evidence/reproduced-prd-status-tests/record.json` |
| prd-split-status-contract | AC1–AC4, AC7–AC9 | captured | passed | `.ai/iterations/ITER-0080/evidence/prd-split-status-contract/record.json` |
| workflow-registry-check | AC8, AC9 | captured | passed | `.ai/iterations/ITER-0080/evidence/workflow-registry-check/record.json` |
| reproduced-full-ci | AC1–AC9 | reproduced | passed | `.ai/iterations/ITER-0080/evidence/reproduced-full-ci/record.json` |
| diff-check | AC9 | captured | passed | `.ai/iterations/ITER-0080/evidence/diff-check/record.json` |

# Verification Results

- AC1–AC4：结构合同核对四态、禁止日期猜测、双层索引、逐字模块、单模块退化和身份/范围/模块一次对齐。
- AC5–AC6：14 个隔离项目用例覆盖两份 PRD 同名 `shared-flow`、详情/工作区筛选、legacy、无匹配 exit 1、所有路径树 hash 零变化，以及混合布局、重复/幽灵 ID、索引漂移、scope retired、树内/祖先 symlink 和坏 CLI。
- AC7–AC8：milestone 新锚点唯一化；两个宿主都把 status 委托同一 CLI、update 强制目标 ID；registry 11 workflows / 45 projections 零漂移。
- AC9：唯一完整 CI exit 0；182 hooks、inbox 11、migration 11、status 14 以及双宿主/Markdown/Goal 合同均通过。

# Goal Calibration

- CAL-001：强审发现 status 未交叉核验 workspace map，retired/拼错 key 可能混入需求范围 → 加 active map 解析与负向 fixture → resolved（reproduced-prd-status-tests）。
- CAL-002：强审发现 `.ai`/project 祖先 symlink 可让只读查询越出项目根 → 逐组件拒绝并校验 resolved path → resolved（reproduced-prd-status-tests）。
- CAL-003：argparse 自带错误会绕过稳定 JSON → 自定义 parser 将坏参数统一为 exit 2 JSON → resolved（reproduced-prd-status-tests）。
- CAL-004：首次完整 CI 读取到 ITER-0079 的 task-state resolved 行 → 新迭代投影整体覆写为 N/A，第二次完整 CI 通过 → resolved（reproduced-full-ci）。

# Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

# Gate Coverage

- 通用质量门禁：专项 21 项、完整 CI、182 hooks、Markdown、双宿主、Goal 与 diff check 通过。
- Tech Plan Alignment：窄 Markdown parser、project index 发现真源、目录/workspace 交叉核验、稳定 JSON 与 host 薄路由均兑现。
- References Compliance：N/A；本迭代未注入外部 PRD，以隔离 synthetic fixture 验证集合行为。

# Review

- 危险模式同上下文完整强审；修复 workspace active 交叉核验、祖先 symlink 逃逸与 argparse 非 JSON 三个 Must Fix。最终 Must Fix 0、Should Fix 0。
- 未执行 fresh-context 独立复核。

# Remaining Risks

- update 仍没有 R7 的事务执行器和持久 receipt；命令已诚实标注，不宣称原子更新可用。
- 实际代码改动与 Workspace Scope 的发现/diff/hook 对账、真实 apps dogfood 留 R8。
- Pi TypeScript 依赖缺失继续按既有 CI 规则降级为警告。

# Handoff / Next Step

- Goal eligible 后关闭 ITER-0080，继续 R7 确定性 PRD 改版与回执。
