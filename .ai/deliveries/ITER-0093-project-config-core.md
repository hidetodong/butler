# ITER-0093 · Butler 项目配置合同与统一读写内核

## 本次交付目标

建立不依赖 Markdown 散文解析的项目级 Butler JSON 配置合同与统一读写内核，为后续部署迁移和消费端切换提供单一机器接口。

## 已完成内容

- 新增严格的扁平 schema v1，固定五个顶层字段、默认值、类型和未知字段策略。
- 新增标准库 `inspect`、`init`、`set` CLI 与可导入模块，区分配置缺失和配置损坏。
- 写入采用同目录临时文件与原子发布；初始化不覆盖已有文件，更新失败保持原配置字节不变。
- 补齐正常、损坏、冲突、路径越界、symlink 和故障注入测试矩阵。

## 关键变更 / 用户可感知变化

R1 只交付可复用的配置内核，尚未切换现有命令和部署流程；现有项目行为保持不变。后续 R2/R3 将在此接口上完成迁移和全链路接线。

## 高层影响范围

新增 `tools/project-config/`，未修改 `local-constraints.md`、部署/升级流程或危险模式、独立复核、偏好和进度的现有读取位置。

## 验证方式与结果摘要

配置专项 18 项通过；完整 CI 在宿主权限下复跑通过，包含 200 个 hook 测试和全部行为组；`git diff --check` 与 Goal 完成资格裁决通过。

## 已知剩余风险 / 延后事项

- 本轮由危险模式自主 ACK；P5 强审修复 1 个 Must Fix 后最终 Must Fix 0、Should Fix 0。
- 项目 `independent_review` 为 off，未执行 fresh-context 独立复核。
- legacy Markdown 迁移和消费端切换按里程碑边界留给 R2/R3，不属于本迭代欠实现。

## 引用

- `.ai/iterations/ITER-0093/AC_LIST.md`
- `.ai/iterations/ITER-0093/TECH_PLAN.md`
- `.ai/iterations/ITER-0093/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0093/evidence/`
- `tools/project-config/README.md`
