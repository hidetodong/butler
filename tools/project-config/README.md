# project-config

项目级 Butler 机器配置的严格读写内核。配置固定落在显式项目根的 `.ai/butler.config.json`，第一版使用顶层扁平字段。

```json
{
  "schema_version": 1,
  "dangerous": false,
  "independent_review": false,
  "preference": true,
  "profiles": []
}
```

## 命令

```bash
python3 tools/project-config/config.py inspect --project-root <PROJECT_ROOT>
python3 tools/project-config/config.py resolve --project-root <PROJECT_ROOT>
python3 tools/project-config/config.py init --project-root <PROJECT_ROOT>
python3 tools/project-config/config.py set dangerous true --project-root <PROJECT_ROOT>
python3 tools/project-config/config.py set profiles '["typescript-rules"]' --project-root <PROJECT_ROOT>
```

- `inspect`：只读。文件缺失时返回默认配置和 `source: missing`，但不写盘；文件存在却非法时 fail-closed。
- `resolve`：兼容期只读入口。JSON 存在时以它为真源并在 `legacy_conflicts` 列出与旧 Markdown 的冲突；JSON 缺失时回退 `.ai/local-constraints.md`，两者都没有机器配置时返回默认值。
- `init`：只在文件缺失时原子创建，拒绝覆盖。
- `set`：只修改三个布尔开关或完整 `profiles` 数组，写前后都执行严格校验。
- stdout 始终为单个 JSON；退出码 `0` 表示成功，`1` 表示安全冲突，`2` 表示坏输入或坏状态。

字段合同以 `butler-config.schema.json` 为真源；运行时校验与 schema 由测试机械对账。

## Legacy 迁移

`parse_legacy` / `plan_migration` 是供 `butler-upgrade` 调用的纯函数：确定性提取旧「Active Profiles」「Butler 功能开关」和 `Review Policy`，生成 JSON bytes，并从 Markdown 中只移除这些机器配置段。模糊 profile、非法开关、重复段、坏 UTF-8、损坏/冲突 JSON 或 symlink 一律首写前拒绝。

双文件提交不由本工具另造事务；升级器的 `migrate_config` action 把 JSON 与收窄后的 Markdown 放进既有 backup/restore/journal。真实版本链 action 在对应发布迁移中登记。

## 消费端合同

- 活规则、Claude 命令与 Codex skills 读取配置时只调用 `resolve`，不得复制 JSON/Markdown parser。非零退出、坏 stdout 或 `status != ok` 一律 fail-closed；`legacy_conflicts` 必须显式报告。
- 回写只调用 `set`，且只有 `resolve.source == "config"` 时允许。`legacy` 先运行 Butler upgrade，`missing` 先 init；消费端不得直接改 `.ai/local-constraints.md`，也不得用默认值覆盖旧配置。
- 进度报告复用一次 resolve 结果，展示 source、冲突、三开关与 profiles；版本从项目入口 managed stamp 或 `VERSION` 读取，配置文件不承载 Butler 版本。
