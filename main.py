import sys
from pathlib import Path

# Adiciona a pasta 'src' ao caminho de pesquisa de módulos do Python
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "src"))

from ingest_99food import carregar_dados_brutos
from process_99food import processar_dados
from kpi_summary import gerar_resumo_kpis

def executar_pipeline_completa():
    print("\n🚀 A INICIAR PIPELINE DE DADOS - AÇAÍ FLASH (99FOOD)")
    print("=" * 55)
    
    print("\n1️⃣ [ETAPA 1/3] Ingestão de Dados...")
    carregar_dados_brutos()
    
    print("\n2️⃣ [ETAPA 2/3] Tratamento e Normalização...")
    processar_dados()
    
    print("\n3️⃣ [ETAPA 3/3] Consolidação de KPIs...")
    gerar_resumo_kpis()
    
    print("\n✅ Pipeline concluída com sucesso!")

if __name__ == "__main__":
    executar_pipeline_completa()
    