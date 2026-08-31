# Task State

- 当前迭代：无 active
- 当前里程碑：MILE-0016
- 阶段：ITER-0119 已收口（2026-08-21），等待开启下一迭代
- 状态：旧 inbox 全链已删净——两份规则真源 `inbox-schema.md` / `inbox-workflow.md`、整个 `tools/inbox/`、合同测试 `test_inbox_contract.py` 与 CI 里那行调用全部消失，`test_inbox_workflow.py` 只剩两个活接线用例，`test_mile0009_e2e.py` 摘掉了头上那段 inbox scan。`origin/` 退出活跃面、原件改放 `.ai/references/raw/`：`references-schema.md` §1/§2 重写成三类资料并点破「引用 references 不等于引用权威投影」，部署协议、里程碑 brief 三处通道、两个命令薄壳、skill、rule-card、README、HUMAN_GUIDE、prd-migration-guide、三份测试夹具与 `.ai/invariants.md` 第 48 条同批改完。新增 `TestLegacyInboxIsRefusedNotRewritten` 四个用例锁死「碰到旧格式一律拒绝且零写入」。`debt.md` 清账（删 1 改 1 增 2 共 15 条）、§5.4 补 5 条、OVERVIEW 已重算（规则 13→11、工具清单去掉 inbox）。CI 退出码 0；AC9 的红绿演示已现场做过（删掉纪律那句 → 1 failed，还原 → 6 passed）。
- 下一动作：MILE-0016 下一条路线 R9（根布局整理：`.ai/milestone-backlog/` 改名 `.ai/backlog/`、`deliveries/` 迁入 `.ai/`）。本轮欠下的两笔分别指向「下次切版之后的任意一轮」（原件只读 hook 门禁）与 R14 / R15（已部署项目残留 `origin/` 与旧格式 `.ai/INBOX.md`）。不切版、不提交、不打 tag 仍然有效。

# Goal Calibration

- 当前无未闭合运行时信号（N/A）。
