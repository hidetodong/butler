---
状态: ack-frozen
ACK 日期: 2026-07-28
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0093

> ⚠️ 危险模式：本验收清单由模型完成反证、自洽性与可验证性审查后自主 ACK，未经用户确认（ITER-0093，2026-07-28）

## Goal

- 建立一个不依赖 Markdown 散文解析的项目级 Butler JSON 配置合同与统一读写内核，为后续迁移和全链路切换提供单一机器接口。

## In Scope

- JSON Schema、标准库 CLI/模块、默认配置、严格校验、原子写入、字段更新和正负向测试。

## Out of Scope

- 不迁移现有项目，不修改 `local-constraints.md`，不切换危险模式、独立复核、偏好或进度命令的现有读取位置。

## Acceptance Checklist

- [ ] AC1: schema v1 严格定义五个顶层字段，禁止额外字段，并约束三个布尔值与去重的非空 profile 字符串数组。
- [ ] AC2: `inspect` 能对合法配置输出稳定单 JSON；配置不存在时明确返回默认配置和 `missing` 来源，不把缺失当损坏。
- [ ] AC3: 已存在配置若 JSON 损坏、字段缺失、类型错误、schema 版本未知或含未知字段，必须非零退出并给出稳定诊断，不静默降级。
- [ ] AC4: `init` 只在文件不存在时原子生成规范默认配置，默认值为 dangerous=false、independent_review=false、preference=true、profiles=[]，不得覆盖已有文件。
- [ ] AC5: `set` 只允许修改三个布尔开关或完整 profiles 数组，写后重新校验，输出采用确定性格式并以原子替换落盘。
- [ ] AC6: 路径解析只接受显式 `--project-root`，拒绝越界、symlink 配置文件和非目录项目根；读取与校验保持零写。
- [ ] AC7: 专项测试覆盖正常、缺失、损坏、未知字段/版本、错误类型、幂等初始化、原子更新和路径安全；完整 CI 与 diff check 不回归。

## Verification Method

- AC1–AC6：`tools/project-config/tests/test_config.py` 以临时项目正负向验证 CLI 与模块合同。
- AC7：专项 pytest、artifact/state/handoff 审计、`scripts/verify-ci.sh` 与 `git diff --check`。

## External References

- N/A

## Open Questions / Risks

- N/A
