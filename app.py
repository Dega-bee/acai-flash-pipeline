import streamlit as st
from pathlib import Path
import sys

# Adiciona a pasta raiz ao caminho do Python
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Importamos o nosso ETL e o módulo de Banco de Dados
from src.etl import processar_relatorio_99food
from src.database import carregar_historico_banco

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
    st.markdown("<p style='color: #63406e; font-weight: 600; font-size: 0.85rem;'>Gestão Operacional & IA</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("<h4 style='color: #3b0a45;'>📁 Alimentar Sistema</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Selecione o relatório Excel (.xlsx)", 
        type=["xlsx"]
    )
    
    st.divider()
    st.info("💡 **Arquitetura Ativa:** ETL centralizado com persistência em SQLite e suporte a Agentes de IA.")

# --- CORPO PRINCIPAL ---
st.markdown('<div class="main-header">🫐 Dashboard Operacional</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Sistema Operacional de IA — Açaí Flash Data Pipeline.</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    try:
        # Guarda o ficheiro bruto na pasta data/raw
        raw_path = BASE_DIR / "data" / "raw" / "relatorio_99food.xlsx"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        with open(raw_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Executa o ETL (que automaticamente valida, limpa e guarda no SQLite)
        dados_processados = processar_relatorio_99food(raw_path)

        receita_total = dados_processados["receita_total"]
        total_vendas = dados_processados["total_vendas"]
        ticket_medio = dados_processados["ticket_medio"]
        taxa_conversao = dados_processados["taxa_conversao"]
        total_visitantes = dados_processados["total_visitantes"]
        novos_clientes = dados_processados["novos_clientes"]
        df_exibir = dados_processados["dataframe_limpo"]

        # --- SEÇÃO 1: INDICADORES DO RELATÓRIO ATUAL ---
        st.markdown("<h3 style='color: #3b0a45; font-weight: 700; font-size: 1.2rem;'>📊 Indicadores do Relatório Atual</h3>", unsafe_allow_html=True)
        
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

    except Exception as e:
        st.error(f"Erro ao processar o ficheiro pelo motor ETL: {e}")

else:
    st.info("👈 Carregue um relatório Excel na barra lateral para analisar os dados atuais.")

# --- SEÇÃO 2: HISTÓRICO ACUMULADO DO BANCO DE DADOS ---
st.markdown("<h3 style='color: #3b0a45; font-weight: 700; font-size: 1.2rem;'>📈 Histórico Operacional Acumulado (Banco SQLite)</h3>", unsafe_allow_html=True)

df_historico = carregar_historico_banco()

if not df_historico.empty:
    st.dataframe(df_historico, width="stretch")
    
    # Gráfico de evolução da receita histórica
    if len(df_historico) > 1:
        st.markdown("<p style='color: #63406e; font-weight: 600; font-size: 0.9rem;'>Evolução da Receita Total por Registo</p>", unsafe_allow_html=True)
        st.line_chart(df_historico.set_index('data_processamento')['receita_total'], color="#4a0e56")
else:
    st.warning("Ainda não existem dados históricos gravados no banco de dados. Carregue pelo menos um relatório na barra lateral.")