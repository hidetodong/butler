# 偏好探针参数

> 偏好探针的可调参数。首次 `/preference on` 时拷贝到 `$BUTLER_PREF/config.md`。
> 本文件缺失时，引擎按以下默认值运行（见 `preference-probe-engine.md` §6.4）。

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
  - 低于此置信度的偏好不得作为无监督自决依据，仅可提示向用户澄清（见引擎 §3-4）。
