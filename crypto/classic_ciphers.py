#!/usr/bin/env python3
"""Cifras clássicas + força bruta.  CLI:
    python3 classic_ciphers.py caesar "Khoor Zruog"        # testa os 26 shifts
    python3 classic_ciphers.py atbash "svool"
    python3 classic_ciphers.py vigenere-dec "LXFOPV" KEY
    python3 classic_ciphers.py vigenere-crack "texto longo cifrado..."   # estima chave
    python3 classic_ciphers.py railfence "WECRLTEERDSOEEFEAOCAIVDEN" 3
    python3 classic_ciphers.py affine "texto"              # testa todas as chaves a,b
    python3 classic_ciphers.py morse ".... .. "
"""
import sys, string
from collections import Counter

A = string.ascii_lowercase

def shift(text, k):
    out = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch) - base + k) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)

def caesar_brute(text):
    for k in range(26):
        print(f"{k:2}: {shift(text, -k)}")

def atbash(text):
    return "".join(
        (chr(ord('a') + 25 - (ord(c) - ord('a'))) if c.islower() else
         chr(ord('A') + 25 - (ord(c) - ord('A'))) if c.isupper() else c) for c in text)

def vigenere(text, key, decrypt=False):
    out, i = [], 0
    for ch in text:
        if ch.isalpha():
            k = ord(key[i % len(key)].lower()) - 97
            out.append(shift(ch, -k if decrypt else k)); i += 1
        else:
            out.append(ch)
    return "".join(out)

ENG = [8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.153,0.772,4.025,2.406,
       6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.758,0.978,2.360,0.150,1.974,0.074]

def _chi(s):
    n = len(s) or 1
    c = Counter(s)
    return sum((c.get(A[i], 0) - n * ENG[i] / 100) ** 2 / (n * ENG[i] / 100) for i in range(26))

def vigenere_crack(ct, maxlen=12):
    """Estatístico, assume texto em inglês e longo. Para português, troque a tabela ENG."""
    letters = "".join(c for c in ct.lower() if c.isalpha())
    best = []
    for L in range(1, maxlen + 1):
        key = ""
        for i in range(L):
            col = letters[i::L]
            key += A[min(range(26), key=lambda k: _chi(shift(col, -k)))]
        best.append((_chi(vigenere(letters, key, True)) / len(letters), L, key))
    for score, L, key in sorted(best)[:3]:
        print(f"len={L} key={key} -> {vigenere(ct, key, True)[:80]}")

def rail_fence_dec(ct, rails):
    n = len(ct); pattern = []
    r, d = 0, 1
    for _ in range(n):
        pattern.append(r)
        if r == 0: d = 1
        elif r == rails - 1: d = -1
        r += d
    idx = sorted(range(n), key=lambda i: pattern[i])
    out = [""] * n
    for pos, ch in zip(idx, ct):
        out[pos] = ch
    return "".join(out)

def affine_brute(ct):
    for a in [1,3,5,7,9,11,15,17,19,21,23,25]:
        ainv = pow(a, -1, 26)
        for b in range(26):
            pt = "".join(chr((ainv * (ord(c.lower()) - 97 - b)) % 26 + 97) if c.isalpha() else c for c in ct)
            print(f"a={a:2} b={b:2}: {pt}")

MORSE = {'.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F','--.':'G','....':'H','..':'I',
 '.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N','---':'O','.--.':'P','--.-':'Q','.-.':'R',
 '...':'S','-':'T','..-':'U','...-':'V','.--':'W','-..-':'X','-.--':'Y','--..':'Z',
 '-----':'0','.----':'1','..---':'2','...--':'3','....-':'4','.....':'5','-....':'6',
 '--...':'7','---..':'8','----.':'9'}

def morse(s):
    return "".join(" " if w == "/" else MORSE.get(w, "?") for w in s.split())

if __name__ == "__main__":
    if len(sys.argv) < 3: print(__doc__); sys.exit()
    c, t = sys.argv[1], sys.argv[2]
    if c == "caesar": caesar_brute(t)
    elif c == "atbash": print(atbash(t))
    elif c == "vigenere-dec": print(vigenere(t, sys.argv[3], True))
    elif c == "vigenere-enc": print(vigenere(t, sys.argv[3]))
    elif c == "vigenere-crack": vigenere_crack(t)
    elif c == "railfence": print(rail_fence_dec(t, int(sys.argv[3])))
    elif c == "affine": affine_brute(t)
    elif c == "morse": print(morse(t))
