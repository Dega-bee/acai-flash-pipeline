import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "99food_processado.csv"

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

def gerar_resumo_kpis():
    if not PROCESSED_DATA_PATH.exists():
        print("[ERRO] Ficheiro processado não encontrado. Execute o process_99food.py primeiro.")
        return

    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Converter colunas numéricas com tratamento de tipos
    df['Total de vendas realizadas'] = converter_para_numero(df['Total de vendas realizadas'])
    df['Receita total de vendas'] = converter_para_numero(df['Receita total de vendas'])
    df['Visitantes da loja'] = converter_para_numero(df['Visitantes da loja'])
    df['Novos clientes'] = converter_para_numero(df['Novos clientes'])

    total_vendas = df['Total de vendas realizadas'].sum()
    receita_bruta = df['Receita total de vendas'].sum()
    ticket_medio = receita_bruta / total_vendas if total_vendas > 0 else 0.0
    total_visitantes = df['Visitantes da loja'].sum()
    novos_clientes = df['Novos clientes'].sum()

    print("====================================================")
    print("      AÇAÍ FLASH — RESUMO CONSOLIDADO (99FOOD)     ")
    print("====================================================")
    print(f" Total de Pedidos Realizados:  {total_vendas:.0f}")
    print(f" Receita Total de Vendas:     R$ {receita_bruta:,.2f}")
    print(f" Ticket Médio Geral:          R$ {ticket_medio:,.2f}")
    print(f" Total de Visitantes da Loja: {total_visitantes:.0f}")
    print(f" Total de Novos Clientes:     {novos_clientes:.0f}")
    print("====================================================")

if __name__ == "__main__":
    gerar_resumo_kpis()