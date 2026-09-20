import os

from Crypto.Cipher import AES

from emulate_kdf import derive

HDR = 60


def decrypt_file(path: str, out_dir: str) -> None:
    with open(path, "rb") as f:
        blob = f.read()
    magic = blob[:8]
    version = int.from_bytes(blob[8:12], "little")
    size = int.from_bytes(blob[12:16], "little")
    salt = blob[16:32]
    nonce = blob[32:44]
    tag = blob[44:60]
    ct = blob[HDR:]
    print(f"{path}: magic={magic!r} version={version} size_field={size} "
          f"file_len={len(blob)} ct_len={len(ct)}")
    key, pw, cap = derive(salt)
    print(f"  salt   : {salt.hex()}")
    print(f"  iter   : {cap['iter']}  dklen={cap['dklen']}  passlen={cap['passlen']}")
    print(f"  key    : {key.hex()}")
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(blob[:44])
    pt = cipher.decrypt_and_verify(ct, tag)
    print(f"  AUTH OK, plaintext {len(pt)} bytes")
    out = os.path.join(out_dir, os.path.basename(path).replace(".encrypted", ""))
    with open(out, "wb") as f:
        f.write(pt)
    print(f"  wrote  : {out}")
    print(f"  head   : {pt[:16].hex()}  {pt[:16]!r}")


if __name__ == "__main__":
    os.makedirs("analysis", exist_ok=True)
    decrypt_file("dataman.encrypted", "analysis")
    decrypt_file("flight.ulg.encrypted", "analysis")