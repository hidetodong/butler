# TECH_PLAN — ITER-0060 · 双宿主工作流注册与分发收敛

> ⚠️ 危险模式：本产物由模型自主 ACK（已过 `dangerous-engine.md §5.2` 自审门），未经用户逐项确认（ITER-0060，2026-07-18）。

## Goal

- 用一个 JSON registry + 一个标准库 renderer/checker 覆盖 AC1–AC8。
- 生成窄元数据与人读表，正文算法继续留在各 command/SKILL/Coder 真源。

## Files / Modules to Change

- **ADD `workflows/registry.json`**：8 workflow 与 plugin/distribution/hook 声明。
- **ADD `scripts/sync-workflow-registry.py`**：schema/结构校验、全量 plan、`--write` 原子更新、`--check` 零写入。
- **ADD `scripts/test-workflow-registry.py`**：临时 fixture 与真实仓合同测试。
- **ADD `docs/workflows.md`**：由 registry 生成的唯一八项能力表与分发边界。
- **EDIT 8 command + 8 SKILL frontmatter、8 `agents/openai.yaml`、8 `.agents/skills`**：受管投影；正文不重写。
- **EDIT `scripts/verify-dual-host.sh`**：接入 registry `--check` 与专项。
- **EDIT README/HUMAN_GUIDE/Codex compatibility/Coder README、项目知识**：改为链接生成表。
- **EDIT plugin/install 文档**：只补显式声明与校验，不改 plugin schema/hook 算法。

## Interface / Contract

```text
python3 scripts/sync-workflow-registry.py --check [--root PATH]
python3 scripts/sync-workflow-registry.py --write [--root PATH]
```

- registry 顶层只允许 `schema_version`、`plugin`、`workflows`。
- plugin 声明 name/root/manifest/hooks/personal installer/marketplace mode/team status；路径均仓内相对。
- workflow 固定字段：id、rule_source、risk、allow_implicit、semantic_triggers、legacy_aliases；`claude`/`codex` 子对象各含 name/path/description/default_prompt。
- write 先校验全部输入并在内存生成所有 bytes/symlink target；任何错误零写入。普通文件同目录 temp + `os.replace`，symlink 只接受/生成 `../../plugins/butler/skills/<name>` 相对 target。
- command frontmatter 只替换 `description`；保留 argument-hint 与正文。SKILL 只替换 name/description；openai.yaml 与 docs/workflows.md 全文件生成。
- check 比较预计 bytes、mode/软链 target 和实际集合；不调用 write，不生成 cache。

## State / Boundary

- registry 是工作流元数据真源；command/SKILL 正文仍是宿主薄路由，`Coder/` 是算法真源。
- docs/workflows.md 是八项人读表真源；其余文档只留概述/链接。
- plugin.json 保持官方 schema，hooks 自动发现文件独立存在；registry 只声明并校验两者关系。
- HOME marketplace 不写；team/public 状态是 `not-configured`，后续获得真实分发方案才能改。
- dangerous ON，自审、RUN_LOG、checkpoint、evidence 和完整审查必做。

## Design Decisions

- JSON + 标准库：无新依赖，CI/安装环境都能 check。
- 窄 frontmatter 投影：集中名称/触发描述但不生成算法正文，避免 registry 变成第二套规则引擎。
- 所有普通 workflow 也显式生成 `allow_implicit_invocation: true`：安全策略不依赖宿主缺省值。
- alias 只进 registry/docs，不生成实体入口：保留识别历史，又不复活 `/loop` harness 冲突。
- 分发状态三态化：repo discovery、personal installer、team/public not-configured；不从本机已安装推断团队能力。

## Execution Steps

- [x] T1 写 registry schema/data 与真实仓校验 → AC1、AC3、AC5
- [x] T2 实现全量 plan、frontmatter/YAML/docs/symlink 投影和原子 write/check → AC2、AC4、AC6
- [x] T3 补 fixture 漂移矩阵与幂等/零写入测试 → AC1–AC7
- [x] T4 运行 write，收敛 8 组元数据和四份人读文档 → AC2–AC6
- [x] T5 接入唯一 CI、官方 validator、plugin cachebuster/reinstall → AC5、AC7
- [x] T6 捕获 evidence、完整强审、修复并收口 ITER-0060/MILE-0007 → AC8

## Verification Plan

- schema/paths/sets：table-driven mutation fixtures。
- projections：frontmatter body preserved、YAML explicit policy、docs golden、symlink exact relative target、write twice no diff、check no writes。
- security：high-risk true/missing、alias entity、path escape、absolute symlink、partial write 注入。
- distribution：plugin manifest/hook matcher/wrapper/mode/setup installer/team state。
- non-regression：registry tests + `verify-ci.sh` + fixed official validators + Markdown + audit/diff evidence。

## Risks / Open Questions

- Python stdlib 无 YAML round-trip；openai.yaml 是完全受管小文件，采用确定模板输出，不解析任意 YAML。
- command/SKILL frontmatter 只支持当前简单单行字段；遇重复/缺 marker/多行 description fail-closed，不猜格式。
- 当前无设计阻塞，影响面与 AC 一致。
