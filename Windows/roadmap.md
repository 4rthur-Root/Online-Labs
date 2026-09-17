# 🪟 Windows SOC Analyst - Roadmap d'apprentissage

**Objectif :** Maîtriser les fondamentaux de Windows, Active Directory et l'analyse de logs pour un poste en SOC (Security Operations Center).

**Méthodologie :** Chaque semaine alterne entre cours théoriques, labs pratiques sur plateforme et tests en VM locale.

**Durée totale :** 8 semaines (rythme de 5-8h/semaine)

---

## 📅 Semaine 1 : Prise en main de Windows

| Élément | Détail |
|---------|--------|
| **Temps estimé** | 5h |
| **Objectifs** | Naviguer dans Windows, comprendre les utilisateurs, permissions, services, registre et GPO |
| **Plateformes** | TryHackMe + VM Windows locale |
| **Ressources** | - [Windows Fundamentals 1](https://tryhackme.com/room/windowsfundamentals1xbx) (THM)<br>- [Windows Fundamentals 2](https://tryhackme.com/room/windowsfundamentals2x0x) (THM)<br>- [Windows Fundamentals 3](https://tryhackme.com/room/windowsfundamentals3xzx) (THM) |

### 🔬 Activités pratiques

1. **THM Rooms :** Terminer les 3 salles Windows Fundamentals
2. **VM Locale :** 
   - Créer un utilisateur standard et un administrateur
   - Modifier une GPO locale (`gpedit.msc`)
   - Explorer le registre (`regedit`) et trouver la clé de démarrage automatique
   - Démarrer/arrêter un service (`services.msc`)

### ✅ Résultats attendus

- [ ] Badges THM "Windows Fundamentals 1, 2, 3" obtenus
- [ ] Capture d'écran de ta VM montrant :
  - La création d'un nouvel utilisateur
  - La modification d'une GPO (ex: "Désactiver l'invite de commande")
  - Une clé de registre modifiée

### 📝 Documentation à créer dans `Online-Labs`

- Créer un fichier `week1-windows-basics.md` avec :
  - Tes notes sur les concepts clés
  - Les commandes utiles (ex: `whoami /priv`, `gpupdate /force`)
  - Les screenshots des manipulations

---

## 📅 Semaine 2 : Active Directory - Concepts fondamentaux

| Élément | Détail |
|---------|--------|
| **Temps estimé** | 6h |
| **Objectifs** | Comprendre les domaines, OUs, arborescence AD, forêts, trusts |
| **Plateformes** | TryHackMe + Microsoft Learn + VM (si AD installé) |
| **Ressources** | - [Active Directory Basics](https://tryhackme.com/room/activedirectorybasics) (THM)<br>- [SC-200 : Comprendre AD](https://learn.microsoft.com/fr-fr/training/paths/security-operations-analyst/) (Microsoft Learn)<br>- [CISA - Intro to Cyber - AD section](https://www.cisa.gov/cybersecurity-awareness-program) |

### 🔬 Activités pratiques

1. **THM :** Terminer la room "Active Directory Basics"
2. **Microsoft Learn :** Suivre le module "Describe Active Directory Domain Services"
3. **VM Locale :** (si tu as un AD installé)
   - Créer une OU (Organizational Unit)
   - Créer un utilisateur dans cette OU
   - Explorer les propriétés d'un objet utilisateur

### ✅ Résultats attendus

- [ ] Badge THM "Active Directory Basics"
- [ ] Trophée Microsoft Learn pour le module AD
- [ ] Capture d'écran de ta VM montrant :
  - L'arborescence AD avec ta nouvelle OU
  - Les propriétés d'un utilisateur (attributs)

### 📝 Documentation

- Créer `week2-ad-basics.md` avec :
  - Schéma d'une forêt AD (domaines, OUs, conteneurs)
  - Liste des attributs importants d'un utilisateur (sAMAccountName, userPrincipalName, etc.)
  - Commandes AD utiles (`Get-ADUser`, `Get-ADGroup` en PowerShell)

---

## 📅 Semaine 3 : Authentification AD - Kerberos et NTLM

| Élément | Détail |
|---------|--------|
| **Temps estimé** | 7h |
| **Objectifs** | Maîtriser les protocoles d'authentification Kerberos et NTLM, comprendre leurs vulnérabilités |
| **Plateformes** | Microsoft Learn + THM + VM |
| **Ressources** | - [SC-200 : Authentication](https://learn.microsoft.com/fr-fr/training/paths/security-operations-analyst/)<br>- [Kerberos explained (vidéo)](https://www.youtube.com/watch?v=5N242XcKAsM)<br>- [NTLM vs Kerberos](https://activedirectorypro.com/kerberos-vs-ntlm/) |

### 🔬 Activités pratiques

1. **Microsoft Learn :** Module "Understand authentication in AD"
2. **THM :** Room "Kerberos Basics" (si disponible)
3. **VM Locale :**
   - Analyser un ticket Kerberos avec `klist`
   - Configurer un service pour utiliser NTLM (désactiver Kerberos)
   - Observer les événements d'authentification dans le Security log

### ✅ Résultats attendus

- [ ] Compréhension écrite des différences Kerberos/NTLM
- [ ] Capture d'écran du Security log montrant :
  - Un Event ID 4624 (Logon réussi) avec le package d'authentification (Kerberos ou NTLM)
- [ ] Schéma du flux Kerberos (AS-REQ, AS-REP, TGS-REQ, TGS-REP)

### 📝 Documentation

- Créer `week3-kerberos-ntlm.md` avec :
  - Diagramme du flux Kerberos
  - Tableau comparatif Kerberos vs NTLM
  - Liste des attaques connues (Pass-the-Ticket, Pass-the-Hash, Golden Ticket)

---

## 📅 Semaine 4 : Réplication AD, Trusts et DCSync

| Élément | Détail |
|---------|--------|
| **Temps estimé** | 6h |
| **Objectifs** | Comprendre la réplication AD, les trusts entre domaines, et l'attaque DCSync |
| **Plateformes** | THM + Microsoft Learn |
| **Ressources** | - [AD Replication](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/active-directory-replication-concepts)<br>- [THM : Attacktive Directory](https://tryhackme.com/room/attacktivedirectory) (salle avancée) |

### 🔬 Activités pratiques

1. **THM :** Commencer la room "Attacktive Directory" (juste la partie réplication)
2. **Microsoft Learn :** Lire sur la réplication et les trusts
3. **VM Locale :**
   - Simuler un DCSync avec Mimikatz (dans ton lab contrôlé, **uniquement**)
   - Observer les événements 4662 (accès à un objet AD) générés

### ✅ Résultats attendus

- [ ] Capture d'écran montrant une tentative DCSync dans les logs (Event ID 4662)
- [ ] Compréhension de ce qu'est un trust et des différents types (bidirectionnel, sortant, entrant)
- [ ] Schéma des flux de réplication AD

### 📝 Documentation

- Créer `week4-replication-dcsync.md` avec :
  - Explication de la réplication multimaster
  - Qu'est-ce que DCSync et comment le détecter
  - Les Event IDs à surveiller (4662, 4768, 4776)

---

## 📅 Semaine 5 : Event Logs Windows - Les fondamentaux

| Élément | Détail |
|---------|--------|
| **Temps estimé** | 7h |
| **Objectifs** | Maîtriser les Event IDs critiques : 4624, 4625, 4688, 4720, 4732, 4648, 1102 |
| **Plateformes** | THM + VM |
| **Ressources** | - [Windows Logging for SOC](https://tryhackme.com/room/windowsloggingforsecurityoperation) (THM)<br>- [Ultimate Windows Event IDs list](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/) |

### 🔬 Activités pratiques

1. **THM :** Terminer la room "Windows Logging for SOC"
2. **VM Locale :**
   - Se connecter/déconnecter et observer les Event IDs 4624/4625
   - Lancer un processus (notepad) et observer le 4688 (si Process Auditing activé)
   - Créer un utilisateur : Event 4720
   - Ajouter un utilisateur à un groupe : Event 4732
   - Effacer les logs : Event 1102

### ✅ Résultats attendus

- [ ] Badge THM "Windows Logging for SOC"
- [ ] Tableau récapitulatif des Event IDs (à inclure dans ta doc)
- [ ] Capture d'écran de l'Event Viewer filtré avec ces IDs

### 📝 Documentation

- Créer `week5-event-ids.md` avec :
  - Tableau complet des Event IDs vus (numéro, description, importance)
  - Exemple de logs pour chaque ID (texte)
  - Comment configurer l'audit des processus (`gpedit.msc` > Security Settings > Audit Policy)

---

## 📅 Semaine 6 : Sysmon et PowerShell Logging (4104)

| Élément | Détail |
|---------|--------|
| **Temps estimé** | 7h |
| **Objectifs** | Installer/configurer Sysmon, analyser ses logs, comprendre PowerShell logging (Event 4104) |
| **Plateformes** | THM + VM |
| **Ressources** | - [Sysmon Room](https://tryhackme.com/room/sysmon) (THM)<br>- [Sysmon configuration file (SwiftOnSecurity)](https://github.com/SwiftOnSecurity/sysmon-config) |

### 🔬 Activités pratiques

1. **THM :** Terminer la room "Sysmon"
2. **VM Locale :**
   - Installer Sysmon avec la config SwiftOnSecurity
   - Exécuter une commande PowerShell (ex: `Get-Process`) et observer Event 4104 (script block logging)
   - Lancer un processus suspect (ex: `certutil -urlcache`) et voir comment Sysmon le capture (Event 1)
   - Observer les connexions réseau (Event 3)

### ✅ Résultats attendus

- [ ] Badge THM "Sysmon"
- [ ] Capture d'écran de l'Event Viewer avec les événements Sysmon (Event ID 1, 3, 7)
- [ ] Capture d'écran d'un Event 4104 (PowerShell)

### 📝 Documentation

- Créer `week6-sysmon-powershell.md` avec :
  - Commande d'installation de Sysmon
  - Explication des événements Sysmon (1=Process, 3=Network, 7=Image Loaded)
  - Comment activer le script block logging PowerShell (`Set-PSRepository`)
  - Exemple de requête KQL pour rechercher du PowerShell suspect

---

## 📅 Semaine 7 : Attack Paths et BloodHound

| Élément | Détail |
|---------|--------|
| **Temps estimé** | 8h |
| **Objectifs** | Cartographier les chemins d'attaque AD avec BloodHound, comprendre les déléguations |
| **Plateformes** | THM + VM |
| **Ressources** | - [Attacktive Directory](https://tryhackme.com/room/attacktivedirectory) (THM)<br>- [BloodHound Basics - SpecterOps](https://training.specterops.io/) (cours gratuit)<br>- [John Hammond BloodHound tutorial](https://www.youtube.com/watch?v=Y3qTX0dNg8A) |

### 🔬 Activités pratiques

1. **THM :** Terminer la room "Attacktive Directory"
2. **VM Locale :**
   - Lancer SharpHound sur ta machine (collecte de données)
   - Importer les données dans BloodHound
   - Trouver le chemin le plus court pour devenir Domain Admin
   - Identifier une déléguation (ex: un utilisateur peut ajouter des membres à un groupe)

### ✅ Résultats attendus

- [ ] Badge THM "Attacktive Directory"
- [ ] Capture d'écran de BloodHound montrant :
  - Un chemin d'attaque (ex: User1 -> Group1 -> DA)
  - Une déléguation dangereuse
- [ ] Liste des 5 chemins d'attaque les plus courants dans AD

### 📝 Documentation

- Créer `week7-bloodhound.md` avec :
  - Comment installer SharpHound et BloodHound
  - Les types de relations dans BloodHound (MemberOf, AdminTo, etc.)
  - Exemple d'une déléguation à surveiller
  - Comment interpréter un graphique BloodHound

---

## 📅 Semaine 8 : Synthèse - Projet pratique de Hunting

| Élément | Détail |
|---------|--------|
| **Temps estimé** | 8h |
| **Objectifs** | Mettre en œuvre toutes les compétences dans un scénario de chasse aux menaces |
| **Plateformes** | THM + VM |
| **Ressources** | - [Active Directory Hardening](https://tryhackme.com/room/activedirectoryhardening) (THM)<br>- [Investigating Windows](https://tryhackme.com/room/investigatingwindows2) (THM) |

### 🔬 Activités pratiques

1. **THM :** Terminer les rooms "Active Directory Hardening" et "Investigating Windows"
2. **VM Locale :**
   - Simuler une attaque (DCSync, Pass-the-Hash)
   - Mettre en place des règles de détection (ex: dans un SIEM)
   - Analyser les logs pour retrouver la source
   - Écrire un rapport d'investigation

### ✅ Résultats attendus

- [ ] Badges THM des deux rooms
- [ ] Rapport d'investigation (1 page) d'un incident simulé contenant :
  - Chronologie des événements
  - Event IDs identifiés
  - Recommandations de durcissement
- [ ] Règle de détection créée (ex: pour Sigma)

### 📝 Documentation

- Créer `week8-final-project.md` avec :
  - Le scénario d'attaque
  - Les logs collectés
  - Les requêtes de recherche
  - Les recommandations de sécurité

---

## 📊 Synthèse des Preuves de Complétion

| Semaine | Plateforme | Preuve obtenue |
|---------|------------|----------------|
| 1 | THM | 3 badges "Windows Fundamentals" |
| 2 | THM + Microsoft Learn | Badge "AD Basics" + Trophée |
| 3 | Microsoft Learn | Trophée |
| 4 | THM | Badge "Attacktive Directory" (partiel) |
| 5 | THM | Badge "Windows Logging for SOC" |
| 6 | THM | Badge "Sysmon" |
| 7 | THM | Badge "Attacktive Directory" (complet) |
| 8 | THM | 2 badges ("Hardening" & "Investigating") |

---

## 🧰 Outils et Liens Utiles

### Outils à installer sur ta VM

| Outil | Utilité | Lien |
|-------|---------|------|
| Sysmon | Logging avancé | [Download](https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon) |
| BloodHound | Cartographie AD | [Download](https://github.com/BloodHoundAD/BloodHound) |
| ProcMon | Analyse processus | [Download](https://docs.microsoft.com/en-us/sysinternals/downloads/procmon) |
| Process Explorer | Analyse processus | [Download](https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer) |

### Cheat Sheets à garder

- **Event IDs essentiels :**
  - `4624` = Logon réussi
  - `4625` = Logon échoué
  - `4688` = Création de processus
  - `4720` = Création d'utilisateur
  - `4732` = Ajout à un groupe
  - `4768` = Ticket Kerberos (TGT)
  - `1102` = Logs effacés

- **Commandes PowerShell utiles :**
  ```powershell
  # Obtenir les utilisateurs AD
  Get-ADUser -Filter * -Properties *

  # Obtenir les groupes
  Get-ADGroup -Filter *

  # Voir les logs de sécurité
  Get-WinEvent -LogName Security -MaxEvents 10

  # Voir les logs Sysmon
  Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 10

🎯 Critères de validation finale
À la fin des 8 semaines, tu dois être capable de :

[] Naviguer dans Windows et AD sans aide
[] Identifier 15 Event IDs critiques
[] Installer et configurer Sysmon
[] Lire un log PowerShell (Event 4104)
[] Utiliser BloodHound pour trouver un chemin d'attaque
[] Rédiger un rapport d'investigation
[] Expliquer Kerberos vs NTLM
[] Détecter un DCSync
