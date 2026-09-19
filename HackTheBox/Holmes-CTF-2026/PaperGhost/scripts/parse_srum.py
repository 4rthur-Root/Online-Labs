"""Dump SRUM (SRUDB.dat) into CSV for offline review.

Produces (in analysis/):
  srum_idmap.csv        -> AppId / UserId maps (readable)
  srum_appresource.csv  -> per-app run windows (Start/End FILETIME)
  srum_netusage.csv     -> per-app network traffic (BytesSent/Recvd)
  srum_netconn.csv      -> connectivity start/end windows
"""

import csv
import sys
from pathlib import Path

from dissect.esedb import EseDB

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ANALYSIS, ARTIFACTS  # noqa: E402
from srum_blobs import parse_id_blob, pretty_app  # noqa: E402
from srum_helpers import (  # noqa: E402
    TABLE_ASR,
    TABLE_NET_CONN,
    TABLE_NET_USAGE,
    filetime,
    find_table,
)

OUT = ANALYSIS


def main(interesting_only=False):
    db = EseDB(open(ARTIFACTS["SRUDB"], "rb"))

    # --- Id map table ---
    idmap = {}

    def appname(appid):
        return idmap.get(("app", appid), f"AppId{appid}")

    def username(userid):
        return idmap.get(("sid", userid), f"User{userid}")

    t = find_table(db, "SruDbIdMapTable")
    with open(OUT / "srum_idmap.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["IdType", "IdIndex", "IdBlob"])
        for r in t.records():
            it, ii, blob = r["IdType"], r["IdIndex"], r["IdBlob"]
            tag, val = parse_id_blob(blob)
            idmap[(tag, ii)] = val
            w.writerow([it, ii, val])
    print(f"[+] srum_idmap.csv rows={len(list(t.records()))}")

    print("\nUSER SIDs:")
    for k, v in idmap.items():
        if k[0] == "sid":
            print(f"  #{k[1]} -> {v}")

    # --- AppResourceUsage ---
    interesting = []

    def tr_asr(record, names, extra):
        row = {c: record[c] for c in names}
        row["StartTime"] = filetime(row.get("EndTime") - row.get("DurationMS", 0) * 10000)
        row["EndTimeS"] = filetime(row.get("EndTime"))
        row["AppName"] = pretty_app(appname(row.get("AppId")))
        row["UserName"] = username(row.get("UserId"))
        return row

    t = find_table(db, TABLE_ASR)
    cols = [c for c in t.column_names if c not in ("StartTime", "EndTime")]
    with open(OUT / "srum_appresource.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["StartTime", "EndTimeS", "DurationMS", "AppName", "UserName"])
        for r in t.records():
            row = tr_asr(r, t.column_names, None)
            app = row["AppName"].lower()
            if interesting_only and (
                any(k in app for k in ("diogen", "desktop", "e:\\", "setup", "update", "EXT-0419", "it_support", "driver"))
            ):
                interesting.append(row)
            w.writerow(
                [row["StartTime"], row["EndTimeS"], row["DurationMS"], row["AppName"], row["UserName"]]
            )
    print(f"[+] srum_appresource.csv app-rows={len(list(find_table(db, TABLE_ASR).records()))}")

    if interesting_only:
        print("\n## 'interesting' apps (diogen/desktop/e:/setup/update):")
        for r in sorted(interesting, key=lambda x: x["StartTime"] or ""):
            print(f"  {r['StartTime']} -> {r['EndTimeS']} ({r['DurationMS']}ms) [{r['UserName']}] {r['AppName']}")

    # --- NetworkUsageByApp ---
    def tr_net(record, names, extra):
        row = {c: record[c] for c in names}
        row["TimeStampS"] = filetime(row.get("TimeStamp"))
        row["AppName"] = pretty_app(appname(row.get("AppId")))
        row["UserName"] = username(row.get("UserId"))
        return row

    t = find_table(db, TABLE_NET_USAGE)
    with open(OUT / "srum_netusage.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow([c for c in t.column_names if c != "TimeStamp"] + ["TimeStampS", "AppName", "UserName"])
        for r in t.records():
            row = tr_net(r, t.column_names, None)
            w.writerow(
                [
                    row[c]
                    for c in t.column_names
                    if c != "TimeStamp"
                ]
                + [row["TimeStampS"], row["AppName"], row["UserName"]]
            )
    print(f"[+] srum_netusage.csv rows={len(list(find_table(db, TABLE_NET_USAGE).records()))}")

    # --- NetworkConnectivity ---
    def tr_conn(record, names, extra):
        row = {c: record[c] for c in names}
        row["TimeStampS"] = filetime(row.get("TimeStamp"))
        row["StartTimeS"] = filetime(row.get("StartTime"))
        row["EndTimeS"] = filetime(row.get("EndTime"))
        row["AppName"] = pretty_app(appname(row.get("AppId")))
        row["UserName"] = username(row.get("UserId"))
        return row

    t = find_table(db, TABLE_NET_CONN)
    with open(OUT / "srum_netconn.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(
            [c for c in t.column_names if c not in ("TimeStamp", "StartTime", "EndTime")]
            + ["TimeStampS", "StartTimeS", "EndTimeS", "AppName", "UserName"]
        )
        for r in t.records():
            row = tr_conn(r, t.column_names, None)
            w.writerow(
                [row[c] for c in t.column_names if c not in ("TimeStamp", "StartTime", "EndTime")]
                + [row["TimeStampS"], row["StartTimeS"], row["EndTimeS"], row["AppName"], row["UserName"]]
            )
    print(f"[+] srum_netconn.csv rows={len(list(find_table(db, TABLE_NET_CONN).records()))}")

    print("\nDone.")


if __name__ == "__main__":
    main(interesting_only=("--interesting" in sys.argv))