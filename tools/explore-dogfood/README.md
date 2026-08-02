# explore-dogfood

这是 Butler Explore 的内部回归 / dogfood harness，不是用户 workflow、Router、agent scheduler 或外部 tracker。

它在临时项目中编排现有 `decision-map`、`decision-work` 与 `decision-promotion` 引擎，复现一条结构化提问卡片决策链：创建依赖图、准备两个可并行 Research、按真实 `serial` 模式回传、显式吸收、在新进程恢复状态，再把 resolved slice 引用到既有 planned Milestone route。

```bash
python3 tools/explore-dogfood/scenario.py
python3 tools/explore-dogfood/scenario.py --inspect-project-root <PROJECT_ROOT> --map-id DMAP-0001
python3 tools/explore-dogfood/scenario.py --verify-project-root <PROJECT_ROOT> --map-id DMAP-0001 --milestone-id MILE-0014 --route-id R5
python3 -m unittest discover -s tools/explore-dogfood/tests
```

stdout 是单个 JSON 观测对象。无参数时临时项目在输出前已被清理；`--inspect-project-root` 只读聚合 Map / Work 的公开 inspect 视图，用一条命令恢复 destination、Frontier、Attempt 和下一动作，不写派生缓存。`--verify-project-root` 另核对 live Map / Work、deferred 候办和已占用路线的 promotion 拒绝，并在前后摘要相同且无 receipt 时才返回 `status=ok`。该对象只用于测试和 verification evidence，不是新的状态真源。生产写入仍只能经过三个相邻 Module 各自的 `inspect / plan / apply / verify` 合同。
