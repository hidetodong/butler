# 偏好探针参数

> 偏好探针的同意状态与可调参数。取得同意后首次采集时由引擎惰性拷贝到 `$BUTLER_PREF/config.md`（也可手动跑 `preference-init.sh`）。
> 本文件缺失时，引擎按以下默认值运行（见 `preference-probe-engine.md` §6.4）。

## 同意状态 (consent)

- `consent`: `unset`
  - `unset`：尚未询问——首次命中可采集决策时引擎全局问一次（见引擎 §2.4）。
  - `granted, YYYY-MM-DD`：已同意，采集默认常驻、不再询问。
  - `declined, YYYY-MM-DD`：已拒绝，采集保持关，直到用户主动 `/preference on`。

## 晋级

- `promotion_threshold`: `2`
  - 晋级为「跨项目通识」所需的**不同项目数**（≥）。单项目内重复不累加。

## confidence 口径

- `low`: 1 个项目背书
- `med`: 2 个不同项目背书
- `high`: ≥ 3 个不同项目背书且无跨情境矛盾

## 时效

- `stale_policy`: 连续相关决策长期未复现、或被近期反例覆盖即标 `stale` 降权。
- 跨情境出现矛盾时不降权而是**情境化拆分**（见引擎 §6.3）。

## 反哺

- `feedback_min_confidence`: `med`
  - 低于此置信度的偏好不得作为提议默认依据，仅可提示向用户澄清（见引擎 §3-4）。
