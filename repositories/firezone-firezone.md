# firezone/firezone

- Repository: https://github.com/firezone/firezone
- Review date: 2026-08-02
- Current commit reviewed: `2b4ffb54ec248ca26cb327af2717f7f8801e3b2f`
- Commit date: 2026-08-01T15:46:11-07:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `privacy-networking-vpn`: secure tunnels, policy-controlled access, DNS and route management, least-privilege connectivity, and observable network behavior.

## Verified Flow

Gateway startup enforces privileges -> reads `/etc/resolv.conf` -> constructs `GatewayTunnel` -> creates a `PhoenixChannel` with exponential backoff -> `Eventloop` reacts to portal messages and tunnel events -> `InitGateway`/authorization messages configure relays, routes, DNS rebinding, and tunnel state -> queue callback tests confirm session durability and identity-merge behavior on the portal side.

- E1 source verified: `rust/gateway/src/main.rs` checks for `root` or `CAP_NET_ADMIN`, loads resolver config, creates the tunnel, and starts portal connectivity with backoff.
- E1 source verified: `rust/gateway/src/eventloop.rs` handles `InitGateway`, `Authorization`, `RejectAccess`, relay updates, route setup, and DNS rebinding.
- E1 source verified: `elixir/test/portal/queue/callbacks_test.exs` verifies queue callback durability, `firezone_id` merge behavior, and session log persistence.
- E1 source verified: `rust/headless-client/src/main.rs` ties policy-granted access to resource activation and DNS-control behavior.

## Architecture

Principal components:

- Rust gateway process, tunnel state, and portal event loop.
- Elixir portal queue and persistence side for durable session callbacks.
- Headless client and policy-controlled activation path.
- DNS, routing, and relay state mutation in response to portal events.

Most interesting mechanism: the gateway does not act as a simple tunnel daemon. It is a policy-driven event loop that turns portal authorization and relay updates into concrete route/DNS/tunnel mutations.

Baseline comparison: a conventional VPN client exposes a static tunnel and maybe a GUI. Firezone splits control plane and data plane, then drives the tunnel from policy and portal events.

## Reuse Guidance

Reusable:

- Keep portal authorization, route selection, and DNS rebinding as explicit events in the control loop.
- Preserve queue durability around session and identity updates.
- Separate least-privilege policy checks from tunnel packet forwarding.

Do not copy:

- Do not copy the product UX or deployment packaging.
- Do not ignore the privileged execution requirement on Linux.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Multi-language implementation with explicit gateway, portal, and test coverage.
- Backoff, telemetry, resolver parsing, and teardown logic are source-verified.
- Queue tests cover real persistence edge cases.

Experimental or incomplete for our needs:

- The review did not validate an end-to-end deployment.
- Policy semantics are distributed across Rust and Elixir components.

Hidden costs and failure modes:

- The gateway needs elevated privileges.
- DNS and route mutation are high-blast-radius operations.
- Multi-process control plane logic can drift if event contracts are not tested.

Adoption experiment:

Prototype a control-loop adapter that turns authorization events into tunnel/DNS/routing updates, then inject disconnects and route changes to verify the gateway always converges back to the last authorized state.

## Candidate Patterns

- `policy-guarded tunnel event loop`
- `queue-durable session merge`
