# fe01 — Hidden JPEG Comment

> **Category:** Forensics
> **Tooling used:** `file`, `strings`, `exiftool`, Python
> **Files:** `image.jpg`
> **Flag:** `s0MeTADaTa2210`

## Scenario

We receive a single JPEG image (`image.jpg`, 480×360). The flag is hidden somewhere in the file — a classic metadata/steganography forensics task.

## Investigation

### 1. Confirm the file type

```bash
$ file fe01/image.jpg
fe01/image.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1,
segment length 16, comment: "466c61673a73304d6554416461546132323130", baseline, precision 8, 480x360
```

The `file` output alone reveals the lead: the JPEG carries a **comment segment** whose content is a hex string:

```text
466c61673a73304d6554416461546132323130
```

### 2. Decode the hex comment

```bash
$ python3 -c "print(bytes.fromhex('466c61673a73304d6554416461546132323130').decode())"
Flag:s0MeTADaTa2210
```

Decoding the hex bytes gives the flag in cleartext.

**Flag:** `s0MeTADaTa2210`

## Vulnerability / Blue-team perspective

### What was actually exploitable

The image leaks sensitive information through **metadata** — in this case a JPEG comment field. On real-world systems, exactly this kind of leak happens constantly: documents and images carry author names, GPS coordinates, software versions, and organizational strings in EXIF/IPTC/XMP metadata, and are shared externally without sanitization.

### How a SOC / blue team would view this

Metadata leakage is an **information-disclosure** issue that supports reconnaissance:

- An attacker in an OSINT pass can harvest internal usernames, usernames in `Author` fields, GPS locations of employees/offices, printer names, or software versions to tailor phishing and lateral movement.
- Regulatory and confidentiality requirements (e.g. PII protection) can be violated by sharing metadata unintentionally.

### Detection & mitigation

- **Metadata sanitization before release**: strip EXIF/metadata from any file leaving the organization. Linux: `exiftool -all= file.jpg`. Windows: File Explorer → Properties → Details → Remove Properties.
- **DPI/Data Loss Prevention (DLP)**: DLP rules can flag or strip metadata on email attachments and uploads.
- **Policy and awareness**: educate users that images and office documents carry hidden fields; enforce sanitization in release workflows and document templates.
- **During IR**: always inspect metadata (EXIF, comments, document properties) — it is a fast, high-value evidence source, exactly as used here.
