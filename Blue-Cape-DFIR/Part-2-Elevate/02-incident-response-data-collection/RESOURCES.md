# Resources — Incident Response and Data Collection Techniques

Reference material and tool downloads used across this module's three labs (SIEM/Splunk, EDR/Velociraptor, Data Collection Techniques).

## Case files

The evidence set used throughout Part 2 — Disk Triage Collection, Memory Image + pagefile.sys, PCAP file, and Splunk log export — was downloaded once at the start of Part 2 and is referenced across all labs in this section and in [`01-security-operations/`](../01-security-operations/README.md). See the [lab setup notes](../lab-setup/README.md) for details.

## Tool downloads and guides

- **Splunk**: [Download & setup](https://www.splunk.com/en_us/download.html) — used for log aggregation and SPL-based analysis in the [SIEM lab](lab-splunk_SIEM-analysis/README.md).
- **Velociraptor**: [Documentation](https://docs.velociraptor.app/) — open-source endpoint data collection and forensic tool, used in the [EDR lab](lab-velociraptor_EDR-analysis/README.md) and the [offline collection workflow](lab-collection-data/README.md).
- **FTK Imager**: [Download](https://accessdata.com/product-download/ftk-imager-version-4-2) — disk and memory image acquisition, first introduced in Part 1.
- **Practical Windows Forensics (PWF) Cheat Sheet**: [GitHub](https://github.com/bluecapesecurity/PWF) — step-by-step reference for parsing forensic artifacts, useful throughout the Splunk and Velociraptor labs.

## Incident response & log analysis references

- Blue Cape Security's blog and articles on correlating Sysmon logs with Windows Event Logs in a SOC context: [bluecapesecurity.com](https://bluecapesecurity.com/)
- **Build Your Forensic Workstation** guide — used as a reference when setting up this repo's own [lab environment](../lab-setup/README.md): [bluecapesecurity.com/build-your-forensic-workstation](https://bluecapesecurity.com/build-your-forensic-workstation/)

## Technique references cited in this module's labs

- **MITRE ATT&CK T1218.005 (Mshta)**: [attack.mitre.org/techniques/T1218/005](https://attack.mitre.org/techniques/T1218/005/)
- **LOLBAS project — Mshta**: [lolbas-project.github.io/lolbas/Binaries/Mshta](https://lolbas-project.github.io/lolbas/Binaries/Mshta/)
- **Red Canary — Mshta threat detection report**: [redcanary.com/threat-detection-report/techniques/mshta](https://redcanary.com/threat-detection-report/techniques/mshta/)
