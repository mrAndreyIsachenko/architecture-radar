# tunnexio/tunnex

- Repository: https://github.com/tunnexio/tunnex
- Review date: 2026-11-06
- Current commit reviewed: `ac9b58b6ca02585cd00a7015871e7ab76f6a9853`
- Commit date: 2026-10-22
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `privacy-networking-vpn`, especially origin-bound access control, safe reconnect behavior, and restart-safe policy enforcement. The reusable mechanism is capability-scoped origin projection: the runtime canonicalizes policy, revalidates DNS answers on each request, pins TLS roots to the reviewed CA material, strips browser authority from outbound requests, and fails closed when restore state is ambiguous.

## Verified Flow

Browser-supplied request -> `originpolicy.Normalize` canonicalizes allowed CIDRs and CA material -> `Checker.Check` validates the origin, re-resolves DNS, rejects control-plane addresses, and reports bounded readiness -> `Transport.RoundTrip` re-checks policy, re-resolves the origin, copies only path/query, and discards browser authority -> `restorebarrier.Check` refuses startup while restore state is unresolved -> `beam.NewRegistryGateway` / `beam.NewGateway` require verified TLS and exact binding headers -> `Connector.Run` keeps the active set bounded and applies backoff on failures.

- E1 source verified: `packages/apptransport/originpolicy/policy.go:38-145` canonicalizes destination CIDRs, rejects forbidden ranges, hashes the CA bundle, and validates resolved destinations against control-plane addresses.
- E1 source verified: `packages/apptransport/originpolicy/check.go:39-184` re-resolves the origin on each check, validates every answer, pins TLS roots, and reports bounded status fields.
- E1 source verified: `packages/apptransport/originpolicy/transport.go:26-144` repeats policy normalization on every request, re-resolves the origin, rewrites only path/query, and disables keep-alive reuse.
- E1 source verified: `packages/apptransport/restorebarrier/barrier.go:12-42` fails closed when the restore marker exists or the restore directory is not safe to inspect.
- E1 source verified: `packages/apptransport/beam/gateway.go:19-79` requires verified TLS 1.3 and exact binding headers before admitting a Beam channel.
- E1 source verified: `packages/apptransport/beam/connector.go:62-360` validates targets, requires verified bindings and certificates, bounds connector admission, and rejects malformed channel responses.
- E2 test verified: `packages/apptransport/http_policy_test.go:12-102` covers credential stripping, origin clustering, and cross-purpose channel refusal.
- E2 test verified: `packages/apptransport/channel_test.go:54-236` covers capacity accounting, lease expiry, and admission failure handling.
- E2 test verified: `packages/apptransport/browser_readiness_test.go:13-79` covers readiness refusal paths and probe-slot release.
- E2 test verified: `packages/apptransport/beam/gateway_test.go:21-114` and `packages/apptransport/beam/routes_test.go:12-55` cover binding validation, verified TLS, and route boundary checks.
- E2 test verified: `packages/apptransport/beam/connector_test.go:286-733` covers stream bounds, wrong-origin rejection, expiry cleanup, backpressure, and websocket handling.

## Architecture

Principal components:

- Origin-policy canonicalizer that normalizes CIDR allowlists and CA material.
- Origin checker that performs per-request DNS revalidation and bounded status reporting.
- Transport wrapper that rewrites requests to a single reviewed origin.
- Restore barrier that refuses startup when offline recovery is ambiguous.
- Beam gateway and connector that admit only verified TLS channels and keep connector counts bounded.

Most interesting mechanism: the code treats destination authority as a reviewed capability rather than something a browser request can provide. That choice survives stripping the product branding: the same mechanism is still a canonical policy envelope, a per-request DNS and TLS recheck, and a fail-closed startup gate.

Baseline comparison: a conventional tunnel or reverse proxy would typically trust configured origin state and rely on cached resolution or permissive startup. This code repeatedly revalidates the origin and refuses to start when recovery state is uncertain.

## Reuse Guidance

Reusable:

- Canonicalize policy before the first network action.
- Revalidate every DNS answer before dialing.
- Treat restore markers as a hard startup gate.
- Bound connector admission and retry loops instead of allowing bursty reconnection.

Do not copy:

- Do not trust browser-supplied authority or stale DNS answers.
- Do not relax startup when restore state is ambiguous.
- Do not copy the Beam transport without the same TLS and binding model.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Policy normalization is explicit and testable.
- Request rewriting is limited to the minimum necessary URL components.
- Restore handling fails closed instead of guessing.
- Admission and backoff logic are bounded rather than best-effort.

Experimental or incomplete for our needs:

- The runtime still needs live reconnect and restore churn validation.
- The Beam transport path is strongly constrained, but it remains coupled to the repository's specific authority and binding model.

Hidden costs and failure modes:

- DNS and TLS revalidation add latency to every request.
- Restart safety depends on the restore marker being correct and visible.
- Connector admission can fail closed under transient infrastructure issues.

Adoption experiment:

Run a gateway and connector through a real reconnect/restart sequence while changing DNS and restore state, then confirm the runtime never reuses stale authority and never starts listeners while recovery is ambiguous.

## Candidate Patterns

- `origin-policy canonicalization`
- `restore-barrier guarded startup`
- `bounded connector admission`

## Previous Reviews

First review. The open reconnect and restore experiment is recorded in the backlog and remains unvalidated.
