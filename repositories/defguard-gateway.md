# DefGuard/gateway

- Repository: https://github.com/DefGuard/gateway
- Review date: 2026-08-08
- Current commit reviewed: `ebac60b5a36ae38b537e3b7af45aa85ad3c785fb`
- Commit date: 2026-08-04T11:27:12+02:00
- Branch: `stable/2.x`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `privacy-networking-vpn`, especially WireGuard gateway management, access-control enforcement, reconnect-safe configuration updates, and mTLS-protected control-plane operation. The reusable mechanism is the configuration-diff loop around a WireGuard interface, not the full Defguard product.

## Verified Flow

Core setup and mTLS bootstrap -> `GatewayServer::start` validates TLS config and launches the gRPC server -> `GatewayServer::bidi` accepts the control-plane stream and forwards updates -> `Gateway::configure` recreates a missing interface, compares old and new interface/firewall state, and applies only the necessary changes -> `Gateway::purge` tears down the interface on disconnect with a grace period -> recovery test confirms purge-then-configure succeeds -> mTLS tests verify certificate acceptance/rejection boundaries.

- E1 source verified: `src/gateway_server.rs` requires TLS configuration, launches the gRPC control plane, and routes streamed updates into the gateway.
- E1 source verified: `src/gateway.rs` implements `configure`, `purge`, `has_firewall_config_changed`, `have_firewall_rules_changed`, and the interface recreation path when the device is missing.
- E1 source verified: `src/setup.rs` manages gateway setup authorization, certificate persistence, and session validation during bootstrap.
- E1 source verified: `src/enterprise/firewall/nftables/mod.rs` and `src/enterprise/firewall/nftables/netfilter.rs` hold the firewall rule mutation logic that the gateway diffs and applies.
- E2 test verified: `src/tests/recovery.rs::test_purge_then_configure_recovers_interface` verifies disconnect teardown followed by successful reconfiguration.
- E2 test verified: `src/tests/mtls.rs::test_start_errors_without_tls_config`, `test_valid_mtls_client_accepted`, and `test_no_client_cert_rejected` verify the mTLS control-plane boundary.
- E2 test verified: `src/gateway/tests.rs` covers interface configuration comparison and firewall configuration change detection.

## Architecture

Principal components:

- `GatewayServer` for gRPC/mTLS control-plane traffic.
- `Gateway` for WireGuard interface lifecycle and firewall diff application.
- Setup logic for bootstrap authorization and certificate handling.
- Firewall modules for nftables/packet-filter behavior.

Most interesting mechanism: the gateway is reconnect-safe because it treats the WireGuard interface as state to reconcile, not as an opaque process to restart. It can tear down on disconnect, wait through a grace period, and reconstruct the interface when the next valid configuration arrives.

Baseline comparison: a simpler gateway daemon would either keep the interface up blindly or rebuild it from scratch on every control-plane change. This implementation diffs interface and firewall state, then rehydrates only what changed.

## Reuse Guidance

Reusable:

- Compare new vs. current interface state before mutating the tunnel.
- Treat purge/disconnect as recoverable, not terminal.
- Use mTLS plus serial-pinned client identity for the control plane.
- Keep firewall diffs separate from tunnel lifecycle decisions.

Do not copy:

- Do not copy the whole Defguard platform or enterprise packaging.
- Do not assume the gateway-only recovery path covers the higher-level policy plane.
- Do not treat the reconnect grace period as a universal default.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Clear gateway/setup separation and explicit mTLS validation.
- Recovery and interface-diff behavior are both tested.
- The interface recreation path is directly covered by regression tests.

Experimental or incomplete for our needs:

- The repository is a component of a larger access-control platform.
- The review did not run the gateway or mTLS tests locally.
- Firewall behavior is inherently environment-sensitive.

Hidden costs and failure modes:

- Configuration drift can hide in interface and firewall diff logic.
- mTLS and serial pinning require careful certificate lifecycle management.
- The disconnect grace period introduces timing sensitivity.

Adoption experiment:

Use the gateway diff/recovery model for a small internal WireGuard control plane, then simulate a disconnect and a missing-interface restart to confirm the interface is recreated only after the next valid configuration arrives.

## Candidate Patterns

- `disconnect-safe interface rehydration`
- `config-diff firewall mutation`
- `serial-pinned mTLS gateway`
