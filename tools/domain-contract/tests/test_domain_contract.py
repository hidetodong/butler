import copy
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

TOOL_ROOT = Path(__file__).parents[1]
ROOT = TOOL_ROOT.parents[1]

SPEC = importlib.util.spec_from_file_location(
    "domain_contract", TOOL_ROOT / "domain_contract.py"
)
dc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dc)


class DomainContractTests(unittest.TestCase):
    def setUp(self):
        self.registry = dc.load_registry(TOOL_ROOT)

    def assert_error(self, errors, token):
        self.assertTrue(
            any(token in error for error in errors),
            f"expected {token!r} in errors: {errors}",
        )

    def test_valid_registry_passes(self):
        ok, errors = dc.check(ROOT)
        self.assertTrue(ok, errors)
        self.assertEqual([], errors)

    def test_duplicate_id_fails(self):
        registry = copy.deepcopy(self.registry)
        registry["entries"][1]["id"] = registry["entries"][0]["id"]
        errors = dc._validate_entries(ROOT, registry)
        self.assert_error(errors, "duplicate id")

    def test_duplicate_owner_fails(self):
        registry = copy.deepcopy(self.registry)
        registry["entries"][0]["owner"] = ["Coder/a.md", "Coder/b.md"]
        errors = dc._validate_entries(ROOT, registry)
        self.assert_error(errors, "co-ownership forbidden")

    def test_unknown_context_fails(self):
        registry = copy.deepcopy(self.registry)
        registry["entries"][0]["context"] = "未知上下文"
        errors = dc._validate_entries(ROOT, registry)
        self.assert_error(errors, "unknown context")

    def test_unknown_contract_type_fails(self):
        registry = copy.deepcopy(self.registry)
        registry["entries"][0]["type"] = "未知种类"
        errors = dc._validate_entries(ROOT, registry)
        self.assert_error(errors, "unknown contract type")

    def test_missing_source_fails(self):
        registry = copy.deepcopy(self.registry)
        registry["entries"][0]["source"] = ""
        errors = dc._validate_entries(ROOT, registry)
        self.assert_error(errors, "missing source")

    def test_out_of_bounds_source_fails(self):
        outside = tempfile.TemporaryDirectory()
        try:
            marker = Path(outside.name) / "outside.md"
            marker.write_text("x", encoding="utf-8")
            rel = os.path.relpath(marker, ROOT)
            registry = copy.deepcopy(self.registry)
            registry["entries"][0]["source"] = rel
            errors = dc._validate_entries(ROOT, registry)
            self.assert_error(errors, "out-of-bounds")
        finally:
            outside.cleanup()

    def test_copy_payload_is_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["entries"][3]["values"] = ["pass", "fail", "defer", "skip"]
        errors = dc._validate_entries(ROOT, registry)
        self.assert_error(errors, "copy-type payload")

    def test_dangling_relation_fails(self):
        registry = copy.deepcopy(self.registry)
        registry["relations"].append({"kind": "并列", "left": "ghost", "right": "dangerous-mode"})
        errors = dc._validate_relations(registry)
        self.assert_error(errors, "dangling")

    def test_containment_assertion_fails_with_reason(self):
        registry = copy.deepcopy(self.registry)
        registry["assertions"].append(
            {
                "file": "Coder/65_Extension_Dangerous/dangerous-engine.md",
                "must_not_contain": ["bounded-convergence.md"],
                "reason": "Dangerous 必须引用共享有界收敛策略",
            }
        )
        errors = dc._validate_assertions(ROOT, registry)
        self.assert_error(errors, "must not contain")
        self.assert_error(errors, "共享有界收敛策略")

    def test_human_section_assertion_fails_with_reason(self):
        registry = copy.deepcopy(self.registry)
        registry["assertions"].append(
            {
                "file": "tools/artifact-pipeline/templates/VERIFY_REPORT.md",
                "must_contain": ["## 不存在的段"],
                "reason": "人测道小结结构由模板拥有",
            }
        )
        errors = dc._validate_assertions(ROOT, registry)
        self.assert_error(errors, "must contain")
        self.assert_error(errors, "人测道小结结构由模板拥有")


if __name__ == "__main__":
    unittest.main()
