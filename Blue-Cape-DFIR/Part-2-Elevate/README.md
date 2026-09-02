# Part 2 - Elevate Your DFIR Skills

This part moves from the general DFIR/forensics foundation built in Part 1 into a full, hands-on investigation: a single incident (Alice's compromised workstation) followed end to end across network capture, log aggregation, endpoint tooling, memory, disk, and timeline evidence.

## Structure

### [`01-security-operations/`](01-security-operations/)
SOC fundamentals - core capabilities, threat intel/hunting, incident handling - closing with the first hands-on lab: full PCAP reconstruction of the initial compromise.
→ [Lab: PCAP Analysis](01-security-operations/lab-pcap-analysis/README.md)

### [`02-incident-response-data-collection/`](02-incident-response-data-collection/)
Data collection and correlation at scale: SIEM-based investigation in Splunk, EDR-style collection with Velociraptor, and offline artifact collection techniques.
→ [Lab: Splunk SIEM Analysis](02-incident-response-data-collection/lab-splunk_SIEM-analysis/README.md)
→ [Lab: Velociraptor/EDR Analysis](02-incident-response-data-collection/lab-velociraptor_EDR-analysis/README.md)
→ [Lab: Collection Data](02-incident-response-data-collection/lab-collection-data/README.md)

### [`03-applied-forensic-analysis/`](03-applied-forensic-analysis/)
Deep artifact-level forensics on the same incident: memory analysis, disk analysis, and timeline reconstruction.
→ [Lab: Memory Analysis](03-applied-forensic-analysis/lab-memory-analysis/README.md)
→ [Lab: Disk Analysis](03-applied-forensic-analysis/lab-disk-analysis/README.md)
→ [Lab: Timeline Analysis](03-applied-forensic-analysis/lab-timeline-analysis/README.md)

## The case

All three sections investigate the same incident: a compromise of `Client2.BCS.local` (Alice's workstation) beginning with a Firefox-delivered HTA stager, leading to PowerShell-based C2, registry persistence, privilege escalation, and data staging/exfiltration. Each lab approaches this from a different evidence source - network, logs, memory, disk, timeline - and is documented independently so it stands on its own, without requiring the others for context.

A full narrative reconstruction of the attack, once every piece was in place, is documented at the repository root in [`Scenario-Reveal.md`](../Scenario-Reveal.md).
