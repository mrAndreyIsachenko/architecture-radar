# Opportunity Demand Radar Interests

This file is the authoritative source for opportunity and demand research priorities.

The radar should find evidence-backed opportunities, not generate speculative product ideas. Findings must connect to observed demand, repeated pain, or ecosystem movement that can be independently checked.

## Topic Scope

Prioritize opportunities related to:

- AI and LLM developer workflows.
- Agents, evals, memory, tool use, context engineering, and observability.
- Blockchain analytics, wallets, protocol tooling, and compliance-adjacent workflows.
- VPN, privacy networking, secure access, and traffic-control systems.
- Drones, robotics, autonomy, telemetry, fleet operations, and simulation.
- Document AI, OCR, multimodal extraction, and evidence ingestion.

Broad topical relevance is not enough. A selected opportunity must expose a concrete demand signal and a testable next step.

Use these topic families for candidate accounting:

- `ai-llm-demand`
- `blockchain-demand`
- `privacy-networking-demand`
- `drones-robotics-demand`
- `document-ai-demand`

## Current Priorities

### AI And LLM Developer Workflows

Open questions:

- Where are teams struggling to evaluate agent behavior before deployment?
- Which workflows need trace-backed debugging rather than more chat UI?
- Where do developers repeatedly ask for better memory, context, tool-call, or prompt-versioning infrastructure?
- Which open-source projects show real adoption but weak commercial packaging?

Useful signals:

- repeated GitHub issues describing the same operational failure;
- growing projects with unresolved enterprise concerns;
- discussion threads asking for hosted versions, integrations, or reliability features;
- benchmarks or eval harnesses that reveal missing tooling.

Avoid:

- generic "AI wrapper" ideas;
- one-off social media hype;
- ideas whose only evidence is a model announcement.

### Blockchain Intelligence

Open questions:

- Where do analysts still rely on manual transaction interpretation?
- Which protocol events are hard to explain from raw logs and traces?
- Where are wallet, compliance, tax, MEV, bridge, or risk workflows blocked by missing provenance?
- Which indexers have adoption but leave interpretation to downstream users?

Useful signals:

- repeated requests for protocol-specific decoding;
- public dashboards that require manual annotation;
- tooling gaps around reorgs, traces, attribution, or cross-chain flows;
- active repositories with users asking for higher-level semantics.

Avoid:

- pure trading signals;
- token recommendations;
- dashboards with no evidence model.

### Privacy Networking And VPN

Open questions:

- Where do teams need private access without managing brittle VPN infrastructure?
- Which operational failures repeat: DNS leaks, split tunnel bugs, key rotation, NAT traversal, route conflicts, device enrollment?
- Where are open-source tools strong technically but weak on policy, observability, or fleet administration?

Useful signals:

- recurring issues around deployment, policy, and diagnostics;
- projects with real users but missing admin workflows;
- requests for integrations with identity providers, device posture, or audit logs.

Avoid:

- consumer VPN ranking;
- marketing-only privacy claims;
- products requiring unnecessary traffic inspection.

### Drones, Robotics, And Autonomy

Open questions:

- Where do operators need better mission auditability, simulation, telemetry review, or safety workflows?
- Which autonomy tools lack evidence-backed replay, incident analysis, or fleet coordination?
- Where do developers struggle with MAVLink, PX4, ArduPilot, ROS 2, maps, or intermittent connectivity?

Useful signals:

- repeated issues around failsafe behavior, telemetry loss, mission planning, or simulation mismatch;
- ground-control or autonomy projects with integration pain;
- datasets or logs showing evaluation gaps.

Avoid:

- hardware-only projects;
- demo scripts with no operational users;
- black-box autonomy claims without logs or tests.

### Document AI And Evidence Ingestion

Open questions:

- Where do teams fail to parse long, messy, multilingual, or layout-heavy documents reliably?
- Which OCR/VLM tools have adoption but poor provenance, batching, runtime, or evaluation support?
- Where do users ask for better table extraction, page-region references, confidence, or reproducibility?

Useful signals:

- repeated issues about hallucinated text, dropped pages, broken tables, memory use, or runtime incompatibility;
- benchmarks with reproducible harnesses;
- projects that expose hard operational constraints.

Avoid:

- one-off OCR demos;
- cloud wrappers with no provenance model;
- benchmark claims without data or scoring code.

## Required Opportunity Shape

Every selected opportunity must include:

- evidence sources and dates;
- the repeated pain or demand signal;
- the likely user or buyer;
- why existing solutions are insufficient;
- what could be tested in one week;
- what would falsify the opportunity;
- confidence level and evidence gaps.

Do not recommend building a product unless the report connects evidence to a testable next action.
