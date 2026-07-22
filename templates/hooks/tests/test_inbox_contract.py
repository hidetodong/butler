from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[3]
SCHEMA = ROOT / "Coder/40_Context_Management/inbox-schema.md"


class InboxContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SCHEMA.read_text(encoding="utf-8")

    def test_sources_and_derivations_fields(self) -> None:
        for marker in ("### 2.1 Sources", "### 2.2 Derivations", "source_revision", "observed_sha256", "processed_sha256", "actual_route", "artifact_ref", "relation"):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_source_identity_is_not_content_hash(self) -> None:
        self.assertIn("`source_id` 不等于内容 hash", self.text)
        self.assertIn("`SRC-NNNN`", self.text)
        self.assertIn("永不因内容、标题、文件名或外部 revision 变化而改变", self.text)

    def test_fingerprint_inputs_are_deterministic(self) -> None:
        self.assertIn("磁盘文件**原始字节**", self.text)
        self.assertIn("`CRLF` / `CR` 规范成 `LF`", self.text)
        self.assertIn("不 trim、不 case-fold、不改 Unicode", self.text)
        self.assertIn("不得用 mtime、大小、路径", self.text)
        self.assertIn("可变 revision / etag 只写 `source_revision`", self.text)
        self.assertIn("不得拼进稳定 locator", self.text)

    def test_status_enum_is_closed(self) -> None:
        expected = ["unprocessed", "analyzed", "awaiting-confirmation", "routed", "ignored", "source-changed", "failed"]
        line = next(line for line in self.text.splitlines() if line.startswith("`unprocessed` /"))
        self.assertEqual(re.findall(r"`([^`]+)`", line), expected)
        self.assertIn("失败、仅分析或等待确认时不得推进 `processed_sha256`", self.text)

    def test_idempotency_and_change_rules(self) -> None:
        for marker in ("同 locator + 同 observed hash", "同 locator + hash 变化", "不同 locator + 同 hash", "同一关系重复回放", "不得写成功关系"):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_origin_is_strictly_read_only_and_ledger_is_thin(self) -> None:
        self.assertIn("不得新增、改写、格式化、重命名、移动、归档或删除", self.text)
        self.assertIn("不存完整原文、长摘录、认证信息", self.text)
        deployment = (ROOT / "Coder/20_Workflow_Lifecycle/mcv-deployment.md").read_text(encoding="utf-8")
        self.assertIn("inbox-schema.md", deployment)
        self.assertIn("不重命名不移动不归档不删除", deployment)

    def test_registered_and_human_guide_points_to_contract(self) -> None:
        self.assertIn("inbox-schema.md", (ROOT / "Coder/README.md").read_text(encoding="utf-8"))
        guide = (ROOT / "HUMAN_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn(".ai/INBOX.md", guide)
        self.assertIn("inbox-schema.md", guide)


if __name__ == "__main__":
    unittest.main()
