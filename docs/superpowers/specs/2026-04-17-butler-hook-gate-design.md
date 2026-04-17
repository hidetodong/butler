---
title: Butler Hook-based 硬门控（Phase 1）设计
audience: AI / 开发者
scope: 通过 Claude Code PreToolUse hook，在目标项目里机械化拦截违反 butler 流程的写操作
status: draft（待用户审阅）
date: 2026-04-17
phase: Phase 1 of Butler Harness 升级 Roadmap
---

# Butler Hook-based 硬门控（Phase 1）

## 0. 背景与定位

Butler 目前是 **prompt-based rule system**：所有流程约束（P1→P5 产物链、mcv-update 协议、Ralph Loop 熔断等）都靠写在 Markdown 里的"必须/不得"措辞由 AI 自觉遵守，缺乏机制化执行与可观测反馈。

相对于成熟的 harness engineering，Butler 在机制层、反馈层、上下文层各存在缺口。本 spec 只覆盖 **机制层中优先级最高的一块**：通过 Claude Code 的 hook 机制，把若干"最不该被违反"的流程规则从"AI 自觉"升级为"工具层拦截"。

本 phase 是 8 phase roadmap 的第一站，后续 phase（工具亲和力矩阵 / 阶段化 context 加载 / 失败模式目录 / SESSION_HANDOFF 结构化 / 沙盒 / 遥测 / 规则自测 fixture）不在本 spec 范围内，但本 spec 的组件结构为它们预留扩展点。

## 1. 目标与非目标

### In scope

1. 在 **使用 butler 的目标项目**（`/mcv-deploy` 部署后的应用项目）里，通过 PreToolUse hook 机械拦截以下三类违规：
   - **(a) 跳过 P1/P2 直接写源码**：对非 `.ai/` / `deliveries/` / `.claude/` / `.git/` / `node_modules/` / `.vscode/` / `.idea/` 的路径发起 `Edit` / `Write` / `MultiEdit`，但 `.ai/CONCEPT.md`、`.ai/AC_LIST.md`、`.ai/TECH_PLAN.md` 任一缺失或为空。
   - **(c) 未经 mcv-update 协议修改业务扩展**：对 `99_Business_Extension/**` 发起写操作。
   - **(e-简化版) 产物链断裂的存在性校验**：`.ai/TECH_PLAN.md` 必须存在（随 (a) 一起判），内容级 AC-ID 引用对齐不在本 phase。
2. hook 脚本与配置作为 **`templates/hooks/`** 加入 butler 仓库，由 `mcv-deployment.md` 协议在部署时拷贝到目标项目 `.claude/hooks/`，并把 PreToolUse 配置合并进目标 `.claude/settings.json`。
3. 违规行为默认硬拦截（exit 2），支持 `BUTLER_BYPASS=1` 环境变量 + `.ai/bypass-reason.md`（必须非空）做显式逃生；每次成功 bypass 追加到 `.ai/RUN_LOG.md`。
4. hook 自身崩溃时 **fail-closed**（拦截），通过 bypass 通道兜底逃生。
5. 提供三层测试：规则模块单测、dispatcher 集成测试、端到端 smoke 脚本。

### Out of scope

- **butler 仓库自身 dogfood**（hooks 不在 butler 仓库内生效）——留给后续增量；butler 非应用项目、无 `.ai/` 结构，规则 (a)(c) 不成立。
- **Bash 子集拦截**（`cat >`、`sed -i`、`tee`、重定向等）——现实中 AI 95%+ 通过 Edit/Write 改源文件，Bash 绕过是边缘路径；正则维护成本 / 误伤显著。
- **`.ai/` 下的 schema 级保护**（结构性改动需走 mcv-update）——本 phase 只拦 `99_Business_Extension/`，`.ai/` 下的正常阶段产物写入不拦，避免与 P1-P5 常规流程冲突；schema 保护留给后续 phase 与 mcv-update 协议联动。
- **内容级 AC-ID 引用对齐** (规则 (e) 完整版)——需要文本 parser、AC-ID 正则、容错、阈值，且触碰 `acceptance-schema.md` / `tech-plan-schema.md`；作为独立 sub-project（工作名 "AC-ID linkage linter"）后置。
- **butler-upgrade 协议对 hook 版本同步**——目标项目拿到的是拷贝副本，butler 升级 hooks 时需要检测并更新目标项目——作为本 phase 的 follow-up 任务，不阻塞首次部署路径。
- **Windows 支持**。部署目标限定 macOS / Linux；路径处理用 `pathlib.PurePosixPath`。
- **性能 / 模糊 / 安全测试**——hook 接受的是本地 Claude Code harness 的可信 JSON，每次调用期望 <100ms（Python 冷启动 ~30ms），不值得 benchmark。

## 2. 关键设计决策

| 编号 | 决策 | 选中值 | 理由摘要 |
|---|---|---|---|
| D1 | 生效范围 | 仅目标项目（α） | 受众清晰、mcv-deployment 已有分发通道；butler 自身 dogfood 后置 |
| D2 | 违规时行为 | 硬拦截 + 显式逃生（c） | 堵 95% 偷懒违规，保留人类 agency，绕过有心理成本与留痕 |
| D3 | bypass 最低成本 | 必须存在非空 `.ai/bypass-reason.md`（ii） | 写一行字是恰到好处的摩擦；AI 自动 bypass 会留下可在 review 中质询的证据 |
| D4 | 拦截工具覆盖 | 仅 `Edit` / `Write` / `MultiEdit`（a） | Bash 绕过场景边缘，正则维护贵、误伤多 |
| D5 | (a) 源文件边界 | 黑名单：除 `.ai/` / `deliveries/` / `.claude/` / `.git/` / `node_modules/` / `.vscode/` / `.idea/` 外全拦（i） | 白名单漏报风险大；配置化延后到 Phase 3 一起做 |
| D6 | (e) 处理粒度 | 存在性降级（Ⅰ） | 内容解析成本高、误伤多；内容版作为独立 sub-project 后置 |
| D7 | 实现形态 | 模块化 Python + 规则注册表（Approach 2） | 与后续 phase 扩展点契合；stdlib 足够、无外部依赖 |
| D8 | (c) 覆盖面 | 仅 `99_Business_Extension/**` | `.ai/` 下正常阶段产物写入必须放行，避免自锁 |
| D9 | hook 崩溃策略 | fail-closed（exit 2） | 宁可烦也不要假阴；bypass 通道兜底 |

## 3. 架构

### 3.1 目录布局

**SSOT（butler 仓库）：**

```txt
butler/
  templates/
    hooks/                           # ← 单一事实源
      butler_gate.py                 # PreToolUse dispatcher
      rules/
        __init__.py
        phase_gate.py                # (a)+(e-简化)：P1/P2/P3 产物存在性
        protected_paths.py           # (c)：99_Business_Extension/ 保护
        artifact_chain.py            # 本 phase 留空占位，后续填充
      lib/
        __init__.py
        bypass.py                    # BUTLER_BYPASS + reason 校验 + RUN_LOG 写入
        io.py                        # stdin JSON 解析、路径归一化、黑名单常量
      tests/
        conftest.py                  # tmp_project fixture（复制 fixtures 到 tmp_path）
        test_rules.py                # Tier 1：规则模块单测
        test_integration.py          # Tier 2：dispatcher 集成测试
        smoke.sh                     # Tier 3：端到端手工脚本
        fixtures/
          empty-project/
          p1-done/
          p1p2-done/
          full-artifacts/
          with-bypass-reason/
      README.md                      # 给贡献者看的使用与测试说明
    settings.hooks-snippet.json      # PreToolUse 配置片段，部署时合并
```

**部署目标项目（mcv-deployment 产物）：**

```txt
<target>/
  .claude/
    hooks/                           # ← 从 butler/templates/hooks/ 拷贝（不含 tests/）
      butler_gate.py
      rules/...
      lib/...
      README.md
    settings.json                    # ← 已合并 PreToolUse 配置
  .ai/
    CONCEPT.md / AC_LIST.md / TECH_PLAN.md / VERIFY_REPORT.md
    RUN_LOG.md                       # ← 首次 bypass 时按需产生
    bypass-reason.md                 # ← 需要 bypass 时由用户/AI 填写
```

### 3.2 关键架构原则

- **SSOT 在 butler，目标项目拿拷贝**（不软链）：跨仓库软链脆弱，拷贝更符合 Butler 现有交付哲学。
- **所有运行态文件按需产生**：`RUN_LOG.md` / `bypass-reason.md` 均首次 bypass 时创建，不预置。
- **`settings.hooks-snippet.json` 提供可幂等合并的片段**：mcv-deployment 与（未来）butler-upgrade 可据此合并进目标 `settings.json`，无需手写 JSON。
- **规则模块只读 FS，不写**：写日志是 `lib/bypass.py` 专责，避免规则副作用。

## 4. 组件职责

### 4.1 dispatcher: `butler_gate.py`

**入口 entry point**，stdin 读 Claude Code PreToolUse JSON。

职责：

1. `io.parse_stdin()` → 标准化 `Context`（`cwd`, `tool_name`, `target_path`, `edit_payload`）。
2. 若 `tool_name ∉ {Edit, Write, MultiEdit}` → `exit 0`（放行）。
3. 顺序执行规则模块（`protected_paths` → `phase_gate` → `artifact_chain`），每条独立判定 `Decision`。
4. 任一 deny → 进入 `lib/bypass.py`：
   - bypass 通过 → 追加 RUN_LOG → `exit 0`
   - bypass 不通过 → `exit 2` + stderr 给 AI 可读的违规摘要
5. 所有 allow → `exit 0`。
6. 顶层 `try/except`：任何异常 → `exit 2` + stderr `butler-gate internal error: <excerpt>`（fail-closed）。

### 4.2 规则模块（统一接口）

**接口契约**：

```python
def evaluate(ctx: Context) -> Decision:
    ...

@dataclass
class Decision:
    verdict: Literal["allow", "deny"]
    rule_id: str
    reason: str         # 给 AI / 人看的原因
    remediation: str    # 可操作的下一步
```

**`phase_gate.py`**（rule_id = `phase_gate`）：
- 若 `ctx.target_path` 在黑名单内 → `allow`
- 否则逐一校验 `.ai/CONCEPT.md`、`.ai/AC_LIST.md`、`.ai/TECH_PLAN.md` 存在且非空（`stat.st_size > 0` 且 strip 后非空）
- 任一缺失 → `deny`，`reason` 明确指出缺哪个文件，`remediation` 指向对应阶段的产出动作

**`protected_paths.py`**（rule_id = `protected_paths`）：
- 若 `ctx.target_path` 命中 `99_Business_Extension/**` 前缀 → `deny`
- `reason` = "业务扩展目录禁止直接写操作"；`remediation` = "走 mcv-update 协议或显式 bypass"

**`artifact_chain.py`**（rule_id = `artifact_chain`）：
- 本 phase 占位，永远返回 `allow`
- 保留 import 位置，后续 phase 加入 AC-ID linkage linter 等规则时不动 dispatcher

### 4.3 lib

**`bypass.py`**：

```python
def evaluate_bypass(ctx: Context, decision: Decision) -> Decision:
    """对 deny 的 Decision 做 bypass 判定。通过则写 RUN_LOG 并返回 allow；否则原样返回 deny。"""
```

流程：

1. 读 `BUTLER_BYPASS` 环境变量，若非 `"1"` → 返回原 decision
2. 读 `<cwd>/.ai/bypass-reason.md`；不存在或 strip 后为空 → 返回原 decision，`reason` 追加"bypass 失败：需先在 `.ai/bypass-reason.md` 写明理由"
3. 追加一行到 `<cwd>/.ai/RUN_LOG.md`（首次时创建父目录 + 文件）：
   ```
   <ISO-UTC> | <rule_id> | <tool_name> | <relative_target> | <reason_first_line>
   ```
4. 返回 `Decision(verdict="allow", ...)`（保留原 rule_id，便于审计）

**`bypass-reason.md` 生命周期**：文件**不自动清理**；只要 `BUTLER_BYPASS=1` 仍然设置，同一 reason 可覆盖同一会话内的多次违规，每次都会追加 RUN_LOG。这是一个有意的权衡：

- **好处**：用户/AI 写一次理由可连续处理；低摩擦
- **代价**：RUN_LOG 可能出现多条相同 reason 的记录

若要求"每次 bypass 必须重写 reason"，实施成本增加但审计信号更强；本 phase 选择低摩擦方案，后续若遥测数据显示 bypass 被滥用，再收紧。

**`io.py`**：

- `parse_stdin() -> dict`：读 stdin JSON；异常让 dispatcher 顶层 catch
- `resolve_target(tool_input) -> Path`：对 `Edit` / `Write` / `MultiEdit` 均取 `file_path`，归一化为相对 `cwd` 的 `PurePosixPath`；超出 cwd（以 `..` 开头）→ 返回特殊标记路径 `OUT_OF_CWD`，由规则模块视作 gated（保守拦截）
- `is_gated(path, blacklist) -> bool`：前缀匹配（归一化后）
- 黑名单常量：
  ```python
  GATED_BLACKLIST = frozenset({
      ".ai/", "deliveries/", ".claude/", ".git/",
      "node_modules/", ".vscode/", ".idea/"
  })
  ```

### 4.4 配置片段：`settings.hooks-snippet.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          { "type": "command", "command": "python3 .claude/hooks/butler_gate.py" }
        ]
      }
    ]
  }
}
```

mcv-deployment 负责**幂等合并**进目标 `settings.json`：若已存在同 matcher 项，不重复插入；若 `hooks.PreToolUse` 不存在则新建。

## 5. 数据流

```
Claude Code (AI)
   │ 1. Edit(file_path="src/auth.ts", ...)
   ▼
Claude Code harness
   │ 2. PreToolUse 匹配 "Edit|Write|MultiEdit"，stdin 注入 JSON
   │    { "tool_name": "Edit",
   │      "tool_input": { "file_path": "src/auth.ts", ... },
   │      "cwd": "/abs/project/root", ... }
   ▼
butler_gate.py
   │ 3. io.parse_stdin() → ctx
   │ 4. io.resolve_target() → Path("src/auth.ts")
   │ 5. tool_name ∈ {Edit,Write,MultiEdit}? 否 → exit 0
   │
   │ 6. rules 顺序执行（protected_paths → phase_gate → artifact_chain）
   │
   ├─ 全部 allow ──► exit 0
   │
   └─ 任一 deny ──► lib.bypass.evaluate_bypass()
                      │
                      ├─ BUTLER_BYPASS != "1" ──► exit 2 + stderr 违规摘要
                      ├─ bypass-reason.md 缺失/空 ──► exit 2 + stderr "需先写 reason"
                      └─ bypass OK ──► 追加 RUN_LOG ──► exit 0

顶层 try/except：任何异常 → exit 2 + stderr "internal error" (fail-closed)
```

### 输入 / 输出契约

| 通道 | 方向 | 内容 |
|---|---|---|
| stdin | in | Claude Code PreToolUse JSON payload |
| stdout | out | 空（本 phase 不使用；预留给未来向 AI 注入 context） |
| stderr | out | 违规时给 AI 的可读摘要 |
| exit code | out | `0`=allow，`2`=deny，其它=fail-closed 等同 deny |
| 文件 `.ai/RUN_LOG.md` | append | 每次成功 bypass 追加一行 |

### stderr 约定格式

```
❌ butler-gate denied: <rule_id>
  tool: <Edit|Write|MultiEdit>
  target: <relative path>
  reason: <规则模块给出的原因>
  remediation: <可操作的下一步>
  bypass: 若坚持绕过，设 BUTLER_BYPASS=1 并在 .ai/bypass-reason.md 写明理由
```

AI 读到即可自解释下一步（hook 作为"教练"而非"门卫"）。

### RUN_LOG 行格式

```
2026-04-17T10:32:11Z | phase_gate | Edit | src/auth.ts | hotfix for prod 500
```

- UTC ISO-8601，管道分隔，单行
- reason 字段只取 `bypass-reason.md` 第一行（strip 后）；完整 reason 保留在 `bypass-reason.md` 供复盘

## 6. 错误处理与边界场景

### 6.1 预料内 deny 路径

| 场景 | 判定 | 行为 |
|---|---|---|
| 源码路径 Edit，三产物齐全 | allow | exit 0 |
| 源码路径 Edit，缺 `CONCEPT.md` | phase_gate deny | exit 2，stderr 指明缺失文件 + P1 提示 |
| Edit `.ai/CONCEPT.md`（P1 阶段） | allow（黑名单内） | exit 0 |
| Edit `99_Business_Extension/policy.md` | protected_paths deny | exit 2，remediation 指向 mcv-update / bypass |
| `BUTLER_BYPASS=1` + reason 非空 | allow | 追加 RUN_LOG，exit 0 |
| `BUTLER_BYPASS=1` 但 reason 缺失 / 空 | deny | exit 2，提示写 reason |

### 6.2 边界场景

1. **首次部署后第一次 Edit**：`.ai/CONCEPT.md` 不存在时，AI 的第一次 Edit 本身是对 `.ai/CONCEPT.md` 的 Write → 目标在黑名单 → phase_gate 放行。**不会自锁**。
2. **Write 在项目根创建新源文件**（如 `Write("new_feature.ts")`）：非黑名单 → phase_gate 检查产物 → 缺则 deny。符合预期。
3. **路径含 `~`、绝对路径、`../`**：`io.resolve_target` 归一化为相对 cwd；超出 cwd → `OUT_OF_CWD` 标记 → 视作 gated（保守拦）。
4. **MultiEdit**：Claude Code 当前 payload 是单 `file_path` + 多 `edits[]`，等同 Edit；若未来改为多路径，`resolve_target` 需返回 list，dispatcher 逐个判定，任一 deny 整体 deny。
5. **symlink**：`Path.resolve()` 后再判定前缀；指向 gated 区间拦。
6. **`deliveries/` 内 Edit**：黑名单内放行。deliveries 是交付归档，写入不触发流程违规。
7. **非 Claude Code 环境手工调用**：stdin 无合法 JSON → 顶层 catch → exit 2。无害。
8. **Windows 路径分隔符**：本 phase 不支持。

### 6.3 Claude Code 版本兼容

- `io.parse_stdin` 只读 `tool_name`、`tool_input.file_path`、`cwd` 三字段，其它忽略，对新增字段健壮。
- 未来字段重命名 → `io.py` 一处兼容多版本，dispatcher 与规则模块不动。
- `README.md` 记录已测试的 Claude Code 版本号。

### 6.4 并发 / 重入

Claude Code 串行调用工具 → PreToolUse 同一时刻至多一实例 → RUN_LOG 追加无需锁。短行 `open(..., 'a')` POSIX 原子写入足够。

### 6.5 Fail-closed 的代价与兜底

一个规则模块 bug 可能把用户锁死（所有 Edit/Write 都 deny）。缓解：

- **bypass 通道始终可用**：AI 或人类写 `.ai/bypass-reason.md` 即可应急。
- **`templates/hooks/README.md` 显著位置**记录"遇到 internal error 的应急流程"。
- **规则模块"禁止 raise"作为最佳实践**（降级为规范而非护栏），但 dispatcher 顶层 catch 兜底。

## 7. 测试策略

### Tier 1 — 规则模块单元测试（`test_rules.py`）

- 纯函数，`pytest` 表驱动
- 覆盖矩阵：每条规则 × {满足/不满足} × {黑名单内/外} × {文件存在/为空/不存在}
- 目标：每条规则 ≥ 6 个用例

### Tier 2 — dispatcher + lib 集成测试（`test_integration.py`）

用 `subprocess.run(["python3", "butler_gate.py"], stdin=..., env=...)` 真实 fork：

- 正常 allow：合法 stdin + 产物齐全 → exit 0
- phase_gate deny 无 bypass → exit 2 + stderr 含 `phase_gate`
- bypass 成功：deny + `BUTLER_BYPASS=1` + reason 非空 → exit 0 + RUN_LOG 追加一行
- bypass 失败：`BUTLER_BYPASS=1` 但 reason 缺失 → exit 2 + stderr 含"需先写 reason"
- hook 崩溃：畸形 stdin → exit 2（fail-closed 验证）

### Tier 3 — 端到端 smoke（`smoke.sh`，手工）

- 起 tmp 项目目录，模拟 mcv-deployment 装 hooks
- 用真实 Claude Code 调一次 Edit，观察拦截
- 文档化为"每次改 hook 后本地跑一遍"的最小仪式；不强制 CI（Phase 8 纳入自动化）

### Fixture 目录

```
templates/hooks/tests/fixtures/
  empty-project/         # .ai/ 空
  p1-done/               # 只有 CONCEPT.md
  p1p2-done/             # + AC_LIST.md
  full-artifacts/        # 三产物齐全
  with-bypass-reason/    # 带 .ai/bypass-reason.md
```

目录命名用语义而非序号，为 Phase 8（规则自测 fixture 扩展为跨 phase 回归场景）预留扩展空间。

### 贡献者本地测试仪式

改 hook 后执行：

```bash
cd templates/hooks && python3 -m pytest tests/
```

写进 `templates/hooks/README.md` 作为贡献者义务。

## 8. 对外集成点

### 8.1 `Coder/20_Workflow_Lifecycle/mcv-deployment.md`

需要新增步骤（mcv-deployment.md 的 "5. Hook 注入" 或合适章节）：

1. 将 `$BUTLER/templates/hooks/` 除 `tests/` 外的内容拷贝到 `<target>/.claude/hooks/`。
2. 读 `$BUTLER/templates/settings.hooks-snippet.json`，与目标 `<target>/.claude/settings.json` 幂等合并：
   - 若 `settings.json` 不存在 → 用 snippet 直接写入
   - 若存在但无 `hooks.PreToolUse` → 合并
   - 若存在且已有 matcher 等于 `"Edit|Write|MultiEdit"` 的 PreToolUse 条目 → 不重复插入

spec 更新交给实施计划处理，本 spec 只规定**接口契约**：snippet 的 key 路径是 `hooks.PreToolUse[*].matcher`，合并策略按 matcher 字面去重。

### 8.2 `Coder/20_Workflow_Lifecycle/butler-upgrade.md`（follow-up）

目标项目的 `.claude/hooks/` 是 butler 仓库的拷贝副本，butler 升级 hooks 时需要同步。本 phase 的 follow-up 任务：

- 在 hooks 目录添加版本标识（如 `VERSION` 文件或 `butler_gate.py` 顶部注释）
- butler-upgrade 协议检测版本差异 → 提示用户是否覆盖

不阻塞本 phase 首次部署路径。

### 8.3 对后续 phase 的扩展点

- **Phase 2（工具亲和力矩阵）**：新增 rule module（如 `tool_affinity.py`）即可，dispatcher 自动分发
- **Phase 4（失败模式目录）**：新增 rule module 或在 `lib/bypass.py` 增强升级到人的触发
- **Phase 7（遥测）**：`RUN_LOG.md` 已是种子，后续扩展记录更多维度
- **Phase 8（规则自测 fixture）**：本 phase 的 `tests/fixtures/` 目录结构与命名已为其预留

## 9. Follow-up 任务（不阻塞本 phase）

1. **butler-upgrade 对 hooks 的版本同步**（8.2）
2. **AC-ID linkage linter**（内容级 (e) 规则，作为独立 sub-project）
3. **Bash 子集拦截**（与 Phase H "沙盒 & 可逆性" 合并）
4. **`.ai/` schema 级保护**（与 mcv-update 协议联动）
5. **butler 仓库自身 dogfood hooks**（增量）
6. **Windows 支持**（若受众需要）

## 10. 交付物清单（本 phase 实施时应产出）

- `templates/hooks/butler_gate.py`
- `templates/hooks/rules/{__init__,phase_gate,protected_paths,artifact_chain}.py`
- `templates/hooks/lib/{__init__,bypass,io}.py`
- `templates/hooks/tests/{conftest,test_rules,test_integration}.py`
- `templates/hooks/tests/smoke.sh`
- `templates/hooks/tests/fixtures/{empty-project,p1-done,p1p2-done,full-artifacts,with-bypass-reason}/`
- `templates/hooks/README.md`
- `templates/settings.hooks-snippet.json`
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md` 更新（新增 hook 注入步骤）
- `Coder/README.md` 更新（`templates/hooks/` 在目录结构表中登记）
- 通过 `cd templates/hooks && python3 -m pytest tests/` 全绿
