import json
import sys

from pyulog import ULog

WAIT = -1
FLAT_KEYS = ["timestamp"]


def rows(ds):
    data = ds.data
    if isinstance(data, dict):
        n = len(next(iter(data.values())))
        fields = list(data.keys())
        for i in range(n):
            yield {f: data[f][i] for f in fields}
    else:
        yield from data


def dump(name, ulog_list, limit=None, fmt=lambda r: r):
    out = []
    for ds in ulog_list:
        if ds.name != name:
            continue
        for r in rows(ds):
            out.append(r)
    out.sort(key=lambda r: r["timestamp"])
    if limit:
        out = out[:limit]
    for r in out:
        print(name, fmt(r))


if __name__ == "__main__":
    ul = ULog(sys.argv[1] if len(sys.argv) > 1 else "analysis/flight.ulg")
    for topic in sys.argv[2:]:
        print("#####", topic)
        dump(topic, ul.data_list, limit=None)