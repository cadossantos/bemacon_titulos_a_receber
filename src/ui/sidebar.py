"""
Componentes da interface lateral (sidebar).
"""

import streamlit as st
import pandas as pd
from typing import Tuple, Optional
from ..config import FiltroRelatorio, config
from ..services.data_filter import DataFilterService
from ..services.pdf_processor import PDFProcessorService
from ..utils.funcionarios import FUNCIONARIOS_POR_LOJA


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
    def filtro_atrasados() -> Tuple[bool, Optional[int], bool, bool, bool]:
        atrasados = st.sidebar.checkbox("Mostrar apenas títulos atrasados")
        tempo = None
        mes_corrente = False
        ja_cobrado = False
        a_cobrar = False

        if atrasados:
            mes_corrente = st.sidebar.checkbox("Mês corrente (slider em semanas)")
            tempo = st.sidebar.slider(
                "Tempo de atraso",
                min_value=1,
                max_value=12 if not mes_corrente else 4,
                step=1,
                format="%d " + ("mês(es)" if not mes_corrente else "semana(s)")
            )
            ja_cobrado = st.sidebar.checkbox("Já cobrados")
            a_cobrar = st.sidebar.checkbox("A cobrar")

        return atrasados, tempo, mes_corrente, ja_cobrado, a_cobrar

    @staticmethod
    def filtro_cobrancas_futuras() -> Tuple[bool, Optional[int]]:
        futuras = st.sidebar.checkbox("Cobranças futuras")
        dias = None
        if futuras:
            dias = st.sidebar.select_slider(
                "Próximos dias",
                options=[7, 14, 21, 30],
                value=30
            )
        return futuras, dias

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
        left_column, right_column = st.sidebar.columns(2)
        with left_column:
            data_inicio = st.date_input("Data inicial", data_min)
        with right_column:
            data_fim = st.date_input("Data final", data_max)
        
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
    def filtro_funcionarios() -> Tuple[bool, Optional[str]]:
        somente_func = st.sidebar.checkbox("Filtrar somente funcionários")
        loja = None

        if somente_func:
            opcoes_lojas = sorted(["Todas"] + list(FUNCIONARIOS_POR_LOJA.keys()))
            loja = st.sidebar.selectbox("Filtrar por loja", opcoes_lojas, index=4)

        return somente_func, loja

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
        
        # Filtros adicionais (atrasados e cobranças futuras)
        atrasados, tempo_atraso, mes_corrente, ja_cobrado, a_cobrar = SidebarComponents.filtro_atrasados()
        cobrancas_futuras, dias_futuros = SidebarComponents.filtro_cobrancas_futuras()

        #Filtros funcionários
        somente_funcionarios, loja = SidebarComponents.filtro_funcionarios()

        # Configurar filtros
        filtros = FiltroRelatorio(
            cliente=cliente_selecionado,
            titulo=titulo_selecionado,
            data_inicio=data_inicio if DataFilterService.validar_intervalo_data(data_inicio, data_fim) else None,
            data_fim=data_fim if DataFilterService.validar_intervalo_data(data_inicio, data_fim) else None,
            valor_min=valor_min,
            valor_max=valor_max,
            atrasados=atrasados,
            tempo_atraso=tempo_atraso,
            mes_corrente=mes_corrente,
            ja_cobrados=ja_cobrado,
            a_cobrar=a_cobrar,
            cobrancas_futuras=cobrancas_futuras,
            dias_futuros=dias_futuros,
            somente_funcionarios=somente_funcionarios,
            loja=loja
        )


        return arquivo_upload, filtros
