# Alert 6358 — Suspicious outbound connection around archive activity

- **Disposition:** Suspicious; escalate within the confirmed host compromise, but do not label this connection as exfiltration without further evidence.
- **Severity / type:** Critical / Exfiltration (as labelled by the alert)
- **Host / user:** `THM-SREYES.tryhatmestudios.thm` / `NT AUTHORITY\SYSTEM`
- **Event time:** 2026-10-26 05:28:33.567

**Evidence:** Sysmon Event ID 3; PowerShell on `10.60.10.20` connects to `104.18.32.47:443` over TCP. Its process GUID differs from the PowerShell process that launched 7-Zip in Alert 6359. The connection precedes the 7-Zip process event at 05:30:24.

## My initial assessment

I initially leaned toward a false positive because the destination appeared to be a Cloudflare address, the IP had a clean VirusTotal result, and I thought the source differed from the other activity. My draft report then contradicted that conclusion by calling it a true positive and asserting that 7-Zip was used to exfiltrate data.

## Review and corrections

The host name in this event is the same compromised `THM-SREYES` host as Alerts 6357–6360. The private source address `10.60.10.20` is not evidence that the event belongs to a different case. A public Cloudflare IP can front many services; a clean reputation result does not establish that the specific connection was benign.

This connection is not directly tied to the later 7-Zip process: the process GUIDs differ, and the connection event occurs before the archive-creation event. Treat it as suspicious outbound PowerShell activity on a compromised host, not as proof that the archive was uploaded. Correlate the domain, TLS metadata, process command line, DNS, proxy/firewall logs, and traffic volume before reaching a more specific conclusion.

The alert summary is dated 2026-10-23, while the raw network event is dated 2026-10-26 05:28:33.567. Resolve that discrepancy as part of timeline validation.

## Case note

> **Disposition:** Escalate as suspicious, potentially incident-related activity. The available record does not prove archive exfiltration or establish the purpose of this particular connection.
>
> **Entities / indicators:** `THM-SREYES.tryhatmestudios.thm`, `10.60.10.20`, PowerShell running as SYSTEM, `104.18.32.47:443/TCP`.
>
> **Next steps:** Resolve the destination at the event time; review SNI, DNS, proxy and firewall records; inspect the process command line and process tree; check for bytes sent/received; compare with approved application traffic. Do not block a shared Cloudflare address without identifying the hosted service and assessing collateral impact.

## MITRE ATT&CK

No technique is confirmed by the network event alone. Web-protocol command and control ([T1071.001](https://attack.mitre.org/techniques/T1071/001/)) is a hypothesis only if the connection's purpose is verified.

## Reporting correction

Keep the initial uncertainty visible, then resolve it with process and timeline evidence. Do not write “7-Zip exfiltrated the archive” here: this event has a different process GUID and predates the archive event.
