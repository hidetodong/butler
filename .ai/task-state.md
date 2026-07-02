# Task State

> 无活跃迭代 · 上一收口 ITER-0020（2026-07-02）。

## 当前状态

- 无活跃迭代（current=none）。ITER-0020「提交与切版 SOP」已收口：提交规约成文（versioning-schema §5）+ 切版 git 仪式补全（§6）+ 指针/引用同步；收口自检 5/5 全绿。
- 独立迭代（所属 milestone —）。MILE-0001 仍 active、聚合发布待定，与本迭代解耦。

## 下一步入口

- 本迭代改动**未提交**（工作区待 commit）；按新 §5 规约，收口提交形如 `docs(versioning): 提交与切版 SOP —— 提交规约成文 + §5 切版 git 仪式补全 (ITER-0020)`，待用户显式指令再提交推送。
- 若开新迭代：按 `iteration-schema §5.1` 开启，P1 起走四件套。
- 若发布 MILE-0001 或聚合切版：按刚补全的 `versioning-schema §6` 切版仪式执行（可 dogfood 新 SOP）。
