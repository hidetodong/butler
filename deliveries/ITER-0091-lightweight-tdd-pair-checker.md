# ITER-0091 · 轻量 TDD 配对合同与检查器

## 本次交付目标

让显式采用 TDD 的任务留下可机械复核的同命令 Red→Green 记录，而不是只靠 AI 口头声称。

## 已完成内容

- 在 `evidence.py` 增加只读 `check-tdd` 子命令，复用现有 evidence v1 record。
- TECH_PLAN 以版本化 marker 和固定表声明 cycle、AC、argv JSON 与 cwd。
- evidence ID 固定为 `tdd-<cycle>-red` / `tdd-<cycle>-green`。
- 21 个正负向场景覆盖缺边、outcome、顺序、命令/目录/AC 漂移、坏声明与归档复核。

## 关键变更 / 用户可感知变化

未声明 TDD 时行为不变；声明后，Red 必须失败、Green 必须通过，且两条记录的命令、目录和 AC 完全一致，顺序不合法就明确拒绝。

## 高层影响范围

verification evidence CLI、其测试与使用文档；R1 尚未接入 Goal/P5 自动收口门。

## 验证方式与结果摘要

专项测试 21/21 通过。首次完整 CI 因沙箱无法访问用户级 `uv` 缓存失败并保留诊断 evidence；同命令获宿主授权后 reproduced exit 0，200 个 hooks 与全部行为组通过。

## 已知剩余风险 / 延后事项

- 本轮由危险模式自主 ACK，P5 完整强审最终 Must Fix 0、Should Fix 0；未执行 fresh-context 独立复核。
- V1 不证明代码修改时序、Red 失败原因或测试未被弱化；这些增强已留在独立候办。

## 引用

- `.ai/iterations/ITER-0091/AC_LIST.md`
- `.ai/iterations/ITER-0091/TECH_PLAN.md`
- `.ai/iterations/ITER-0091/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0091/evidence/`
- `tools/verification-evidence/README.md`
