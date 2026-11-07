### ‎ >_ `import ctf_toolkit` | Kit de ferramentas para CTF

[![Banner](gif1.gif)](gif1.gif)

```python
if __name__ == "__main__":
    print("Escola de Cyber + Cyber Telecom Battle ✿")
```

> **Legenda:** ☑ `pronto` (disponível) • ☐ `wip` (em andamento)

---

### ✉︎ Sobre o Repositório

`print("sobre")`

- [x] `const temas` Scripts e cheatsheets para **RSA, criptografia clássica, XOR, hashes, encoding, AES, Web, OSINT e esteganografia**
- [x] `string linguagem = "Python 3"` com `requirements.txt` pronto
- [x] `bool offline = True` tudo em `crypto/` roda sem internet (exceto consulta opcional ao FactorDB)
- [ ] `// TODO` writeups e scripts de `web/`/`stego/` sendo adicionados conforme resolvo desafios ✿

---

### ✉︎ Estrutura

`tree .`

```
.
├── README.md
├── links.md
├── requirements.txt
├── gif1.gif
├── gif2.gif
├── crypto/
│   ├── rsa_toolkit.py
│   ├── classic_ciphers.py
│   ├── xor_tools.py
│   ├── encoding_decoder.py
│   ├── hash_tools.py
│   └── aes_examples.py
├── web/
│   ├── sqli_cheatsheet.md
│   └── xss_jwt_cheatsheet.md
├── osint/
│   └── osint_checklist.md
├── stego/
│   └── stego_checklist.md
├── misc/
│   └── recon_checklist.md
└── writeups/
```

---

### ✉︎ Scripts — `crypto/`

`map<script, funcao> kit = { ... };`

| Script                  | Para quê                                                                 | Status |
|:-------------------------|:--------------------------------------------------------------------------|:------:|
| `rsa_toolkit.py`          | RSA: fatoração, Fermat, Wiener, common modulus, Håstad, e=3 sem módulo     | ☑      |
| `classic_ciphers.py`      | César, Atbash, Vigenère (decifrar e quebrar), Rail Fence, Afim, Morse      | ☑      |
| `xor_tools.py`            | XOR de 1 byte, chave repetida (Hamming), known-plaintext                  | ☑      |
| `encoding_decoder.py`     | Decodificador em cadeia (base64/32/58/85, hex, url, rot13, html...)       | ☑      |
| `hash_tools.py`           | Identificar, gerar e crackear hashes por wordlist                         | ☑      |
| `aes_examples.py`         | AES (CBC/ECB/CTR/GCM), detectar ECB, ataque byte-a-byte, bit-flipping     | ☑      |

---

### ✉︎ Cheatsheets

`vector<string> notas = { ... };`

| Pasta      | Conteúdo                                                                 | Status |
|:-----------|:---------------------------------------------------------------------------|:------:|
| `web/`     | SQLi (UNION/blind), XSS, JWT (alg=none, RS256↔HS256), LFI/SSRF/IDOR        | ☑      |
| `osint/`   | Imagem, username, domínio/empresa, Google dorks                           | ☑      |
| `stego/`   | exiftool → binwalk → strings → zsteg → steghide → espectrograma de áudio  | ☑      |
| `misc/`    | Primeiros passos quando não sabe a categoria, comandos canivete-suíço     | ☑      |
| `writeups/`| Resoluções comentadas dos desafios                                        | ☐      |

Ver também: [`links.md`](./links.md) — sites úteis por tema (OSINT, Web, criptografia, stego, RE, TLS/pcap...)

---

### ✉︎ Como usar

`pip install -r requirements.txt`

```bash
git clone https://github.com/NjjSouza/cyber-studies
cd cyber-studies/ctf-toolkit
pip install -r requirements.txt

# exemplo
python3 crypto/rsa_toolkit.py auto --n N --e E --c C
python3 crypto/encoding_decoder.py "SGVsbG8h"
```

---

[![Banner](gif2.gif)](gif2.gif)
