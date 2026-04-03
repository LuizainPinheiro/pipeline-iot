import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Configuração da Página
st.set_page_config(page_title="Dashboard IoT - 3 Views SQL", layout="wide")

# Conexão com o Banco (Engine SQLAlchemy)
engine = create_engine('postgresql://postgres:senha123@localhost:5432/postgres')

def carregar_dados(view_name):
    try:
        query = f"SELECT * FROM {view_name}"
        return pd.read_sql(query, engine)
    except Exception as e:
        st.warning(f"Aviso: A View '{view_name}' não foi encontrada. Execute o script 'processamento.py' para criá-la.")
        return pd.DataFrame()

# --- CABEÇALHO ---
st.title("Monitoramento IoT - Camada Analítica")
st.markdown("Dashboard conectado a **3 Views SQL** no PostgreSQL")

# --- CARGA DE DADOS ---
df_resumo = carregar_dados("vw_resumo_iot")
df_alertas = carregar_dados("vw_alertas_criticos")
df_volume = carregar_dados("vw_volume_dados")

# --- LINHA 1: KPIs (Usando as Views de Volume e Resumo) ---
col1, col2, col3 = st.columns(3)

with col1:
    if not df_volume.empty:
        total_leituras = df_volume['total_leituras'].sum()
        st.metric("Total de Leituras", f"{total_leituras} registos")
    else:
        st.metric("Total de Leituras", "N/D")

with col2:
    if not df_resumo.empty:
        media_geral = df_resumo['media_temperatura'].mean()
        st.metric("Média Térmica Global", f"{media_geral:.2f} °C")
    else:
        st.metric("Média Térmica Global", "N/D")

with col3:
    if not df_resumo.empty:
        max_absoluta = df_resumo['temperatura_maxima'].max()
        st.metric("Pico de Temperatura", f"{max_absoluta:.2f} °C")
    else:
        st.metric("Pico de Temperatura", "N/D")

st.divider()

# --- LINHA 2: GRÁFICO E ALERTAS ---
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Tendência Diária (View: vw_resumo_iot)")
    if not df_resumo.empty:
        # Gráfico de linha com a média diária
        st.line_chart(df_resumo.set_index('data_leitura')['media_temperatura'])
    else:
        st.info("Aguardando criação da View de Resumo analítico...")

with right_col:
    st.subheader("Alertas Críticos (>25°C)")
    st.caption("Fonte: vw_alertas_criticos")
    if not df_alertas.empty:
        st.dataframe(df_alertas[['data_leitura', 'temperatura']], hide_index=True, use_container_width=True)
    else:
        st.success("Nenhum alerta crítico detetado no momento.")

# --- RODAPÉ ---
st.info("ADS UniFECAF - Projeto Pipeline IoT com Docker e PostgreSQL")