# state-ledger

Butler 双台账的确定性热表与固定区间冷分片工具。身份至少四位，排序、最大号和路由都使用数字部分。

## 布局

- 根热表：`.ai/ITERATIONS.md`、`.ai/MILESTONES.md`，默认各保留最新 20 行。
- 冷分片：`.ai/history/iterations/ITER-000001-000050.md`、`.ai/history/milestones/MILE-000001-000050.md`，默认每个固定数字区间 50 个身份。
- 有界根索引：`.ai/state-index.json` schema v2，只保存最大号、计数和固定区间路由公式；分片增多不会向根索引追加逐片目录。
- 分片回执：每个 `.md` 冷片都有同名 `.json`，独立记录 start/end/path/count/SHA-256；定向读取时只需根索引、热表和命中的一对分片文件。
- 旧版兼容：迁移会读取 v1 的 `ITERATIONS.cold.md` / `MILESTONES.cold.md`，成功后事务删除。

固定数字区间意味着分片路径不会因新历史加入而重排；某区间中仍在热表的近期行不会重复写入冷片。

## 命令

```bash
python3 tools/state-ledger/state_ledger.py inspect --project-root .
python3 tools/state-ledger/state_ledger.py migrate --project-root .
python3 tools/state-ledger/state_ledger.py check --project-root .
python3 tools/state-ledger/state_ledger.py lookup ITER-0042 --project-root .
```

- `inspect`：只读计算目标索引。
- `migrate`：事务写热表、冷分片、分片回执和有界根 index，并移除被替代的受管旧文件；重复执行字节级幂等。
- `check`：读取全部分片，检查跨热/冷重复、格式、哈希、路由、孤立文件和上限。
- `lookup`：读取有界根 index 与热表；未命中时按公式只读取一个冷分片及其回执。found=0，not_found=1，坏输入或坏状态=2。

迁移不重编号、不改交付路径。路径越界、symlink、坏 UTF-8、重复身份或半迁移状态都 fail-closed。
