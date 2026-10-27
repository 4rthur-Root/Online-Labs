# Alert 6355 — Anomalous Credential Vault Access

- **Disposition:** True positive; escalate as credential-access discovery within the malicious PowerShell chain.
- **Severity / type:** High / Credential Access
- **Host / user:** `THM-MSMITH.tryhatmestudios.thm` / `TRYHATME\m.smith`
- **Event time:** 2026-10-23 02:42:16.962
**Evidence:** Sysmon Event ID 1; the script `svchost_update.ps1`, launched by hidden PowerShell from the user's Temp directory, runs `C:\Windows\Sysnative\vaultcmd.exe /listcreds:Windows Credentials`.

## My initial assessment

I recognized that `vaultcmd.exe` is a Windows utility and that the `Sysnative` path can be legitimate. I also noted the suspicious PowerShell parent, Temp-directory script, and unfamiliar account context, and classified the activity as a true positive. I initially described the command as identifying credential targets and suggested that it could lead to password extraction.

## Review and corrections

`vaultcmd /listcreds` enumerates entries in Windows Credential Manager; this command does not, by itself, reveal plaintext passwords or prove that credentials were extracted. The `Sysnative` path is a Windows alias that lets a 32-bit process access the native 64-bit System32 directory, so it is not inherently a malicious file location.

The key context is the parent process: a hidden, execution-policy-bypassed PowerShell process running a script from the user's Temp directory. That makes this credential enumeration suspicious, even though the built-in utility and its path can be legitimate. A hash difference from a third-party reference is not proof of tampering; compare the file version, signature, and hash against a trusted copy from the same OS build.

The event time is 2026-10-23, not the 2026-10-26 date in my original report. The employee/account lookup and timeline should be verified before describing the user as unknown or unauthorized.

## Case note

> **Disposition:** True positive; escalate. The event shows credential-store enumeration by a script in a suspicious execution chain. It does not show successful password extraction.
>
> **Entities / indicators:** `THM-MSMITH.tryhatmestudios.thm`, `TRYHATME\m.smith`, `vaultcmd.exe`, `/listcreds:Windows Credentials`, `%LOCALAPPDATA%\Temp\svchost_update.ps1`, hidden PowerShell.
>
> **Next steps:** Inspect PowerShell/script content and process descendants; review vault-related file access and any credential use afterward; determine whether the user had a legitimate troubleshooting task; scope the account and host for lateral movement. Treat credentials as potentially exposed if corroborating evidence is found.

## MITRE ATT&CK

| Technique | ID | Evidence |
|---|---|---|
| Credentials from Password Stores: Windows Credential Manager | [T1555.004](https://attack.mitre.org/techniques/T1555/004/) | The command enumerates the Windows Credential Manager. It does not alone prove credential theft. |
| PowerShell | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) | The script is executed by PowerShell. |

## Reporting correction

Use the event timestamp, and say “enumerated stored credentials” rather than “stole passwords.” Escalation is still justified by the suspicious parent process and the relationship to the broader intrusion.
