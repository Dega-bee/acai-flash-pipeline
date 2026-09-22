import streamlit as st
import pandas as pd
from pathlib import Path

# Configuração da página Web
st.set_page_config(
    page_title="Açaí Flash — Dashboard Operacional",
    page_icon="🫐",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent

# Estilização CSS Personalizada (Fundo Roxo Claro, Botões Roxo Escuro, Fonte Moderna)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    /* Fonte Global */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Fundo Roxo Claro em todo o aplicativo */
    .stApp {
        background-color: #f4eef8 !important;
    }

    /* Barra Lateral Roxo Suave */
    [data-testid="stSidebar"] {
        background-color: #eae0f2 !important;
        border-right: 2px solid #d4c2e3;
    }

    /* Título Principal */
    .main-header {
        color: #3b0a45;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .sub-header {
        color: #63406e;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 25px;
    }

    /* Estilo para Cartões de KPIs */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #3b0a45 !important;
        padding: 16px 20px !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 10px rgba(59, 10, 69, 0.08) !important;
    }

    [data-testid="stMetricLabel"] {
        color: #5c1f69 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }

    [data-testid="stMetricValue"] {
        color: #28052f !important;
        font-weight: 800 !important;
    }

    /* Botões Roxo Escuro Estilizados */
    .stButton > button, div[data-testid="stFileUploader"] section button {
        background-color: #4a0e56 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 8px rgba(74, 14, 86, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stButton > button:hover, div[data-testid="stFileUploader"] section button:hover {
        background-color: #2d0535 !important;
        box-shadow: 0 6px 14px rgba(45, 5, 53, 0.4) !important;
        transform: translateY(-2px);
        color: #ffffff !important;
    }

    /* Botão de Download personalizado */
    .stDownloadButton > button {
        background-color: #3b0a45 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
    }

    /* Área de Upload de Ficheiros */
    div[data-testid="stFileUploader"] section {
        background-color: #ffffff !important;
        border: 2px dashed #4a0e56 !important;
        border-radius: 14px !important;
        padding: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Função de conversão numéricas
def converter_para_numero(serie):
    if serie.dtype == 'object':
        serie = (
            serie.astype(str)
            .str.replace('R$', '', regex=False)
            .str.replace(' ', '', regex=False)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
    return pd.to_numeric(serie, errors='coerce').fillna(0)

# --- BARRA LATERAL (Sidebar) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/blueberry.png", width=75)
    st.markdown("<h2 style='color: #3b0a45; font-weight: 800; margin-bottom: 0;'>Açaí Flash</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #63406e; font-weight: 600;'>Gestão Operacional 99Food</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("<h4 style='color: #3b0a45;'>📁 Alimentar Sistema</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Selecione o relatório Excel (.xlsx)", 
        type=["xlsx"]
    )
    
    st.divider()
    st.info("💡 **Como usar:** Faça o download do relatório no portal da 99Food e envie-o aqui para atualizar o painel.")

# --- CORPO PRINCIPAL ---
st.markdown('<div class="main-header">🫐 Dashboard Operacional</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Acompanhamento consolidado de vendas e desempenho no delivery.</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    try:
        # Tenta guardar cópia na pasta raw se não estiver bloqueado
        raw_path = BASE_DIR / "data" / "raw" / "relatorio_99food.xlsx"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(raw_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        except PermissionError:
            pass

        df_raw = pd.read_excel(uploaded_file)

        # Mapeamento de colunas
        col_vendas = 'Total de vendas realizadas' if 'Total de vendas realizadas' in df_raw.columns else 'Vendas concluidas'
        col_receita = 'Receita total de vendas' if 'Receita total de vendas' in df_raw.columns else 'Receita de vendas(R$)'
        col_visitantes = 'Visitantes da loja'
        col_novos = 'Novos clientes'

        # Cálculos de Indicadores
        total_vendas = converter_para_numero(df_raw[col_vendas]).sum() if col_vendas in df_raw.columns else 0.0
        receita_total = converter_para_numero(df_raw[col_receita]).sum() if col_receita in df_raw.columns else 0.0
        total_visitantes = converter_para_numero(df_raw[col_visitantes]).sum() if col_visitantes in df_raw.columns else 0.0
        novos_clientes = converter_para_numero(df_raw[col_novos]).sum() if col_novos in df_raw.columns else 0.0

        ticket_medio = receita_total / total_vendas if total_vendas > 0 else 0.0
        taxa_conversao = (total_vendas / total_visitantes * 100) if total_visitantes > 0 else 0.0

        # --- SEÇÃO 1: INDICADORES ---
        st.markdown("<h3 style='color: #3b0a45; font-weight: 700;'>📊 Indicadores de Desempenho</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Receita Total", f"R$ {receita_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col2.metric("📦 Pedidos Concluídos", f"{int(total_vendas)}")
        col3.metric("🎯 Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col4.metric("🔥 Taxa Conversão", f"{taxa_conversao:.2f}%".replace(".", ","))

        st.markdown("<br>", unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        col5.metric("👀 Visitantes na Loja", f"{int(total_visitantes)}")
        col6.metric("👤 Novos Clientes", f"{int(novos_clientes)}")

        st.divider()

        # --- SEÇÃO 2: GRÁFICOS ---
        st.markdown("<h3 style='color: #3b0a45; font-weight: 700;'>📈 Visão Gráfica</h3>", unsafe_allow_html=True)
        
        cols_exibir = [c for c in [col_vendas, col_receita, col_visitantes, col_novos] if c in df_raw.columns]
        df_exibir = df_raw[cols_exibir].copy()
        for col in df_exibir.columns:
            df_exibir[col] = converter_para_numero(df_exibir[col])

        graf1, graf2 = st.columns(2)
        
        with graf1:
            st.markdown("<p style='color: #3b0a45; font-weight: 600;'>Pedidos vs. Novos Clientes</p>", unsafe_allow_html=True)
            st.bar_chart(df_exibir[[col_vendas, col_novos]])

        with graf2:
            st.markdown("<p style='color: #3b0a45; font-weight: 600;'>Fluxo de Visitantes</p>", unsafe_allow_html=True)
            st.line_chart(df_exibir[col_visitantes])

        st.divider()

        # --- SEÇÃO 3: TABELA ---
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
        st.error(f"Erro ao processar o ficheiro: {e}")

else:
    st.info("👈 Utilize o menu à esquerda para carregar o relatório Excel da 99Food.")