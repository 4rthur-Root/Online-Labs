# Alert 8

- id: 6359

- alert Rule: Suspicious archive utility execution on workstation

- Severity: <span style="color: orange;">High</span>   

- Type: Collection

- Date: Oct 26rd 2026 at 05:32

Description:

This detection fires when an archive utility is executed on a workstation to compress the contents of a directory that the interactive user does not normally package. Bulk compression is how collected data is prepared before it is moved off a host, but backup and diagnostic jobs produce the same telemetry, including under automated non-interactive parents, so parent interactivity alone does not separate them. The analyst must establish what was compressed, where the archive was written, which process launched the utility, and what that same process did on the network afterwards.

CommandLine:

"C:\Program Files\7-Zip\7z.exe" a -mx=1 C:\Windows\Temp\nx_build_beta.7z C:\Dev\NeuralNexus\Build\*

Company:

Igor Pavlov

CurrentDirectory:

C:\Windows\System32\

Description:

7-Zip Console

EventCode:

1

EventType:

4

FileVersion:

24.09

Hashes:

MD5=B6D5860F368B28CAA9DD14A51666A5CD,SHA256=E2CA3EC168AE9C0B4115CD4FE220145EA9B2DC4B6FC79D765E91F415B34D00DE,IMPHASH=C9F19638C1640C54CAB9BD55C830AAED

Image:

C:\Program Files\7-Zip\7z.exe

IntegrityLevel:

System

LogName:

Microsoft-Windows-Sysmon/Operational

LogonGuid:

{3af46175-ee50-6a8e-e703-000000000000}

LogonId:

0x3E7

OpCode:

Info

OriginalFileName:

7z.exe

ParentCommandLine:

powershell.exe -NoP -NonI -W Hidden -ExecutionPolicy Bypass -File C:\Windows\Temp\svchost_update.ps1

ParentImage:

C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

ParentProcessGuid:

{3af46175-3bfc-6a90-a41c-000000001100}

ParentProcessId:

14264

ParentUser:

NT AUTHORITY\SYSTEM

ProcessGuid:

{3af46175-3cec-6a90-e61c-000000001100}

ProcessId:

9104

Product:

7-Zip

Sid:

S-1-5-18

SidType:

0

SourceName:

Microsoft-Windows-Sysmon

TaskCategory:

Process Create (rule: ProcessCreate)

TerminalSessionId:

0

Type:

Information

User:

[ "NOT_TRANSLATED", "NT AUTHORITY\\SYSTEM" ]

category:

Process Create (rule: ProcessCreate)

event_id:

43451

host:

THM-SREYES.tryhatmestudios.thm

timestamp:

10/26/2026 05:30:24.567

datasource:

WinEventLog:Microsoft-Windows-Sysmon/Operational

```Time of activity: Oct 26th 2026 at 05:32

List of Affected Entities: HM-MSMITH.tryhatmestudios.thm host

Reason for Classifying as True Positive: the malicious script is using 7z maybe to exfiltrate stolen data to a remote server .

Reason for Escalating the Alert: A high level user is using 7z to zip something and send

Recommended Remediation Actions: investigate what was zipped and whether it was sent or not and to who ?

List of Attack Indicators: svchost_update.exe; 7zip.exe , AUTHORITY/SYSTEM```

wAS I WRONG FOR THE PREVIOUS ONE ?