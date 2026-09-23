import sqlite3
from pathlib import Path
import pandas as pd

# Define o caminho do banco de dados na pasta data/processed
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "acai_flash.db"

def obter_conexao():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(DB_PATH)
    return conexao

def criar_tabelas():
    """Cria a tabela de histórico de vendas caso ela ainda não exista."""
    conexao = obter_conexao()
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
    """Insere um novo registo com os KPIs calculados pelo ETL no banco de dados."""
    criar_tabelas()
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("""
        INSERT INTO vendas_99food (
            receita_total, total_vendas, ticket_medio, 
            taxa_conversao, total_visitantes, novos_clientes
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        indicadores["receita_total"],
        indicadores["total_vendas"],
        indicadores["ticket_medio"],
        indicadores["taxa_conversao"],
        indicadores["total_visitantes"],
        indicadores["novos_clientes"]
    ))
    
    conexao.commit()
    conexao.close()

def carregar_historico_banco():
    """Carrega todo o histórico armazenado no banco de dados para análise futura."""
    criar_tabelas()
    conexao = obter_conexao()
    df_historico = pd.read_sql("SELECT * FROM vendas_99food", conexao)
    conexao.close()
    return df_historico