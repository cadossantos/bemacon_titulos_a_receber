"""
Serviço de parsing de arquivos PDF.
Extrai dados de relatórios financeiros em formato PDF.
"""

import pdfplumber
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any


class PDFParserService:
    """Serviço responsável pela extração de dados de arquivos PDF."""
    
    @staticmethod
    def limpar_valor(valor: str) -> str:
        """
        Limpa e converte valores monetários do formato brasileiro.
        
        Args:
            valor: String com valor no formato brasileiro (1.234,56)
            
        Returns:
            String com valor no formato decimal (1234.56)
        """
        return valor.replace('.', '').replace(',', '.')
    
    @staticmethod
    def extrair_dados_pdf(caminho_pdf: Path) -> pd.DataFrame:
        """
        Extrai dados estruturados de um arquivo PDF.
        
        Args:
            caminho_pdf: Caminho para o arquivo PDF
            
        Returns:
            DataFrame com os dados extraídos
        """
        dados = []
        cliente_atual = None

        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    lines = page.extract_text().split('\n')

                    for i in range(len(lines) - 1):
                        l1 = lines[i].strip()
                        l2 = lines[i + 1].strip()

                        # Identificar cliente
                        if PDFParserService._e_linha_cliente(l1):
                            cliente_atual = l1.split("-", 1)[1].strip()
                            continue

                        # Processar linha de dados
                        if PDFParserService._e_linha_dados(l1, l2, cliente_atual):
                            try:
                                dados_extraidos = PDFParserService._extrair_dados_linha(l1, l2, cliente_atual)
                                if dados_extraidos:
                                    dados.append(dados_extraidos)
                            except Exception as e:
                                print(f"[ERRO] Falha ao parsear linha {i} da página {page_num + 1}: {e}")

        except Exception as e:
            print(f"[ERRO] Falha ao processar PDF {caminho_pdf}: {e}")
            
        return pd.DataFrame(dados)
    
    @staticmethod
    def _e_linha_cliente(linha: str) -> bool:
        """Verifica se a linha contém informações de cliente."""
        return (
            "-" in linha and 
            not linha.startswith("Aberto") and 
            "Loja" not in linha and 
            "Crediario" not in linha
        )
    
    @staticmethod
    def _e_linha_dados(l1: str, l2: str, cliente_atual: str) -> bool:
        """Verifica se as linhas contêm dados de títulos."""
        return (
            any(palavra in l1 for palavra in ["Loja", "Crediario"]) and
            l2.startswith("Aberto") and
            cliente_atual is not None
        )
    
    @staticmethod
    def _extrair_dados_linha(l1: str, l2: str, cliente_atual: str) -> Dict[str, Any]:
        """
        Extrai dados estruturados de uma linha do PDF.
        
        Args:
            l1: Primeira linha com dados do título
            l2: Segunda linha com dados complementares
            cliente_atual: Nome do cliente atual
            
        Returns:
            Dicionário com os dados extraídos
        """
        partes1 = l1.split()
        partes2 = l2.split()

        # Validar se os últimos 3 valores da segunda linha são numéricos
        if not PDFParserService._validar_valores_numericos(partes2[-3:]):
            print(f"[SKIP] Linha ignorada por dados inválidos: {l2}")
            return None

        # Extrair dados da primeira linha
        titulo = partes1[0]
        valor_original = PDFParserService.limpar_valor(partes1[-1])
        especie = partes1[-2]
        local = partes1[-3]

        # Encontrar a fatura (último número antes do nome)
        idx_fatura = -4
        while idx_fatura > -len(partes1):
            if partes1[idx_fatura].isdigit():
                break
            idx_fatura -= 1
        fatura = partes1[idx_fatura] if abs(idx_fatura) <= len(partes1) else ""

        # Nome é tudo entre título e fatura
        nome = " ".join(partes1[1:idx_fatura]) if abs(idx_fatura) <= len(partes1) else ""

        # Extrair dados da segunda linha
        status = partes2[0]
        vencimento = partes2[1]
        conta_corrente = " ".join(partes2[2:-3])
        acres = PDFParserService.limpar_valor(partes2[-3])
        juros = PDFParserService.limpar_valor(partes2[-2])
        valor_total = PDFParserService.limpar_valor(partes2[-1])

        return {
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
        }
    
    @staticmethod
    def _validar_valores_numericos(valores: List[str]) -> bool:
        """
        Valida se os valores podem ser convertidos para numérico.
        
        Args:
            valores: Lista de strings a serem validadas
            
        Returns:
            True se todos os valores são válidos
        """
        for valor in valores:
            if not valor.replace(',', '.').replace('.', '').isdigit():
                return False
        return True
    
    @staticmethod
    def salvar_csv(df: pd.DataFrame, destino: Path) -> None:
        """
        Salva o DataFrame em formato CSV.
        
        Args:
            df: DataFrame a ser salvo
            destino: Caminho de destino do arquivo CSV
        """
        try:
            # Criar diretório se não existir
            destino.parent.mkdir(parents=True, exist_ok=True)
            
            # Salvar CSV
            df.to_csv(destino, index=False)
            print(f"CSV salvo com sucesso: {destino}")
            
        except Exception as e:
            print(f"[ERRO] Falha ao salvar CSV {destino}: {e}")
    
    @staticmethod
    def processar_pdf(caminho_pdf: Path, destino_csv: Path) -> pd.DataFrame:
        """
        Processa um arquivo PDF completo e salva os dados em CSV.
        
        Args:
            caminho_pdf: Caminho do arquivo PDF a ser processado
            destino_csv: Caminho onde salvar o CSV resultante
            
        Returns:
            DataFrame com os dados extraídos
        """
        print(f"Processando PDF: {caminho_pdf}")
        
        # Extrair dados
        df = PDFParserService.extrair_dados_pdf(caminho_pdf)
        
        if df.empty:
            print("⚠️ Nenhum dado foi extraído do PDF")
        else:
            print(f"✅ {len(df)} registros extraídos com sucesso")
            
            # Salvar CSV
            PDFParserService.salvar_csv(df, destino_csv)
        
        return df


# Função de compatibilidade com o código antigo
def processar_pdf(caminho_pdf: Path, destino_csv: Path) -> pd.DataFrame:
    """
    Função de compatibilidade com a versão anterior.
    
    Args:
        caminho_pdf: Caminho do arquivo PDF
        destino_csv: Caminho do arquivo CSV de destino
        
    Returns:
        DataFrame com os dados processados
    """
    return PDFParserService.processar_pdf(caminho_pdf, destino_csv)