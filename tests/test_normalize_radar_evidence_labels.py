from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import ModuleType


def load_normalizer() -> ModuleType:
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "normalize-radar-evidence-labels.py"
    spec = importlib.util.spec_from_file_location("normalize_radar_evidence_labels", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load normalize-radar-evidence-labels.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


normalizer = load_normalizer()


class NormalizeRadarEvidenceLabelsTest(unittest.TestCase):
    def test_spec_path_e1_is_downgraded_to_e3(self) -> None:
        text = "- E1 source verified: OpenLineage schema evidence in `spec/OpenLineage.json`.\n"

        normalized, changed = normalizer.normalize_text(text)

        self.assertEqual(1, changed)
        self.assertEqual("- E3 maintainer stated: OpenLineage schema evidence in `spec/OpenLineage.json`.\n", normalized)

    def test_test_path_e1_is_downgraded_to_e2(self) -> None:
        text = "- E1 source verified: recovery behavior is covered by `tests/test_recovery.py`.\n"

        normalized, changed = normalizer.normalize_text(text)

        self.assertEqual(1, changed)
        self.assertEqual("- E2 test verified: recovery behavior is covered by `tests/test_recovery.py`.\n", normalized)

    def test_symbol_plus_spec_path_is_still_downgraded(self) -> None:
        text = "- E1 source verified: `OpenLineageAdapter` consumes `spec/OpenLineage.json`.\n"

        normalized, changed = normalizer.normalize_text(text)

        self.assertEqual(1, changed)
        self.assertEqual("- E3 maintainer stated: `OpenLineageAdapter` consumes `spec/OpenLineage.json`.\n", normalized)

    def test_mixed_implementation_and_spec_paths_are_left_for_validation(self) -> None:
        text = "- E1 source verified: flow links `src/openlineage.py` with `spec/OpenLineage.json`.\n"

        normalized, changed = normalizer.normalize_text(text)

        self.assertEqual(0, changed)
        self.assertEqual(text, normalized)

    def test_candidate_ledger_repository_url_alias_is_normalized(self) -> None:
        text = "\n".join(
            [
                "## Candidate Ledger",
                "",
                "| Repository | Repository URL | Commit | Discovery source | Family | Stage | Decision |",
                "|---|---|---|---|---|---|---|",
                "| `owner/repo` | https://github.com/owner/repo | `abc` | search | `ai-llm-systems` | triaged | selected |",
                "",
            ]
        )

        normalized, changed = normalizer.normalize_text(text)

        self.assertEqual(1, changed)
        self.assertIn("| Repository | URL | Commit | Discovery source | Family | Stage | Decision |", normalized)

    def test_candidate_ledger_without_url_like_alias_is_left_for_validation(self) -> None:
        text = "\n".join(
            [
                "## Candidate Ledger",
                "",
                "| Repository | Commit | Discovery source | Family | Stage | Decision |",
                "|---|---|---|---|---|---|",
                "| `owner/repo` | `abc` | search | `ai-llm-systems` | triaged | selected |",
                "",
            ]
        )

        normalized, changed = normalizer.normalize_text(text)

        self.assertEqual(0, changed)
        self.assertEqual(text, normalized)


if __name__ == "__main__":
    unittest.main()
