> ITER-0038 · MILE-0004 R3 · 首切入口并进 /milestone + 两海拔交叉指针 · 收口即归档

本文件是**当前活跃迭代**的对象级变更流（ADD/EDIT/DELETE）。收口时归档至 `iterations/ITER-0038/CHANGELOG.md`。

## ADD

- 无（本轮为接线，无新文件）

## EDIT

- `Coder/20_Workflow_Lifecycle/milestone-schema.md`：① §6.4 合成协议新增**步 6"大 PRD 并进分支"**——brief 是大 PRD（判据回指 `references-schema §2`）时除合成三段外额外触发 `prd-split` 切成 `references/prd/`（一份输入喂两个海拔）+ 两次 soft 对齐合并成一次呈交 + 落交叉指针；非大 PRD 到步 5 即止（非回归）。② §6.4 brief 定位补一条——PRD 喂两海拔、origin 非权威只读 vs references/prd 权威投影、生命周期独立。③ §5.3 拆分路线图新增**可选「相关 slug」标注**（方向→细节下钻指针，映射单一真源在路线图，非 PRD 里程碑不需要）。现有五步/模板字面未动。
- `Coder/40_Context_Management/prd-split.md` §3：补一条 blockquote——`/milestone` 触发首切时 `00_INDEX` 入口叙述记 owning 里程碑号（"本 PRD 服务 MILE-NNNN，映射见其 §5.3"），**只回指不重列**（细节→方向指针）；手动注入无此句。
- `Coder/40_Context_Management/references-schema.md` §8：flip R3 前向指针（"/milestone 触发首切 + 交叉指针" → **✅ 已由 `milestone-schema §6.4/§5.3` 落地**）。
- `Coder/README.md`：prd-split 名册条目同步——把"/milestone 并进入口属 R3–R5"更新为"手动注入(R2) + /milestone 并进入口(R3 已落地，指 milestone-schema §6.4 步 6) / 钉版·改版同步属 R4–R5"（P5 独立复核挑出的 flip 连带漂移）。

## DELETE

- 无
