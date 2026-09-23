import json
from src.database import carregar_historico_banco

def gerar_contexto_ia_json():
    """Lê o histórico do banco de dados e gera um JSON estruturado para os Agentes de IA."""
    df_historico = carregar_historico_banco()
    
    if df_historico.empty:
        return json.dumps({"status": "aviso", "mensagem": "Nenhum dado histórico encontrado no banco."}, ensure_ascii=False)
    
    # Pega no registo mais recente da operação
    ultimo_registo = df_historico.iloc[-1].to_dict()
    
    # Monta o payload de contexto para a IA
    contexto_ia = {
        "empresa": "Açaí Flash",
        "canal": "99Food",
        "resumo_operacional_recente": {
            "data_registro": str(ultimo_registo.get("data_processamento")),
            "receita_total_brl": float(ultimo_registo.get("receita_total", 0)),
            "total_pedidos": int(ultimo_registo.get("total_vendas", 0)),
            "ticket_medio_brl": float(ultimo_registo.get("ticket_medio", 0)),
            "taxa_conversao_percentual": float(ultimo_registo.get("taxa_conversao", 0)),
            "visitantes_loja": int(ultimo_registo.get("total_visitantes", 0)),
            "novos_clientes": int(ultimo_registo.get("novos_clientes", 0))
        },
        "total_registros_historicos": len(df_historico)
    }
    
    return json.dumps(contexto_ia, indent=4, ensure_ascii=False)

def gerar_contexto_ia_texto():
    """Gera um resumo em texto natural formatado para injetar num prompt de Agente de IA."""
    df_historico = carregar_historico_banco()
    
    if df_historico.empty:
        return "Ainda não existem dados operacionais registados para o Açaí Flash."
    
    u = df_historico.iloc[-1]
    
    texto_resumo = (
        f"[RELATÓRIO OPERACIONAL - AÇAÍ FLASH]\n"
        f"Data do registo: {u.get('data_processamento')}\n"
        f"- Receita Total: R$ {u.get('receita_total', 0):.2f}\n"
        f"- Pedidos Concluídos: {u.get('total_vendas', 0)}\n"
        f"- Ticket Médio: R$ {u.get('ticket_medio', 0):.2f}\n"
        f"- Taxa de Conversão: {u.get('taxa_conversao', 0):.2f}%\n"
        f"- Visitantes na Loja: {u.get('total_visitantes', 0)}\n"
        f"- Novos Clientes: {u.get('novos_clientes', 0)}\n"
    )
    
    return texto_resumo