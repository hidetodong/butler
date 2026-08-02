---
title: Decision Work 帮手
audience: AI / 开发者
scope: Explore 中对已显式选择并领取的 Decision 执行一次受控 research / prototype / grilling / task 工作；不拥有 Decision Map 写权
---

# Decision Work 帮手

## 1. 角色

Decision Work 是一份 host-neutral worker 合同，不是新的 workflow、用户入口或四套子 agent。四种 `work_type` 共享同一 Task Packet / Result Envelope 和失败语义；持久化、状态派生与 absorb 的机器真源是 `../../tools/decision-work/README.md`。

它只回答“这次决策工作产出了什么”。它无权回答“Decision 是否已经解决”；后者必须由 Butler 协调器审阅后显式 absorb，并且只能经 Decision Map Module 写入。

## 2. 何时调用

只在用户已经 opt-in Explore、已有结构化 Decision Map，且协调器完成以下机械前置后调用：

1. `inspect` 展示 Frontier；
2. 用户/协调器显式选择 Decision ID，不自动取第一项；
3. 逐项通过 `tools/decision-map/` claim；
4. 通过 `tools/decision-work/` prepare Task Packet。

模型不能按“需求大/不清晰/我没把握”静默创建 Map、选择 Decision 或决定并行度。Decision Work 也不参与 promotion、Milestone 或 Iteration admission。

## 3. 输入

帮手只接收已发布的 `task.json` 内容和一个隔离临时工作目录。允许读取的问题信息仅限 Packet 中的 Decision question、confirmed context、constraints、expected output 与 work-type discriminator。

不得补喂：主会话原始 transcript、明文 Claim token、目标项目写路径、宿主私有推理、未确认偏好或“直接修改项目/Map”的指令。若完成工作必须获取缺失输入，返回 `needs_input`，不能自行猜测。

## 4. 四种模式

| 模式 | 怎么执行 | 不能做什么 |
|---|---|---|
| `research` | 对显式 batch 中互相独立的 Decision 求证；宿主支持时可 fresh-context parallel，否则 serial | 不并行写 Map，不把相似问题擅自合并，不凭搜索结果自动 resolve |
| `prototype` | 在隔离临时目录制作 throwaway artifact，回到协调器/真人处评价 | 没有 `human_evaluation` 不得返回 candidate，不写目标项目 |
| `grilling` | 由协调器主持真实问答，帮手整理问题、真人回答、假设与取舍 | 不得自问自答伪造人的选择，不强制后台化 |
| `task` | 执行解除 Decision 阻塞的窄前置动作并给证据 | 不扩张为最终交付，不声称代码/产品已实现 |

只有 Research 可多项并行；并行的是求证，不是 Map 写入。Prototype、Grilling、Task 一次只处理一个 Attempt，保持 serial/HITL。

## 5. 输出

只返回符合工具合同的一个 Result Envelope：`candidate / needs_input / failed / cancelled`。实际运行模式和是否 fresh context 必须如实回传；宿主不支持并行时写 `serial`，不能冒称 parallel。

- candidate 只是一份可审阅候选，不是决定。
- needs_input 终结当前 Attempt；协调器取得输入后创建绑定 predecessor 的新 Attempt，不改旧 result。
- failed/cancelled 不触发自动 retry、re-claim 或新 Attempt。
- 不输出模型私有推理；rationale 只写可检查的理由与证据。

## 6. 协调器接回

协调器通过 Decision Work `record_result` 保存 Envelope，再用 `inspect` 展示 `timeliness / relation / absorbable`。即使显示 absorbable，也要明确审阅候选：

- 接受：使用当前 Claim owner/token 显式 `absorb_result`；工具会把候选逐字交给 R2 resolve，并追加带 SHA-256 的 sidecar pointer。
- 需要补充：不修改旧结果；准备一个新 Attempt。
- 不接受：不 absorb。若要不同结论，创建新 Attempt，不覆盖历史。
- stale/late/failed/cancelled/needs-input：只能作为参考，不能吸收。

## 7. 权限、隔离与诚实降级

沿用 `overview.md §3` 的诚实与中立定义原则。此帮手对目标项目和 `.ai/` 是零写；所有持久化由协调器调用两个驻留 Module 完成。Research 需要独立求证时优先 fresh-context worker；宿主起不了时允许 serial 降级，但必须记录真实模式。Prototype/Grilling 的真人评价与回答留在主协调会话，不能把“新子 agent”冒充 HITL。

任何坏 Packet、越权要求、无来源 candidate 或无法满足的输入都返回明确失败/needs-input；不能偷偷扩大权限，也不能把未执行描述成已完成。
