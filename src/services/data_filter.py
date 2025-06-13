"""
Serviço responsável por aplicar filtros aos dados do relatório.
"""

import pandas as pd
from typing import Tuple, Optional
from ..config import FiltroRelatorio


class DataFilterService:
    """Serviço para aplicação de filtros nos dados."""
    
    @staticmethod
    def aplicar_filtros(df: pd.DataFrame, filtros: FiltroRelatorio) -> pd.DataFrame:
        """
        Aplica todos os filtros configurados ao DataFrame.
        
        Args:
            df: DataFrame original
            filtros: Configuração de filtros
            
        Returns:
            DataFrame filtrado
        """
        df_filtrado = df.copy()
        
        # Filtro por cliente
        if filtros.tem_filtro_cliente():
            df_filtrado = DataFilterService._filtrar_por_cliente(df_filtrado, filtros.cliente)
        
        # Filtro por título
        if filtros.tem_filtro_titulo():
            df_filtrado = DataFilterService._filtrar_por_titulo(df_filtrado, filtros.titulo)
        
        # Filtro por data
        if filtros.tem_filtro_data():
            df_filtrado = DataFilterService._filtrar_por_data(
                df_filtrado, filtros.data_inicio, filtros.data_fim
            )
        
        # Filtro por valor
        if filtros.tem_filtro_valor():
            df_filtrado = DataFilterService._filtrar_por_valor(
                df_filtrado, filtros.valor_min, filtros.valor_max
            )
        
        return df_filtrado
    
    @staticmethod
    def _filtrar_por_cliente(df: pd.DataFrame, cliente: str) -> pd.DataFrame:
        """Filtra o DataFrame por cliente específico."""
        return df[df["Cliente"] == cliente]
    
    @staticmethod
    def _filtrar_por_titulo(df: pd.DataFrame, titulo: str) -> pd.DataFrame:
        """Filtra o DataFrame por título específico."""
        return df[df["Título"] == titulo]
    
    @staticmethod
    def _filtrar_por_data(df: pd.DataFrame, data_inicio: str, data_fim: str) -> pd.DataFrame:
        """Filtra o DataFrame por intervalo de datas."""
        data_inicio_pd = pd.to_datetime(data_inicio)
        data_fim_pd = pd.to_datetime(data_fim)
        
        return df[
            (df["Vencimento"] >= data_inicio_pd) & 
            (df["Vencimento"] <= data_fim_pd)
        ]
    
    @staticmethod
    def _filtrar_por_valor(df: pd.DataFrame, valor_min: float, valor_max: float) -> pd.DataFrame:
        """Filtra o DataFrame por faixa de valores."""
        return df[
            (df["R$ Total"] >= valor_min) & 
            (df["R$ Total"] <= valor_max)
        ]
    
    @staticmethod
    def preparar_dados_para_filtros(df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepara os dados convertendo tipos e tratando valores.
        
        Args:
            df: DataFrame original
            
        Returns:
            DataFrame preparado
        """
        df_preparado = df.copy()
        
        # Converter coluna de vencimento para datetime
        df_preparado["Vencimento"] = pd.to_datetime(
            df_preparado["Vencimento"], 
            dayfirst=True, 
            errors="coerce"
        )
        
        return df_preparado
    
    @staticmethod
    def obter_opcoes_filtros(df: pd.DataFrame, cliente: Optional[str] = None) -> dict:
        """
        Extrai as opções disponíveis para cada filtro, podendo aplicar restrições com base no cliente.
        
        Args:
            df: DataFrame com os dados
            cliente: Cliente selecionado (se houver)
            
        Returns:
            Dicionário com as opções de filtro ajustadas
        """
        if cliente and cliente != "Todos":
            df = df[df["Cliente"] == cliente]

        return {
            "clientes": sorted(df["Cliente"].unique().tolist()),
            "titulos": sorted(df["Título"].dropna().unique().tolist()),
            "data_min": df["Vencimento"].min(),
            "data_max": df["Vencimento"].max(),
            "valor_min": float(df["R$ Total"].min()),
            "valor_max": float(df["R$ Total"].max())
        }

    
    @staticmethod
    def validar_intervalo_data(data_inicio, data_fim) -> bool:
        """
        Valida se o intervalo de datas é válido.
        
        Args:
            data_inicio: Data inicial
            data_fim: Data final
            
        Returns:
            True se o intervalo é válido
        """
        return (
            data_inicio is not None and 
            data_fim is not None and 
            data_inicio <= data_fim
        )