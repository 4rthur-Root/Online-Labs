# CTF Writeup — "Its all about timings"

> **Plateforme :** BootUpCTF  
> **Challenge :** Its all about timings  
> **Catégorie :** Network / Misc  
> **Difficulté :** Easy/Medium  
> **Flag :** `thE-END-oF_AN_ERA-1928189`

---

## 📋 Description

> Access the network service on `3-nh01.bootupctf.net` port `8229` and find a way to get the flag by presenting the correct challenge.

---

## 🔍 Phase 1 — Reconnaissance

La première chose à faire est de se connecter manuellement au service pour comprendre ce qu'il fait.

```bash
$ nc 3-nh01.bootupctf.net 8229
Enter your challenge:
```

Le serveur demande un "challenge". En envoyant des valeurs aléatoires :

```bash
$ nc 3-nh01.bootupctf.net 8229
Enter your challenge: flag
# (aucune réponse — connexion fermée)

$ nc 3-nh01.bootupctf.net 8229
Enter your challenge: flag.txt
Expected challenge: 3546820562
Rejected challenge.
```

**Observation clé :** quand on envoie quelque chose d'invalide, le serveur révèle ce qu'il attendait.

---

## 🧩 Phase 2 — Analyse du pattern

En enchaînant plusieurs connexions, on collecte les valeurs attendues :

| Connexion | Input envoyé | Expected reçu |
|-----------|-------------|----------------|
| 1 | `flag.txt` | `3546820562` |
| 2 | `3546820562` | `15960692718` |
| 3 | `15960692718` | `3546820636` |

### Recherche du pattern mathématique

```
3546820562 ÷ 2 = 1773410281  ← timestamp Unix !
3546820636 ÷ 2 = 1773410318  ← timestamp Unix 37s plus tard ✓
```

On remarque que `expected ÷ timestamp_connexion` donne toujours un **entier** (1, 2, 9, 10...).  
Le multiplicateur **change à chaque connexion** — c'est là le piège.

### Pourquoi ça échoue à la main ?

La fenêtre de validité est **la seconde courante** au moment de la connexion TCP.

```
[t=0.00s]  Connexion TCP établie  →  serveur capture le timestamp
[t=0.50s]  Banner reçu "Enter your challenge: "
[t=2-3s]   Humain tape la réponse  →  TROP TARD, la seconde a changé !
```

Un humain met minimum 2-3 secondes à répondre. La seconde Unix change toutes les... secondes. **Impossible à la main.**

---

## 💡 Phase 3 — Compréhension du mécanisme

Le serveur génère :
```
expected = timestamp_connexion × multiplicateur_aléatoire
```

Le challenge consiste à **deviner et envoyer** ce nombre dans la même seconde que la connexion.

La solution : un script qui :
1. Se connecte
2. Capture le timestamp **immédiatement**
3. Calcule `timestamp × multiplicateur` pour plusieurs multiplicateurs possibles
4. Envoie chaque candidat **sans délai**

---

## 🛠️ Phase 4 — Exploitation

### Script de reconnaissance (`inspect_banner.py`)

```python
#!/usr/bin/env python3
import socket
import time

HOST = "3-nh01.bootupctf.net"
PORT = 8229

def inspect_banner():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    
    t_connect = time.time()
    s.connect((HOST, PORT))
    
    # Lire le banner byte par byte
    full_data = b""
    s.settimeout(2)
    while True:
        try:
            chunk = s.recv(1)
            if not chunk:
                break
            full_data += chunk
            if full_data.endswith(b": "):
                break
        except socket.timeout:
            break

    print(f"Banner: {full_data!r}")
    
    # Tester tous les multiplicateurs de 1 à 10
    ts = int(time.time())
    for mult in range(1, 11):
        challenge = str(ts * mult)
        s.sendall((challenge + "\n").encode())
        
        s.settimeout(2)
        resp = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk: break
                resp += chunk
        except:
            pass
        
        decoded = resp.decode(errors='replace').strip()
        print(f"ts×{mult} = {challenge} → {decoded!r}")
        
        if "flag" in decoded.lower() or "correct" in decoded.lower():
            print(f"\n[+] FLAG: {decoded}")
            break
    
    s.close()

inspect_banner()
```

### Exécution

```bash
$ python3 inspect_banner.py
Banner: b'Enter your challenge: '
ts×1 = 1773411179 → 'Expected challenge: 1773411179\n\nFlag: thE-END-oF_AN_ERA-1928189'
[+] FLAG: Expected challenge: 1773411179

Flag: thE-END-oF_AN_ERA-1928189
```

Le multiplicateur était **×1** — autrement dit, le challenge attendu était simplement le **timestamp Unix brut** de la connexion.

---

## 🎯 Explication finale

```
expected = unix_timestamp(moment_connexion) × 1
```

Le nom du challenge **"Its all about timings"** était littéral :

- La **valeur** à envoyer est basée sur le temps (timestamp Unix)
- La **fenêtre** pour répondre est d'une seconde maximum
- Il est **physiquement impossible** pour un humain de répondre à temps à la main

C'est un exemple classique de **race condition** / **timing side-channel** : la contrainte temporelle rend la solution triviale pour un script (microsecondes de réaction) et impossible manuellement.

---

## 🏁 Flag

```
thE-END-oF_AN_ERA-1928189
```

---

## 📁 Scripts

| Fichier | Description |
|---------|-------------|
| `inspect_banner.py` | Script final d'exploitation |
| `timing_attack.py` | Script d'analyse et brute-force timing |
| `solve_timing.py` | Premier solver (analyse du multiplicateur) |

---

## 🔑 Takeaways

1. **Lire le titre** — "timings" = penser timestamp, race condition, délais réseau
2. **Collecter des données** — plusieurs connexions pour trouver le pattern mathématique
3. **Automatiser** — dès qu'une fenêtre de temps est impliquée, un script est indispensable
4. **Tester simple d'abord** — le multiplicateur ×1 (timestamp brut) était la bonne réponse
