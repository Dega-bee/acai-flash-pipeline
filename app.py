import streamlit as st
import pandas as pd
from pathlib import Path

# Configuração da página Web
st.set_page_config(
    page_title="Açaí Flash - Painel 99Food",
    page_icon="🫐",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

st.title("🫐 Açaí Flash — Dashboard Operacional (99Food)")
st.markdown("Alimente o sistema carregando o relatório em Excel fornecido pela 99Food para calcular automaticamente os indicadores do seu negócio.")

st.divider()

def converter_para_numero(serie):
    """Trata textos com formatação de moeda/milhar e converte para numérico."""
    if serie.dtype == 'object':
        serie = (
            serie.astype(str)
            .str.replace('R$', '', regex=False)
            .str.replace(' ', '', regex=False)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
    return pd.to_numeric(serie, errors='coerce').fillna(0)

# Área para envio do ficheiro Excel
uploaded_file = st.file_uploader(
    "📤 Arraste ou selecione o relatório em Excel (.xlsx) da 99Food", 
    type=["xlsx"]
)

if uploaded_file is not None:
    try:
        # Tenta guardar cópia na pasta raw se não estiver bloqueado pelo Excel
        raw_path = BASE_DIR / "data" / "raw" / "relatorio_99food.xlsx"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(raw_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        except PermissionError:
            st.warning("⚠️ Nota: O ficheiro local está aberto no Excel, mas o aplicativo está a processar os dados diretamente da memória!")

        # Leitura dos dados diretamente do ficheiro enviado
        df_raw = pd.read_excel(uploaded_file)

        # Mapeamento dinâmico dos nomes das colunas
        col_vendas = 'Total de vendas realizadas' if 'Total de vendas realizadas' in df_raw.columns else 'Vendas concluidas'
        col_receita = 'Receita total de vendas' if 'Receita total de vendas' in df_raw.columns else 'Receita de vendas(R$)'
        col_visitantes = 'Visitantes da loja'
        col_novos = 'Novos clientes'

        # Limpeza e conversão das colunas para numérico
        total_vendas = converter_para_numero(df_raw[col_vendas]).sum() if col_vendas in df_raw.columns else 0.0
        receita_total = converter_para_numero(df_raw[col_receita]).sum() if col_receita in df_raw.columns else 0.0
        total_visitantes = converter_para_numero(df_raw[col_visitantes]).sum() if col_visitantes in df_raw.columns else 0.0
        novos_clientes = converter_para_numero(df_raw[col_novos]).sum() if col_novos in df_raw.columns else 0.0

        ticket_medio = receita_total / total_vendas if total_vendas > 0 else 0.0
        taxa_conversao = (total_vendas / total_visitantes * 100) if total_visitantes > 0 else 0.0

        st.success("✅ Ficheiro processado com sucesso!")

        st.subheader("📊 Indicadores Principais (KPIs)")
        
        # Cartões de indicadores
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        
        c1.metric("Pedidos Realizados", f"{int(total_vendas)}")
        c2.metric("Receita Total", f"R$ {receita_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        c3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        c4.metric("Visitantes Loja", f"{int(total_visitantes)}")
        c5.metric("Novos Clientes", f"{int(novos_clientes)}")
        c6.metric("Taxa Conversão", f"{taxa_conversao:.2f}%".replace(".", ","))

        st.divider()

        # Tabela com as colunas relevantes tratadas
        cols_exibir = [c for c in [col_vendas, col_receita, col_visitantes, col_novos] if c in df_raw.columns]
        df_exibir = df_raw[cols_exibir].copy()
        for col in df_exibir.columns:
            df_exibir[col] = converter_para_numero(df_exibir[col])

        st.subheader("📋 Tabela de Dados Processados")
        st.dataframe(df_exibir, use_container_width=True)

        # Botão para descarregar o relatório limpo
        csv = df_exibir.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descarregar Dados Processados (CSV)",
            data=csv,
            file_name="relatorio_processado_acai_flash.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o ficheiro: {e}")

else:
    st.info("👆 Por favor, envie um ficheiro Excel acima para visualizar os indicadores.")