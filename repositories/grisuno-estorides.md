# grisuno/estorides

- Repository: https://github.com/grisuno/estorides
- Review date: 2026-08-05
- Current commit reviewed: `324c2a45c9d7a9f3545b785d3c42322b77cc4449`
- Commit date: 2026-07-28T21:24:45-04:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, specifically OSINT/event intelligence, evidence-backed reasoning, knowledge graphs, and entity resolution. The reusable mechanism is the deterministic identity and confidence-weighted fact fusion layer, not the UI or product shell.

## Verified Flow

`Orchestrator.run` query input -> source selection and async fanout with deadline caps -> per-source parsing and extraction -> `entity_resolution.py` normalizes and canonicalizes entities with blocking plus Jaro-Winkler / transliteration scoring -> `fusion_store.py` persists source-attributed entities, observations, properties, and relationships in SQLite/WAL -> tests verify probabilistic fusion, deterministic IDs, cross-script normalization, and monotonic scoring behavior.

- E1 source verified: `estorides_core/orchestrator.py`, the orchestrator wires source registry, async client, knowledge graph, optional Kuzu/case/entity/fusion stores, and deadline-bounded fanout.
- E1 source verified: `estorides_core/entity_resolution.py`, deterministic types are exact-only; fuzzy types use blocking, transliteration, consonant skeletons, and Jaro-Winkler scoring.
- E1 source verified: `estorides_core/entity_resolution.py`, canonical IDs are hash-derived from type plus normalized value.
- E1 source verified: `estorides_core/fusion_store.py`, the SQLite fusion store uses WAL mode, one serialized connection, foreign keys, and deterministic `entity_id` values.
- E1 source verified: `estorides_core/fusion_store.py`, the store persists source catalog metadata, fused entities, observations, properties, and relationships with provenance.
- E2 test verified: `tests/test_entity_resolution.py::TestCrossScriptPersonFusion.test_three_spellings_fuse` verifies cross-script person fusion.
- E2 test verified: `tests/test_entity_resolution.py::TestDomainCaseVariantMerge.test_domain_merge_is_exact` verifies deterministic exact merges.
- E2 test verified: `tests/test_entity_resolution.py::TestLookAlikeDomainsSurfaceAsLink.test_look_alike_domains_produce_same_as_link` verifies SAME_AS linking for look-alikes.
- E2 test verified: `tests/test_probabilistic_fusion.py::TestCorroborationLiftsScore.test_two_sources_are_better_than_one` verifies multi-source score lift.
- E2 test verified: `tests/test_probabilistic_fusion.py::TestMergeMonotonic.test_lower_confidence_never_decreases` verifies monotonic confidence.

## Architecture

Principal components:

- `Orchestrator`: fanout, deadline management, persistence, and per-source observation capture.
- `entity_resolution`: canonical IDs, blocking keys, cross-script similarity, and SAME_AS links.
- `fusion_store`: source-attributed SQLite fact store with entities, observations, properties, and relationships.
- Optional backends: Kuzu graph, case store, entity store, and recon fusion path.

Most interesting mechanism: the repository separates canonical identity from probabilistic corroboration. Exact types never fuzzy merge; fuzzy types either merge deterministically or surface as links; and the fusion store preserves every contributing source while still letting the score rise with corroboration.

Baseline comparison: a typical OSINT scraper stores raw observations and a single latest entity row. This repository adds stable IDs, source attribution, confidence weighting, and explicit same-as ambiguity instead of collapsing all claims together.

## Reuse Guidance

Reusable:

- Use deterministic canonical IDs for exact or near-exact entity types before you do any probabilistic fusion.
- Keep source attribution on every fused fact so confidence is explainable.
- Separate merge decisions from link decisions for near-matches that should not be auto-fused.

Do not copy:

- Do not copy the product-facing orchestration shell as the main architectural artifact.
- Do not treat optional backends as always present; the code is explicitly fail-soft.
- Do not assume LLM extraction is enough without deterministic normalization and persistence.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Strong test surface around entity resolution and confidence behavior.
- Deterministic normalization and canonical IDs are source-backed, not just documentation claims.
- The fusion store uses WAL SQLite with explicit schema and provenance fields.

Experimental or incomplete for our needs:

- The run still depends on optional backends that can fail soft.
- The review did not run the local Python test suite.
- Confidence scoring is good, but it is still a heuristic rather than a formally calibrated model.

Hidden costs and failure modes:

- Cross-script matching can over-normalize if blocking or transliteration settings are too aggressive.
- The fusion store is serialized around one connection, which simplifies correctness but caps concurrency.
- Fanout deadlines can cause partial result sets that need explicit operator interpretation.

Adoption experiment:

Apply the canonical-ID plus confidence-fusion pattern to one internal OSINT or threat-intel ingest path, then measure whether the same source evidence produces the same canonical node and a monotonic confidence score across repeated runs.

## Candidate Patterns

- `deterministic canonical identity`
- `confidence-weighted fact fusion`
