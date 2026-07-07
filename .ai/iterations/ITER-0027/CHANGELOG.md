> 吸纳最小实现纪律（ITER-0027）· closed · 2026-07-06

本文件是 ITER-0027 收口时归档的对象级变更流切片（ADD/EDIT/DELETE）。

## ADD

- `Coder/30_Quality_Gate/implementation-discipline.md` — 新建 P4 最小实现纪律：§1 定位（与 correction-contract 并列的常驻底线）+ §2 最小实现阶梯（YAGNI→复用→标准库→平台原生→已装依赖→一行→最小新代码，停在第一个成立的档，理解在前）+ §3 有意简化标记（`butler-min:` + 天花板/升级路径 + JS/Python 示例）+ §4 修根因不修症状（grep 全 caller / 守卫放共享函数一处）+ §5 何时不许偷懒（信任边界/防丢数据/安全/无障碍/用户明确要求 + 不对理解偷懒）+ §6 关系 → AC1 AC2 AC3 AC4 AC5

## EDIT

- `templates/rule-card.md 执行纪律` — 加一条压缩纪律 bullet（最小实现阶梯 + 简化标记 + 修根因 + 不许偷懒边界，指向 implementation-discipline.md、不重抄全文） → AC7
- `Coder/30_Quality_Gate/correction-contract.md §3` — 加第 5 条互引指针（修根因 / 最小改动定位 → implementation-discipline.md §4，并列不重叠） → AC7
- `Coder/README.md` — 目录结构树 + 目录说明（30_Quality_Gate 段）+ 分文件说明三处注册 `implementation-discipline.md` → AC6
- `.ai/PROJECT.md 现行约束` — 加"最小实现纪律"一条（收口前滚步④）

## DELETE

- 无
