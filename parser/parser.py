# parser/parser.py

import pdfplumber
import pandas as pd
from pathlib import Path

def limpa_valor(valor: str) -> str:
    return valor.replace('.', '').replace(',', '.')

def extrair_dados_pdf(caminho_pdf: Path) -> pd.DataFrame:
    dados = []
    cliente_atual = None

    with pdfplumber.open(caminho_pdf) as pdf:
        for page in pdf.pages:
            lines = page.extract_text().split('\n')

            for i in range(len(lines) - 1):
                l1 = lines[i].strip()
                l2 = lines[i + 1].strip()

                if "-" in l1 and not l1.startswith("Aberto") and "Loja" not in l1 and "Crediario" not in l1:
                    cliente_atual = l1.split("-", 1)[1].strip()
                    continue

                if (any(c in l1 for c in ["Loja", "Crediario"]) and l2.startswith("Aberto") and cliente_atual):
                    try:
                        partes1 = l1.split()
                        partes2 = l2.split()

                        if not all([
                            partes2[-3].replace(',', '.').replace('.', '').isdigit(),
                            partes2[-2].replace(',', '.').replace('.', '').isdigit(),
                            partes2[-1].replace(',', '.').replace('.', '').isdigit(),
                        ]):
                            print(f"[SKIP] Linha {i} ignorada por dados inválidos")
                            continue

                        titulo = partes1[0]
                        valor_original = limpa_valor(partes1[-1])
                        especie = partes1[-2]
                        local = partes1[-3]

                        idx_fatura = -4
                        while idx_fatura > -len(partes1):
                            if partes1[idx_fatura].isdigit():
                                break
                            idx_fatura -= 1
                        fatura = partes1[idx_fatura]

                        nome = " ".join(partes1[1:idx_fatura])

                        status = partes2[0]
                        vencimento = partes2[1]
                        conta_corrente = " ".join(partes2[2:-3])
                        acres = limpa_valor(partes2[-3])
                        juros = limpa_valor(partes2[-2])
                        valor_total = limpa_valor(partes2[-1])

                        dados.append({
                            "Cliente": cliente_atual,
                            "Status": status,
                            "Título": titulo,
                                                        "Fatura": fatura,
                            "Local": local,
                            "Espécie": especie,
                            "Vencimento": vencimento,
                            "Conta Corrente": conta_corrente,
                            "Acres/Desc": float(acres),
                            "Juros/Multa": float(juros),
                            "R$ Original": float(valor_original),
                            "R$ Total": float(valor_total),
                        })

                    except Exception as e:
                        print(f"[ERRO] Falha ao parsear linha {i}: {e}")

    return pd.DataFrame(dados)

def salvar_csv(df: pd.DataFrame, destino: Path) -> None:
    df.to_csv(destino, index=False)

def processar_pdf(caminho_pdf: Path, destino_csv: Path):
    df = extrair_dados_pdf(caminho_pdf)
    salvar_csv(df, destino_csv)
    return df
