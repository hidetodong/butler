<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0099 · 升级器 hook 树摘要与部署文件集对齐

身份迁移: 原工作在远端同步前暂用 ITER-0096；该编号已被远端正式收口任务占用，2026-08-01 按单调编号规则迁移为 ITER-0099。需求与技术范围不变，验证证据重新采集。

分流: 完整 | 命中升级信号: 多文件改动、契约变更、关键路径、跨模块影响 | 2026-07-29

## Current Understanding

- 现象：凡是升级队列里含 `sync_hooks` 的已部署项目，`plan` 一律停在 `conflict` 并报 `target hook tree is not a recognized Butler-managed version; refusing overwrite`。本机 6 个已部署项目实测**全部失配、无一例外**，等于所有老项目都被挡在升级门外。
- 根因是同一个文件集被两套口径统计。`upgrade.py` 的 `hook_source_files()` 从 `templates/hooks` 收集文件时只跳过 `tests/`、`__pycache__`、`.pytest_cache` 与 `.pyc`，于是把躺在顶层的 `conftest.py` 和 `pytest.ini` 一起算进了树摘要；但这两个文件是跑 hook 单元测试用的脚手架，部署到目标项目时从来不铺。白名单摘要按「含脚手架」算，项目实际树按「不含脚手架」算，两者永久对不上，而且项目再干净也无法自证清白。
- 这不是「有人改过 hook」。以 butler-radar 为例，它的 9 个 hook 文件与 v1.0.0 **逐字全等**、零项目独有文件，跟 v1.0.0 的唯一差别就是缺这两个脚手架文件。守门器把「部署时的合理裁剪」误判成了「内容被篡改」。
- 修复方向：让 `hook_source_files()` 与 `target_hook_files()` 同时排除 pytest 脚手架，使摘要口径回到「实际会铺到项目里的文件集」，再按新口径重算 `migrations/manifest.json` 的 `known_hook_tree_digests`。已用复算脚本验证：改后 6 个项目里 5 个立刻命中历史版本（butler-radar 对上 v1.0.0，butler-sticker 对上 v3.1.0，m5-sticks3-lab 对上 v1.6.0，ultra-learning 与 utopia 对上 v0.2.0）。
- 顺带发现白名单本身既不完整也不同口径：现有 7 个值只覆盖到 v2.17.0，缺 v2.18.0、v3.0.0、v3.1.0 三版的树。**修订（2026-07-29，P4 复算后）**：其中 `4ff6400939b6cabf…` 起初被判为来源不明，实为**新口径下** v2.2.0–v2.13.0 的摘要——旧白名单混了两种口径，v2.2.0–v2.13.0 这一段同时存在旧口径的 `99a64950…` 与新口径的 `4ff64009…`。最合理解释是当年已有项目撞过同一堵墙，有人把该项目实测摘要手工补进白名单救急而未追根因。这既是本缺陷早已发作的旁证，也说明打补丁的绕法不解决口径分叉。

## Scope

- 改 `tools/butler-upgrade/upgrade.py`：让 `hook_source_files()` 与 `target_hook_files()` 用同一份排除清单，把 pytest 脚手架排除在摘要之外。两个函数的过滤规则必须收敛到单一定义，不再各写一遍，否则同类错位还会再犯。
- 按新口径重算并替换 `migrations/manifest.json` 的 `known_hook_tree_digests`，补齐缺失版本，并对来源不明的那一项作出保留或移除的显式决定。
- 补机械测试锁定「部署会铺的文件集 == 参与摘要的文件集」这个不变量，让以后往 `templates/hooks` 加非部署文件时测试先红，而不是等某个项目升级时才炸。
- 不改 hook 自身的判定行为，不改任何被观测项目的文件，不动 `[split]` 与 `migrate_config` 的既有语义。
- 不在本迭代内执行 butler-radar 的升级；那是本迭代交付之后的独立动作。

## Open Questions / Risks

- 白名单里 `4ff6400939b6cabf…` 查不到对应版本。重算时若直接丢弃，万一某台机器上真存在与之匹配的项目就会突然失配；若原样保留，等于继续信任一个来源不明的值。倾向保留并加注释说明来源待考，但需在 P3 定夺。
- 改摘要口径会让全部历史白名单值一次性作废，必须与重算后的新值在同一次提交里落地。中间态（新代码配旧白名单）会把「全部失配」变成「依然全部失配」，虽不比现状更坏，但不能分两次发布。
- `claude-skills` 只有 1 个 hook 文件，新口径下仍失配。需先判断它究竟是不是 Butler 部署项目，再决定它是否属于本迭代要覆盖的情形。
- Active Profiles 段拒绝「名字 — 中文说明」这种人类写法，是同一次升级暴露的第二个缺陷（utopia 也中）。它的根因与本迭代不同，属独立需求，不合并进来。
- `tools/artifact-pipeline/artifacts.v1.json` 对 CONCEPT 的段落定义与 `concept-schema.md` 的散文模板不是一套，且它声明的 `templates/CONCEPT.md` 并不存在。属同类型的第三处机器与文档错位，本迭代只记录、不修。
