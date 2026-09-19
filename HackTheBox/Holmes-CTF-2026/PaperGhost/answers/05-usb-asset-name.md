# Q5 — The asset name DIOGENES tagged the USB with

## Question

DIOGENES tagged the USB with an asset name that surfaced as the device name on connection. What
was it?

## Why this matters

Operational teams (here "DIOGENES", an external contractor) tag their physical delivery media with
an internal asset reference. That tag surfaces to the victim's Windows session as the volume
**label** on connection, and Windows Search records it per-volume in the property store.

## Investigation steps

1. Walk `Windows.edb` `SystemIndex_GthrPth` and associate the two USB scope GUIDs (E: data
   partition, F: `VTOYEFI` boot partition) with the same physical Lexar Ventoy stick
   (`MountedDevices` + volume GUIDs `61486a41/42/43-...`).
2. Read the property-store row for the volume roots `file:E:` and `file:F:` — Windows stores the
   label in `System_ItemNameDisplay`.
3. That label is what Windows displays as the drive name when the device connects (Ventoy sticks
   expose both the data partition label and `VTOYEFI` for the boot part).

## Key findings

- The Lexar is a **Ventoy** multi-boot USB with two partitions:
  - `E:` = data partition (top level: `CO-LT-0469 update package`, `Drivers`, `Manifest`,
    `OldFiles`, `Recovery`, `Utils`)
  - `F:` = `VTOYEFI` boot partition (EFI/grub/ventoy/tool, `ENROLL_THIS_KEY_IN_MOKMANAGER.cer`)
- Property store, volume root rows:
  - `file:E:` → `System_ItemNameDisplay = "CO-USB-0091 (E:)"`
  - `file:F:` → `System_ItemNameDisplay = "VTOYEFI (F:)"`
- So the data partition was labeled **`CO-USB-0091`**, which is exactly what surfaced as the
  device name on connection.

> The previous candidate `EXT-0419` (a PDF filename from the delivery package) was an identifier
> inside the document set, **not** the volume label: the volume label is `CO-USB-0091`.

## Final answer

```text
CO-USB-0091
```

## Summary

The asset tag DIOGENES burned onto the USB is the volume label of its data partition, recorded by
Windows Search in the `SystemIndex_PropertyStore` (`file:E:` row, `System_ItemNameDisplay`). It
follows the `CO-<asset>` inventory scheme and surfaced on the victim machine as `CO-USB-0091 (E:)`
on connection.

## Difficultés rencontrées (leçons apprises)

- **Faux positif `EXT-0419`** : c'était le nom d'un PDF du package decoy (Desktop `DIOGENES_26`),
  pas le label du volume. Le label n'apparaît **pas** dans les noms de fichiers indexés mais dans
  la propriété `System_ItemNameDisplay` de la **racine du volume** (`file:E:`).
- **`F:` n'était pas un second device** : `F:` est la partition VTOYEFI d'une clé **Ventoy** (2
  partitions du même Lexar). Le décodage complet de `MountedDevices` (volume GUIDs `61486a41-…`)
  était nécessaire pour éviter de croire à un deuxième USB.
- **Structure d'encodage du property store** : les colonnes portent un préfixe de tag
  (`-System_ItemNameDisplay`), le texte est en UTF-16LE ; les dates sont des bytes FILETIME.
- La donnée est en UTC ; le `(E:)` ajouté par Windows au label ne fait pas partie du tag.

## Ressources & mapping (SOC / ATT&CK)

- Attribution du device physique → **T1091 Replication Through Removable Media**
  (<https://attack.mitre.org/techniques/T1091/>).
- Windows Search index comme source DFIR : **Aon Cyber Labs — Windows Search Index: The forensic
  artifact you've been searching for** (<https://www.aon.com/cyber-solutions/aon_cyber_labs/windows-search-index-the-forensic-artifact-youve-been-searching-for>)
  et la spec **libyal esedb-kb**
  (<https://github.com/libyal/esedb-kb/blob/main/documentation/Windows%20Search.asciidoc>).
- Outil alternatif pour Windows.edb : **Windexter**
  <https://github.com/digitalsleuth/windexter>.