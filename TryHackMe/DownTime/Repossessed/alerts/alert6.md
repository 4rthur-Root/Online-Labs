# Alert 6

- id: 6357

- alert Rule: Suspicious remote logon and service creation 

- Severity: <span style="color: red;">Critical</span>   

- Type: Lateral Movement 

- Date: Oct 23rd 2026 at 05:25


Description:

This detection fires when a new Windows service is registered on a host and its configured binary path does not resolve to a recognised service executable. Service creation is a durable execution mechanism that runs with high privilege, and software deployment tooling uses it legitimately. The analyst must inspect what the service was configured to run and how that command line was constructed, determine which account created the service and whether the registering session originated over the network or at the console, and establish whether the service started.

Account_Domain:

TRYHATME

Account_Name:

svc-mktshare

EventCode:

4697

EventType:

0

LogName:

Security

Logon_ID:

0x24F6572

Message:

A service was installed in the system. Subject: Security ID: S-1-5-21-1966530601-3185510712-10604624-1126 Account Name: svc-mktshare Account Domain: TRYHATME Logon ID: 0x24F6572 Service Information: Service Name: SvcUpdate Service File Name: cmd.exe /c start /b powershell.exe -NoP -NonI -W Hidden -ExecutionPolicy Bypass -File C:\Windows\Temp\svchost_update.ps1 Service Type: 0x10 Service Start Type: 3 Service Account: LocalSystem

OpCode:

Info

Security_ID:

S-1-5-21-1966530601-3185510712-10604624-1126

Service_Account:

LocalSystem

Service_File_Name:

cmd.exe /c start /b powershell.exe -NoP -NonI -W Hidden -ExecutionPolicy Bypass -File C:\Windows\Temp\svchost_update.ps1

Service_Name:

SvcUpdate

Service_Start_Type:

3

Service_Type:

0x10

SourceName:

Microsoft Windows security auditing.

Subject_Account_Domain:

TRYHATME

Subject_Account_Name:

svc-mktshare

Subject_Logon_ID:

0x24F6572

Subject_Security_ID:

S-1-5-21-1966530601-3185510712-10604624-1126

TaskCategory:

Security System Extension

Type:

Information

body:

A service was installed in the system. Subject: Security ID: S-1-5-21-1966530601-3185510712-10604624-1126 Account Name: svc-mktshare Account Domain: TRYHATME Logon ID: 0x24F6572 Service Information: Service Name: SvcUpdate Service File Name: cmd.exe /c start /b powershell.exe -NoP -NonI -W Hidden -ExecutionPolicy Bypass -File C:\Windows\Temp\svchost_update.ps1 Service Type: 0x10 Service Start Type: 3 Service Account: LocalSystem

category:

Security System Extension

dest_nt_domain:

TRYHATME

dest_nt_host:

THM-SREYES.tryhatmestudios.thm

event_id:

7589

host:

THM-SREYES.tryhatmestudios.thm

member_dn:

svc-mktshare

member_id:

S-1-5-21-1966530601-3185510712-10604624-1126

service_name:

SvcUpdate

signature:

A service was installed in the system

src_nt_domain:

S-1-5-21-1966530601-3185510712-10604624-1126

src_subject_security_id:

S-1-5-21-1966530601-3185510712-10604624-1126

start_mode:

manual

user:

svc-mktshare

timestamp:

10/26/2026 05:23:33.567

datasource:

WinEventLog:Security


The MITRE ATT&CK tactic for lateral movement is identified as TA0008.
The downloaded ps1 file is now creating 

The core  command executes the PowerShell script   with hidden window and bypassed execution policy settings, launched silently from Command Prompt again

Security Assessment:

High Suspicion Indicator: This specific command line structure (-NoP -NonI -W Hidden -ExecutionPolicy Bypass) is a commonly observed pattern in malware, cryptominers, and ransomware execution. Attackers use it to run malicious payloads without user interaction or visibility.
Location Risk: Executing scripts from %TEMP% (C:\Windows\Temp) is a known technique for living-off-the-land or dropped-malware attacks, as this directory is writable by standard users.
Execution Policy Bypass: The -ExecutionPolicy Bypass flag disables PowerShell’s default safety checks, allowing unsigned and potentially malicious scripts to run. 
Hidden Window: The -W Hidden (or -WindowStyle Hidden) flag prevents the PowerShell window from appearing, aiding stealth.


Here true positive 

Here's a breakdown of the **attack indicators** mapped to that command line:

## MITRE ATT&CK Techniques

| ID | Technique | Indicator in Command |
|---|---|---|
| **T1059.003** | Command and Scripting Interpreter: Windows Command Shell | `cmd.exe /c` as launcher |
| **T1059.001** | Command and Scripting Interpreter: PowerShell | `powershell.exe` execution |
| **T1027.010** | Obfuscated Files or Information: Command Obfuscation | Abbreviated flags (`-NoP`, `-NonI`, `-W`) to shorten the command line and evade signature-based detection |
| **T1059.001** | Execution Policy Bypass | `-ExecutionPolicy Bypass` disables script signing checks |
| **T1070** | Indicator Removal: Hidden Window | `-W Hidden` suppresses the PowerShell console window |
| **T1036** | Masquerading | `svchost_update.ps1` mimics the legitimate `svchost.exe` service host name |
| **T1564.001** | Hide Artifacts | Background execution via `start /b` + hidden window |
| **T1027** | Obfuscated Files or Information | Script dropped in `%TEMP%` with a benign-looking name |

## Specific IoCs (Indicators of Compromise)

| Category | Indicator |
|---|---|
| **Process** | `powershell.exe` spawned by `cmd.exe` (not `explorer.exe`) |
| **Command Line** | `powershell.exe -NoP -NonI -W Hidden -ExecutionPolicy Bypass -File <path>` |
| **File Path** | `C:\Windows\Temp\*.ps1` — script in a world-writable temp directory |
| **File Name** | `svchost_update.ps1` — masquerading as a Windows system process |
| **Flags** | `-NoProfile` (no profile load), `-NonInteractive` (no user input), `-W Hidden` (no visible window) |
| **Execution Policy** | `-ExecutionPolicy Bypass` — overrides system-level script restrictions |
| **Parent Process** | `cmd.exe` with `/c` (run and exit) + `start /b` (background) — classic silent-launch chain |

## Detection Queries (Sysmon EID 1)

```
Image = "powershell.exe"
AND CommandLine CONTAINS "-ExecutionPolicy Bypass"
AND CommandLine CONTAINS "-W Hidden"
AND CommandLine CONTAINS "-File C:\Windows\Temp\"
AND ParentImage = "cmd.exe"
```

## Key Red Flags (Combined)

Any **single** flag can be legitimate. The **combination** is the real indicator:

1. **Temp directory + .ps1** → dropped payload
2. **Hidden window + NonInteractive** → no user awareness
3. **ExecutionPolicy Bypass** → unsigned script execution
4. **svchost_** prefix → masquerading to blend into process lists
5. **cmd.exe → powershell.exe** chain → common malware execution pattern

This exact pattern is documented by **APT28**, **APT29**, **APT32**, and **APT41** in MITRE ATT&CK group mappings.

```
Time of activity: Oct 26th 2026 at 05:26



List of Affected Entities: HM-MSMITH.tryhatmestudios.thm host



Reason for Classifying as True Positive: The suspicious script is installing a service 



Reason for Escalating the Alert: The content of the file and damages done on the host must be inverstigated



Recommended Remediation Actions: 

Investigate the File
Check for Persistence
Scan for Malware:
Review Process Tree: 


List of Attack Indicators: powershell.exe spawned by cmd.exe

powershell.exe -NoP -NonI -W Hidden -ExecutionPolicy Bypass -File &lt;path>

cmd.exe with /c + start /b ( — classic silent-launch chain


```