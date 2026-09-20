import struct

import sys

SECTOR = 60
HDR = 4
PAY = 56


def parse_item(payload):
    lat, lon = struct.unpack_from("<dd", payload, 0)
    params = struct.unpack_from("<7f", payload, 16)
    nav_cmd, do_jump_idx, do_jump_repeat, do_jump_current = struct.unpack_from(
        "<HHHH", payload, 44)
    bits = struct.unpack_from("<H", payload, 52)[0]
    frame = bits & 0xF
    origin = (bits >> 4) & 0x7
    loiter_exit_xtrack = (bits >> 7) & 1
    force_heading = (bits >> 8) & 1
    alt_rel = (bits >> 9) & 1
    autocontinue = (bits >> 10) & 1
    vtol = (bits >> 11) & 1
    return dict(lat=lat, lon=lon, params=params, nav_cmd=nav_cmd,
               do_jump_idx=do_jump_idx, do_jump_repeat=do_jump_repeat,
               do_jump_current=do_jump_current, frame=frame, origin=origin,
               alt_rel=alt_rel, autocontinue=autocontinue)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "analysis/dataman"
    bank = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    d = open(path, "rb").read()
    base = 0x2118 + bank * 10000 * SECTOR
    for i in range(n):
        off = base + i * SECTOR
        hdr = d[off:off + HDR]
        payload = d[off + HDR:off + HDR + PAY]
        if bytes(payload) == bytes(PAY):
            print(f"item {i:2d} @0x{off:06x} header={hdr.hex()}  EMPTY")
            continue
        it = parse_item(payload)
        print(f"item {i:2d} @0x{off:06x} header={hdr.hex()}"
              f" cmd={it['nav_cmd']:5d} frame={it['frame']} origin={it['origin']}"
              f" la={it['lat']:.7f} lo={it['lon']:.7f} params={['%g' % p for p in it['params']]}"
              f" jump({it['do_jump_idx']},{it['do_jump_repeat']},{it['do_jump_current']})"
              f" altrel={it['alt_rel']} auto={it['autocontinue']}")
        print(f"      raw: {payload.hex(' ')}")


if __name__ == "__main__":
    main()