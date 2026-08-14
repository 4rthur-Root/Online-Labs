# ch02 — Binary to Base64

> **Category:** Crypto
> **Tooling used:** Python 3
> **Files:** `code.txt` (binary string), `decode.py` / `deocde_base.py` (helper scripts)
> **Flag:** `senEIadnenC-sx280`

## Scenario

We are given `code.txt` containing a long string of 8-bit binary tokens. The goal is to convert the binary into text, then further decode the resulting payload to recover the flag.

## Investigation

### 1. Binary → ASCII

The file contains space-separated 8-bit binary values:

```text
01111000 01101000 01010010 01101101 ...
```

Converting each token to its ASCII character yields a text string:

```python
ascii_text = ''.join(chr(int(b, 2)) for b in open('code.txt').read().split())
```

Which produces:

```text
xhRmogZz9Nc2VuRUlhZG5lbkMtc3gyODA=OT
```

### 2. Identifying the base64 payload

Scanning the string, a clearly base64-looking segment stands out, bounded by noise:

```text
...Nc2VuRUlhZG5lbkMtc3gyODA=OT
    ^^^^^^^^^^^^^^^^^^^^^^^^
```

The clean segment is `c2VuRUlhZG5lbkMtc3gyODA=` (24 chars — a valid base64 block with padding).

### 3. Base64 → flag

```python
import base64
base64.b64decode('c2VuRUlhZG5lbkMtc3gyODA=').decode()
```

Result:

```text
senEIadnenC-sx280
```

Cross-checking by re-encoding confirms the relationship is exact:

```python
base64.b64encode(b'senEIadnenC-sx280').decode() == 'c2VuRUlhZG5lbkMtc3gyODA='  # True
```

**Flag:** `senEIadnenC-sx280`

> **Note on data quality:** the original `code.txt` binary string contained surrounding noise (`xhRmogZz9Nc...OT`) that broke naive full-string base64 decoding. The flag was recovered by extracting the single clean base64 block. This should be re-verified against the original challenge if the intent was a different flag format.

## Vulnerability / Blue-team perspective

### What was actually exploitable

Nothing is *encrypted* here — the data was only **encoded**. Binary → ASCII → base64 is pure encoding: it changes representation, not confidentiality. Anyone with the file can reverse it with a single command. This is the classic "hiding in plain sight" pattern.

### How a SOC / blue team would view this

Encoding (base64, hex, URL-encoding) is ubiquitous in both legitimate traffic and malware:

- **Malware often base64-encodes payloads, C2 configs, or command lines** to evade simple string/pattern matching and to avoid on-disk plaintext detection.
- **Email gateways and web proxies see base64 blobs constantly** (MIME attachments, encoded parameters) — the encoding itself is not suspicious, the *content and context* are.

### Detection & mitigation

- **Decode-then-inspect**: a SOC workflow should include automated decoding (base64, hex, gzip) of flagged blobs before analysis — this lab's own chain is exactly that.
- **Context over encoding**: alert on encoded payloads in unexpected places (e.g. encoded PowerShell in email, encoded scripts downloaded from the web), not on encoding alone.
- **Script Block Logging / command-line logging**: capture decoded or decoded-equivalent commands so encoded payloads are seen in cleartext in the logs.
- **Baseline and filter**: legitimate use of base64 is common; use frequency and destination analysis to surface anomalies rather than blocking all encoded data.