# TECH_PLAN — ITER-0056 · 安装器事务安全

## Goal

- 从已冻结的 AC1–AC8 实现一个“先完整预检、再逐对象原子应用”的全局配置更新器。
- 让 `setup.sh` 只做跨组件编排；配置冲突在任何用户文件写入前暴露，Codex plugin 失败则明确报告 Claude 侧已完成的部分状态。

## Files / Modules to Change

- **ADD `scripts/configure-global-install.py`**：零依赖标准库 helper；规划并应用 shell rc、Claude 全局配置、命令命名空间和旧扁平软链清理。
- **ADD `scripts/test-configure-global-install.py`**：直接测试纯 plan/merge/ownership 判断与临时 HOME 应用，锁住异常输入零写入和成功路径幂等。
- **EDIT `scripts/setup.sh`**：删除脆弱的 `grep/sed/awk/ln` 直接编辑，调用 helper；捕获 plugin installer 失败并输出“Claude 已完成、Codex 失败”的部分完成信息。
- **EDIT `scripts/verify-dual-host.sh`**：先跑 helper 单元测试，再保留 setup 有/无 Codex 的集成矩阵；补日志、权限、目标树和仓路径迁移断言。
- **EDIT `HUMAN_GUIDE.md`**：在安装/升级说明旁登记三类 fail-closed 冲突及人工处理入口；只写用户该怎么处理，不复制算法。
- **P4/P5 状态文件**：按 AC 维护 `task-state`、`01_CHANGELOG`、VERIFY 和交付归档，不改规则算法正文。

## Interface / Contract

- helper CLI：`python3 scripts/configure-global-install.py --butler-root <绝对路径> [--home <测试 HOME>]`。
- 默认 HOME 从环境读取；`--home` 只为隔离测试和明确调用提供，不推断真实用户目录。
- 成功返回 `0`，打印每个对象的 `写入 / 更新 / 保持 / 清理 / 跳过` 状态。
- 配置冲突或 I/O 失败返回 `2`，错误包含冲突对象、检测结果和人工修复办法；未进入 apply 前不修改任何受管对象。
- `setup.sh` 仅在 helper 成功后进入 Codex plugin 步骤；plugin 失败沿用其非零状态，并额外说明 Claude 配置已经完成、Codex 未完成，不打印总成功。

### shell rc 契约

- 有效行匹配 `^[空白]*export[空白]+BUTLER_PATH[空白]*=`，注释和普通文本不算。
- 0 条：在文件尾以规范区块追加一条；1 条：只替换该行；多条：冲突退出。
- 没有 `.zshrc`/`.bashrc`：保持现有“跳过并给手动命令”，不擅自创建用户 shell 配置。

### Claude 全局配置契约

- marker 字符串必须作为独立行出现；0 个可追加，恰好 2 个可替换两者之间的完整 managed block。
- 其他数量、marker 只以内联文本出现或边界无法唯一识别时冲突退出。
- 成功替换只改变 managed block；前缀、后缀、换行和文件 mode 保持。

### 命令软链所有权契约

- `~/.claude/commands/butler` 不存在：原子建立指向当前源的软链。
- 已指向当前源：保持或原子刷新，结果幂等。
- 指向旧源：只有当词法目标符合 `<butler-root>/.claude/commands/butler`，且该 root 仍有 `Coder/README.md` 与 `scripts/setup.sh` 等 Butler 身份证据时才允许迁移。
- 真实文件/目录、无关软链、无法证明归属的断链：冲突退出，绝不删除或在其内部新建软链。
- 旧 `butler-prd.md` 软链同样先验所有权；只清理由可识别 Butler checkout 创建的旧路径，不按文件名直接删除。

## State / Boundary

- helper 的 `plan()` 完成所有内容解析和所有权检查，不产生副作用；任一冲突都会阻止全部配置对象进入 apply。
- `apply()` 为每个普通文件在同目录创建临时文件、写全内容、复制原 mode，再用 `os.replace` 原子替换；临时文件在成功或异常后都清理。
- 软链先在目标父目录创建临时链接，再以 `os.replace` 切换；不通过 `ln -sfn` 对真实目录做模糊处理。
- 多对象无法获得真正的文件系统级全局事务。预检能避免已知冲突造成部分修改；apply 期间若出现外部 I/O 故障，保留已完成对象并准确报告，不伪称整体回滚。
- Codex plugin 是 helper 之后的外部组件，不进入用户文件事务；R1 不改 `install-codex-plugin.sh`。

## Design Decisions

- **选择标准库 Python helper，拒绝继续堆 Bash 文本编辑**：Python 能统一 macOS/Linux 行为，并直接复用本仓已验证的 tempfile + mode + `os.replace` 模式；代价是 setup 明确依赖 Python 3，而仓库现有 renderer、resolver、hooks 已经有相同依赖，不新增运行时类别。
- **helper 专管全局安装，不抽取 renderer 通用库**：两者 marker、目标和迁移语义不同；本轮只复用安全模式，不为了几行原子写把成熟 renderer 一起重构。
- **先全量 plan、再 apply**：比“每一步发现问题再停”更能避免已知 marker/软链冲突留下半安装；但不冒称跨文件 ACID 事务。
- **不自动保留长期 `.bak` 文件**：原子替换、mode 保持和冲突前零写入已经满足冻结 AC；长期 backup 会引入命名、清理和敏感内容副本问题。若未来需要恢复历史，另开明确契约。
- **所有权证据宁严勿松**：旧 checkout 仍可识别时自动迁移；证据消失的断链交给用户确认，避免凭 basename 接管别人的路径。
- Active Profiles：无，仅遵循通用实现纪律、测试策略和 fail-closed 边界。

## Execution Steps

- [x] **T1** 先写 helper 单元测试，覆盖 marker、export、软链所有权、mode、幂等和三个已知缺陷 → AC1–4、AC6
- [x] **T2** 实现无副作用 plan、原子普通文件/软链 apply 与可执行错误信息 → AC1–5
- [x] **T3** 改 `setup.sh` 调 helper，并补 plugin 失败的部分完成回声 → AC3–5、AC7
- [x] **T4** 扩展隔离 HOME 集成矩阵，覆盖空首装、重复安装、旧路径迁移、无/fake/失败 Codex installer → AC6–7
- [x] **T5** 更新最小人读冲突说明，运行专项测试、双宿主矩阵、diff 检查和主 agent review → AC8

## Verification Plan

- **AC1/AC2**：单 marker、3/4 marker、内联 marker、完整 pair + 前后用户字节、特殊 mode、重复运行逐例断言。
- **AC3**：注释伪命中、0/1/2 条有效 export、前导空白、路径迁移和 mode 保持逐例断言。
- **AC4**：目标缺失、当前 Butler 软链、可识别旧 Butler 软链、真实目录、普通文件、无关软链、可识别/不可识别断链逐例断言。
- **AC5**：plan 冲突前快照全部受管对象；失败后逐字比对无变化、无临时垃圾；fake plugin 失败验证无总成功文案且退出非零。
- **AC6/AC7**：运行 `python3 scripts/test-configure-global-install.py` 与扩展后的隔离 `verify-dual-host.sh`。
- **AC8**：运行 `bash scripts/verify-dual-host.sh`、`git diff --check`；审查 Git diff 不包含 renderer、resolver、hooks、workflow 算法和真实 HOME。

## Risks / Open Questions

- `os.replace` 对普通文件和软链在同一文件系统内原子，但多个目标之间不是全局原子；日志与文档必须保持这一诚实边界。
- 旧软链认领规则若太松会误接管，太严会让部分历史安装需人工清理；按“可识别 checkout 自动、证据缺失停下”取安全侧。
- shell rc 可能使用复杂条件生成 `BUTLER_PATH`；helper 只管理简单 export 行，复杂写法按冲突/未识别处理并回声，不尝试解释 shell 程序。
- 当前无阻塞问题；方案获 ACK 后可进入 P4。
