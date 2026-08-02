# netbirdio/netbird

- Repository: https://github.com/netbirdio/netbird
- Review date: 2026-08-02
- Current commit reviewed: `f2318a8fef230219110c9eeb58ca7f60e247ad98`
- Commit date: 2026-08-02T09:51:14+02:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `privacy-networking-vpn`: mesh networking, private routing, relay coordination, access control, DNS routing, and human-readable network status.

## Verified Flow

Proto status -> `ConvertToStatusOutputOverview` -> mapped peer, management, signal, relay, DNS, SSH, and session-expiry views -> `GeneralSummary` renders a consolidated snapshot for operators -> tests assert peer sorting and state formatting.

- E1 source verified: `client/status/status.go` converts the protobuf status into a normalized snapshot, including peers, relays, DNS groups, SSH sessions, and session expiry.
- E1 source verified: `client/status/status.go` sorts peers, derives relay connectivity states, and carries connection-type labels.
- E1 source verified: `client/status/status_test.go` checks conversion, sorting, and output formatting behavior.
- E3 maintainer stated: the top-level README describes a WireGuard-based overlay with centralized access control, private DNS, routing, relay fallback, and multi-account profiles.

## Architecture

Principal components:

- Management, signal, relay, and client status layers.
- Protobuf-backed status model converted into operator-facing output.
- DNS, SSH, relay, and peer connectivity state folded into a single overview.

Most interesting mechanism: the client produces a normalized connectivity snapshot that unifies overlay peers, relay availability, DNS groups, SSH sessions, and expiry into a single observable model.

Baseline comparison: a typical VPN client shows only a connection toggle and maybe route settings. NetBird exposes a structured control-plane state model that can be rendered, filtered, or compared in tests.

## Reuse Guidance

Reusable:

- Normalize network control-plane state into a single typed snapshot.
- Keep relay, DNS, and session-expiry status separately visible.
- Test the rendering layer so operator output remains stable.

Do not copy:

- Do not copy the product surface as the mechanism.
- Do not assume the status adapter proves the routing engine or policy engine itself.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Clear data-model conversion layer with tests.
- Broad product scope around overlay networking, DNS, and relay state.
- Snapshot semantics are useful for operators and health monitors.

Experimental or incomplete for our needs:

- The review stayed at the status-adapter layer, not the full routing plane.
- Some semantics are inherited from protobuf and upstream services rather than local code.

Hidden costs and failure modes:

- The snapshot can hide transient connectivity races.
- A single overview can flatten multiple failure modes unless the raw fields remain visible.

Adoption experiment:

Use the status-conversion layer idea for an internal tunnel health view: expose peer, relay, DNS, and session-expiry state as a typed snapshot and assert the rendering stays stable under reconnects.

## Candidate Patterns

- `normalized connectivity status snapshot`
- `overlay control-plane summary`
