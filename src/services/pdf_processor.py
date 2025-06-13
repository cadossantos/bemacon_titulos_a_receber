"""
Serviço responsável pelo processamento de arquivos PDF.
"""

import pandas as pd
from pathlib import Path
from typing import Optional
from ..config import config
from .pdf_parser import processar_pdf


class PDFProcessorService:
    """Serviço para processamento de arquivos PDF."""
    
    @staticmethod
    def processar_arquivo_upload(arquivo_upload) -> Optional[pd.DataFrame]:
        """
        Processa um arquivo PDF enviado via upload.
        
        Args:
            arquivo_upload: Arquivo enviado via Streamlit file_uploader
            
        Returns:
            DataFrame com os dados extraídos ou None se houver erro
        """
        if arquivo_upload is None:
            return None
        
        try:
            # Gerar caminho do arquivo
            caminho_arquivo = PDFProcessorService._gerar_caminho_arquivo(arquivo_upload.name)
            
            # Salvar arquivo
            PDFProcessorService._salvar_arquivo(arquivo_upload, caminho_arquivo)
            
            # Processar e retornar dados
            return processar_pdf(caminho_arquivo, config.CAMINHO_CSV)
            
        except Exception as e:
            print(f"Erro ao processar arquivo PDF: {e}")
            return None
    
    @staticmethod
    def carregar_dados_padrao() -> pd.DataFrame:
        """
        Carrega os dados do CSV padrão quando nenhum arquivo é enviado.
        
        Returns:
            DataFrame com os dados padrão
        """
        try:
            return pd.read_csv(config.CAMINHO_CSV)
        except FileNotFoundError:
            print(f"Arquivo CSV não encontrado: {config.CAMINHO_CSV}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Erro ao carregar dados padrão: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def _gerar_caminho_arquivo(nome_arquivo: str) -> Path:
        """
        Gera o caminho completo para salvar o arquivo PDF.
        
        Args:
            nome_arquivo: Nome original do arquivo
            
        Returns:
            Path completo para o arquivo
        """
        nome_limpo = Path(nome_arquivo).stem.replace(" ", "_")
        return config.CAMINHO_MEDIA / f"{nome_limpo}.pdf"
    
    @staticmethod
    def _salvar_arquivo(arquivo_upload, caminho_destino: Path) -> None:
        """
        Salva o arquivo enviado no caminho especificado.
        
        Args:
            arquivo_upload: Arquivo do Streamlit
            caminho_destino: Caminho onde salvar o arquivo
        """
        with open(caminho_destino, "wb") as f:
            f.write(arquivo_upload.read())
    
    @staticmethod
    def obter_nome_arquivo_processado(arquivo_upload) -> str:
        """
        Obtém o nome do arquivo que foi processado.
        
        Args:
            arquivo_upload: Arquivo do Streamlit
            
        Returns:
            Nome do arquivo processado
        """
        return arquivo_upload.name if arquivo_upload else "relatorio_padrao.csv"