# Alert 6360 — Suspicious outbound connection following archive creation

- **Disposition:** True positive / escalate as likely command-and-control activity; confirm whether any archive data was transferred.
- **Severity / type:** Critical / Exfiltration
- **Host / user:** `THM-SREYES.tryhatmestudios.thm` / `NT AUTHORITY\SYSTEM`
- **Event time:** 2026-10-26 15:11:41.384

**Evidence:** Sysmon Event ID 3; PowerShell on `10.60.10.20` connects to `45.147.230.131:8067` over TCP. Its process GUID matches the parent PowerShell process GUID recorded for 7-Zip in Alert 6359. The destination is also reported in Alert 6354.

## My initial assessment

I identified the destination as a previously reported malicious IP and classified the alert as a true positive requiring escalation. My draft said there was a “high volume” of traffic, but the supplied event contains no byte counts or connection totals to support that claim. I also used the wrong host label in the report.

## Review and corrections

The matching process GUID links this network event to the PowerShell process that launched 7-Zip, which is materially stronger evidence than simple time proximity. It supports the conclusion that the same suspicious process both staged the archive and connected to the known destination.

There is a substantial timestamp gap: 7-Zip is recorded at 05:30:24, while this connection is recorded at 15:11:41. Confirm clock/timezone normalization, process lifetime, and the alert's aggregation window. The network-connect event does not include byte counts, request contents, or proof that `nx_build_beta.7z` was sent. Report probable C2/possible exfiltration, not confirmed exfiltration, until traffic or destination-side evidence verifies transfer.

The alert summary itself is dated 2026-10-23 05:30, while the raw event is dated 2026-10-26 15:11:41.384. Resolve both the alert-to-event discrepancy and the ten-hour gap to Alert 6359 before asserting sequence or duration.

## Case note

> **Disposition:** True positive; escalate as part of the confirmed compromise. The shared process GUID and known destination support malicious network activity; the actual transfer of archive contents remains unverified.
>
> **Entities / indicators:** `THM-SREYES.tryhatmestudios.thm`, `10.60.10.20`, SYSTEM, PowerShell PID 14264, `45.147.230.131:8067/TCP`, `7z.exe`, `C:\Windows\Temp\nx_build_beta.7z`.
>
> **Next steps:** Correlate the process GUID with all Sysmon and PowerShell events; verify time normalization and connection duration/volume; examine DNS, proxy, firewall, and packet data; determine whether the archive was opened or transmitted; hunt for the destination across the environment and preserve the archive and script.

## MITRE ATT&CK

| Technique | ID | Confidence |
|---|---|---|
| Web Protocols | [T1071.001](https://attack.mitre.org/techniques/T1071/001/) | Likely if the connection is confirmed as command and control; TCP port 8067 alone does not identify the application protocol. |
| Exfiltration Over C2 Channel | [T1041](https://attack.mitre.org/techniques/T1041/) | Possible, not confirmed. Requires evidence that collected data was transmitted over the command-and-control channel. |

## Reporting correction

Use the actual host, destination, and event time. Remove the unsupported “high volume” claim unless flow or proxy records confirm it. Separate confirmed process lineage from the still-unconfirmed transfer of archive contents.
