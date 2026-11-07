# Checklist geral / primeiros passos no desafio

Quando não souber nem a categoria certa, siga esta ordem:

1. **`file arquivo`** — identifica o tipo real do arquivo (ignore a extensão, pode estar errada de propósito)
2. **`strings arquivo | grep -i flag`** — testa achar a flag direto
3. **`exiftool arquivo`** — metadados
4. **`binwalk arquivo`** — arquivos escondidos dentro de outro
5. Se for rede (`.pcap`) → abra no Wireshark, use "Follow TCP/UDP/HTTP Stream" e procure texto plano ou `flag{`
6. Se for binário executável → `file`, depois Ghidra/strings; veja se é desafio de RE
7. Se for texto estranho → jogue no `encoding_decoder.py` do kit (cadeia automática) e no dCode

## Comandos canivete-suíço
```bash
file arquivo
strings -n 6 arquivo | grep -iE "flag|ctf|inatel"
xxd arquivo | less             # ver hexdump
exiftool arquivo
binwalk -e arquivo
unzip arquivo || 7z x arquivo  # tenta extrair caso seja arquivo compactado disfarçado
```

## Formato comum de flag nesta formação
Observado no cronograma: desafios de OSINT, Web, RSA e criptografia geral. Teste os dois padrões mais comuns:
```
flag{...}
inatel{...}
```
(ajuste o grep/regex do `encoding_decoder.py` se o formato oficial do CTF for outro — ele já reconhece qualquer `palavra{...}`)

## Gerenciamento de tempo em prova
- Não trave mais de 15-20 min numa questão sem pista nova — pule e volte depois
- Sempre leia a descrição do desafio de novo depois de tentar um pouco: muita dica fica escondida no enunciado
- Anote hashes/valores intermediários que achar — podem servir pra outra questão
