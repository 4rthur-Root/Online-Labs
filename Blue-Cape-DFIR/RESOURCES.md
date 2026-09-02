# Resources

Tools, references, and case material used across this project.

## Case Files

The full case data set — PCAP, memory image, disk triage collection, and log files — is provided by Blue Cape Security in the course's case file lesson. See [`Scenario-Reveal.md`](Scenario-Reveal.md) for the full incident narrative these files support.

## Tools

| Tool | Purpose | Link |
|---|---|---|
| Wireshark | Packet capture analysis | https://www.wireshark.org/ |
| Splunk | Log aggregation and SIEM correlation | https://www.splunk.com/en_us/download.html |
| Sysmon | Windows system activity logging (process creation, network, registry) | https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon |
| Volatility 3 | Memory analysis | https://github.com/volatilityfoundation/volatility3 |
| bulk_extractor | Pattern/string extraction from unstructured data | https://github.com/simsong/bulk_extractor |
| RegRipper 3.0 | Windows registry hive parsing | https://github.com/keydet89/RegRipper3.0 |
| Eric Zimmerman's Tools | NTFS / MFT analysis | https://ericzimmerman.github.io/ |
| FTK Imager | Forensic disk/memory image acquisition | https://www.exterro.com/digital-forensics-software/ftk-imager |
| Velociraptor | Remote endpoint collection and analysis (EDR-style) | https://docs.velociraptor.app/ |
| Timesketch | Timeline building and analysis | https://www.timesketch.org/ |

## Cheat Sheets & Setup Guides

- [Practical Windows Forensics Cheat Sheet (PDF, root of this repo)](PracticalWindowsForensics-cheat-sheet.pdf)
- [Blue Cape Security PWF GitHub repository](https://github.com/bluecapesecurity/PWF) — includes the Atomic-Red-Team-based attack simulation script used to generate a realistic compromise scenario, and the PWFA certification track
- [Build Your Forensic Workstation Guide](https://bluecapesecurity.com/build-your-forensic-workstation/) — lab environment setup

## Section-specific resources

Tooling and references specific to memory/disk/timeline forensics are documented separately in [`Part-2-Elevate/03-applied-forensic-analysis/RESOURCES.md`](Part-2-Elevate/03-applied-forensic-analysis/RESOURCES.md).
