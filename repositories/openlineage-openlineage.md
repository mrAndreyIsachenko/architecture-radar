# OpenLineage/OpenLineage

- Repository: https://github.com/OpenLineage/OpenLineage
- Review date: 2026-08-02
- Branch: `main`
- Commit reviewed: `13f1b0ac406bc276b3fa23445062c2f119b4fe91`
- Commit date: 2026-07-31T10:12:29Z
- Release/tag: not determined from the shallow clone
- Previous commit reviewed: none
- Current decision: adopt the event-envelope pattern conceptually for evidence-backed execution graphs; do not adopt the full client stack unless interoperating with OpenLineage consumers.

## Problem Fit

OpenLineage directly informs the `Evidence-backed semantic execution graph` and `AI knowledge layer and metadata systems` interests. Its core mechanism is not an AI graph, but a schema-versioned envelope for run, job, dataset, and facet metadata that can preserve producer identity, event time, parent runs, and extensible evidence facets.

## Source Structure

- `spec/OpenLineage.json` defines base event, run, job, dataset, and facet schemas.
- `spec/registry/**/facets/*.json` defines versioned extension facets.
- `client/python/src/openlineage/client/generated/base.py` contains generated attrs classes for `RunEvent`, `Run`, `Job`, `InputDataset`, `OutputDataset`, and facets.
- `client/python/src/openlineage/client/generated/parent_run.py` models parent/root run causality.
- `client/python/src/openlineage/client/client.py` resolves configuration, filters, and transport, then enriches and emits events.
- `client/python/src/openlineage/client/serde.py` serializes events while removing nulls and enum wrappers.
- Tests inspected: `client/python/tests/test_client.py`, `test_events.py`, and `test_facet_v2.py`.

## Verified Flow

`RunEvent object -> event/facet validation -> client facet enrichment -> JSON serialization -> HTTP transport POST -> receiver-visible lineage event`

- E1 source verified: `RunEvent` in `client/python/src/openlineage/client/generated/base.py` requires `run` and `job`, accepts `inputs` and `outputs`, and inherits `eventTime`, `producer`, and `schemaURL` from `BaseEvent`.
- E1 source verified: `BaseEvent.__attrs_post_init__` sets a producer default and schema URL; validators parse event time and URI-like producer/schema fields.
- E1 source verified: `BaseFacet` separately carries `_producer` and `_schemaURL`, allowing every facet to identify its own producer and schema.
- E1 source verified: `ParentRunFacet` in `client/python/src/openlineage/client/generated/parent_run.py` carries parent `run`, parent `job`, and optional root `run`/`job`.
- E1 source verified: `OpenLineageClient.emit` rejects unsupported event classes, adds environment facets, updates tags, adds source-code-location facets, applies filters, and calls the configured transport.
- E1 source verified: `HttpTransport.emit` serializes with `Serde.to_json`, posts to `urljoin(self.url, self.endpoint)`, closes the response, raises HTTP errors, and restores `http.client.HTTPConnection.debuglevel`.
- E2 test verified: `test_client_sends_proper_json_with_minimal_run_event` asserts the emitted HTTP JSON includes run, job, inputs, outputs, producer, schemaURL, and default tags.
- E2 test verified: `test_custom_facet` verifies custom `RunFacet` subclasses serialize with `_producer` and `_schemaURL`.

## Architecture

Principal components:

- Versioned specification: JSON Schema defines the stable envelope.
- Generated model layer: Python attrs classes enforce event shape and schema URLs.
- Facet extension layer: run, job, dataset, input, and output facets extend core events without changing the envelope.
- Client enrichment layer: environment variables, tags, and source-code location can be added consistently before emission.
- Transport layer: HTTP, async HTTP, Kafka, file, console, composite, and other transports are selected from config.

Most interesting mechanism: schema-scoped facets let independent producers add evidence without collapsing verified facts, operational context, parent causality, and extension metadata into one untyped blob.

## Comparison

Baseline: execution metadata is often logged as unstructured JSON per service or stored as rows in a workflow table. OpenLineage uses a standard event envelope whose facets are individually schema-addressed and producer-addressed.

Genuinely unusual:

- I interpretation: facet-level `_producer` and `_schemaURL` are a reusable provenance boundary for AI execution graphs where tool traces, evidence hashes, model judgments, and human approvals may come from different producers.
- I interpretation: `ParentRunFacet` gives a compact parent-child causality model that could map to long-running agent subtasks.

Standard engineering:

- JSON Schema, generated classes, and pluggable transports are standard integration infrastructure.

## Production Qualities

- E1 source verified: configuration merges constructor config, YAML config, and `OPENLINEAGE__` environment variables.
- E1 source verified: filters can prevent configured events from emitting.
- E1 source verified: HTTP auth supports API key and JWT token providers, and the HTTP transport validates URLs.
- E2 test verified: tests cover serialization, filtering, transport selection, custom facets, UUID validation, and HTTP request shape.

## Limitations

- I interpretation: OpenLineage records lineage events but does not by itself provide graph storage, replay, confidence propagation, or partial recomputation.
- I interpretation: event correctness depends on instrumentations supplying accurate inputs, outputs, and facets.
- H hypothesis: AI-specific evidence payloads would need custom facets and governance to avoid turning facets into arbitrary narrative blobs.

## Reuse

Reusable mechanism:

- Use a small required envelope (`eventTime`, `producer`, `schemaURL`, run/job identity) with typed facets for optional evidence.
- Let facets carry their own producer and schema URL.
- Model parent/root causality as a facet rather than a special case in every event type.

Do not copy:

- Do not copy OpenLineage's data-pipeline vocabulary wholesale for agent execution; map it to agent-specific run, tool-call, artifact, and review concepts.
- Do not rely on transport emission as a durable audit log without a receiving store that preserves ordering and idempotency.

Evidence still required before adoption:

- A custom facet schema for evidence hashes, confidence, model provenance, and decision rationale.
- A projection store design that consumes these events into queryable execution graphs.
- Idempotency and ordering policy for retries and duplicate event delivery.

## Extracted Patterns

- [Schema-Faceted Provenance Event Envelope](../patterns/schema-faceted-provenance-event-envelope.md)

