---
title: Butler 机器级安装命令
audience: AI / 开发者
scope: /butler:setup 与 $butler-setup 的触发、授权、路径解析和结果汇报
---

# Butler Setup

## 1. 职责边界

`/butler:setup` 与 `$butler-setup` 负责安装或刷新 Butler 的机器级能力：Claude 全局配置/命令、Codex plugin 和 Pi 扩展。安装算法只有一个真源：`scripts/setup.sh`；宿主入口不得复制、改写或逐步模拟脚本。

setup 不初始化当前项目，不升级项目 `.ai/`，也不替用户接受 Codex hook trust。项目首次部署走 `butler-init`，既有项目迁移走 `butler-upgrade`。

## 2. Butler 根解析

按以下顺序解析唯一 `BUTLER_PATH`：

1. 用户显式给出的 Butler 仓绝对路径；
2. 环境变量 `$BUTLER_PATH`；
3. 当前 Git 根本身同时含 `VERSION`、`Coder/README.md`、`scripts/setup.sh`；
4. 当前 skill/command 可证明来自仓库发现面时，沿真实路径回到包含上述三项的祖先目录。

候选必须是绝对、真实目录，且三项文件齐全；多候选不一致或无法证明时零写退出，请用户给出仓路径。不得从任意同名目录猜测。

## 3. 授权与执行

执行前回声 Butler 根，并亮明会修改用户级 shell/Claude 配置、个人 Codex plugin cache/marketplace，以及检测到 Pi 时的用户扩展软链。

- 用户显式输入 `/butler:setup`、`$butler-setup`，或明确说“现在安装/刷新 Butler”即视为本次机器级安装确认。
- 仅从“怎么安装”“能否 setup”等咨询语义触发时，只说明将执行的命令并等待确认，不能直接写用户目录。

确认后只执行：

```bash
bash "$BUTLER_PATH/scripts/setup.sh"
```

必须以独立 argv 调用，保留 stdout、stderr 与真实退出码；不得注入 `BUTLER_BYPASS`，不得在失败后自行改用户配置补救。

## 4. 结果汇报

- exit 0：按脚本输出分别报告 Claude、Codex、Pi 的 installed/refreshed/skipped 状态，并提醒重启终端或 source shell 配置、新开宿主会话；首次 Codex hook 仍需人工审阅信任。
- 非零：报告真实退出码和脚本已经完成/未开始的组件边界；不得概括成“安装成功”，也不得自动重跑。
- 完全空白机器还没有 Butler 命令发现面时，首次入口仍是 clone Butler 仓后运行 `bash scripts/setup.sh`；命令解决的是已发现 Butler 后的记忆负担，不伪装消除 bootstrap。
