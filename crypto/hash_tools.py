#!/usr/bin/env python3
"""Hashes: identificar, gerar, quebrar por wordlist.
    python3 hash_tools.py id 5f4dcc3b5aa765d61d8327deb882cf99
    python3 hash_tools.py gen "senha"
    python3 hash_tools.py crack HASH /usr/share/wordlists/rockyou.txt [md5|sha1|sha256]
    python3 hash_tools.py hmac KEY MSG
Online: crackstation.net, hashes.com | offline: hashcat, john (veja links.md)
"""
import sys, hashlib, hmac as _hmac

LEN = {32: "MD5 / NTLM", 40: "SHA-1", 56: "SHA-224", 64: "SHA-256", 96: "SHA-384", 128: "SHA-512"}

def identify(h):
    h = h.strip()
    for pre, name in (("$2", "bcrypt"), ("$1$", "MD5-crypt"), ("$5$", "SHA256-crypt"),
                      ("$6$", "SHA512-crypt"), ("$argon2", "argon2")):
        if h.startswith(pre): return name
    return LEN.get(len(h), "desconhecido")

def gen(s):
    for a in ("md5", "sha1", "sha256", "sha512"):
        print(f"{a:7}", hashlib.new(a, s.encode()).hexdigest())

def crack(h, wl, algo=None):
    algo = algo or {32: "md5", 40: "sha1", 64: "sha256", 128: "sha512"}.get(len(h))
    with open(wl, errors="ignore") as f:
        for line in f:
            w = line.rstrip("\n")
            if hashlib.new(algo, w.encode()).hexdigest() == h.lower():
                return w
    return None

if __name__ == "__main__":
    if len(sys.argv) < 3: print(__doc__); sys.exit()
    c = sys.argv[1]
    if c == "id": print(identify(sys.argv[2]))
    elif c == "gen": gen(sys.argv[2])
    elif c == "crack": print(crack(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None) or "não encontrado")
    elif c == "hmac": print(_hmac.new(sys.argv[2].encode(), sys.argv[3].encode(), "sha256").hexdigest())
