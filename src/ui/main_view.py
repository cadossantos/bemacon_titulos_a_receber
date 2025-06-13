"""
Componentes da interface principal da aplicação.
"""

import streamlit as st
import pandas as pd
from typing import Optional
from ..config import config
from ..utils.formatters import preparar_dataframe_visualizacao, calcular_total_formatado


class MainViewComponents:
    """Componentes da interface principal."""
    
    @staticmethod
    def configurar_pagina() -> None:
        """Configura as propriedades da página Streamlit."""
        st.set_page_config(
            layout=config.LAYOUT,
            page_title=config.TITULO_PAGINA,
            initial_sidebar_state=config.SIDEBAR_STATE
        )
    
    @staticmethod
    def titulo_principal() -> None:
        """Exibe o título principal da aplicação."""
        st.title("📋 " + config.TITULO_PAGINA)
    
    @staticmethod
    def mensagem_sucesso_upload(nome_arquivo: str) -> None:
        """
        Exibe mensagem de sucesso após upload do arquivo.
        
        Args:
            nome_arquivo: Nome do arquivo processado
        """
        st.success(f"Arquivo '{nome_arquivo}' processado com sucesso.")
    
    @staticmethod
    def subtitulo_resultados(total_registros: int) -> None:
        """
        Exibe subtítulo com o número de títulos encontrados.
        
        Args:
            total_registros: Número total de registros
        """
        st.subheader(f"Títulos encontrados: {total_registros}")
    
    @staticmethod
    def tabela_dados(df: pd.DataFrame) -> None:
        """
        Exibe a tabela com os dados do relatório.
        
        Args:
            df: DataFrame com os dados
        """
        # Preparar dados para visualização
        df_formatado = preparar_dataframe_visualizacao(df)
        
        # Exibir tabela
        st.dataframe(df_formatado, use_container_width=True)
    
    @staticmethod
    def metrica_total(df: pd.DataFrame, coluna: str = "R$ Total") -> None:
        """
        Exibe a métrica com o total em aberto.
        
        Args:
            df: DataFrame com os dados
            coluna: Coluna para calcular o total
        """
        total_formatado = calcular_total_formatado(df, coluna)
        st.metric("Total em aberto", f"R$ {total_formatado}")
    
    @staticmethod
    def botao_download(df: pd.DataFrame, nome_arquivo: str = "relatorio_filtrado.csv") -> None:
        """
        Exibe botão para download do CSV filtrado.
        
        Args:
            df: DataFrame com os dados
            nome_arquivo: Nome do arquivo para download
        """
        # Preparar dados para download (com formatação)
        df_download = preparar_dataframe_visualizacao(df)
        csv = df_download.to_csv(index=False).encode("utf-8")
        
        st.download_button(
            "⬇️ Baixar CSV filtrado",
            csv,
            nome_arquivo,
            "text/csv"
        )
    
    @staticmethod
    def exibir_interface_principal(df: pd.DataFrame, arquivo_processado: Optional[str] = None) -> None:
        """
        Exibe toda a interface principal da aplicação.
        
        Args:
            df: DataFrame com os dados filtrados
            arquivo_processado: Nome do arquivo processado (se houver)
        """
        # Título
        MainViewComponents.titulo_principal()
        
        # Mensagem de sucesso se arquivo foi processado
        if arquivo_processado:
            MainViewComponents.mensagem_sucesso_upload(arquivo_processado)
        
        # Verificar se há dados para exibir
        if df.empty:
            st.warning("Nenhum dado encontrado com os filtros aplicados.")
            return
        
        # Subtítulo com número de registros
        MainViewComponents.subtitulo_resultados(len(df))
        
        # Tabela de dados
        MainViewComponents.tabela_dados(df)
        
        # Métrica de total
        MainViewComponents.metrica_total(df)
        
        # Botão de download
        MainViewComponents.botao_download(df)
    
    @staticmethod
    def exibir_erro(mensagem: str) -> None:
        """
        Exibe uma mensagem de erro.
        
        Args:
            mensagem: Mensagem de erro a ser exibida
        """
        st.error(mensagem)
    
    @staticmethod
    def exibir_aviso(mensagem: str) -> None:
        """
        Exibe uma mensagem de aviso.
        
        Args:
            mensagem: Mensagem de aviso a ser exibida
        """
        st.warning(mensagem)