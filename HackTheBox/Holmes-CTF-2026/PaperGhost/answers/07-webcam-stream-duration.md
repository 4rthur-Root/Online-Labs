# Q7 — For how many seconds did the webcam stream?

## Question

VON BORK mapped Voss's office through her webcam — who came and went, what lay on her desk. For how
many seconds did the webcam stream?

## Why this matters

Webcam exfiltration is one of the most intrusive spyware behaviors and, like microphone capture,
leaves a measurable footprint — duration of the capture session, frame count, encoding bitrate,
file size. Packet captures of the exfil stream and any local encoded artifact allow the analyst to
compute the exact duration.

## Investigation steps

1. Look for encoded video artifacts (local or indexed): `*.mp4`, `*.avi`, `*.wmv`, `*.mkv`,
   `*.webm`, thumbnails (.thumbnails somehow present on the exfil desktop?).
2. Look for camera usage recorded in the triage (none of the collected hives store camera streams).
3. Derive duration if a C2 pcap were available: `duration ≈ stream_bytes / bitrate`.

## Key findings / Evidence gap

The triage contains:

- **no video file** — no MP4/AVI/WMV in the Windows Search index, no webcam cache folder,
- **no camera-usage record** in the collected registry hives,
- **no C2 pcap** — the SRUM NetworkUsage only tells us *update.exe* sent 172,064,531 bytes in its
  window (Q8); it cannot distinguish microphone bytes from webcam bytes.

The implant clearly had a large outbound channel (172 MB in ~10–15 minutes), but that volume is
shared with the microphone session (Q6), configuration calls and any file uploads. Neither the
duration nor a per-medium split can be derived from SRUM alone.

## Final answer

```text
Not determinable from the provided triage artifacts.
Evidence required: video artifact (local or exfiltrated) or C2 pcap with media stream metadata.
```

## Summary

Another explicit evidence gap. The answer set is stronger when the shortcoming is stated precisely:
SRUM gives byte-level network totals, not per-stream durations. A complete disk image or C2-side
capture is required to answer camera questions.

## Difficultés rencontrées (leçons apprises)

- **Le device webcam existe dans l'énumération** (`USB\VID_0C45` = Sonix, instance `SN0001`), mais
  une présence dans `Enum\USB` ne dit rien d'une capture : aucun fichier vidéo ni cache
  webcam n'était indexé.
- **SRUM mélange les flux** : les 172 MB upload de `update.exe` (Q8) regroupent micro, webcam,
  config et fichiers — impossible d'en dériver la durée d'une seule session vidéo sans pcap des
  métadonnées du stream (bitrate, framerate).
- Tenter `durée ≈ octets / bitrate` nécessite un bitrate *connu*, inconnu ici — au-delà du degré de
  précision un rapport d'IR doit assumer.

## Ressources & mapping (SOC / ATT&CK)

- Capture vidéo → **T1125 Video Capture** (<https://attack.mitre.org/techniques/T1125/>).
- Indices de présence de webcam dans l'énum : `SYSTEM\ControlSet001\Enum\USB\VID_0C45`
  (<https://www.devicehunt.com/vendor/0c45/>) — toujours distinguer « device présent » de « device
  utilisé ».
- Cas d'usage réels d'implant avec exfiltration media : **The DFIR Report**
  <https://thedfirreport.com/>.