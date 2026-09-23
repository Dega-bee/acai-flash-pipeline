import streamlit as st
import pandas as pd
from src.etl import processar_relatorio_99food
from src.database import carregar_historico_banco, salvar_indicadores_no_banco

# Configuração da página
st.set_page_config(page_title="Açaí Flash - Gestão Operacional & IA", layout="wide")

st.markdown("<h1 style='color: #3b0a45;'>Açaí Flash</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #63406e; font-weight: 600;'>Gestão Operacional & IA</p>", unsafe_allow_html=True)

# --- BARRA LATERAL: ALIMENTAR SISTEMA ---
st.sidebar.markdown("<h2>📁 Alimentar Sistema</h2>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Selecione o relatório Excel (.xlsx)", type=["xlsx"])

# --- PROCESSAMENTO DO RELATÓRIO ATUAL ---
if uploaded_file is not None:
    try:
        # Processa o Excel usando o motor ETL
        indicadores = processar_relatorio_99food(uploaded_file)
        
        # Salva no banco SQLite de forma segura (com proteção contra duplicados)
        salvar_indicadores_no_banco(indicadores)
        
        st.markdown("<h3 style='color: #3b0a45; font-weight: 700; font-size: 1.2rem;'>📊 Indicadores do Relatório Atual</h3>", unsafe_allow_html=True)
        
        # Cards de Métricas (Seção 1)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="💰 Receita Total", value=f"R$ {indicadores['receita_total']:,.2f}")
        with col2:
            st.metric(label="📦 Pedidos Concluídos", value=f"{indicadores['total_vendas']}")
        with col3:
            st.metric(label="🎯 Ticket Médio", value=f"R$ {indicadores['ticket_medio']:,.2f}")
            
        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric(label="🔥 Taxa de Conversão", value=f"{indicadores['taxa_conversao']:.2f}%")
        with col5:
            st.metric(label="👥 Visitantes na Loja", value=f"{indicadores['total_visitantes']}")
        with col6:
            st.metric(label="⭐ Novos Clientes", value=f"{indicadores['novos_clientes']}")
            
    except Exception as e:
        st.error(f"Erro ao processar o relatório: {e}")
else:
    st.info("👈 Carregue um relatório Excel na barra lateral para analisar os dados atuais.")

st.markdown("---")

# --- SEÇÃO 2: HISTÓRICO ACUMULADO E GRÁFICOS DO BANCO DE DADOS ---
st.markdown("<h3 style='color: #3b0a45; font-weight: 700; font-size: 1.2rem;'>📈 Histórico Operacional & Gráficos (Banco SQLite)</h3>", unsafe_allow_html=True)

df_historico = carregar_historico_banco()

if not df_historico.empty:
    # Remove eventuais duplicados para limpar o histórico
    df_historico = df_historico.drop_duplicates(subset=['receita_total', 'total_vendas', 'total_visitantes'])
    
    # Mostra a tabela de dados acumulados
    st.dataframe(df_historico, use_container_width=True)
    
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    # Layout em colunas para os gráficos
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("<p style='color: #3b0a45; font-weight: 700; font-size: 1rem;'>💰 Evolução da Receita Total (R$)</p>", unsafe_allow_html=True)
        if len(df_historico) >= 1:
            st.bar_chart(df_historico.set_index('data_processamento')['receita_total'], color="#4a0e56")
            
    with col_g2:
        st.markdown("<p style='color: #3b0a45; font-weight: 700; font-size: 1rem;'>📦 Volume de Pedidos Concluídos</p>", unsafe_allow_html=True)
        if len(df_historico) >= 1:
            st.bar_chart(df_historico.set_index('data_processamento')['total_vendas'], color="#63406e")

    # Gráfico de Conversão
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #3b0a45; font-weight: 700; font-size: 1rem;'>🔥 Taxa de Conversão (%) ao Longo do Tempo</p>", unsafe_allow_html=True)
    st.line_chart(df_historico.set_index('data_processamento')['taxa_conversao'], color="#5c1f69")

else:
    st.warning("Ainda não existem dados históricos gravados no banco de dados. Carregue pelo menos um relatório na barra lateral.")
    