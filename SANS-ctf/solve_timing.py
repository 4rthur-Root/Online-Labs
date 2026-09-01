#!/usr/bin/env python3
"""
Solver for "Its all about timings" CTF challenge.
Formula discovered: expected_challenge = unix_timestamp_at_connection * 2
"""
import socket
import time

HOST = "3-nh01.bootupctf.net"
PORT = 8229

def solve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT))

    # Read the prompt
    data = b""
    while b":" not in data:
        data += s.recv(4096)

    print(f"[Server] {data.decode().strip()}")

    # Compute the expected challenge: timestamp * 2
    # We use the timestamp RIGHT NOW (as close to connection time as possible)
    ts = int(time.time())
    challenge = str(ts * 2)
    
    print(f"[*] Sending challenge: {challenge}  (ts={ts}, ts*2={challenge})")
    s.sendall((challenge + "\n").encode())

    # Read response
    response = b""
    s.settimeout(3)
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
    except socket.timeout:
        pass

    s.close()
    print(f"[Server] {response.decode().strip()}")
    return response.decode()


def solve_with_retry(max_tries=10):
    """Try multiple times adjusting for off-by-one on timestamp."""
    for delta in [0, 1, -1, 2, -2]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((HOST, PORT))

            data = b""
            while b":" not in data:
                data += s.recv(4096)
            print(f"[Server] {data.decode().strip()}")

            ts = int(time.time()) + delta
            challenge = str(ts * 2)
            print(f"[*] Try delta={delta:+d}, challenge={challenge}")
            s.sendall((challenge + "\n").encode())

            response = b""
            s.settimeout(3)
            try:
                while True:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    response += chunk
            except socket.timeout:
                pass
            s.close()

            resp_str = response.decode().strip()
            print(f"[Server] {resp_str}\n")

            if "flag" in resp_str.lower() or "correct" in resp_str.lower() or "boot" in resp_str.lower():
                print(f"\n[+] SUCCESS! Flag: {resp_str}")
                return resp_str

            # If rejected, extract what was expected and compute multiplier
            if "Expected challenge:" in resp_str:
                expected = int(resp_str.split("Expected challenge:")[1].split()[0])
                print(f"  -> Server expected: {expected}")
                print(f"  -> expected / ts = {expected / ts:.6f}")
                print(f"  -> expected / (ts+delta) = {expected / (ts+delta):.6f}")

        except Exception as e:
            print(f"[!] Error: {e}")

        time.sleep(0.5)


if __name__ == "__main__":
    print("=== CTF Timing Solver ===\n")
    print("[*] Strategy: expected = unix_timestamp * 2\n")
    solve_with_retry()
