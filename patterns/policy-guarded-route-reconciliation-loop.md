# Policy-Guarded Route Reconciliation Loop

- Canonical name: Policy-Guarded Route Reconciliation Loop
- Aliases: route reconciliation loop, reconnect-safe route propagation, policy-synchronized tunnel update loop, access-controlled route refresh
- Avoided duplicate names: VPN sync loop, route syncer, control-plane poller, reconnect handler
- Last updated: 2026-10-31

## Problem

Private-network control planes need to reconcile peers, routes, DNS, access policy, and reconnect state without exposing stale reachability. A plain tunnel daemon or static peer list does not solve route approval, policy reload, reconnect ordering, or health-state cleanup.

## Mechanism

Treat route and policy management as an ordered reconciliation loop:

- Reconnect or poll to ingest the newest node-reported hostinfo, endpoints, and announced routes first.
- Rebuild derived adjacency or peer maps when policy changes.
- Persist approved routes explicitly rather than treating them as ephemeral UI state.
- Recompute primary routes and advertised reachability after the source state has been refreshed.
- Clear stale health or approval bits when the node no longer qualifies as an HA candidate.
- Normalize revocation and policy decisions on full peer keys, not short fingerprints, so the control plane cannot be tricked by a truncated identity.

The loop keeps raw node state, policy state, and derived reachability state distinct, then replays the derived state whenever a source input changes.

## Invariants

- Announced routes must be present before primary-route selection.
- Policy reload must refresh derived adjacency, not just raw policy bytes.
- Clearing approved routes must also clear stale health/HA state when the node is no longer eligible.
- Reconnect handling must not expose a route window built from stale hostinfo.
- Derived reachability should always be recomputable from persisted source state.

## Implementation Variants

- Reconnect-first subnet-router reconciliation: Headscale updates node state from `MapRequest` before `Connect`, then re-approves routes and rebuilds peer maps on policy reload.
- Generation-stamped cleanup-timer reconciliation: Headscale keeps ephemeral GC timers alive across failed reconnects, then suppresses stale deletions when the node has re-keyed or already has live sessions.
- Policy-event tunnel reconciliation: Firezone routes portal authorization and relay updates through a gateway event loop that mutates route, DNS, and tunnel state.
- Connectivity-status projection: NetBird normalizes peers, relays, DNS, SSH, and session expiry into one operator-facing snapshot so route health can be observed coherently.
- Key-revocation tunnel reconciliation: `dyber-pqc/DyberVPN` normalizes peer keys, hot-reloads policy and CRL state, and scans revoked peers on a periodic timer so reconnects do not resurrect stale access.

## Known Repositories

- `juanfont/headscale` reviewed at `7721d8c29978b65b68269bb58391fcd25a8c1085`.
- `firezone/firezone` reviewed at `ac4e69ea9d86f21b26d09106d9ac1a5afacb5b55`.
- `netbirdio/netbird` reviewed at `791401060d2b95e5f51e3439c0649729132f571e`.
- `dyber-pqc/DyberVPN` reviewed at `943cf5012dc370a5768550eab6a0b7a3c71711c7`.

## Comparison Of Implementations

Headscale is strongest when the main problem is reconnect ordering plus approved-route persistence. Its state layer explicitly refreshes policy, hostinfo, and route approval in a defined order.

Firezone is strongest when the main problem is event-driven tunnel mutation. Its gateway event loop turns authorization and relay changes into concrete route and DNS updates.

NetBird is strongest when the main problem is operator observability. Its status conversion layer collapses connectivity, DNS, relay, and session metadata into a single snapshot.

`dyber-pqc/DyberVPN` is strongest when the main problem is access-control churn around a tunnel. Its policy engine refuses truncated identity matches, reloads policy and CRL state explicitly, and scans revoked peers on a timer so reconnects do not silently re-open access.

The conventional baseline is a tunnel client that applies route and DNS changes opportunistically. That is easier to build, but it loses the explicit reconciliation contract needed for least-privilege private networking.

## Failure Modes

- Reconnect races can produce empty AllowedIPs windows.
- Policy reload can drift from node store state if derived adjacency is not refreshed.
- Approved-route persistence can re-apply stale routes after restart if empty slices are mishandled.
- Health bits can leak across disconnect/reconnect cycles and misclassify HA candidates.
- Truncated fingerprints can allow an identity collision to inherit policy or revocation state.
- Policy and CRL reloads can diverge if operators change one without the other.

## Trade-Offs

- More explicit reconciliation improves correctness but increases control-plane complexity.
- Persisting derived route state improves recovery but raises the risk of stale-state bugs if invalidation is incomplete.
- Tight ordering around reconnect and policy events can require more tests than a purely stateless tunnel layer.

## Applicability To Interests

- `privacy-networking-vpn`: directly applicable to route approval, policy routing, DNS leak avoidance, and reconnect recovery.
- `satellites-space-systems`: useful as an analogy for delayed command/telemetry reconciliation when connectivity is intermittent.
- `drones-robotics-autonomy`: useful where ground-control links need the same explicit route and state reconciliation discipline.
- `ai-llm-systems`: useful as a general pattern for policy-driven control surfaces that must fail closed on stale or truncated identity state.

## Adoption Conditions

- Add tests for reconnect ordering, route approval propagation, policy reload, and restart recovery.
- Validate that the derived route view is always recomputable from persisted node state.
- Check that empty route clears and health-bit cleanup survive restart and reconnect sequences.
- Validate that key normalization rejects short fingerprints and that policy reload stays in step with CRL reload.

## Evidence References

- E1 source verified: Headscale `hscontrol/poll.go` updates node state from `MapRequest` before `Connect`, and `hscontrol/app.go` / `hscontrol/db/node.go` suppress stale ephemeral GC timers after reconnect or re-key events.
- E1 source verified: Headscale `hscontrol/state/state.go:ReloadPolicy`, `SetApprovedRoutes`, and `AutoApproveRoutes` re-run policy and route reconciliation.
- E2 test verified: Headscale `hscontrol/poll_test.go`, `hscontrol/servertest/routes_test.go`, `policy_test.go`, and `state/persist_test.go` verify reconnect recovery, stale-timer suppression, route propagation, policy changes, and restart persistence.
- E1 source verified: Firezone `rust/gateway/src/main.rs` and `rust/gateway/src/eventloop.rs` drive gateway state from portal authorization and relay updates.
- E1 source verified: NetBird `client/status/status.go` converts protobuf status into a normalized connectivity snapshot.
- E1 source verified: DyberVPN `crates/dybervpn-tunnel/src/policy.rs::normalize_peer_key`, `PolicyEngine::evaluate`, and `reload` enforce full-key matching and policy hot reload.
- E1 source verified: DyberVPN `crates/dybervpn-tunnel/src/revocation.rs::check_key`, `revoke_key`, `suspend_key`, `reinstate_key`, and `reload` maintain the CRL lifecycle.
- E2 test verified: DyberVPN `crates/dybervpn-tunnel/src/policy.rs` and `revocation.rs` tests cover collision rejection, policy-from-JSON loading, and revocation roundtrip.
