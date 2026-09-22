import pandas as pd
from pathlib import Path

# Caminhos dos ficheiros
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "relatorio_99food.xlsx"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "99food_processado.csv"

def processar_dados():
    print("A carregar e transformar os dados do relatório...")
    df = pd.read_excel(RAW_DATA_PATH)

    # Seleção das colunas principais de vendas, financeiro e clientes
    colunas_interesse = [
        'Data',
        'Total de vendas realizadas',
        'Receita total de vendas',
        'Valor médio dos pedidos',
        'Despesas de marketing',
        'Despesas de comissão',
        'Receita total',
        'Visitantes da loja',
        'Clientes que fizeram um pedido',
        'Novos clientes',
        'Clientes recorrentes'
    ]

    # Filtrar apenas as colunas selecionadas
    df_clean = df[colunas_interesse].copy()

    # Formatar campo de Data
    df_clean['Data'] = pd.to_datetime(df_clean['Data']).dt.strftime('%Y-%m-%d')
    df_clean = df_clean.sort_values(by='Data')

    # Guardar o ficheiro limpo em data/processed/
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(PROCESSED_DATA_PATH, index=False, encoding='utf-8-sig')

    print(f"\n[SUCESSO] Ficheiro limpo guardado em: {PROCESSED_DATA_PATH}")
    print("\n--- RESUMO DOS DADOS PROCESSADOS ---")
    print(df_clean.info())
    print("\n--- PRIMEIRAS LINHAS ---")
    print(df_clean.head())

if __name__ == "__main__":
    processar_dados()
    