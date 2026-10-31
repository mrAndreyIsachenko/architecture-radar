# juanfont/headscale

- Repository: https://github.com/juanfont/headscale
- Review date: 2026-10-31
- Current commit reviewed: `7721d8c29978b65b68269bb58391fcd25a8c1085`
- Commit date: 2026-10-30T14:51:17+00:00
- Branch: `main`
- Previous commit reviewed: `cee9066e91156d51e47fad3ca6c6bbda743750f0`
- Material changes since previous review: keeps the reconnect/policy model intact but closes a stale ephemeral-GC timer hole by deferring cancellation until after `Connect`, rejecting timers for nodes that are no longer ephemeral, and dropping queued deletions when the node has a live session.
- Decision: track

## Problem Fit

This repository informs `privacy-networking-vpn`, especially reconnect recovery, route approval, and control-plane behavior when a node rekeys, reconnects, or loses session state. The reusable mechanism is now more specific than the general policy-guarded route loop: the control plane uses generation-stamped ephemeral deletion timers so a reconnect, re-key, or failed poll cannot accidentally delete a node that has become permanent or already has a live session.

## Verified Flow

`app.go` installs the ephemeral garbage collector with a callback that first checks whether the node still exists, then whether it is still ephemeral, then whether it still has active sessions before deleting anything -> `poll.go` waits until `State.Connect` succeeds before cancelling the ephemeral timer, so a failed reconnect cannot clear a pending deletion schedule -> `db/node.go` arms timers with generation numbers, reaps old watcher goroutines on reschedule/cancel, and drops queued deletions whose generation no longer matches -> `poll_test.go` exercises failed reconnects, stale timers after re-keying, delete-cancels-timer behavior, and never-polled ephemeral cleanup.

- E1 source verified: `hscontrol/app.go:162-203` installs the ephemeral GC callback and rejects deletion when the node is gone, no longer ephemeral, or still has live sessions.
- E1 source verified: `hscontrol/poll.go:292-300` cancels ephemeral GC only after `Connect` succeeds, preserving the timer on failed reconnects.
- E1 source verified: `hscontrol/db/node.go:367-504` implements generation-stamped timer scheduling, cancel/reap semantics, and stale-deletion suppression.
- E2 test verified: `hscontrol/poll_test.go:301-361` proves a failed reconnect must not cancel the ephemeral GC timer.
- E2 test verified: `hscontrol/poll_test.go:363-448` proves a reconnected node survives a stale timer until it actually goes idle again.
- E2 test verified: `hscontrol/poll_test.go:450-575` proves delete cancels the timer and a saved ephemeral node still gets a GC timer.
- E2 test verified: `hscontrol/poll_test.go:577-623` proves re-keying to a permanent key does not let a stale timer delete the node.

## Architecture

Principal components:

- State-layer lifecycle hooks that own node visibility and session counts.
- Ephemeral-GC scheduling with explicit timer ownership and generation checks.
- Poll/long-poll sequencing that preserves the deletion timer across failed reconnects.
- Property and integration tests that pin stale-timer and re-key behavior.

Most interesting mechanism: reconnect recovery is not just about preserving routes or policy. The node lifecycle also protects against a stale timer from an earlier ephemeral identity. The timer is only cancelled when the reconnect actually succeeds, and the deletion callback refuses to act if the node has been re-keyed to permanent or already has a live session.

Baseline comparison: a simpler control plane would cancel the timer at poll entry or trust that a node's old ephemeral timer cannot outlive the old session. Headscale instead treats session count and node type as authoritative, so a stale timer becomes a no-op instead of a destructive surprise.

## Reuse Guidance

Reusable:

- Cancel cleanup timers only after the reconnect path has committed the new state.
- Make deletion callbacks re-check the live node type and session count before acting.
- Stamp queued deletions so a stale timer cannot delete a newer generation.
- Keep failed reconnects from clearing pending cleanup state.

Do not copy:

- Do not copy the timer pattern without the surrounding session-count and node-type checks.
- Do not assume a reconnect that failed before `Connect` can safely cancel cleanup.
- Do not treat the stale-timer tests as a substitute for live churn validation.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The deletion path is explicit about existence, ephemerality, and active sessions.
- The reconnect path has a test for failed reconnects preserving cleanup.
- Re-keying, delete, and never-polled states all have direct regression tests.

Experimental or incomplete for our needs:

- The source still needs live reconnect-storm validation with multiple nodes and route churn.
- The timer logic is safe in source, but operational proof under long churn is still missing.
- The control plane remains coupled to session and policy state; misuse of those checks can still strand or delete nodes incorrectly.

Hidden costs and failure modes:

- A stale GC timer can still delete a node if the re-checks drift from the state layer.
- Overly aggressive cancellation would reintroduce the "stranded offline" bug this change fixes.
- Cleanup logic is sensitive to races between reconnect, disconnect, and delete.

Adoption experiment:

Run a small tailnet with one ordinary node and one ephemeral node, trigger a failed reconnect and then a re-key to permanent while the old timer is still armed, and confirm that the timer survives the failed reconnect but becomes a no-op once the node is no longer ephemeral.

## Candidate Patterns

- `reconnect-safe route approval propagation`
- `session-epoch gated reconnect recovery`
- `atomic HA primary-election batch`
- `policy-driven peer-recompute gate`
- `tagged-node reauthentication guard`
- `API-key ownership projection`
- `generation-stamped cleanup timer`

## Previous Review

The [2026-10-13 report](../reports/2026-10-13.md) and the previous card recorded the tagged-node reauth, API-key ownership, and peer-recompute behavior at `cee9066e91156d51e47fad3ca6c6bbda743750f0`. This current review adds the stale-timer suppression path at `7721d8c29978b65b68269bb58391fcd25a8c1085`.
