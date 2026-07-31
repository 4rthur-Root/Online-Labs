# Part 1 - Jumpstart Your DFIR Journey

This folder contains the notes, reference materials, and visual assets for the first part of the Blue Cape DFIR course. It covers the threat landscape, essential forensic concepts, and the tools needed to build a strong DFIR workflow.

## Folder structure

- `Welcome to the first session.txt` - raw session notes from the webinar series
- `README.md` - high-level summary and guidance for this module
- `screenshots/` - slides and diagrams referenced throughout the course
- `Exterro FTK Suite 8.2 - Installation Guide.pdf` - FTK installation reference
- `Exterro FTK Suite 8.2 - Artifacts Guide.pdf` - FTK artifact extraction reference
- `Exterro FTK Suite 8.2 - Release Notes.pdf` - FTK version details
- `NIST.CSWP.29.pdf` - NIST source material for incident response and forensic process

## Summary

Part 1 is structured into three sessions:

1. **Understanding the Threat Landscape**
2. **Cyber Threats and Important Forensic Concepts**
3. **Essential Tools and Applications for DFIR Environments**

The goal is to move from general threat awareness to practical forensic techniques and tool selection.

## Session 1 - Understanding the Threat Landscape

This session introduces the DFIR discipline and explains why the threat landscape matters.

Key points:

- Threat actors and motivations
- Data breach cost context, with reference to IBM reports (2024 and 2026)
- Ransomware and attacker lifecycles
- Initial access vectors and how ransomware campaigns evolve
- NIST incident response process, based on the NIST SP 800-61r2 framework
- Forensic process foundations, including the four forensic process phases
- Case study: ransomware attack lifecycle, attack infrastructure, post-exploitation behavior
- Attacker mindset emphasis: think like the adversary to improve detection and response

## Session 2 - Cyber Threats and Important Forensic Concepts

This session deepens the technical foundation for DFIR investigations.

Key points:

- Mapping cyber threats to frameworks such as MITRE ATT&CK
- Ransomware, phishing, and business email compromise as attack vectors
- Review of the forensic analysis process, building on the initial session
- Windows data collection options and the importance of selecting the right evidence sources
- NTFS forensic artifacts, including `$MFT`, `$LogFile`, and `$UsnJrnl`
- FTK Imager demonstration and use cases for disk and memory acquisition
- Exporting artifacts such as MFT records to CSV for analysis
- Understanding file metadata, non-resident file records, and deleted file behavior in NTFS

### Useful command example

- `C:\Tools\EZTools\net6\MFTECmd.exe -f $MFT --csv`
- `MFTECmd.exe --de` for details on a specific file record

## Session 3 - Essential Tools and Applications for DFIR Environments

This session focuses on practical tools, lab design, and the workflow for forensic investigations.

Key points:

- Forensic workstation workflow:
  - Data acquisition
  - Data processing
  - Memory analysis
  - Disk analysis
  - Log analysis
  - Malware analysis
  - Timeline analysis
  - Reporting
- Lab planning: define goals and select the right resources before building the environment
- Available options: build your own forensic workstation versus using ready-made VMs
- Demo coverage for KAPE and Autopsy
- KAPE strengths: artifact collection, source targeting, and parser-driven extraction
- Autopsy strengths: graphical forensic analysis and evidence browsing
- Enterprise DFIR tool landscape: SIEM, EDR, NDR visibility triad
- Remote acquisition and automated processing using tools like Velociraptor, Plaso, and Timesketch
- Timesketch for timeline analysis and collaborative investigation

## Key visual assets

This folder contains 36 screenshot files. The list below highlights the primary visuals referenced in this summary, with additional useful diagrams in `screenshots/`.

- `screenshots/attack-lifecycle.png` — ransomware and attacker lifecycle overview
- `screenshots/incident-response-process.png` — incident response workflow and phases
- `screenshots/forensic-process.png` — layered forensic analysis model
- `screenshots/data-acquisition-options.png` — evidence collection choices for Windows and VMs
- `screenshots/NTFS-data-examination.png` — NTFS artifacts and metadata extraction
- `screenshots/FTK-example.png` — FTK tool demonstration and reporting
- `screenshots/understand-threat-landscape.png` — threat landscape summary
- `screenshots/data-breach.png` — data breach cost context
- `screenshots/attack-infrastructure.png` — example attacker infrastructure
- `screenshots/attack-post-exploitation.png` — post-exploitation behavior
- `screenshots/forensic-workstation-goals.png` — forensic lab planning and goals
- `screenshots/forensics-workstations-ready-vms.png` — ready-made forensic VM options
- `screenshots/timesketch.png` — timeline analysis and collaboration
- `screenshots/windows-sources.png` — Windows evidence source mapping
- `screenshots/streamlined-forensic-analysis-workflow.png` — streamlined DFIR workflow

## Recommended resources

- IBM data breach report: https://www.ibm.com/reports/data-breach
- NIST Cybersecurity Framework and incident response guidance: https://www.nist.gov/cyberframework
- FTK Imager download: https://accessdata.com/product-download/ftk-imager-version-4-2
- Eric Zimmerman tools: https://ericzimmerman.github.io/
- MITRE ATT&CK: https://attack.mitre.org/
- Blue Cape forensic workstation guide: https://bluecapesecurity.com/build-your-forensic-workstation/
- Autopsy: https://www.sleuthkit.org/autopsy/
- Timesketch: https://www.timesketch.org/
- Velociraptor docs: https://docs.velociraptor.app/
- NTFS artifact cheat sheet: https://github.com/bluecapesecurity/PWF

## How to use this folder

- Start with `Welcome to the first session.txt` to review the raw notes from the course.
- Use `screenshots/` to view the slide visuals and reinforce key concepts.
- Open the provided PDF guides for deeper reference on FTK and NIST process details.
- Use this `README.md` as the structured summary and learning roadmap for Part 1.

