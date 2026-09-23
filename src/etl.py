import pandas as pd
from pathlib import Path

def converter_para_numero(serie):
    """Converte colunas monetárias e textuais em números limpos para cálculo."""
    if serie.dtype == 'object':
        serie = (
            serie.astype(str)
            .str.replace('R$', '', regex=False)
            .str.replace(' ', '', regex=False)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
    return pd.to_numeric(serie, errors='coerce').fillna(0)

def processar_relatorio_99food(caminho_arquivo):
    """Lê o Excel bruto da 99Food, limpa os dados e retorna um dicionário com os KPIs calculados."""
    
    df_raw = pd.read_excel(caminho_arquivo)

    # Mapeamento dinâmico de colunas do relatório
    col_vendas = 'Total de vendas realizadas' if 'Total de vendas realizadas' in df_raw.columns else 'Vendas concluidas'
    col_receita = 'Receita total de vendas' if 'Receita total de vendas' in df_raw.columns else 'Receita de vendas(R$)'
    col_visitantes = 'Visitantes da loja' if 'Visitantes da loja' in df_raw.columns else 'Visitantes'
    col_novos = 'Novos clientes' if 'Novos clientes' in df_raw.columns else 'Novos'

    # Cálculos analíticos
    total_vendas = converter_para_numero(df_raw[col_vendas]).sum() if col_vendas in df_raw.columns else 0.0
    receita_total = converter_para_numero(df_raw[col_receita]).sum() if col_receita in df_raw.columns else 0.0
    total_visitantes = converter_para_numero(df_raw[col_visitantes]).sum() if col_visitantes in df_raw.columns else 0.0
    novos_clientes = converter_para_numero(df_raw[col_novos]).sum() if col_novos in df_raw.columns else 0.0

    ticket_medio = receita_total / total_vendas if total_vendas > 0 else 0.0
    taxa_conversao = (total_vendas / total_visitantes * 100) if total_visitantes > 0 else 0.0

    # Organiza os dados limpos num dicionário de saída
    indicadores = {
        "receita_total": receita_total,
        "total_vendas": int(total_vendas),
        "ticket_medio": ticket_medio,
        "taxa_conversao": taxa_conversao,
        "total_visitantes": int(total_visitantes),
        "novos_clientes": int(novos_clientes),
        "dataframe_limpo": df_raw
    }

    return indicadores
