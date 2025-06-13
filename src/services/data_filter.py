"""
Serviço responsável por aplicar filtros aos dados do relatório.
"""

import pandas as pd
import re
from typing import Tuple, Optional
from ..config import FiltroRelatorio
from ..utils.funcionarios import FUNCIONARIO_PARA_LOJA


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
        
        # Filtro: títulos atrasados
        if filtros.atrasados and filtros.tempo_atraso:
            hoje = pd.Timestamp.today()
            dias_limite = filtros.tempo_atraso * (7 if filtros.mes_corrente else 30)

            df_filtrado = df_filtrado[df_filtrado["Vencimento"] < hoje]
            df_filtrado = df_filtrado[(hoje - df_filtrado["Vencimento"]).dt.days <= dias_limite]

        # Filtro: cobranças futuras
        if filtros.cobrancas_futuras and filtros.dias_futuros:
            hoje = pd.Timestamp.today()
            limite = hoje + pd.Timedelta(days=filtros.dias_futuros)

            df_filtrado = df_filtrado[
                (df_filtrado["Vencimento"] > hoje) &
                (df_filtrado["Vencimento"] <= limite)
            ]

        # Filtro: Somente Funcionários
        if filtros.somente_funcionarios:
            # Normalizar nomes para comparação
            nomes_funcionarios = {nome.lower(): loja for nome, loja in FUNCIONARIO_PARA_LOJA.items()}

            # Filtrar apenas clientes que são funcionários
            df_filtrado["Cliente_normalizado"] = (
                df_filtrado["Cliente"]
                .str.replace(r"\s*\(FUNCION[AÁ]RIO\)", "", flags=re.IGNORECASE, regex=True)
                .str.lower()
                .str.normalize("NFKD")
                .str.encode("ascii", errors="ignore")
                .str.decode("utf-8")
            )
            df_filtrado = df_filtrado[df_filtrado["Cliente_normalizado"].isin(nomes_funcionarios.keys())]

            # Adicionar coluna Loja
            df_filtrado["Funcionário"] = df_filtrado["Cliente_normalizado"].map(nomes_funcionarios)

            # Aplicar filtro de loja, se necessário
            if filtros.loja != "Todas" and "Funcionário" in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado["Funcionário"] == filtros.loja]
            
            if "Cliente_normalizado" in df_filtrado.columns:
                df_filtrado.drop(columns=["Cliente_normalizado"], inplace=True)

        
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