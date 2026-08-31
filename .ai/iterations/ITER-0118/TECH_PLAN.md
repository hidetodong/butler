<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0118

方案状态: pass

## Design Decisions

- **D1 · 工具落 `tools/intake/`，入口 `intake.py`，与 `intake-schema.md` 同名同源。** CLI 照 `tools/decision-map/` 的既有约定：子命令 + 必填 `--project-root` + 单行 JSON 输出（`json.dumps(..., ensure_ascii=False, sort_keys=True, separators=(",",":"))`）。Python 零依赖，测试放 `tools/intake/tests/`，用 `unittest`。带一份 `README.md`，它的第一个标题会被 `sync-project-overview.py` 抓去当驻留工具清单里的一句话说明。

- **D2 · 三个子命令的参数形状，写死不猜。**
  - `add --project-root <p> --text "<一句话>" [--date YYYY-MM-DD]` → 返回 `{"key": "...", "state": "new"}`。`--date` 只用于测试固定时间，正常调用取当天。
  - `list --project-root <p> [--layer inbox|backlog|all] [--state ...] [--scale ...]` → 返回两层的条目数组。
  - `handle --project-root <p>` 分两种目标，**显式区分、不靠猜键的形状**：
    - `--inbox <闪念键> --to incubated|done|dropped`，其中 `incubated` 另需 `--slug` `--scale` `--title` `--reason`，`done` / `dropped` 需 `--note`。
    - `--backlog <候办键> --exit promote|iterate|withdraw`，`withdraw` 需 `--reason`。
  - 两个目标参数互斥且必须给其一。确定性工具不该在 `YYYY-MM-DD-slug` 和裸 slug 之间猜用户指的是哪一层。

- **D3 · 分流的「决定」在命令层做，工具只认已定好的目标态。**（对应 AC_LIST 未定项一）工具不判断「这条该孵化还是该丢」，只做三件事：校验这一步转移合不合法、把要写的内容全算出来、原子落盘。理由是 butler 既有的分工就是这样——确定性程序登记事实、模型做语义判断；把判断塞进工具会得到一个不可测也不可复核的黑盒。代价是 `handle` 这个动词有点名不副实，它更像「执行一次已经定好的处置」。缓解办法是在动作层规则里把这句话明写出来，别让读者以为工具会替他想。

- **D4 · 草稿正文的交接点：工具产骨架并留可机检的占位标记，`list` 负责把没填完的挑出来。**（对应未定项二）`handle --to incubated` 按 `--scale` 生成对应档的段落骨架，每段正文放一行占位标记（`<!-- TODO(intake): ... -->` 这种一眼能看见、也能被脚本找出来的注释）。`list` 对仍含该标记的草稿返回 `"incomplete": true`。这样「工具写了个空壳、模型以为写好了」这个失败模式有一条现成的检出路径，而且**不新增第四个子命令**——检查落在本来就要跑的读路径上。

- **D5 · 动作层新建 `Coder/40_Context_Management/intake-workflow.md`，不改写 `inbox-workflow.md`。**（对应未定项三）新建的理由有两条：改写旧文件违反本轮 Out of Scope，而且会把 R8 的退役工作提前拽进来；「数据契约 + 动作层」这个二分是既有结构（`inbox-schema.md` 配 `inbox-workflow.md`），照抄读者不用学新东西。文件里要写死三个动作各自的「工具决定 / 必须问用户」分界，以及 D3 那句实话。

- **D6 · 注册表复用 `inbox` 这个 id，只改字段不动集合。** `rule_source` 由 `inbox-workflow.md` 改指 `intake-workflow.md`；`claude.description` / `codex.description` / `semantic_triggers` 改成新语义，去掉 `scan origin` / `处理 origin` 这类字样。id 不变意味着 `EXPECTED_IDS`、工作流个数、命令文件集合、skill 集合、软链集合全都不动，人读文档里那三处散文计数也不用碰。改完跑 `sync-workflow-registry.py --write` 重生成投影（命令 frontmatter、skill frontmatter、`agents/openai.yaml`、`docs/workflows.md` 表）。**顺带一处容易漏的**：`workflows/router-examples.json` 里 inbox 那条示例请求写的是「处理 origin 里的需求收件箱」，也得换成新语义的说法，否则示例在描述一个已经不存在的行为。

- **D7 · `test_inbox_workflow.py` 拆成「跟着命令走」和「留给 R8」两半，文件名不动。** 三个用例的处置：
  - `test_inbox_workflow_route_and_safety_contract`（断言旧规则文件的 8 个分类、双指纹字段等内容）→ **原样保留**，它描述的是 `inbox-workflow.md` 这份文件本身，R8 连文件一起删。
  - `test_inbox_is_registered_for_both_hosts` → `rule_source` 的断言改指 `intake-workflow.md`，命令名、skill 名、`allow_implicit_invocation` 三条不变。
  - `test_host_entries_are_thin_and_resolve_project_root` → 断言改为薄壳里必须出现 `intake-schema.md`、`intake-workflow.md`、`tools/intake/`；**删掉 `origin/` 那条**，保留 `BUTLER_PATH` 与 `mcv-deployment.md §0.1`。

  文件名保持 `test_inbox_workflow.py`：它测的仍是 inbox 这个工作流，那个目录是 pytest 目录发现、改名不影响运行，但也没有收益。

- **D8 · `milestone-schema.md §7.6` 的「普通暂缓」改为指向工具，改动全落 §7.6 内。** 现在那五步里，第 3 步（写草稿文件）与第 4 步（追加索引行）是让模型照文字手工做的。改法是把这两步合并成一步「调用 `tools/intake/intake.py handle --inbox <闪念键> --to incubated ...`，由工具原子写这两处」，并保留第 1、2、5 步（切方向、选稳定键、不写 `.ai/MILESTONE.md` 不改 `current`）。不改「误开后退回」那半段——它处理的是正式表上的临时行，跟闪念口无关。

- **D9 · 跨文件原子性做不到真原子，做「先算后写 + 失败即回滚」，并且如实这么说。** 实现是：先把每个目标文件的最终字节和原始字节（不存在则记 `None`）全算出来，全部校验通过后按序写；任一步写失败就把已写的按逆序还原（原来不存在的删掉），再以非零码退出。单个文件的写用临时文件加 `os.replace` 保证它自己那一次是原子的。**这不等于数据库那种事务**——如果回滚过程本身也失败（比如磁盘满），仍可能留下半截态。这句实话要写进 `intake-workflow.md` 和验证报告，不许在文档里用「原子事务」这种过头的词。测试用注入第二处、第三处写失败的方式，断言三处全部回到原样且退出码非零。

- **D10 · 两条出口里工具只做确定性可核对的那部分。**
  - `--exit promote`（限 `milestone` 档）：校验 `.ai/MILESTONES.md` 的 `current` 为 `none` → 领下一个连续 `MILE-NNNN` → 正式表追加 `active` 行 → `current` 指向它 → 把草稿正文原样搬进 `.ai/MILESTONE.md`（能原样搬正是因为 `milestone` 档的四段就是 §5 要的四段）→ 删草稿 + 删索引行。全部进同一个写盘计划。
  - `--exit iterate`（限 `iteration` 档）：校验 `.ai/ITERATIONS.md` 的 `current` 为 `none` → 领下一个 `ITER-NNNN` → 台账追加 `active` 行 → `current` 指向它 → 删草稿 + 删索引行。**不写四件套**——那是 `iteration-schema.md §5.1` 里模型的活，工具在返回的 JSON 里给一个 `next_step` 指明该去写 P1 的 CONCEPT，不代劳。
  - `--exit withdraw`（任意档）：删草稿 + 删索引行 + 在 `.ai/MILESTONE.md §5.4` 追加一行原因（该文件不存在时跳过并在 JSON 里说明）+ 回写关联的闪念行为 `dropped`。

  关联闪念的找法：扫 `.ai/INBOX.md` 找「去向」列恰好等于这份草稿路径的那一行；找不到就是这份草稿不是从闪念来的，跳过回写。

- **D11 · dogfood 选题必须是真的：交付页渲染器现在住在会话临时目录里。** 本会话反复用的那个把交付总结 `.md` 渲染成固定格式 HTML 的脚本，实际存放位置在会话临时目录下，换个会话就没了；而 `delivery-summary.md §9` 说 HTML 模板是唯一真源，却从没说渲染器在哪——仓库里根本没有。这是一个真实、具体、够一个迭代收口的缺口，正好是 `iteration` 档，顺带能证明新的 `iteration` 档只写两段是够用的。**不为了跑通流程编假需求**——在自己的台账里造假条目正是 MILE-0016 一直在修的那类问题。

- **D12 · 沙箱 dogfood 在临时目录造项目根，只证代码路径。** 造一个含 `.ai/MILESTONES.md`（`current: none` + 空正式表 + 待办区一行）、`.ai/ITERATIONS.md`（`current: none`）、`.ai/MILESTONE.md` 与一份对应档草稿的临时项目根，把 `promote` 与 `iterate` 各跑一遍，断言台账出现预期行、`current` 已指向、草稿与索引行两侧删净。**这一档在验证报告里必须与 D11 分开写**：它证明的是代码路径通，不是真实使用下好用。

- **D13 · CI 接入一行。** 在 `scripts/verify-ci.sh` 里紧挨旧 inbox 工具那行之后加一行跑 `tools/intake/tests` 的发现式测试。旧的那行原样保留（旧工具 R8 才删）。

- **执行顺序**：T1 写 `tools/intake/`（`intake.py` + `README.md` + 测试）→ T2 写 `intake-workflow.md` → T3 改注册表 + 路由示例 + 两份薄壳正文，跑 `--write` 重生成投影 → T4 拆 `test_inbox_workflow.py` → T5 改 `milestone-schema.md §7.6` → T6 `Coder/README.md` 两处注册 → T7 CI 接入一行 → T8 butler 仓真实 dogfood（D11 选题）→ T9 沙箱 dogfood（D12）→ T10 `.ai/MILESTONE.md §5.4` 三条登记 + `.ai/debt.md` 增减 → T11 OVERVIEW 重算 → T12 两组扫描脚本 → T13 CI + 审计取退出码。

## Failure Paths

- **薄壳里残留 `origin/` 或旧动作层文件名的字样。** 新命令不扫 `origin/`，留着这个词就是写假话；但删了它旧断言会红，容易图省事留着。检出手段：A 组扫描断言两份薄壳正文里这两个字样各零命中，同时 D7 的用例改造必须落地。
- **拆测试时手滑改到旧规则文件或另一份测试。** 那等于把 R8 的退役工作提前引爆。检出手段：`inbox-schema.md`、`inbox-workflow.md`、`test_inbox_contract.py`、`tools/inbox/` 全目录与 `pre-p4.baseline` 逐份哈希比对。
- **三处联动写盘留下半截态。** 最典型是草稿写了、索引行没写，或者闪念行回写了、草稿没落盘。检出手段：注入写失败的单元测试断言全部回滚；另有审计里现成的候办集合相等断言（索引集合 == 文件集合）做事后兜底。
- **回滚本身失败。** D9 已承认这条兜不住。缓解只有把话说清楚，不在文档里用「事务」这种过头的词，并如实登记。
- **工具写的台账行格式与状态台账迁移工具或审计的解析对不上。** 检出手段：dogfood 跑完立刻跑一次 `state_ledger.py migrate` 加审计，退出码必须 0；沙箱那半也断言写出的行能被同一套解析器读回来。
- **`handle --to incubated` 生成的骨架没人填。** 检出手段：`list` 对含占位标记的草稿标 `incomplete`；B 组扫描断言 dogfood 产出的那份草稿里已无该标记。
- **路由示例还在描述已经不存在的行为。** `router-examples.json` 里 inbox 那条写的是「处理 origin 里的需求收件箱」。检出手段：`sync-workflow-registry.py --check` 只校验覆盖度不校验语义，所以这条只能靠 B 组扫描断言新措辞在场、旧措辞不在。
- **OVERVIEW 的驻留工具清单没跟上。** 新工具要有 `README.md` 且第一个标题就是那句说明，否则清单里会出现一个破折号。检出手段：`--write` 后 `--check` 取退出码并断言清单里有 `tools/intake/`。
- **扫描脚本自命中。** 模式串用片段拼接构造，跟前两轮同法。

## Test Strategy

- **本轮有真代码，所以有 TDD 配对。** `tools/intake/` 的核心行为（闪念键生成与撞名退让、非法转移拒绝、三处联动回滚）按先写测试后写实现的顺序做，用同一条发现式测试命令留 Red → Green 配对证据。
- **单元测试覆盖四类**：①`add` 的键生成、撞名、建表头、追加不动其余行；②`list` 的只读性（跑前跑后哈希不变）与筛选；③`handle` 的四条合法转移逐条通过、非法组合逐条被拒且不留痕；④三条出口的前置校验与两侧删净。
- **注入失败测试**单独一类：让写盘计划的第二处、第三处抛错，断言三处文件全部回到原始字节、退出码非零。
- **端到端脚本**在临时目录里跑真实命令行（不是直接调函数），断言退出码与 JSON 结构，避免「函数对了但命令行接线错了」这种漏网。
- **两组扫描各一遍**：A 组查越界（活跃面不出现 R9 才存在的孵化区路径、新工具与新规则不出现旧编号前缀与双指纹字段名、两份薄壳不出现 `origin/` 与旧动作层文件名），B 组查在场（旧链哈希未变、三个动作与三条出口在场、README 两处注册、§7.6 已改指、候办 9 → 10、dogfood 草稿无占位残留、路由示例已换措辞）。
- **门禁两条取退出码**：`bash scripts/verify-ci.sh` 须为 0（含新接入的那行）；`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 须为 0 且 `[UNRELEASED]` 恰 2 条。
- **机器证不了的部分说清楚**：沙箱那两条出口证明的是代码路径通，不是真实使用下好用；真实使用只覆盖了 `new → incubated` 这一段。这条写进验证报告的剩余风险，不混进「dogfood 已完成」。

<!-- butler-tdd-cycles: v1 -->
| Cycle | AC | argv_json | cwd |
|---|---|---|---|
| intake | AC1,AC2,AC3,AC4,AC5 | `["python3","-m","unittest","discover","-s","tools/intake/tests","-t","."]` | `.` |

## References Compliance

- 本迭代无 `.ai/references/` 外部参考资料，无 PRD 约束，无 workspace scope 边界需要对账。
- 内部依赖与引用方式：`Coder/40_Context_Management/intake-schema.md`（R6 定的数据契约，本轮全部实现以它为准，新动作层指针引用不重抄字段定义）；`milestone-schema.md §4.5`（候办键与索引行规则，工具按它生成）、`§7.1`（`promote` 的动作真源）、`§7.6`（本轮改指工具）；`iteration-schema.md §5.1`（`iterate` 的动作真源，工具只做台账那半、四件套仍归模型）；`scripts/sync-workflow-registry.py`（注册表校验与投影规则，不改脚本只改数据）；`tools/decision-map/`（同类工具的命令行与测试约定，照抄不重造）。
- 新增规则文件按 `CLAUDE.md` 的约束在 `Coder/README.md` 两处注册；新增工具带 `README.md` 以接入 OVERVIEW 的驻留工具清单。
- 书写口径按 `artifact-style.md`：动作层规则对 AI 用「必须 / 不得」，给人读的说明句守说人话四条——「受管区块标记」「占位标记」「先算后写」这类词第一次出现要紧跟一句大白话。
