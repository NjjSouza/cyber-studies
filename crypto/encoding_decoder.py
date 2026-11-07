#!/usr/bin/env python3
"""Auto-decoder em cadeia: base64/32/58/85, hex, binário, octal, decimal, url, rot13, html, reverse.
    python3 encoding_decoder.py "SGVsbG8="
    echo "..." | python3 encoding_decoder.py -
Mostra cada caminho de decodificação (até 6 níveis) e destaca flags.
"""
import sys, base64, codecs, re, urllib.parse, html

def b64(s):  return base64.b64decode(s + "=" * (-len(s) % 4))
def b64u(s): return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
def b32(s):  return base64.b32decode(s + "=" * (-len(s) % 8))
def b85(s):  return base64.b85decode(s)
def a85(s):  return base64.a85decode(s)
def hexd(s): return bytes.fromhex(re.sub(r"(0x|\\x|\s|:)", "", s))
def binary(s):
    s = re.sub(r"\s", "", s); return int(s, 2).to_bytes(len(s) // 8, "big")
def octal(s): return bytes(int(x, 8) for x in s.split())
def dec(s):   return bytes(int(x) for x in re.split(r"[\s,]+", s.strip()))
def url(s):   return urllib.parse.unquote(s).encode()
def rot13(s): return codecs.decode(s, "rot13").encode()
def htm(s):   return html.unescape(s).encode()
def rev(s):   return s[::-1].encode()
def b58(s):
    A = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = 0
    for ch in s: n = n * 58 + A.index(ch)
    return n.to_bytes((n.bit_length() + 7) // 8, "big")

DECODERS = dict(base64=b64, base64url=b64u, base32=b32, base85=b85, ascii85=a85, hex=hexd,
                binary=binary, octal=octal, decimal=dec, url=url, rot13=rot13, html=htm,
                base58=b58, reverse=rev)

LEAF = {'rot13', 'reverse', 'html', 'url'}

def printable(b):
    try: t = b.decode()
    except UnicodeDecodeError: return None
    return t if t and sum(c.isprintable() or c in "\n\t" for c in t) / len(t) > .9 else None

def walk(s, depth=0, seen=None):
    seen = set() if seen is None else seen
    if depth > 6 or s in seen: return
    seen = seen | {s}
    for name, f in DECODERS.items():
        try:
            t = printable(f(s.strip()))
            if t and t != s:
                print("  " * depth + f"[{name}] {t[:200]}")
                m = re.search(r"\w+\{[^}]*\}", t)
                if m: print("  " * depth + ">>> POSSÍVEL FLAG:", m.group())
                if name not in LEAF:      # rot13/reverse/html só mostram, não encadeiam
                    walk(t, depth + 1, seen)
        except Exception:
            pass

if __name__ == "__main__":
    s = sys.stdin.read() if len(sys.argv) < 2 or sys.argv[1] == "-" else sys.argv[1]
    walk(s)
