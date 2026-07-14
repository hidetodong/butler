# constraints（现行约束）

> 只放长期边界，实现细节指对应 schema。与 `invariants` 的区别：不变量是"设计骨架不能动"，约束是"干活时必须守的边界"。

- **写作面向 AI 执行**：措辞用"必须 / 不得 / 应"，中文说明、标识符与文件名用英文。规则之间靠文件名互相引用，不写绝对路径。真源 仓库根 `CLAUDE.md`。
- **注册即真源、无隐式依赖**：新增规则文件必须在 `Coder/README.md` 的目录结构 + 读取顺序注册；新增知识主题必须在 `.ai/project/00_INDEX.md` 主题表登记。没注册 = 不存在。
- **frontmatter 必标 audience + scope**：每个规则文件头必须写清给谁读、管什么范围。
- **版本 semver（规则仓口径）**：MAJOR 破坏性 / MINOR 兼容新增 / PATCH 澄清修订；切版必写迁移配方 + 打 tag `vX.Y.Z`，切版前后各跑一遍一致性自检。真源 `versioning-schema.md §6`。
- **提交规约**：`type(scope): 中文描述 (ITER-NNNN)`，发布用 `chore(release): vX.Y.Z — 聚合 …`，末行 `Co-Authored-By` 署名；提交单元 = 迭代收口，"提交 ≠ 切版"（发布提交独立）。非 hook 门禁，靠纪律兜底。真源 `versioning-schema.md §5`。
- **测试自动化优先**：能自动化的验证必须自动化（含浏览器自动化覆盖 UI / 交互），人测只留机器不可测的残余；P5 分自动道 / 人测道回填、叠**分级置信**（可靠 / 弱 / 待人）。感知项先造**代理验证**（截图 diff / VLM 判图）挣"弱"档，不冒充"可靠绿"。人测残余走 `human-test-bridge.md` 四态回传闭环。真源 `testing-strategy.md §3` / `verify-schema.md`。
- **最小实现纪律（P4 常驻）**：写新码爬"最小实现阶梯"（YAGNI→复用→标准库→平台原生→已装依赖→一行→最小新代码，停在第一个成立的档）；有意简化用 `butler-min:` 注释标天花板 + 升级路径；修 bug 挖根因不打症状补丁。但信任边界校验 / 防丢数据 / 安全 / 无障碍 / 用户明确要求不得砍，且绝不对"理解问题"偷懒。真源 `implementation-discipline.md`。
- **无人残余处置（`/butler:dangerous`）**：无人值守下人测残余按依赖感知准入闸处置——不阻塞异步入账、卡下游不硬闯、**红线绝不假绿**。真源 `dangerous-engine §7.4`。
