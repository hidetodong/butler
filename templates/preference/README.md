# 偏好探针存储骨架

本目录是 `70_Extension_Preference/preference-probe-engine.md` 定义的**外置偏好存储**的初始骨架。

偏好数据**不存在 butler 仓库内**，而是落在仓库之外的 `$BUTLER_PREF`（默认 `~/.butler/preferences/`，路径发现见引擎 §4.1）。首次 `/preference on` 时，把本目录文件拷贝到该路径作为起点：

```
$BUTLER_PREF/
├── signals/                 # 证据真源（append-only，按项目分片）；参考 signals.example.md
├── profile.md               # 派生产物（通识层 + 情境限定区）
└── config.md                # 可调参数
```

- `config.md`：缺失时引擎按其内默认值运行（见引擎 §6.4）。
- `profile.md`：首次蒸馏前两区为空，达标后由引擎写入。
- `signals.example.md`：单条信号的格式示例，仅供参考，不拷入 `signals/`。

字段定义以 `preference-probe-engine.md` §4 为准，本骨架不重复定义、只给可落地的起点。
