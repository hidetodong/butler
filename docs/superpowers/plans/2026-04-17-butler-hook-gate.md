# Butler Hook-based 硬门控（Phase 1）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 butler 仓库 `templates/hooks/` 实现 Claude Code PreToolUse hook 骨架（Python 模块化 dispatcher + 规则注册表），并更新 mcv-deployment 协议使其在部署目标项目时分发 hooks。

**Architecture:** 模块化 Python 脚本：`butler_gate.py` dispatcher 读 stdin JSON，顺序执行 `rules/` 下规则模块（`protected_paths` / `phase_gate` / `artifact_chain`），任一 deny 走 `lib/bypass.py` 的逃生判定（`BUTLER_BYPASS=1` + `.ai/bypass-reason.md` 非空），成功 bypass 追加 `.ai/RUN_LOG.md`；hook 自身崩溃 fail-closed。

**Tech Stack:** Python 3.9+（仅 stdlib：`json`、`pathlib`、`dataclasses`、`datetime`）；pytest（单测 + 集成）；bash（smoke 脚本）。

**Spec 引用：** `docs/superpowers/specs/2026-04-17-butler-hook-gate-design.md`

---

## 文件结构

**新建：**

```
templates/
  hooks/
    butler_gate.py                     # dispatcher
    pytest.ini                         # pythonpath = .
    conftest.py                        # （顶层 shim，保证 pytest 能导入 lib/rules）
    rules/
      __init__.py                      # 空
      phase_gate.py                    # (a)+(e) 存在性规则
      protected_paths.py               # (c) 规则
      artifact_chain.py                # 占位，永远 allow
    lib/
      __init__.py                      # 空
      io.py                            # Context, Decision, parse_stdin, resolve_target, is_gated, GATED_BLACKLIST
      bypass.py                        # evaluate_bypass, _append_run_log
    tests/
      __init__.py                      # 空（避免 test 模块名冲突）
      conftest.py                      # tmp_project fixture（拷贝 fixtures/<name> 到 tmp_path）
      test_io.py                       # lib/io.py 单测
      test_bypass.py                   # lib/bypass.py 单测
      test_protected_paths.py          # rules/protected_paths.py 单测
      test_phase_gate.py               # rules/phase_gate.py 单测
      test_artifact_chain.py           # rules/artifact_chain.py 单测
      test_integration.py              # dispatcher 子进程集成测试
      smoke.sh                         # Tier 3 手工 smoke
      fixtures/
        empty-project/.ai/.gitkeep
        p1-done/.ai/CONCEPT.md         # 非空占位
        p1p2-done/.ai/CONCEPT.md
        p1p2-done/.ai/AC_LIST.md
        full-artifacts/.ai/CONCEPT.md
        full-artifacts/.ai/AC_LIST.md
        full-artifacts/.ai/TECH_PLAN.md
        with-bypass-reason/.ai/CONCEPT.md
        with-bypass-reason/.ai/AC_LIST.md
        with-bypass-reason/.ai/TECH_PLAN.md
        with-bypass-reason/.ai/bypass-reason.md
    README.md                          # 贡献者说明
  settings.hooks-snippet.json          # PreToolUse 配置片段
```

**修改：**

- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`：新增 "5. Hook 注入" 步骤
- `Coder/README.md`：`templates/` 目录说明登记 `hooks/` 与 `settings.hooks-snippet.json`

---

## 导入契约

- `templates/hooks/` 目录通过 `pytest.ini` 的 `pythonpath = .` 加入 sys.path，使 `from lib.io import ...`、`from rules import ...` 在测试中可用。
- `butler_gate.py` 作为脚本被 Claude Code 以 `python3 .claude/hooks/butler_gate.py` 调用时，在文件顶部做 `sys.path.insert(0, str(Path(__file__).resolve().parent))` 使绝对导入生效。
- 子模块间一律用**绝对导入**（`from lib.io import ...`），不使用相对导入。

---

## 任务列表概览

- **Task 1**: 目录骨架 + 空 `__init__.py` + 测试 fixtures
- **Task 2**: `lib/io.py` — 类型、常量、IO helpers（TDD）
- **Task 3**: `lib/bypass.py` — BUTLER_BYPASS + reason + RUN_LOG（TDD）
- **Task 4**: `rules/protected_paths.py`（TDD）
- **Task 5**: `rules/phase_gate.py`（TDD）
- **Task 6**: `rules/artifact_chain.py`（stub + 测试）
- **Task 7**: `butler_gate.py` dispatcher + 集成测试
- **Task 8**: `smoke.sh` + `settings.hooks-snippet.json`
- **Task 9**: `templates/hooks/README.md`
- **Task 10**: 更新 `mcv-deployment.md` 与 `Coder/README.md`

---

## Task 1: 目录骨架 + 空文件 + 测试 fixtures

**Files:**
- Create: `templates/hooks/pytest.ini`
- Create: `templates/hooks/conftest.py`
- Create: `templates/hooks/rules/__init__.py`
- Create: `templates/hooks/lib/__init__.py`
- Create: `templates/hooks/tests/__init__.py`
- Create: `templates/hooks/tests/conftest.py`
- Create: `templates/hooks/tests/fixtures/empty-project/.ai/.gitkeep`
- Create: `templates/hooks/tests/fixtures/p1-done/.ai/CONCEPT.md`
- Create: `templates/hooks/tests/fixtures/p1p2-done/.ai/CONCEPT.md`
- Create: `templates/hooks/tests/fixtures/p1p2-done/.ai/AC_LIST.md`
- Create: `templates/hooks/tests/fixtures/full-artifacts/.ai/CONCEPT.md`
- Create: `templates/hooks/tests/fixtures/full-artifacts/.ai/AC_LIST.md`
- Create: `templates/hooks/tests/fixtures/full-artifacts/.ai/TECH_PLAN.md`
- Create: `templates/hooks/tests/fixtures/with-bypass-reason/.ai/CONCEPT.md`
- Create: `templates/hooks/tests/fixtures/with-bypass-reason/.ai/AC_LIST.md`
- Create: `templates/hooks/tests/fixtures/with-bypass-reason/.ai/TECH_PLAN.md`
- Create: `templates/hooks/tests/fixtures/with-bypass-reason/.ai/bypass-reason.md`

- [ ] **Step 1: 创建 pytest.ini**

Write `templates/hooks/pytest.ini`:

```ini
[pytest]
pythonpath = .
testpaths = tests
```

- [ ] **Step 2: 创建顶层 conftest.py（占位，内容空）**

Write `templates/hooks/conftest.py`:

```python
```

- [ ] **Step 3: 创建各包 `__init__.py`（全部空文件）**

Write `templates/hooks/rules/__init__.py`：空。
Write `templates/hooks/lib/__init__.py`：空。
Write `templates/hooks/tests/__init__.py`：空。

- [ ] **Step 4: 创建 fixtures — empty-project**

Write `templates/hooks/tests/fixtures/empty-project/.ai/.gitkeep`：空。

- [ ] **Step 5: 创建 fixtures — p1-done**

Write `templates/hooks/tests/fixtures/p1-done/.ai/CONCEPT.md`:

```markdown
# CONCEPT (fixture)
占位内容，用于测试：文件存在且非空
```

- [ ] **Step 6: 创建 fixtures — p1p2-done**

Write `templates/hooks/tests/fixtures/p1p2-done/.ai/CONCEPT.md`:

```markdown
# CONCEPT (fixture)
占位内容
```

Write `templates/hooks/tests/fixtures/p1p2-done/.ai/AC_LIST.md`:

```markdown
# AC_LIST (fixture)
占位内容
```

- [ ] **Step 7: 创建 fixtures — full-artifacts**

Write `templates/hooks/tests/fixtures/full-artifacts/.ai/CONCEPT.md`:

```markdown
# CONCEPT (fixture)
占位内容
```

Write `templates/hooks/tests/fixtures/full-artifacts/.ai/AC_LIST.md`:

```markdown
# AC_LIST (fixture)
占位内容
```

Write `templates/hooks/tests/fixtures/full-artifacts/.ai/TECH_PLAN.md`:

```markdown
# TECH_PLAN (fixture)
占位内容
```

- [ ] **Step 8: 创建 fixtures — with-bypass-reason**

复制 full-artifacts 的三个 `.md` 到 `with-bypass-reason/.ai/`，另外新增：

Write `templates/hooks/tests/fixtures/with-bypass-reason/.ai/CONCEPT.md`:

```markdown
# CONCEPT (fixture)
占位内容
```

Write `templates/hooks/tests/fixtures/with-bypass-reason/.ai/AC_LIST.md`:

```markdown
# AC_LIST (fixture)
占位内容
```

Write `templates/hooks/tests/fixtures/with-bypass-reason/.ai/TECH_PLAN.md`:

```markdown
# TECH_PLAN (fixture)
占位内容
```

Write `templates/hooks/tests/fixtures/with-bypass-reason/.ai/bypass-reason.md`:

```markdown
hotfix for prod 500
详细理由：XYZ 在生产环境抛 500，需要立即打补丁，事后补 AC
```

- [ ] **Step 9: 创建 tests/conftest.py（tmp_project fixture）**

Write `templates/hooks/tests/conftest.py`:

```python
"""pytest fixtures shared across hook tests."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def tmp_project(tmp_path: Path):
    """Copy a named fixture tree into tmp_path. Returns the project root."""

    def _make(fixture_name: str) -> Path:
        src = FIXTURES_DIR / fixture_name
        if not src.exists():
            raise FileNotFoundError(f"fixture not found: {fixture_name}")
        for item in src.rglob("*"):
            rel = item.relative_to(src)
            dst = tmp_path / rel
            if item.is_dir():
                dst.mkdir(parents=True, exist_ok=True)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst)
        return tmp_path

    return _make
```

- [ ] **Step 10: 运行 pytest（应为 0 tests）**

Run: `cd templates/hooks && python3 -m pytest tests/ -v`
Expected: `no tests ran in ...`（0 collected，0 failed）

- [ ] **Step 11: 提交**

```bash
git add templates/hooks/
git commit -m "feat(hook-gate): scaffold templates/hooks/ directory and test fixtures"
```

---

## Task 2: `lib/io.py` — 类型、常量、IO helpers（TDD）

**Files:**
- Test: `templates/hooks/tests/test_io.py`
- Create: `templates/hooks/lib/io.py`

- [ ] **Step 1: 写失败的测试**

Write `templates/hooks/tests/test_io.py`:

```python
"""Unit tests for lib.io."""
from __future__ import annotations

import io as stdio
import json
import sys
from pathlib import PurePosixPath

import pytest

from lib.io import (
    Context,
    Decision,
    GATED_BLACKLIST,
    OUT_OF_CWD,
    is_gated,
    parse_stdin,
    resolve_target,
)


class TestResolveTarget:
    def test_relative_path_preserved(self):
        result = resolve_target({"file_path": "src/auth.ts"}, cwd="/tmp/proj")
        assert result == PurePosixPath("src/auth.ts")

    def test_missing_file_path_returns_out_of_cwd(self):
        result = resolve_target({}, cwd="/tmp/proj")
        assert result == OUT_OF_CWD

    def test_empty_file_path_returns_out_of_cwd(self):
        result = resolve_target({"file_path": ""}, cwd="/tmp/proj")
        assert result == OUT_OF_CWD

    def test_parent_reference_resolves_within_cwd(self, tmp_path):
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "a.ts").write_text("x")
        result = resolve_target(
            {"file_path": "src/../src/a.ts"}, cwd=str(tmp_path)
        )
        assert result == PurePosixPath("src/a.ts")

    def test_parent_reference_escapes_cwd_returns_sentinel(self, tmp_path):
        result = resolve_target(
            {"file_path": "../escape.ts"}, cwd=str(tmp_path)
        )
        assert result == OUT_OF_CWD

    def test_absolute_path_inside_cwd_resolved_to_relative(self, tmp_path):
        target = tmp_path / "src" / "a.ts"
        target.parent.mkdir(parents=True)
        target.write_text("x")
        result = resolve_target({"file_path": str(target)}, cwd=str(tmp_path))
        assert result == PurePosixPath("src/a.ts")

    def test_absolute_path_outside_cwd_returns_sentinel(self, tmp_path):
        other = tmp_path.parent / "other_dir"
        result = resolve_target({"file_path": str(other / "x.ts")}, cwd=str(tmp_path))
        assert result == OUT_OF_CWD


class TestIsGated:
    def test_source_path_is_gated(self):
        assert is_gated(PurePosixPath("src/auth.ts")) is True

    def test_ai_directory_exempt(self):
        assert is_gated(PurePosixPath(".ai/CONCEPT.md")) is False

    def test_deliveries_exempt(self):
        assert is_gated(PurePosixPath("deliveries/x.md")) is False

    def test_claude_dir_exempt(self):
        assert is_gated(PurePosixPath(".claude/settings.json")) is False

    def test_node_modules_exempt(self):
        assert is_gated(PurePosixPath("node_modules/foo/index.js")) is False

    def test_out_of_cwd_is_gated_conservative(self):
        assert is_gated(OUT_OF_CWD) is True

    def test_root_of_blacklisted_dir_exempt(self):
        assert is_gated(PurePosixPath(".ai")) is False

    def test_prefix_collision_not_false_positive(self):
        # ".github" must NOT match ".git" prefix
        assert is_gated(PurePosixPath(".github/workflows/ci.yml")) is True


class TestParseStdin:
    def test_parse_valid_json(self, monkeypatch):
        payload = {"tool_name": "Edit", "tool_input": {"file_path": "x"}, "cwd": "/tmp"}
        monkeypatch.setattr(sys, "stdin", stdio.StringIO(json.dumps(payload)))
        assert parse_stdin() == payload

    def test_parse_invalid_json_raises(self, monkeypatch):
        monkeypatch.setattr(sys, "stdin", stdio.StringIO("not json"))
        with pytest.raises(json.JSONDecodeError):
            parse_stdin()


class TestDecision:
    def test_decision_defaults(self):
        d = Decision(verdict="allow", rule_id="x")
        assert d.verdict == "allow"
        assert d.rule_id == "x"
        assert d.reason == ""
        assert d.remediation == ""


class TestBlacklistContents:
    def test_expected_entries(self):
        assert ".ai/" in GATED_BLACKLIST
        assert "deliveries/" in GATED_BLACKLIST
        assert ".claude/" in GATED_BLACKLIST
        assert ".git/" in GATED_BLACKLIST
        assert "node_modules/" in GATED_BLACKLIST
        assert ".vscode/" in GATED_BLACKLIST
        assert ".idea/" in GATED_BLACKLIST
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd templates/hooks && python3 -m pytest tests/test_io.py -v`
Expected: `ModuleNotFoundError: No module named 'lib.io'`

- [ ] **Step 3: 实现 lib/io.py**

Write `templates/hooks/lib/io.py`:

```python
"""Types, constants, and stdin/path helpers for butler_gate."""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Literal

GATED_BLACKLIST = frozenset({
    ".ai/",
    "deliveries/",
    ".claude/",
    ".git/",
    "node_modules/",
    ".vscode/",
    ".idea/",
})

OUT_OF_CWD = PurePosixPath("__OUT_OF_CWD__")


@dataclass(frozen=True)
class Context:
    cwd: str
    tool_name: str
    target_path: PurePosixPath
    tool_input: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Decision:
    verdict: Literal["allow", "deny"]
    rule_id: str
    reason: str = ""
    remediation: str = ""


def parse_stdin() -> dict:
    """Reads Claude Code PreToolUse JSON from stdin."""
    return json.loads(sys.stdin.read())


def resolve_target(tool_input: dict, cwd: str) -> PurePosixPath:
    """Normalize file_path into a path relative to cwd.

    Returns OUT_OF_CWD sentinel for missing, empty, or escaped paths.
    """
    raw = tool_input.get("file_path", "")
    if not raw:
        return OUT_OF_CWD

    p = Path(raw).expanduser()
    cwd_resolved = Path(cwd).resolve()

    if p.is_absolute():
        try:
            rel = p.resolve().relative_to(cwd_resolved)
        except ValueError:
            return OUT_OF_CWD
        return PurePosixPath(rel.as_posix())

    # Relative path: resolve against cwd, check it stays inside.
    try:
        resolved = (cwd_resolved / p).resolve()
        rel = resolved.relative_to(cwd_resolved)
    except ValueError:
        return OUT_OF_CWD
    return PurePosixPath(rel.as_posix())


def is_gated(target: PurePosixPath, blacklist: frozenset = GATED_BLACKLIST) -> bool:
    """True when the target path is subject to gating (i.e. NOT in the exempt blacklist)."""
    if target == OUT_OF_CWD:
        return True
    target_str = target.as_posix()
    for prefix in blacklist:
        p = prefix.rstrip("/")
        if target_str == p or target_str.startswith(p + "/"):
            return False
    return True
```

- [ ] **Step 4: 运行测试确认通过**

Run: `cd templates/hooks && python3 -m pytest tests/test_io.py -v`
Expected: 所有 test 通过（~17 个）

- [ ] **Step 5: 提交**

```bash
git add templates/hooks/lib/io.py templates/hooks/tests/test_io.py
git commit -m "feat(hook-gate): add lib/io types, constants, and path helpers"
```

---

## Task 3: `lib/bypass.py` — BUTLER_BYPASS + reason + RUN_LOG（TDD）

**Files:**
- Test: `templates/hooks/tests/test_bypass.py`
- Create: `templates/hooks/lib/bypass.py`

- [ ] **Step 1: 写失败的测试**

Write `templates/hooks/tests/test_bypass.py`:

```python
"""Unit tests for lib.bypass."""
from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

import pytest

from lib.bypass import evaluate_bypass
from lib.io import Context, Decision


def make_ctx(cwd: Path, target: str = "src/auth.ts") -> Context:
    return Context(
        cwd=str(cwd),
        tool_name="Edit",
        target_path=PurePosixPath(target),
        tool_input={"file_path": target},
    )


DENY = Decision(
    verdict="deny",
    rule_id="phase_gate",
    reason="缺 .ai/CONCEPT.md",
    remediation="先完成 P1",
)

ALLOW = Decision(verdict="allow", rule_id="phase_gate")


class TestBypassEnvUnset:
    def test_returns_original_decision(self, tmp_path, monkeypatch):
        monkeypatch.delenv("BUTLER_BYPASS", raising=False)
        result = evaluate_bypass(make_ctx(tmp_path), DENY)
        assert result.verdict == "deny"
        assert result.rule_id == "phase_gate"

    def test_pass_through_allow_unchanged(self, tmp_path, monkeypatch):
        monkeypatch.delenv("BUTLER_BYPASS", raising=False)
        result = evaluate_bypass(make_ctx(tmp_path), ALLOW)
        assert result.verdict == "allow"


class TestBypassEnvSetButNoReason:
    def test_missing_reason_file_stays_deny(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        # no .ai/bypass-reason.md
        result = evaluate_bypass(make_ctx(tmp_path), DENY)
        assert result.verdict == "deny"
        assert "bypass-reason.md" in result.reason

    def test_empty_reason_stays_deny(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("")
        result = evaluate_bypass(make_ctx(tmp_path), DENY)
        assert result.verdict == "deny"

    def test_whitespace_only_reason_stays_deny(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("   \n\t\n")
        result = evaluate_bypass(make_ctx(tmp_path), DENY)
        assert result.verdict == "deny"


class TestBypassSuccess:
    def test_valid_reason_allows(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("hotfix\ndetails")
        result = evaluate_bypass(make_ctx(tmp_path), DENY)
        assert result.verdict == "allow"
        assert result.rule_id == "phase_gate"

    def test_run_log_appended(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("hotfix for prod")
        evaluate_bypass(make_ctx(tmp_path), DENY)
        log = (tmp_path / ".ai" / "RUN_LOG.md").read_text()
        assert "phase_gate" in log
        assert "Edit" in log
        assert "src/auth.ts" in log
        assert "hotfix for prod" in log

    def test_run_log_line_format(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("x")
        evaluate_bypass(make_ctx(tmp_path), DENY)
        log = (tmp_path / ".ai" / "RUN_LOG.md").read_text().strip()
        # <ISO-UTC> | <rule_id> | <tool_name> | <relative_target> | <reason_first_line>
        pattern = (
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z \| phase_gate \| Edit \| src/auth\.ts \| x$"
        )
        assert re.match(pattern, log), f"actual: {log!r}"

    def test_run_log_only_first_line_of_reason(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text(
            "hotfix first line\nsecond line\nthird"
        )
        evaluate_bypass(make_ctx(tmp_path), DENY)
        log = (tmp_path / ".ai" / "RUN_LOG.md").read_text()
        assert "hotfix first line" in log
        assert "second line" not in log

    def test_run_log_appends_not_overwrites(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "RUN_LOG.md").write_text("existing line\n")
        (tmp_path / ".ai" / "bypass-reason.md").write_text("new reason")
        evaluate_bypass(make_ctx(tmp_path), DENY)
        log = (tmp_path / ".ai" / "RUN_LOG.md").read_text()
        assert log.startswith("existing line\n")
        assert "new reason" in log

    def test_run_log_creates_ai_dir_if_missing(self, tmp_path, monkeypatch):
        # Edge case: .ai/ not yet created; bypass should still create it when writing log.
        # But this scenario also requires reason file — which lives in .ai/ — so in practice
        # .ai/ must exist when bypass is used. Still verify mkdir parents=True works.
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("r")
        # Delete RUN_LOG.md if any prior state
        log_path = tmp_path / ".ai" / "RUN_LOG.md"
        assert not log_path.exists()
        evaluate_bypass(make_ctx(tmp_path), DENY)
        assert log_path.exists()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd templates/hooks && python3 -m pytest tests/test_bypass.py -v`
Expected: `ModuleNotFoundError: No module named 'lib.bypass'`

- [ ] **Step 3: 实现 lib/bypass.py**

Write `templates/hooks/lib/bypass.py`:

```python
"""BUTLER_BYPASS evaluation and RUN_LOG append."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

from lib.io import Context, Decision


def evaluate_bypass(ctx: Context, decision: Decision) -> Decision:
    """Decide whether an environment-based bypass overrides a deny decision.

    Returns a new Decision: the original if not overridden, or an allow Decision
    with RUN_LOG appended if bypass succeeds.
    """
    if decision.verdict != "deny":
        return decision
    if os.environ.get("BUTLER_BYPASS") != "1":
        return decision

    reason_path = Path(ctx.cwd) / ".ai" / "bypass-reason.md"
    if not reason_path.exists():
        return Decision(
            verdict="deny",
            rule_id=decision.rule_id,
            reason=f"{decision.reason}\n  bypass 失败：需先在 .ai/bypass-reason.md 写明理由",
            remediation=decision.remediation,
        )

    content = reason_path.read_text(encoding="utf-8").strip()
    if not content:
        return Decision(
            verdict="deny",
            rule_id=decision.rule_id,
            reason=f"{decision.reason}\n  bypass 失败：.ai/bypass-reason.md 为空",
            remediation=decision.remediation,
        )

    first_line = content.splitlines()[0].strip()
    _append_run_log(ctx, decision, first_line)

    return Decision(
        verdict="allow",
        rule_id=decision.rule_id,
        reason="bypass ok",
        remediation="",
    )


def _append_run_log(ctx: Context, decision: Decision, reason_first_line: str) -> None:
    log_path = Path(ctx.cwd) / ".ai" / "RUN_LOG.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = (
        f"{ts} | {decision.rule_id} | {ctx.tool_name} | "
        f"{ctx.target_path.as_posix()} | {reason_first_line}\n"
    )
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line)
```

- [ ] **Step 4: 运行测试确认通过**

Run: `cd templates/hooks && python3 -m pytest tests/test_bypass.py -v`
Expected: 所有 test 通过（~9 个）

- [ ] **Step 5: 提交**

```bash
git add templates/hooks/lib/bypass.py templates/hooks/tests/test_bypass.py
git commit -m "feat(hook-gate): add bypass evaluation and RUN_LOG append"
```

---

## Task 4: `rules/protected_paths.py`（TDD）

**Files:**
- Test: `templates/hooks/tests/test_protected_paths.py`
- Create: `templates/hooks/rules/protected_paths.py`

- [ ] **Step 1: 写失败的测试**

Write `templates/hooks/tests/test_protected_paths.py`:

```python
"""Unit tests for rules.protected_paths."""
from __future__ import annotations

from pathlib import PurePosixPath

from lib.io import Context
from rules import protected_paths


def make_ctx(target: str) -> Context:
    return Context(
        cwd="/tmp/proj",
        tool_name="Edit",
        target_path=PurePosixPath(target),
        tool_input={"file_path": target},
    )


class TestProtectedPaths:
    def test_business_extension_denies(self):
        d = protected_paths.evaluate(make_ctx("99_Business_Extension/policy.md"))
        assert d.verdict == "deny"
        assert d.rule_id == "protected_paths"
        assert "99_Business_Extension" in d.reason
        assert d.remediation

    def test_business_extension_nested_denies(self):
        d = protected_paths.evaluate(
            make_ctx("99_Business_Extension/nested/deep/file.md")
        )
        assert d.verdict == "deny"

    def test_normal_source_allows(self):
        d = protected_paths.evaluate(make_ctx("src/auth.ts"))
        assert d.verdict == "allow"
        assert d.rule_id == "protected_paths"

    def test_ai_directory_allows(self):
        d = protected_paths.evaluate(make_ctx(".ai/CONCEPT.md"))
        assert d.verdict == "allow"

    def test_similar_name_not_false_positive(self):
        # "99_business_extension_notes.md" should NOT match the protected prefix
        d = protected_paths.evaluate(make_ctx("99_business_extension_notes.md"))
        assert d.verdict == "allow"

    def test_path_at_root_matching_prefix(self):
        d = protected_paths.evaluate(make_ctx("99_Business_Extension"))
        # root of the protected dir itself — treat as protected or allow?
        # Spec says **/*.md under it, but a write *to* that path (as a file) is unusual.
        # Choose: treat it as allow since it's not under the directory hierarchy.
        # Adjust implementation accordingly.
        assert d.verdict == "allow"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd templates/hooks && python3 -m pytest tests/test_protected_paths.py -v`
Expected: `ImportError: cannot import name 'protected_paths' from 'rules'` 或类似错误

- [ ] **Step 3: 实现 rules/protected_paths.py**

Write `templates/hooks/rules/protected_paths.py`:

```python
"""Rule: deny writes under 99_Business_Extension/."""
from __future__ import annotations

from lib.io import Context, Decision

RULE_ID = "protected_paths"
PROTECTED_PREFIXES = ("99_Business_Extension/",)


def evaluate(ctx: Context) -> Decision:
    target = ctx.target_path.as_posix()
    for prefix in PROTECTED_PREFIXES:
        p = prefix.rstrip("/")
        if target.startswith(p + "/"):
            return Decision(
                verdict="deny",
                rule_id=RULE_ID,
                reason=f"业务扩展目录 {prefix} 禁止直接写操作",
                remediation=(
                    "走 mcv-update 协议或显式 bypass"
                    "（BUTLER_BYPASS=1 + .ai/bypass-reason.md）"
                ),
            )
    return Decision(verdict="allow", rule_id=RULE_ID)
```

- [ ] **Step 4: 运行测试确认通过**

Run: `cd templates/hooks && python3 -m pytest tests/test_protected_paths.py -v`
Expected: 所有 test 通过（6 个）

- [ ] **Step 5: 提交**

```bash
git add templates/hooks/rules/protected_paths.py templates/hooks/tests/test_protected_paths.py
git commit -m "feat(hook-gate): add protected_paths rule for 99_Business_Extension/"
```

---

## Task 5: `rules/phase_gate.py`（TDD）

**Files:**
- Test: `templates/hooks/tests/test_phase_gate.py`
- Create: `templates/hooks/rules/phase_gate.py`

- [ ] **Step 1: 写失败的测试**

Write `templates/hooks/tests/test_phase_gate.py`:

```python
"""Unit tests for rules.phase_gate."""
from __future__ import annotations

from pathlib import Path, PurePosixPath

from lib.io import Context, OUT_OF_CWD
from rules import phase_gate


def make_ctx(cwd: Path, target: str) -> Context:
    return Context(
        cwd=str(cwd),
        tool_name="Edit",
        target_path=PurePosixPath(target),
        tool_input={"file_path": target},
    )


def make_ctx_oocwd(cwd: Path) -> Context:
    return Context(
        cwd=str(cwd),
        tool_name="Edit",
        target_path=OUT_OF_CWD,
        tool_input={},
    )


class TestPhaseGate:
    def test_blacklist_path_allows(self, tmp_project):
        proj = tmp_project("empty-project")
        d = phase_gate.evaluate(make_ctx(proj, ".ai/CONCEPT.md"))
        assert d.verdict == "allow"
        assert d.rule_id == "phase_gate"

    def test_all_artifacts_present_allows(self, tmp_project):
        proj = tmp_project("full-artifacts")
        d = phase_gate.evaluate(make_ctx(proj, "src/auth.ts"))
        assert d.verdict == "allow"

    def test_concept_missing_denies(self, tmp_project):
        proj = tmp_project("empty-project")
        d = phase_gate.evaluate(make_ctx(proj, "src/auth.ts"))
        assert d.verdict == "deny"
        assert d.rule_id == "phase_gate"
        assert "CONCEPT.md" in d.reason

    def test_ac_list_missing_denies(self, tmp_project):
        proj = tmp_project("p1-done")
        d = phase_gate.evaluate(make_ctx(proj, "src/auth.ts"))
        assert d.verdict == "deny"
        assert "AC_LIST.md" in d.reason

    def test_tech_plan_missing_denies(self, tmp_project):
        proj = tmp_project("p1p2-done")
        d = phase_gate.evaluate(make_ctx(proj, "src/auth.ts"))
        assert d.verdict == "deny"
        assert "TECH_PLAN.md" in d.reason

    def test_empty_file_denies(self, tmp_path):
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "CONCEPT.md").write_text("")
        d = phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts"))
        assert d.verdict == "deny"
        assert "CONCEPT.md" in d.reason

    def test_whitespace_only_file_denies(self, tmp_path):
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "CONCEPT.md").write_text("   \n\n")
        d = phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts"))
        assert d.verdict == "deny"

    def test_out_of_cwd_denies(self, tmp_project):
        proj = tmp_project("full-artifacts")
        d = phase_gate.evaluate(make_ctx_oocwd(proj))
        assert d.verdict == "deny"

    def test_reason_includes_remediation(self, tmp_project):
        proj = tmp_project("empty-project")
        d = phase_gate.evaluate(make_ctx(proj, "src/x.ts"))
        assert d.remediation
        assert "P1" in d.remediation
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd templates/hooks && python3 -m pytest tests/test_phase_gate.py -v`
Expected: `ImportError` 或模块未找到

- [ ] **Step 3: 实现 rules/phase_gate.py**

Write `templates/hooks/rules/phase_gate.py`:

```python
"""Rule: require P1/P2/P3 artifacts before gated source edits."""
from __future__ import annotations

from pathlib import Path

from lib.io import Context, Decision, is_gated

RULE_ID = "phase_gate"

REQUIRED_ARTIFACTS = [
    (".ai/CONCEPT.md", "P1", "先完成 P1 分析并产出 .ai/CONCEPT.md"),
    (".ai/AC_LIST.md", "P2", "先完成 P2 验收清单并产出 .ai/AC_LIST.md"),
    (".ai/TECH_PLAN.md", "P3", "先完成 P3 技术方案并产出 .ai/TECH_PLAN.md"),
]


def evaluate(ctx: Context) -> Decision:
    if not is_gated(ctx.target_path):
        return Decision(verdict="allow", rule_id=RULE_ID)

    for rel_path, phase, hint in REQUIRED_ARTIFACTS:
        artifact = Path(ctx.cwd) / rel_path
        if not _is_nonempty(artifact):
            return Decision(
                verdict="deny",
                rule_id=RULE_ID,
                reason=f"{phase} 产物缺失：{rel_path} 不存在或为空",
                remediation=hint,
            )
    return Decision(verdict="allow", rule_id=RULE_ID)


def _is_nonempty(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return False
    try:
        return bool(path.read_text(encoding="utf-8").strip())
    except OSError:
        return False
```

- [ ] **Step 4: 运行测试确认通过**

Run: `cd templates/hooks && python3 -m pytest tests/test_phase_gate.py -v`
Expected: 所有 test 通过（9 个）

- [ ] **Step 5: 提交**

```bash
git add templates/hooks/rules/phase_gate.py templates/hooks/tests/test_phase_gate.py
git commit -m "feat(hook-gate): add phase_gate rule for P1/P2/P3 artifact presence"
```

---

## Task 6: `rules/artifact_chain.py`（占位 + 测试）

**Files:**
- Test: `templates/hooks/tests/test_artifact_chain.py`
- Create: `templates/hooks/rules/artifact_chain.py`

- [ ] **Step 1: 写失败的测试**

Write `templates/hooks/tests/test_artifact_chain.py`:

```python
"""Unit tests for rules.artifact_chain (stub placeholder rule)."""
from __future__ import annotations

from pathlib import PurePosixPath

from lib.io import Context
from rules import artifact_chain


def make_ctx(target: str = "src/x.ts") -> Context:
    return Context(
        cwd="/tmp/proj",
        tool_name="Edit",
        target_path=PurePosixPath(target),
        tool_input={"file_path": target},
    )


class TestArtifactChainStub:
    def test_always_allows_source_path(self):
        d = artifact_chain.evaluate(make_ctx("src/auth.ts"))
        assert d.verdict == "allow"
        assert d.rule_id == "artifact_chain"

    def test_always_allows_protected_path(self):
        # Even paths that other rules deny must be allowed by the stub.
        d = artifact_chain.evaluate(make_ctx("99_Business_Extension/x.md"))
        assert d.verdict == "allow"

    def test_rule_id_stable(self):
        assert artifact_chain.RULE_ID == "artifact_chain"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd templates/hooks && python3 -m pytest tests/test_artifact_chain.py -v`
Expected: `ImportError`

- [ ] **Step 3: 实现 rules/artifact_chain.py（占位）**

Write `templates/hooks/rules/artifact_chain.py`:

```python
"""Rule: placeholder reserved for AC-ID linkage and other artifact-chain checks.

Currently always returns allow. Future phases will populate this module
(AC-ID linkage linter, etc.) without touching the dispatcher wiring.
"""
from __future__ import annotations

from lib.io import Context, Decision

RULE_ID = "artifact_chain"


def evaluate(ctx: Context) -> Decision:
    return Decision(verdict="allow", rule_id=RULE_ID)
```

- [ ] **Step 4: 运行测试确认通过**

Run: `cd templates/hooks && python3 -m pytest tests/test_artifact_chain.py -v`
Expected: 所有 test 通过（3 个）

- [ ] **Step 5: 提交**

```bash
git add templates/hooks/rules/artifact_chain.py templates/hooks/tests/test_artifact_chain.py
git commit -m "feat(hook-gate): add artifact_chain rule stub for future extension"
```

---

## Task 7: `butler_gate.py` dispatcher + 集成测试

**Files:**
- Create: `templates/hooks/butler_gate.py`
- Test: `templates/hooks/tests/test_integration.py`

本 task 特殊：dispatcher 是入口点，集成测试用 subprocess 跑真实 python 进程，验证 stdin/stdout/stderr/exit code 契约。**先写 dispatcher 再写集成测试**（因为无法单元测试 main()；集成测试本身即第一层验证）。

- [ ] **Step 1: 实现 butler_gate.py**

Write `templates/hooks/butler_gate.py`:

```python
#!/usr/bin/env python3
"""Claude Code PreToolUse dispatcher for butler harness gating.

Invoked by Claude Code with tool-call JSON on stdin. Exit code semantics:
  0  = allow
  2  = deny (either a rule said deny with no valid bypass, or internal crash)

Rule modules are evaluated in registered order; the first deny wins.
Hook itself is fail-closed on any uncaught exception.
"""
from __future__ import annotations

import sys
import traceback
from pathlib import Path

# Make absolute imports work when invoked as a script.
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from lib.bypass import evaluate_bypass
from lib.io import Context, Decision, parse_stdin, resolve_target
from rules import artifact_chain, phase_gate, protected_paths

GATED_TOOLS = frozenset({"Edit", "Write", "MultiEdit"})

# Registered in evaluation order. First deny wins; more specific rules first.
RULE_MODULES = [protected_paths, phase_gate, artifact_chain]


def main() -> int:
    try:
        payload = parse_stdin()
        tool_name = payload.get("tool_name", "")
        if tool_name not in GATED_TOOLS:
            return 0

        cwd = payload.get("cwd", ".")
        tool_input = payload.get("tool_input", {})
        target = resolve_target(tool_input, cwd)

        ctx = Context(
            cwd=cwd,
            tool_name=tool_name,
            target_path=target,
            tool_input=tool_input,
        )

        for mod in RULE_MODULES:
            decision = mod.evaluate(ctx)
            if decision.verdict == "deny":
                final = evaluate_bypass(ctx, decision)
                if final.verdict == "allow":
                    return 0
                _print_denial(ctx, final)
                return 2
        return 0
    except Exception:
        print("❌ butler-gate internal error:", file=sys.stderr)
        traceback.print_exc(limit=3, file=sys.stderr)
        print(
            "  bypass: 若要继续，设 BUTLER_BYPASS=1 并在 .ai/bypass-reason.md 写明理由",
            file=sys.stderr,
        )
        return 2


def _print_denial(ctx: Context, decision: Decision) -> None:
    print(f"❌ butler-gate denied: {decision.rule_id}", file=sys.stderr)
    print(f"  tool: {ctx.tool_name}", file=sys.stderr)
    print(f"  target: {ctx.target_path.as_posix()}", file=sys.stderr)
    print(f"  reason: {decision.reason}", file=sys.stderr)
    if decision.remediation:
        print(f"  remediation: {decision.remediation}", file=sys.stderr)
    print(
        "  bypass: 若坚持绕过，设 BUTLER_BYPASS=1 并在 .ai/bypass-reason.md 写明理由",
        file=sys.stderr,
    )


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: 写集成测试**

Write `templates/hooks/tests/test_integration.py`:

```python
"""Integration tests: run butler_gate.py as subprocess with real stdin/env."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

GATE = Path(__file__).resolve().parent.parent / "butler_gate.py"


def run_gate(payload: dict, cwd: Path, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env.pop("BUTLER_BYPASS", None)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(GATE)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        cwd=str(cwd),
    )


def edit_payload(cwd: Path, target: str) -> dict:
    return {
        "tool_name": "Edit",
        "tool_input": {"file_path": target, "old_string": "a", "new_string": "b"},
        "cwd": str(cwd),
    }


class TestAllowPaths:
    def test_allow_when_all_artifacts_present(self, tmp_project):
        proj = tmp_project("full-artifacts")
        r = run_gate(edit_payload(proj, "src/auth.ts"), proj)
        assert r.returncode == 0, r.stderr

    def test_non_gated_tool_passes_through(self, tmp_project):
        proj = tmp_project("empty-project")
        payload = {
            "tool_name": "Read",
            "tool_input": {"file_path": "src/foo.ts"},
            "cwd": str(proj),
        }
        r = run_gate(payload, proj)
        assert r.returncode == 0

    def test_edit_inside_blacklist_allowed_even_without_artifacts(self, tmp_project):
        proj = tmp_project("empty-project")
        r = run_gate(edit_payload(proj, ".ai/CONCEPT.md"), proj)
        assert r.returncode == 0


class TestDenyPaths:
    def test_phase_gate_denies_when_concept_missing(self, tmp_project):
        proj = tmp_project("empty-project")
        r = run_gate(edit_payload(proj, "src/auth.ts"), proj)
        assert r.returncode == 2
        assert "phase_gate" in r.stderr
        assert "CONCEPT.md" in r.stderr

    def test_protected_paths_denies_business_extension(self, tmp_project):
        proj = tmp_project("full-artifacts")
        r = run_gate(edit_payload(proj, "99_Business_Extension/policy.md"), proj)
        assert r.returncode == 2
        assert "protected_paths" in r.stderr

    def test_stderr_format_contains_all_fields(self, tmp_project):
        proj = tmp_project("empty-project")
        r = run_gate(edit_payload(proj, "src/x.ts"), proj)
        assert r.returncode == 2
        assert "denied:" in r.stderr
        assert "tool:" in r.stderr
        assert "target:" in r.stderr
        assert "reason:" in r.stderr
        assert "bypass:" in r.stderr


class TestBypassFlow:
    def test_bypass_without_reason_still_denies(self, tmp_project):
        proj = tmp_project("empty-project")
        r = run_gate(
            edit_payload(proj, "src/x.ts"), proj, env_extra={"BUTLER_BYPASS": "1"}
        )
        assert r.returncode == 2
        assert "bypass-reason.md" in r.stderr

    def test_bypass_with_reason_allows(self, tmp_project):
        proj = tmp_project("with-bypass-reason")
        # with-bypass-reason fixture includes all three artifacts too; to actually
        # exercise bypass we write to a protected path instead.
        r = run_gate(
            edit_payload(proj, "99_Business_Extension/policy.md"),
            proj,
            env_extra={"BUTLER_BYPASS": "1"},
        )
        assert r.returncode == 0, r.stderr
        log = (proj / ".ai" / "RUN_LOG.md").read_text()
        assert "protected_paths" in log

    def test_bypass_with_empty_reason_denies(self, tmp_project):
        proj = tmp_project("with-bypass-reason")
        (proj / ".ai" / "bypass-reason.md").write_text("")
        r = run_gate(
            edit_payload(proj, "99_Business_Extension/policy.md"),
            proj,
            env_extra={"BUTLER_BYPASS": "1"},
        )
        assert r.returncode == 2


class TestFailClosed:
    def test_malformed_stdin_fails_closed(self, tmp_project):
        proj = tmp_project("full-artifacts")
        env = os.environ.copy()
        env.pop("BUTLER_BYPASS", None)
        r = subprocess.run(
            [sys.executable, str(GATE)],
            input="this is not json",
            capture_output=True,
            text=True,
            env=env,
            cwd=str(proj),
        )
        assert r.returncode == 2
        assert "internal error" in r.stderr

    def test_missing_tool_name_passes_through(self, tmp_project):
        proj = tmp_project("empty-project")
        r = run_gate({"tool_input": {}}, proj)
        # No tool_name → not in GATED_TOOLS → exit 0
        assert r.returncode == 0
```

- [ ] **Step 3: 运行集成测试**

Run: `cd templates/hooks && python3 -m pytest tests/test_integration.py -v`
Expected: 所有 test 通过（~11 个）

- [ ] **Step 4: 运行全部测试，确认全绿**

Run: `cd templates/hooks && python3 -m pytest tests/ -v`
Expected: 全部测试通过（~55 个）

- [ ] **Step 5: 提交**

```bash
git add templates/hooks/butler_gate.py templates/hooks/tests/test_integration.py
git commit -m "feat(hook-gate): add butler_gate dispatcher with integration tests"
```

---

## Task 8: `smoke.sh` + `settings.hooks-snippet.json`

**Files:**
- Create: `templates/hooks/tests/smoke.sh`
- Create: `templates/settings.hooks-snippet.json`

- [ ] **Step 1: 创建 settings.hooks-snippet.json**

Write `templates/settings.hooks-snippet.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/butler_gate.py"
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 2: 验证 JSON 合法**

Run: `python3 -c "import json; json.load(open('templates/settings.hooks-snippet.json'))"`
Expected: 无输出，返回 0

- [ ] **Step 3: 创建 smoke.sh**

Write `templates/hooks/tests/smoke.sh`:

```bash
#!/usr/bin/env bash
# Tier 3 end-to-end smoke test for butler_gate.py.
# Not part of pytest — runs hook as a real subprocess with crafted stdin.
# Expected to be run manually after changing hook code.
set -euo pipefail

HOOKS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GATE="${HOOKS_DIR}/butler_gate.py"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "[smoke] tmp project: $TMP"

mkdir -p "$TMP/.ai"
cd "$TMP"

# --- Case 1: missing artifacts + gated path → expect exit 2 ---
echo "[smoke] case 1: gated path, no artifacts"
set +e
OUTPUT=$(echo '{"tool_name":"Edit","tool_input":{"file_path":"src/x.ts"},"cwd":"'"$TMP"'"}' \
  | python3 "$GATE" 2>&1)
RC=$?
set -e
if [[ $RC -ne 2 ]]; then
  echo "[smoke] FAIL: expected exit 2, got $RC"
  echo "$OUTPUT"
  exit 1
fi
if ! grep -q "phase_gate" <<<"$OUTPUT"; then
  echo "[smoke] FAIL: stderr did not mention phase_gate"
  echo "$OUTPUT"
  exit 1
fi
echo "[smoke] case 1 OK"

# --- Case 2: artifacts present + gated path → expect exit 0 ---
echo "[smoke] case 2: gated path, artifacts present"
printf "# CONCEPT\nstub\n" > .ai/CONCEPT.md
printf "# AC_LIST\nstub\n" > .ai/AC_LIST.md
printf "# TECH_PLAN\nstub\n" > .ai/TECH_PLAN.md
set +e
echo '{"tool_name":"Edit","tool_input":{"file_path":"src/x.ts"},"cwd":"'"$TMP"'"}' \
  | python3 "$GATE"
RC=$?
set -e
if [[ $RC -ne 0 ]]; then
  echo "[smoke] FAIL: expected exit 0, got $RC"
  exit 1
fi
echo "[smoke] case 2 OK"

# --- Case 3: bypass with reason → expect exit 0 + RUN_LOG entry ---
echo "[smoke] case 3: bypass with reason for protected path"
printf "hotfix reason\n" > .ai/bypass-reason.md
set +e
BUTLER_BYPASS=1 \
  echo '{"tool_name":"Edit","tool_input":{"file_path":"99_Business_Extension/x.md"},"cwd":"'"$TMP"'"}' \
  | env BUTLER_BYPASS=1 python3 "$GATE"
RC=$?
set -e
if [[ $RC -ne 0 ]]; then
  echo "[smoke] FAIL: expected exit 0 under bypass, got $RC"
  exit 1
fi
if ! grep -q "protected_paths" .ai/RUN_LOG.md; then
  echo "[smoke] FAIL: RUN_LOG.md missing protected_paths entry"
  cat .ai/RUN_LOG.md
  exit 1
fi
echo "[smoke] case 3 OK"

echo "[smoke] ALL PASS"
```

- [ ] **Step 4: 设置 smoke.sh 为可执行并运行**

Run:
```bash
chmod +x templates/hooks/tests/smoke.sh
bash templates/hooks/tests/smoke.sh
```
Expected: 最后输出 `[smoke] ALL PASS`

- [ ] **Step 5: 提交**

```bash
git add templates/hooks/tests/smoke.sh templates/settings.hooks-snippet.json
git commit -m "feat(hook-gate): add smoke script and PreToolUse settings snippet"
```

---

## Task 9: `templates/hooks/README.md`

**Files:**
- Create: `templates/hooks/README.md`

- [ ] **Step 1: 写 README**

Write `templates/hooks/README.md`:

```markdown
---
title: Butler Hook Gate — 贡献者说明
audience: 开发者
scope: templates/hooks/ 的结构、运行机制、测试与应急流程
---

# Butler Hook Gate

`templates/hooks/` 是 butler 的 Claude Code PreToolUse hook SSOT。`mcv-deployment.md` 协议在部署目标项目时，把这里除 `tests/` 外的内容拷到目标 `.claude/hooks/`，并把 `../settings.hooks-snippet.json` 合并进目标 `.claude/settings.json`。

## 目录结构

```txt
butler_gate.py           # PreToolUse 入口
rules/
  protected_paths.py     # 拦 99_Business_Extension/
  phase_gate.py          # 拦源码路径在 P1/P2/P3 产物缺失时
  artifact_chain.py      # 占位，未来承载 AC-ID linkage 等规则
lib/
  io.py                  # Context, Decision, parse_stdin, resolve_target, is_gated, GATED_BLACKLIST
  bypass.py              # BUTLER_BYPASS 评估 + RUN_LOG 追加
tests/                   # 本目录的测试（不分发到目标项目）
```

## 运行机制

1. Claude Code 在 `Edit` / `Write` / `MultiEdit` 前通过 PreToolUse 调用 `python3 .claude/hooks/butler_gate.py`，stdin 传入 JSON。
2. Dispatcher 顺序执行 `RULE_MODULES`（`protected_paths → phase_gate → artifact_chain`），任一 `deny` 即终止。
3. `deny` 后走 `lib/bypass.py`：若 `BUTLER_BYPASS=1` 且 `.ai/bypass-reason.md` 非空，追加 `.ai/RUN_LOG.md` 后放行；否则 `exit 2` + stderr 给 AI 可读的违规摘要。
4. 任何未捕获异常由 dispatcher 顶层 catch，`exit 2`（**fail-closed**）。

## 退出码契约

| exit | 含义 |
|---|---|
| 0 | 放行（允许工具执行） |
| 2 | 拒绝（含规则 deny 与 internal error） |

## Bypass 流程

```bash
# 在目标项目根
echo "hotfix: XYZ in prod, will supplement AC after" > .ai/bypass-reason.md
BUTLER_BYPASS=1 claude ...     # 或直接在该 shell 里用 Claude Code
```

- `bypass-reason.md` **不会**被 hook 自动清理；同一会话内多次 bypass 会复用同一 reason 并在 `RUN_LOG.md` 留多条记录。
- 绕过 **会被 git 看见**（RUN_LOG 是追加历史），review 时可追问。

## Fail-closed 与应急流程

若 hook 自身有 bug 把你锁死（所有 Edit/Write 都 `exit 2`）：

1. 写 `.ai/bypass-reason.md`（非空）并设 `BUTLER_BYPASS=1` 绕过。
2. 在 butler 仓库提 issue，贴 stderr 里的 `internal error` 回溯。

## 本地测试

改 hook 后必须跑：

```bash
cd templates/hooks
python3 -m pytest tests/         # Tier 1 + Tier 2
bash tests/smoke.sh              # Tier 3（可选，不入 CI）
```

## 已测试的 Claude Code 版本

- 待补（首次部署后验证过的版本号写在这里）

## 平台支持

- macOS、Linux
- Windows 不在本 phase 范围
```

- [ ] **Step 2: 提交**

```bash
git add templates/hooks/README.md
git commit -m "docs(hook-gate): add contributor README for templates/hooks/"
```

---

## Task 10: 更新 `mcv-deployment.md` 与 `Coder/README.md`

**Files:**
- Modify: `Coder/20_Workflow_Lifecycle/mcv-deployment.md`
- Modify: `Coder/README.md`

- [ ] **Step 1: 读 mcv-deployment.md 当前结构，准备插入点**

Run: `grep -n "^## " Coder/20_Workflow_Lifecycle/mcv-deployment.md`
Expected: 看到类似 `## 0. Butler 路径发现`、`## 1. 落地前侦察`、`## 2. 基础设施展开`、`## 3. 规则注入`、`## 4. 本地化适配` 的章节标题。

- [ ] **Step 2: 在 "4. 本地化适配" 之后插入 "5. Hook 注入"**

Edit `Coder/20_Workflow_Lifecycle/mcv-deployment.md`，在 "4. 本地化适配" 章节末尾（文件末尾）追加：

```markdown

## 5. Hook 注入 (Hook Injection)

把 butler 的 PreToolUse hook 体系部署到目标项目的 `.claude/`。Hook 提供机制化的流程约束——源码路径写操作在 P1/P2/P3 产物缺失时被拦截、`99_Business_Extension/` 写操作被拦截，绕过需显式 `BUTLER_BYPASS=1` + `.ai/bypass-reason.md`（非空）。

### 5.1 文件拷贝

将 `$BUTLER/templates/hooks/` 除 `tests/` 子目录外的内容全部拷贝到 `<target>/.claude/hooks/`：

- `butler_gate.py`
- `rules/` 整目录
- `lib/` 整目录
- `README.md`

若目标目录已存在同名文件，**以 butler 版本为准覆盖**（目标项目的 hooks 是 butler 的拷贝副本，不得本地改动；本地化需求应回流到 butler 仓库）。

### 5.2 settings.json 幂等合并

读 `$BUTLER/templates/settings.hooks-snippet.json`，合并进 `<target>/.claude/settings.json`：

1. 若目标 `settings.json` 不存在 → 直接写入 snippet 内容。
2. 若存在但无 `hooks.PreToolUse` 数组 → 添加 `hooks.PreToolUse = [snippet 中的条目]`。
3. 若已有 `hooks.PreToolUse` 数组 → 检查是否已有 `matcher == "Edit|Write|MultiEdit"` 且 `command` 以 `python3 .claude/hooks/butler_gate.py` 结尾的条目；已有则跳过，否则追加。

合并规则的去重键：`hooks.PreToolUse[*].matcher` 字面比较；AI 执行此步骤时必须幂等，重复部署不重复插入。

### 5.3 验证

部署完成后，在目标项目根执行：

```bash
echo '{"tool_name":"Edit","tool_input":{"file_path":"src/x.ts"},"cwd":"'"$(pwd)"'"}' \
  | python3 .claude/hooks/butler_gate.py
echo "exit=$?"
```

- 若 `.ai/CONCEPT.md` 等产物尚未产生 → 期望 `exit=2` 且 stderr 含 `phase_gate`。
- 这条验证命令写入部署报告。

### 5.4 与 butler-upgrade 的联动（Follow-up）

Hook 副本与 butler 仓库版本可能漂移。`butler-upgrade.md` 协议需要扩展以检测并同步 hook 副本；本协议本身只负责**首次部署路径**，不处理升级。
```

- [ ] **Step 3: 更新 butler 根 CLAUDE.md 的 templates/ 职责说明**

> 说明：spec §10 交付清单提到更新 `Coder/README.md`，但 `Coder/README.md` 的 scope 只覆盖 `Coder/` 子系统（如 `00_System_Prompt/`、`20_Workflow_Lifecycle/` 等），不跟踪 `templates/`。新增 hook 体系属于 `templates/` 下的内容，正确的登记位置是 butler 根 `CLAUDE.md`。

Edit `/Users/cyborgno2/Documents/WorkCode.nosync/butler/CLAUDE.md`：

找到行：
```
- `templates/` — 目标项目使用的 CLAUDE.md 模板与浓缩规则卡
```

替换为：
```
- `templates/` — 目标项目使用的 CLAUDE.md 模板、浓缩规则卡与 hook 体系（`hooks/`、`settings.hooks-snippet.json`）
```

不动 `Coder/README.md`。

- [ ] **Step 4: 再跑一次全量测试确保没退化**

Run: `cd templates/hooks && python3 -m pytest tests/ -v`
Expected: 全部通过（~55 个）

- [ ] **Step 5: 提交**

```bash
git add Coder/20_Workflow_Lifecycle/mcv-deployment.md CLAUDE.md
git commit -m "docs(hook-gate): register hook injection in mcv-deployment and CLAUDE.md"
```

---

## 完成条件

执行完全部 10 个 task 后，以下应全部满足：

- [ ] `cd templates/hooks && python3 -m pytest tests/ -v` 全绿（≥55 tests）
- [ ] `bash templates/hooks/tests/smoke.sh` 输出 `[smoke] ALL PASS`
- [ ] `python3 -c "import json; json.load(open('templates/settings.hooks-snippet.json'))"` 无错
- [ ] `Coder/20_Workflow_Lifecycle/mcv-deployment.md` 包含 "## 5. Hook 注入" 章节
- [ ] 仓库根 CLAUDE.md 的 `templates/` 职责说明已扩充
- [ ] git log 有 10 次 feat/docs 提交，顺序对应 Task 1–10

执行完后：

1. 用 `/mcv-deploy` 或手工流程在一个 tmp 项目部署一次，按 `mcv-deployment.md` §5.3 的验证命令跑一遍，确认端到端 OK。
2. 如果验证发现 bug，**不 amend 已提交的 task commits**；新开 bugfix commit。
