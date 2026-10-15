# juanfont/headscale

- Repository: https://github.com/juanfont/headscale
- Review date: 2026-10-13
- Current commit reviewed: `cee9066e91156d51e47fad3ca6c6bbda743750f0`
- Commit date: 2026-10-13T05:01:46Z
- Branch: `main`
- Previous commit reviewed: `c90ba0f0d6f82fe79fc2da82d95561f0e2780628`
- Material changes since previous review: adds tagged-node reauth expiry guards, reused-user-preauth-key recovery, API-key prefix/expiry/user-assignment handling, and refreshed reconnect/health tests while keeping the bounded peer-recompute gate intact.
- Decision: track

## Problem Fit

This repository informs `privacy-networking-vpn`, especially reconnect recovery, route approval, tagged-node reauthentication, and control-plane behavior when policy or node health changes. The reusable mechanism is the combination of policy compilation, node-store snapshots, auth-path ownership handling, and session-aware connect/disconnect logic that keeps peer recomputation bounded.

## Verified Flow

`PolicyManager::NewPolicyManager` parses and validates policy, resolves user references, compiles filter and grant structures, and caches the derived peer/filter artifacts -> `HandleNodeFromAuthPath` loads the cached registration, resolves the user, serializes by machine key, and either updates the existing node or creates a new one while preserving tag ownership and policy refresh ordering -> `HandleNodeFromPreAuthKey` reuses tagged nodes on legitimate restart, rejects ambiguous machine-key ownership, and only re-validates spent keys when the reauth path actually changes ownership or key state -> `db.ValidateAPIKey` / `AuthenticateAPIKey` parse prefixed or legacy API keys and enforce expiry/user ownership -> `State.Connect` increments the node session epoch, marks the node online, clears unhealthy state, emits a lightweight online change, and only emits a policy recompute when the node role requires it -> `State.Disconnect` decrements active sessions, only marks offline when the last live session ends, persists last-seen data, and emits the minimal offline change plus policy recompute when needed -> `State.BatchSetNodeHealth` applies health flips atomically and runs primary-route election once after the batch -> `auth_tagged_expiry_test.go`, `connect_test.go`, `node_recompute_test.go`, and `node_health_test.go` exercise tagged reauth expiry, reused-user PAK restart behavior, ordinary reconnects, relay/subnet-router recompute gates, and batched health invariants.

- E1 source verified: `hscontrol/policy/v2/policy.go:32-103,198-240` implements policy validation, cache invalidation, auto-approver resolution, and the peer-recompute classification gate.
- E1 source verified: `hscontrol/state/state.go:2379-2540,2574-2725` implements auth-path node updates, tagged-node recovery, preauth-key restart behavior, and policy refresh ordering.
- E1 source verified: `hscontrol/db/api_key.go:28-220` implements API-key creation, expiry, authentication, prefix parsing, and owner assignment.
- E1 source verified: `hscontrol/types/api_key.go:13-63` implements masked logging for API-key identity and expiration metadata.
- E1 source verified: `hscontrol/state/state.go:651-760,1470-1581` implements connect/disconnect session handling, approved-route persistence, batched node-health updates, and API-key passthrough helpers.
- E2 test verified: `hscontrol/state/connect_test.go:56-209,238-275` covers ordinary reconnects, relay-target recompute, subnet-router recompute, and out-of-order disconnect safety.
- E2 test verified: `hscontrol/policy/v2/node_recompute_test.go:12-132` pins which node roles force peer recomputation.
- E2 test verified: `hscontrol/state/node_health_test.go:69-85` confirms unchanged health writes skip publication.
- E2 test verified: `hscontrol/state/auth_tagged_expiry_test.go:20-239` covers tagged reauth expiry retention, reused-user one-shot-key restart behavior, and expired-node key reuse guards.

## Architecture

Principal components:

- Policy manager that compiles ACLs, grants, auto-approvers, and SSH policy.
- NodeStore copy-on-write snapshot with atomic batched writes and route-election state.
- State layer that coordinates connect/disconnect, approved routes, auth-path reauth, and health updates.
- API-key parsing and projection helpers that normalize expiry and owner identity.
- Property and integration tests that pin reconnect, tagged reauth, and HA election behavior.

Most interesting mechanism: reconnect recovery is session-aware rather than epoch-only, and the auth path is ownership-aware rather than key-string-only. A node only goes offline when the last session is released, and tagged-node reauth, spent preauth keys, and API-key expiry rules all preserve the distinction between ordinary reconnects and ownership-changing transitions.

Baseline comparison: a simpler control plane would treat every reconnect or auth callback as a fresh node lifecycle event. Headscale narrows the fan-out, keeps ordinary reconnects lightweight, and preserves machine identity when the same node legitimately reauthenticates or retags.

## Reuse Guidance

Reusable:

- Separate ordinary reconnects from topology-changing reconnects.
- Use a session count, not only a last-epoch check, to avoid stranding a node online after out-of-order disconnects.
- Preserve tagged-node ownership and key-expiry semantics across restart and reauth paths.
- Batch HA health flips so primary election sees the post-batch state only.
- Keep policy compilation caches explicit and invalidate them only when the derived artifacts actually change.

Do not copy:

- Do not copy the NodeStore snapshot layout without understanding the surrounding policy and DB contracts.
- Do not assume the recompute gates are sufficient without real reconnect churn and multi-node validation.
- Do not treat the property tests as a substitute for live overlay recovery.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The control plane distinguishes ordinary peer patches from expensive recompute paths.
- Route approval, connect/disconnect, auth-path restart behavior, and HA health all have tests that codify the intended invariants.
- NodeStore write batching and snapshot replacement are explicit rather than accidental.

Experimental or incomplete for our needs:

- The source evidence is strong, but live reconnect storms, mixed-role HA recovery, and tagged-node restart churn still need runtime validation.
- The current code assumes the policy and node-store layers remain coherent under concurrent churn; that is well motivated but still deserves fault-injection proof.
- The policy layer is broad and can become coupling-heavy if reused without the rest of the state machine.

Hidden costs and failure modes:

- A stale unhealthy bit or stale primary assignment can mislead peer routing if health and disconnect paths diverge.
- Too many recompute triggers would reintroduce CPU-heavy fan-out on reconnect storms.
- Tagged-node reauth and spent-key restart paths are security-sensitive: a bad ownership decision can either strand a valid node or silently authorize the wrong one.

Adoption experiment:

Run a small tailnet with one ordinary node and one subnet-router or relay target, inject reconnect storms plus overlapping disconnects, and then re-authenticate a tagged node with a reused preauth key to confirm ordinary reconnects stay lightweight while topology-changing nodes still trigger exactly one recompute and tagged reauth stays keyed to the same machine identity.

## Candidate Patterns

- `reconnect-safe route approval propagation`
- `session-epoch gated reconnect recovery`
- `atomic HA primary-election batch`
- `policy-driven peer-recompute gate`
- `tagged-node reauthentication guard`
- `API-key ownership projection`
