# Alert 6352 — Suspicious child process spawned

- **Initial disposition:** False positive for the `ai.exe` process event; keep the related document activity open and correlate it with Alert 6353.
- **Severity / type:** High / Execution
- **Host / user:** `THM-MSMITH.tryhatmestudios.thm` / `TRYHATME\m.smith`
- **Event time:** 2026-10-25 01:27:19.569

**Evidence:** Sysmon Event ID 1; `WINWORD.EXE` opened `Q3_PressKit_Feedback.docm` and spawned Microsoft's `ai.exe` from the Office AI directory. The binary is described as the local AI host and carries a Microsoft company name. The same Word parent process GUID appears in Alert 6353.

## My initial assessment

I first leaned toward a false positive because the child was a Microsoft Office AI component and my initial Splunk search did not return useful related events. I then noticed the macro-enabled document and the connection with the later PowerShell alert, so I changed my view and escalated the activity.

![Splunk search with no matching events](./evidences/file-name.png)

## Review and corrections

The `ai.exe` event itself is consistent with a legitimate Office helper; its presence alone does not establish malicious execution. The screenshot's query searches for `DC-01.tryhatmestudios.thm`, not the alerted host `THM-MSMITH.tryhatmestudios.thm`, so its zero results do not validate this event. A missing Splunk result is not proof that nothing happened: check the time range, host and field names, index permissions, and expected ingestion delay.

The correlation is still important. Alert 6353 records the same `WINWORD.EXE` parent process launching hidden PowerShell. Treat the AI helper as benign unless contrary evidence appears, but investigate the document and its other child processes as part of the confirmed suspicious chain. This is a useful example of separating a benign event from a malicious process launched by the same parent.

The alert summary labels the activity as 2026-10-26 02:05, while the supplied Sysmon event is timestamped 2026-10-25 01:27:19.569. Confirm timezone and alert-window normalization before using either as the incident timeline.

## Case note

> **Disposition:** False positive for this specific child-process event. Correlate and escalate the document/process chain with Alert 6353; do not close the related incident based on the benign AI binary.
>
> **Entities:** `THM-MSMITH.tryhatmestudios.thm`, `TRYHATME\m.smith`, `WINWORD.EXE`, `ai.exe`, `Q3_PressKit_Feedback.docm`.
>
> **Next steps:** Verify the document's origin and hash, inspect the complete Word process tree and adjacent Sysmon events, and determine whether any macro or embedded content ran. Preserve the document and related telemetry.

## MITRE ATT&CK

No technique is established by the `ai.exe` event alone. Do not assign a malicious-document technique to a legitimate helper process without evidence that the document's contents executed.
