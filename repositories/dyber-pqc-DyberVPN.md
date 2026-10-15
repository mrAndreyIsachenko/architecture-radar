# dyber-pqc/DyberVPN

- Repository: https://github.com/dyber-pqc/DyberVPN
- Review date: 2026-10-07
- Current commit reviewed: `943cf5012dc370a5768550eab6a0b7a3c71711c7`
- Commit date: 2026-07-27
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `privacy-networking-vpn`, especially route/policy reconciliation, key revocation, reconnect-safe control planes, and audit-friendly tunnel enforcement. The reusable mechanism is the policy-and-revocation loop, not the crypto or branding around it.

## Verified Flow

`PolicyEngine::new` loads and compiles the role policy, optionally from an external file -> `normalize_peer_key` rejects truncated fingerprints and only accepts full 32-byte keys -> `PolicyEngine::evaluate` matches by peer name or full key, applies first-match-wins rule evaluation, and defaults closed when no rule matches -> `PolicyEngine::reload` hot-reloads policy from disk -> `RevocationEngine::new` loads the CRL and persisted first-seen timestamps -> `check_key`, `revoke_key`, `suspend_key`, and `reinstate_key` maintain the revocation lifecycle -> `daemon::handle_reload`, `scan_revoked_peers`, and `handle_timers` enforce reload and revocation during runtime -> the CLI commands expose revocation, suspension, reinstatement, and listing.

- E1 source verified: `crates/dybervpn-tunnel/src/policy.rs::normalize_peer_key`, `PolicyEngine::new`, `evaluate`, and `reload` implement full-key policy matching and hot reload.
- E1 source verified: `crates/dybervpn-tunnel/src/revocation.rs::check_key`, `revoke_key`, `suspend_key`, `reinstate_key`, `reload`, and `list_revoked` implement the CRL lifecycle and restart-persistent first-seen timestamps.
- E1 source verified: `crates/dybervpn-tunnel/src/daemon.rs::handle_reload`, `scan_revoked_peers`, and `handle_timers` apply policy and revocation during live packet processing.
- E1 source verified: `crates/dybervpn-cli/src/main.rs::cmd_revoke_key`, `cmd_suspend_key`, `cmd_reinstate_key`, and `cmd_list_revoked` wire the lifecycle into the CLI.
- E2 test verified: `crates/dybervpn-tunnel/src/policy.rs` and `revocation.rs` tests cover full-key matching, collision rejection, policy-from-JSON loading, CRL roundtrip, suspend/reinstate, and stats tracking.

## Architecture

Principal components:

- Policy engine with explicit per-peer name/key caches and hot reload.
- Revocation engine with CRL persistence, expiration, suspension, and reinstatement.
- Tunnel daemon that enforces reload, revocation scanning, and key-age checks during live operation.
- CLI operations for human-managed revocation lifecycle changes.

Most interesting mechanism: the daemon does not trust a short fingerprint or a stale policy blob. It treats the full key, policy file, and CRL as authoritative sources and replays them into the live enforcement path on reload.

Baseline comparison: a basic VPN daemon would authenticate peers and forward packets, but leave policy and revocation changes to restarts. DyberVPN makes policy and revocation a live control surface.

## Reuse Guidance

Reusable:

- Require full-key matching for policy and revocation decisions.
- Keep policy reload and revocation reload explicit and fail-closed.
- Persist revocation and first-seen timestamps so key-age logic survives restart.
- Make revoke/suspend/reinstate operations first-class administrative commands.

Do not copy:

- Do not copy the CLI UX or config layout without a real gateway need.
- Do not rely on short fingerprints for anything security-sensitive.
- Do not adopt the daemon loop without reconnect and reload validation on real links.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Policy evaluation, revocation, and daemon enforcement are all source-backed.
- Collision and malformed-input cases have direct tests.
- Reload is an explicit path, not a side effect.

Experimental or incomplete for our needs:

- The reviewed source does not prove live reconnect/reload churn on a real deployment.
- Policy and revocation logic are split across tunnel and CLI crates.
- The full behavior under simultaneous reload, disconnect, and revocation pressure remains unproven.

Hidden costs and failure modes:

- A truncated or colliding fingerprint can create a privilege or denial bug if reused incorrectly.
- CRL and policy reloads can diverge if operators change one without the other.
- Session and key-age logic depends on the correctness of persisted first-seen data.

Adoption experiment:

Run the tunnel through a disconnect/reconnect cycle while reloading policy and CRL updates, then confirm revoked peers stay blocked, reinstated peers recover, and no stale route or key-acceptance state survives the churn.

## Candidate Patterns

- `Policy-Guarded Route Reconciliation Loop`
- `full-key policy and revocation gate`
