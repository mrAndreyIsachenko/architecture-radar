# Schema-Faceted Provenance Event Envelope

- Canonical name: Schema-Faceted Provenance Event Envelope
- Aliases: typed evidence envelope, facet-scoped lineage event, schema-addressed provenance event
- Avoided duplicate names: generic lineage event, provenance blob, execution log row
- Last updated: 2026-08-02

## Problem

Architecture Radar needs evidence-backed semantic execution graphs that can model steps, tool calls, inputs, outputs, retries, artifacts, parent-child causality, confidence, and decision rationale without collapsing verified facts, model inferences, and operational context into unverifiable summaries.

## Mechanism

Represent each execution or lineage observation as a small required event envelope plus typed facets. The envelope gives stable identity, event time, producer, and schema URL. Facets carry optional evidence such as parent run, source code location, environment, dataset schema, evidence hashes, model provenance, or confidence. Each facet has its own schema and producer boundary.

## Invariants

- Every event has a producer identity and schema URL.
- Optional metadata is typed as a facet, not appended as free-form narrative.
- Facets can evolve independently of the core event envelope.
- Parent/root causality is explicit and queryable.
- Serialization must preserve enough structure for deterministic projection into a graph.

## Implementation Variants

- OpenLineage-style run/job/dataset envelope with schema-scoped facets.
- Agent-execution variant with run/tool-call/artifact/review entities and custom facets for evidence hash, model call, confidence, authorization, and human approval.
- Hybrid variant where OpenLineage events are consumed into a broader semantic execution graph.

## Known Repositories

- OpenLineage/OpenLineage at `13f1b0ac406bc276b3fa23445062c2f119b4fe91`: schema-defined `RunEvent`, `Run`, `Job`, datasets, `BaseFacet`, and `ParentRunFacet`.
- getzep/graphiti at `7cf0cab4b43f55d768b64584ffa9829bbeec1e9d`: not an event-envelope implementation, but its episodic evidence graph is a complementary projection target for facet-backed events.

## Comparison

OpenLineage provides stronger schema and producer boundaries. Graphiti provides stronger graph-native temporal fact modeling. A useful Architecture Radar design would combine OpenLineage-style facet envelopes with Graphiti-style episode/fact projection.

## Failure Modes

- Facets become arbitrary JSON blobs without validation.
- Producers omit stable IDs, making replay and deduplication unreliable.
- Event transport succeeds but receiving storage does not preserve order, idempotency, or original payloads.
- Parent/root causality is optional and inconsistently populated.
- AI-generated claims are stored beside verified evidence without explicit evidence class or confidence.

## Trade-Offs

- Strong schemas improve auditability but require versioning discipline.
- Facet extensibility avoids core schema churn but can fragment query semantics.
- Event envelopes are easy to emit but still need a durable projection store.

## Applicability

Applies directly to `Evidence-backed semantic execution graph` and `AI knowledge layer and metadata systems` in `interests.md`. It is especially relevant for preserving tool-call evidence, source references, confidence, and decision rationale across long-running agent workflows.

## Adoption Conditions

- Define first-class facets for evidence hashes, source references, model/tool provenance, confidence, decision rationale, authorization, and human review.
- Store immutable raw events before graph projection.
- Make projection idempotent and replayable.
- Separate E1/E2/E3/I/H evidence classes in facet schemas.

## Evidence References

- E1 source verified: OpenLineage `spec/OpenLineage.json` defines `BaseEvent`, `RunEvent`, `Run`, `Job`, inputs, and outputs.
- E1 source verified: OpenLineage `client/python/src/openlineage/client/generated/base.py` sets `producer`/`schemaURL` on events and `_producer`/`_schemaURL` on facets.
- E1 source verified: OpenLineage `client/python/src/openlineage/client/generated/parent_run.py` models parent and root run/job causality.
- E2 test verified: OpenLineage `client/python/tests/test_facet_v2.py::test_custom_facet` verifies custom facets serialize with producer and schema URL.

