import streamlit as st
import pandas as pd
from pathlib import Path
from parser.parser import processar_pdf


st.set_page_config(layout="wide", page_title="Relatório de Títulos a Receber", initial_sidebar_state="expanded")

# Upload do arquivo PDF ========================================================================
arquivo_pdf = st.sidebar.file_uploader("Carregar relatório em PDF", type=["pdf"])
caminho_arquivo_salvo = None

# Carregar dados
@st.cache_data
def carregar_dados():
    if arquivo_pdf is not None:
        nome_base = Path(arquivo_pdf.name).stem.replace(" ", "_")
        caminho_arquivo_salvo = Path("media") / f"{nome_base}.pdf"
        caminho_csv = Path("parser") / "relatorio.csv"

        # Salvar o arquivo PDF
        with open(caminho_arquivo_salvo, "wb") as f:
            f.write(arquivo_pdf.read())

        # Processar e gerar o CSV
        df = processar_pdf(caminho_arquivo_salvo, caminho_csv)
        return df

    # Se nenhum arquivo for carregado, lê o CSV padrão
    return pd.read_csv("parser/relatorio.csv")


df = carregar_dados()

if arquivo_pdf is not None:
    st.success(f"Arquivo '{arquivo_pdf.name}' processado com sucesso.")


st.title("📋 Relatório de Títulos a Receber")

# SIDEBAR ===================================================================================================================================

# Filtro por cliente ========================================================================
clientes = df["Cliente"].unique()
cliente_selecionado = st.sidebar.selectbox("Filtrar por cliente", ["Todos"] + list(clientes))

if cliente_selecionado != "Todos":
    df = df[df["Cliente"] == cliente_selecionado]

# Campo com autocomplete de Títulos ========================================================================
titulos_disponiveis = df["Título"].dropna().unique().tolist()
titulo_input = st.sidebar.selectbox("Buscar por Título", ["Todos"] + titulos_disponiveis, index=0)

if titulo_input != "Todos":
    df = df[df["Título"] == titulo_input]



# Filtro por data de vencimento ========================================================================
# Filtros de data separados ========================================================================================
df["Vencimento"] = pd.to_datetime(df["Vencimento"], dayfirst=True, errors="coerce")
datas = df["Vencimento"]

data_min, data_max = datas.min(), datas.max()

data_inicio = st.sidebar.date_input("Data inicial", data_min)
data_fim = st.sidebar.date_input("Data final", data_max)

if data_inicio and data_fim and data_inicio <= data_fim:
    df = df[(df["Vencimento"] >= pd.to_datetime(data_inicio)) &
            (df["Vencimento"] <= pd.to_datetime(data_fim))]

    st.sidebar.caption(f"De: {data_inicio.strftime('%d/%m/%Y')} até: {data_fim.strftime('%d/%m/%Y')}")
else:
    st.sidebar.caption("Selecione um intervalo de datas válido.")

# Filtro por faixa de valor (R$ Total) ========================================================================
valor_min, valor_max = float(df["R$ Total"].min()), float(df["R$ Total"].max())
if valor_min == valor_max:
    faixa_valor = (valor_min, valor_max)
else:
    faixa_valor = st.sidebar.slider(
        "Filtrar por valor total (R$)",
        min_value=valor_min,
        max_value=valor_max,
        value=(valor_min, valor_max),
        step=100.0,
        format="%.2f"
    )
    df = df[(df["R$ Total"] >= faixa_valor[0]) & (df["R$ Total"] <= faixa_valor[1])]

# Ajustes ========================================================================

# Formatar coluna de data no padrão brasileiro ========================================================================
df["Vencimento"] = df["Vencimento"].dt.strftime("%d/%m/%Y")

# Formatar colunas de valor para padrão brasileiro ========================================================================
total = df["R$ Total"].sum()

df["R$ Original"] = df["R$ Original"].map(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
df["R$ Total"] = df["R$ Total"].map(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Mostrar DataFrame
st.subheader(f"Títulos encontrados: {len(df)}")
st.dataframe(df, use_container_width=True)

# Totalizador ========================================================================
# total = df["R$ Total"].sum()
st.metric("Total em aberto", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Download
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Baixar CSV filtrado", csv, "relatorio_filtrado.csv", "text/csv")
