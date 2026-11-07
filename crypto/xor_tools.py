#!/usr/bin/env python3
"""XOR: chave de 1 byte (brute), chave repetida (quebra), known-plaintext.
    python3 xor_tools.py single HEXSTRING            # testa 256 chaves
    python3 xor_tools.py key HEXSTRING flag{         # recupera chave por texto conhecido
    python3 xor_tools.py repeat HEXSTRING            # estima tamanho de chave e quebra
    python3 xor_tools.py dec HEXSTRING KEYTEXT       # decifra com chave
"""
import sys, string

def xor(data, key):
    if isinstance(key, int): key = bytes([key])
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def score(b):
    ok = string.ascii_letters + string.digits + " _{}-.,!?:'\n"
    good = sum(chr(c) in ok for c in b)
    return good + 3 * b.count(b"flag") - 5 * sum(c < 9 or c > 126 for c in b)

def single_brute(data, top=5):
    res = sorted(((score(xor(data, k)), k, xor(data, k)) for k in range(256)), reverse=True)[:top]
    for s, k, pt in res:
        print(f"key=0x{k:02x} ({chr(k)!r}) score={s}: {pt[:80]}")

def known_plain(data, known):
    key = xor(data[:len(known)], known)
    print("início da chave:", key, key.hex())

def hamming(a, b): return sum(bin(x ^ y).count("1") for x, y in zip(a, b))

def guess_keylen(data, maxk=40):
    """distância de Hamming normalizada média entre blocos consecutivos; menor = mais provável."""
    sc = []
    for k in range(2, min(maxk, len(data) // 3)):
        n = len(data) // k - 1
        d = sum(hamming(data[i*k:(i+1)*k], data[(i+1)*k:(i+2)*k]) for i in range(n)) / (n * k)
        sc.append((d, k))
    sc.sort()
    best = sc[0][0]
    # prefere o menor k cuja nota está perto da melhor (evita múltiplos da chave real)
    cands = sorted(k for d, k in sc if d <= best * 1.06)
    return cands[:3]

def repeat_break(data):
    cands = set()
    for k in guess_keylen(data):
        cands |= {d for d in range(2, k + 1) if k % d == 0}   # inclui divisores (a chave real costuma ser um deles)
    res = []
    for k in cands:
        key = bytes(max(range(256), key=lambda c: score(xor(data[i::k], c))) for i in range(k))
        res.append((score(xor(data, key)) / len(data), k, key))
    for sc, k, key in sorted(res, reverse=True)[:3]:
        print(f"keylen={k} key={key} -> {xor(data, key)[:70]}")

if __name__ == "__main__":
    if len(sys.argv) < 3: print(__doc__); sys.exit()
    d = bytes.fromhex(sys.argv[2])
    {"single": lambda: single_brute(d), "key": lambda: known_plain(d, sys.argv[3].encode()),
     "repeat": lambda: repeat_break(d),
     "dec": lambda: print(xor(d, sys.argv[3].encode()))}[sys.argv[1]]()
