# parse_pdf_manual.py

from pathlib import Path
from parser.parser import processar_pdf

# Caminho para o PDF que você quer processar
caminho_pdf = Path("media/CREDIARIO JUN25.pdf")

# Caminho para salvar o CSV gerado
destino_csv = Path("parser/relatorio.csv")

# Processar o PDF e salvar o CSV
df = processar_pdf(caminho_pdf, destino_csv)

print("CSV gerado com sucesso em:", destino_csv)
print(df.head())
