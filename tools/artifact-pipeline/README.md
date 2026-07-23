# artifact-pipeline

Butler 五件套结构的机器真源。`artifacts.v1.json` 唯一定义模板版本、产物路径、阶段、一级段落顺序、固定表头、状态字段和条件段；`templates/` 是与 manifest 对账的 canonical 骨架。

固定的是容器，不是正文措辞。条件段不得删除，不适用时保留 `N/A`。带 `butler-artifact-template` 标记的新 live 产物走 strict 合同；旧项目和 `.ai/iterations/` 历史归档默认 legacy，只读不追罚。

## 生成命令

```bash
python3 tools/artifact-pipeline/contract.py render concept --project-root . --iteration ITER-0001 --title 标题 --current-phase P1
python3 tools/artifact-pipeline/contract.py init acceptance --project-root . --iteration ITER-0001 --current-phase P2 --dry-run
python3 tools/artifact-pipeline/contract.py reset tech_plan --project-root . --iteration ITER-0001 --current-phase P3 --force
```

`render` 零写输出；`init` 只补缺失文件、绝不覆盖；`reset` 对已存在目标要求显式 `--force`。调用方必须声明当前阶段，生成下游产物会被拒绝。

## Legacy 迁移

`migration.py plan/apply/verify/rollback` 把当前 live legacy 五件套迁到 canonical v1。兼容 legacy H1/H2 章节，但只接受 canonical 章节集合；未知或重复段拒绝。apply 先备份 pre bytes，再成组原子写；rollback 受 post hash 门控。历史 `.ai/iterations/` 不参与迁移。
