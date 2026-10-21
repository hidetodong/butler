# Butler 开源就绪：补齐授权、安装、贡献与安全入口

## 本次交付目标

Butler 原来的 README 已能讲清项目定位、P1–P5 工作方式和主要能力，但缺少许可证、贡献指南、安全报告渠道和完整的零基础安装路径。公开可读不等于开源可用：没有授权和协作入口，外部用户仍不知道能否合法修改、如何贡献，也无法安全报告漏洞。

本次把这些基础入口一次补齐，让陌生用户能从 README 判断用途、完成安装、验证结果，并找到普通支持、贡献和安全问题各自对应的渠道。

## 已完成内容

- 新增根级 `LICENSE`，采用用户确认的 Apache License 2.0，版权归属为 `© 2026 hidetodong`；第三方子目录许可证继续独立生效。
- 新增 `CONTRIBUTING.md`，说明可贡献内容、Issue/PR 流程、固定开发工具链、完整 CI 和改动边界。
- 新增 `SECURITY.md`，说明支持版本、GitHub 私密漏洞报告、禁止公开披露和协调处理流程。
- 重构 `README.md`：补全目录、Git/Bash/Python 3 前置条件、官方 clone、机器级写入影响、安装生效与成功验证，并增加一分钟使用示例。
- 顶部徽章从五个静态描述收敛为 CI、版本、许可证和宿主支持四类可判断状态；README 末尾新增支持、贡献、安全和许可证入口。

## 关键变更 / 用户可感知变化

- 第一次接触 Butler 的人不再需要猜仓库地址或先翻长指南：README 已给出从 clone 到看到 `Butler ready` 的完整最短路径。
- 安装命令执行前就能看到它会修改哪些用户级配置，以及 Claude Code、Codex、Pi 分别会安装什么。
- 外部用户现在有明确的 Issue、Pull Request 和私密漏洞报告路径，仓库也有可识别的 Apache-2.0 授权。
- Butler 的 P1–P5 规则算法、安装脚本行为、Hooks、plugin、迁移配方和已部署项目结构均未改变。

## 高层影响范围

公开内容改动只涉及仓根 `README.md`，并新增 `LICENSE`、`CONTRIBUTING.md`、`SECURITY.md`。流程产物和证据归档在 `.ai/iterations/ITER-0098/`。

本迭代没有修改 GitHub 仓库设置，也没有新增行为准则、Issue/PR 模板或中英文双语 README；这些属于后续治理或维护选择，不在本轮范围内。

对象级变更见 `.ai/iterations/ITER-0098/CHANGELOG.md`。

## 验证方式与结果摘要

五条 evidence record 已归档，其中最终绿色证据覆盖 AC1–AC7：

- `readme-open-source-readiness`：确定性检查许可证关键结构、贡献/安全内容、README 目录与 H2 一致性、安装链路、最小示例和 SPDX 标识。
- `repository-doc-checks`：仓库内 809 个 Markdown 文件、68 个链接全部通过，`git diff --check` 通过。
- `full-ci-final`：完整 `bash scripts/verify-ci.sh` 通过。此前两次失败也保留：一次是沙箱不能访问 uv 用户缓存，一次是 `task-state` 固定 N/A 句式被改写；修正后最终全绿。

AC3 与 AC6 标为弱验证：前者未能读取 GitHub 私密漏洞开关状态，后者包含同上下文可读性走查。其余 AC 为可靠自动道。

## 已知剩余风险 / 延后事项

- GitHub Private Vulnerability Reporting 是否已启用尚未核实。`SECURITY.md` 已说明按钮不可见时不要公开披露，并先请求私密联系渠道；仓库管理员仍应到 GitHub Security 设置确认开关。
- Apache-2.0 与 `hidetodong` 版权主体由用户 ACK，未经过公司法务复核；机器验证不能替代知识产权判断。
- 本次是同上下文 P5 简评，项目配置未开启独立复核。
- `CODE_OF_CONDUCT.md` 和中英文双语 README 明确后置：前者需要真实的社区执行责任，后者会引入长期同步成本。

## 引用

- 验收清单：`.ai/iterations/ITER-0098/AC_LIST.md`
- 技术方案：`.ai/iterations/ITER-0098/TECH_PLAN.md`
- 验证报告：`.ai/iterations/ITER-0098/VERIFY_REPORT.md`
- 对象级变更流：`.ai/iterations/ITER-0098/CHANGELOG.md`
- 证据目录：`.ai/iterations/ITER-0098/evidence/`
