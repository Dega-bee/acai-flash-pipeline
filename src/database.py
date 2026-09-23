import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "acai_flash.db"

def criar_banco_se_nao_existir():
    """Gera a pasta e a tabela de histórico no SQLite caso não existam."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas_99food (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            receita_total REAL,
            total_vendas INTEGER,
            ticket_medio REAL,
            taxa_conversao REAL,
            total_visitantes INTEGER,
            novos_clientes INTEGER
        )
    """)
    conexao.commit()
    conexao.close()

def salvar_indicadores_no_banco(indicadores):
    """Guarda os indicadores no SQLite e limpa automaticamente eventuais duplicados."""
    criar_banco_se_nao_existir()
    
    conexao = sqlite3.connect(DB_PATH)
    
    novo_registo = {
        "receita_total": float(indicadores["receita_total"]),
        "total_vendas": int(indicadores["total_vendas"]),
        "ticket_medio": float(indicadores["ticket_medio"]),
        "taxa_conversao": float(indicadores["taxa_conversao"]),
        "total_visitantes": int(indicadores["total_visitantes"]),
        "novos_clientes": int(indicadores["novos_clientes"])
    }
    
    # Insere o novo registo
    df_novo = pd.DataFrame([novo_registo])
    df_novo.to_sql("vendas_99food", conexao, if_exists="append", index=False)
    
    # Limpeza automática: Mantém apenas a primeira ocorrência de cada conjunto de métricas idênticas
    cursor = conexao.cursor()
    cursor.execute("""
        DELETE FROM vendas_99food 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM vendas_99food 
            GROUP BY receita_total, total_vendas, ticket_medio, taxa_conversao, total_visitantes, novos_clientes
        )
    """)
    conexao.commit()
    conexao.close()

def carregar_historico_banco():
    """Lê todo o histórico acumulado do SQLite e devolve um DataFrame do Pandas limpo."""
    criar_banco_se_nao_existir()
    conexao = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM vendas_99food", conexao)
    conexao.close()
    return df
