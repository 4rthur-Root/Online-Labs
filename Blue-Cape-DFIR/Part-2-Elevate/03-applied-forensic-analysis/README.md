# 03 — Applied Forensic Analysis

This section applies deep, artifact-level forensics to the same incident investigated in the earlier sections of Part 2 — this time from the underlying evidence itself (RAM, disk, and a unified timeline) rather than from logs or network capture.

Reference process followed throughout: **Data acquisition → Processing → Memory analysis → Disk → Log → Malware → Timeline → Report**

## Labs

### [Memory Analysis](lab-memory-analysis/README.md)
Full volatile memory forensics on `memdump.mem` using Volatility 3, raw string extraction, and bulk_extractor. Recovered the fileless PowerShell persistence chain, registry-staged payload, and C2 beacon details (`3.140.33.120:9001`, spoofed User-Agent) directly from RAM.

### [Disk Analysis](lab-disk-analysis/README.md)
Registry hive triage (`SYSTEM`, `SOFTWARE`, `NTUSER.DAT`) using RegRipper, confirming host identity and disabled Defender protections. Paused partway through deeper artifact extraction — documented transparently, including why.

### [Timeline Analysis](lab-timeline-analysis/README.md)
Intended to unify all prior evidence sources into a single chronological view via Plaso/Timesketch. Reviewed through the instructor's walkthrough (notably, plaintext recovery of previously base64-encoded payloads); an independently-generated working timeline was not yet produced. Paused, with a clear next step identified.

## Resources

See [`RESOURCES.md`](RESOURCES.md) for the tools, cheat sheets, and case file references used across all three labs.

## Status

Memory analysis is complete and fully documented. Disk and timeline analysis reached a solid theoretical and initial-triage stage but are currently **paused on tooling blockers** (RegRipper's mixed-encoding output; Timesketch's strict CSV schema with no reference command available) rather than on a gap in understanding — confirmed independently by a 100% score on both the "Disk and Memory Analysis" and "Timeline Analysis" categories of the course's knowledge assessment. Both labs document exactly what was attempted, what blocked progress, and the concrete next step to unblock them.
