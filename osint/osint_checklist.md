# Checklist de OSINT para CTF

## Imagem (foto/print dada no desafio)
1. Metadados: `exiftool imagem.jpg` (local) ou https://exif.tools/ — procure GPS, data, modelo de câmera, software
2. Busca reversa: Google Lens, TinEye, Yandex Images (Yandex costuma achar mais em rostos/lugares)
3. Geolocalização "manual": placas, idioma em placas, lado da direção do trânsito, vegetação, arquitetura

## Nome de usuário / pessoa
1. Sherlock (busca username em centenas de redes): `python3 sherlock.py usuario`
2. Google dork: `"nome completo" site:linkedin.com`
3. Have I Been Pwned — ver se e-mail/usuário apareceu em vazamentos (pode indicar outras contas/serviços usados)
4. Wayback Machine — versões antigas de um perfil/site que foi apagado

## Domínio / site / empresa
1. WHOIS — dono, data de registro, servidores de nome
2. `theHarvester -d dominio.com -b all` — emails, subdomínios
3. Shodan — `shodan.io` — serviços e portas expostos daquele IP/domínio
4. Certificado SSL (crt.sh) — às vezes revela subdomínios: `https://crt.sh/?q=%.dominio.com`
5. Ver `robots.txt`, `sitemap.xml`, comentários no HTML

## Google Dorks úteis
```
site:dominio.com filetype:pdf
site:dominio.com intitle:"index of"
site:pastebin.com "dominio.com"
"flag{" site:github.com
intext:"senha" filetype:txt
```

## Dica geral de prova
- Anote TUDO que achar (mesmo que pareça irrelevante) — em OSINT a flag costuma estar na junção de 2-3 pistas espalhadas
- Sempre teste variações do que achar: username com "_" "." maiúsculas, domínios .com/.net/.br
