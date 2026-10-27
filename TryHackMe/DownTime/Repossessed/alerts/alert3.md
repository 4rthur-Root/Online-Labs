# Alert 6354 — Suspicious outbound connection following document activity

- **Disposition:** True positive / escalate in the context of the confirmed PowerShell intrusion; validate the event chronology.
- **Severity / type:** High / Command and Control
- **Host / user:** `THM-MSMITH.tryhatmestudios.thm` / `TRYHATME\m.smith`
- **Event time:** 2026-10-24 01:07:28.474

**Evidence:** Sysmon Event ID 3; PowerShell on `10.60.10.22` connected to `45.147.230.131:8067` over TCP. The alert identifies this as an outbound connection. The same IP and port appear in the downloader infrastructure described in Alert 6353.

![VirusTotal reputation snapshot for 45.147.230.131](./evidences/virus-total.png)

## My initial assessment

I searched Splunk for the destination IP but did not find useful context, then checked VirusTotal and saw a malicious reputation. I classified the connection as a true positive and recommended investigating the traffic. My report had the wrong destination IP (`5.147.230.131`) and used a date/time that did not match this event.

## Review and corrections

The destination is `45.147.230.131`—not `5.147.230.131`. The VirusTotal screenshot shows 10 of 92 vendors flagging the IP at the time captured. That is supporting threat-intelligence context, not proof by itself. The event timestamp is 2026-10-24 01:07:28.474. This predates the 2026-10-26 PowerShell download event, despite the apparent relationship in the scenario. Do not silently treat the timestamps as one chronological sequence: confirm the room's timezone, event normalization, and whether the supplied records span different scenario dates.

The process, destination, port, and threat-intelligence context make this connection suspicious and worthy of escalation. A VirusTotal verdict is supporting context, not proof by itself. A Sysmon network-connect event establishes a connection attempt/session, not what data was exchanged or whether the connection succeeded.

## Case note

> **Disposition:** True positive in the broader incident context; escalate for investigation. The connection is suspicious, but the event alone does not establish the content or volume of traffic.
>
> **Entities / indicators:** `THM-MSMITH.tryhatmestudios.thm`, `10.60.10.22`, `TRYHATME\m.smith`, PowerShell, `45.147.230.131:8067/TCP`.
>
> **Next steps:** Correlate by process GUID and time with DNS, proxy, firewall, and packet/flow records. Confirm whether the destination resolves to `paylink-cdn.thm`, inspect byte counts and response data, and search for the IP/domain on other endpoints. Preserve the threat-intelligence result with its lookup date and source.

## MITRE ATT&CK

| Technique | ID | Confidence |
|---|---|---|
| Web Protocols | [T1071.001](https://attack.mitre.org/techniques/T1071/001/) | Possible only if follow-up confirms this traffic was used for command and control. The network event by itself does not prove that purpose. |

## Reporting correction

Replace the incorrect IP and time in the original report with the event values above. Phrase the finding as an outbound PowerShell connection to a threat-reported destination; avoid claiming successful data transfer without traffic evidence.
