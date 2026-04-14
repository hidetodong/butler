# Coder

`Coder/` 是 butler 体系中的工程开发与 AI 协作子系统入口。

它承载当前这套通用规则体系，用于沉淀：

- 系统提示
- 工程规范
- 验收导向流程
- 质量门禁
- 上下文治理
- 业务扩展插槽

当其他应用或文件需要直接引用开发协作子系统时，应以 `Coder/README.md` 作为入口。

## 目录结构

```txt
/Coder
  README.md

  /00_System_Prompt
    identity.md
    logic-protocol.md

  /10_Engineering_Standard
    vue3-standard.md
    typescript-rules.md
    build-tooling.md

  /20_Workflow_Lifecycle
    lifecycle.md
    acceptance-schema.md
    progressive-handoff.md
    mcv-deployment.md
    maintenance-boundaries.md

  /30_Quality_Gate
    linting.md
    testing-strategy.md

  /40_Context_Management
    state-tracking.md
    checkpoint.md
    mode-switch.md
    handoff-spec.md

  /99_Business_Extension
    .gitkeep
```

## 读取顺序

建议 AI 或开发者按以下顺序读取：

1. `00_System_Prompt/identity.md`
2. `00_System_Prompt/logic-protocol.md`
3. `10_Engineering_Standard/`
4. `20_Workflow_Lifecycle/`
5. `30_Quality_Gate/`
6. `40_Context_Management/`（长任务、多阶段任务、上下文压缩前重点读取）
7. `99_Business_Extension/*.md`（如存在）

其中：

- `20_Workflow_Lifecycle/mcv-deployment.md` 负责基地车部署协议。
- `20_Workflow_Lifecycle/maintenance-boundaries.md` 负责维护成本与批处理边界。
- `40_Context_Management/handoff-spec.md` 负责 `SESSION_HANDOFF.md` 的高密度结构约束。

## 使用原则

- 默认按通用工程规范执行。
- 若 `99_Business_Extension/` 下存在业务文档，则将其视为最高优先级业务约束。
- 所有非极小任务默认遵循 `Plan -> Acceptance -> Design -> Execute -> Verify` 流程。
- `20_Workflow_Lifecycle/` 负责流程推进、交付节奏与基地车部署约束。
- `40_Context_Management/` 负责长上下文、状态同步、阶段快照、交接规范与模式切换治理。
- 质量校验必须可验证、可追踪、可回溯到验收项。
