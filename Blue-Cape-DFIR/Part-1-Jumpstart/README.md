# Part 1 - Jumpstart Your DFIR Journey

This folder contains the notes, reference materials, and visual assets for the first part of the Blue Cape DFIR course. It covers the threat landscape, essential forensic concepts, and the tools needed to build a strong DFIR workflow.

## Folder structure

- `README.md` - summary and guidance for this module
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

This folder contains all screenshots used for Part 1. The list below includes the most relevant diagrams and the broader visual assets that support each major section.

### Threat landscape and attacker behavior
- [attack-lifecycle.png](screenshots/attack-lifecycle.png) - ransomware and attacker lifecycle overview
- [a-ransomware-lifecycle.png](screenshots/a-ransomware-lifecycle.png) - ransomware lifecycle example
- [ransomware-attack-lifecycle.png](screenshots/ransomware-attack-lifecycle.png) - attack phases for ransomware cases
- [attack-infrastructure.png](screenshots/attack-infrastructure.png) - attacker infrastructure example
- [attack-post-exploitation.png](screenshots/attack-post-exploitation.png) - post-exploitation actions
- [organized-crime-ransomware.png](screenshots/organized-crime-ransomware.png) - organized cybercrime and ransomware ecosystem
- [understand-threat-landscape.png](screenshots/understand-threat-landscape.png) - threat landscape summary
- [data-breach.png](screenshots/data-breach.png) - data breach cost context
- [understanding-ressources.png](screenshots/understanding-ressources.png) - resources to understand threat context

### Incident response and forensic process
- [incident-response-process.png](screenshots/incident-response-process.png) - incident response workflow and phases
- [process-analysis.png](screenshots/process-analysis.png) - process analysis concepts
- [forensic-process.png](screenshots/forensic-process.png) - layered forensic analysis model
- [streamlined-forensic-analysis-workflow.png](screenshots/streamlined-forensic-analysis-workflow.png) - streamlined DFIR workflow
- [streamlined-forensic-analysis-workflow-diagram.png](screenshots/streamlined-forensic-analysis-workflow-diagram.png) - workflow diagram
- [forensic-resource.png](screenshots/forensic-resource.png) - key forensic resource types
- [incident-response-personas.png](screenshots/incident-response-personas.png) - incident response roles
- [dfir-most-challenging-area.png](screenshots/dfir-most-challenging-area.png) - common DFIR challenge areas
- [entrprise-dfir-domains.png](screenshots/entrprise-dfir-domains.png) - enterprise DFIR domains

### Windows, data sources, and evidence collection
- [data-acquisition-options.png](screenshots/data-acquisition-options.png) - evidence collection choices for Windows and VMs
- [data-acquisition-virtual-machines.png](screenshots/data-acquisition-virtual-machines.png) - acquisition options for virtual machines
- [windows-sources.png](screenshots/windows-sources.png) - Windows evidence source mapping
- [data-sources.png](screenshots/data-sources.png) - general forensic data sources
- [hard-drive-data-examination.png](screenshots/hard-drive-data-examination.png) - hard drive data examination
- [MFT-data-examination.png](screenshots/MFT-data-examination.png) - MFT data examination
- [NTFS-data-examination.png](screenshots/NTFS-data-examination.png) - NTFS artifacts and metadata extraction
- [resource-understand-timestamp-windows.png](screenshots/resource-understand-timestamp-windows.png) - Windows timestamp analysis
- [csv-file-sort.png](screenshots/csv-file-sort.png) - example CSV export and sorting

### Tools and environment
- [FTK-example.png](screenshots/FTK-example.png) - FTK tool demonstration and reporting
- [FTK-file-example-informations.png](screenshots/FTK-file-example-informations.png) - FTK file metadata example
- [autopsy.png](screenshots/autopsy.png) - Autopsy forensic GUI
- [an-example-of-cape.png](screenshots/an-example-of-cape.png) - CAPE/KAPE artifact collection example
- [forensic-workstation-goals.png](screenshots/forensic-workstation-goals.png) - forensic lab planning and goals
- [forensics-workstations-ready-vms.png](screenshots/forensics-workstations-ready-vms.png) - ready-made forensic workstation VMs
- [free-forensic-tools.png](screenshots/free-forensic-tools.png) - free forensic tool options
- [hands-on-analysis.png](screenshots/hands-on-analysis.png) - practical DFIR analysis focus
- [timesketch.png](screenshots/timesketch.png) - timeline analysis and collaboration
- [session_learn.png](screenshots/session_learn.png) - session learning outcomes

## Key resources

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


