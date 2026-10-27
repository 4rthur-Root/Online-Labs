# Alert 6359 — Suspicious archive utility execution

- **Disposition:** True positive; escalate as suspicious collection and staging.
- **Severity / type:** High / Collection
- **Host / user:** `THM-SREYES.tryhatmestudios.thm` / `NT AUTHORITY\SYSTEM`
- **Event time:** 2026-10-26 05:30:24.567

**Evidence:** Sysmon Event ID 1; `7z.exe` runs as SYSTEM with the command `7z.exe a -mx=1 C:\Windows\Temp\nx_build_beta.7z C:\Dev\NeuralNexus\Build\*`. Its parent is hidden PowerShell running `C:\Windows\Temp\svchost_update.ps1`.

## My initial assessment

I recognized that the suspicious script launched 7-Zip to archive the NeuralNexus build output into `C:\Windows\Temp`. I suspected the archive might be prepared for exfiltration, but my notes overstated what was proved by saying the data was being sent.

## Review and corrections

The command proves that 7-Zip was instructed to create an archive from the build directory. The parent-child relationship to the suspicious script, SYSTEM context, and staging location make the activity highly suspicious. The event does not show the archive's contents, successful creation, or transfer to a remote destination.

The later Alert 6360 connection shares the parent PowerShell process GUID, which is relevant to the broader chain. Alert 6358 is a different PowerShell process and occurred before this archive event; it should not be used as proof of this archive's transfer.

## Case note

> **Disposition:** True positive; escalate as suspicious collection/staging in a confirmed intrusion. Exfiltration remains unconfirmed until network or file evidence links the archive to a transfer.
>
> **Entities / indicators:** `THM-SREYES.tryhatmestudios.thm`, SYSTEM, `7z.exe`, `C:\Dev\NeuralNexus\Build\*`, `C:\Windows\Temp\nx_build_beta.7z`, `svchost_update.ps1`.
>
> **Next steps:** Preserve and hash the archive; inspect its contents and creation metadata; compare the source build to a known-good signed artifact; inspect 7-Zip and parent PowerShell logs; correlate Alert 6360 by process GUID and network telemetry.

## MITRE ATT&CK

| Technique | ID | Evidence |
|---|---|---|
| Archive Collected Data: Archive via Utility | [T1560.001](https://attack.mitre.org/techniques/T1560/001/) | 7-Zip is instructed to archive build output. |

## Reporting correction

Use “archive creation/staging” until transfer is demonstrated. `7z.exe` is the executable name in the event; do not report `7zip.exe` or `svchost_update.exe` as observed process names.
