"""
Utilitários para formatação de dados.
"""

import pandas as pd
import re
from typing import Union


def formatar_valor_brasileiro(valor: Union[float, int]) -> str:
    """
    Formata um valor numérico para o padrão brasileiro (1.234,56).
    
    Args:
        valor: Valor numérico a ser formatado
        
    Returns:
        String formatada no padrão brasileiro
    """
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_data_brasileira(data: pd.Timestamp) -> str:
    """
    Formata uma data para o padrão brasileiro (dd/mm/yyyy).
    
    Args:
        data: Data a ser formatada
        
    Returns:
        String formatada no padrão brasileiro
    """
    if pd.isna(data):
        return ""
    return data.strftime("%d/%m/%Y")


def formatar_coluna_valor(serie: pd.Series) -> pd.Series:
    """
    Formata uma série de valores para o padrão brasileiro.
    
    Args:
        serie: Série pandas com valores numéricos
        
    Returns:
        Série formatada
    """
    return serie.map(formatar_valor_brasileiro)


def formatar_coluna_data(serie: pd.Series) -> pd.Series:
    """
    Formata uma série de datas para o padrão brasileiro.
    
    Args:
        serie: Série pandas com datas
        
    Returns:
        Série formatada
    """
    return serie.map(formatar_data_brasileira)


def preparar_dataframe_visualizacao(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara o DataFrame para visualização formatando colunas de data e valor.
    
    Args:
        df: DataFrame com dados brutos
        
    Returns:
        DataFrame formatado para visualização
    """
    df_formatado = df.copy()
    
    # Formatar datas
    if "Vencimento" in df_formatado.columns:
        df_formatado["Vencimento"] = formatar_coluna_data(df_formatado["Vencimento"])
    
    # Formatar valores monetários
    colunas_valor = ["R$ Original", "R$ Total"]
    for coluna in colunas_valor:
        if coluna in df_formatado.columns:
            df_formatado[coluna] = formatar_coluna_valor(df_formatado[coluna])
    
    # Reorganizar colunas: colocar "Funcionário" ao lado de "Cliente"
    colunas = list(df_formatado.columns)
    if "Cliente" in colunas and "Funcionário" in colunas:
        colunas.remove("Funcionário")
        idx_cliente = colunas.index("Cliente")
        colunas.insert(idx_cliente + 1, "Funcionário")
        df_formatado = df_formatado[colunas]
    # Remover sufixos como (FUNCIONÁRIO) dos nomes visíveis
    if "Cliente" in df_formatado.columns:
        df_formatado["Cliente"] = df_formatado["Cliente"].str.replace(
            r"\s*\(FUNCION[AÁ]RIO\)", "", flags=re.IGNORECASE, regex=True
        )

    return df_formatado


def calcular_total_formatado(df: pd.DataFrame, coluna: str = "R$ Total") -> str:
    """
    Calcula o total de uma coluna e retorna formatado.
    
    Args:
        df: DataFrame com os dados
        coluna: Nome da coluna para calcular o total
        
    Returns:
        Total formatado no padrão brasileiro
    """
    total = df[coluna].sum()
    return formatar_valor_brasileiro(total)