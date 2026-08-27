# peterbussch/pageledger

- Repository: https://github.com/peterbussch/pageledger
- Review date: 2026-08-26
- Current commit reviewed: `fd1c1da0fbdc366222170f24fb22890f8a19f8a0`
- Commit date: 2026-08-16T22:51:21-04:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially provenance-preserving extraction, rerun planning, quality queues, and auditability over long OCR jobs. The reusable mechanism is the filesystem-native run ledger: extraction is not just output, it is a manifest-backed record with page-level evidence, rerun lineage, and verification checks.

## Verified Flow

`pageledger run` loads config and adapter choices -> pages are paginated and routed -> budget preflight and mid-run guards decide whether extraction proceeds -> the adapter extracts page content -> quality signals are graded and turned into review and quarantine queues -> `build_manifest`, `build_audit`, and `build_rerun_manifest` write the run record -> `pageledger rerun` validates the parent manifest, source checksums, and rerun depth before replaying exactly the queued pages -> `verify_run` checks artifact coherence, symlink safety, config hashes, and rerun manifest consistency.

I inspected the source and test surface, but I could not run `pytest` in this CI image because `pytest` is not installed here.

## Architecture

Principal components:

- `pageledger/runner.py` for run orchestration, rerun planning, and artifact emission.
- `pageledger/artifacts.py` for manifest, audit, route-map, and rerun-manifest builders.
- `pageledger/policy.py` for page-policy validation and review/quarantine queue rebuilding.
- `pageledger/verify.py` for run-directory coherence checks.
- `pageledger/quality.py`, `grading.py`, and `routing.py` for quality and routing evidence.

Most interesting mechanism: the rerun manifest is executable evidence. It preserves `page_id`, `page_number`, source path, reason, previous grade, run depth, and parent lineage, and `pageledger rerun` refuses to replay if the parent run is incoherent or the source checksum has changed.

Baseline comparison: a normal OCR pipeline would write extracted text and maybe a loose audit log. PageLedger instead keeps the run directory itself as the evidence object, with stable manifests, route maps, quality records, and verification rules that can be replayed or audited later.

## Reuse Guidance

Reusable:

- Treat OCR output as a ledgered run, not just a text artifact.
- Keep rerun candidates page-granular and source-addressable.
- Make source checksums and parent run IDs part of the replay contract.
- Separate review, quarantine, and rerun semantics so they can evolve independently.

Do not copy:

- Do not copy the exact adapter ecosystem or the domain-specific page taxonomy without adaptation.
- Do not treat the current in-repo verification code as a substitute for backend validation under real workloads.
- Do not collapse the rerun manifest into a simple list of file paths; the lineage fields are the point.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The repository has a substantial test suite for rerun semantics, quality queues, and run verification.
- `verify_run` explicitly rejects symlink escapes and manifest inconsistencies.
- The run and rerun artifacts are all plain files, which makes inspection and replay straightforward.

Experimental or incomplete for our needs:

- The adapter surface is broad, and behavior still depends on external OCR or document tools.
- I could not execute the Python test suite in this runner because `pytest` is unavailable here.
- The system is intentionally opinionated about page-level workflows, so not every document pipeline will map cleanly.

Hidden costs and failure modes:

- Provenance and verification create more artifact plumbing than a basic extraction script.
- External adapters can fail independently of the ledger logic.
- If callers treat generated artifacts as authoritative without re-running `verify_run`, they can miss tampering or drift.

Adoption experiment:

Run one document through `pageledger run`, inspect the audit and rerun manifest, then replay only the warning pages with a stronger adapter and confirm that the parent checksum and page IDs remain stable.

## Candidate Patterns

- `page-granular rerun manifest`
- `filesystem-native audit ledger`
- `source-checksum replay gate`
