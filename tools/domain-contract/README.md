# domain-contract

Butler 高风险身份、状态与引用的**最小领域合同**。`domains.v1.json` 只登记导航元信息——概念身份、所属限界上下文、受控合同种类、唯一所有者与仓内执行真源——外加关系与文件级断言；`domain_contract.py check` 做 fail-closed 校验。

它是导航层，不是第二真源：**不得**复制 Dangerous/Loop 激活枚举、bridge manifest/results 字段全集、四态枚举或 artifact 算法；任何复制型载荷字段（如 `values` / `fields` / `enum`）都会被拒。

## 用法

```bash
python3 tools/domain-contract/domain_contract.py check --project-root .
```

- 退出码 `0`：注册表完整 + 关系无悬空 + 断言全部通过。
- 退出码 `1`：任一校验失败（重复 id / 重复所有者 / 未知上下文·种类 / 缺失或越界真源 / 复制型载荷 / 悬空引用 / 断言命中）。
- 退出码 `2`：注册表损坏或不可解析。

## 注册表 schema

- `contexts`：五限界上下文封闭枚举（与 `Coder/domain-model.md` 一致）。
- `contract_types`：受控合同种类封闭枚举（模式身份 / 状态枚举 / 结构所有权 / 桥输入输出 / 共享策略）。
- `entries[]`：每条含 `id`（稳定唯一）、`concept`、`context`、`type`、`owner`（唯一所有者，单个仓内路径）、`source`（执行真源，单个仓内路径）。未知字段 fail-closed。
- `relations[]`：`kind`（并列 / 共享策略）+ `left` / `right` 引用既有 entry id。
- `assertions[]`：`file` + `must_contain[]` / `must_not_contain[]`（子串）+ `reason`，把 Dangerous/Loop 错绑、人测段所有权等回归检查数据化。

## 自测

```bash
python3 -m unittest discover -s tools/domain-contract/tests
```

正负 fixture 覆盖：重复 id / 重复所有者 / 未知上下文·种类 / 缺失或越界真源 / 复制型载荷 / 悬空引用 / 旧包含措辞断言命中；每条负例断言命中**具体诊断**，不只看非零退出。
