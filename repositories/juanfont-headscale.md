# juanfont/headscale

- Repository: https://github.com/juanfont/headscale
- Review date: 2026-09-13
- Current commit reviewed: `4087d1fee9d34d042b279262ffbdaf1030ffd5e8`
- Commit date: 2026-09-10T14:12:53+02:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `privacy-networking-vpn`: route approval, policy reload, reconnect ordering, route visibility, and stale-health cleanup for a private network control plane.

## Verified Flow

Client reconnects with `MapRequest` hostinfo and announced routes -> `poll.go` updates node state before `Connect()` -> `State.Connect()` recalculates primary routes from the updated node store -> `SetApprovedRoutes()` persists approved routes and clears stale unhealthy state when approvals empty -> `ReloadPolicy()` re-reads policy, rebuilds peer maps, clears SSH check auth, and re-runs auto-approval -> `servertest` checks verify approved routes propagate to AllowedIPs and persist across restart.

- E1 source verified: `hscontrol/poll.go` processes the initial `MapRequest` before `state.State.Connect` so announced routes are present before primary-route selection.
- E1 source verified: `hscontrol/state/state.go:ReloadPolicy`, `SetPolicy`, and `AutoApproveRoutes` rebuild derived policy state, refresh peer maps, and persist auto-approved routes.
- E1 source verified: `hscontrol/state/state.go:SetApprovedRoutes` persists approved routes, clears stale unhealthy bits when approvals are empty, and emits policy changes when primary routes shift.
- E2 test verified: `hscontrol/servertest/routes_test.go::TestRoutes` verifies advertised routes reach hostinfo and approved routes appear in AllowedIPs.
- E2 test verified: `hscontrol/servertest/policy_test.go::TestPolicyChanges` verifies policy changes propagate into peer visibility and packet filters.
- E2 test verified: `hscontrol/state/persist_test.go::TestPersistEmptyApprovedRoutes` verifies cleared approved routes survive a restart instead of being re-applied from stale persistence.

## Architecture

Principal components:

- Control-plane state machine in `hscontrol/state`.
- Reconnect and poll handling in `hscontrol/poll.go`.
- Policy manager and route auto-approval logic.
- Servertest harnesses for route, policy, and restart regression coverage.

Most interesting mechanism: reconnect processing is deliberately ordered so the node store sees announced routes before connect-time route election. That avoids a stale empty-route window for subnet router failover and keeps route approval changes synchronized with policy reload.

Baseline comparison: a conventional VPN control plane often treats reconnect, policy, and route approval as loosely coupled updates. Headscale makes those transitions explicit and replays derived state when policy or route approval changes.

## Reuse Guidance

Reusable:

- Treat reconnect, policy reload, and route approval as one ordered reconciliation loop.
- Persist approved routes and derived health state together so stale approvals do not survive clears.
- Rebuild derived adjacency after policy changes before sending new netmaps.

Do not copy:

- Do not copy the product surface or deployment assumptions.
- Do not assume reconnect state can be applied after primary-route selection without races.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Strong source/test pairing around route propagation, policy changes, and persistence.
- Clear separation between raw node state and derived policy/reachability state.
- Restart regression coverage for approved-route persistence.

Experimental or incomplete for our needs:

- The review did not validate live multi-node reconnect behavior under production load.
- The HA health and route election path still deserves runtime validation outside the test harness.

Hidden costs and failure modes:

- Reconnect ordering bugs can create empty route windows or stale AllowedIPs.
- Policy reloads can drift from node-store state if derived adjacency is not rebuilt consistently.
- Route approval persistence has a restart blast radius if nil/empty slices are mishandled.

Adoption experiment:

Drive a reconnect plus policy-reload test against a live control plane, then confirm the node store, approved routes, and peer AllowedIPs converge in the same order after a disconnect/reconnect cycle.

## Candidate Patterns

- `policy-guarded route reconciliation loop`
- `reconnect-safe route approval propagation`

