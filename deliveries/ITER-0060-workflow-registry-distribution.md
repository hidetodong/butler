# ITER-0060 · 双宿主工作流注册与分发收敛

> 迭代交付（小版本） · 2026-07-18 · MILE-0007 R5 · 危险模式自主 ACK / 完整审查

## 本次交付目标

把八个 Butler 工作流在 Claude、Codex、仓内发现、plugin 和文档里的入口元数据收成一份机器登记表，让 CI 自动拦住漏同步，尤其锁死高风险工作流不得隐式触发。

## 已完成内容

- 新增 `workflows/registry.json`，统一名称、路径、规则真源、风险、隐式策略、触发、旧名与分发状态。
- 新增标准库同步器，管理 33 个窄投影；`--write` 原子、可回滚且幂等，`--check` 零写入。
- 新增 8 组专项，覆盖 schema、路径逃逸、正文保护、软链、hooks、installer、distribution、漂移与失败恢复。
- 生成唯一人读表 `docs/workflows.md`，四份入口文档改为链接，不再各自维护完整八项清单。
- 注册表专项与检查接入唯一 CI/local 矩阵；个人 Butler plugin 按官方 cachebuster/install 链刷新。
- 证据工具补 `--allow-closed` 窄口：只允许 `current: none` 的已关闭迭代捕获最终状态审计，闭环 AC8 而不放宽默认 current 闸。
- 状态审计器补 VERSION tag→HEAD 对账：工作树即使干净，只要当前提交领先发布 tag，仍明确标成 `UNRELEASED`。

## 关键变更 / 用户可感知变化

- 普通六项与高风险两项现在都显式写 `allow_implicit_invocation`，不再依赖宿主缺省值。
- `/loop` 等旧名只登记兼容/碰撞状态，不会重新生成危险实体入口。
- 改 registry 后运行一次 `--write`；忘记同步 command、skill、YAML、软链、hooks 或人读表时，`--check`/CI 会给出具体漂移路径。
- 个人 plugin 可安装已验证；团队/公共分发明确标成未配置，不会把本机状态冒充组织能力。

## 高层影响范围

- 新增 registry、同步器、专项与生成文档；更新六份普通 workflow YAML、四份入口文档和完整验证矩阵。
- command/SKILL 正文、Coder 工作流算法、P1–P5 与升级事务没有改变。
- 源码 plugin 版本保持与 `VERSION` 精确一致；只有安装副本带 cachebuster。

## 验证方式与结果摘要

- `workflow-registry-tests-closure`：8/8，覆盖 AC1–AC8 的正常、漂移、安全和恢复路径。
- `full-matrix-closure`：固定 Python 3.12.12 / uv 0.9.28 下完整矩阵通过，含官方 plugin/8 skill validators 和 127 hook tests。
- 首次裸系统 Python validator 因缺 PyYAML 失败，record 保留；随后由固定 uv 入口 reproduced 通过。
- 强复核发现并修复 hooks 命令尾缀校验过宽；最终 Must Fix 0、Should Fix 0。

## 已知剩余风险 / 延后事项

- 团队/公共 marketplace 尚未配置；真实 GitHub 双系统运行和 required check 仍是外部 pending。
- 同步器只管理元数据，不替代对工作流正文语义的审查。
- 裸系统 Python 不保证具备 validator 依赖，完整验证必须使用 `bash scripts/verify-ci.sh`。

## 引用（只引用，不嵌入）

- `.ai/iterations/ITER-0060/AC_LIST.md`
- `.ai/iterations/ITER-0060/TECH_PLAN.md`
- `.ai/iterations/ITER-0060/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0060/evidence/`
- `workflows/registry.json`
- `docs/workflows.md`
- checkpoint `f0f8c98`
