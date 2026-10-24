# Alert 2

- id: 6360

- alert Rule: Suspicious external Connection following Archive creation 

- Severity: <span style="color: red;">Critical</span>   

- Type: Exfiltration

- Date: Oct 23rd 2026 at 02:59

| Field | Value |
|-------|-------|
| Description | This detection fires when a host transmits data to an external destination around the time an archive file is created locally. Connections to the same destination are grouped, so an alert may represent several connections rather than one, and the analyst is expected to establish how many occurred and over what interval. Archive creation followed by an outbound transfer matches the pattern used to move collected data out of an environment, but it also matches routine backup, telemetry, and vendor integration traffic. The analyst must establish what the archive contained, which process opened the connection, and whether the destination is a known and approved service before reaching a verdict. |
| DestinationIp | 45.147.230.131 |
| DestinationPort | 8067 |
| EventCode | 3 |
| EventType | 4 |
| Image | `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe` |
| Initiated | true |
| LogName | Microsoft-Windows-Sysmon/Operational |
| OpCode | Info |
| ProcessGuid | {3af46175-3bfc-6a90-a41c-000000001100} |
| ProcessId | 14264 |
| Protocol | tcp |
| Sid | S-1-5-18 |
| SidType | 0 |
| SourceIp | 10.60.10.20 |
| SourceName | Microsoft-Windows-Sysmon |
| SourcePort | 52624 |
| TaskCategory | Network connection detected (rule: NetworkConnect) |
| Type | Information |
| User | [ "NOT_TRANSLATED", "NT AUTHORITY\\SYSTEM" ] |
| category | Network connection detected (rule: NetworkConnect) |
| event_id | 43456 |
| host | THM-SREYES.tryhatmestudios.thm |
| timestamp | 10/23/2026 02:57:42.962 |
| datasource | WinEventLog:Microsoft-Windows-Sysmon/Operational |