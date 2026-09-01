#!/usr/bin/env python3
"""
Inspect exactly what the server sends before we respond.
Maybe the multiplier is hidden in the banner!
"""
import socket
import time

HOST = "3-nh01.bootupctf.net"
PORT = 8229

def inspect_banner():
    """Read banner very carefully, byte by byte, with timing."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    
    t_connect = time.time()
    s.connect((HOST, PORT))
    t_after = time.time()
    
    print(f"[*] Connected at t={t_connect:.6f}")
    print(f"[*] Connection took {t_after - t_connect:.6f}s")
    
    # Read ALL data until ":" with small chunks to see everything
    full_data = b""
    s.settimeout(2)
    while True:
        try:
            chunk = s.recv(1)
            if not chunk:
                break
            full_data += chunk
            if full_data.endswith(b":") or full_data.endswith(b": "):
                # Maybe more data follows? Wait a tiny bit
                s.settimeout(0.5)
                try:
                    extra = s.recv(4096)
                    full_data += extra
                except:
                    pass
                break
        except socket.timeout:
            break

    t_read = time.time()
    print(f"[*] Banner read at t={t_read:.6f} (took {t_read-t_after:.4f}s)")
    print(f"[*] Raw bytes: {full_data}")
    print(f"[*] Hex:       {full_data.hex()}")
    print(f"[*] Decoded:   {full_data.decode(errors='replace')!r}")
    print(f"[*] Length:    {len(full_data)} bytes")
    
    # Now try sending the challenge immediately
    ts = int(time.time())
    for mult in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        challenge = str(ts * mult)
        print(f"\n[*] Sending ts*{mult} = {challenge}")
        s.sendall((challenge + "\n").encode())
        
        s.settimeout(2)
        resp = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                resp += chunk
        except:
            pass
        
        decoded = resp.decode(errors='replace').strip()
        print(f"[*] Response: {decoded!r}")
        
        if "correct" in decoded.lower() or "flag" in decoded.lower() or "boot" in decoded.lower():
            print(f"\n[+] SUCCESS with multiplier {mult}!")
            break
        
        if "Rejected" in decoded:
            if "Expected challenge:" in decoded:
                expected = int(decoded.split("Expected challenge:")[1].split()[0])
                actual_mult = expected / ts
                print(f"    Expected {expected}, ratio = {actual_mult:.4f}")
            break
    
    s.close()

def sniff_timing_of_banner():
    """
    Connect multiple times and measure if banner arrival TIME gives a hint.
    The multiplier might be encoded in HOW LONG the server takes to send the banner.
    """
    print("\n=== BANNER TIMING ANALYSIS ===")
    for i in range(5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        t0 = time.perf_counter()
        s.connect((HOST, PORT))
        t1 = time.perf_counter()
        
        data = b""
        while b":" not in data:
            data += s.recv(4096)
        t2 = time.perf_counter()
        
        print(f"  Conn {i}: connect={t1-t0:.4f}s  banner={t2-t1:.6f}s  total={t2-t0:.4f}s  data={data!r}")
        
        # Don't bother answering, just close
        s.close()
        time.sleep(0.3)

if __name__ == "__main__":
    print("=== BANNER INSPECTOR ===\n")
    inspect_banner()
    print()
    sniff_timing_of_banner()
