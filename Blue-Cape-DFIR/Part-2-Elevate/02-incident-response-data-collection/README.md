# Incident Response and Data Collection Techniques

> **Module:** Part 2 – Elevate Your DFIR Skills
> **Topics covered:** 5 (per course outline)

## Overview

Where [Security Operations](../01-security-operations/README.md) established the network-layer story of Alice's compromise, this module goes deeper into host-side investigation and the tooling that supports it — moving from manual SIEM correlation to purpose-built EDR and collection frameworks, and closing with the underlying principles of sound forensic data collection.

## Topics

1. **Triage & Analysis Introduction** — theory, framing the investigative mindset for what follows
2. **Lab: Analysis SIEM/Splunk** — full host-based reconstruction of the attack chain from Sysmon and PowerShell logs
3. **Lab: Analysis EDR/Velociraptor** — exploring endpoint detection and response tooling as an alternative to manual log correlation
4. **Lab: Data Collection Techniques** — forensic principles behind live collection, disk imaging, and offline collection workflows
5. **Resources**

## Labs

| Lab | Focus | Status |
|---|---|---|
| [SIEM/Splunk Analysis](lab-splunk_SIEM-analysis/README.md) | Full attack chain reconstruction: delivery → execution → persistence → privilege escalation → staging, via Sysmon/PowerShell logs | Complete, fully reproduced |
| [EDR/Velociraptor Analysis](lab-velociraptor_EDR-analysis/README.md) | Velociraptor architecture, collection import, and hunt workflow | Exploratory — partially reproduced, see lab notes |
| [Data Collection Techniques](lab-collection-data/README.md) | Forensic data collection principles; KAPE-based offline collection via Velociraptor | Conceptual overview — course-demonstrated, not independently reproduced |

Additional reference material for this module is consolidated in [`resources.md`](resources.md).

## Key takeaway

The SIEM lab in this module is the most demanding piece of work in the repository so far — a single confirmed indicator (the malicious domain) followed, one `ProcessGuid` at a time, into a complete host-side kill chain. The Velociraptor and Data Collection labs then reframe that same investigation from a different angle: everything manually reconstructed in Splunk is exactly the kind of visibility an EDR platform is built to surface natively. Documenting both — the hard manual path and the tooling that would make it faster — is deliberate: understanding *why* EDR/collection tooling matters requires having felt the cost of not having it first.

## Next step

➡️ Part 3 – Knowledge Assessment
