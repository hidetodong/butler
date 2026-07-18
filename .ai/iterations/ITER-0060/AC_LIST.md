---
状态: ack-frozen
ACK 日期: 2026-07-18
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 `dangerous-engine.md §5.1` 自审门），未经用户逐项确认（ITER-0060，2026-07-18）。

# Goal

用单一机器注册表收敛八个 Butler 工作流的双宿主发现、触发、安全、兼容和分发元数据，并让生成器/CI 机械阻止名称、入口、软链、hook、文档或风险策略漂移。

# In Scope

- 八工作流 registry schema/data：ID、Claude/Codex 名称和路径、描述/default prompt、规则真源、风险、隐式触发、语义触发和 legacy aliases。
- 确定性 `--write/--check`：窄更新 command/skill frontmatter、生成 openai.yaml/人读表、维护 repo discovery 软链。
- plugin manifest/hooks/个人 installer/团队边界的注册与结构校验。
- README/HUMAN_GUIDE/Codex compatibility/Coder README 改为引用生成能力表，不再手写第二份八项清单。
- 专项漂移 fixture、官方 validators、完整 CI/evidence 和危险模式强审。

# Out of Scope

- 不生成或合并八个工作流的算法正文，不改变 PRD/review/milestone/upgrade/ideation/preference/loop/dangerous 语义。
- 不恢复 `/loop`、`/dangerous` 等可能碰撞 harness 的旧实体命令；alias 只登记兼容识别和弃用文案。
- 不创建公共/团队 marketplace，不写其他用户或团队机器配置，不承诺 plugin 已在团队分发。
- 不把 hooks 字段塞入官方不支持的 plugin.json；只校验标准自动发现文件。
- 不推进新业务能力，不修改 R4 升级事务，不发布/推送除非整体收口流程另有明确授权。

# Acceptance Checklist

- [x] **AC1（注册表完整唯一）**：机器 registry 由 schema version 管理且恰含 8 个唯一 workflow；每项含唯一 id、Claude command/path、Codex skill/path、规则真源、两宿主描述/default prompt、risk、allow_implicit、semantic triggers、legacy aliases。所有路径必须仓内相对且存在，名称/路径/ID 一一对应；重复、缺项、额外入口、越界或未知字段均失败。
- [x] **AC2（确定性生成与零写入检查）**：一条标准库命令支持 `--write` 和 `--check`；write 后第二次 write 字节幂等，check 前后全仓相关摘要不变。它只窄更新 8 command/skill frontmatter、生成 8 openai.yaml 与单个人读能力表、创建/校正 8 个相对软链；正文 user content 不变，错误输入零部分写入。
- [x] **AC3（高风险触发门）**：registry 显式规定 loop/dangerous `risk=high` 且 `allow_implicit=false`，其余 6 项显式 true；生成的 openai.yaml 与 skill/command 描述保持该意图。任何 high-risk 缺失/true、普通项策略漂移或旧名被生成为可隐式高风险入口均被 check 拒绝。
- [x] **AC4（宿主与 repo discovery 对账）**：每项 Claude command 文件、Codex SKILL name/frontmatter、openai.yaml display/prompt/policy 和 `.agents/skills/<codex-name>` 相对软链都由 registry 对账；断链、绝对软链、复制目录、遗漏/额外 workflow 或宿主名称不匹配给出精确诊断。
- [x] **AC5（plugin hooks 与分发声明）**：registry 显式指向 plugin manifest、`hooks/hooks.json`、个人 installer 和 personal marketplace 模式；check 验证 plugin name/skills path、Pre/Post matcher/脚本、wrapper 可执行、setup→installer 接线。生成能力表明确 repo discovery、个人安装、团队/公共未配置三种状态，不把个人安装冒充团队分发。
- [x] **AC6（旧名兼容与人读单源）**：registry 登记 8 项 legacy aliases、碰撞/弃用说明和当前 canonical 名；`/loop` harness 冲突明确。生成 `docs/workflows.md` 是唯一八项能力表，README/HUMAN_GUIDE/Codex compatibility/Coder README 只链接或概述，不再各自维护完整名称/策略清单。
- [x] **AC7（漂移与非回归测试）**：fixture 至少覆盖 duplicate/missing/extra、路径逃逸、frontmatter/name/openai/doc stale、broken/absolute symlink、high-risk implicit、hook matcher/wrapper、plugin/installer/distribution 漂移；正常 registry write/check、官方 plugin + 8 skill validators 和现有双宿主/hook 测试均通过。
- [x] **AC8（证据与收口）**：registry 专项、write→write 幂等/check 零写入、完整 `verify-ci.sh`、`git diff --check`、active/closed state audit 与风险 reproduced 均生成 ITER-0060 evidence record；P5 逐 AC 引用 record，完整审查 Must Fix=0 后归档，随后收口 MILE-0007。

# Verification Method

- AC1：加载真实 registry 并对每类 schema/集合/path mutation 跑负向 fixture。
- AC2：临时复制最小 repo，write 两次比较 bytes/inode target；check 比较摘要；在一项 invalid 时断言所有受管文件零改。
- AC3：改 high-risk implicit、删除 policy、给 alias 生成入口、翻普通策略，均断言失败；核生成 YAML 显式 true/false。
- AC4：逐项核 command/SKILL/openai/symlink；构造 broken/absolute/copy/extra/mismatched name。
- AC5：变更 plugin name/skills、hook matcher/command/mode、setup installer 引用和 distribution 字段，断言精确失败。
- AC6：对生成 docs 做 golden/idempotence；静态检查四份人读文档不再复制八项完整枚举且链接真源。
- AC7：运行 registry 专项、官方 validators、双宿主完整矩阵。
- AC8：用 evidence runner 捕获正常/负向复核、完整矩阵、diff/state，失败首跑保留。

# Open Questions / Risks

- frontmatter 的窄重写必须保留 command 的 `argument-hint` 和 skill 正文；实现应先全量 plan 后统一写，避免第七项失败时前六项已改。
- 个人 marketplace 文件在 HOME，不作为 registry 生成目标；仓库只登记模式/installer 并在隔离 HOME 验证，避免越权接管用户 marketplace。
- 本轮改变 plugin skills 元数据，最终须按 plugin-creator 官方 cachebuster/reinstall 流程刷新安装副本；仓内源版本仍严格等于 VERSION。
