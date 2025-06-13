"""
Componentes da interface lateral (sidebar).
"""

import streamlit as st
import pandas as pd
from typing import Tuple, Optional
from ..config import FiltroRelatorio, config
from ..services.data_filter import DataFilterService
from ..services.pdf_processor import PDFProcessorService


class SidebarComponents:
    """Componentes da sidebar da aplicação."""
    
    @staticmethod
    def upload_arquivo() -> Optional[object]:
        """
        Componente para upload de arquivo PDF.
        
        Returns:
            Arquivo enviado ou None
        """
        return st.sidebar.file_uploader(
            "Carregar relatório em PDF",
            type=config.TIPOS_ARQUIVO_PERMITIDOS
        )
    
    @staticmethod
    def filtro_cliente(opcoes_clientes: list) -> str:
        """
        Componente para filtro por cliente.
        
        Args:
            opcoes_clientes: Lista de clientes disponíveis
            
        Returns:
            Cliente selecionado
        """
        return st.sidebar.selectbox(
            "Filtrar por cliente",
            ["Todos"] + opcoes_clientes
        )
    
    @staticmethod
    def filtro_titulo(opcoes_titulos: list) -> str:
        """
        Componente para filtro por título.
        
        Args:
            opcoes_titulos: Lista de títulos disponíveis
            
        Returns:
            Título selecionado
        """
        return st.sidebar.selectbox(
            "Buscar por Título",
            ["Todos"] + opcoes_titulos,
            index=0
        )
    
    @staticmethod
    def filtro_data(data_min: pd.Timestamp, data_max: pd.Timestamp) -> Tuple[object, object]:
        """
        Componente para filtro por intervalo de datas.
        
        Args:
            data_min: Data mínima disponível
            data_max: Data máxima disponível
            
        Returns:
            Tupla com (data_inicio, data_fim)
        """
        st.sidebar.caption("**Escolha o intervalo de vencimento**")
        
        data_inicio = st.sidebar.date_input("Data inicial", data_min)
        data_fim = st.sidebar.date_input("Data final", data_max)
        
        # Mostrar intervalo selecionado
        if DataFilterService.validar_intervalo_data(data_inicio, data_fim):
            st.sidebar.caption(
                f"De: {data_inicio.strftime('%d/%m/%Y')} "
                f"até: {data_fim.strftime('%d/%m/%Y')}"
            )
        else:
            st.sidebar.caption("Selecione um intervalo de datas válido.")
        
        return data_inicio, data_fim
    
    @staticmethod
    def filtro_valor(valor_min: float, valor_max: float) -> Tuple[float, float]:
        """
        Componente para filtro por faixa de valor.
        
        Args:
            valor_min: Valor mínimo disponível
            valor_max: Valor máximo disponível
            
        Returns:
            Tupla com (valor_min_selecionado, valor_max_selecionado)
        """
        if valor_min == valor_max:
            return valor_min, valor_max
        
        return st.sidebar.slider(
            "Filtrar por valor total (R$)",
            min_value=valor_min,
            max_value=valor_max,
            value=(valor_min, valor_max),
            step=100.0,
            format="%.2f"
        )
    
    @staticmethod
    def construir_sidebar(df: pd.DataFrame) -> Tuple[object, FiltroRelatorio]:
        """
        Constrói toda a sidebar com todos os componentes.
        
        Args:
            df: DataFrame com os dados para extrair opções
            
        Returns:
            Tupla com (arquivo_upload, filtros_configurados)
        """
        # Upload de arquivo
        arquivo_upload = SidebarComponents.upload_arquivo()

        # Passo 1: filtro de cliente
        opcoes_gerais = DataFilterService.obter_opcoes_filtros(df)
        cliente_selecionado = SidebarComponents.filtro_cliente(opcoes_gerais["clientes"])

        # Passo 2: obter opções com base no cliente
        opcoes_filtradas = DataFilterService.obter_opcoes_filtros(df, cliente=cliente_selecionado)

        # Filtros subsequentes com base no cliente
        titulo_selecionado = SidebarComponents.filtro_titulo(opcoes_filtradas["titulos"])
        data_inicio, data_fim = SidebarComponents.filtro_data(
            opcoes_filtradas["data_min"], opcoes_filtradas["data_max"]
        )
        valor_min, valor_max = SidebarComponents.filtro_valor(
            opcoes_filtradas["valor_min"], opcoes_filtradas["valor_max"]
        )

        # Configurar filtros
        filtros = FiltroRelatorio(
            cliente=cliente_selecionado,
            titulo=titulo_selecionado,
            data_inicio=data_inicio if DataFilterService.validar_intervalo_data(data_inicio, data_fim) else None,
            data_fim=data_fim if DataFilterService.validar_intervalo_data(data_inicio, data_fim) else None,
            valor_min=valor_min,
            valor_max=valor_max
        )

        return arquivo_upload, filtros
