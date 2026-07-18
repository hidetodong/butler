# CONCEPT — ITER-0060 · 双宿主工作流注册与分发收敛

> 分流: 完整 | 命中升级信号: 跨宿主元数据、生成器、兼容与分发契约 | 2026-07-18

## 一句话

把 Butler 八个工作流在 Claude、Codex、repo discovery、plugin 和文档里的“叫什么、能否语义触发、旧名是什么、怎么分发”收成一份登记表。以后加改工作流只改注册源并重生成，CI 会拦住任何一处漏同步，尤其不能让 loop/dangerous 的高风险显式门槛漂移。

## Goal

- G1：建立八工作流单一注册源，覆盖宿主名称、路径、描述、触发策略、风险级别、旧名和规则真源。
- G2：确定性生成或校验 Claude/Codex 入口元数据、Codex `openai.yaml`、`.agents/skills` 软链与人读能力表。
- G3：机械锁死 loop/dangerous 禁隐式、高风险旧名不降门槛；普通六项显式登记允许语义触发。
- G4：把 plugin hooks、个人 marketplace 安装和团队分发边界写成可校验声明，避免“个人已装”被误写为团队可用。
- G5：接入唯一 CI/local 矩阵并用 evidence 证明正常生成、零写入 check 和多类漂移拒绝。

## Current Understanding

- 仓库已有 8 个 `.claude/commands/butler/*.md`、8 个 `plugins/butler/skills/*/SKILL.md`、8 个 `agents/openai.yaml` 和 8 个 `.agents/skills` 相对软链，但没有共同登记表。
- 名称/描述/默认 prompt/隐式策略散落：只有 loop/dangerous 的 YAML 写 `allow_implicit_invocation: false`，其余靠字段缺省表达 true；安全意图不够显式。
- README、HUMAN_GUIDE、Codex compatibility 和项目知识分别手写“8 个入口”及名称，改名时容易漏一处。
- plugin manifest 不能写不受支持的 `hooks` 字段；hooks 的合法显式声明应指向自动发现的 `plugins/butler/hooks/hooks.json`，并由 registry contract 校验，而不是破坏官方 manifest schema。
- 当前 marketplace 是个人 `~/.agents/plugins/marketplace.json`，source 指 `~/plugins/butler`；`scripts/install-codex-plugin.sh` 负责复制、cachebuster、官方校验和 reinstall。团队分发尚无发布 marketplace，不应冒称团队已配置。

## Constraints

- 注册表只管元数据和分发治理，不复制 `Coder/` 工作流算法或把八份正文模板化成难维护的大生成文件。
- 生成器必须标准库可运行；`--check` 零写入、给出具体漂移路径，`--write` 只改登记产物/受管 frontmatter/软链。
- loop/dangerous 的 `allow_implicit_invocation: false` 是安全不变量；任何缺失/true 都必须失败。
- 旧名只做可检测兼容/弃用说明，不重新创建与 Claude harness 冲突的 `/loop` 实体命令。
- plugin manifest 保持官方 schema；hooks/distribution 通过 registry + 现有文件校验显式化。
- 不发布公共 marketplace、不写团队机器配置、不修改业务算法、不切版/推送，直到里程碑收口判断。

## Impact Scope

- 新增：工作流 registry、render/check 工具、生成的人读能力表和专项 fixture 测试。
- 修改：8 command/skill frontmatter、8 openai.yaml、统一验证入口、README/HUMAN/Codex/Coder 指针和 plugin 分发说明。
- 校验：8 symlink 集合、plugin manifest、hooks.json、installer/setup 接线、legacy alias 与风险策略。
- 不影响：命令/skill 正文算法、P1–P5、升级器项目事务、目标项目文件和远端 marketplace/ruleset。

## Project Type / Active Profiles

- 项目类型：Markdown 规则仓 + JSON registry + Python 生成/校验 + Codex plugin。
- Active Profiles：无，仅按通用 SOP；危险模式护栏持续生效。

## Open Questions

- 无阻塞。采用“registry 生成窄元数据与能力表、校验正文/分发结构”的边界，避免生成整份命令正文。
