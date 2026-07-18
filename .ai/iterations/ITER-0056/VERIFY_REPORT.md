# Verification Summary

- 覆盖全局 Claude 配置、shell export、命令软链、setup 编排、隔离 HOME 回归和全仓双宿主矩阵。
- AC1–AC8 全部通过；P5 完整审查发现的 2 个 Must Fix（计划后状态竞态、CRLF 用户字节漂移）均已修复，定点复查与全量复查通过。

# AC Status（道 + 置信档合并标记）

- [x] AC1 (auto·可靠) ✓ marker 为 0/2 时安全写入，单个、重复和内联 marker 均被确定性拒绝。
- [x] AC2 (auto·可靠) ✓ 管理区前后用户字节、CRLF、无尾换行和文件 mode 均有断言，重复运行不漂移。
- [x] AC3 (auto·可靠) ✓ 0/1/多条 export、注释伪命中、路径 quoting 和 mode 均有隔离断言。
- [x] AC4 (auto·可靠) ✓ 当前/旧 Butler 软链可保持或迁移，真实目录、无关与不可认领断链均拒绝且目标树不变。
- [x] AC5 (auto·可靠) ✓ plan 后状态变化会在暂存前及提交前复核；文件/软链同目录暂存并原子替换，plugin 失败只报告部分完成。
- [x] AC6 (auto·可靠) ✓ 三个原始缺陷均进入 16 项专项回归并断言零意外变化。
- [x] AC7 (auto·可靠) ✓ 空环境、重复安装、旧仓迁移、无/fake/失败 Codex 均在临时 HOME 验证。
- [x] AC8 (auto·可靠) ✓ 完整矩阵、语法/编译、plugin validator、diff whitespace 和人读冲突说明均通过。

# Verification Results

- `python3 scripts/test-configure-global-install.py`：16 tests passed。
- `bash scripts/verify-dual-host.sh`：renderer 8 tests、resolver 7 tests、global installer 16 tests、Codex R1/R2、hook wrapper、127 个 pytest、plugin validator 全绿。
- `python3 -m py_compile scripts/configure-global-install.py scripts/test-configure-global-install.py`：通过。
- `bash -n scripts/setup.sh scripts/verify-dual-host.sh`：通过。
- `git diff --check`：通过。
- 测试均使用临时 HOME；未读写真实用户 HOME。

# Gate Coverage

- 通用质量门禁：逻辑边界、用户数据保护、命令注入、权限保持、资源清理、幂等、失败回声、shell syntax、Python compile 与全仓回归均检查。
- Active Profiles：无。
- Tech Plan Alignment：T1–T5 全部兑现；helper 负责 plan/apply，`setup.sh` 保持薄编排，plugin 仍是独立组件，未越界改 renderer/hook/workflow 算法。
- References Compliance：N/A；本迭代未使用 `.ai/references/` 外部规格。

# Independent Review

- 未执行 fresh-context 独立复核；本轮执行的是主 agent 同上下文完整多维审查，不冒称独立。
- 完整审查结论：初审 2 个 Must Fix、0 个 Should Fix；两项修复后复审 0 个 Must Fix、0 个 Should Fix。

# Remaining Risks

- 多个用户对象之间仍不是文件系统级 ACID 事务；apply 中途发生真实 I/O 故障时保留已完成对象并如实回声，这是冻结范围内的明确边界。
- 无法证明归属的历史断链必须人工处理；这是避免误接管用户路径的 fail-closed 成本。

# Handoff / Next Step

- ITER-0056 可收口归档；MILE-0007 下一条路线是 R2“状态审计与收口一致性”。
