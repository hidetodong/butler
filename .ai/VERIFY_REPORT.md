# Verification Summary

ITER-0060 已把八个 Butler 工作流的名称、路径、风险、隐式策略、触发、旧名与分发声明收敛到 `workflows/registry.json`，并以标准库同步器生成/校验 33 个窄投影。危险模式强复核发现 hooks 命令校验只比尾缀的缺口，已收紧为完整对象匹配；最终专项 8/8 与固定工具链完整矩阵通过。

# AC Status（道 + 置信档合并标记）

- [x] AC1 (auto·可靠) ✓ `workflow-registry-tests-closure` 覆盖恰好八项、唯一 ID/名称、未知字段、missing/extra/duplicate、仓内路径与路径逃逸。
- [x] AC2 (auto·可靠) ✓ 同一 record 真跑 write→write→check 摘要对比、frontmatter 正文哨兵与注入失败回滚；`workflow-registry-check-final` 证明真实仓 33 投影无漂移。
- [x] AC3 (auto·可靠) ✓ 专项断言 loop/dangerous high+false、其余六项 true，并拒绝策略翻转与旧高风险实体命令；生成 YAML 全部显式写 policy。
- [x] AC4 (auto·可靠) ✓ 专项覆盖 command/SKILL/openai/doc stale、broken/absolute/copy symlink 和额外 discovery；真实仓 8 个相对软链由 check 对账。
- [x] AC5 (auto·可靠) ✓ 专项拒绝 manifest、hook matcher/command/wrapper mode、installer 与 distribution 漂移；`full-matrix-closure` 通过固定官方 plugin/8 skill validators，个人安装副本已按 cachebuster 流程刷新。
- [x] AC6 (auto·可靠) ✓ `docs/workflows.md` 是 registry 生成的人读表，四份入口文档由 checker 强制指向它；aliases 含 `/loop` harness collision 与弃用状态但不生成旧实体。
- [x] AC7 (auto·可靠) ✓ `workflow-registry-tests-closure` 8/8；`full-matrix-closure` 通过固定 Python/uv、双宿主、Markdown、CI contract、官方 validators 与 127 hook tests。
- [x] AC8 (auto·可靠) ✓ 专项、check、diff、active audit 与完整矩阵均有机器 record；首次系统 Python validator 失败原样保留，固定 uv 入口随后复现通过；强审最终 Must Fix 0、Should Fix 0。

# Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| workflow-registry-tests | AC1–AC4, AC6–AC8 | captured | passed（首版 6 项） | `.ai/iterations/ITER-0060/evidence/workflow-registry-tests/record.json` |
| workflow-registry-check | AC1–AC6, AC8 | captured | passed | `.ai/iterations/ITER-0060/evidence/workflow-registry-check/record.json` |
| diff-check | AC8 | captured | passed | `.ai/iterations/ITER-0060/evidence/diff-check/record.json` |
| state-audit-active | AC8 | captured | passed（UNRELEASED 亮牌） | `.ai/iterations/ITER-0060/evidence/state-audit-active/record.json` |
| full-matrix | AC1–AC8 | captured | passed | `.ai/iterations/ITER-0060/evidence/full-matrix/record.json` |
| workflow-registry-tests-final | AC1–AC8 | reproduced | passed（强审后 7 项） | `.ai/iterations/ITER-0060/evidence/workflow-registry-tests-final/record.json` |
| workflow-registry-check-final | AC1–AC6, AC8 | reproduced | passed | `.ai/iterations/ITER-0060/evidence/workflow-registry-check-final/record.json` |
| plugin-contract-final | AC3–AC5, AC7–AC8 | captured | failed（系统 Python 缺 PyYAML，保留） | `.ai/iterations/ITER-0060/evidence/plugin-contract-final/record.json` |
| full-matrix-final | AC1–AC8 | reproduced | passed（固定 uv 环境） | `.ai/iterations/ITER-0060/evidence/full-matrix-final/record.json` |
| workflow-registry-tests-closure | AC1–AC8 | reproduced | passed（最终 8 项） | `.ai/iterations/ITER-0060/evidence/workflow-registry-tests-closure/record.json` |
| full-matrix-closure | AC1–AC8 | reproduced | passed（最终完整矩阵） | `.ai/iterations/ITER-0060/evidence/full-matrix-closure/record.json` |
| diff-check-closed | AC8 | reproduced | passed（收口态） | `.ai/iterations/ITER-0060/evidence/diff-check-closed/record.json` |
| workflow-registry-check-closed | AC1–AC6, AC8 | reproduced | passed（收口态） | `.ai/iterations/ITER-0060/evidence/workflow-registry-check-closed/record.json` |
| state-audit-closed | AC8 | captured | failed（证据热区存在时 auditor 正确拒绝闭态归档不一致） | `.ai/iterations/ITER-0060/evidence/state-audit-closed/record.json` |

# Verification Results

- 注册表同步器对真实仓报告 `workflows=8 projections=33`，第二次 write 变更数为 0，check 零写入。
- 最终专项 8/8，覆盖 schema/set/path、安全策略、窄投影、文档/软链漂移、plugin/distribution 契约和写失败回滚。
- 最终完整矩阵通过：renderer 8、root resolver 7、installer 16、upgrade 16、evidence 11、auditor 12、Markdown 3、CI contract 5、官方 plugin/8 skills validators 与 127 hook tests。
- plugin-creator 更新链成功：源码 manifest 保持 `2.16.0`，个人安装副本为带 cachebuster 的 `2.16.0+codex.20260718092203`，来自 personal marketplace 且 enabled。
- 收口态 auditor 在 evidence 重开期间正确报归档/热区不一致，失败 record 保留；evidence 重新归档后最终只读 audit 全绿。由于 audit 自身必须检查“热区为空、归档集合闭合”，其最终绿结果不能同时写进正在被它审计的同一 evidence 集合，故最终命令输出作为收口仪式回声，不冒称 record reproduced。

# Gate Coverage

- 通用质量门：未知字段、路径逃逸、集合封闭、软链所有权、高风险隐式策略、原子写/回滚、插件声明、文档单源和固定验证依赖均有机器探测。
- Active Profiles：无；危险模式已执行自主 ACK、checkpoint、RUN_LOG、证据封存与完整审查。
- Tech Plan Alignment：T1–T6 全部兑现；没有生成算法正文、公共 marketplace 或团队配置。
- References Compliance：N/A；未使用外部规格。

# Independent Review

- 未执行 fresh-context 独立复核：当前协作约束未明确授权启动子 agent，未冒称独立。
- 主 agent 逐 AC 冷读 registry、同步器、专项、生成物、hooks、安装链与提交前状态。发现 1 个 Should Fix：hook command 原先仅检查尾缀；另发现 1 个 Must Fix：auditor 只查 tag 名存在、未核 tag→HEAD。前者改为完整 `{type, command}` 精确匹配，后者改为 HEAD 指向对账，均补回归。
- 最终 Must Fix 0，Should Fix 0。

# Remaining Risks

- team/public distribution 仍是 `not-configured`；个人安装成功不能推断团队可用。
- workflow 尚未推送，GitHub Linux/macOS 的真实 run 和 required check 仍受 R3 已记录的远端套餐/可见性限制。
- `--write` 只管理元数据投影，不会替作者同步工作流正文语义；正文继续由 Coder 规则真源治理。
- 官方 validator 必须走 `scripts/verify-ci.sh` 的锁定 uv 环境；裸系统 Python 可能缺 PyYAML，失败 record 已保留。

# Handoff / Next Step

- 归档 ITER-0060 evidence/四件套/changelog，生成 MD/HTML 交付并折叠项目知识；随后关闭 MILE-0007、生成版本级 MD/HTML 总结并跑 closed state audit。
