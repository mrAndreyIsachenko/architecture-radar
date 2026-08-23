# openziti/ziti

- Repository: https://github.com/openziti/ziti
- Review date: 2026-08-23
- Current commit reviewed: `804f55abb3694c4fc1fd46a685df3a7775ee2414`
- Commit date: 2026-08-23
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `privacy-networking-vpn`, especially zero-trust control-plane recovery, link reconciliation, and policy-backed routing state. The reusable mechanism is the reconnect path that resends the full router-link state with explicit delivery confirmation so stale controller state can be pruned safely.

## Verified Flow

`Router.NotifyOfReconnect` delegates to the link registry -> `linkRegistryImpl.NotifyOfReconnect` retries the reconnect announcement up to three times -> `sendFullRefresh` snapshots dialed links into a `RouterLinks` message with `FullRefresh: true` and sends it with `SendAndWaitForWire` -> the controller can prune links it no longer sees because the refresh is complete, not incremental -> tests prove the retry bound, closed-channel exit, and failure when the message was queued but not actually written -> related controller store tests verify router and service-policy data-model semantics.

- E1 source verified: `router/link/link_registry.go` implements reconnect retries, full-refresh construction, and wire-confirmed delivery.
- E2 test verified: `router/link/link_registry_test.go` verifies retry-until-delivered, bounded retries, channel-close exit, and queued-but-discarded failure semantics.
- E1 source verified: `common/router_data_model.go` defines the router/service/policy data model that the controller and router side both project into.
- E2 test verified: `controller/db/service_policy_store_test.go` and `controller/db/router_store_test.go` cover store semantics for service policies and routers.

## Architecture

Principal components:

- Router link registry: tracks dialed links and reconnect state.
- Controller data model: typed router, service, and policy projection.
- Controller DB stores: persist router and policy state.
- Test harnesses: confirm reconnect behavior and store semantics.

Most interesting mechanism: the reconnect path does not trust an incremental retry. It resends the whole link set with a `FullRefresh` flag and waits for wire-level confirmation so the controller can reconcile stale state and prune links that should no longer exist.

Baseline comparison: a simpler control plane would retry an announcement until the send queue accepts it. This repository distinguishes queue acceptance from wire delivery and treats accepted-but-undelivered messages as failures.

## Reuse Guidance

Reusable:

- Use a full-refresh reconnect message when the remote side needs to prune stale state.
- Confirm wire delivery rather than merely queue acceptance.
- Bound retries and exit cleanly on channel closure.
- Keep typed controller-side data models and store tests around the reconnect path.

Do not copy:

- Do not copy the whole router/controller surface without narrowing it to the relevant control-plane state.
- Do not treat queue acceptance as success.
- Do not assume the same refresh strategy works for every transport or topology.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The reconnect contract is explicitly tested.
- Delivery semantics are distinguished from queueing semantics.
- The control-plane data model is separated from the reconnect logic.

Experimental or incomplete for our needs:

- The codebase is large and heavily coupled to the rest of the Ziti control plane.
- The reconnect mechanism depends on the controller and channel semantics actually honoring `SendAndWaitForWire`.
- Operational behavior still needs live validation under controller load.

Hidden costs and failure modes:

- Full refreshes are more expensive than incremental deltas.
- A stuck controller or overloaded send path can still defer reconciliation until the next reconnect.
- If the controller or channel behavior changes, the “delivered versus queued” distinction can drift.

Adoption experiment:

Mirror this reconnect shape in one of our control paths, then inject a channel backlog and verify that a queued-but-never-written message is retried rather than falsely marked reconciled.

## Candidate Patterns

- `full-refresh reconnect reconciliation`
- `wire-confirmed control-plane announcement`
