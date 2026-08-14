# users-db — SQLite Flag

> **Category:** Web / Database
> **Tooling used:** Python 3 (`sqlite3`), SQL
> **Files:** `users.db` (SQLite database)
> **Flag:** `mne{sm4ll_things_b1g_consqu3nce5}`

## Scenario

We are handed a SQLite database file (`users.db`) from a web application's backend. The goal is to recover the flag and any credentials it contains.

## Investigation

### 1. Inspect the schema

```python
import sqlite3
con = sqlite3.connect('users.db')
for row in con.execute("SELECT name, sql FROM sqlite_master WHERE type='table'"):
    print(row)
```

The `users` table stands out — note the `FLAG` column:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TEXT NOT NULL,
    email TEXT,
    is_active BOOLEAN DEFAULT 1,
    role TEXT DEFAULT 'user',
    FLAG TEXT
)
```

### 2. Dump the rows

```python
for row in con.execute('SELECT id, username, password, role, FLAG FROM users'):
    print(row)
```

```text
(1, 'dev', '18a7763dbf76f40177acbfda65e84214', 'user', 'FLAG2: mne{sm4ll_things_b1g_consqu3nce5}')
(2, 'admin', '2365bfe9e7e5331dd2daf29d50bb0903', 'administrator', None)
```

The flag is stored directly in a `FLAG` column of the user table.

**Flag:** `mne{sm4ll_things_b1g_consqu3nce5}`

### 3. Bonus — the passwords are weakly hashed MD5

The `password` fields are MD5 hashes:

- `dev`   → `18a7763dbf76f40177acbfda65e84214`
- `admin` → `2365bfe9e7e5331dd2daf29d50bb0903`

A dictionary pass (`deocde_base.py`) was attempted with a small wordlist but the plaintexts were **not recovered** — the hashes likely use a salt or a stronger password. Even so, MD5 (salted or not) is a weak choice: it is trivially fast to brute-force at billions of hashes/sec with proper tooling (Hashcat/John + rockyou).

## Vulnerability / Blue-team perspective

### What was actually exploitable

The database exposes two classic weaknesses:

1. **Secrets stored in plaintext/readable form in the DB** — the flag column is unencrypted.
2. **Weak password hashing** — MD5 with no salt. MD5 is broken and bruteforceable at billions of hashes/sec; any user who ever chooses a weak password is recoverable in seconds.

In a real web app, such a database is typically reached through **SQL injection** (unparameterized queries) or **exposure of the DB file/backups**, both of which hand the attacker everything at once.

### How a SOC / blue team would view this

- **SQL injection** is consistently one of the top web vulnerabilities (OWASP Top 10) and a common initial-access vector (e.g. dumping user credentials, then password-spraying them elsewhere).
- **Stolen hash databases** from breaches are exactly how attackers build credential-stuffing lists.
- A leaked `users.db`-style artifact is a goldmine during IR: it ties usernames, roles, and secrets together in one file.

### Detection & mitigation

- **Parameterized queries / prepared statements** everywhere — the definitive SQLi fix.
- **Modern password hashing**: use Argon2/bcrypt/scrypt with a per-user salt. Never MD5/SHA1/SHA256 unsalted.
- **Least privilege & encryption**: don't store secrets (flags, tokens) in the same table as credentials; encrypt sensitive columns; restrict DB file access and backups.
- **Web application firewall (WAF) + input validation** as defense-in-depth against injection attempts.
- **Monitoring**: alert on suspicious SQL in access logs or DB queries; audit DB file/backup access (a `users.db` in the wrong place is a red flag).
- **Credential hygiene**: the dumped hashes must be assumed compromised — force resets, enable MFA, and check for password reuse across accounts.
