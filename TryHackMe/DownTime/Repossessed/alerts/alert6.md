# Alert 6357 — Suspicious service creation

- **Disposition:** True positive; escalate as suspicious persistence and privileged execution.
- **Severity / type:** Critical / Lateral Movement (as labelled by the alert)
- **Host / account:** `THM-SREYES.tryhatmestudios.thm` / `TRYHATME\svc-mktshare`
- **Event time:** 2026-10-26 05:23:33.567

**Evidence:** Windows Security Event ID 4697 records creation of service `SvcUpdate`. Its configured command is `cmd.exe /c start /b powershell.exe -NoP -NonI -W Hidden -ExecutionPolicy Bypass -File C:\Windows\Temp\svchost_update.ps1`; the service account is `LocalSystem`, and start type is 3 (manual/demand start).

## My initial assessment

I recognized the hidden PowerShell command, the Temp-directory script, and the `svchost_update.ps1` name as suspicious, and classified the event as a true positive. My notes also called this a remote logon and said the service was running; those conclusions are not established by this event alone.

## Review and corrections

Event 4697 proves that a service was installed, not that it started. Start type 3 means the service is configured for manual start. The log excerpt does not establish how the account reached the host or whether the service creation came from a remote session; correlate logon events and source-host telemetry before calling it remote service creation.

The command chain is nevertheless strongly suspicious: a service configured to invoke `cmd.exe`, which starts hidden PowerShell as LocalSystem from `C:\Windows\Temp`. The service name `SvcUpdate` and script name resemble update/system components, but names alone do not prove masquerading. `-ExecutionPolicy Bypass` changes PowerShell's policy handling for that process; it does not disable all security controls. The `-W Hidden` flag hides the window, not the event from all monitoring.

The alert summary says 2026-10-23 05:25, whereas the Security event is timestamped 2026-10-26 05:23:33.567. Reconcile this before building a cross-alert timeline.

## Case note

> **Disposition:** True positive; escalate. Service registration creates a potential privileged persistence/execution mechanism. Confirm whether the service was started and what the script did.
>
> **Entities / indicators:** `THM-SREYES.tryhatmestudios.thm`, `TRYHATME\svc-mktshare`, service `SvcUpdate`, LocalSystem, `cmd.exe`, hidden PowerShell, `C:\Windows\Temp\svchost_update.ps1`.
>
> **Next steps:** Preserve service configuration and binary/script contents; inspect Event IDs 4697, 7045, 7036, process-creation events, and the service's logon context; verify file hashes and signatures; check for additional services/tasks/accounts; contain the host and scope any LocalSystem activity.

## MITRE ATT&CK

| Technique | ID | Evidence |
|---|---|---|
| Windows Service | [T1543.003](https://attack.mitre.org/techniques/T1543/003/) | A new Windows service is registered with a suspicious command. |
| Windows Command Shell | [T1059.003](https://attack.mitre.org/techniques/T1059/003/) | `cmd.exe /c` launches the next process. |
| PowerShell | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) | The service command invokes PowerShell. |
| Hidden Window | [T1564.003](https://attack.mitre.org/techniques/T1564/003/) | The command requests a hidden PowerShell window. |

## Reporting correction

Describe this as service creation, not confirmed service execution or confirmed remote logon. Avoid unsupported mappings such as Indicator Removal or generic “obfuscation” for abbreviated PowerShell flags.
