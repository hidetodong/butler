# 01_CHANGELOG

> 安装器事务安全 · closed · 2026-07-18

## ADD

- `scripts/configure-global-install.py §plan/apply` — 新增先全量预检、再逐对象原子更新的全局配置 helper，并以所有权证据保护用户软链 → AC1, AC2, AC3, AC4, AC5
- `scripts/test-configure-global-install.py §GlobalInstallTests` — 新增隔离 HOME 专项回归，覆盖 marker、export、软链、权限、字节保真、竞态与幂等 → AC1, AC2, AC3, AC4, AC5, AC6, AC7

## EDIT

- `scripts/setup.sh §用户级配置/Codex plugin` — 改为调用安全 helper，并在 plugin 失败时返回真实状态而非假报总成功 → AC3, AC4, AC5, AC7
- `scripts/verify-dual-host.sh §setup matrix` — 接入专项测试，补预检零写入、重复安装与 plugin 部分失败场景 → AC6, AC7, AC8
- `HUMAN_GUIDE.md §安装` — 补 marker、重复 export、命令目录冲突的人工处理入口与逐对象原子边界 → AC8
- `README.md §仓库结构` — 注册全局配置 helper → AC8

## DELETE

- 无
