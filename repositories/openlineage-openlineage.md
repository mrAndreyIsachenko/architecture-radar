# OpenLineage/OpenLineage

- Repository: https://github.com/OpenLineage/OpenLineage
- Review date: 2026-08-02
- Current commit reviewed: `13f1b0ac406bc276b3fa23445062c2f119b4fe91`
- Commit date: 2026-07-31T12:12:29+02:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

OpenLineage informs the `Evidence-backed semantic execution graph` and `AI knowledge layer and metadata systems` priorities in `interests.md`: stable provenance, parent-child causality, source references, operational lineage, schema evolution, and separation of events/facets across systems.

## Verified Flow

Producer constructs a `RunEvent` with run/job/input/output datasets -> generated client model fills schema identity and producer metadata -> `OpenLineageClient.emit` enriches facets, applies filters, and emits through configured transport -> downstream lineage service can materialize run/job/dataset graph from versioned envelopes.

- E1 source verified: `spec/OpenLineage.json` at `13f1b0...` defines `BaseEvent` with required `eventTime`, `producer`, and `schemaURL`.
- E1 source verified: `spec/OpenLineage.json` defines `RunEvent` with `eventType`, `run`, `job`, `inputs`, and `outputs`, and requires `run` and `job`.
- E1 source verified: `spec/OpenLineage.json` defines `Run`, `Job`, and `Dataset` objects with facet maps; `BaseFacet` requires `_producer` and `_schemaURL`.
- E1 source verified: `spec/facets/ParentRunFacet.json` models parent and root run/job identity, preserving causal relationships across spawned runs.
- E1 source verified: `spec/facets/ColumnLineageDatasetFacet.json` models output fields, input fields, and transformations.
- E1 source verified: `client/python/src/openlineage/client/generated/base.py` sets `schemaURL` automatically for generated `BaseEvent`, `BaseFacet`, and `RunEvent` classes.
- E1 source verified: `client/python/src/openlineage/client/client.py`, `OpenLineageClient.emit` validates event type, adds environment/source-code/tag facets, applies filters, and sends to transport.
- E2 test verified: `client/python/tests/test_client.py::test_client_sends_proper_json_with_minimal_run_event` asserts emitted JSON contains `eventTime`, `eventType`, `producer`, `schemaURL`, `run.runId`, `job`, `inputs`, and `outputs`.

## Architecture

Principal components:

- Versioned JSON schema: stable base event and facet contracts.
- Facets: extensible typed metadata attached to runs, jobs, datasets, input datasets, and output datasets.
- Generated clients: language bindings enforce schema defaults and validation.
- Transport abstraction: HTTP, Kafka, file, console, composite, async HTTP, and cloud-specific transports.
- Integrations: Spark, dbt, Flink, SQL, and related integration code adapt source systems into OpenLineage events.

Most interesting mechanism: every event and facet carries producer and schema identity, while the core event keeps run/job/dataset identity separate from typed extension facets. This makes evidence envelopes composable across tools.

Baseline comparison: a conventional metadata graph directly mutates nodes and edges in a central service. OpenLineage sends versioned facts about execution and datasets, letting consumers project the graph while preserving the producing system and schema version.

## Reuse Guidance

Reusable:

- Adopt the event/facet split for internal execution graph evidence: immutable base identity plus typed evidence facets.
- Require producer URI and schema URL on every evidence-carrying envelope.
- Model parent/root causality as explicit facets instead of relying on implicit naming.
- Use transport adapters so agents, batch jobs, and research tools can emit evidence without sharing a runtime.

Do not copy:

- Do not limit internal execution graphs to data-job concepts only; agent tool calls need additional facets for prompts, tool permission scopes, evidence hashes, and decision rationale.
- Do not assume schema validity proves factual correctness. A valid event can still contain wrong lineage.
- Do not expose environment variable facets without a strict allowlist; the client supports environment collection, which needs local policy.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Versioned spec, generated clients, and many integrations.
- Tests cover client emission and config/transport behavior.
- Facets let independent producers extend metadata without changing the base envelope.

Experimental or incomplete for our needs:

- Confidence scoring and evidence hashes are not first-class base fields.
- Parent run facets preserve causality but not full step-level replay semantics.
- The review did not execute OpenLineage integration tests locally.

Hidden costs and failure modes:

- Consumers must handle schema evolution and facet version drift.
- Multiple producers can emit inconsistent claims about the same dataset or run.
- Transport success does not imply downstream materialization success.

Adoption experiment:

Define an `AgentStepRunFacet` and `EvidenceHashFacet` compatible with OpenLineage-style producer/schema conventions. Emit events from one agent workflow and one data workflow into a local projector, then verify parent-child causality and source references survive projection.
