# Q9 — Credentials surfaced for a DIOGENES developer

## Question

Voss reviewed DIOGENES contractors NAPOLEON may now hunt. What set of credentials did the spying
surface for a developer working on DIOGENES tickets?

## Why this matters

Credential exfiltration is the usual endgame of an insider-flavored spyware campaign: the implant
captures secrets from the victim's working session and the operator pivots into the developer
accounts that manage the ticketing environment (here "DIOGENES tickets").

## Investigation steps

1. Inventory credential-bearing material in the triage:
   - the Windows Search index for indexed text bodies (`SystemIndex_PropertyStore`),
   - the `DIOGENES_Contractor_Assignments.csv` and `IT_Asset_Inventory.csv` documents present on
     the desktop copy of the delivery package (document objects in `Windows.edb`),
   - browsers, DPAPI, saved network credentials — none present in this acquisition.
2. Attempt to recover the CSV bodies from the full-text index.
3. Correlate any recovered developer identifier with the observed sessions.

## Key findings / Evidence gap

- `Windows.edb` indexes the two data files as **documents** (`DIOGENES_Contractor_Assignments.csv`,
  `IT_Asset_Inventory.csv`) and their current paths, but their **indexed bodies are empty**: no
  CSV text token (no `password`, `username`, `developer`, `contractor`, ticket IDs, etc.) can be
  extracted from the property store or the full-text index.
- The triage scope (`RegistryHives`, `LNKFilesAndJumpLists`, `SRUM`) contains **no credential
  store**: no browser profile, no DPAPI context, no saved-credentials hive.
- SRUM/OS Prefetch (not collected) could reveal which password manager executed, but not the
  secret itself.

The spying *did* surface credentials on the live system (the text of the aggregate questions
asserts it), but none of it persisted in this triage set.

## Final answer

```text
Not determinable from the provided triage artifacts.
Evidence required: the CSV file bodies (IT_Asset_Inventory.csv /
DIOGENES_Contractor_Assignments.csv), a browser profile, or C2-side captured keystrokes.
```

## Summary

The analyst must report the *known unknowns*: the file paths exist in the Windows Search index, the
bodies do not. That precise statement is more useful to the blue team than a guessed
`username:password`. The recovery path is a full disk image (to read the CSVs) or the C2 side of
the operation.

## Difficultés rencontrées (leçons apprises)

- **Corps de fichiers non indexés** : `Windows.edb` conserve les chemins (`SystemIndex_Gthr`) et un
  nombre limité de propriétés, mais pas le contenu texte des CSV (aucun token `username`/
  `password`/`developer` extractible du property store).
- **Limite du périmètre** : ni navigateur, ni DPAPI, ni registre de credentials ne sont dans le
  scope KAPE (`RegistryHives + LNK + SRUM`) — un vrai triage hétérogène manquera presque toujours
  les secrets.
- Même sur image disque complète, la récupération des secrets nécessiterait : `$MFT`/slack,
  navigateurs, ou côté C2 (keystrokes/logs). Documenter la chaîne d'acquisition requise plutôt que
  de deviner.

## Ressources & mapping (SOC / ATT&CK)

- Lecture/collection de données locales → **T1005 Data from Local System**
  (<https://attack.mitre.org/techniques/T1005/>), pivot vers comptes → **T1078 Valid Accounts**
  (<https://attack.mitre.org/techniques/T1078/>).
- Exploiter `Windows.edb` plus profondément : **WinEDB** de kacos2000
  (<https://github.com/kacos2000/WinEDB>) et **SIDR** (reporter de Stroz Friedberg, décrit dans le
  billet Aon <https://www.aon.com/cyber-solutions/aon_cyber_labs/windows-search-index-the-forensic-artifact-youve-been-searching-for>).
- DPAPI / extraction de secrets côté Windows : outils **Mimikatz/DPAPImk2john** par usage éthique en
  lab uniquement.