# Q4 — Exact timestamp when the malicious package was executed

## Question

Believing it a routine update, Voss launched the spyware. At what exact timestamp did she execute
the malicious package?

## Why this matters

The precise execution window of the implant anchors the entire incident timeline. It must be
reconciled against the USB arrival (Q1), the documents she opened, and the C2 telemetry (Q8) to
build a coherent attack narrative.

## Investigation steps

1. Filter the SRUM AppResourceUsage table `{5C8CF1C7-7257-4F13-B223-970EF5939312}` for the app
   index of `update.exe` (idmap `#430`, `update.exe!2010/04/14:22:06:53!3b283!`).
2. Read `EndTime` (FILETIME) and `DurationMS`, compute `StartTime = EndTime - DurationMS`.
3. Resolve the `UserId` index to a SID and to the profile list.

## Key findings

```
AppId 430 (update.exe) - UserId 374
  Start 2026-08-19 15:36:00.009
  End   2026-08-19 15:46:00.010
  Duration 600001 ms (10-minute bucket, entire window)
```

UserId `374` resolves to `S-1-5-21-1025544563-1542558241-544662972-1002`, which `SOFTWARE`
`ProfileList` maps to `C:\Users\cvoss` — **Clara Voss** ran the payload 10 seconds after the USB
was installed (15:35:50). The nearest document-level events corroborate the chain:

| Event | Time (UTC) |
|---|---|
| `DIOGENES_26` desktop folder populated | 2026-08-19 13:42:30 |
| USB connected (FirstInstallDate) | 2026-08-19 15:35:50 |
| `Driver Update Package.pdf` opened (Recent LNK created `15:35:19.913`) | 2026-08-19 15:35:19 |
| `update.exe` execution window (SRUM start, 15:36:00.009) | **2026-08-19 15:36:00** |
| USB removed | 2026-08-19 15:51:06 |

## Final answer

```text
2026-08-19 15:36:00
```

Corroboration and precision notes:

- SRUM is recorded in **UTC** and is the only process-start telemetry in a triage-only acquisition
  (no Prefetch in this triage).
- The SRUM interval starts at `15:36:00.009`; the whole-second form `2026-08-19 15:36:00` is the
  answer (same `YYYY-MM-DD hh:mm:ss` UTC format as Q1).
- 40 seconds earlier the user opened `Driver Update Package.pdf` (Recent LNK `Driver Update
  Package.lnk` created `2026-08-19 15:35:19.913`) — the "routine update" document that preceded
  launching the payload; that LNK targets the Desktop copy, not the payload itself.

## Difficultés rencontrées (leçons apprises)

- **Pas de colonne StartTime brute** dans la table AppResourceUsage : le début s'obtient par
  `EndTime (FILETIME) − DurationMS × 10 000` — un calcul facile à oublier et source d'erreur
  d'interprétation (le `.009` vient de cette arithmétique, pas d'un horodatage stocké).
- **Colonne `TimeStamp` SRUM encodée** : elle n'est pas un FILETIME standard (valeur > plage
  légale) — ne pas la décoder naïvement ; elle code le flush provider, pas l'exécution.
- **Absence de Prefetch** dans ce triage : si `C:\Windows\Prefetch` était présent, `update.exe` y
  aurait un `.pf` avec un timestamp d'exécution fin ; ici seule la fenêtre SRUM subsiste.
- **Piège LNK** : les champs du header d'un `.lnk` (cTime/aTime/wTime) sont les horodatages de la
  **cible**, pas du fichier `.lnk` ; les vrais timestamps du fichier viennent du **CopyLog KAPE**
  (`CreatedOnUtc`). `Driver Update Package.lnk` pointe vers le PDF du Desktop, pas vers l'exe.
- Le format d'horodatage attendu est celui de Q1 (UTC, secondes entières) — homogénéiser les
  réponses.

## Ressources & mapping (SOC / ATT&CK)

- Tactique correspondante → **T1204.002 User Execution: Malicious File**
  (<https://attack.mitre.org/techniques/T1204/002/>).
- SRUM : blog **Magnet Forensics** « SRUM: Forensic Analysis of Windows System Resource Utilization
  Monitor » (<https://www.magnetforensics.com/blog/srum-forensic-analysis-of-windows-system-resource-utilization-monitor>)
  et **SrumECmd** (<https://github.com/EricZimmerman/Srum>).
- Format LNK : spécification **MS-SHLLINK**
  <https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/>.

## Summary

- SRUM AppResourceUsage is the only registry/DB telemetry precise enough to date an execution from
  a triage-only acquisition.
- The 10-minute-aligned bucket and run duration tell us the process was alive during the whole
  window — consistent with a spyware implant establishing persistence, not a one-shot installer.