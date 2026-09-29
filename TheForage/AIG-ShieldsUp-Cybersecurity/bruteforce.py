'''
AIG "Shields Up: Cybersecurity" - Forage job simulation
Task 2: Bypassing ransomware

Goal: recover the ransomware-encrypted `enc.zip` without paying,
by bruteforcing the ZIP password against a curated wordlist
(a subset of rockyou.txt provided by the simulation).
'''

from zipfile import ZipFile


def attempt_extract(zf, password):
    """
    Try to extract every member of the archive using `password`.

    zf.extractall(pwd=password) expects `password` as bytes, which is
    exactly what we get from reading rockyou.txt in binary mode ('rb')
    in main() below - no manual encode()/decode() needed.

    On a ZipCrypto-encrypted archive, a wrong password doesn't always
    fail cleanly: the common case is a RuntimeError("Bad password for
    file ...") raised as soon as the per-file password check fails,
    which is what this archive triggers on every wrong guess. A
    hardened version would also catch zlib.error / BadZipFile, since a
    wrong password can occasionally pass the initial check and only
    fail once the (garbage) bytes reach the decompressor - that path
    wasn't hit here, but it's worth knowing about for other archives.
    """
    try:
        zf.extractall(pwd=password)
        return True
    except RuntimeError:
        zf.close()
        return False


def main():
    print("[+] Beginning bruteforce")

    with ZipFile('enc.zip') as zf:
        with open('rockyou.txt', 'rb') as f:
            for line in f:
                password = line.strip()

                if attempt_extract(zf, password):
                    print(f"[+] Extraction successful - password: {password}")
                    break
                else:
                    print(f"[-] Extraction failed - password: {password}")
                    # A failed attempt leaves the ZipFile handle closed
                    # (attempt_extract() closes it in the except branch),
                    # so it's reopened here before the next try.
                    zf = ZipFile('enc.zip', 'r')


if __name__ == "__main__":
    main()
