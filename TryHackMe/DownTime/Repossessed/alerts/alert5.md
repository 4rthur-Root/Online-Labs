# Alert 5

- id: 6356

- alert Rule: Rapid domain and host enumeration from Non-administrative host

- Severity: <span style="color: orange;">High</span>   

- Type: Discovery

- Date: Oct 23rd 2026 at 02:05


escription:

This detection fires when a workstation that is not used for directory administration runs several domain and host enumeration commands in quick succession. The burst is aggregated, so a single alert represents the sequence rather than one execution, and the analyst is expected to recover the full set of commands issued. Administrators legitimately issue these queries, but rarely as a burst from a standard user endpoint, and the same sequence is a routine early step for a threat actor mapping an environment after gaining execution. The analyst must identify the account and the parent process behind the commands, what information they returned, and what activity followed them.

CommandLine:

"C:\Windows\system32\net.exe" user /domain

Company:

Microsoft Corporation

CurrentDirectory:

C:\Windows\system32\

Description:

Net Command

EventCode:

1

EventType:

4

FileVersion:

10.0.22621.1 (WinBuild.160101.0800)

Hashes:

MD5=28C604BE558D42A7A999B67219BCE2DB,SHA256=43C411FC62EEE2A3F04B02C2785DAF37D5B26A36171D037855667D8F32C3D142,IMPHASH=6C829877160814FC33B041AB46ABAC59

Image:

C:\Windows\SysWOW64\net.exe

IntegrityLevel:

Medium

LogName:

Microsoft-Windows-Sysmon/Operational

LogonGuid:

{3af46175-c39c-6a8f-e030-9c0000000000}

LogonId:

0x9C30E0

OpCode:

Info

OriginalFileName:

net.exe

ParentCommandLine:

"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -NoP -W Hidden -ExecutionPolicy Bypass -File "C:\Users\MC0CD~1.SMI\AppData\Local\Temp\svchost_update.ps1"

ParentImage:

C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe

ParentProcessGuid:

{3af46175-390a-6a90-991d-000000001200}

ParentProcessId:

9356

ParentUser:

TRYHATME\m.smith

ProcessGuid:

{3af46175-3a39-6a90-d91d-000000001200}

ProcessId:

9744

Product:

Microsoft® Windows® Operating System

Sid:

S-1-5-18

SidType:

0

SourceName:

Microsoft-Windows-Sysmon

TaskCategory:

Process Create (rule: ProcessCreate)

TerminalSessionId:

4

Type:

Information

User:

[ "NOT_TRANSLATED", "TRYHATME\\m.smith" ]

category:

Process Create (rule: ProcessCreate)

event_id:

46239

host:

THM-MSMITH.tryhatmestudios.thm

timestamp:

10/26/2026 02:08:42.547

datasource:

WinEventLog:Microsoft-Windows-Sysmon/Operational


Same host and same script running this command `"C:\Windows\system32\net.exe" user /domain`. At this point due to the context it is still True positive

The primary MITRE ATT&CK tactic for this activity is Discovery (TA0007).

Specific techniques and detection strategies include:

Account Discovery: Domain Account (T1087.002): Adversaries use commands like net user /domain, PowerShell cmdlets (Get-ADUser), or LDAP queries to list domain users. 
Permission Groups Discovery: Domain Groups (T1069.002): Adversaries identify domain administrative groups (e.g., "Domain Admins") using tools like net group or AdFind. 
Detection Strategy DET0129: This strategy specifically targets Domain Account Enumeration Across Platforms, focusing on detecting enumeration commands (such as net.exe, PowerShell, WMI, or LDAP) executed from non-domain controllers or non-admin endpoints

```
Time of activity: Oct 26th 2026 at 05:23

List of Affected Entities: HM-MSMITH.tryhatmestudios.thm host

Reason for Classifying as True Positive: The same suspicious ps1 file starts enumeration . 

Reason for Escalating the Alert: the non administrator host running is suspicious  as suggested by Mitre tactic Discovery (TA0007)

Recommended Remediation Actions: See the content of svchost_update.ps1 

List of Attack Indicators: Suspicious file downloaded enumerating from a non administrative host 
```