---
description: 偏好探针开关——留空看当前状态；on/off 隐私总开关；reback on/off 开关反哺；distill 手动蒸馏（实验性，数据存 butler 仓库之外）
argument-hint: "[留空=看状态 | on | off | reback on | reback off | distill]"
---

你正在操作 butler 的 **偏好探针开关**。本命令是**薄壳路由器**——只做三件事：① 保证把对的规则读进上下文，② 按参数分派到对的开关动作，③ 委托真源执行并回声状态。**同意协议、采集 / 蒸馏 / 反哺算法、安全底线、外置存储契约一律以被指向的规则文件为准，本文件不复述**（守 butler DRY 红线）。

> **路径约定（本命令可在任意项目里运行，当前目录不一定是 butler 仓）**：下文引用的 `Coder/…` 都是 **butler 规则仓库**里的文件，一律相对 `$BUTLER_PATH`（`setup.sh` 全局安装时写入的环境变量）解析。偏好数据一律落**外置存储** `$PREF`（`$BUTLER_PREF` 或默认 `~/.butler/preferences/`，路径发现见引擎 §4.1），**绝不写当前项目的 `.ai/`、也绝不写 butler 仓**。

> **项目根硬门**：全局 `$PREF` 操作不依赖项目根；但一旦要读项目抑制开关，必须先按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1` 解析 `PROJECT_ROOT`。无法唯一解析时回报“项目抑制态不适用”，不从 `cwd` 猜测。

## 第 0 步 先认清这是实验性、数据在仓库之外
偏好探针是**实验性**能力：它把你的决策取舍抽象记到**外置存储** `$PREF`、蒸馏成跨项目通识、opt-in 反哺到有监督提议。开关（`on`/`off`/`reback`）是**全局**的，任何项目里都能敲、**不强依赖当前项目 `.ai/`**；`distill` 只在有采集到的信号时才有东西可蒸。
- 读得到 `Coder/70_Extension_Preference/preference-probe-engine.md`（butler 可达）→ 正常往下走。
- 读不到（当前环境没接 butler、`$BUTLER_PATH` 未设）→ 一句话告诉用户「偏好探针是 butler 能力，需先全局安装 butler（`setup.sh`）」。**不报错、不空跑。**

## 按 `$ARGUMENTS` 路由
先读 `Coder/70_Extension_Preference/preference-probe-engine.md`——所有分支的公共真源（§2 开关语义、§3 安全底线、§4 存储契约、§5–§8 采集/蒸馏/反哺/隔离）。取 `$ARGUMENTS` 的**首 token** 分派；首 token 是 `reback` 时**再看第二 token**。

**分支 空 ── 留空 → 只读状态回声**
不改任何开关。按 §4.2 存储布局**只读** `$PREF/config.md`，回报三件事的当前态：① 隐私总开关（consent：granted / declined / 未记）、② 反哺 `reback` 开 / 关、③ 当前项目抑制态（读本项目 `.ai/local-constraints.md`「Butler 功能开关」`preference`，缺则视为 `on`；没有 `.ai/` 就说不适用）。**只读、不写 `$PREF`、不写 `.ai/`。**

**分支 on / off ── 隐私总开关**
委托 §2.3：`off`=停采集+蒸馏+反哺、保留已存数据；`on`=恢复默认（数据回路开、反哺关）。**首次 `on`**（`$PREF/config.md` 无 `consent` 记录、且在托管项目命中可采集点）按 §2.4 一次性同意协议走——**披露记什么/存哪/怎么关、先问后写**，本文件不复述该协议，照真源执行。

**分支 reback on / reback off ── 影响回路（反哺）开关**
委托 §2.2 + §7：`reback on` 开启后，仅在**有监督**决策（P2/P3 提案、选项排序）把画像作参考、绝不替你 ACK、绝不参与 `/dangerous`；默认关。第二 token 只认 `on`/`off`。

**分支 distill ── 手动蒸馏 + 维护**
委托 §6：把 `signals/` 归纳为偏好、跨情境背书核验、晋级/降级维护。这是 §8 允许的安全边界触发点之一；蒸馏读 signals、写 `profile.md`，仍不碰 `.ai/`。

**兜底 裸 reback（无第二 token）** → 不误动开关：回声当前 reback 态 + 提示补 `on` 或 `off`。
**兜底 未知参数** → 提示合法参数集（留空 / `on` / `off` / `reback on` / `reback off` / `distill`），不瞎猜执行。

## 收尾
任何开关变更后，**当回合**用一句话显式回声当前状态（§2.3 硬要求）：现在隐私总开关、反哺各是开还是关。只读分支则直接把查到的状态报给用户。
