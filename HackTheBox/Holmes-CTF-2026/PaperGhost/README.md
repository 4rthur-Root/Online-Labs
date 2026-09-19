# PaperGhost — Sherlock 04 "The False Employee" (Holmes CTF 2026)

Analysis of the PaperGhost sherlock from the Holmes CTF 2026 lab environment. A USB device left by a
contractor ("Elias Venn") at an employee's desk delivers a fake update package; a spyware implant
("update.exe") is executed by the victim (Clara Voss, `cvoss` on host `CO-LT-0469`), exfiltrating
172 MB to a C2. This workbook reconstructs the kill chain from a **triage-only** acquisition
(KAPE `TaC\Triage`: `RegistryHives`, `LNKFilesAndJumpLists`, `SRUM`).

## Reproducible analysis

Environment pinned with `uv` (`PaperGhost/pyproject.toml` → `regipy`, `dissect.esedb`):

```bash
uv sync
uv run python scripts/extract_usbstor.py   # Q1, Q2 — USBSTOR serial + timestamps
uv run python scripts/parse_srum.py        # Q3/Q4/Q8 — SRUM idmap / execution / network
```

Scripts write raw outputs into `analysis/` (git-ignored). Artifacts in `artifacts/Triage/` are
read-only.

## Folder layout

- `artifacts/` — challenge triage artifacts (read-only)
- `scripts/` — reproducible parsers (paths, usbstor, srum)
- `analysis/` — generated CSV extracts (ignored)
- `answers/` — question-by-question walkthroughs

## Questions covered

1. When did Voss first connect the dropped device?
2. Serial number of the dropped device
3. Full path of the payload hidden in the fake update package
4. Exact timestamp of payload execution
5. Asset name DIOGENES tagged the USB with
6. Time the microphone capture began
7. Webcam stream duration in seconds
8. Decimal megabytes of outbound traffic to the C2
9. Credentials surfaced for a DIOGENES developer

## Answers summary

- 1 — `2026-08-19 15:35:50` (USBSTOR FirstInstallDate, single connection)
- 2 — `RS200000000627E4&0` (Lexar USB Flash Drive, USBSTOR instance, VID_21C4&PID_0CD1)
- 3 — `E:\CO-LT-0469 update package\update.exe` (SRUM idmap + Windows Search index)
- 4 — `2026-08-19 15:36:00` (SRUM AppResourceUsage, cvoss; window start `15:36:00.009`)
- 5 — `CO-USB-0091` (E: volume label — Ventoy data partition asset tag)
- 6 — not determinable from triage (microphone evidence gap)
- 7 — not determinable from triage (webcam/video evidence gap)
- 8 — `172.064531` MB outbound (172,064,531 bytes sent, 615,595 recv)
- 9 — not determinable from triage (credential/CSV-body evidence gap)

## Kill-chain summary

1. **Delivery**: Lexar Ventoy USB (`RS200000000627E4&0`, USB\VID_21C4&PID_0CD1, data partition
   labeled `CO-USB-0091`) carries `CO-LT-0469 update package\update.exe` — an impostor "IT update"
   folder; the desktop copy of the decoy package (`DIOGENES_26`) contains PDFs and asset/contractor
   CSVs.
2. **Initial access**: USB installed 15:35:50; Voss launches the "update" → `update.exe` runs
   from E: starting 15:36:00 (SRUM, user `cvoss`).
3. **C2 / exfiltration**: `update.exe` pushes 172,064,531 bytes outbound (≈1:1 – 280 upload vs
   download) — consistent with live microphone/webcam session streaming to the "riverside relay".
4. **Cleanup**: USB removed 15:51:06; the implant left no persistence artifacts in the collected
   scopes.

## Next steps for a full resolution

- Obtain the full disk image to read `IT_Asset_Inventory.csv` / `DIOGENES_Contractor_Assignments.csv`
  (Q9 credentials).
- Obtain the C2-side capture / media files for the microphone (Q6) and webcam (Q7) sessions.
- Add Prefetch/EventLogs/AMCache to the acquisition for persistence and service-creation proof.

## Pour apprendre

- **Mapping SOC/ATT&CK**, difficultés rencontrées et liens réels (KAPE, SrumECmd, SRUM-DUMP,
  USBSTOR, Windows.edb) : voir [answers/README.md](answers/README.md).
- Chaque walkthrough (`answers/01…09`) finit par « Difficultés rencontrées (leçons apprises) » et
  « Ressources & mapping (SOC / ATT&CK) » — pensés pour reproduire l'enquête en lab.
- Réexécution reproductible : `uv run python scripts/extract_usbstor.py` (Q1/Q2) et
  `uv run python scripts/parse_srum.py` (Q3/Q4/Q8) alimentant `analysis/`.

## Start here

Use the answers index in [answers/README.md](answers/README.md) to navigate all question
walkthroughs.