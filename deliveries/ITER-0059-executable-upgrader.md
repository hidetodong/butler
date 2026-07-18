# ITER-0059 · 可执行升级器交付总结

> 迭代交付（小版本） · 2026-07-18 · 危险模式自主 ACK / 完整审查

## 本次交付目标

把 Butler 已部署项目升级从“模型解释 Markdown 后手工执行”改成确定性程序：先给零写入计划，再在明确边界内事务执行，冲突不覆盖、失败可恢复、结果可复跑并有机器证据。

## 已完成内容

- 建立 `migrations/manifest.json` 连续机器台账，覆盖 v1.0.0→v2.16.0 的 26 个发布区间，action 的 ID、type、domain、parameters、preconditions 均可校验。
- 新增 `tools/butler-upgrade/upgrade.py`，提供 inspect/plan/apply/global-install；项目 apply 带 before hash、lock、backup、restore manifest、journal 和失败恢复。
- 双入口、hook/settings、rename/add-field、restamp/no-op 均有限动作化；split、无戳 bootstrap、HOME 安装保持明确人工/外部边界。
- Claude `/butler:upgrade` 与 Codex `$butler-upgrade` 已收薄到同一 CLI；历史 recipe 结构与人类文档同步。
- 升级专项接入唯一 CI/local 矩阵，危险模式完整审查发现的问题均已修复并复现关闭。

## 关键变更 / 用户可感知变化

- 运行升级会先看到结构化版本队列、逐文件变化、冲突和机器级待办；dry-run 不写项目或 HOME。
- 项目升级必须显式 apply。发生写入故障会恢复已触及文件，不再依靠操作者手工 `git reset`。
- `[split]` 可以明确暂缓；选择现在迁时，程序诚实停在语义交接点，不粗暴拆用户知识。
- `[global-install]` 单独确认、单独报告；项目成功不会把未执行的 HOME 动作伪装成完成。

## 高层影响范围

- 新增机器台账和驻留升级器：`migrations/manifest.json`、`tools/butler-upgrade/`。
- 更新升级规则、MCV/migration schema、两宿主入口、历史 recipe 和使用文档。
- 新增 16 项升级器专项，并接入 `scripts/verify-dual-host.sh` / `verify-ci.sh`。
- 不改业务工作流算法，不自动改 `origin/`、deliveries、历史归档或任意用户知识语义。

## 验证方式与结果摘要

- 最终 `upgrade-tests-final`：16/16，覆盖 CLI JSON 零写入、历史跨版、幂等、protected path、marker/hook/current drift、split/global、TOCTOU、锁和两类故障恢复。
- 最终 `upgrade-full-matrix-final`：固定工具链下完整双宿主矩阵通过，含 8 skills 官方校验与 127 hook tests。
- `review-upgrade-safety`、`review-manifest-current-drift`：风险相关命令由复核步骤重新执行并生成 reproduced record。
- 首次失败的 `state-audit-active` 保留；修复后 3 份状态审计连续通过。完整索引见归档 VERIFY 与 `.ai/iterations/ITER-0059/evidence/`。

## 已知剩余风险 / 延后事项

- semantic split 仍需有人处理；这是防内容损失的设计边界。
- HOME 全局安装不属于项目事务，需单独显式确认。
- `SIGKILL` 遗留 lock 需按 journal/restore/backup 人工审阅后处理。
- workflow 尚未推送，真实 GitHub Linux/macOS run 和 required check 仍受 R3 已记录的远端套餐/可见性限制。

## 引用（只引用，不嵌入）

- `.ai/iterations/ITER-0059/AC_LIST.md`
- `.ai/iterations/ITER-0059/TECH_PLAN.md`
- `.ai/iterations/ITER-0059/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0059/evidence/`
- `tools/butler-upgrade/README.md`
- checkpoint `c061209`
