# geiserx/tailscale-rs

- Repository: https://github.com/geiserx/tailscale-rs
- Review date: 2026-08-05
- Current commit reviewed: `ec52d873bb78f260ae6b2a71c82c63d51d9fd54c`
- Commit date: 2026-08-04T12:53:32+02:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: watch

## Problem Fit

This repository informs `privacy-networking-vpn`, specifically secure tunnels, access control, traffic routing, and leak detection. The reusable mechanism is the Go-shaped `tsnet` facade plus the repo-local invariant checks that keep the network path fail-closed.

## Verified Flow

`tsnet::Server` field assignment -> lazy `up()` start path builds `Config` and starts the wrapped device -> `listen` / `dial_tcp` / `loopback` / `status` forward through the device surface -> `checks/src/funnel_fail_closed.rs` and `checks/src/ipv4_only_host_net.rs` scan production sources for forbidden cert-minting or IPv6-leak tokens -> live E2E tests in `tests/tsnet_facade_e2e.rs` exercise registration, overlay TCP listen/dial, loopback, local API, and TLS fail-closed behavior.

- E1 source verified: `src/tsnet.rs`, `Server` is a thin facade over `Device` and `Config`, with lazy start, `FileStore`/`MemStore`, and Go-shaped methods.
- E1 source verified: `src/tsnet.rs`, `StateStore` keeps only the identity blob under a single key, which is a smaller persistence contract than Go `tsnet` but still explicit.
- E1 source verified: `checks/src/funnel_fail_closed.rs`, production TLS paths are scanned for self-signed or ephemeral cert minting tokens and fail closed if they appear.
- E1 source verified: `checks/src/ipv4_only_host_net.rs`, host route and DNS programming is guarded against IPv6 tokens and `-6` routing flags.
- E1 source verified: `checks/src/ipv4_only_forwarder.rs`, the egress path is similarly guarded against IPv6 socket creation.
- E2 test verified: `tests/tsnet_facade_e2e.rs::f1_facade_up_status_close` validates lazy start, status, and graceful close.
- E2 test verified: `tests/tsnet_facade_e2e.rs::f2_facade_listen_and_dial_two_nodes` validates overlay listen/dial round-tripping.
- E2 test verified: `tests/tsnet_facade_e2e.rs::f3_facade_loopback_and_localclient` validates the loopback and local API path.
- E2 test verified: `tests/tsnet_facade_e2e.rs::f4_facade_listen_tls_failclosed` validates typed fail-closed TLS behavior.

## Architecture

Principal components:

- `tsnet::Server`: Go-shaped facade over the engine.
- `StateStore` implementations: file-backed or in-memory identity persistence.
- `checks` crate: repo-local invariant scanner for leak-firewall rules.
- `tests/tsnet_facade_e2e.rs`: live integration against real Tailscale.

Most interesting mechanism: the fork preserves a familiar Go embedding surface without giving up typed Rust errors or engine-native returns. The repo then backs that ergonomic layer with explicit invariant checks that reject IPv6 route leakage and self-signed TLS fallback in the production path.

Baseline comparison: a conventional wrapper would just translate method names and hope the lower layer stays safe. This repo couples the ergonomic facade to compile-time and repository-scanned checks that enforce the security posture.

## Reuse Guidance

Reusable:

- Use a thin facade when you need compatibility with an existing API shape, but keep typed engine errors underneath.
- Put leak-firewall checks in the repo so the unsafe path cannot drift quietly.
- Separate host-route programming from overlay-facing transport code so IPv6 and TLS fallback rules can be audited independently.

Do not copy:

- Do not copy the project as a stable production dependency without first validating the fork status and live Tailscale assumptions.
- Do not treat the state store as a full `tsnet` equivalence layer; it only persists identity keys here.
- Do not rely on live E2E tests without a gated credential and network setup.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The facade and the invariant checks are both explicit and tested.
- Live E2E coverage proves the facade can actually join and use Tailscale.
- The code documents where it intentionally deviates from Go semantics.

Experimental or incomplete for our needs:

- The repository is a fork and still describes itself as unstable/WIP.
- Live E2E tests require real Tailscale credentials and are feature-gated.
- The review did not run the live network tests locally.

Hidden costs and failure modes:

- The facade adds ergonomic compatibility at the cost of another state contract.
- The fail-closed checks are source scanners, not formal proofs.
- Live tests can only validate the happy path with real external infrastructure present.

Adoption experiment:

Take one small private-network service and enforce the same pattern: a lazy-start facade, a fail-closed TLS path, and a repo-local leak firewall that rejects IPv6 route programming in the host path before the service is shipped.

## Candidate Patterns

- `fail-closed leak firewall`
- `Go-shaped lazy tsnet facade`
