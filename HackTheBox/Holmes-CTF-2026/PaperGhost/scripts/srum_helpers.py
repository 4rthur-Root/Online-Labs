"""Shared helpers for SRUM / ESEDB dumps."""

from datetime import datetime, timedelta, timezone

EPOCH_1601 = datetime(1601, 1, 1, tzinfo=timezone.utc)

TABLE_ASR = "{5C8CF1C7-7257-4F13-B223-970EF5939312}"
TABLE_NET_USAGE = "{973F5D5C-1D90-4944-BE8E-24B94231A174}"
TABLE_NET_CONN = "{7ACBBAA3-D029-4BE4-9A7A-0885927F1D8F}"
TABLE_TIMELINE = "{DD6636C4-8929-4683-974E-22C046A43763}"


def filetime(ft):
    """Convert a Windows FILETIME (100ns since 1601-01-01) to UTC str or None."""
    if not ft:
        return None
    try:
        return (EPOCH_1601 + timedelta(microseconds=ft / 10)).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3]
    except Exception:
        return None


def decode_blob(x):
    """Best-effort decode of an SRUM IdBlob (UTF-16 path or SID etc.)."""
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    if isinstance(x, bytes):
        for enc in ("utf-16-le", "utf-8"):
            try:
                s = x.decode(enc)
            except Exception:
                continue
            if all(
                c
                in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ._\\:/@#-()+%&^=;!,{}\'[]*"
                for c in s
            ):
                return s
        return x.hex()
    return str(x)


def find_table(db, name):
    for t in db.tables():
        if t.name == name:
            return t
    return None


def utc(epoch_ts):
    pass