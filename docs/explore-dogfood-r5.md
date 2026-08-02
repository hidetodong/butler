# MILE-0014 R5 · Butler Explore dogfood

> 日期：2026-08-02
> 样本：`.ai/milestone-backlog/codex-structured-question-cards.md`
> live Map：`DMAP-0001`
> 结论口径：只报告本地单仓观测，不外推多人、跨机器或所有宿主体验。

## 场景与边界

本次把“结构化提问卡片”候办当作真实探索样本，但没有提升该候办、领取它自己的 Milestone / Iteration 或开始实现卡片。live Map 包含三个 Decision：卡片适用边界、三宿主可诚实承诺的能力、建设自定义 UI / 外部协调层所需证据；另保留一个 Fog，表示真实跨宿主节时与纠错率尚未取得。

Router 侧仍只有既有 `ideation` workflow。显式 Explore / 探索 / Decision Map / 跨会话决策 / Wayfinder 语料进入它；普通明确任务继续走 Standard，Standard 后验建议必须给具体 blocker、零写并等待同意。

## 观测一：跨会话恢复成本

### 口径

- 新进程不读取原始对话或本迭代 CONCEPT，只读取 Decision Map / Work 持久状态。
- 以“恢复命令数、读取对象、能否得到 destination / Frontier / Attempt relation / next action”计数，不用主观回忆时间。

### 原始观测

- `tools/explore-dogfood/scenario.py --inspect-project-root . --map-id DMAP-0001` 用一条命令聚合两个 Module 的只读 inspect。
- transcript reads = 0；读取 1 个 Map state、2 个 Task、2 个 Result。
- 恢复出三个 Decision 均 resolved、两个 Attempt 均 absorbed、Frontier 为空；下一动作是处理开放 Fog，promotion 仍为可选显式动作。
- 对应 evidence ID：`explore-dogfood-live-r2`、`explore-dogfood-harness-r2`。

### 结论

本地跨会话恢复成立，且不需要回放对话。单命令可以恢复“为什么探索、当前到哪、下一步是什么”；Map / Work 仍各守自己的写真源，聚合视图不落缓存。

### 局限

这里只证明同一文件系统和当前 schema 的恢复；没有测跨机器同步、多人同时解释同一 Map，也没有测长期积累数百张 Map 后的发现成本。

## 观测二：错误路线与误写

### 口径

- Router 代表 corpus 中每个例子必须给唯一预期 status / workflow，Router 决策阶段 `expected_state_writes=false`。
- live promotion 对已绑定 R5 的请求必须确定性拒绝，且拒绝前后语义树 hash 不变。
- Result 落盘不得自动 resolve；候办台账与最大 ITER/MILE 号不得因 dogfood 改变。

### 原始观测

- Router corpus 共 24 个代表例，包含六个核心快路径：明确小修复、独立 Iteration、直接 Milestone、轻量 Ideation、显式持久化 Explore、无具体 blocker 的模糊请求。测试对六例另做不读取预期结果的 literal-trigger 下界核对；13 项 registry 测试通过，workflow 数仍为 13，没有 `explore` ID。
- live `route-reference` 指向 `MILE-0014 / R5` 返回 `route_unavailable`、exit 1，`zero_semantic_writes=true`；没有 live promotion receipt。
- 两个 Research Result record 后 Map revision 未变化，只有协调器显式 absorb 后对应 Decision 才 resolved。
- `codex-structured-question-cards` 仍为 `deferred`，MILE-0014 仍只绑定 ITER-0102～ITER-0106。
- 对应 evidence ID：`router-contract-r2`、`explore-dogfood-live-r2`。

### 结论

已覆盖的显式场景没有出现第二入口、自动升级或部分写入；交付路线所有权没有被 dogfood 绕过。Router 与三个 Module 的安全边界按预期工作。

### 局限

代表 corpus 与 literal-trigger 下界不能证明任意自然语言改写都被模型正确理解，也不能统计生产用户的真实误路由率。这里证明的是显式标记与合同样本，不是一个通用语义分类器；任意改写仍由模型按共同 Router 合同理解。

## 观测三：Research 并行效果

### 口径

- 两个无依赖 Decision 必须可组成同一 Research batch、分别 claim 和 record。
- 报告 requested / actual execution mode、fresh-context 与是否出现丢更新；不以合成 sleep 或单次墙钟时间证明收益。

### 原始观测

- harness 与 live 均形成 `max_parallel=2` 的 Research batch，两个结果都可独立 absorb，后一个 absorb 未被前一个 Map revision 污染。
- requested mode = `parallel`；actual modes = `serial, serial`；fresh_context = `false, false`。
- record changed Map = false；显式 absorb 后 Map / Work verify 均为 `ok`。
- 对应 evidence ID：`explore-dogfood-harness-r2`、`explore-dogfood-live-r2`、`decision-modules-regression-r2`。

### 结论

结构上的可并行性和单写吸收已证明，但本轮没有观察到实际并行节时收益。当前宿主权限下的真实结论是“可安全降级为串行”，不是“并行已经提速”。

### 局限

没有创建 fresh-context 子 agent，也没有跨宿主测量 Research 耗时；未来只有在真实并行会话中才能补充吞吐结论。

## 观测四：Map 维护开销

### 口径

- 记录 coordinator apply 次数、持久 JSON 数量、开放状态与恢复命令数。
- 把业务选择动作和工具内部实现分开；不把自动测试速度当作用户维护成本。

### 原始观测

- 隔离 harness：14 次 coordinator apply、6 个持久 JSON（含 promotion receipt）、1 个开放 Fog、1 条恢复命令。
- live：15 次成功 apply（10 Map + 5 Work）、5 个持久 JSON、1 个开放 Fog、无 promotion receipt、1 条恢复命令。
- 首次 live record 因调用方漏写 `sha256:` 前缀被 `invalid_digest` 拒绝；harness 用相同坏输入重现了 fail-closed 与零写，再以标准库 SHA-256 计算正确 digest 继续。这暴露了人工编排 JSON 的实际摩擦，但未造成部分 Result。
- 对应 evidence ID：`explore-dogfood-harness-r2`、`explore-dogfood-live-r2`。

### 结论

本地状态量很小且恢复直接，但 15 次显式 apply 对一次三决策探索并不轻。现阶段这套能力适合跨会话、确有阻塞 Decision 的大需求，不应成为普通任务或轻量 Ideation 的默认路径。

### 局限

一次三决策样本无法给出长期增长曲线；`applied_operations` 与 sidecar 随使用累积，压缩、搜索和批量归档仍需未来规模证据。

## 外部 tracker 裁决

最终裁决: `defer`

- 未观察到跨机器、多人写入、查询/通知或长期规模对本次本地 dogfood 构成实际阻塞，因此不支持现在建设外部 tracker。
- 单机恢复与状态核验已经成立，但 Research 没有实际并行，维护动作也不算轻；这说明下一步应先积累真实使用数据，而不是把状态搬到更重的平台。
- 当出现至少一项可复现阻塞——跨机器协作无法安全交接、多人写入需要身份/仲裁、Map 数量使本地扫描失效、或查询/通知成为持续人工负担——再重开 `go` 评估。

## MILE-0014 收口判断

R5 实现、专项测试、完整 CI 与 P5 evidence 全部通过后，MILE-0014 可按 R1–R5 均 closed 的规则另行收口。开放 `FOG-0001` 是未来真实使用数据，不拥有交付生命周期，也不阻塞本里程碑；Decision Map 保留为参考来源。
