# ch01 — XOR Obfuscated Flag

> **Category:** Crypto
> **Tooling used:** Python 3
> **Files:** `crypt.py` (encryption source, obfuscated), `transcription.py` (cleaner copy), `decrypt.py` (solver), `flag.txt` (encrypted flag)
> **Flag:** `youreadthiswell98912`

## Scenario

We are given a Python script that encrypts user input with a custom XOR-based scheme, together with the encrypted flag in `flag.txt`. The catch: the script's variable names are replaced by random Unicode characters, which is an obfuscation trick to slow down anyone trying to read the logic.

## Investigation

### 1. Recognizing the obfuscation

Opening `crypt.py` shows every identifier replaced with random Unicode characters (e.g. `𗃣ꃣ𐬗...`). After replacing them with meaningful names (`range`, `len`, `chr`, `ord`, `zip`, `print`, `input`), the logic becomes clear:

- A fixed key array is used:
  ```python
  key = [3, 19, 1337, 42, 9, 11, 56, 2, 72, 100, 81, 90, 11, 23, 84, 77, 192, 810, 999, 239, 74]
  ```
- Two fixed phrases are used as key streams:
  ```python
  phrase1 = "the quick fox jumps over the lazy dog"
  phrase2 = "lorem ipsum dolor sit amet consectetur adipiscing elit"
  ```
- For each input character `input[i]`:
  1. `char1 = phrase1[(key[i] * i) % len(phrase1)]`
  2. `char2 = phrase2[(key[i] * i) % len(phrase2)]`
  3. `xor1 = char1 XOR char2`
  4. `xor2 = xor1 XOR input[i]`
  5. Append the hex of `xor2` to the result
- The final ciphertext is **reversed** (`result[::-1]`).

### 2. Reversing the encryption

Decryption simply inverts each step in reverse order:

1. Reverse the ciphertext string.
2. Split into 2-char hex pairs and decode each to a byte.
3. Recompute `char1` and `char2` with the same key/phrases.
4. `xor1 = char1 XOR char2`, then `input_char = xor1 XOR decoded_byte` (XOR is its own inverse).

`decrypt.py` implements exactly this:

```python
encrypted_flag = "7792c3732707226742f346b62702d77747c76216"
reversed_flag = encrypted_flag[::-1]

key = [3, 19, 1337, 42, 9, 11, 56, 2, 72, 100, 81, 90, 11, 23, 84, 77, 192, 810, 999, 239, 74]
phrase1 = "the quick fox jumps over the lazy dog"
phrase2 = "lorem ipsum dolor sit amet consectetur adipiscing elit"

decoded = [binascii.unhexlify(reversed_flag[i:i+2]).decode()
           for i in range(0, len(reversed_flag), 2)]

result = ""
for i, char in enumerate(decoded):
    char1 = phrase1[(key[i] * i) % len(phrase1)]
    char2 = phrase2[(key[i] * i) % len(phrase2)]
    xor1 = chr(ord(char1) ^ ord(char2))
    input_char = chr(ord(xor1) ^ ord(char))
    result += input_char
```

### 3. Recovering the flag

```bash
$ python3 decrypt.py
Decoded hex values: ['a', '&', '|', 't', 'w', '}', ' ', 'r', 'k', 'd', '?', '$', 'v', '"', 'p', 'r', '7', '<', ')', 'w']
Decrypted flag: youreadthiswell98912
```

**Flag:** `youreadthiswell98912`

## Vulnerability / Blue-team perspective

### What was actually exploitable

The "vulnerability" here is **custom crypto**: the scheme is a XOR stream cipher built from fixed, publicly-known key material. XOR is reversible by design, and once the algorithm is understood (even through obfuscation), recovery is a mechanical exercise. Obfuscating variable names adds friction but zero real security — it is security by obscurity.

### How a SOC / blue team would view this

In the real world, the same pattern appears as:

- **Malware / scripts using XOR or custom encoders** to hide strings, C2 URLs, or payloads (e.g. a simple XOR loop over an embedded key). Detecting it requires reversing the algorithm, exactly as done here.
- **Obfuscated PowerShell/scripts** that replace identifiers or use Unicode tricks to evade signature-based detection. This is a classic AV bypass technique.

### Detection & mitigation

- **Code review and deobfuscation tooling**: normalize identifiers and reformat code (tools like `pycdc`, `de4py`, or manual renaming) before analysis.
- **Behavioral detection over signature**: a script's *behavior* (what it calls, what it connects to, what it writes) is more reliable than its appearance. Script Block Logging (PowerShell Event ID 4104) and EDR behavior rules catch obfuscated execution even when static AV is evaded.
- **Application control**: restrict script execution (AppLocker / WDAC) to block arbitrary interpreted scripts.
- **Secure design principle**: never invent crypto for protection — use vetted, standard primitives and libraries. Custom schemes are reversible, as demonstrated.
