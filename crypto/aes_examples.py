#!/usr/bin/env python3
"""AES com pycryptodome (pip install pycryptodome) + ataques comuns em CTF."""
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def aes_cbc_dec(ct, key, iv):  return unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ct), 16)
def aes_ecb_dec(ct, key):      return unpad(AES.new(key, AES.MODE_ECB).decrypt(ct), 16)
def aes_ctr_dec(ct, key, nonce): return AES.new(key, AES.MODE_CTR, nonce=nonce).decrypt(ct)
def aes_gcm_dec(ct, key, nonce, tag): return AES.new(key, AES.MODE_GCM, nonce=nonce).decrypt_and_verify(ct, tag)

def is_ecb(ct):
    """blocos de 16 bytes repetidos => provável ECB."""
    blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
    return len(blocks) != len(set(blocks))

def ecb_byte_at_a_time(oracle, bs=16):
    """oracle(bytes)->bytes, que faz encrypt(entrada + SEGREDO). Recupera o segredo."""
    secret = b""
    for i in range(len(oracle(b""))):
        prefix = b"A" * ((bs - 1 - i) % bs)
        blk = slice((i // bs) * bs, (i // bs + 1) * bs)
        target = oracle(prefix)[blk]
        for c in range(256):
            if oracle(prefix + secret + bytes([c]))[blk] == target:
                secret += bytes([c]); break
        else:
            break
    return secret

def cbc_bitflip(ct, block_idx, old, new):
    """Troca 'old' por 'new' (mesmo tamanho) no bloco block_idx (>=1). O bloco anterior fica corrompido."""
    ct = bytearray(ct); pos = (block_idx - 1) * 16
    for i, (o, n) in enumerate(zip(old, new)):
        ct[pos + i] ^= o ^ n
    return bytes(ct)

# Reuso de keystream (CTR/OTP/XOR): c1 ^ c2 = p1 ^ p2  -> "crib drag" com palavra provável ("flag{", "the ")
def xor(a, b): return bytes(x ^ y for x, y in zip(a, b))
