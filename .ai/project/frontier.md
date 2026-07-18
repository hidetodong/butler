# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：v2.17.0；MILE-0007 的 R1–R5 已实现、验证、收口并聚合发布。
- **工程化加固**：安全安装、证据/状态审计、固定 CI 合同、可执行升级器与八工作流 registry 全部闭环；本地 Darwin/arm64 完整矩阵有机器证据。
- **双宿主治理**：33 个入口元数据投影由 registry 生成/校验；个人 Butler plugin 已刷新，team/public distribution 明确未配置。
- **远端保护**：workflow 尚未推送；required API 返回 403，当前私有仓库需升级 GitHub Pro 或改公开，状态为 `pending external capability`。

## 活跃战线

- MILE-0008“目标可信闭环”active；R1–R3 closed。Goal 不新增第二台账；派生六状态、完成候选、TECH_PLAN 四态 verdict、七项反证清单和共享 P4 写门已进入共同规则。
- 危险模式仍为 ON；R4 下一步把执行中新问题、假设失效、测试失败和审查发现回流到正确阶段。

## 下一个瓶颈

- Goal 闭环仍缺问题回流 action、机械完成裁决器和宿主投影；由 R4–R6 依序补齐。当前 hook 只验证显式 verdict，不证明自然语言方案绝对正确。
- 若要让 `Butler required checks` 成为远端合并门禁，需用户授权套餐/可见性变化，并在 workflow 推送后配置和核验保护规则。
- 可执行升级器仍缺一份真实外部老项目的受监督 dogfood；首次使用保留 backup/journal 并人工审阅 diff。
