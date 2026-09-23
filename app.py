import streamlit as st
from pathlib import Path
import sys

# Adiciona a pasta raiz ao caminho do Python para encontrarmos a pasta 'src'
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Importamos a nossa função profissional de ETL
from src.etl import processar_relatorio_99food

# Configuração da página Web
st.set_page_config(
    page_title="Açaí Flash — Dashboard Operacional",
    page_icon="🫐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS Personalizada
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .stApp {
        background-color: #f4eef8 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #eae0f2 !important;
        border-right: 2px solid #d4c2e3;
    }

    .main-header {
        color: #3b0a45;
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 2px;
    }

    .sub-header {
        color: #63406e;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 20px;
    }

    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #3b0a45 !important;
        padding: 12px 16px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 8px rgba(59, 10, 69, 0.06) !important;
    }

    [data-testid="stMetricLabel"] {
        color: #5c1f69 !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
    }

    [data-testid="stMetricValue"] {
        color: #28052f !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
    }

    .stButton > button, div[data-testid="stFileUploader"] section button {
        background-color: #4a0e56 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 8px 20px !important;
        box-shadow: 0 3px 6px rgba(74, 14, 86, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stButton > button:hover, div[data-testid="stFileUploader"] section button:hover {
        background-color: #2d0535 !important;
        transform: translateY(-1px);
        color: #ffffff !important;
    }

    div[data-testid="stFileUploader"] section {
        background-color: #ffffff !important;
        border: 2px dashed #4a0e56 !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/blueberry.png", width=70)
    st.markdown("<h2 style='color: #3b0a45; font-weight: 800; margin-bottom: 0;'>Açaí Flash</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #63406e; font-weight: 600; font-size: 0.85rem;'>Gestão Operacional 99Food</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("<h4 style='color: #3b0a45;'>📁 Alimentar Sistema</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Selecione o relatório Excel (.xlsx)", 
        type=["xlsx"]
    )
    
    st.divider()
    st.info("💡 **Pipeline Ativo:** Os dados são processados de forma centralizada pelo nosso motor ETL.")

# --- CORPO PRINCIPAL ---
st.markdown('<div class="main-header">🫐 Dashboard Operacional</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Arquitetura Integrada — Açaí Flash Data Pipeline.</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    try:
        # Guarda uma cópia local do ficheiro bruto na pasta data/raw
        raw_path = BASE_DIR / "data" / "raw" / "relatorio_99food.xlsx"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        with open(raw_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # --- AQUI ESTÁ A MAGIA DA ARQUITETURA ---
        # Chamamos o nosso módulo ETL para processar o ficheiro guardado
        dados_processados = processar_relatorio_99food(raw_path)

        # Extraímos os indicadores limpos retornados pelo dicionário do ETL
        receita_total = dados_processados["receita_total"]
        total_vendas = dados_processados["total_vendas"]
        ticket_medio = dados_processados["ticket_medio"]
        taxa_conversao = dados_processados["taxa_conversao"]
        total_visitantes = dados_processados["total_visitantes"]
        novos_clientes = dados_processados["novos_clientes"]
        df_exibir = dados_processados["dataframe_limpo"]

        # --- SEÇÃO 1: INDICADORES ---
        st.markdown("<h3 style='color: #3b0a45; font-weight: 700; font-size: 1.2rem;'>📊 Indicadores de Desempenho</h3>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("💰 Receita Total", f"R$ {receita_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        c2.metric("📦 Pedidos Concluídos", f"{total_vendas}")
        c3.metric("🎯 Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        c4, c5, c6 = st.columns(3)
        c4.metric("🔥 Taxa de Conversão", f"{taxa_conversao:.2f}%".replace(".", ","))
        c5.metric("👀 Visitantes na Loja", f"{total_visitantes}")
        c6.metric("👤 Novos Clientes", f"{novos_clientes}")

        st.divider()

        # --- SEÇÃO 2: GRÁFICOS ---
        st.markdown("<h3 style='color: #3b0a45; font-weight: 700; font-size: 1.2rem;'>📈 Visão Gráfica</h3>", unsafe_allow_html=True)
        
        col_vendas_nome = 'Total de vendas realizadas' if 'Total de vendas realizadas' in df_exibir.columns else 'Vendas concluidas'
        col_novos_nome = 'Novos clientes' if 'Novos clientes' in df_exibir.columns else 'Novos'
        col_visitantes_nome = 'Visitantes da loja' if 'Visitantes da loja' in df_exibir.columns else 'Visitantes'

        graf1, graf2 = st.columns(2)
        
        with graf1:
            st.markdown("<p style='color: #3b0a45; font-weight: 600; font-size: 0.9rem;'>Pedidos vs. Novos Clientes</p>", unsafe_allow_html=True)
            if col_vendas_nome in df_exibir.columns and col_novos_nome in df_exibir.columns:
                st.bar_chart(df_exibir[[col_vendas_nome, col_novos_nome]], color=["#4a0e56", "#8e44ad"])

        with graf2:
            st.markdown("<p style='color: #3b0a45; font-weight: 600; font-size: 0.9rem;'>Fluxo de Visitantes</p>", unsafe_allow_html=True)
            if col_visitantes_nome in df_exibir.columns:
                st.line_chart(df_exibir[col_visitantes_nome], color="#4a0e56")

        st.divider()

        # --- SEÇÃO 3: TABELA COMPLETA ---
        with st.expander("📋 Visualizar Tabela Completa de Dados"):
            st.dataframe(df_exibir, width="stretch")
            
            csv = df_exibir.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descarregar Tabela em CSV",
                data=csv,
                file_name="relatorio_acai_flash_processado.csv",
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Erro ao processar o ficheiro pelo motor ETL: {e}")

else:
    st.info("👈 Utilize o menu à esquerda para carregar o relatório Excel da 99Food.")