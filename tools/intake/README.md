# intake — 三层录入契约的写盘者

把「随手记一句 → 想清楚值不值得做 → 真的开工」这三层的全部文件读写收在一个确定性程序里。数据形态的真源是 `Coder/40_Context_Management/intake-schema.md`，动作边界的真源是 `Coder/40_Context_Management/intake-workflow.md`；本工具不重抄规则，只执行。

## 它做什么、不做什么

**做**：校验一步转移合不合法、把要写的内容全算出来、按计划落盘、失败时回滚。

**不做**：不替你判断「这条闪念该孵化还是该丢」。那个决定由命令层问过你之后，以已经定好的目标态传进来。所以 `handle` 这个动词更准确的读法是「执行一次已经定好的处置」。

## 三个子命令

所有子命令都必须给 `--project-root`，输出是一行 JSON，任何校验不过时**整次不落盘**并以非零码退出。`--date` 只在测试里用来固定时间，正常调用省略即取当天。

```bash
# 记一条闪念（闪念键形如 2026-08-20-ship-renderer）
python3 tools/intake/intake.py add --project-root . --text "把交付渲染器搬进仓库" --slug ship-renderer

# 只读地列出两层；--layer / --state / --scale 可筛
python3 tools/intake/intake.py list --project-root . --layer backlog --scale iteration

# 处置一条闪念：new → incubated | done | dropped
python3 tools/intake/intake.py handle --project-root . \
  --inbox 2026-08-20-ship-renderer --to incubated \
  --slug ship-renderer --scale iteration --title "把交付渲染器搬进仓库" --reason "当前 active 占着"

# 处置一份孵化区草稿：promote | iterate | withdraw
python3 tools/intake/intake.py handle --project-root . --backlog ship-renderer --exit iterate
```

`--text` 里没有 ASCII 字母数字时（比如纯中文），工具推不出 kebab 形态的键，会要求你显式给 `--slug`。它不做音译——猜出来的键不稳定，而键是要长期引用的。

## 关于「原子」的实话

一次 `handle --to incubated` 要动三处：回写闪念行、写草稿文件、在待办区追加索引行。跨文件做不到真正的原子，这里做的是**先算后写、失败即回滚**——先把每个目标文件的最终字节和原始字节全算出来，全部校验通过后按序写；任一步失败就把已经动过的按逆序还原。单个文件的那一次写用临时文件加 `os.replace`，它自己是原子的。

**这不等于数据库那种事务**：如果回滚过程本身也失败（磁盘满、权限变化），仍可能留下半截态。测试用注入写失败的方式覆盖了正常回滚路径，覆盖不了回滚自身失败。

## 测试

```bash
python3 -m unittest discover -s tools/intake/tests -t . -q
```

已接入 `scripts/verify-ci.sh`。
