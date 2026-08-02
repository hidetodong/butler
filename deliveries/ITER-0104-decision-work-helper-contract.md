# Decision Work 帮手合同与显式吸收

## 本次交付目标

把 Wayfinder 式“并行求证”接入 Butler 已有 Decision Map，同时确保 helper 只产出可审阅事实，不能靠模型临场判断直接改 Map 或推进交付流程。

## 已完成内容

- 新增驻留工具 `tools/decision-work/`，以 `inspect`、`plan`、`apply`、`verify` 四动作统一管理不可变 Task Packet 与 Result Envelope。
- 用一个 helper 合同覆盖 research、prototype、grilling、task 四种模式；只有 Research 可对显式选择且分别 claim 的 Decision 组成受控 batch。
- 建立 candidate、needs-input、failed、cancelled 与 predecessor Attempt 合同；迟到结果可保存为参考，但不会自动 retry、re-claim 或 resolve。
- 将候选吸收固定为协调器显式动作，并只通过 Decision Map Module 提交 resolve 与带摘要的相对证据指针。
- 接入 Ideation、帮手名册、驻留工具说明、统一领域词汇、workflow 静态边界与完整 CI。

## 关键变更 / 用户可感知变化

- Explore 仍是单一 opt-in 入口；模型不会根据需求大小、清晰度或置信度自动启用 Decision Work。
- 前期流程现在是明确的“展示 Frontier → 显式选 ID → 逐项 claim → prepare → helper/HITL → record → 审阅 → absorb”，每一步都可恢复、可核验。
- 并行的是隔离的 Research 求证，不是 Map 写入。Prototype、Grilling、Task 保持单项 serial/HITL，宿主不支持并行时必须如实降级。
- helper 完成、result 落盘或 `absorbable=true` 都不等于 Decision 已解决；跳过 absorb 时 R2 state 保持不变。

## 高层影响范围

- 新增 `tools/decision-work/` 深 Module、CLI、合同文档和 17 项专项测试。
- 新增 `Coder/62_Extension_Agents/decision-work.md`，并更新 Agents 总述、Ideation 真源、驻留工具部署说明、Coder / 项目 README 与 `CONTEXT.md`。
- 扩展 workflow registry 合同测试和 `verify-dual-host.sh`，但没有新增 workflow ID、宿主命令、R2 schema、agent scheduler 或 R4 promotion。

## 验证方式与结果摘要

- Decision Work 专项 17 项通过，覆盖四类 schema、真实双进程竞争、故障回滚、跨进程恢复、迟到/stale/篡改和显式 absorb。
- P5 同上下文简评发现的幂等重新 plan 问题已修复；风险定点测试重新执行并以 `reproduced` evidence 通过，最终 Must Fix 0、Should Fix 0。
- Workflow 合同 12 项通过，确认 Router + 13 workflows、单一 Ideation 入口、opt-in 与从 P1 promotion 的边界不变。
- 完整 `scripts/verify-ci.sh` 在 Python 3.12.12 / uv 0.9.28 下 exit 0；四份 evidence 已归档并通过 archive verifier。

## 已知剩余风险 / 延后事项

- 核心只能校验宿主回传的实际执行模式，不能证明第三方宿主真的创建了 fresh-context worker；多宿主端到端 dogfood 留给 MILE-0014 R5。
- 不可变 sidecar 会随 Attempt 增长；随 Map promotion/归档的生命周期属于 R4。
- Claim token digest 是本地绑定而非身份认证；文件锁与原子发布不覆盖跨主机或网络文件系统。
- R4 promotion/admission 尚未启动，本轮不会自动创建下一迭代。

## 引用

- `.ai/iterations/ITER-0104/CONCEPT.md`
- `.ai/iterations/ITER-0104/AC_LIST.md`
- `.ai/iterations/ITER-0104/TECH_PLAN.md`
- `.ai/iterations/ITER-0104/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0104/CHANGELOG.md`
- `.ai/iterations/ITER-0104/evidence/`
