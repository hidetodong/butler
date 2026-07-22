---
title: 工作区地图与需求级代码范围契约
audience: AI / 开发者
scope: Monorepo 与单包项目的稳定 workspace key、当前路径映射、共享/生成路径归属、需求级四类读写范围、模块子集、计划与改动门禁、越界扩张及 fail-closed 不变量
---

# workspace-scope-schema（工作区地图与需求级代码范围）

本文件定义项目工作区身份与路径归属、需求允许的读写范围，以及计划、写前 hook 和 git diff 如何消费同一份范围。所有消费者共用确定性解析内核，不能另造范围算法。

## 1. 两层职责

| 层 | 真源 | 回答的问题 |
|---|---|---|
| 项目工作区地图 | `.ai/project/workspaces.md` | `workspace_key` 现在解析到哪个项目内路径 |
| 单需求范围 | `.ai/references/prd/<prd_id>/00_INDEX.md` 的 `Workspace Scope` | 这份需求允许在哪些工作区写、只读或完全排除 |

PRD 不按工作区复制、嵌套或分家。跨三个包的需求仍只有一个 `prd_id`，用范围集合表达影响面。

## 2. 项目工作区地图

`.ai/project/workspaces.md` 是项目当前拓扑的知识主题，遵守 `.ai/project/` 的 current-truth 覆写语义。最小结构：

```md
# Workspaces

| workspace_key | package_identity | path | kind | status | evidence |
|---|---|---|---|---|---|
| @acme/web | @acme/web | apps/web | app | active | apps/web/package.json:name |
| @acme/ui | @acme/ui | packages/ui | library | active | packages/ui/package.json:name |
```

字段合同：

| 字段 | 含义 |
|---|---|
| `workspace_key` | 项目内稳定身份；需求和计划只引用它，不引用当前路径 |
| `package_identity` | manifest 中的包身份；没有 manifest 时为 `—` |
| `path` | 相对唯一 `PROJECT_ROOT` 的当前规范化路径 |
| `kind` | `app` / `service` / `library` / `tooling` / `root` / `other` |
| `status` | `active` / `retired`；退役键不回收。目录移动后仍是 `active` |
| `evidence` | 身份与路径的证据来源，如 manifest 字段或人工确认记录 |

地图只记可寻址工作区，不把每个源码子目录都登记为 workspace。仓根共享配置或生成文件必须显式声明唯一归属，不暗中把整个仓根设为可写：

```md
## Path Ownership

| path_pattern | workspace_key | path_kind | evidence |
|---|---|---|---|
| package-lock.json | @acme/web | generated | npm-root-lock |
| tooling/** | @acme/ui | shared | architecture-decision |
```

`path_pattern` 只允许规范化项目相对精确路径或以 `/**` 结尾的目录前缀；`path_kind` 只允许 `shared` / `generated`。归属键必须 active，证据非空，任意两个 pattern 不得重叠。路径若同时落入工作区目录和 Path Ownership，两者必须指向同一键，否则 fail-closed。

## 3. 稳定键与路径规则

### 3.1 分配优先级

1. package / workspace manifest 提供稳定、项目内唯一的 package identity 时，优先直接用它作 `workspace_key`。
2. 没有 package identity 时，显式分配语义化项目内稳定键；必须记录确认依据，不得从临时绝对路径或随机串生成。
3. 单包项目使用保留键 `root`，`path` 为 `.`，`kind` 为 `root`。

键一旦被需求、计划或交付引用就终身不变。目录移动只更新 `path` 和 evidence，状态保持 `active`；包展示名变化若会改变既有键，也只更新 `package_identity`，不得静默重命名历史 `workspace_key`。

### 3.2 必须 fail-closed 的异常

- 两行使用相同 `workspace_key`。
- 两个 active 键解析到同一规范化路径。
- `path` 是绝对路径、含解析后逃出 `PROJECT_ROOT` 的 `..`，或经符号链接落到项目外。
- 需求引用地图不存在或 `retired` 的键。
- manifest 身份冲突、嵌套 workspace 归属不唯一，或项目根无法唯一解析。

异常未解决前，不得用“最像的目录”猜测，也不得把整个仓库作为兜底范围。

## 4. 单需求四类范围

每份 PRD 的 `<prd_id>/00_INDEX.md` 必须在入口层声明：

```md
## Workspace Scope

- primary_write: [@acme/web]
- supporting_write: [@acme/ui]
- read_only: [@acme/api-contracts]
- excluded: [@acme/admin]
```

| 类别 | 权限与责任 |
|---|---|
| `primary_write` | 主要实现工作区；至少一个，核心行为应落在这里 |
| `supporting_write` | 为完成需求允许的配套写入；不能借此做无关重构 |
| `read_only` | 可以读取上下文，禁止写入 |
| `excluded` | 默认既不读取也不写入；范围扩张审查通过后才能解除 |

四个集合必须两两互斥，所有键必须在项目地图中 active。可写集合严格等于：

```txt
allowed_write = primary_write ∪ supporting_write
```

`read_only`、`excluded`、未声明键以及无法解析的键一律 deny-write。未声明不是默许，空白也不是全仓通配符；`*`、`all`、项目根路径和父目录不得作为 workspace key。

## 5. 模块范围只能收窄

单需求模块可以声明更窄范围，但必须满足：

```txt
module.primary_write    ⊆ requirement.primary_write
module.supporting_write ⊆ requirement.supporting_write
module.read_only        ⊆ requirement.read_only ∪ requirement.primary_write ∪ requirement.supporting_write
module.excluded         ⊇ requirement.excluded
module.allowed_write    ⊆ requirement.allowed_write
```

模块四类集合也必须两两互斥。模块不声明范围时继承整份需求范围；一旦声明就必须给出完整四类，不能靠省略制造默认放行。模块不得把需求级 read-only 提升为 supporting write，不得解除 excluded，也不得引用地图外键。需要扩大时先走 §6，不能在模块表里偷渡。

声明只能位于单需求入口 `00_INDEX.md`，不得写进无损切片正文；精确表头为：

```md
## Module Workspace Scope

| module_slug | primary_write | supporting_write | read_only | excluded |
|---|---|---|---|---|
| login-flow | [@acme/web] | [] | [@acme/ui, @acme/api] | [@acme/admin] |
```

## 6. 范围扩张纪律

执行中发现必须写入当前可写集合外的工作区时，先停止该越界分支并产出扩张提案：

- 为什么现有范围不足；
- 拟新增或改类的 `workspace_key`；
- 会影响哪些 AC、方案步骤、验证和现有排除理由；
- 是否存在不扩张的更小替代；
- 扩张后的专项与回归验证。

提案通过用户 ACK，或危险模式的完整范围自审后，先更新需求 `Workspace Scope`，再按既有 amend / P3 重审纪律使旧方案 verdict 失效；完成重新冻结后才允许写。不得先改代码再补范围，不得只在 task-state 留一句说明冒充范围已更新。

目录移动不属于需求范围扩张：只要稳定键身份未变，只更新项目地图的 `path/evidence`，历史 PRD、AC 与交付继续引用原键。

## 7. 与宿主权限和项目根的关系

- 先由 `mcv-deployment.md §0.1` 解析唯一 `PROJECT_ROOT`。
- 再由宿主 sandbox / 用户授权决定物理可写上限。
- 最后由本契约决定项目根内这份需求允许写哪些 workspace。

三层取交集，任何一层拒绝都不能由另两层放行。危险模式冻结的授权上限不会因 `supporting_write` 增加而扩大。

## 8. 发现、计划与执行门禁

驻留入口为 `python3 tools/workspace-scope/workspace_scope.py`，所有子命令只读并输出稳定 JSON：

- `discover`：读取根 `package.json` 的 npm workspaces 数组/对象或 `pnpm-workspace.yaml`；只接受精确目录与单层尾随 `/*`。glob 下没有 manifest 的普通目录跳过，声明最终匹配不到任何 package manifest、身份重复、嵌套、symlink 或 npm/pnpm 声明冲突均 fail-closed。单包退化为 `root → .`。
- `validate`：严格校验工作区表、manifest identity、active/retired 状态与 `## Path Ownership` 唯一归属。
- `check-plan`：解析 AC 的每个钉版 `prd_refs`；live 版本不符时只读该 `prd_id/.archive/<prd_version>/00_INDEX.md`，组合模块有效范围，再校验 TECH_PLAN。
- `check-paths --path ...`：逐路径核对 owner、钉版权限和写计划；任一拒绝则整体失败。
- `check-diff --base <rev> [--head <rev>] [--include-untracked]`：以 Git `--name-status -z --find-renames` 同时核旧/新路径；删除、重命名、复制和未跟踪文件都不得绕过。

P3 的机器可读计划结构固定为：

```md
# Workspace Write Plan

| workspace_key | access | path_patterns | rationale |
|---|---|---|---|
| @acme/web | primary_write | [apps/web/src/**] | 核心实现 |
| @acme/ui | supporting_write | [packages/ui/src/login/**] | 配套组件 |
```

`access` 只允许 `primary_write` / `supporting_write` 且必须与钉版有效范围完全一致；`path_patterns` 非空、每项归属唯一且位于该键，计划至少含一个 primary。未列计划、read-only、excluded、未声明或无 owner 路径一律拒绝。

PreToolUse 对 `apply_patch` / `Edit` / `Write` / `MultiEdit` 的每个项目内非豁免目标执行同一 `check-paths` 判定；多目标调用中一个目标失败即整次 deny。AC 无 `prd_refs` 时该规则明确 N/A；只有 legacy `prd_version` 时 fail-closed 并要求先迁移。宿主 sandbox 仍是更高授权上限。

范围确需扩大时不得临时加宽 Write Plan：先改 PRD Scope、重新冻结 AC、使旧方案 verdict 失效并重审 P3，之后才可继续写入。

## 9. 退化态与动作边界

- 单包项目：地图只含 `root → .`，需求通常 `primary_write: [root]`；仍守同一四类与扩张合同。
- 非代码需求若确实没有实现工作区，由后续消费者定义受控 N/A，不得伪造 `primary_write`。
- legacy PRD 迁移时如何补范围属于 R5；首切如何生成范围提案属于 R6。
- 本门禁不拦 shell、网络或宿主允许的项目外写入；交付前仍须运行 `check-diff` 做完整改动面对账。
