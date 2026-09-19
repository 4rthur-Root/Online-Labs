# Q3 — Full path of the payload hidden in the fake update package

## Question

VON BORK's payload hid inside a fake update package Elias delivered. What is the full path of the
payload? (full path of file, starting with drive letter)

## Why this matters

Mapping the malformed "update" to its exact location on disk is what turns a USB delivery into an
attribution trail: which drive letter, which folder name, which file. SRUM (AppResourceUsage /
NetworkUsage) records the full application path for every executable that ran, and the Windows
Search index captures the same file objects the moment the removable volume is crawled.

## Investigation steps

1. Parse `SRUDB.dat` and dump the `SruDbIdMapTable` — SRUM stores a numeric `AppId` per binary.
2. Look for an entry under the removable volume `HarddiskVolume5` with an `update` theme.
3. Confirm the leaf name and location in the Windows Search index (`Windows.edb`,
   `SystemIndex_Gthr` + `SystemIndex_GthrPth`), which stores both the C: desktop copy and the E:
   drive objects.

## Key findings

SRUM idmap entries:

```
#436 : \device\harddiskvolume5\co-lt-0469 update package\update.exe
#438 : \Device\HarddiskVolume5\CO-LT-0469 update package\update.exe  (canonical casing)
```

`HarddiskVolume5` is the volume GUID that `MountedDevices` binds to the Lexar USB (`E:`).
`Windows.edb` independently confirms the object on the E: volume:

```
file:E:/CO-LT-0469 update package/update.exe      Kind=program
```

The `E:` scope is the volume GUID `{43cec11d-65ac-4ce1-90d0-4851dfc7a806}`, i.e. the Lexar drive.

## Final answer

```text
E:\CO-LT-0469 update package\update.exe
```

## Summary

Two independent sources (SRUM idmap + Windows Search index) point at the same object: a file named
`update.exe` sitting in a folder literally called "CO-LT-0469 update package" on the target's own
hostname — the social-engineering disguise used to make an unknown executable look like an
approved IT update for `CO-LT-0469`.

## Difficultés rencontrées (leçons apprises)

- **Idmap SRUM dupliqué** : `#436` et `#438` stockent le même chemin avec une casse différente
  (`\device\...` vs `\Device\...`) — SRUM crée une entrée par forme rencontrée. Ne pas supposer
  qu'une seule entrée existe ; dédupliquer en normalisant la casse.
- **Résolution volume → lettre** : `HarddiskVolume5` n'est pas un fichier attendu ; il faut passer
  par `MountedDevices` (`\??\Volume{GUID}\`→`E:`) pour joindre le chemin "device" au chemin
  lisible par l'utilisateur.
- **GUID ≠ lettre de lecteur** : dans `Windows.edb`, la racine de volume est référencée par une
  somme GUID (`{43cec11d-...}` pour E:), pas par une lettre — établir la correspondance avant
  d'interpréter les URLs `file:E:/...`.
- Le challenge attend le chemin **avec la lettre de lecteur** (`E:\...`) — toujours rendre le
  résultat dans la forme attendue (drive letter full path).

## Ressources & mapping (SOC / ATT&CK)

- Chaîne complète livraison→exécution → **T1091 Replication Through Removable Media** puis
  **T1204.002 User Execution: Malicious File** (<https://attack.mitre.org/techniques/T1204/002/>).
- SRUM idmap : documentation et usage de **SrumECmd**
  <https://github.com/EricZimmerman/Srum>.
- Windows.edb / spec du schéma Windows Search : **libyal esedb-kb**
  <https://github.com/libyal/esedb-kb/blob/main/documentation/Windows%20Search.asciidoc>.