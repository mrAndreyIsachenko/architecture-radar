# google/sam

- Repository: https://github.com/google/sam
- Review date: 2026-10-07
- Current commit reviewed: `12dea1138cc40df0d440830d8c93de4408f95986`
- Commit date: 2026-10-07
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially durable agent workflows, sidecar-gated execution, tool discovery, and mesh-wide service invocation. The reusable mechanism is the sidecar-backed agent runtime, not the agent product framing.

## Verified Flow

`cmd/sam-node/main.go` builds the node, parses run flags, and starts the sidecar server -> `internal/node/sidecar.go::StartSidecarServer` mounts health, readiness, auth, egress, MCP, and OpenAI-compatible routes behind socket/token/mTLS gating -> `internal/node/mcp.go` registers local and remote mesh tools and documents when to call `discover_remote_services`, `find_remote_tools`, and `call_remote_tool` -> `internal/node/mcp_handlers.go` discovers services, narrows results, and calls remote tools over the mesh -> `internal/node/sidecar_test.go` verifies auth gating, token requirements, and readiness behavior -> `tests/integration/sdk_mesh_test.go::TestNativeSDKsMesh` runs a real mesh with routers, a sam-node, and SDK members that discover services and call tools over the mesh.

- E1 source verified: `internal/node/sidecar.go::StartSidecarServer`, `withAuth`, and the route mounting logic gate local API, egress, MCP, and OpenAI-compatible traffic.
- E1 source verified: `internal/node/mcp.go` and `internal/node/mcp_handlers.go` define and implement mesh service discovery and tool invocation.
- E1 source verified: `cmd/sam-node/main.go` wires the run command, sidecar startup, token handling, and mesh configuration.
- E2 test verified: `internal/node/sidecar_test.go` covers auth enforcement, authorization fallback scope, and token-mandatory startup behavior.
- E2 test verified: `tests/integration/sdk_mesh_test.go::TestNativeSDKsMesh` exercises multi-node mesh discovery, tool calls, and agent-card rewriting.

## Architecture

Principal components:

- Node bootstrap and run command.
- Sidecar HTTP API with explicit local-socket and token/mTLS gate behavior.
- MCP catalog and remote tool discovery.
- Mesh integration test harness with routers and SDK members.

Most interesting mechanism: the node treats local API access as a sidecar boundary and keeps discovery, auth, and tool invocation explicit. That gives the runtime a reusable contract even when the transport changes from socket to TCP.

Baseline comparison: a conventional agent mesh would couple discovery, auth, and tool invocation into one opaque SDK flow. SAM splits those responsibilities and surfaces them as distinct handlers and tools.

## Reuse Guidance

Reusable:

- Keep local-socket, token, and mTLS gates explicit at the sidecar boundary.
- Separate service discovery from remote tool invocation.
- Make mesh service catalogs callable from integration tests.
- Expose the readiness contract as part of the runtime, not only as an operational note.

Do not copy:

- Do not copy the mesh and SDK assumptions without confirming your transport and auth model.
- Do not rely on the OpenAI-compatible façade without validating downstream credential forwarding.
- Do not assume the integration test matrix substitutes for fleet-scale churn.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The sidecar route gating is source-backed and test-covered.
- Discovery and remote tool calling are explicit protocol steps.
- The integration test walks a real multi-node mesh.

Experimental or incomplete for our needs:

- The repository still reads as early-stage runtime work.
- The reviewed source does not prove fleet-scale reconnect churn or long-lived operational recovery.
- Some handlers are intentionally narrow and rely on mesh-specific assumptions.

Hidden costs and failure modes:

- Sidecar auth errors can wedge clients if the token or socket ownership drifts.
- Discovery can succeed while deeper mesh state is still unhealthy.
- Proxying credentials across the sidecar boundary requires careful header handling.

Adoption experiment:

Run a multi-node mesh with one sam-node, one router, and at least one SDK member, then restart the sidecar and a peer mid-run to confirm discovery, auth, and remote tool calls recover without leaking or duplicating credentials.

## Candidate Patterns

- `Evidence-Carrying Execution Envelopes`
- `readiness-gated sidecar runtime`
