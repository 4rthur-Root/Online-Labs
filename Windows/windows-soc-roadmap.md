# 🪟 Windows SOC Analyst — Learning Roadmap

**Goal:** Build solid fundamentals in Windows, Active Directory, and log analysis for a SOC / Blue Team role, addressing the Windows internals gap identified after the Blue Cape Security DFIR course.

**Method:** Sequential units, not fixed weeks. Each unit has a clear objective, defined resources, hands-on lab work, and a concrete proof of completion. Units run in parallel with other ongoing work, so pace is adaptive — an estimated duration is given for planning purposes only, not as a deadline.

**Location in repo:** `Windows/` at the root of `Online-Labs`, one subfolder per unit, each with a self-contained `README.md` following existing repo conventions (flag-level command explanations, inline evidence screenshots, `evidences/` reserved for forensic artifacts, `screenshots/` for course/platform material, mandatory Detection & Mitigation section on offense-oriented units).

**Scope note:** The final synthesis project (originally "Week 8") is **not** part of this roadmap or of `Online-Labs`. It is self-directed, not tied to any platform, and will live in its own dedicated repository.

---

## 🧪 Lab Environment (Unit 00 — prerequisite for everything else)

### Host & hypervisor

Reuses the existing setup from the Blue Cape Security lab:

- **Host:** Fedora
- **Hypervisor:** libvirt/KVM
- **Provisioning:** Vagrant is used where convenient (Linux boxes), but Windows VMs are provisioned directly through libvirt/`virt-manager`/`virsh`, since Vagrant's Windows box support is inconsistent and adds friction for domain-joined machines.

### Virtual machines required

| VM | Role | OS Source | vCPU | RAM | Disk |
|---|---|---|---|---|---|
| **DC01** | Primary Domain Controller + DNS | Windows Server 2022 Evaluation (180-day, Microsoft Evaluation Center) | 2 | 4–8 GB | 60 GB |
| **WIN10-CLIENT** | Domain-joined workstation | Windows 10/11 Enterprise Evaluation (180-day, Microsoft Evaluation Center) | 2 | 4 GB | 60 GB |
| **DC02** *(optional, Unit 04a only)* | Secondary Domain Controller — replication testing | Same as DC01 | 2 | 4 GB | 60 GB |

**Sizing note:** these are minimums for smooth operation. If the Fedora host has 16 GB RAM or less, DC01 + WIN10-CLIENT running simultaneously is manageable; adding DC02 concurrently may require shutting down other VMs (e.g. the Blue Cape Debian/Kali boxes) first. Document actual host resource usage in the Unit 00 README — this is exactly the kind of blocker worth being transparent about if it comes up.

### Networking

- A dedicated **libvirt network** (NAT or isolated, host's choice) where DC01, DC02, and WIN10-CLIENT can all reach each other.
- DC01 must be the **authoritative DNS server** for this network — domain join fails silently or with cryptic errors if client DNS doesn't point to the DC.
- Static IPs recommended for DC01/DC02 (DHCP-assigned addresses complicate DNS records and Kerberos SPNs later).

### Setup sequence

1. Download both evaluation ISOs from the Microsoft Evaluation Center.
2. Create DC01 in `virt-manager`, install Windows Server 2022.
3. Promote DC01 to Domain Controller:
   ```powershell
   Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
   Install-ADDSForest -DomainName "lab.local"
   ```
4. Create WIN10-CLIENT, install Windows 10/11, set DNS to DC01's IP.
5. Join WIN10-CLIENT to the domain:
   ```powershell
   Add-Computer -DomainName "lab.local" -Restart
   ```
6. Verify the setup:
   ```powershell
   Get-ADDomain
   nltest /dsgetdc:lab.local
   ```
   Confirm ping and name resolution both directions between DC01 and WIN10-CLIENT.
7. *(Unit 04a only)* Stand up DC02, promote as an additional DC in the same domain, confirm replication with `repadmin /showrepl`.

### Proof of completion

- Screenshot: `Get-ADDomain` output on DC01
- Screenshot: WIN10-CLIENT showing "lab.local" under System Properties (domain-joined)
- Screenshot: successful `nltest /dsgetdc:lab.local` from the client

---

## 📚 Units

### Unit 01 — Windows Fundamentals

| | |
|---|---|
| **Est. effort** | ~5h |
| **Objective** | Navigate Windows confidently: desktop, file system (NTFS), user accounts, UAC, Task Manager, Registry, Control Panel/Settings, Event Viewer basics |
| **Resources** | [Windows Fundamentals 1](https://tryhackme.com/room/windowsfundamentals1xbx) (THM, free) · [Windows Fundamentals 2](https://tryhackme.com/room/windowsfundamentals2x0x) (THM, free) |
| **Hands-on** | Complete both rooms · On WIN10-CLIENT: create a standard user + an administrator, edit a local GPO (`gpedit.msc`), explore the registry (`regedit`) and locate an autorun key, start/stop a service (`services.msc`) |
| **Proof of completion** | 2 THM badges (WF1, WF2) · Screenshots: new user creation, GPO change, modified registry key |

> Windows Fundamentals 3 (Defender, BitLocker, Windows Update) is a **TryHackMe Premium room** and is dropped from this roadmap — its content is secondary to the SOC/DFIR track. Revisit later if useful.

---

### Unit 02 — Active Directory Basics

| | |
|---|---|
| **Est. effort** | ~6h |
| **Objective** | Understand domains, OUs, forests/trees, trusts, and core AD object attributes |
| **Resources** | [Describe Active Directory Domain Services](https://learn.microsoft.com/en-us/training/paths/security-operations-analyst/) (Microsoft Learn, free) |
| **Hands-on** | On DC01: create an OU, create a user inside it, explore the user object's attributes (`sAMAccountName`, `userPrincipalName`, etc.) via ADUC and PowerShell |
| **Proof of completion** | Microsoft Learn trophy · Screenshots: OU tree in ADUC, user object properties |

> The TryHackMe "Active Directory Basics" room is **Premium** (only the intro task is free) and is replaced entirely by Microsoft Learn, which covers the same ground without a paywall.

**Documentation to produce:** forest/domain/OU diagram, table of key user attributes, useful AD PowerShell commands (`Get-ADUser`, `Get-ADGroup`).

---

### Unit 03 — Kerberos & NTLM

| | |
|---|---|
| **Est. effort** | ~7h |
| **Objective** | Understand both authentication protocols, how they differ, and their known weaknesses |
| **Resources** | MS Learn "Understand authentication in AD" (part of the SC-200 path above) · [Kerberos explained (video)](https://www.youtube.com/watch?v=5N242XcKAsM) · [NTLM vs Kerberos](https://activedirectorypro.com/kerberos-vs-ntlm/) |
| **Hands-on** | On WIN10-CLIENT: inspect a Kerberos ticket with `klist`, observe Security log authentication events, identify the auth package (Kerberos vs NTLM) in Event ID 4624 |
| **Proof of completion** | Screenshot: Event 4624 showing the authentication package · Kerberos flow diagram (AS-REQ, AS-REP, TGS-REQ, TGS-REP) |

**Documentation to produce:** Kerberos flow diagram, Kerberos vs NTLM comparison table, list of known attacks (Pass-the-Ticket, Pass-the-Hash, Golden Ticket) — detection angle for each.

---

### Unit 04a — AD Replication & Trusts

| | |
|---|---|
| **Est. effort** | ~4h |
| **Objective** | Understand multi-master replication between domain controllers and how trusts work between domains |
| **Resources** | [AD Replication concepts](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/active-directory-replication-concepts) (Microsoft Learn, free) |
| **Hands-on** | Requires DC02 (see Unit 00). Confirm replication with `repadmin /showrepl`, force replication with `repadmin /syncall`, observe replication-related Event IDs |
| **Proof of completion** | Screenshot: `repadmin /showrepl` output showing successful replication between DC01/DC02 · Replication flow diagram |

**Documentation to produce:** explanation of multi-master replication, trust types (one-way, two-way, transitive), replication diagram.

---

### Unit 04b — DCSync (Attack & Detection)

| | |
|---|---|
| **Est. effort** | ~4h |
| **Objective** | Understand and observe the DCSync attack technique, and how to detect it |
| **Resources** | [Attacktive Directory](https://tryhackme.com/room/attacktivedirectory) (THM, **free**, full 8 tasks including DCSync via `secretsdump.py`) |
| **Hands-on** | Complete Attacktive Directory (enumeration → Kerberos abuse → DCSync). In the isolated lab **only**, reproduce the equivalent against DC01 and capture the resulting Event ID 4662 |
| **Proof of completion** | THM room flags submitted · Screenshot: Event 4662 (AD object access) generated by the DCSync attempt |

**Documentation to produce:** what DCSync is and why the `Replicating Directory Changes` permission matters, Event IDs to monitor (4662, 4768, 4776), **mandatory Detection & Mitigation section** — this unit is attack-oriented by nature, so the blue-team reframing matters most here.

---

### Unit 05 — Windows Event Logs Fundamentals

| | |
|---|---|
| **Est. effort** | ~5h |
| **Objective** | Master the critical Event IDs: 4624, 4625, 4688, 4720, 4732, 4648, 1102 |
| **Resources** | [Windows Logging for SOC](https://tryhackme.com/room/windowsloggingforsoc) (THM, free — note the corrected URL slug) · [Ultimate Windows Event IDs list](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/) |
| **Hands-on** | Complete the THM room. On WIN10-CLIENT: log in/out (4624/4625), enable process auditing and launch a process (4688), create a user (4720), add a user to a group (4732), clear the logs (1102) |
| **Proof of completion** | THM badge · Screenshot: Event Viewer filtered to these IDs |

**Documentation to produce:** full Event ID table (number, description, why it matters), one example log per ID, how to enable process-creation auditing via `gpedit.msc`.

---

### Unit 06 — Sysmon & PowerShell Logging

| | |
|---|---|
| **Est. effort** | ~6h |
| **Objective** | Install and configure Sysmon, read its logs, understand PowerShell Script Block Logging (Event 4104) |
| **Resources** | [Sysmon official docs](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) (Microsoft Sysinternals, free) · [Sysmon config — SwiftOnSecurity](https://github.com/SwiftOnSecurity/sysmon-config) |
| **Hands-on** | Install Sysmon on WIN10-CLIENT with the SwiftOnSecurity config. Run a PowerShell command and capture Event 4104. Trigger a suspicious-looking process (e.g. `certutil -urlcache`) and observe Sysmon Event 1. Observe a network connection via Event 3 |
| **Proof of completion** | Screenshots: Sysmon Events 1, 3, 7 · Screenshot: Event 4104 |

> No TryHackMe room used here — the "Sysmon" room is **Premium**. Fully covered via official documentation + hands-on practice on the lab VM, which is arguably closer to real-world onboarding of an unfamiliar tool.

**Documentation to produce:** Sysmon install command, explanation of key event types (1=Process, 3=Network, 7=Image Loaded), how to enable PowerShell script block logging, one example KQL/SPL query to hunt suspicious PowerShell.

---

### Unit 07a — BloodHound (Collection & Mapping)

| | |
|---|---|
| **Est. effort** | ~5h |
| **Objective** | Collect AD data with SharpHound and read attack paths in BloodHound |
| **Resources** | [BloodHound Basics — SpecterOps](https://training.specterops.io/) (free course) · [SharpHound / BloodHound](https://github.com/BloodHoundAD/BloodHound) |
| **Hands-on** | Run SharpHound against the lab domain, import into BloodHound, explore the graph structure and relationship types |
| **Proof of completion** | Screenshot: BloodHound graph loaded with lab domain data |

**Documentation to produce:** SharpHound/BloodHound install steps, relationship types (MemberOf, AdminTo, HasSession, etc.), how to read the graph.

---

### Unit 07b — Attack Paths & Delegations

| | |
|---|---|
| **Est. effort** | ~5h |
| **Objective** | Identify realistic attack paths to Domain Admin and dangerous delegations |
| **Resources** | [Attacktive Directory](https://tryhackme.com/room/attacktivedirectory) (THM, free — same room as 04b, different lens) · [John Hammond BloodHound tutorial](https://www.youtube.com/watch?v=Y3qTX0dNg8A) |
| **Hands-on** | Using the BloodHound data from 07a, find the shortest path to Domain Admin in the lab domain. Identify one dangerous delegation (e.g. a user with `GenericAll` on a privileged group) |
| **Proof of completion** | Screenshot: shortest path graph (User → Group → DA) · Screenshot: identified delegation |

**Documentation to produce:** list of the 5 most common AD attack paths, one worked delegation example, **Detection & Mitigation section**.

---

## 📊 Completion Summary

| Unit | Platform | Proof |
|---|---|---|
| 00 | Lab (libvirt/KVM) | DC promoted + client domain-joined |
| 01 | THM | 2 badges (WF1, WF2) |
| 02 | Microsoft Learn | Trophy |
| 03 | Microsoft Learn + lab | Event 4624 captured |
| 04a | Microsoft Learn + lab | Replication confirmed (DC01/DC02) |
| 04b | THM (Attacktive Directory) | Flags + Event 4662 captured |
| 05 | THM | Badge |
| 06 | Sysinternals docs + lab | Events 1/3/7/4104 captured |
| 07a | SpecterOps + lab | BloodHound graph |
| 07b | THM (Attacktive Directory) | Attack path + delegation identified |

---

## 🧰 Tools to Install

| Tool | Purpose | Source |
|---|---|---|
| Sysmon | Advanced endpoint logging | [Sysinternals](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) |
| BloodHound + Neo4j | AD attack path mapping | [GitHub](https://github.com/BloodHoundAD/BloodHound) |
| SharpHound | BloodHound data collector | Bundled with BloodHound / Impacket toolset |
| Process Explorer | Process analysis | [Sysinternals](https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer) |
| Procmon | Process/file/registry activity monitor | [Sysinternals](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) |

## 📎 Cheat Sheet — Core Event IDs

| ID | Meaning |
|---|---|
| 4624 | Successful logon |
| 4625 | Failed logon |
| 4648 | Explicit credential logon |
| 4662 | Operation on an AD object (DCSync indicator) |
| 4688 | Process creation |
| 4720 | User account created |
| 4732 | User added to a security-enabled group |
| 4768 | Kerberos TGT requested |
| 1102 | Audit log cleared |

```powershell
# AD objects
Get-ADUser -Filter * -Properties *
Get-ADGroup -Filter *

# Security log
Get-WinEvent -LogName Security -MaxEvents 10

# Sysmon log
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 10
```

---

## 🎯 Final Validation Criteria

By the end of this roadmap, the following should be true without hesitation:

- [ ] Navigate Windows and AD independently
- [ ] Identify the 9+ core Event IDs on sight
- [ ] Install and configure Sysmon from scratch
- [ ] Read a PowerShell Script Block Logging event (4104)
- [ ] Use BloodHound to find an attack path
- [ ] Explain Kerberos vs NTLM clearly
- [ ] Detect a DCSync attempt from logs
- [ ] Explain AD replication and trust types

The final synthesis project — applying all of this in an original investigation scenario — lives in its own dedicated repository, not in `Online-Labs`.
