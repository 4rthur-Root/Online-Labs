# SANS CTF — Writeups

> **Event:** AWS Skills to Jobs CTF 2026 (SANS Institute)
> **Date:** March 2026
> **Platform:** bootupctf.net
> **Focus:** Hands-on CTF covering crypto, forensics, reverse engineering and web/DB exploitation.

## Summary

These writeups document the challenges solved during the SANS "AWS Skills to Jobs" CTF 2026. Each writeup follows the same structure: the challenge scenario, the investigation steps with the exact commands used, the recovered flag, and — from a SOC / blue-team perspective — the underlying vulnerability class and the mitigation that would have prevented or detected it.

The evidence files were salvaged from a larger, untidy archive and moved here so each writeup is self-contained (no duplicates).

## Solved challenges

| Category | Challenge | Type | Flag |
|---|---|---|---|
| Crypto | [ch01 — XOR obfuscated flag](Crypto/ch01-XOR-obfuscated-flag/README.md) | Custom XOR cipher + Unicode-obfuscated source | `youreadthiswell98912` |
| Crypto | [ch02 — binary to base64](Crypto/ch02-binary-to-base64/README.md) | Binary → ASCII → base64 decode | `senEIadnenC-sx280` |
| Forensics | [fe01 — hidden JPEG comment](Forensics/fe01-jpeg-comment/README.md) | Flag in hex-encoded EXIF comment | `s0MeTADaTa2210` |
| Forensics | [fe02 — PDF plaintext flag](Forensics/fe02-pdf-plaintext-flag/README.md) | Flag embedded in PDF text layer | `n1CeReDaCTION-sureLYNot911081` |
| Reverse | [intro04 — direct execution](Reverse/intro04-direct-execution/README.md) | ELF binary that reveals the flag on execution | `diReCt_eXecUTiOn-161799` |
| Web/DB | [users-db — SQLite flag](Web/users-db-sqli-flag/README.md) | Flag left in a SQLite user table | `mne{sm4ll_things_b1g_consqu3nce5}` |

## Recurring blue-team themes

Across these challenges, a few defensive takeaways stand out:

1. **Metadata leaks** (fe01) — documents and images silently leak data via EXIF/comments. Sanitize files before release.
2. **Plaintext secrets** (fe02, intro04) — flags hidden in plain text or printed by binaries. On real hosts, equivalent secrets often sit in cleartext configs, PDFs and scripts.
3. **Weak custom crypto** (ch01) — rolling your own XOR/key scheme is trivially reversible. Use standard, vetted algorithms.
4. **Encoding is not encryption** (ch02) — base64/hex hides data from casual review but provides zero security.
5. **Insecure DB exposure** (users-db) — database files reaching the wrong hands expose credentials and secrets; hash passwords properly and never store plaintext flags.
