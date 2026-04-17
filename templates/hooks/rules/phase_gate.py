"""Rule: require P1/P2/P3 artifacts before gated source edits."""
from __future__ import annotations

from pathlib import Path

from lib.io import Context, Decision, OUT_OF_CWD, is_gated

RULE_ID = "phase_gate"

REQUIRED_ARTIFACTS = [
    (".ai/CONCEPT.md", "P1", "先完成 P1 分析并产出 .ai/CONCEPT.md"),
    (".ai/AC_LIST.md", "P2", "先完成 P2 验收清单并产出 .ai/AC_LIST.md"),
    (".ai/TECH_PLAN.md", "P3", "先完成 P3 技术方案并产出 .ai/TECH_PLAN.md"),
]


def evaluate(ctx: Context) -> Decision:
    if not is_gated(ctx.target_path):
        return Decision(verdict="allow", rule_id=RULE_ID)

    # Conservative: OUT_OF_CWD writes can never satisfy the artifact check.
    if ctx.target_path == OUT_OF_CWD:
        return Decision(
            verdict="deny",
            rule_id=RULE_ID,
            reason="目标路径超出项目 cwd，无法校验阶段产物",
            remediation="请将写操作指向项目内路径",
        )

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
