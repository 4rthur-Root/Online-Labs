# PaperGhost answers index

This folder contains the 9 question-by-question walkthroughs for the PaperGhost (Sherlock 04 —
"The False Employee") challenge. Each walkthrough documents the reasoning path from a
triage-only acquisition (KAPE `TaC\Triage`: RegistryHives, LNKFilesAndJumpLists, SRUM) to the final
answer, including explicit evidence gaps.

## Index

1. [01-usb-first-connection-time.md](01-usb-first-connection-time.md)
2. [02-usb-serial-number.md](02-usb-serial-number.md)
3. [03-payload-full-path.md](03-payload-full-path.md)
4. [04-payload-execution-timestamp.md](04-payload-execution-timestamp.md)
5. [05-usb-asset-name.md](05-usb-asset-name.md)
6. [06-microphone-capture-start.md](06-microphone-capture-start.md)
7. [07-webcam-stream-duration.md](07-webcam-stream-duration.md)
8. [08-outbound-traffic-megabytes.md](08-outbound-traffic-megabytes.md)
9. [09-developer-credentials.md](09-developer-credentials.md)

## SOC mapping

This challenge aligns to the following SOC and digital forensics competencies:

- USB device forensics (USBSTOR properties, serials, volume binding)
- Windows Search index forensics (`Windows.edb` URL / scope reconstruction)
- SRUM triage (AppResourceUsage execution windows, NetworkUsage egress volume)
- LNK / Recent document timeline reconstruction
- kill-chain timeline building from triage-only artifacts
- honest reporting of "evidence gaps" when the acquisition scope cannot answer a question

## Reading pattern

Each file follows the same structure:

- Question
- Why it matters in a real SOC investigation
- Technical investigation steps
- Key findings
- Final answer
- Summary / learning points

## Final answer set

- Q1: `2026-08-19 15:35:50` (first USB connection)
- Q2: `RS200000000627E4&0` (full USBSTOR instance serial)
- Q3: `E:\CO-LT-0469 update package\update.exe`
- Q4: `2026-08-19 15:36:00` (payload execution, SRUM window start `15:36:00.009`)
- Q5: `CO-USB-0091` (volume label = asset tag)
- Q6: not determinable from triage (no mic-capture artifact)
- Q7: not determinable from triage (no webcam/video artifact)
- Q8: `172.064531` (decimal MB outbound)
- Q9: not determinable from triage (CSV bodies / credential store absent)

## Timeline (UTC, 2026-08-19)

| Time | Event |
|---|---|
| 13:42:30 | `DIOGENES_26` delivery folder populated on Desktop |
| 13:44:18 | `DIOGENES_26.lnk` created |
| 15:35:19 | `Driver Update Package.pdf` opened (Recent LNK created) |
| 15:35:50 | Lexar USB connected (FirstInstallDate); E: label `CO-USB-0091`, F: `VTOYEFI` |
| 15:36:00 | `update.exe` payload executes (cvoss; SRUM `15:36:00.009`, 10-min window) |
| 15:38:24–15:38:27 | IT_SUPPORT / EXT-0419 PDFs opened |
| 15:51:06 | USB removed |
| (≈15:36–15:46) | C2 egress: 172,064,531 bytes sent, 615,595 recv |

## Mapping SOC / ATT&CK

Kill-chain vue blue team (tactic → technique MITRE ATT&CK) :

| Step | ATT&CK | Question |
|---|---|---|
| Livraison par USB | **T1091** Replication Through Removable Media | Q1, Q2, Q5 |
| Utilisateur exécute le package | **T1204.002** User Execution: Malicious File | Q3, Q4 |
| Collecte (fichiers locaux) | **T1005** Data from Local System | Q9 |
| Capture audio / vidéo | **T1123** Audio Capture / **T1125** Video Capture | Q6, Q7 |
| Exfiltration | **T1041** Exfiltration Over C2 Channel | Q8 |
| Pivot credentials | **T1078** Valid Accounts | Q9 |

Toutes les références : <https://attack.mitre.org/>.

## Difficultés rencontrées (transverses, vécues sur cette affaire)

Chaque walkthrough documente ses propres pièges ; en transversal :

1. **Version-sensibilité des parsers** — `regipy` renvoie des `datetime` pré-décodés selon la
   version (USBSTOR `Properties\{83da6326…}`) ; toujours traiter brute *et* décodée.
2. **Colonnes/tables SRUM** — pas de `StartTime` brut (dérivé `EndTime − DurationMS×10_000`),
   colonne `TimeStamp` non-FILETIME, GUID de tables variant selon la littérature → lister
   `db.tables()`/colonnes réels avant de coder.
3. **FILETIME dans `Windows.edb`** — les dates ne se lisent pas toujours en
   `int.from_bytes(…,'little')` direct (cas 3448/9135) ; sanity-checker la plage de valeur.
4. **Pièges LNK vs CopyLog KAPE** — timestamps du header LNK = timestamps *cible*, files
   timestamps réels = colonnes `CreatedOnUtc/ModifiedOnUtc` du CopyLog.
5. **Ventoy = 2 partitions** — E: (data `CO-USB-0091`) et F: (`VTOYEFI`) sur le même stick ; sans le
   décodage complet de `MountedDevices`, `F:` aurait été pris pour un second device.
6. **UTC partout** : SRUM / USBSTOR / WSearch / CopyLog sont en UTC → normaliser avant tout
   croisement avec l'heure « locale » du double-clic.
7. **Méta vs contenu** : l'index Windows donne chemins + propriétés, pas les corps de fichiers
   (CSV) — distinguer « document indexé » de « contenu indexé ».

## Ressources (liens réels vérifiés)

Outillage & acquis lab :
- **KAPE** (Eric Zimmerman / Kroll) : <https://ericzimmerman.github.io/KapeDocs>
- **Outils EZ + SrumECmd** : <https://ericzimmerman.github.io/> , <https://github.com/EricZimmerman/Srum>
- **SRUM-DUMP** (Mark Baggett, SANS) : <https://www.sans.org/tools/srum-dump>
- **SRUM expliqué** (Magnet Forensics) : <https://www.magnetforensics.com/blog/srum-forensic-analysis-of-windows-system-resource-utilization-monitor>
- **regipy** : <https://github.com/mkorman90/regipy>
- **dissect.esedb** : <https://github.com/fox-it/dissect.esedb>

Sources d'apprentissage :
- **USB device serials** (SANS, les « mensonges » des outils) :
  <https://www.sans.org/blog/the-truth-about-usb-device-serial-numbers>
- **Windows.edb / spec du schéma Search** (Joachim Metz, libyal) :
  <https://github.com/libyal/esedb-kb/blob/main/documentation/Windows%20Search.asciidoc>
- **Windows Search en DFIR** (Aon Cyber Labs) :
  <https://www.aon.com/cyber-solutions/aon_cyber_labs/windows-search-index-the-forensic-artifact-youve-been-searching-for>
- **Artefacts registre Windows** : <https://artefacts.help/windows_registry_usb_activity.html>
- Cas réels d'IR : **The DFIR Report** <https://thedfirreport.com/> ; framework MITRE ATT&CK
  <https://attack.mitre.org/> ; méthodo NIST SP 800-86
  <https://csrc.nist.gov/publications/detail/sp/800-86/final>.