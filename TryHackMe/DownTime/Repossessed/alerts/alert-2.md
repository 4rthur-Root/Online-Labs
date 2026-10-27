# Alert 6353 — Suspicious child process spawned

- **Disposition:** True positive; escalate as part of the document-led intrusion chain.
- **Severity / type:** High / Execution
- **Host / user:** `THM-MSMITH.tryhatmestudios.thm` / `TRYHATME\m.smith`
- **Event time:** 2026-10-26 02:03:38.547

**Evidence:** Sysmon Event ID 1; `WINWORD.EXE` launched 32-bit PowerShell with `-NoP -W Hidden -Enc`. The decoded command downloads `svchost_update.ps1` from `http://paylink-cdn.thm:8067/` to the user's Temp directory and launches it in another hidden PowerShell process. The parent Word process GUID matches Alert 6352.

## My initial assessment

I decoded the Base64 command and identified a remote PowerShell download followed by hidden execution. I correctly treated the activity as a true positive, but my initial report stopped short of a firm incident assessment because I wanted to inspect the downloaded script and network data first.

## What the command does

The encoded command:

1. Sets a staging path at `%TEMP%\svchost_update.ps1`.
2. Uses .NET `WebClient.DownloadFile` to retrieve a script over HTTP from `paylink-cdn.thm:8067`.
3. Starts another PowerShell process with no profile, a hidden window, and a process-scoped execution-policy bypass to run the downloaded file.

The execution-policy option does not disable every Windows security control. The filename resembles a system component, but that is a suspicion indicator rather than proof of masquerading.

See the decoded command in [`alert-2.ps1`](./alert-2.ps1).

## Assessment and next steps

The Word-to-PowerShell parent-child relationship, encoded command, remote script retrieval, and stealth-oriented launch options are strong evidence of malicious execution. Classify this alert as a true positive and escalate. The payload's exact capabilities and impact remain unknown until `svchost_update.ps1` and subsequent activity are examined.

> **Entities / indicators:** `THM-MSMITH.tryhatmestudios.thm`, `TRYHATME\m.smith`, `Q3_PressKit_Feedback.docm`, `WINWORD.EXE`, `powershell.exe`, `%TEMP%\svchost_update.ps1`, `paylink-cdn.thm:8067`, HTTP.
>
> **Actions:** Preserve the downloaded script and document; collect the full process tree, file hashes, PowerShell logs, DNS/proxy/firewall records, and any related Sysmon network events. Scope the destination across other hosts. Contain the affected endpoint and rotate exposed credentials in coordination with incident response.

## MITRE ATT&CK

| Technique | ID | Evidence |
|---|---|---|
| PowerShell | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) | PowerShell launches the downloader and staged script. |
| Ingress Tool Transfer | [T1105](https://attack.mitre.org/techniques/T1105/) | The command retrieves a script from a remote host. |
| Hidden Window | [T1564.003](https://attack.mitre.org/techniques/T1564/003/) | `-W Hidden` and `-WindowStyle Hidden` request hidden execution. |
| Encrypted/Encoded File | [T1027.013](https://attack.mitre.org/techniques/T1027/013/) | The initial PowerShell command is Base64-encoded. |

## Reporting correction

Use the event time above, not a later network timestamp copied into the report. State that the script was downloaded and launched; do not claim a particular impact until the downloaded content and follow-on events establish it.
