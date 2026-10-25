# nasa/openmct

- Repository: https://github.com/nasa/openmct
- Review date: 2026-10-25
- Current commit reviewed: `e09bfaf47856b2b7ae2ea74334800b26fd27a41e`
- Commit date: 2026-10-06T17:01:32-07:00
- Branch: `master`
- Previous commit reviewed: `n/a`
- Material changes since previous review: first review for this repository in the radar; the current head was reviewed for telemetry request/subscribe flow and independent time-context handling.
- Decision: track

## Problem Fit

This repository informs `satellites-space-systems` through a mission-control telemetry and time-coordination layer. The reusable mechanism is not the dashboard UI; it is the combination of abortable telemetry requests, strategy-aware subscription caching, and per-view independent time contexts.

## Verified Flow

Domain object with telemetry -> `TelemetryCollection.load()` sets the time system, captures bounds, starts request and subscription watchers -> `TelemetryAPI.standardizeRequestOptions()` fills in missing time bounds and domain key -> `TelemetryCollection._requestHistoricalTelemetry()` attaches `onPartialResponse`, creates an `AbortController`, emits `requestStarted`, applies request interceptors, and awaits the provider -> `TelemetryAPI.request()` also uses an abort controller, applies request interceptors, and clears the controller in `finally` -> `TelemetryAPI.subscribe()` hashes domain object plus options, caches provider subscriptions by strategy, and fans callbacks out as latest or batch values -> `TimeAPI.getContextForView()` and `addIndependentContext()` return or create a per-view time context that follows the global time system but keeps its own bounds and mode.

- E1 source verified: `src/api/telemetry/TelemetryCollection.js::load`, `_requestHistoricalTelemetry`, `_initiateSubscriptionTelemetry`, and `destroy` define the telemetry lifecycle and abort/cleanup behavior.
- E1 source verified: `src/api/telemetry/TelemetryAPI.js::standardizeRequestOptions`, `applyRequestInterceptors`, `request`, and `subscribe` normalize requests, apply interceptors, enforce abort handling, and cache strategy-aware subscriptions.
- E1 source verified: `src/api/time/TimeAPI.js::addIndependentContext`, `getContextForView`, `addTimeSystem`, and `addClock` implement per-view time contexts and the time-system registry.
- E2 test verified: `src/api/telemetry/TelemetryAPISpec.js::telemetry batching support` verifies cache separation, latest-vs-batch callback behavior, and legacy-provider fallback.
- E2 test verified: `src/api/time/TimeAPISpec.js::Provides a default time context`, `Without a clock, is in fixed time mode`, and `Provided a clock, is in real-time mode` verify the default context and clock-driven mode switch.

## Architecture

Principal components:

- Telemetry collection object that owns the historical request, live subscription, bounds tracking, and teardown.
- Telemetry service that resolves providers, normalizes options, and applies request interceptors.
- Subscription cache keyed by domain object and options hash.
- Time service that owns the global time system, clocks, and independent per-view contexts.

Most interesting mechanism: the subscription cache preserves strategy semantics instead of flattening them into a single provider subscription. Latest and batch consumers can share the same underlying provider while still receiving the shape they requested.

Baseline comparison: a simpler client would keep a single global time window and one subscription per consumer. Open MCT keeps time-context isolation and request/subscribe lifecycle control separate, which is the more reusable abstraction.

## Reuse Guidance

Reusable:

- Separate global time from per-view time contexts.
- Make historical telemetry fetches abortable and explicit.
- Cache subscription lifecycles by strategy and option hash.
- Put request interception in front of provider execution.

Do not copy:

- Do not copy the subscription cache without preserving the latest/batch contract.
- Do not treat independent time contexts as trivial state; they need path comparison and cleanup.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Source and tests both cover the time-context baseline and the request/subscription contract.
- Historical requests and subscriptions have explicit teardown behavior.
- Strategy-aware fan-out is tested rather than assumed.

Experimental or incomplete for our needs:

- The current review did not trace a real mission data source through a deployed telemetry provider, but the code-level contract is already strong.

Hidden costs and failure modes:

- Subscription caching can mask incorrect strategy propagation if the provider contract drifts.
- Independent contexts can become stale if object-path comparisons are wrong.
- Abortable request handling adds lifecycle complexity for downstream providers.

Adoption experiment:

Attach a custom telemetry provider, create one latest and one batch subscription for the same domain object, and verify that each consumer receives the expected shape while a per-view time context stays isolated from the global time bounds.

## Candidate Patterns

- `strategy-aware telemetry subscription cache`
- `abortable historical telemetry request`
- `independent per-view time context`

## Previous Reviews

First review for this repository in the radar.
