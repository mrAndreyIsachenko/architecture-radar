# Tailscale Split-Tunnel Routing Exception Diagnostics

## Opportunity Summary
Public Tailscale issues repeatedly ask for domain, app, and device exceptions to exit-node and DNS routing behavior. The opportunity is a routing-policy diagnostic that explains what will break before users deploy mixed VPN or split-tunnel setups.

## Evidence
- M2 repeated pain: `#6912` (2023-01-08) asks for Android split tunneling so specific apps can bypass the VPN.
- M2 repeated pain: `#13677` (2024-10-03) asks for website-based/IP-based split tunneling on macOS.
- M2 repeated pain: `#18378` (2026-01-10) reports an Android regression where excluded apps lose network access after update.
- M2 repeated pain: `#15521` (2025-04-03) asks to exclude certain domains from Mullvad exit-node routing.
- M4 workaround evidence: `#15521` also describes using an App Connector as a suboptimal workaround for domain exclusions.
- M4 workaround evidence: `#3506` (2021-12-05) shows users disabling Tailscale DNS settings or manually manipulating DNS search order to cope.
- M3 competitor proof: the macOS split-tunneling request explicitly points to PIA as an open-source example that already implements the feature.

## Repeated Pain Or Demand Signal
Users want fine-grained control over where traffic goes, but the current model still forces coarse app exclusion, DNS hacks, or alternative VPNs for everyday web traffic.

## Likely User Or Buyer
IT admins, security-conscious teams, and power users managing laptops, phones, and home or office exit-node policies.

## Current Workaround Or Money Signal
People disable MagicDNS, use App Connectors, exclude the browser, or switch to other VPN products when Tailscale routing does not fit the workflow.

## Proposed Offer
A free routing-policy linter that checks a Tailscale configuration and explains whether it will need app split tunneling, domain exceptions, DNS overrides, or an App Connector.

## Success Threshold
At least 5 public users or admins run the linter in one week and report that it caught a real routing conflict before rollout.

## Falsification Threshold
Users say the current app-level workarounds are good enough, or they do not recognize split-tunnel friction as a recurring operational problem.

## Evidence Gaps
- No procurement or job-post evidence yet.
- Need better proof that admins would pay for diagnostics rather than rely on community knowledge.

## Decision
Selected.
