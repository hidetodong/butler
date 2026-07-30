<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0096 变更流

## ADD

- `Coder/40_Context_Management/sidework-receipt.md §1–§9` — 新增旁路工作短回执的定位、固定结构、生产/消费、路径安全、权限与可信度合同 → AC1,AC3,AC4
- `templates/sidework-receipt.md` — 新增代码与调研混合成果的六段 canonical 回执骨架 → AC2
- `scripts/test-sidework-receipt.py` — 新增规则、模板、入口、非授权与并发 create-only 的静态合同检查 → AC2,AC3,AC4,AC5,AC6

## EDIT

- `Coder/README.md §目录结构/规则索引/使用原则` — 注册旁路回执规则并限定触发式读取、禁止自动扫描 → AC1,AC5
- `HUMAN_GUIDE.md §部署目录/旁路成果回钩/规则速查` — 增加按需目录与用户发起、主 Agent 接回示例 → AC5
- `scripts/verify-ci.sh` — 把旁路回执专项接入唯一完整 CI → AC6

## DELETE

- 无
