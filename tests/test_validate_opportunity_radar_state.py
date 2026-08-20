from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-opportunity-radar-state.py"

spec = importlib.util.spec_from_file_location("validate_opportunity_radar_state", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


PAID_WEDGE = "Teams pay to reduce engineering time spent reconstructing failed agent runs."
DISTRIBUTION_CHANNEL = "CLI installed from GitHub or PyPI and run locally against exported traces."
DO_NOT_BUILD_UNTIL = "Three teams agree to run the audit on real traces or one team asks for a paid follow-up."
BUYER = "Engineering managers responsible for production agent reliability."
EXISTING_SPEND = "Teams already spend engineering hours manually reading traces and reconstructing failed runs."
PAID_EXPERIMENT = "Offer a $49 manual trace audit to three agent teams and treat one paid request as validation."
SOURCE_CLASSES = ["github", "forum"]
TECHNOLOGY_SHIFT = {
    "what_changed": "Agent traces became common enough that small teams need repeatable debugging workflows.",
    "when": "2026-08-11",
    "old_constraint": "Trace debugging required ad hoc logs and custom scripts.",
    "new_capability": "A lightweight audit can summarize failures and recovery paths.",
    "cost_delta": "Manual review time can be reduced if the report is accepted.",
    "quality_delta": "Debugging output becomes more consistent across incidents.",
    "latency_delta": "Initial triage can happen before a full engineering investigation.",
    "accessibility_delta": "Public examples and exported traces make a first test reachable.",
    "affected_workflows": ["Agent incident debugging", "Trace review"],
}
STRUCTURAL_PATTERN = "Diagnostic control layer for fragmented agent trace, runtime, and checkpoint debugging workflows."
PRIMITIVE_GROWTH = "Agent runtimes, tracing exports, checkpoint savers, and observability tools are now common enough to create operational fragmentation."
FRAGMENTATION_SUMMARY = "Failure evidence is split across traces, checkpoints, logs, issue threads, and local configuration, so teams compare signals manually."
MANUAL_WORKFLOW = "Engineers manually inspect exported traces, checkpoint metadata, logs, and issue references to reconstruct failed agent runs."
OBJECTIVE_FUNCTION = "Minimize incident triage time and duplicated agent work while preserving replay correctness."
EXECUTION_LADDER = {
    "observe": "Read exported traces, checkpoint metadata, runtime logs, and relevant configuration files.",
    "recommend": "Explain likely failure modes and suggest safer trace or checkpoint review actions.",
    "choose": "Rank debugging paths by incident impact, confidence, and engineering effort.",
    "execute": "Generate a local audit report only; automatic runtime mutation is outside the first wedge.",
}
ECONOMIC_PAIN = "Engineering time is spent reconstructing failures, repeated tool calls, and unreliable replay behavior instead of fixing the incident."
TIMING_REASON = "Agent runtime adoption and trace exports are now common enough that small teams need repeatable diagnostics."
COMPETITORS = ["manual trace review", "observability dashboards", "custom debug scripts"]
STRUCTURAL_SCORES = {
    "fragmentation": 4,
    "manual_pain": 4,
    "economic_value": 3,
    "objective_measurability": 3,
    "execution_potential": 3,
    "timing": 3,
    "competition_gap": 3,
    "prototype_feasibility": 4,
    "total": 7,
}
FRAGMENTED_PROVIDERS = "Agent runtimes, trace stores, checkpoint savers, and observability tools create fragmented operational surfaces."
MULTI_PROVIDER_USER = "Small agent teams use runtime libraries, hosted traces, storage backends, and issue workflows across multiple providers."
BOUNDARY_WORKFLOW = "Engineers reconcile traces, checkpoints, logs, storage costs, and runtime settings across provider boundaries."
BUILD_VS_BUY_REASON = "Teams buy because incident diagnostics are repeated operational glue rather than core model or product IP."
INTERNAL_BUILD_LIKELIHOOD = "medium"
MONEY_FLOW = "Budget already flows to agent platforms, observability tools, and engineering incident response time."
RECURRENCE = "The workflow recurs whenever teams ship new agents, change savers, or investigate production incidents."
PERMISSIONLESS_VALIDATION = "A first audit can use public examples, synthetic traces, and exported local runs without private customer data."
SMALLEST_WEDGE = "Checkpoint and trace audit report for one failed workflow, not a platform or marketplace."
INTERMEDIARY_MATURITY = "Existing observability tools help, but a narrow cross-tool incident audit layer is still immature."


def complete_report(
    selected: bool = True,
    *,
    topic_coverage: str | None = None,
    commercial_delta: str | None = None,
) -> str:
    selected_text = "- Agent trace debugging for small teams, backed by `M2 repeated pain`."
    reviews = "The opportunity has repeated public issue evidence. `M2 repeated pain`."
    build_readiness = "\n".join(
        [
            "| Opportunity | Paid wedge | Distribution channel | Private data barrier | OSS commoditization risk | Product shape | Pricing hypothesis | Do not build until | Build decision |",
            "|---|---|---|---|---|---|---|---|---|",
            f"| Agent trace debugging | {PAID_WEDGE} | {DISTRIBUTION_CHANNEL} | `public-only` | `medium` | `cli` | `team` | {DO_NOT_BUILD_UNTIL} | `selected-for-test` |",
        ]
    )
    money_readiness = "\n".join(
        [
            "| Opportunity | Pain | Spend | Reachability | Timing | Buildability | Buyer | Existing spend | Paid experiment | Source classes | Stage |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
            f"| Agent trace debugging | 5 | 2 | 3 | 3 | 4 | {BUYER} | {EXISTING_SPEND} | {PAID_EXPERIMENT} | github, forum | `selected-for-test` |",
        ]
    )
    structural_ranking = "\n".join(
        [
            "| Rank | Opportunity | Ecosystem | Score | Why now | Manual workflow | Wedge |",
            "|---|---|---|---|---|---|---|",
            f"| 1 | Agent trace debugging | Agent runtime observability | 7 | {TIMING_REASON} | {MANUAL_WORKFLOW} | {PAID_WEDGE} |",
        ]
    )
    structural_scores = "\n".join(
        [
            "| Opportunity | Fragmentation | Manual pain | Economic value | Objective measurability | Execution potential | Timing | Competition gap | Prototype feasibility | Total |",
            "|---|---|---|---|---|---|---|---|---|---|",
            "| Agent trace debugging | 4 | 4 | 3 | 3 | 3 | 3 | 3 | 4 | 7 |",
        ]
    )
    commercial_filter = "\n".join(
        [
            "| Opportunity | Fragmented providers | Multi-provider user | Boundary workflow | Build-vs-buy | Internal build likelihood | Money flow | Permissionless validation | Smallest wedge | Decision |",
            "|---|---|---|---|---|---|---|---|---|---|",
            f"| Agent trace debugging | {FRAGMENTED_PROVIDERS} | {MULTI_PROVIDER_USER} | {BOUNDARY_WORKFLOW} | {BUILD_VS_BUY_REASON} | `{INTERNAL_BUILD_LIKELIHOOD}` | {MONEY_FLOW} | {PERMISSIONLESS_VALIDATION} | {SMALLEST_WEDGE} | `selected-for-test` |",
        ]
    )
    if topic_coverage is None:
        topic_coverage = "\n".join(
            [
                "| Family | Signals reviewed | Best candidate | Decision | Reason |",
                "|---|---:|---|---|---|",
                "| `ai-llm-demand` | 1 | Agent trace debugging | selected-for-test | Repeated agent debugging pain has enough public support for a manual test. |",
            ]
        )
    if commercial_delta is None:
        commercial_delta = "\n".join(
            [
                "| Opportunity | Previous stage | Current stage | Commercial delta | Decision |",
                "|---|---|---|---|---|",
                "| Agent trace debugging | none | selected-for-test | New candidate for this run with no previous selected state. | selected-for-test |",
            ]
        )
    if not selected:
        selected_text = "None."
        reviews = "No selected opportunities."
        build_readiness = "None."
        money_readiness = "None."
        structural_ranking = "None."
        structural_scores = "None."
        commercial_filter = "None."

    sections = {
        "Prerequisites And State": "- workspace verified",
        "Signal Counts": "- `triaged`: 1",
        "Selected Opportunities": selected_text,
        "Executive Summary": "One demand signal was reviewed.",
        "Signal Ledger": "\n".join(
            [
                "| Source | URL | Family | Signal type | Evidence label | Decision | Reason |",
                "|---|---|---|---|---|---|---|",
                "| GitHub issue | https://example.com/issue | `ai-llm-demand` | `repeated-pain` | `M2 repeated pain` | selected | Repeated agent debugging pain. |",
            ]
        ),
        "Topic Coverage": topic_coverage,
        "Commercial Delta": commercial_delta,
        "Structural Candidate Ranking": structural_ranking,
        "Structural Score Breakdown": structural_scores,
        "Commercial Filter": commercial_filter,
        "Opportunity Reviews": reviews,
        "Build Readiness": build_readiness,
        "Money Readiness": money_readiness,
        "Recommended Next Test": "Interview three teams and offer a trace-debugging report.",
        "Rejected Or Deferred Signals": "- None.",
        "Evidence Gaps": "- No paid demand yet.",
    }

    body = ["# Opportunity Radar Report: 2026-08-11", ""]
    for heading, content in sections.items():
        body.extend([f"## {heading}", "", content, ""])
    return "\n".join(body)


def complete_state(
    *,
    array_name: str = "selected",
    stage: str = "selected-for-test",
    paid_wedge: str = PAID_WEDGE,
    spend_score: int = 2,
    reachability_score: int = 3,
    source_classes: list[str] | None = None,
    paid_experiment: str = PAID_EXPERIMENT,
    structural_scores: dict[str, int] | None = None,
    manual_workflow: str = MANUAL_WORKFLOW,
    internal_build_likelihood: str = INTERNAL_BUILD_LIKELIHOOD,
    multi_provider_user: str = MULTI_PROVIDER_USER,
    money_flow: str = MONEY_FLOW,
    permissionless_validation: str = PERMISSIONLESS_VALIDATION,
    smallest_wedge: str = SMALLEST_WEDGE,
) -> str:
    data: dict[str, object] = {
        "schema_version": 1,
        "discovery_mode": "watchlist-directed",
        "selected": [],
        "deferred": [],
        "watchlisted": [],
    }
    entry = {
        "id": "agent-trace-debugging",
        "family": "ai-llm-demand",
        "title": "Agent trace debugging",
        "file": "opportunities/agent-trace-debugging.md",
        "stage": stage,
        "score": 7,
        "pain_score": 5,
        "spend_score": spend_score,
        "reachability_score": reachability_score,
        "timing_score": 3,
        "buildability_score": 4,
        "confidence": "medium",
        "money_signal": "weak",
        "reachability": "high",
        "evidence_count": 3,
        "next_test": "Offer a manual trace debugging report to three agent teams.",
        "technology_shift": TECHNOLOGY_SHIFT,
        "buyer": BUYER,
        "expensive_workflow": "Engineers lose time manually reconstructing failed agent runs from traces.",
        "existing_spend": EXISTING_SPEND,
        "paid_experiment": paid_experiment,
        "source_classes": source_classes or SOURCE_CLASSES,
        "structural_pattern": STRUCTURAL_PATTERN,
        "primitive_growth": PRIMITIVE_GROWTH,
        "fragmentation_summary": FRAGMENTATION_SUMMARY,
        "manual_workflow": manual_workflow,
        "objective_function": OBJECTIVE_FUNCTION,
        "execution_ladder": EXECUTION_LADDER,
        "economic_pain": ECONOMIC_PAIN,
        "timing_reason": TIMING_REASON,
        "competitors": COMPETITORS,
        "structural_scores": structural_scores or STRUCTURAL_SCORES,
        "fragmented_providers": FRAGMENTED_PROVIDERS,
        "multi_provider_user": multi_provider_user,
        "boundary_workflow": BOUNDARY_WORKFLOW,
        "build_vs_buy_reason": BUILD_VS_BUY_REASON,
        "internal_build_likelihood": internal_build_likelihood,
        "money_flow": money_flow,
        "recurrence": RECURRENCE,
        "permissionless_validation": permissionless_validation,
        "smallest_wedge": smallest_wedge,
        "intermediary_maturity": INTERMEDIARY_MATURITY,
        "paid_wedge": paid_wedge,
        "distribution_channel": DISTRIBUTION_CHANNEL,
        "private_data_barrier": "public-only",
        "oss_commoditization_risk": "medium",
        "product_shape": "cli",
        "pricing_hypothesis": "team",
        "do_not_build_until": DO_NOT_BUILD_UNTIL,
        "labels": ["M2", "M4"],
    }
    items = data[array_name]
    assert isinstance(items, list)
    items.append(entry)
    return json.dumps(data)


def write_complete_state(
    root: Path,
    *,
    array_name: str = "selected",
    stage: str = "selected-for-test",
    paid_wedge: str = PAID_WEDGE,
    spend_score: int = 2,
    reachability_score: int = 3,
    source_classes: list[str] | None = None,
    paid_experiment: str = PAID_EXPERIMENT,
    structural_scores: dict[str, int] | None = None,
    manual_workflow: str = MANUAL_WORKFLOW,
    internal_build_likelihood: str = INTERNAL_BUILD_LIKELIHOOD,
    multi_provider_user: str = MULTI_PROVIDER_USER,
    money_flow: str = MONEY_FLOW,
    permissionless_validation: str = PERMISSIONLESS_VALIDATION,
    smallest_wedge: str = SMALLEST_WEDGE,
) -> None:
    (root / "opportunities.json").write_text(
        complete_state(
            array_name=array_name,
            stage=stage,
            paid_wedge=paid_wedge,
            spend_score=spend_score,
            reachability_score=reachability_score,
            source_classes=source_classes,
            paid_experiment=paid_experiment,
            structural_scores=structural_scores,
            manual_workflow=manual_workflow,
            internal_build_likelihood=internal_build_likelihood,
            multi_provider_user=multi_provider_user,
            money_flow=money_flow,
            permissionless_validation=permissionless_validation,
            smallest_wedge=smallest_wedge,
        ),
        encoding="utf-8",
    )


def complete_signal_note(url: str = "https://example.com/issue") -> str:
    return "\n".join(
        [
            "# Agent trace debugging signal note",
            "",
            "- Sources:",
            f"  - {url}",
            "- Date range: 2026-08-10 to 2026-08-11",
            "- Family: ai-llm-demand",
            "- Signal type: repeated-pain",
            "- Labels: M2 repeated pain, M4 workaround evidence",
            "- Notes: Repeated public issue comments show agent debugging pain that should be revisited later.",
            "",
        ]
    )


def write_topic_scope(root: Path, families: list[str] | None = None) -> None:
    families = families or ["ai-llm-demand"]
    docs = root / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "opportunity-research-scope.md").write_text(
        "## Topic Families\n\n" + "\n".join(f"- `{family}`" for family in families) + "\n",
        encoding="utf-8",
    )
    (root / "opportunity-interests.md").write_text(
        "# Opportunity Radar Interests\n\n"
        "Use these topic families for accounting:\n\n"
        + "\n".join(f"- `{family}`" for family in families)
        + "\n",
        encoding="utf-8",
    )


def write_signal_note(root: Path, url: str = "https://example.com/issue", families: list[str] | None = None) -> Path:
    write_topic_scope(root, families=families)
    signal = root / "signals" / "2026-08-11-agent-trace-debugging.md"
    signal.parent.mkdir(exist_ok=True)
    signal.write_text(complete_signal_note(url), encoding="utf-8")
    return signal


def complete_opportunity() -> str:
    sections = {
        "Opportunity Summary": "Trace-backed debugging reports for small agent teams.",
        "Evidence": "- `M2 repeated pain`: repeated public issues about debugging failed agent runs.",
        "Structural Pattern": STRUCTURAL_PATTERN,
        "Primitive Growth": PRIMITIVE_GROWTH,
        "Fragmentation": FRAGMENTATION_SUMMARY,
        "Manual Workflow": MANUAL_WORKFLOW,
        "Objective Function": OBJECTIVE_FUNCTION,
        "Execution Ladder": "\n".join(
            [
                "- Observe: Read exported traces, checkpoint metadata, runtime logs, and relevant configuration files.",
                "- Recommend: Explain likely failure modes and suggest safer trace or checkpoint review actions.",
                "- Choose: Rank debugging paths by incident impact, confidence, and engineering effort.",
                "- Execute: Generate a local audit report only; automatic runtime mutation is outside the first wedge.",
            ]
        ),
        "Economic Pain": ECONOMIC_PAIN,
        "Timing Reason": TIMING_REASON,
        "Competitors": "\n".join(f"- {competitor}" for competitor in COMPETITORS),
        "Structural Scores": "\n".join(
            [
                "- Fragmentation: 4",
                "- Manual pain: 4",
                "- Economic value: 3",
                "- Objective measurability: 3",
                "- Execution potential: 3",
                "- Timing: 3",
                "- Competition gap: 3",
                "- Prototype feasibility: 4",
                "- Total: 7",
            ]
        ),
        "Repeated Pain Or Demand Signal": "Teams repeatedly ask how to inspect failed agent runs.",
        "Likely User Or Buyer": "Engineering teams deploying multi-step LLM agents.",
        "Current Workaround Or Money Signal": "Teams use ad hoc logs and manual trace reading.",
        "Technology Shift": "Agent traces are common enough that lightweight incident audit workflows are now testable.",
        "Buyer": BUYER,
        "Expensive Workflow": "Engineers spend incident response time manually reconstructing failed agent runs.",
        "Existing Spend": EXISTING_SPEND,
        "Paid Experiment": PAID_EXPERIMENT,
        "Money-First Scores": "\n".join(
            [
                "- Pain: 5",
                "- Spend: 2",
                "- Reachability: 3",
                "- Timing: 3",
                "- Buildability: 4",
            ]
        ),
        "Source Classes": "github, forum",
        "Fragmented Providers": FRAGMENTED_PROVIDERS,
        "Multi-Provider User": MULTI_PROVIDER_USER,
        "Boundary Workflow": BOUNDARY_WORKFLOW,
        "Build-vs-buy Reason": BUILD_VS_BUY_REASON,
        "Internal Build Likelihood": INTERNAL_BUILD_LIKELIHOOD,
        "Money Flow": MONEY_FLOW,
        "Recurrence": RECURRENCE,
        "Permissionless Validation": PERMISSIONLESS_VALIDATION,
        "Smallest Wedge": SMALLEST_WEDGE,
        "Intermediary Maturity": INTERMEDIARY_MATURITY,
        "Paid Wedge": PAID_WEDGE,
        "Distribution Channel": DISTRIBUTION_CHANNEL,
        "Private Data Barrier": "public-only",
        "OSS Commoditization Risk": "medium",
        "Product Shape": "cli",
        "Pricing Hypothesis": "team",
        "Do Not Build Until": DO_NOT_BUILD_UNTIL,
        "Proposed Offer": "A manual trace audit report for one failed workflow.",
        "Success Threshold": "Three teams agree to share traces or pay for an audit.",
        "Falsification Threshold": "Teams decline because existing tools already solve it.",
        "Evidence Gaps": "No direct paid demand signal yet.",
        "Decision": "selected for manual test",
    }
    body = ["# Agent Trace Debugging Opportunity", ""]
    for heading, content in sections.items():
        body.extend([f"## {heading}", "", content, ""])
    return "\n".join(body)


class ValidateOpportunityRadarStateTest(unittest.TestCase):
    def test_markdown_sections_extracts_h2_sections(self) -> None:
        sections = validator.markdown_sections("intro\n\n## First\n\nalpha\n\n## Second\n\nbeta\n")

        self.assertEqual(sections["First"], "alpha")
        self.assertEqual(sections["Second"], "beta")

    def test_signal_ledger_accepts_required_columns_and_labels(self) -> None:
        ledger = "\n".join(
            [
                "| Source | URL | Family | Signal type | Evidence label | Decision | Reason |",
                "|---|---|---|---|---|---|---|",
                "| GitHub issue | https://example.com | `ai-llm-demand` | `repeated-pain` | `M2 repeated pain` | selected | Repeated pain. |",
            ]
        )

        validator.validate_signal_ledger(ROOT / "opportunity-reports" / "test.md", ledger)

    def test_signal_ledger_rejects_unsupported_label(self) -> None:
        ledger = "\n".join(
            [
                "| Source | URL | Family | Signal type | Evidence label | Decision | Reason |",
                "|---|---|---|---|---|---|---|",
                "| GitHub issue | https://example.com | `ai-llm-demand` | `repeated-pain` | `E3 maintainer stated` | selected | Wrong label. |",
            ]
        )

        with patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
            validator.validate_signal_ledger(ROOT / "opportunity-reports" / "test.md", ledger)

    def test_report_structure_accepts_complete_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(complete_report(), encoding="utf-8")
            write_complete_state(root)
            write_signal_note(root)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_missing_topic_coverage_family(self) -> None:
        topic_coverage = "\n".join(
            [
                "| Family | Signals reviewed | Best candidate | Decision | Reason |",
                "|---|---:|---|---|---|",
                "| `ai-llm-demand` | 1 | Agent trace debugging | selected-for-test | Repeated agent debugging pain has enough public support for a manual test. |",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(complete_report(topic_coverage=topic_coverage), encoding="utf-8")
            write_complete_state(root)
            write_signal_note(root, families=["ai-llm-demand", "blockchain-demand"])

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_repeated_selected_focus_without_commercial_delta(self) -> None:
        commercial_delta = "\n".join(
            [
                "| Opportunity | Previous stage | Current stage | Commercial delta | Decision |",
                "|---|---|---|---|---|",
                "| Agent trace debugging | selected-for-test | selected-for-test | Extra GitHub issues only; no new commercial delta. | main focus |",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(complete_report(commercial_delta=commercial_delta), encoding="utf-8")
            write_complete_state(root)
            write_signal_note(root)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch.object(validator, "read_base_opportunities_state", return_value=json.loads(complete_state())),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_report_structure_allows_repeated_selected_carried_forward_without_delta(self) -> None:
        commercial_delta = "\n".join(
            [
                "| Opportunity | Previous stage | Current stage | Commercial delta | Decision |",
                "|---|---|---|---|---|",
                "| Agent trace debugging | selected-for-test | selected-for-test | No new commercial delta; carried forward as an active experiment. | carried-forward |",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(complete_report(commercial_delta=commercial_delta), encoding="utf-8")
            write_complete_state(root)
            write_signal_note(root)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch.object(validator, "read_base_opportunities_state", return_value=json.loads(complete_state())),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_selected_without_market_evidence(self) -> None:
        bad_report = complete_report().replace("`M2 repeated pain`", "`H hypothesis`")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(bad_report, encoding="utf-8")
            write_complete_state(root)
            write_signal_note(root)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_missing_build_readiness(self) -> None:
        bad_report = complete_report().replace(
            "## Build Readiness\n\n"
            "| Opportunity | Paid wedge | Distribution channel | Private data barrier | OSS commoditization risk | Product shape | Pricing hypothesis | Do not build until | Build decision |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            "| Agent trace debugging | Teams pay to reduce engineering time spent reconstructing failed agent runs. | CLI installed from GitHub or PyPI and run locally against exported traces. | `public-only` | `medium` | `cli` | `team` | Three teams agree to run the audit on real traces or one team asks for a paid follow-up. | `selected-for-test` |\n\n",
            "",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(bad_report, encoding="utf-8")
            write_complete_state(root)
            write_signal_note(root)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_missing_money_readiness(self) -> None:
        bad_report = complete_report().replace(
            "## Money Readiness\n\n"
            f"| Opportunity | Pain | Spend | Reachability | Timing | Buildability | Buyer | Existing spend | Paid experiment | Source classes | Stage |\n"
            f"|---|---|---|---|---|---|---|---|---|---|---|\n"
            f"| Agent trace debugging | 5 | 2 | 3 | 3 | 4 | {BUYER} | {EXISTING_SPEND} | {PAID_EXPERIMENT} | github, forum | `selected-for-test` |\n\n",
            "",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(bad_report, encoding="utf-8")
            write_complete_state(root)
            write_signal_note(root)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_missing_structural_sections(self) -> None:
        bad_report = complete_report().replace(
            "## Structural Candidate Ranking\n\n"
            f"| Rank | Opportunity | Ecosystem | Score | Why now | Manual workflow | Wedge |\n"
            f"|---|---|---|---|---|---|---|\n"
            f"| 1 | Agent trace debugging | Agent runtime observability | 7 | {TIMING_REASON} | {MANUAL_WORKFLOW} | {PAID_WEDGE} |\n\n",
            "",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(bad_report, encoding="utf-8")
            write_complete_state(root)
            write_signal_note(root)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_structural_score_total_mismatch(self) -> None:
        bad_report = complete_report().replace("| Agent trace debugging | 4 | 4 | 3 | 3 | 3 | 3 | 3 | 4 | 7 |", "| Agent trace debugging | 4 | 4 | 3 | 3 | 3 | 3 | 3 | 4 | 8 |")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(bad_report, encoding="utf-8")
            write_complete_state(root)
            write_signal_note(root)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_commercial_filter_rejects_selected_with_high_internal_build(self) -> None:
        commercial_filter = "\n".join(
            [
                "| Opportunity | Fragmented providers | Multi-provider user | Boundary workflow | Build-vs-buy | Internal build likelihood | Money flow | Permissionless validation | Smallest wedge | Decision |",
                "|---|---|---|---|---|---|---|---|---|---|",
                f"| Agent trace debugging | {FRAGMENTED_PROVIDERS} | {MULTI_PROVIDER_USER} | {BOUNDARY_WORKFLOW} | {BUILD_VS_BUY_REASON} | `high` | {MONEY_FLOW} | {PERMISSIONLESS_VALIDATION} | {SMALLEST_WEDGE} | `selected-for-test` |",
            ]
        )

        with patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
            validator.validate_commercial_filter_table(ROOT / "opportunity-reports" / "test.md", commercial_filter)

    def test_report_structure_rejects_commercial_filter_field_mismatch(self) -> None:
        bad_report = complete_report().replace(MONEY_FLOW, "Budget path differs from the canonical state and should fail consistency checks.")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(bad_report, encoding="utf-8")
            write_complete_state(root)
            write_signal_note(root)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_build_readiness_rejects_selected_with_private_data_barrier(self) -> None:
        readiness = "\n".join(
            [
                "| Opportunity | Paid wedge | Distribution channel | Private data barrier | OSS commoditization risk | Product shape | Pricing hypothesis | Do not build until | Build decision |",
                "|---|---|---|---|---|---|---|---|---|",
                "| Agent trace debugging | Teams pay to reduce engineering time spent reconstructing failed agent runs. | CLI installed from GitHub or PyPI and run locally against exported traces. | `private-data-required` | `medium` | `cli` | `team` | Three teams agree to run the audit on real traces or one team asks for a paid follow-up. | `selected-for-test` |",
            ]
        )

        with patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
            validator.validate_build_readiness_table(ROOT / "opportunity-reports" / "test.md", readiness)

    def test_report_structure_rejects_build_readiness_missing_from_state(self) -> None:
        bad_report = complete_report().replace("Agent trace debugging |", "Unknown opportunity |")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(bad_report, encoding="utf-8")
            write_complete_state(root)
            write_signal_note(root)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_build_readiness_decision_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(complete_report(), encoding="utf-8")
            write_complete_state(root, stage="selected-for-build")
            write_signal_note(root)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_build_readiness_field_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(complete_report(), encoding="utf-8")
            write_complete_state(root, paid_wedge="Teams pay for a different validated debugging workflow.")
            write_signal_note(root)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_signal_url_missing_from_notes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(complete_report(), encoding="utf-8")
            write_complete_state(root)
            write_signal_note(root, "https://example.com/different-issue")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_signal_note_file_accepts_required_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            signal = write_signal_note(root)

            with patch.object(validator, "ROOT", root):
                self.assertEqual(validator.validate_signal_note_file(signal), {"https://example.com/issue"})

    def test_signal_note_file_rejects_missing_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            signal = write_signal_note(root)
            signal.write_text(complete_signal_note().replace("- Date range: 2026-08-10 to 2026-08-11\n", ""), encoding="utf-8")

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_signal_note_file(signal)

    def test_label_text_rejects_architecture_evidence_labels(self) -> None:
        with patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
            validator.validate_label_text(ROOT / "opportunity-reports" / "test.md", "Claim uses `E1 source verified`.")

    def test_selected_opportunity_file_requires_contract_and_market_label(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            opportunity = root / "opportunities" / "trace-debugging.md"
            opportunity.parent.mkdir()
            opportunity.write_text(complete_opportunity(), encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "changed_opportunity_files", return_value=[opportunity]),
            ):
                validator.validate_selected_opportunity_files()

    def test_selected_opportunity_file_rejects_build_selection_with_unclear_wedge(self) -> None:
        text = complete_opportunity().replace(
            "Teams pay to reduce engineering time spent reconstructing failed agent runs.",
            "unclear",
        ).replace("selected for manual test", "selected for build")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            opportunity = root / "opportunities" / "trace-debugging.md"
            opportunity.parent.mkdir()
            opportunity.write_text(text, encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "changed_opportunity_files", return_value=[opportunity]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_selected_opportunity_files()

    def test_selected_opportunity_file_rejects_selected_with_unclear_structural_workflow(self) -> None:
        text = complete_opportunity().replace(MANUAL_WORKFLOW, "unclear manual workflow").replace(
            "selected for manual test",
            "selected for test",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            opportunity = root / "opportunities" / "trace-debugging.md"
            opportunity.parent.mkdir()
            opportunity.write_text(text, encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "changed_opportunity_files", return_value=[opportunity]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_selected_opportunity_files()

    def test_selected_opportunity_file_rejects_selected_with_high_internal_build(self) -> None:
        text = complete_opportunity().replace(
            "## Internal Build Likelihood\n\nmedium",
            "## Internal Build Likelihood\n\nhigh",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            opportunity = root / "opportunities" / "trace-debugging.md"
            opportunity.parent.mkdir()
            opportunity.write_text(text, encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "changed_opportunity_files", return_value=[opportunity]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_selected_opportunity_files()

    def test_selected_opportunity_file_rejects_selected_with_platform_wedge(self) -> None:
        text = complete_opportunity().replace(
            SMALLEST_WEDGE,
            "Platform for every agent operations workflow across traces, storage, evaluation, and deployment.",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            opportunity = root / "opportunities" / "trace-debugging.md"
            opportunity.parent.mkdir()
            opportunity.write_text(text, encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "changed_opportunity_files", return_value=[opportunity]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_selected_opportunity_files()

    def test_selected_opportunity_file_treats_sell_before_build_as_selected(self) -> None:
        text = complete_opportunity().replace("selected for manual test", "Sell before build").replace(
            MONEY_FLOW,
            "unclear; no budget or money flow is visible yet",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            opportunity = root / "opportunities" / "trace-debugging.md"
            opportunity.parent.mkdir()
            opportunity.write_text(text, encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "changed_opportunity_files", return_value=[opportunity]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_selected_opportunity_files()

    def test_state_schema_accepts_empty_state_arrays(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                json.dumps({"schema_version": 1, "selected": [], "deferred": [], "watchlisted": []}),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root):
                validator.validate_state()

    def test_state_schema_accepts_selected_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root):
                validator.validate_state()

    def test_state_schema_rejects_invalid_structural_total(self) -> None:
        bad_scores = dict(STRUCTURAL_SCORES)
        bad_scores["total"] = 9
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(structural_scores=bad_scores),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_state_schema_rejects_selected_with_unclear_structural_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(manual_workflow="unclear manual workflow for the selected opportunity"),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_state_schema_rejects_selected_with_unclear_paid_wedge(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(paid_wedge="unclear"),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_state_schema_rejects_selected_with_high_internal_build(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(internal_build_likelihood="high"),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_state_schema_rejects_selected_with_unclear_multi_provider_user(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(multi_provider_user="unclear; no multi-provider user is proven"),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_state_schema_rejects_selected_with_unclear_money_flow(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(money_flow="unclear; no budget or money flow is visible yet"),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_state_schema_rejects_selected_with_platform_wedge(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(smallest_wedge="Platform for every agent operations workflow across traces, storage, evaluation, and deployment."),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_state_schema_allows_unclear_paid_wedge_on_watchlist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(
                    array_name="watchlisted",
                    stage="watchlist",
                    paid_wedge="unclear; no direct budget evidence yet",
                    spend_score=1,
                    reachability_score=1,
                    source_classes=["github"],
                    paid_experiment="unclear; a team must ask for a paid report or share a budget-backed workflow.",
                ),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root):
                validator.validate_state()

    def test_state_schema_rejects_build_without_low_internal_build_likelihood(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(
                    stage="selected-for-build",
                    spend_score=3,
                    reachability_score=3,
                    source_classes=["github", "docs", "job"],
                    internal_build_likelihood="medium",
                ),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_state_schema_allows_sell_before_build_stage(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(stage="sell-before-build"),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root):
                validator.validate_state()

    def test_state_schema_rejects_selected_with_low_spend_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(spend_score=1),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_state_schema_rejects_selected_with_github_only_source_classes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(source_classes=["github"]),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_state_schema_rejects_build_with_too_few_source_classes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(stage="selected-for-build", spend_score=3, reachability_score=3),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_money_readiness_rejects_selected_with_low_spend(self) -> None:
        readiness = "\n".join(
            [
                "| Opportunity | Pain | Spend | Reachability | Timing | Buildability | Buyer | Existing spend | Paid experiment | Source classes | Stage |",
                "|---|---|---|---|---|---|---|---|---|---|---|",
                f"| Agent trace debugging | 5 | 1 | 3 | 3 | 4 | {BUYER} | {EXISTING_SPEND} | {PAID_EXPERIMENT} | github, forum | `selected-for-test` |",
            ]
        )

        with patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
            validator.validate_money_readiness_table(ROOT / "opportunity-reports" / "test.md", readiness)

    def test_money_readiness_rejects_selected_with_github_only_sources(self) -> None:
        readiness = "\n".join(
            [
                "| Opportunity | Pain | Spend | Reachability | Timing | Buildability | Buyer | Existing spend | Paid experiment | Source classes | Stage |",
                "|---|---|---|---|---|---|---|---|---|---|---|",
                f"| Agent trace debugging | 5 | 2 | 3 | 3 | 4 | {BUYER} | {EXISTING_SPEND} | {PAID_EXPERIMENT} | github | `selected-for-test` |",
            ]
        )

        with patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
            validator.validate_money_readiness_table(ROOT / "opportunity-reports" / "test.md", readiness)

    def test_state_schema_rejects_stage_mismatched_array(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                complete_state(array_name="watchlisted", stage="selected-for-test"),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_state_schema_rejects_missing_comparison_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "discovery_mode": "watchlist-directed",
                        "selected": [
                            {
                                "id": "agent-trace-debugging",
                                "family": "ai-llm-demand",
                                "status": "selected",
                                "labels": ["M2", "M4"],
                            }
                        ],
                        "deferred": [],
                        "watchlisted": [],
                    }
                ),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_watchlist_accepts_expected_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_topic_scope(root)
            (root / "opportunity-watchlist.yml").write_text(
                "\n".join(
                    [
                        "entries:",
                        "  - source: GitHub issue",
                        "    url: https://example.com",
                        "    family: ai-llm-demand",
                        "    signal_type: repeated-pain",
                        "    priority: medium",
                        "    status: watch",
                        "    reason: Repeated pain around debugging agent traces in public issues.",
                    ]
                ),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root):
                validator.validate_watchlist()

    def test_watchlist_rejects_missing_priority_family_seed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_topic_scope(root, families=["ai-llm-demand", "blockchain-demand"])
            (root / "opportunity-watchlist.yml").write_text(
                "\n".join(
                    [
                        "entries:",
                        "  - source: GitHub issue",
                        "    url: https://example.com",
                        "    family: ai-llm-demand",
                        "    signal_type: repeated-pain",
                        "    priority: medium",
                        "    status: watch",
                        "    reason: Repeated pain around debugging agent traces in public issues.",
                    ]
                ),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_watchlist()


if __name__ == "__main__":
    unittest.main()
