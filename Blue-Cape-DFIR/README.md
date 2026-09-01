# Blue Cape Security — DFIR Foundations and Techniques

<div align="center">
  <h3>Tools used across this project</h3>
  <table>
    <tr>
      <td align="center" width="100">
        <img src="assets/splunk.jpeg" width="80" alt="Splunk"/><br/>
        <sub>Splunk</sub>
      </td>
    </tr>
  </table>
</div>

This repository documents hands-on practice through Blue Cape Security's free **DFIR Foundations and Techniques** course — SOC operations, incident response, and applied digital forensics. All analysis was performed on self-hosted virtual machines for educational purposes.

**Certificate of Completion:** [`DFIR-Certificate.pdf`](DFIR-Certificate.pdf) — 94.37% (67/71), 8 CEUs.

## Structure

### [`Part-0-Welcome/`](Part-0-Welcome/)
Course orientation — goals, role of a forensic analyst, what the course covers.

### [`Part-1-Jumpstart/`](Part-1-Jumpstart/)
DFIR fundamentals: the forensic process, incident response lifecycle, attack lifecycle, data acquisition options, forensic workstation setup, and an introduction to FTK.

### [`Part-2-Elevate/`](Part-2-Elevate/)
The core of this repository — a full, hands-on investigation of a single incident (Alice's compromised workstation, `Client2.BCS.local`), carried across every major evidence source:

- [`01-security-operations/`](Part-2-Elevate/01-security-operations/) — SOC fundamentals and the initial PCAP-based reconstruction of the compromise
- [`02-incident-response-data-collection/`](Part-2-Elevate/02-incident-response-data-collection/) — Splunk SIEM correlation, Velociraptor/EDR exploration, offline collection techniques
- [`03-applied-forensic-analysis/`](Part-2-Elevate/03-applied-forensic-analysis/) — memory, disk, and timeline forensics on the raw evidence itself

Each lab has its own self-contained `README.md` — commands explained at the flag level, evidence embedded inline, and a "Detection & Mitigation" section reframing findings from a blue team perspective.

### [`lab-setup/`](Part-2-Elevate/lab-setup/)
Vagrant/libvirt automation used to provision the lab environment (Splunk, Sysmon, attack replay scripts) locally.

## The Case

Every lab in `Part-2-Elevate/` investigates the same incident, approached from a different evidence source each time. The full attack chain, once every piece was in place:

1. **Delivery** — a Firefox download stager retrieved a payload from `http://w1ndowsupdate.com:8080/update.exe.hta` (DNS typosquatting on "windowsupdate").
2. **Execution** — `update.exe.hta` executed, spawning a first PowerShell-based C2 agent.
3. **C2 agent 1** — a PowerShell process communicating with `3.140.33.120` on port 9001.
4. **Persistence** — a registry `Run` key maintained contact with the C2 across reboots/logons.
5. **Privilege escalation** — an environment-variable-based script elevated the session, spawning a second, higher-privileged agent.
6. **C2 agent 2** — a second PowerShell process, this one running with admin rights, communicating over port 9003.
7. **Reconnaissance** — standard discovery commands (`whoami`, filesystem navigation, DNS queries).
8. **Process injection attempts** — observed, but unsuccessful.
9. **Staging** — `C:\Temp` created, `Alice\Documents` compressed into `C:\Temp\1.zip`.
10. **Exfiltration** — `1.zip` uploaded via the second C2 agent, then deleted locally.

Total data exfiltrated was small (~4 MB), but the chain covers the three pillars that matter most in a real incident: **initial access and system compromise, persistence, and exfiltration** — a compact but complete demonstration of what an attacker does once inside, and where each stage leaves evidence.

Full narrative writeup: [`Scenario-Reveal.md`](Scenario-Reveal.md)

Cross-referenced against independent evidence sources across this project:
- Delivery, C2 IP, and initial PowerShell payload → confirmed via [PCAP analysis](Part-2-Elevate/01-security-operations/lab-pcap-analysis/README.md) and [Splunk](Part-2-Elevate/02-incident-response-data-collection/lab-splunk_SIEM-analysis/README.md)
- Registry persistence and the second (port 9003) listener → confirmed live in [memory](Part-2-Elevate/03-applied-forensic-analysis/lab-memory-analysis/README.md)
- Host identity and disabled AV/Defender protections → confirmed via [disk/registry triage](Part-2-Elevate/03-applied-forensic-analysis/lab-disk-analysis/README.md)

## Documentation Principles

- One `README.md` per lab, fully self-contained — no dependency on other labs to be understood.
- `screenshots/` for course-material captures; `evidences/` reserved strictly for forensic investigation artifacts.
- Every command explained at the flag level, not just reproduced.
- A "Detection & Mitigation" section in every investigation writeup, reframing offensive findings from a blue team perspective.
- Negative results and blockers are documented, not hidden — see the disk and timeline analysis labs for two honest examples of work paused on tooling issues rather than silently omitted.

## Resources

Course tools, cheat sheets, and case file references: [`Part-2-Elevate/03-applied-forensic-analysis/RESOURCES.md`](Part-2-Elevate/03-applied-forensic-analysis/RESOURCES.md)
