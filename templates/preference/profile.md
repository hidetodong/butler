# 决策风格档案

> 由偏好探针蒸馏产出。真源为 `$BUTLER_PREF/signals/`（证据），本文件可被重新蒸馏。
> 字段定义见 `preference-probe-engine.md` §4.4。先验非权威：绝不覆盖用户当前显式指令。

## 通识层（跨项目，反哺真源）

<!--
scope = 跨项目通识；仅「跨情境 ≥ promotion_threshold 个不同项目一致复现」的偏好进入本区。
这是反哺（opt-in，仅有监督工作的 P2/P3 提案 / 选项排序）唯一读取的区域；`/dangerous` 完全不读。
首次蒸馏前为空，达标后由引擎写入。格式示例（删除注释后即为真实条目）：

- 陈述：倾向最小侵入式改动，而非大范围重构
  - scope: 跨项目通识
  - 适用范围: 架构
  - confidence: high
  - 背书: project-A / project-B / project-C（signals: A#12, B#7, C#3）
  - 状态: active（更新 2026-06-09）

- 陈述：取舍时可读性优先于物理归组
  - scope: 跨项目通识
  - 适用范围: 取舍
  - confidence: med
  - 背书: project-A / project-B（signals: A#5, B#11）
  - 状态: active（更新 2026-06-09）
-->

## 情境限定区（不跨项目反哺）

<!--
scope = 情境限定(条件: …)；只在命中其情境条件时可选参考，默认不参与跨项目反哺。
格式示例：

- 陈述：遗留目录放宽类型检查
  - scope: 情境限定(条件: 项目含 /legacy 旧代码)
  - 适用范围: 流程
  - confidence: low
  - 背书: project-A（signals: A#20）
  - 状态: active（更新 2026-06-09）
-->
