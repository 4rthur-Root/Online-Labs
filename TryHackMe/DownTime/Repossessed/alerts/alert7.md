# Alert 7

- id: 6358

- alert Rule: Suspicious External connection following archive creation 

- Severity: <span style="color: red;">Critical</span>   

- Type: Exfiltration

- Date: Oct 23rd 2026 at 05:30

Description:

This detection fires when a host transmits data to an external destination around the time an archive file is created locally. Connections to the same destination are grouped, so an alert may represent several connections rather than one, and the analyst is expected to establish how many occurred and over what interval. Archive creation followed by an outbound transfer matches the pattern used to move collected data out of an environment, but it also matches routine backup, telemetry, and vendor integration traffic. The analyst must establish what the archive contained, which process opened the connection, and whether the destination is a known and approved service before reaching a verdict.

DestinationIp:

104.18.32.47

DestinationPort:

443

EventCode:

3

EventType:

4

Image:

C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

Initiated:

true

LogName:

Microsoft-Windows-Sysmon/Operational

OpCode:

Info

ProcessGuid:

{3af46175-3c7c-6a90-d11c-000000001100}

ProcessId:

12408

Protocol:

tcp

Sid:

S-1-5-18

SidType:

0

SourceIp:

10.60.10.20

SourceName:

Microsoft-Windows-Sysmon

SourcePort:

56222

TaskCategory:

Network connection detected (rule: NetworkConnect)

Type:

Information

User:

[ "NOT_TRANSLATED", "NT AUTHORITY\\SYSTEM" ]

category:

Network connection detected (rule: NetworkConnect)

event_id:

43438

host:

THM-SREYES.tryhatmestudios.thm

timestamp:

10/26/2026 05:28:33.567

datasource:

WinEventLog:Microsoft-Windows-Sysmon/Operational


things are taking shape it is now extracting data to a cloudflare  IP 104.18.32.47 marked clean by virustotal though . but wait first of all it is not the same ip 20 not 22 , not same scipt or user , this might be just noise or legitimate so , false positive 

```
ime of activity: Oct 26th 2026 at 05:32


List of Affected Entities: HM-MSMITH.tryhatmestudios.thm host


Reason for Classifying as True Positive: the malicious script is using 7z maybe to exfiltrate stolen data to a remote server .


Reason for Escalating the Alert: A high level user is using 7z to zip something and send


Recommended Remediation Actions: investigate what was zipped and whether it was sent or not and to who ?


List of Attack Indicators: svchost_update.exe; 7zip.exe , AUTHORITY/SYSTEM
```