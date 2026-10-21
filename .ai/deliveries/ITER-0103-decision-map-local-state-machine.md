# Decision Map 本地合同与确定性状态机

## 本次交付目标

把 Wayfinder 式依赖图、Frontier 与并行领取能力落成 Butler 的确定性本地状态 Module，同时避免把关键路由和状态转换交给模型临场判断。

## 已完成内容

- 新增驻留工具 `tools/decision-map/`，对外只提供 `inspect`、`plan`、`apply`、`verify` 四个动作。
- 为每张 Decision Map 建立单一原子状态、依赖 DAG、派生 Frontier、Fog graduation 和 Claim Lease 合同。
- 用 revision、state digest、operation receipt、文件锁和原子替换保证并发、幂等与故障恢复。
- 将结构化 Explore 状态接入现有 Ideation 文档和部署矩阵，同时保持 R1 的单入口、opt-in 与显式 promotion 边界。
- 新增 18 项 Decision Map 专项测试，并接入完整 CI。

## 关键变更 / 用户可感知变化

- 用户选择深入 Explore 后，可以把结构化 Decision Map 跨会话保存，并让多个 worker 在互不依赖的 Frontier 上领取决策工作。
- 模型或 helper 只提交 operation spec；状态机负责判断转换是否合法，模型的“清晰度 / 大小 / 置信度”不再决定 Map 生命周期。
- 同时竞争、过期重领、旧 token 提交、重复请求和中途写入故障都有确定性结果，不依赖会话记忆兜底。
- 本轮没有增加第二个用户入口，也没有实现 Milestone / Iteration promotion；交付交接仍遵守 R1 已确认的显式路径。

## 高层影响范围

- 新增 `tools/decision-map/` resident Module、CLI、合同文档和专项测试。
- 更新 Ideation 真源、驻留工具部署说明、Coder / 项目 README、workflow 合同测试与完整 CI。
- 没有新增 workflow registry ID、宿主命令、远端状态后端，也没有改变 Milestone / Iteration 的所有权。

## 验证方式与结果摘要

- Decision Map 专项：18 项测试通过，覆盖状态、存储、CLI、真实双进程竞争与跨进程恢复。
- Workflow 合同：12 项测试通过，确认单一 Ideation 入口、opt-in、零写 suggest 和从 P1 promotion 的边界不变。
- P5 同上下文风险复核：Must Fix 0、Should Fix 0；复核发现的三项防御性细节均已修正并重新验证。
- 完整 `scripts/verify-ci.sh` 在 Python 3.12.12 / uv 0.9.28 下 exit 0；四份 evidence 已归档并通过 archive verifier。

## 已知剩余风险 / 延后事项

- `applied_operations` receipt 会随单张 Map 的操作数增长；R2 不做需要迁移的压缩。
- 本轮只保证 Butler 当前 macOS / Linux 本地文件系统；跨主机和网络文件系统协调不在范围内。
- Claim token 是协调凭据，不是权限认证边界。
- R3 research helper 与 R4 promotion 仍为 planned，必须由用户显式启动，不会自动进入下一迭代。

## 引用

- `.ai/iterations/ITER-0103/CONCEPT.md`
- `.ai/iterations/ITER-0103/AC_LIST.md`
- `.ai/iterations/ITER-0103/TECH_PLAN.md`
- `.ai/iterations/ITER-0103/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0103/CHANGELOG.md`
- `.ai/iterations/ITER-0103/evidence/`
