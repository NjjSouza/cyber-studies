# Checklist de Esteganografia para CTF

Ordem recomendada de testes num arquivo suspeito (imagem, áudio, etc.):

## 1. Metadados
```bash
exiftool arquivo.jpg
```
Veja todos os campos, inclusive "Comment" e "UserComment" — às vezes a flag está ali, direto em texto.

## 2. Procurar dados escondidos depois do fim do arquivo
```bash
binwalk arquivo.jpg          # lista arquivos embutidos
binwalk -e arquivo.jpg       # extrai automaticamente
foremost arquivo.jpg         # recupera arquivos embutidos por assinatura
```

## 3. Strings — texto escondido no binário
```bash
strings arquivo.jpg | grep -i flag
strings -n 8 arquivo.jpg | less
```

## 4. LSB (Least Significant Bit) — PNG/BMP
```bash
zsteg arquivo.png            # testa várias combinações de LSB automaticamente
```
Ou online: https://stegonline.georgeom.net/ (também converte PNG↔BMP se precisar)

## 5. Esteganografia com senha (steghide — comum em JPG)
```bash
steghide info arquivo.jpg
steghide extract -sf arquivo.jpg          # pede senha; tente vazia e wordlist comum
```

## 6. Diferença entre imagens (se vierem duas parecidas)
```python
from PIL import Image, ImageChops
a, b = Image.open("1.png"), Image.open("2.png")
diff = ImageChops.difference(a.convert("RGB"), b.convert("RGB"))
diff.save("diff.png")
```

## 7. Áudio
- Espectrograma! Muita flag em CTF vem escrita no espectro de frequência:
  ```bash
  sox arquivo.wav -n spectrogram -o spec.png
  ```
  ou abra no Audacity: Analyze > Plot Spectrum, ou visualize em modo "Spectrogram"
- Morse em áudio: ouça o ritmo, ou use `strings`/binwalk se for um wav com dados embutidos

## 8. PDF
```bash
exiftool arquivo.pdf
pdfimages -all arquivo.pdf saida        # extrai imagens embutidas
strings arquivo.pdf | grep -i flag
```

## Ferramenta "tudo em um"
https://aperisolve.fr/ — roda exiftool, binwalk, zsteg, strings e mais, tudo de uma vez (precisa de internet)
