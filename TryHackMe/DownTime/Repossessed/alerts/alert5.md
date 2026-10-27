# Alert 6356 — Rapid domain and host enumeration

- **Disposition:** True positive; escalate as post-compromise discovery.
- **Severity / type:** High / Discovery
- **Host / user:** `THM-MSMITH.tryhatmestudios.thm` / `TRYHATME\m.smith`
- **Event time:** 2026-10-26 02:08:42.547

**Evidence:** Sysmon Event ID 1; `net.exe user /domain` runs as a child of hidden PowerShell executing `%LOCALAPPDATA%\Temp\svchost_update.ps1`.

## My initial assessment

I connected the domain-user enumeration to the same suspicious script and correctly classified it as a true positive. I identified Discovery as the relevant tactic and recommended inspecting the script.

## Review and corrections

The process lineage is strong context: this is not just an isolated use of a built-in administrative command. `net user /domain` queries domain accounts. The evidence provided here does not show `net group` or another group-enumeration command, so do not report domain-group discovery as observed. The alert description says the detection aggregates a burst, but this event record shows only one command; retrieve the full grouped event set before describing the complete sequence.

The initial report's host label should be `THM-MSMITH.tryhatmestudios.thm`, not `HM-MSMITH`.

The alert summary is dated 2026-10-23, but the event record is dated 2026-10-26 02:08:42.547. Use the event timestamp provisionally and verify the time range and normalization in the SIEM.

## Case note

> **Disposition:** True positive; escalate as part of the confirmed script-led intrusion.
>
> **Entities / indicators:** `TRYHATME\m.smith`, `THM-MSMITH.tryhatmestudios.thm`, `net.exe user /domain`, `svchost_update.ps1`, hidden PowerShell.
>
> **Next steps:** Recover the full enumeration burst and command outputs if logged; identify subsequent authentication and network activity; search for the same script, hash, and account on other systems; investigate potential credential use and lateral movement.

## MITRE ATT&CK

| Technique | ID | Evidence |
|---|---|---|
| Account Discovery: Domain Account | [T1087.002](https://attack.mitre.org/techniques/T1087/002/) | `net.exe user /domain` enumerates domain accounts. |
| PowerShell | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) | PowerShell launches the script that starts the enumeration. |

## Reporting correction

Keep the claim to domain-account enumeration unless the remaining aggregated events show group or host discovery. “The attacker enumerated domain users” is better supported than “the attacker enumerated users and groups.”
