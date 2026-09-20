import hashlib
import sys

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_PROT_ALL, UC_HOOK_CODE
from unicorn.x86_const import (UC_X86_REG_RDI, UC_X86_REG_RSI, UC_X86_REG_RDX, UC_X86_REG_RCX, UC_X86_REG_R8, UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_RAX)

PX4 = "px4"
KDF = 0x170AF0
CALL_CLEANSE = 0x170CFF
CALL_SHA256 = 0x170D50
CALL_PBKDF2 = 0x170D74
TEXT_END = 0x8ED698
RW_OFF = 0x8EDEC0
RW_VA = 0x8EEEC0
RW_SIZE = 0x7F648

SALT_ADDR = 0x7000000
OUT_ADDR = 0x7000010
STACK_BASE = 0x2000000 + 0x20000

captured = {}


def build_uc(salt: bytes) -> Uc:
    data = open(PX4, "rb").read()
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    tsize = (TEXT_END + 0xFFF) & ~0xFFF
    uc.mem_map(0, tsize, UC_PROT_ALL)
    uc.mem_write(0, data[:TEXT_END])
    rw = (RW_SIZE + 0xFFF + 1) & ~0xFFF
    uc.mem_map(RW_VA & ~0xFFF, rw, UC_PROT_ALL)
    uc.mem_write(RW_VA, data[RW_OFF: RW_OFF + RW_SIZE])
    uc.mem_map(0x7000000, 0x10000, UC_PROT_ALL)
    uc.mem_write(SALT_ADDR, salt)
    uc.mem_map(STACK_BASE - 0x4000, 0x10000, UC_PROT_ALL)
    uc.reg_write(UC_X86_REG_RDI, SALT_ADDR)
    uc.reg_write(UC_X86_REG_RSI, OUT_ADDR)
    uc.reg_write(UC_X86_REG_RSP, STACK_BASE)
    return uc


def hook(uc, address, size, user_data):
    if address == CALL_CLEANSE:
        n = uc.reg_read(UC_X86_REG_RSI)
        p = uc.reg_read(UC_X86_REG_RDI)
        uc.mem_write(p, b"\x00" * n)
        uc.reg_write(UC_X86_REG_RIP, 0x170D04)
    elif address == CALL_SHA256:
        uc.reg_write(UC_X86_REG_RAX, 1)
        uc.reg_write(UC_X86_REG_RIP, 0x170D55)
    elif address == CALL_PBKDF2:
        captured["pass"] = uc.mem_read(uc.reg_read(UC_X86_REG_RDI), uc.reg_read(UC_X86_REG_RSI))
        captured["salt"] = uc.mem_read(uc.reg_read(UC_X86_REG_RDX), uc.reg_read(UC_X86_REG_RCX))
        captured["iter"] = uc.reg_read(UC_X86_REG_R8)
        captured["dklen"] = int.from_bytes(uc.mem_read(uc.reg_read(UC_X86_REG_RSP), 8), "little")
        captured["passlen"] = uc.reg_read(UC_X86_REG_RSI)
        uc.emu_stop()


def derive(salt: bytes) -> bytes:
    uc = build_uc(salt)
    uc.hook_add(UC_HOOK_CODE, hook)
    uc.emu_start(KDF, 0x170D79)
    pw = captured["pass"]
    if len(pw) != captured["passlen"]:
        pw = pw[:captured["passlen"]]
    key = hashlib.pbkdf2_hmac("sha256", pw, captured["salt"], captured["iter"], dklen=captured["dklen"])
    return key, pw, captured


if __name__ == "__main__":
    salt_hex = sys.argv[1] if len(sys.argv) > 1 else None
    if salt_hex is None:
        salt = bytes.fromhex(open(sys.argv[2] if len(sys.argv) > 2 else "", "rb").read(16).hex())
    else:
        salt = bytes.fromhex(salt_hex)
    key, pw, cap = derive(salt)
    print("PBKDF2 args at call site:")
    print("  passlen :", cap["passlen"])
    print("  pass[:16] hex :", pw[:16].hex())
    print("  salt hex:", cap["salt"].hex())
    print("  iter   :", cap["iter"])
    print("  dklen  :", cap["dklen"])
    print("AES-256 key:", key.hex())