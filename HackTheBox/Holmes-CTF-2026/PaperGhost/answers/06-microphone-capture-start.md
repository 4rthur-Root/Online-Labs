# Q6 — Time the microphone capture began

## Question

Once C2 Access was live, VON BORK's listening post woke the microphone to spy on Voss's meetings.
At what time did capture begin?

## Why this matters

Microphone telemetry is a high-priority detection signal: aggressive audio capture is one of the
trademark behaviors of office-spyware implants. Knowing exactly when the mic opened lets a SOC
correlate it with the C2 beaconing and the victim's meeting schedule (`Schedule.pdf`).

## Investigation steps

1. Search the triage for audio-capture evidence:
   - `SystemEvents` / media-usage data recorded by SRUM (audio device use is not recorded there),
   - recorded media files (`*.wav`, `*.mp3`, `*.wma`, `*.m4a`) in Windows Search index,
   - C2 delivery of audio chunks.
2. Correlate the implant's execution window (Q4, `update.exe` alive 15:36–15:46 UTC) with any
   captured media object.

## Key findings / Evidence gap

The acquisition scope (`RegistryHives`, `LNKFilesAndJumpLists`, `SRUM`) contains:

- **no audio capture records** — SRUM does not record microphone-session start times, and no
  WAW/MP3 artifact managed to the disk,
- **no media file** indexed in `Windows.edb` matching an audio capture,
- **no C2 packet capture** that would show the audio stream upload.

The composable facts: the implant ran from 15:36 UTC and held its C2 channel open (see Q8 — 172 MB
exfiltrated mostly outbound), which would allow remote mic activation. Without the CSIDL-media
artifact, the *Windows partition* or a *C2 pcap*, the capture start time cannot be derived from this
triage.

## Final answer

```text
Not determinable from the provided triage artifacts.
Evidence required: media artifacts (e.g. %TEMP% WAVs), C2 pcap, or endpoint microphone telemetry.
```

## Summary

This is an honest "evidence gap" answer: a competent triage-only report flags which questions are
unanswerable rather than guessing. The realistic recommendation for the blue team is a
full-disk acquisition of the system that hosted the implant plus any C2-side captures.

## Difficultés rencontrées (leçons apprises)

- **SRUM ne journalise pas les sessions micro** : les tables contiennent des compteurs d'activité
  (CPU, réseau, énergie) mais pas « quand le micro a été ouvert ». La seule déduction possible est
  indirecte via le volume réseau exfiltré (Q8).
- **« Absence d'évidence ≠ absence de capture »** : l'implant étant vivant 15:36–15:46 UTC avec un
  canal upload massif, on ne peut pas dire que la micro n'a pas servi — simplement qu'un triage
  extrait des hives + LNK + SRUM ne peut pas le prouver.
- Un bon rapport distingue « non observé » de « non dérivable » et liste exactement *quel*
  artefact supplémentaire répondrait (WAV dans %TEMP%, pcap C2, télémétrie endpoint).

## Ressources & mapping (SOC / ATT&CK)

- Capture audio → **T1123 Audio Capture** (<https://attack.mitre.org/techniques/T1123/>).
- Comment les équipes IR réelles corrèlent ces comportements : références de cas réels sur
  **The DFIR Report** (<https://thedfirreport.com/>).
- Télémétrie micro/audio côté survie : documentation EDR/Velociraptor
  (<https://docs.velociraptor.app/>) pour récupérer ce type de données à froid.