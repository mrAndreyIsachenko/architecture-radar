# juanfont/headscale

- Repository: https://github.com/juanfont/headscale
- Review date: 2026-10-22
- Current commit reviewed: `cc66979b16cfbdc76b1d582b028108bb8b823354`
- Commit date: 2026-10-20T11:55:11+02:00
- Branch: `main`
- Previous commit reviewed: `cee9066e91156d51e47fad3ca6c6bbda743750f0`
- Material changes since previous review: adds authoritative ACME DNS challenge publication and propagation waits, expands the peer-map index benchmark surface, and refreshes TLS/DNS/policy tests while keeping the reconnect and peer-recompute gates intact.
- Decision: track

## Problem Fit

This repository informs `privacy-networking-vpn`, especially reconnect recovery, route approval, tagged-node reauthentication, and DNS-certificate issuance under churn. The reusable mechanism is the combination of policy compilation, authoritative challenge propagation, node-store snapshots, auth-path ownership handling, and session-aware connect/disconnect logic that keeps peer recomputation bounded.

## Verified Flow

`dns.NewChallenges` wires DNS certificate issuance into server startup -> `Challenges.Present` publishes TXT records, enforces per-node limits, extends challenge lifetime on successful propagation, and keeps ownership stable across renames -> `dns.AwaitTXT` / `txtChecker.wait` follow CNAMEs, resolve authoritative nameservers, and wait for all of them to serve the TXT value before returning -> `PolicyManager::NewPolicyManager` parses and validates policy, resolves user references, compiles filter and grant structures, and caches the derived peer/filter artifacts -> `buildPeerMapPairScan` keeps the old pair-scan peer-map behavior as a reference for the indexed builder -> `TestReloadPolicyRebuildsPeerMapOnChangeOnly` proves a policy write rebuilds once on change and not on idempotent reload -> `TestSetDNS` drives the Noise-authenticated SetDNS path and confirms rename-following certificate domains -> `TestACMETLSSettings` spins up Pebble plus authoritative DNS to validate TLS settings for each challenge type.

- E1 source verified: `hscontrol/app.go:144-150,170-193` wires challenge handling into startup and keeps the ephemeral garbage collector session-aware.
- E1 source verified: `hscontrol/dns/challenge.go:23-207` implements challenge TTL, lifetime extension, per-node limits, ownership transfer, propagation waits, and provider append/delete semantics.
- E1 source verified: `hscontrol/dns/propagation.go:28-237` implements authoritative TXT propagation waits, CNAME chain following, nameserver lookup, and not-propagated errors.
- E1 source verified: `hscontrol/policy/v2/policy.go:32-103,198-220` implements policy validation, cache invalidation, auto-approver resolution, and the peer-recompute metadata gate.
- E2 test verified: `hscontrol/policy/v2/peermap_scan_test.go:17-80` defines the reference pair-scan peer-map builder that the indexed implementation must match.
- E2 test verified: `hscontrol/state/reload_policy_test.go:12-88` proves changed policies rebuild the peer map once and idempotent reloads do not.
- E2 test verified: `hscontrol/servertest/setdns_test.go:19-88` exercises authenticated SetDNS ownership checks and rename-following certificate domains.
- E2 test verified: `hscontrol/app_tls_test.go:34-240` drives Pebble plus authoritative DNS to validate ACME/TLS settings end to end.
- E2 test verified: `hscontrol/policy/v2/peermap_scan_test.go:295-833` validates the indexed peer-map builder against the reference pair-scan behavior across randomized policy and node sets.
- E2 test verified: `hscontrol/state/reload_policy_test.go:17-88` confirms a policy write rebuilds once on change and not on repeated reload of the same state.
- E2 test verified: `hscontrol/servertest/setdns_test.go:21-88` confirms unauthorized SetDNS attempts are rejected and certificate domains follow node renames.
- E2 test verified: `hscontrol/app_tls_test.go:191-240` proves the ACME settings work with DNS-01, HTTP-01, and TLS-ALPN-01.

## Architecture

Principal components:

- DNS challenge manager with per-node ownership and propagation waits.
- Policy manager that compiles ACLs, grants, auto-approvers, and SSH policy.
- NodeStore copy-on-write snapshot with atomic batched writes and route-election state.
- State layer that coordinates connect/disconnect, approved routes, auth-path reauth, and health updates.
- ACME and DNS integration tests that pin certificate issuance, propagation, and rename behavior.

Most interesting mechanism: Headscale now separates three expensive transitions that are easy to confuse in a control plane. Reconnect recovery is session-aware rather than epoch-only, DNS issuance waits for authoritative propagation rather than the first resolver response, and peer-map rebuilds are change-detected rather than recomputed on every reload. That keeps ordinary reconnects and reloads cheap while making the risky paths explicit.

Baseline comparison: a simpler control plane would treat every reconnect, DNS challenge, or policy reload as a fresh lifecycle event. Headscale narrows the fan-out, keeps ordinary reconnects lightweight, and preserves machine identity and certificate issuance semantics when the same node legitimately reauthenticates or retags.

## Reuse Guidance

Reusable:

- Separate ordinary reconnects from topology-changing reconnects.
- Wait for authoritative propagation, not just a first resolver response, before treating a DNS challenge as ready.
- Use a session count, not only a last-epoch check, to avoid stranding a node online after out-of-order disconnects.
- Preserve tagged-node ownership and key-expiry semantics across restart and reauth paths.
- Batch HA health flips so primary election sees the post-batch state only.
- Keep policy compilation caches explicit and invalidate them only when the derived artifacts actually change.
- Use a reference pair-scan test when introducing a faster peer-map builder.

Do not copy:

- Do not copy the NodeStore snapshot layout without understanding the surrounding policy and DB contracts.
- Do not copy the ACME propagation waits without the authoritative-DNS assumptions that make them meaningful.
- Do not assume the recompute gates are sufficient without real reconnect churn and multi-node validation.
- Do not treat the property tests as a substitute for live overlay recovery.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The control plane distinguishes ordinary peer patches from expensive recompute paths.
- Route approval, connect/disconnect, auth-path restart behavior, authoritative DNS propagation, and HA health all have tests that codify the intended invariants.
- NodeStore write batching and snapshot replacement are explicit rather than accidental.
- The new peer-map benchmark/test surface keeps the faster builder honest against the reference scan.

Experimental or incomplete for our needs:

- The source evidence is strong, but live reconnect storms, mixed-role HA recovery, and tagged-node restart churn still need runtime validation.
- The current code assumes the DNS provider and authoritative servers remain coherent under concurrent churn; that is well motivated but still deserves operational proof.
- The policy layer is broad and can become coupling-heavy if reused without the rest of the state machine.

Hidden costs and failure modes:

- A stale unhealthy bit or stale primary assignment can mislead peer routing if health and disconnect paths diverge.
- Too many recompute triggers would reintroduce CPU-heavy fan-out on reconnect storms.
- Tagged-node reauth and spent-key restart paths are security-sensitive: a bad ownership decision can either strand a valid node or silently authorize the wrong one.
- DNS propagation waits can stall certificate issuance if authoritative servers or resolvers are slow or inconsistent.

Adoption experiment:

Run a small tailnet with one ordinary node and one subnet-router or relay target, inject reconnect storms plus overlapping disconnects, and then re-authenticate a tagged node with a reused preauth key while also issuing a certificate challenge to confirm ordinary reconnects stay lightweight, topology-changing nodes still trigger exactly one recompute, and DNS issuance waits for authoritative propagation rather than a first-resolver guess.

## Candidate Patterns

- `authoritative ACME challenge propagation gate`
- `reconnect-safe route approval propagation`
- `session-epoch gated reconnect recovery`
- `atomic HA primary-election batch`
- `policy-driven peer-recompute gate`
- `tagged-node reauthentication guard`
- `API-key ownership projection`
