# intro04 — Direct Execution

> **Category:** Reverse Engineering
> **Tooling used:** `file`, `strings`, execution in a sandboxed environment
> **Files:** `program` (ELF 64-bit)
> **Flag:** `diReCt_eXecUTiOn-161799`

## Scenario

We receive a 64-bit Linux ELF executable. The goal is to recover the flag from the binary — this one is the "easy/intro" tier of the reverse category.

## Investigation

### 1. Confirm the binary type

```bash
$ file program
program: ELF 64-bit LSB pie executable, x86-64, dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,
BuildID[sha1]=2b48b0d11c0bc8c9841db7c1d93a95375085984f, for GNU/Linux 3.2.0, not stripped
```

Notes: a standard PIE executable, **not stripped** — meaning symbol names survive, which makes analysis far easier.

### 2. Static peek with `strings`

```bash
$ strings program | grep -i flag
Flag: diReCt_eXecUTiOn-161799
```

The flag string is embedded directly in the binary's read-only data.

### 3. Confirmation by execution (in a sandbox/VM)

```bash
$ ./program
Flag: diReCt_eXecUTiOn-161799
```

The program simply prints the flag — no input handling, no checks. It is a straight "run it and read the output" challenge.

**Flag:** `diReCt_eXecUTiOn-161799`

## Vulnerability / Blue-team perspective

### What was actually exploitable

Hardcoded secrets stored in **plaintext inside a binary**. The flag sits in the `.rodata`/data segment and is trivially readable via `strings`. In the real world this is exactly how malware and legitimate software leak credentials, API keys, hardcoded passwords, or C2 endpoints.

### How a SOC / blue team would view this

During malware triage and reverse engineering:

- **`strings` on a suspicious binary is a mandatory first step** — C2 URLs, bot tokens, embedded keys, and unique strings are usually recoverable in minutes.
- **Hardcoded secrets in shipped binaries** are a real finding for blue teams (e.g. hardcoded AWS keys in a mobile app or agent) and are catalogued in leak databases when found.

### Detection & mitigation

- **Sandboxed execution**: always run unknown binaries in a VM/container with network isolation (this lab's own run was done safely). Dynamic analysis reveals behavior static review can miss.
- **Automated triage**: feed binary artifacts to malware-analysis pipelines (e.g. Cuckoo/CAPE, VirusTotal) that automatically extract strings, imports, and IOCs.
- **Secret hygiene in development**: forbid hardcoded secrets in code; use vaults, key management, and config injection. Add secret scanners to CI/CD to catch them before release.
- **For IR**: the strings embedded in a binary (paths, internal IPs, usernames) are also rich threat-intel pivots.
