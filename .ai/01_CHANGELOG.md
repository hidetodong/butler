> R3「交付自测」桥工具（ITER-0023） · active · —

本文件是**当前活跃迭代 ITER-0023** 的对象级变更流（ADD/EDIT/DELETE）。

## ADD

- `tools/delivery-selftest/render.js`（AC1/AC2/AC6）——`render(manifest)→HTML` 纯函数 + `VERDICTS` 四态 + `escapeHtml`；GitHub 风格分步流程页 + 客户端脚本（四态 / 进度 / POST 提交）。
- `tools/delivery-selftest/bridge.js`（AC1/AC3/AC4/AC6）——CLI + HTTP 服务（GET / · /health · POST /submit）+ 开浏览器 + 写 results.json + 进程自退；导出 `createBridge` 可测。
- `tools/delivery-selftest/README.md`（AC5）——用法 + manifest / results 契约 + 四态路由表 + R4/R5 边界。
- `tools/delivery-selftest/example/manifest.json`（AC5）——示例人测清单。
- `tools/delivery-selftest/test/bridge.test.js`（AC7）——node 内建端到端 + render 单测。
- `tools/delivery-selftest/package.json`（AC6）——零依赖标识（type/scripts、dependencies 空）。

## EDIT

- 仓库根 `CLAUDE.md`（AC9）——目录结构与职责加 `tools/`。
- `.ai/PROJECT.md`（AC9，收口前滚）——tools/ 与桥工具入架构图 / 现行约束。

## DELETE

- 无
