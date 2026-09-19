# Q8 — How many decimal megabytes of outbound traffic flowed to the C2?

## Question

The riverside relay drank Voss's secrets. How many decimal megabytes of outbound traffic flowed
from the compromised machine to the C2?

## Why this matters

Network egress quantification is the bread-and-butter of breach triage. SRUM NetworkUsage (fields
`BytesSent` / `BytesRecvd` per application) provides a per-process byte ledger without any packet
capture — exactly the metric needed to size an exfiltration.

## Investigation steps

1. Parse `SRUDB.dat` table `{973F5D5C-1D90-4944-BE8E-24B94231A174}` (NetworkUsage,
   `BytesSent`/`BytesRecvd`). Note: the GUID varies across published docs — verify the actual table
   schema (`db.tables()`/columns) before coding.
2. Filter rows by the AppId of the payload (`#436` = `\device\harddiskvolume5\co-lt-0469 update
   package\update.exe`).
3. Confirm the user context: UserId `374` = `S-1-5-21-1025544563-1542558241-544662972-1002` =
   `cvoss`.
4. Convert bytes to decimal megabytes (`bytes / 1_000_000`).

## Key findings

```
AppId 436  \device\harddiskvolume5\co-lt-0469 update package\update.exe
  BytesSent = 172,064,531
  BytesRecvd = 615,595
  (UserId = 374 → cvoss)
```

- Outbound: `172 064 531 B` → `172.064531 MB` (decimal)
- Inbound is negligible (615 KB) — a strictly upload-oriented channel, typical of a media/log
  bulker feeding the C2 relay.

## Final answer

```text
172.064531
```

## Summary

SRUM is the one artifact in a KAPE triage that can reconstruct per-process egress volume. The
~1:280 upload/download imbalance is itself diagnostic: the implant is built to exfiltrate, not to
receive commands over volume — command-and-control here is a thin control channel riding on a fat
upload stream (the microphone/webcam sessions).

## Difficultés rencontrées (leçons apprises)

- **GUID de tables SRUM incohérents dans la littérature** : la table NetworkUsage effective est
  `{973F5D5C-1D90-4944-BE8E-24B94231A174}` (champs `BytesSent/BytesRecvd`) — les GUID publiés
  diffèrent selon les sources ; toujours **lister les tables + colonnes réelles du fichier avant de
  coder** (`dissect.esedb` : `db.tables()` puis `t.columns`).
- **Unité : méga-octets décimaux** : la question demande des « decimal megabytes » → `bytes /
  1_000_000` (pas `2^20`) = `172.064531` ; documenter l'unité choisie sinon la réponse varie.
- **Le UserId SRUM est un index, pas un SID** : `374` → SID → `cvoss` via la résolution idmap puis
  `SOFTWARE\...\ProfileList`.
- L'AppId réseau (#436, minuscules) diffère de l'AppId d'exécution (#430) — toujours relire les
  deux formes du chemin.

## Ressources & mapping (SOC / ATT&CK)

- Exfiltration → **T1041 Exfiltration Over C2 Channel** (<https://attack.mitre.org/techniques/T1041/>).
- **SrumECmd** (parse officiel, inclut SOFTWARE pour les interfaces réseau) :
  <https://github.com/EricZimmerman/Srum>.
- **SRUM-DUMP** de Mark Baggett (vue tableur orientée analyse) :
  <https://www.sans.org/tools/srum-dump>.