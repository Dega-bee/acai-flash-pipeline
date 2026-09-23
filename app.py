# --- SEÇÃO 2: HISTÓRICO ACUMULADO E GRÁFICOS DO BANCO DE DADOS ---
st.markdown("<h3 style='color: #3b0a45; font-weight: 700; font-size: 1.2rem;'>📈 Histórico Operacional & Gráficos (Banco SQLite)</h3>", unsafe_allow_html=True)

df_historico = carregar_historico_banco()

if not df_historico.empty:
    # Remove eventuais duplicados para limpar o histórico
    df_historico = df_historico.drop_duplicates(subset=['receita_total', 'total_vendas', 'total_visitantes'])
    
    # Mostra a tabela de dados acumulados
    st.dataframe(df_historico, width="stretch")
    
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    # Layout em colunas para os gráficos
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("<p style='color: #3b0a45; font-weight: 700; font-size: 1rem;'>💰 Evolução da Receita Total (R$)</p>", unsafe_allow_html=True)
        # Se houver apenas 1 registo, mostramos um gráfico de barras/métricas visual; se houver mais, linha temporal
        if len(df_historico) >= 1:
            st.bar_chart(df_historico.set_index('data_processamento')['receita_total'], color="#4a0e56")
            
    with col_g2:
        st.markdown("<p style='color: #3b0a45; font-weight: 700; font-size: 1rem;'>📦 Volume de Pedidos Concluídos</p>", unsafe_allow_html=True)
        if len(df_historico) >= 1:
            st.bar_chart(df_historico.set_index('data_processamento')['total_vendas'], color="#63406e")

    # Gráfico de Conversão se houver dados suficientes
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #3b0a45; font-weight: 700; font-size: 1rem;'>🔥 Taxa de Conversão (%) ao Longo do Tempo</p>", unsafe_allow_html=True)
    st.line_chart(df_historico.set_index('data_processamento')['taxa_conversao'], color="#5c1f69")

else:
    st.warning("Ainda não existem dados históricos gravados no banco de dados. Carregue pelo menos um relatório na barra lateral.")
    