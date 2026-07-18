# 01_CHANGELOG — ITER-0060

## ADD

- `workflows/registry.json`：新增八工作流与 plugin/distribution 的机器元数据真源，登记双宿主名称/路径、风险、隐式策略、语义触发和 legacy aliases。→ AC1、AC3、AC5、AC6
- `scripts/sync-workflow-registry.py`：新增严格 schema/set/plugin/doc 校验、33 个投影、原子 `--write`、零写入 `--check` 与失败回滚。→ AC1–AC6
- `scripts/test-workflow-registry.py`：新增 8 组 registry/projection/plugin 漂移、幂等、零写入与回滚测试。→ AC1–AC7
- `docs/workflows.md`：新增由 registry 生成的唯一八项人读能力与分发状态表。→ AC5、AC6

## EDIT

- `plugins/butler/skills/butler-{prd,review,milestone,upgrade,ideation,preference}/agents/openai.yaml`：普通工作流显式生成 `allow_implicit_invocation: true`，与高风险 false 形成闭合集合。→ AC3、AC4
- `README.md`、`HUMAN_GUIDE.md`、`docs/codex-compatibility.md`、`Coder/README.md`：移除重复八项入口枚举或增加指针，统一路由生成表。→ AC6
- `scripts/verify-dual-host.sh`：把 registry 专项、`--check` 和编译检查接入唯一 CI/local 矩阵。→ AC7
- `tools/verification-evidence/evidence.py`、`README.md`、`test_evidence.py`：新增显式 `--allow-closed`，仅在 `current: none` 且目标行 closed 时允许补捕获/移动最终状态审计证据，默认闸不放宽。→ AC8
- `scripts/audit-project-state.py`、`test-audit-project-state.py`：发布对账从“tag 名存在”收紧为当前 VERSION tag 必须指向 HEAD；干净但领先 tag 的提交仍亮 `UNRELEASED`。→ AC8
- `.ai/AC_LIST.md`、`.ai/TECH_PLAN.md`、`.ai/VERIFY_REPORT.md`：冻结、自主执行并以机器 evidence 逐 AC 收口。→ AC8

## DELETE

- 四份人读入口中的重复完整能力清单不再作为维护真源；legacy alias 仅登记，不删除兼容识别元数据。→ AC6
