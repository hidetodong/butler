# Goal

- 修复 Bucket E（平台与回退健壮性）2 条 Should Fix。

# In Scope

- E-1: `scripts/setup.sh` 的 `sed -i` 跨平台兼容（macOS/BSD 与 Linux 都能正确工作）。
- E-2: `Coder/00_System_Prompt/logic-protocol.md § 4.2` 参考资料注入表，补充 skill 不可用时的 fallback 规则。

# Out of Scope

- Bucket B / C / D（其余 5 条 Should Fix）。
- 不重构 setup.sh 整体逻辑，仅改 sed 调用。
- 不修改 `.ai/references/` 存储路径或命名约定。

# Acceptance Checklist

- [ ] **E-1** `scripts/setup.sh` 在 macOS 与 Linux 下 `sed -i` 调用均能成功（不报 `extra characters at end of command` 或 `unknown option` 类错误）
- [ ] **E-2** `logic-protocol.md § 4.2` 明确定义当 `confluence-api-extractor` / `mastergo-codegen` 等 skill 不可用时的 fallback 路径，方案待拍板

# Verification Method

- **E-1**：
  - 阅读 setup.sh 修复后的 sed 段，确认包含平台检测分支或等价兼容写法；
  - `bash -n scripts/setup.sh` 通过语法检查；
  - 在 macOS 下执行 dry-run（或 trace）确认既有路径未变；Linux 真机验证受限（本地无环境），仅做代码评审。
- **E-2**：
  - `logic-protocol.md § 4.2` 在表格下方或作为新段落包含"fallback / 回退"关键字；
  - fallback 规则明确三种 skill 失效场景（skill 未安装 / 认证失败 / 超时）的处理；
  - 最终产物落盘路径与现有 `.ai/references/` 约定一致，不变更命名前缀（`api-` / `design-` / `insight-` / 无前缀）。

# Open Questions / Risks

## ❓ 待拍板 - E-2 方案选择

**问题**：`logic-protocol.md` 定义了 Confluence / MasterGo 等参考资料通过专用 skill 提取。但：
- 不是所有 AI 环境都装了 `confluence-api-extractor` 或 `mastergo-codegen` skill
- skill 可能因认证失败、网络超时等运行时原因返回错误
- 当前规则对此没有明确的回退路径，AI 可能直接卡住或擅自跳过参考资料

### 方案 α — 降级链：先 skill → 失败时 AI 用通用工具 → 都失败时问用户

- 第 1 层：优先调用对应 skill。
- 第 2 层：skill 不可用或失败时，AI 用通用工具（WebFetch 读取公开链接、Read 读取本地文件）自行提取结构化信息。
- 第 3 层：通用工具也失败时（比如需要认证、格式复杂），提示用户手动提供文本并粘贴到对话。
- AI 无论走哪条路径，产物必须落盘到 `.ai/references/`，命名和元信息（source URL、处理方式）保留，供后续审计。

### 方案 β（推荐）— 降级链：先 skill → 失败时问用户

- 第 1 层：优先调用对应 skill。
- 第 2 层：skill 不可用或失败时，**不越权用 WebFetch/网络请求**，直接提示用户手动提取后粘贴（"请把 XX 页面的内容贴给我"）。
- AI 只落盘用户提供的文本，不自作主张访问外部资源。
- **理由**：AI 主动网络请求可能越过权限边界，尤其在企业环境下（Confluence 多带鉴权）。交由用户提供避免权限/安全风险。

### 方案 γ — 硬失败

- skill 不可用时报错并暂停任务，要求用户先安装 skill。
- **缺点**：对轻量场景过苛（用户可能只是想临时引用一次）；不推荐。

---

## 风险

- 改动均为规则文本 + shell 脚本兼容，无运行时行为变更。
- setup.sh 的 Linux 验证受限（本地无 Linux 环境），只能靠代码评审。生产中第一个 Linux 用户会实测到。

---

# 请回复

1. **E-2 方案选择**：α / β / γ

E-1 无设计取舍，按 `bash if/else + $OSTYPE` 方案直接实施。回复方案选择后我进入 P3。
