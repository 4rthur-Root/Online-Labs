# Alert 1

- id: 6355

- alert Rule: Anomalous Credential Vault Access

- Severity: <span style="color: orange;">High</span>   

- Type: Credential Access

- Date: Oct 23rd 2026 at 02:44

## Key details

| Field | Value |
|-------|-------|
| Description | This detection fires when a process enumerates or reads credentials held in the local Windows credential store. Stored credentials are a common target once a threat actor has obtained code execution on a host, because they allow movement to other systems without further exploitation. Support staff do occasionally query the credential store during troubleshooting, so the analyst must determine which process initiated the access, what launched that process, and which credentials were exposed. |
| CommandLine | `"C:\Windows\Sysnative\vaultcmd.exe" "/listcreds:Windows Credentials"` |
| Company | Microsoft Corporation |
| CurrentDirectory | `C:\Windows\system32\` |
| Description (Process) | Vault cmdline Program |
| EventCode | 1 |
| EventType | 4 |
| FileVersion | 10.0.22621.1 (WinBuild.160101.0800) |
| Hashes | MD5=4D2AD9A08F33212EDE3A128E23F00759, SHA256=D76274F883C86EF2B9090E43935D9ADC6B81B35A2A6FA39E37890F80FDFA9B76, IMPHASH=423E299DF33B8039596FF81AE53C9CA4 |
| Image | `C:\Windows\System32\VaultCmd.exe` |
| IntegrityLevel | Medium |
| LogName | Microsoft-Windows-Sysmon/Operational |
| LogonGuid | {3af46175-c39c-6a8f-e030-9c0000000000} |
| LogonId | 0x9C30E0 |
| OpCode | Info |
| OriginalFileName | VAULTCMD.EXE |
| ParentCommandLine | `"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -NoP -W Hidden -ExecutionPolicy Bypass -File "C:\Users\MC0CD~1.SMI\AppData\Local\Temp\svchost_update.ps1"` |
| ParentImage | `C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe` |
| ParentProcessGuid | {3af46175-390a-6a90-991d-000000001200} |
| ParentProcessId | 9356 |
| ParentUser | TRYHATME\m.smith |
| ProcessGuid | {3af46175-390c-6a90-9d1d-000000001200} |
| ProcessId | 10872 |
| Product | Microsoft® Windows® Operating System |
| Sid | S-1-5-18 |
| SidType | 0 |
| SourceName | Microsoft-Windows-Sysmon |
| TaskCategory | Process Create (rule: ProcessCreate) |
| TerminalSessionId | 4 |
| Type | Information |
| User | [ "NOT_TRANSLATED", "TRYHATME\\m.smith" ] |
| category | Process Create (rule: ProcessCreate) |
| event_id | 46167 |
| host | THM-MSMITH.tryhatmestudios.thm |
| timestamp | 10/23/2026 02:42:16.962 |
| datasource | WinEventLog:Microsoft-Windows-Sysmon/Operational |

This alert involver `VaultCmd.exe` which is Windows Credential Manager. More information on how to identify it on [strontic](https://strontic.github.io/xcyclopedia/library/VaultCmd.exe-24AD59DBE3B726704E1444C83F6CEF06.html).

The command `vaultcmd /listcreds:"Windows Credentials"` is a native Windows utility used to **enumerate and list credentials** stored in the Windows Credential Manager for applications and devices using **NTLM or Kerberos** authentication.

Key details regarding its usage and security implications include:

*   **Functionality**: It displays metadata such as resource, identity, and authentication type, but **does not reveal clear-text passwords** because the data is encrypted using the Windows Data Protection API (DPAPI).
*   **File Locations**: The encrypted credentials are stored in `.vcrd` files within `%Systemdrive%\Users\[Username]\AppData\Local\Microsoft\Vault`, while the decryption key is stored in `Policy.vpol`.
*   **Security Risk**: Adversaries use this command ([MITRE ATT&CK **T1555.004**](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1555.004/T1555.004.md)) to identify valuable credentials for lateral movement, often correlating it with direct file access to `.vcrd` files to attempt offline decryption.
*   **Detection**: Security solutions monitor for the execution of `vaultcmd.exe` with the `/listcreds:` argument to detect unauthorized credential access attempts.

The legitimate location is **C:\Windows\System32\vaultcmd.exe**. 

The path encountered here **c:\windows\sysnative\vaultcmd.exe**  is the same file. Sysnative is a virtual folder that 32-bit processes on a 64-bit OS use to access the real 64-bit System32 directory (the reverse of SysWOW64, which 64-bit processes use to reach 32-bit binaries). So a 32-bit process referencing sysnative\vaultcmd.exe is hitting the exact same binary as a 64-bit process referencing system32\vaultcmd.exe. 

But in other locations (e.g. %AppData%\Local\Temp, %AppData%\Roaming\...), that's a red flag cause those are common paths for malicious copies.

Things are getting weird cause the user who ran it is *TRYHATME\m.smith* who is not known employeer according to [Company Information](./../README.md/###company-information) but mostly **`C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -NoP -W Hidden -ExecutionPolicy Bypass -File "C:\Users\MC0CD~1.SMI\AppData\Local\Temp\svchost_update.ps1`** is a highly suspicious command line indicative of malware or a fileless attack.

Key Indicators of Malicious Activity:

- *Hidden Window (-W Hidden)*: Legitimate administrative scripts rarely need to run invisibly. This flag is commonly used by malware to hide its execution from the user.

- *Execution Policy Bypass (-ExecutionPolicy Bypass)*: This overrides Windows security settings that normally prevent unsigned or unauthorized scripts from running. 

- *Temp Directory Location (AppData\Local\Temp)*: Malware frequently drops scripts in temporary folders to avoid detection in standard program directories.

- *Deceptive Filename (svchost_update.ps1)*: The script mimics the name of svchost.exe, a critical Windows system process, to trick users into ignoring it.

- *Encoded Command Precedent*: Security logs often show similar malicious commands using -EncodedCommand (long base64 strings) to hide the actual payload, so using -File with a hidden window is a common variant.

And `file.path="C:\Users\MC0CD~1.SMI\AppData\Local\Temp\svchost_update.ps1"` doesn't show anything in splunk .

vaultcmd by itself only enumerates (lists usernames, target resources, auth type). It can't spit out plaintext passwords. But in this context, it's likely a recon step inside a larger malicious operation:
| Flag | Why it's suspicious |
|------|---|
| `-NoP` | NoProfile hides PowerShell banner, common in malware |
| `-W Hidden` | No visible window |
| `-ExecutionPolicy Bypass` | Overrides script execution restrictions |
| `AppData\Local\Temp\svchost_update.ps1` | Script in Temp, name mimics a legitimate Windows process (`svchost`) |

What the attacker can do with the vaultcmd output:

1. Identify targets: the output tells them which credentials exist (e.g., a saved RDP credential to 10.0.1.50, a web credential to internal-portal.corp.com, a WiFi profile). This is the "what's worth stealing" phase.
2. Extract actual passwords: once they know what's there, they can :

- Read the .vcrd files directly from %AppData%\Local\Microsoft\Vault\ and attempt offline DPAPI decryption (using the user's DPAPI key from the registry)

- Use Mimikatz (vault::list / vault::cred) or Get-WebCredentials.ps1 to pull plaintext

- Import vaultcli.dll directly into their own process (seen in info-stealers like Meduza)

3. Lateral movement: harvested RDP/NTLM credentials let them pivot to other hosts.

The combination of a hidden PowerShell from Temp calling vaultcmd is a classic [MITRE T1555.004 (Credentials from Password Stores: Windows Credential Manager) pattern.](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1555.004/T1555.004.md).
Hash also different from [strontic one's](https://strontic.github.io/xcyclopedia/library/VaultCmd.exe-24AD59DBE3B726704E1444C83F6CEF06.html).

So I decided to claasify as <span style="color: red;">True Positive</span>.



## Report
```Markdown
Time of activity: Oct 23rd 2026 at 02:44

List of Affected Entities: A machine running Windows OS

Reason for Classifying as True Positive: A not known user ran a custom script with suspicious flags to identify targets on the machine . 

Reason for Escalating the Alert: This alert looks like the first phase of a reconnaissance as atomic red team T1555.004 suggests it .

Recommended Remediation Actions: 

List of Attack Indicators: CommandLine:
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -NoP -W Hidden -ExecutionPolicy Bypass -File "C:\Users\MC0CD~1.SMI\AppData\Local\Temp\svchost_update.ps1
User: TRYHATME\m.smith
```

Go to [alert2](./alert2.md)
