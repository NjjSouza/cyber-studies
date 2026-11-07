#!/usr/bin/env python3
"""
RSA toolkit para CTF.  Uso rápido:
    python3 rsa_toolkit.py auto --n N --e E --c C          # tenta vários ataques
    python3 rsa_toolkit.py pq --p P --q Q --e E --c C      # decifra com p e q
    python3 rsa_toolkit.py cube --e 3 --c C                # e pequeno, sem módulo
    python3 rsa_toolkit.py common --n N --e1 E1 --e2 E2 --c1 C1 --c2 C2
    python3 rsa_toolkit.py wiener --n N --e E --c C
    python3 rsa_toolkit.py hastad --e 3 --ns N1 N2 N3 --cs C1 C2 C3
Números aceitam decimal ou hex (0x...).
Dependências: pip install sympy requests (opcionais)
"""
import argparse, math, sys

def num(x):
    return int(x, 0) if isinstance(x, str) else int(x)

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y

def modinv(a, m):
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError("sem inverso modular (gcd != 1)")
    return x % m

def iroot(k, n):
    """raiz k-ésima inteira (floor) por busca binária."""
    lo, hi = 0, 1 << (n.bit_length() // k + 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** k <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo

def i2b(m):
    return m.to_bytes((m.bit_length() + 7) // 8, "big")

def show(m):
    b = i2b(m)
    print("[int ]", m)
    print("[hex ]", b.hex())
    try:
        print("[text]", b.decode())
    except UnicodeDecodeError:
        print("[text]", b)

def decrypt_pq(p, q, e, c):
    return pow(c, modinv(e, (p - 1) * (q - 1)), p * q)

def decrypt_multiprime(primes, e, c):
    """n = produto de vários primos (ex.: factordb devolve 3+ fatores)."""
    n = math.prod(primes)
    phi = math.prod(p - 1 for p in primes)
    return pow(c, modinv(e, phi), n)

def fermat(n, rounds=1_000_000):
    """funciona se p e q são próximos."""
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    for _ in range(rounds):
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            return a - b, a + b
        a += 1
    return None

def small_e_no_mod(e, c):
    """m^e < n  ->  m = raiz e-ésima de c."""
    m = iroot(e, c)
    return m if m ** e == c else None

def small_e_with_padding(e, c, n, tries=100000):
    """m^e = c + k*n  (m^e um pouco maior que n)."""
    for k in range(tries):
        m = iroot(e, c + k * n)
        if m ** e == c + k * n:
            return m
    return None

def common_modulus(n, e1, e2, c1, c2):
    """mesma msg, mesmo n, expoentes e1,e2 coprimos."""
    g, a, b = egcd(e1, e2)
    if g != 1:
        raise ValueError("gcd(e1,e2) != 1")
    if a < 0:
        c1, a = modinv(c1, n), -a
    if b < 0:
        c2, b = modinv(c2, n), -b
    return (pow(c1, a, n) * pow(c2, b, n)) % n

def hastad(e, ns, cs):
    """mesma msg, e pequeno, módulos diferentes (CRT)."""
    N = math.prod(ns)
    x = 0
    for n, c in zip(ns, cs):
        Ni = N // n
        x += c * Ni * modinv(Ni, n)
    return iroot(e, x % N)

def shared_prime(n1, n2):
    """dois n compartilham um primo -> gcd."""
    g = math.gcd(n1, n2)
    return (g, n1 // g, n2 // g) if 1 < g < n1 else None

def _cf(n, d):
    out = []
    while d:
        q = n // d
        out.append(q)
        n, d = d, n - q * d
    return out

def _convergents(cf):
    h0, h1, k0, k1 = 0, 1, 1, 0
    for a in cf:
        h0, h1 = h1, a * h1 + h0
        k0, k1 = k1, a * k1 + k0
        yield h1, k1

def wiener(n, e):
    """d pequeno (e muito grande)."""
    for k, d in _convergents(_cf(e, n)):
        if k == 0 or (e * d - 1) % k:
            continue
        phi = (e * d - 1) // k
        s = n - phi + 1
        disc = s * s - 4 * n
        if disc >= 0:
            r = math.isqrt(disc)
            if r * r == disc and (s + r) % 2 == 0:
                return d
    return None

def factordb(n):
    """consulta factordb.com (precisa de internet). Devolve lista de primos ou None."""
    try:
        import requests
        r = requests.get("http://factordb.com/api", params={"query": str(n)}, timeout=15).json()
        if r.get("status") in ("FF", "CF"):
            out = []
            for f, mult in r["factors"]:
                out += [int(f)] * mult
            if math.prod(out) == n and len(out) > 1:
                return out
        print("[factordb] status:", r.get("status"), "(não totalmente fatorado)")
    except Exception as ex:
        print("[factordb] falhou:", ex)
    return None

def sympy_factor(n, limit=10**6):
    try:
        from sympy import factorint, isprime
        f = factorint(n, limit=limit)
        primes = [p for p, m in f.items() for _ in range(m)]
        return primes if math.prod(primes) == n and all(isprime(p) for p in primes) and len(primes) > 1 else None
    except ImportError:
        return None

def auto(n, e, c):
    print(f"[i] n tem {n.bit_length()} bits, e = {e}")
    if e <= 65 and (m := small_e_no_mod(e, c)):
        print("[+] e pequeno sem módulo"); return show(m)
    print("[*] sympy (primos pequenos)...")
    if (pr := sympy_factor(n)):
        print("[+] fatores:", pr); return show(decrypt_multiprime(pr, e, c))
    print("[*] Fermat (p ≈ q)...")
    if (f := fermat(n, 200000)):
        print("[+] Fermat:", f); return show(decrypt_pq(*f, e, c))
    print("[*] Wiener (d pequeno)...")
    if (d := wiener(n, e)):
        print("[+] Wiener d =", d); return show(pow(c, d, n))
    print("[*] factordb...")
    if (pr := factordb(n)):
        print("[+] factordb:", pr); return show(decrypt_multiprime(pr, e, c))
    if e <= 17 and (m := small_e_with_padding(e, c, n, 20000)):
        print("[+] e pequeno com k*n"); return show(m)
    print("[-] nada funcionou. Veja: common modulus, hastad, n compartilhado (gcd), RsaCtfTool.")

def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    def add(name, *args):
        a = sp.add_parser(name)
        for x in args: a.add_argument(f"--{x}", required=True)
        return a
    add("auto", "n", "e", "c"); add("pq", "p", "q", "e", "c"); add("cube", "e", "c")
    add("common", "n", "e1", "e2", "c1", "c2"); add("wiener", "n", "e", "c")
    h = add("hastad", "e"); h.add_argument("--ns", nargs="+", required=True); h.add_argument("--cs", nargs="+", required=True)
    g = ap.parse_args()
    if g.cmd == "auto": auto(num(g.n), num(g.e), num(g.c))
    elif g.cmd == "pq": show(decrypt_pq(num(g.p), num(g.q), num(g.e), num(g.c)))
    elif g.cmd == "cube": show(small_e_no_mod(num(g.e), num(g.c)) or sys.exit("não é raiz exata"))
    elif g.cmd == "common": show(common_modulus(num(g.n), num(g.e1), num(g.e2), num(g.c1), num(g.c2)))
    elif g.cmd == "wiener":
        d = wiener(num(g.n), num(g.e)); print("d =", d)
        if d: show(pow(num(g.c), d, num(g.n)))
    elif g.cmd == "hastad": show(hastad(num(g.e), [num(x) for x in g.ns], [num(x) for x in g.cs]))

if __name__ == "__main__":
    main()
