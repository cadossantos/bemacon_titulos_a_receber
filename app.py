"""
Aplicação principal do Relatório de Títulos a Receber.

Este módulo orquestra todos os componentes da aplicação de forma limpa e organizada.
"""

import streamlit as st
from src.config import config
from src.services.pdf_processor import PDFProcessorService
from src.services.data_filter import DataFilterService
from src.ui.sidebar import SidebarComponents
from src.ui.main_view import MainViewComponents


@st.cache_data
def carregar_dados(arquivo_upload):
    """
    Carrega os dados do relatório com cache do Streamlit.
    
    Args:
        arquivo_upload: Arquivo enviado via upload ou None
        
    Returns:
        DataFrame com os dados carregados
    """
    if arquivo_upload is not None:
        return PDFProcessorService.processar_arquivo_upload(arquivo_upload)
    
    return PDFProcessorService.carregar_dados_padrao()


def processar_dados():
    """
    Processa os dados principais da aplicação.
    
    Returns:
        Tupla com (dataframe_filtrado, nome_arquivo_processado)
    """
    # Carregar dados iniciais
    df_inicial = carregar_dados(None)  # Carregar dados padrão primeiro
    
    if df_inicial.empty:
        return df_inicial, None
    
    # Preparar dados para filtros
    df_preparado = DataFilterService.preparar_dados_para_filtros(df_inicial)
    
    # Construir sidebar e obter filtros
    arquivo_upload, filtros = SidebarComponents.construir_sidebar(df_preparado)
    
    # Recarregar dados se novo arquivo foi enviado
    if arquivo_upload is not None:
        df_novo = carregar_dados(arquivo_upload)
        if df_novo is not None and not df_novo.empty:
            df_preparado = DataFilterService.preparar_dados_para_filtros(df_novo)
            nome_arquivo = PDFProcessorService.obter_nome_arquivo_processado(arquivo_upload)
        else:
            nome_arquivo = None
    else:
        nome_arquivo = None
    
    # Aplicar filtros
    df_filtrado = DataFilterService.aplicar_filtros(df_preparado, filtros)
    
    return df_filtrado, nome_arquivo


def main():
    """Função principal da aplicação."""
    # Configurar página
    MainViewComponents.configurar_pagina()
    
    try:
        # Processar dados
        df_filtrado, nome_arquivo = processar_dados()
        
        # Exibir interface principal
        MainViewComponents.exibir_interface_principal(df_filtrado, nome_arquivo)
        
    except Exception as e:
        MainViewComponents.exibir_erro(f"Erro inesperado na aplicação: {str(e)}")
        st.exception(e)  # Para debug em desenvolvimento


if __name__ == "__main__":
    main()