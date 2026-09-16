# juanfont/headscale

- Repository: https://github.com/juanfont/headscale
- Review date: 2026-09-16
- Current commit reviewed: `c90ba0f0d6f82fe79fc2da82d95561f0e2780628`
- Commit date: 2026-09-14T17:04:04+03:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `privacy-networking-vpn`, especially reconnect recovery, route approval, and control-plane behavior when policy or node health changes. The reusable mechanism is the combination of policy compilation, node-store snapshots, and session-aware connect/disconnect handling that keeps peer recomputation bounded.

## Verified Flow

`PolicyManager::NewPolicyManager` parses and validates policy, resolves user references, compiles filter and grant structures, and caches the derived peer/filter artifacts -> `PolicyManager::NodeNeedsPeerRecompute` classifies subnet routers, relay targets, and via targets as peers that need full recomputation when online state changes -> `State.Connect` increments the node session epoch, marks the node online, clears unhealthy state, emits a lightweight online change, and only emits a policy recompute when the node role requires it -> `State.Disconnect` decrements active sessions, only marks offline when the last live session ends, persists last-seen data, and emits the minimal offline change plus policy recompute when needed -> `State.SetApprovedRoutes` updates approved routes, clears stale unhealthy bits when no routes remain, persists the node, and refreshes policy -> `State.BatchSetNodeHealth` applies health flips atomically and runs primary-route election once after the batch -> `connect_test.go`, `primaries_property_test.go`, and `route_approval_test.go` exercise ordinary reconnects, relay/subnet-router recompute gates, route approval compatibility, and batched primary-route election invariants.

- E1 source verified: `hscontrol/policy/v2/policy.go:31-91,101-220,280-420` implements policy validation, cache invalidation, auto-approver resolution, and the peer-recompute classification gate.
- E1 source verified: `hscontrol/state/state.go:637-748,1007-1042,1334-1418` implements connect/disconnect session handling, approved-route persistence, and batched node-health updates.
- E1 source verified: `hscontrol/state/node_store.go:101-176,259-315` implements the copy-on-write snapshot store and atomic batched writes.
- E2 test verified: `hscontrol/state/connect_test.go:56-209,238-275` covers ordinary reconnects, relay-target recompute, subnet-router recompute, and out-of-order disconnect safety.
- E2 test verified: `hscontrol/state/primaries_property_test.go:393-620` covers primary-route election across connect/disconnect, probe health, batch health flips, and simultaneous offline transitions.
- E2 test verified: `hscontrol/policy/route_approval_test.go:14-847` covers route-approval compatibility across tags, groups, overlapping prefixes, exit-node behavior, and aggregate policy cases.

## Architecture

Principal components:

- Policy manager that compiles ACLs, grants, auto-approvers, and SSH policy.
- NodeStore copy-on-write snapshot with atomic batched writes and route-election state.
- State layer that coordinates connect/disconnect, approved routes, and health updates.
- Property and integration tests that pin reconnect and HA election behavior.

Most interesting mechanism: reconnect recovery is session-aware rather than epoch-only. A node only goes offline when the last session is released, and full peer recomputation is gated to the node roles that actually change peer topology.

Baseline comparison: a common control plane would treat every reconnect as a broad policy refresh. Headscale narrows the fan-out, keeps ordinary reconnects lightweight, and reserves full recomputation for subnet routing, relay, and via-target cases.

## Reuse Guidance

Reusable:

- Separate ordinary reconnects from topology-changing reconnects.
- Use a session count, not only a last-epoch check, to avoid stranding a node online after out-of-order disconnects.
- Batch HA health flips so primary election sees the post-batch state only.
- Keep policy compilation caches explicit and invalidate them only when the derived artifacts actually change.

Do not copy:

- Do not copy the NodeStore snapshot layout without understanding the surrounding policy and DB contracts.
- Do not assume the recompute gates are sufficient without real reconnect churn and multi-node validation.
- Do not treat the property tests as a substitute for live overlay recovery.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The control plane distinguishes ordinary peer patches from expensive recompute paths.
- Route approval, connect/disconnect, and HA health all have tests that codify the intended invariants.
- NodeStore write batching and snapshot replacement are explicit rather than accidental.

Experimental or incomplete for our needs:

- The source evidence is strong, but live reconnect storms and mixed-role HA recovery still need runtime validation.
- The current code assumes the policy and node-store layers remain coherent under concurrent churn; that is well motivated but still deserves fault-injection proof.
- The policy layer is broad and can become coupling-heavy if reused without the rest of the state machine.

Hidden costs and failure modes:

- A stale unhealthy bit or stale primary assignment can mislead peer routing if health and disconnect paths diverge.
- Too many recompute triggers would reintroduce CPU-heavy fan-out on reconnect storms.
- Copy-on-write snapshots are fast for reads but can still make write batching sensitive to burst size.

Adoption experiment:

Run a multi-node tailnet through reconnect storms, overlapping disconnects, and HA health flips, then confirm that ordinary reconnects stay lightweight while subnet-router and relay paths still trigger exactly one needed recompute per change.

## Candidate Patterns

- `session-epoch gated reconnect recovery`
- `atomic HA primary-election batch`
- `policy-driven peer-recompute gate`
