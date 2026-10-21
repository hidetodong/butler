# 把交付页渲染器搬进仓库并在 delivery-summary 里指明位置

候办键: delivery-renderer-in-repo
候办状态: deferred
规模: iteration

## 要解决什么

每个迭代收口都要把交付总结的 `.md` 渲染成固定格式的 HTML。模板 `templates/delivery.html.template` 是唯一真源，这一点 `Coder/20_Workflow_Lifecycle/delivery-summary.md §9` 写清楚了；但**渲染器本身不在仓库里**——它每次都是在会话临时目录里现写一个 `render_delivery.py`，会话一结束就没了。

后果有三条，都已经真实发生过：

- 每轮重写一遍渲染器，参数约定（三个位置参数：`<md> <template> <out>`）只能靠翻上一轮的会话记录才知道。
- 剥模板注释、检查未转换的裸 markdown 标记这些踩过的坑，没有代码承载，每次靠记忆或翻记忆库复现。
- `delivery-summary.md §9` 说了模板是真源，却没说渲染器在哪，读者按图索骥会找不到东西——规则在描述一个仓库里不存在的部件。

要做的事：把渲染器落进 `tools/` 下成为驻留工具（带 `README.md` 接入 OVERVIEW 的驻留工具清单、带测试接入 CI），把已知的坑写成测试用例，并在 `delivery-summary.md §9` 补一句它在哪、怎么调。

## 暂缓原因

当前 `MILE-0016`（Butler 瘦身与重造）与 `ITER-0118` 都是 active，按单 active 约束不能再开一个。本条是在 ITER-0118 的真实 dogfood 里用新命令记下来的，只入孵化区、本轮不开工。

捡回来的时机：MILE-0016 收口后。它跟 MILE-0016 的瘦身主题不冲突但也不同路——瘦身是在删东西，这条是在补一个本来就该有、却一直漏在会话临时目录里的部件。
