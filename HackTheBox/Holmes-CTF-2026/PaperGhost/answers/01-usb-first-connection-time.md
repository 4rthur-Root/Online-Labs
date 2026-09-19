# Q1 — When did Clara Voss first connect the device Elias Venn left at her desk?

## Question

When did Clara Voss first connect the device Elias Venn left at her desk?

## Why this matters

Every removable-device investigation starts with the same primitive question: when did the
device show up? The PnP manager writes a set of device-property timestamps that let an analyst
reconstruct the whole life of a USB device — first install, last arrival, last removal — without
touching the disk image.

## Investigation steps

1. Walk `HKLM\SYSTEM\ControlSet001\Enum\USBSTOR` for the inserted USB device.
2. Read the device-property class `{83da6326-97a6-4088-9453-a1923f573b29}`:
   - `0064` = `PKEY_Device_FirstInstallDate`
   - `0065` = `PKEY_Device_LastArrivalDate`
   - `0066` = `PKEY_Device_LastRemovalDate`
3. Convert each `REG_QWORD` FILETIME to UTC.

## Key findings

The device is a **Lexar USB Flash Drive** (`Disk&Ven_Lexar&Prod_USB_Flash_Drive&Rev_2.00`), instance
`RS200000000627E4&0`, physical device path `USB\VID_21C4&PID_0CD1\RS200000000627E4`.

| Property | Value (UTC) |
|---|---|
| FirstInstallDate (`0064`) | `2026-08-19 15:35:50.428692` |
| LastArrivalDate (`0065`) | `2026-08-19 15:35:50.428692` |
| LastRemovalDate (`0066`) | `2026-08-19 15:51:06.432548` |

`FirstInstallDate == LastArrivalDate` — the device was connected a single time, plugged in at
15:35:50 and removed at 15:51:06.

## Final answer

```text
2026-08-19 15:35:50
```

## Summary

The USBSTOR property store gives the authoritative "first touch" timestamp for an inserted
removable device. This becomes the anchor for the rest of the kill-chain timeline (payload
execution, C2 traffic, USB removal).

## Difficultés rencontrées (leçons apprises)

- **Version-sensibilité de la librairie** : selon la version de `regipy`, la valeur de
  `Properties\{83da6326-97a6-4088-9453-a1923f573b29}:0064` est renvoyée comme `int` FILETIME brut
  ou comme objet `datetime` déjà décodé. Le script d'extraction doit accepter les deux formes.
- **Le suffixe `&0`** : le nom d'instance USBSTOR (`RS200000000627E4&0`) porte le numéro de LUN ;
  pour Q1 on lit les propriétés PnP, pas le nom d'instance — ne pas confondre l'identifiant
  d'instance avec la valeur de timestamp.
- **Tous ces horodatages sont UTC** ; les fichiers KAPE en local time peuvent induire en erreur si
  l'on mélange les sources sans normaliser.
- `FirstInstallDate == LastArrivalDate` (une seule connexion) ; dans la vraie vie, comparer les
  deux champs indique si le device a été réinséré plusieurs fois.

## Ressources & mapping (SOC / ATT&CK)

- Repère temporel du kill-chain → **T1091 Replication Through Removable Media**
  (<https://attack.mitre.org/techniques/T1091/>).
- Guide méthodologique d'acquisition : **NIST SP 800-86** (Guide to Integrating Forensic
  Techniques into Incident Response).
- Localisation des artefacts USB : <https://artefacts.help/windows_registry_usb_activity.html> et
  <https://vortexforensic.com/repository/Registry/usbstor_reg.html>.
- Très bonne piqûre de rappel sur ce que ces valeurs sont réellement :
  <https://www.sans.org/blog/the-truth-about-usb-device-serial-numbers>.