# Q2 — What serial number did the dropped device leave behind?

## Question

What serial number did the dropped device leave behind?

## Why this matters

A serial number is the single most durable identifier of a USB device. It lets an incident
response team blacklist the hardware in the EDR, SIEM and physical-access systems, and answer
"is this same device showing up on other machines?" — the classic handshake used in targeted
USB-dropping attacks (vishing/physical social engineering, FOB smuggling).

## Investigation steps

1. From `HKLM\SYSTEM\ControlSet001\Enum\USBSTOR`, list every instance under the Lexar class
   `Disk&Ven_Lexar&Prod_USB_Flash_Drive&Rev_2.00`.
2. Cross-check the `USB\VID_21C4&PID_0CD1\<serial>` identity in `HKLM\SYSTEM\ControlSet001\Enum\USB`.
3. Cross-check the drive-letter binding in `HKLM\SYSTEM\MountedDevices`.

## Key findings

- USBSTOR instance: `RS200000000627E4&0`
- USB device path: `USB\VID_21C4&PID_0CD1\RS200000000627E4`
- Vendor/product: Lexar (VID `21C4`), USB Flash Drive (PID `0CD1`)
- `MountedDevices` maps the volume to `E:` via the same USBSTOR identity:
  `\??\USBSTOR#Disk&Ven_Lexar&Prod_USB_Flash_Drive&Rev_2.00#RS200000000627E4&0#...`

## Final answer

```text
RS200000000627E4&0
```

## Summary

The serial is embedded in the **USBSTOR instance name** (`RS200000000627E4&0` — the full instance
key under `Disk&Ven_Lexar&Prod_USB_Flash_Drive&Rev_2.00`), and confirmed in every other artifact:
`USB\VID_21C4&PID_0CD1\RS200000000627E4`, `MountedDevices`
(`\??\USBSTOR#Disk&Ven_Lexar&Prod_USB_Flash_Drive&Rev_2.00#RS200000000627E4&0#...`) and the
WPD/STORE device paths. The accepted answer is the **full USBSTOR instance name including the `&0`
suffix**.

## Difficultés rencontrées (leçons apprises)

- **Nomenclature trompeuse** : ce que les outils appellent « serial number » n'est pas toujours le
  serial défini par le fabricant (string descriptor iSerialNumber). Ici l'instance USBSTOR
  (`RS200000000627E4&0`) et le subkey USB (`RS200000000627E4`) diffèrent par le suffixe `&0` — la
  réponse attendue était le **nom complet d'instance**, ce qui montre qu'il faut toujours
  documenter *quelle* forme d'identifiant on rapporte.
- **Cross-check systématique** : même serial retrouvé dans `USB` (VID/PID), `USBSTOR`,
  `MountedDevices` et `WPDBUSENUM` — c'est la méthode qui évite de se tromper d'appareil.
- **Il n'existait ici qu'un seul device USB de stockage** ; sur une vraie machine, plusieurs
  devices partagent VID/PID mais se distinguent par le serial — toujours filtrer sur le serial.
- Le serial n'apparaît **jamais** en clair dans le texte du Windows Search index ; il faut lire les
  hives SYSTEM/SOFTWARE bruts (avec un grep binaire `-a` par exemple).

## Ressources & mapping (SOC / ATT&CK)

- IOC hardware à blacklister → **T1091 Replication Through Removable Media**
  (<https://attack.mitre.org/techniques/T1091/>) ; corrélation avec les remontées EDR/SIEM sur la
  présence du serial sur d'autres machines.
- Article de référence sur les pièges du nommage : **The Truth About USB Device Serial Numbers**
  <https://www.sans.org/blog/the-truth-about-usb-device-serial-numbers>.
- Référentiel d'artefacts : <https://artefacts.help/windows_registry_usb_activity.html> et
  <https://forensafe.com/blogs/usbforensics.html>.