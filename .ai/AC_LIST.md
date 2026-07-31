---
状态: ack-frozen
ACK 日期: 2026-07-31
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0098

## Goal

- 补齐 Butler 的开源授权、零基础使用和社区协作入口，让陌生用户不读仓库内部实现也能判断项目用途、完成安装、验证结果并找到正确的反馈渠道。

## In Scope

- 根级 `LICENSE`、`CONTRIBUTING.md`、`SECURITY.md`。
- README 的目录、获取与安装、前置条件、安装影响、成功验证、支持/维护、贡献、安全、许可证、健康状态徽章和最小成果示例。
- 所有新增入口使用仓库内相对链接，并纳入现有 Markdown 链接检查与完整 CI。

## Out of Scope

- 不新增行为准则，不承诺尚未建立的社区执法机制。
- 不增加中英文双语 README。
- 不修改安装脚本、Butler 规则算法、Hooks、plugin、迁移配方或 GitHub 仓库设置。
- 不回溯改写历史交付与历史版本说明。

## Acceptance Checklist

- [ ] AC1: 根目录存在用户确认的标准开源许可证全文；README 末尾写明 SPDX 标识、版权归属并链接该文件，且不把第三方子目录许可证误写成全仓许可证。
- [ ] AC2: `CONTRIBUTING.md` 说明接受哪些贡献、如何提 Issue/PR、本地前置条件、修改边界、必跑验证和行为预期；README 提供清晰入口。
- [ ] AC3: `SECURITY.md` 说明受支持版本、私密漏洞报告渠道、禁止公开披露的边界和响应流程；README 的安全章节只做摘要并链接全文。
- [ ] AC4: README 的快速开始覆盖前置条件、官方仓库获取、`setup.sh` 的主要用户级写入影响、安装命令、重启/生效方式和成功验证，不要求读者先翻 `HUMAN_GUIDE.md` 才能完成首次使用。
- [ ] AC5: README 增加覆盖全部二级标题的目录；顶部徽章收敛为 CI、版本、许可证和宿主支持等可判断状态，静态版本与仓库 `VERSION` 保持一致。
- [ ] AC6: README 给出一个最小任务输入及其可预期产物/确认点，让读者在一分钟内理解 Butler 的实际使用结果；详细能力清单和深层说明仍通过现有文档下沉。
- [ ] AC7: README 明确普通支持、维护者、贡献、安全和许可证入口；所有仓库内 Markdown 链接通过离线检查，`git diff --check` 与完整 `bash scripts/verify-ci.sh` 通过。

## Verification Method

- AC1: 核对根级许可证为所选标准文本；检查 README SPDX 标识、版权归属和相对链接；确认第三方许可证仍局限在其子目录。
- AC2: 按“贡献类型 → Issue/PR → 本地准备 → 验证 → 提交”路径人工走读；核对文中命令与仓库现有入口一致。
- AC3: 核对支持版本表、私密报告渠道、公开披露限制和维护者响应步骤齐全；若渠道依赖外部设置，明确写出启用前提。
- AC4: 从空白读者视角按 README 命令顺序检查 clone、依赖、安装、生效和验证链路；对照 `scripts/setup.sh` 确认主要副作用没有遗漏或夸大。
- AC5: 提取 README 二级标题与目录逐项对账；核对版本徽章与 `VERSION`；检查徽章目标链接可解释且没有重复装饰性信息。
- AC6: 人工走读最小示例，确认输入、P2/P3 确认和最终 `.ai/`/`deliveries/` 结果首尾相接。
- AC7: 运行 `python3 scripts/check-markdown-links.py --root .`、`git diff --check` 与 `bash scripts/verify-ci.sh`，并用 evidence record 逐项绑定 AC。

## External References

- [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) — README 常见信息与相对链接口径，支撑 AC4、AC7。
- [GitHub Community Profiles](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories) — LICENSE、CONTRIBUTING、CODE_OF_CONDUCT 和 SECURITY 等社区健康入口，支撑 AC1–AC3。
- [Open Source Guides: Starting a Project](https://opensource.guide/starting-a-project/) — 开源项目启动清单，支撑 AC1–AC3。
- [Standard Readme specification](https://github.com/RichardLitt/standard-readme/blob/main/spec.md) — 长 README 目录、安装、使用、贡献和许可证章节口径，支撑 AC1、AC2、AC4–AC7。

## Open Questions / Risks

- 2026-07-31 用户已 ACK：Apache-2.0；接受 GitHub Issues 和 Pull Requests；普通支持走 GitHub Issues；安全问题走 GitHub Private Vulnerability Reporting；维护者写 `@hidetodong`。
- `ego-browser` 能创建 GitHub 标签页但无法附着活动标签，未能只读确认私密漏洞报告入口是否已开启。AC3 不会假称外部设置已就绪；若 P4/P5 仍无法核实，须作为外部待办和剩余风险明确交付。
- 外部规范是参考基线，不把 Standard Readme 的英文标题或固定章节顺序机械照搬到中文 README；以首次使用和社区协作是否闭环为最终判断。
