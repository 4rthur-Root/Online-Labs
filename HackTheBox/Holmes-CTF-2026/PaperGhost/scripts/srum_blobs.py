"""Convert SRUM binary SIDs and app-id blobs to readable strings."""

import struct


APP_TAG = "app"
SID_TAG = "sid"


def parse_id_blob(raw):
    """Parse a SRUM SruDbIdMapTable IdBlob.

    Returns (tag, value) where tag is 'app' or 'sid'.
    """
    if raw is None:
        return (None, None)
    if isinstance(raw, str):
        return (APP_TAG, raw)

    try:
        # --- SID structure ---
        if len(raw) >= 8 and raw[0] == 1:  # SID revision in first byte + ""
            rev = raw[0]
            subauth_count = raw[1]
            if len(raw) >= (8 + 4 * subauth_count):
                authority = int.from_bytes(raw[2:8], "big")
                subs = [
                    int.from_bytes(raw[8 + 4 * i : 12 + 4 * i], "little")
                    for i in range(subauth_count)
                ]
                return (
                    SID_TAG,
                    "S-" + "-".join([str(rev), str(authority)] + [str(s) for s in subs]),
                )
    except Exception:
        pass

    # --- AppId / path (UTF-16 prefixed with type/format marker) ---
    # Typical shape: 0x21 0x00 0x21 0x00 + utf16-le text
    data = raw
    if data[:4] in (b"\x21\x00\x21\x00", b"\x21\x00\x00\x00"):
        data = raw[4:]
    for enc in ("utf-16-le", "utf-8"):
        try:
            s = data.decode(enc).rstrip("\x00")
            if s and all(
                c.isprintable() or c in "\t\n" for c in s
            ):
                return (APP_TAG, s)
        except Exception:
            continue
    return (APP_TAG, raw.hex())


def pretty_app(app):
    """Strip the !metadata suffix from an app string: 'path!date!hash![tag]'."""
    if not app:
        return app
    if "!" not in app:
        return app
    return app.split("!")[0]