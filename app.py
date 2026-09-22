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

# Estilização visual personalizada (Tema Açaí Flash)
st.markdown("""
    <style>
    /* Estilo para os cartões de KPIs */
    [data-testid="stMetric"] {
        background-color: #f7f3f9;
        border: 1px solid #e1d5e7;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    [data-testid="stMetricLabel"] {
        color: #4A154B;
        font-weight: 600;
        font-size: 0.95rem;
    }
    [data-testid="stMetricValue"] {
        color: #2D002E;
        font-weight: 700;
    }
    /* Estilo do cabeçalho */
    .main-header {
        color: #3b003d;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #666;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Função auxiliar de conversão numéricas
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
    st.image("https://img.icons8.com/color/96/blueberry.png", width=70)
    st.title("🫐 Açaí Flash")
    st.caption("Painel de Gestão de Vendas (99Food)")
    st.divider()
    
    st.subheader("📁 Alimentar Sistema")
    uploaded_file = st.file_uploader(
        "Carregue o relatório Excel (.xlsx)", 
        type=["xlsx"]
    )
    
    st.divider()
    st.info("💡 **Dica:** Descarregue o relatório do portal da 99Food e solte-o aqui para atualizar os gráficos.")

# --- CORPO PRINCIPAL DO DASHBOARD ---
st.markdown('<div class="main-header">🫐 Dashboard Operacional</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Acompanhamento consolidado do desempenho de vendas no delivery.</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    try:
        # Tenta guardar cópia local (se não estiver bloqueado)
        raw_path = BASE_DIR / "data" / "raw" / "relatorio_99food.xlsx"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(raw_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        except PermissionError:
            pass

        df_raw = pd.read_excel(uploaded_file)

        # Mapeamento dinâmico de colunas
        col_vendas = 'Total de vendas realizadas' if 'Total de vendas realizadas' in df_raw.columns else 'Vendas concluidas'
        col_receita = 'Receita total de vendas' if 'Receita total de vendas' in df_raw.columns else 'Receita de vendas(R$)'
        col_visitantes = 'Visitantes da loja'
        col_novos = 'Novos clientes'

        # Totais
        total_vendas = converter_para_numero(df_raw[col_vendas]).sum() if col_vendas in df_raw.columns else 0.0
        receita_total = converter_para_numero(df_raw[col_receita]).sum() if col_receita in df_raw.columns else 0.0
        total_visitantes = converter_para_numero(df_raw[col_visitantes]).sum() if col_visitantes in df_raw.columns else 0.0
        novos_clientes = converter_para_numero(df_raw[col_novos]).sum() if col_novos in df_raw.columns else 0.0

        ticket_medio = receita_total / total_vendas if total_vendas > 0 else 0.0
        taxa_conversao = (total_vendas / total_visitantes * 100) if total_visitantes > 0 else 0.0

        # --- SEÇÃO 1: CARTÕES DE KPIS ---
        st.subheader("📈 Visão Geral de Desempenho")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Receita Total", f"R$ {receita_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col2.metric("📦 Pedidos Concluídos", f"{int(total_vendas)}")
        col3.metric("🎯 Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col4.metric("🔥 Taxa de Conversão", f"{taxa_conversao:.2f}%".replace(".", ","))

        st.markdown("<br>", unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        col5.metric("👀 Visitantes na Loja", f"{int(total_visitantes)}")
        col6.metric("👤 Novos Clientes", f"{int(novos_clientes)}")

        st.divider()

        # --- SEÇÃO 2: GRÁFICOS VISUAIS ---
        st.subheader("📊 Análise Gráfica")
        
        cols_exibir = [c for c in [col_vendas, col_receita, col_visitantes, col_novos] if c in df_raw.columns]
        df_exibir = df_raw[cols_exibir].copy()
        for col in df_exibir.columns:
            df_exibir[col] = converter_para_numero(df_exibir[col])

        graf1, graf2 = st.columns(2)
        
        with graf1:
            st.markdown("**Comparativo: Pedidos vs. Novos Clientes**")
            st.bar_chart(df_exibir[[col_vendas, col_novos]])

        with graf2:
            st.markdown("**Volume de Visitantes**")
            st.line_chart(df_exibir[col_visitantes])

        st.divider()

        # --- SEÇÃO 3: TABELA E EXPORTAÇÃO ---
        with st.expander("📋 Visualizar Tabela Completa de Dados Processados"):
            st.dataframe(df_exibir, width="stretch")
            
            csv = df_exibir.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descarregar Tabela em CSV",
                data=csv,
                file_name="relatorio_acai_flash_processado.csv",
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Erro ao processar o ficheiro carregado: {e}")

else:
    st.info("👈 Por favor, utilize a barra lateral à esquerda para carregar o relatório Excel da 99Food.")