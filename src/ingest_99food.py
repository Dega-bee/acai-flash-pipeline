import pandas as pd
from pathlib import Path

# Caminho dinâmico para o relatório bruto
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "relatorio_99food.xlsx"

def carregar_dados_brutos():
    print(f"Lendo o relatório em: {RAW_DATA_PATH}")
    try:
        df = pd.read_excel(RAW_DATA_PATH)
        
        print("\n--- VISÃO GERAL DOS DADOS ---")
        print(f"Total de linhas e colunas: {df.shape}")
        print("\n--- COLUNAS ENCONTRADAS ---")
        print(df.columns.tolist())
        print("\n--- PRIMEIRAS 5 LINHAS ---")
        print(df.head())
        
        return df
    except FileNotFoundError:
        print(f"\n[ERRO] Arquivo não encontrado em: {RAW_DATA_PATH}")

if __name__ == "__main__":
    carregar_dados_brutos()
