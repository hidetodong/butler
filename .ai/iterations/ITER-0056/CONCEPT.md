# CONCEPT — ITER-0056 · 安装器事务安全

> 分流: 完整 | 命中升级信号: 多文件改动、关键路径、跨模块影响、设计取舍 | 2026-07-18

## 一句话

让 `setup.sh` 只修改它能明确认领、完整理解的用户配置；输入异常或目标归用户所有时宁可停下，也不能删内容、装错位置或假报成功。

## Goal

- G1：修复 Claude 全局配置只有一个残缺 marker 时，脚本会丢弃 marker 后用户内容的问题。
- G2：让 shell 配置只识别真正生效的 `BUTLER_PATH` export，不把注释或普通文本当成已配置。
- G3：让 Claude 命令命名空间只更新 Butler 自己的软链；真实目录或无关软链发生冲突时零破坏退出。
- G4：对每个用户文件采用“先校验起始态、再生成完整新内容、最后原子替换”的边界，并让日志准确反映成功、跳过、冲突或部分完成。
- G5：用隔离 HOME 自动化覆盖上述缺陷和原有幂等安装路径，防止以后回归。

## Current Understanding

- [scripts/setup.sh] 目前只要在 `~/.claude/CLAUDE.md` 找到任意一个 marker 就进入替换分支；单 marker 会让 `awk` 一直跳过到文件尾，已经在隔离 HOME 复现用户内容丢失。
- shell 配置目前用宽泛的 `grep 'BUTLER_PATH'` 判断是否已配置；注释里出现这个词时，后续 `sed` 没有匹配行，但脚本仍输出“已更新”。
- `ln -sfn SOURCE DEST` 遇到现存真实目录时，会把软链建到目录里面而不是接管 `DEST`；脚本随后仍输出“命名空间已安装”。
- `setup.sh` 同时处理 shell、Claude 配置、Claude 命令和 Codex plugin。R1 的“事务安全”按每个用户配置对象定义：单个对象失败不得留下半写内容；后续独立组件失败时如实报告部分完成，不承诺跨所有外部组件自动回滚。
- 任务属于 Bash/Python 辅助脚本与规则仓测试，不命中特定 Domain / Stack Profile。

## Constraints

- 不覆盖 marker 管理区外的 Claude 用户原文，不删除用户自有命令目录或无关软链。
- marker 数量/顺序异常、有效 export 多于一条、命令目标所有权不明时 fail-closed，并给出可执行的人工修复提示。
- 空 HOME 首装、重复运行、Butler 仓迁路径、无 Codex CLI 和有 Codex CLI 的现有成功路径必须保持。
- 不依赖 GNU-only 参数；至少兼容当前 macOS，并为 R3 的 Linux CI 留出可移植实现。
- 不借本迭代重构 plugin installer、公开 marketplace、迁移引擎或全仓 CI。
- 任何测试只使用隔离 HOME，不触碰真实 `~/.zshrc`、`~/.claude` 或已安装 plugin。

## Impact Scope

- 主要实现：`scripts/setup.sh`，必要时增加一个职责单一、标准库实现的配置更新 helper。
- 测试：`scripts/verify-dual-host.sh` 或拆出的 setup 专项测试，覆盖异常输入和原有成功路径。
- 说明：与安装冲突处理直接相关的 README/HUMAN_GUIDE/脚本输出；不扩写双宿主算法正文。
- 状态：本迭代四件套、台账、MILE-0007 R1 与对象级 changelog。
- 不影响：P1–P5 规则算法、项目根 resolver、renderer、hook rules、8 个工作流语义和历史迁移配方。

## Project Type / Active Profiles

- 项目类型：Markdown 规则仓 + Bash/Python 安装/验证工具。
- Active Profiles：无；仅按通用 SOP、实现纪律和测试策略推进。

## Open Questions

- 无阻塞问题。P2 采用默认边界：marker 只接受 0 个或完整一对；有效 `BUTLER_PATH` export 接受 0 或 1 条；命令目标只接受不存在或可证明为 Butler 所有的软链，其余情况拒绝修改。
- P3 需要在“纯 Bash 临时文件替换”和“小型标准库 helper”之间选最小且跨平台更可靠的方案，并明确文件权限保持方式。
