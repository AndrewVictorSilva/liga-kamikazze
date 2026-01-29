"""
Página de Ranking Geral - Visualização pública
"""
import streamlit as st
import pandas as pd
import config
from core import db

# Configuração da página
st.set_page_config(
    page_title=f"{config.APP_ICON} Ranking Geral",
    page_icon="🏆",
    layout="wide"
)

# Título
st.title("🏆 Ranking Geral - Acumulado")
st.markdown("Classificação geral do campeonato com valores acumulados por cada participante.")

try:
    # Buscar dados do ranking
    ranking = db.get_ranking_geral()
    
    if not ranking:
        st.info("📊 Ainda não há classificações registradas.")
        st.info("👉 Entre em contato com o administrador para começar a registrar os resultados!")
        st.stop()
    
    # Converter para DataFrame
    df = pd.DataFrame(ranking)
    
    # Adicionar coluna de posição
    df.insert(0, 'posicao_ranking', range(1, len(df) + 1))
    
    # Adicionar emojis de medalha para top 3
    def adicionar_medalha(pos):
        if pos == 1:
            return "🥇"
        elif pos == 2:
            return "🥈"
        elif pos == 3:
            return "🥉"
        else:
            return f"{pos}º"
    
    df['posicao_display'] = df['posicao_ranking'].apply(adicionar_medalha)
    
    # Estatísticas gerais
    st.markdown("### 📊 Resumo Geral")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_participantes = len(df)
        st.metric("👥 Participantes", total_participantes)
    
    with col2:
        total_distribuido = df['total_acumulado'].sum()
        st.metric("💰 Total Distribuído", f"R$ {total_distribuido:,.2f}")
    
    with col3:
        if total_participantes > 0:
            media_por_pessoa = total_distribuido / total_participantes
            st.metric("📊 Média por Pessoa", f"R$ {media_por_pessoa:,.2f}")
        else:
            st.metric("📊 Média por Pessoa", "R$ 0,00")
    
    with col4:
        total_colocacoes = df['total_colocacoes'].sum()
        st.metric("🎯 Total de Colocações", int(total_colocacoes))
    
    st.markdown("---")
    
    # Tabela principal do ranking
    st.markdown("### 🏅 Classificação")
    
    # Preparar DataFrame para exibição
    df_display = df[[
        'posicao_display',
        'nome_time',
        'nome_dono',
        'total_acumulado',
        'total_colocacoes',
        'primeiros_lugares',
        'segundos_lugares',
        'terceiros_lugares'
    ]].copy()
    
    df_display.columns = [
        'Pos',
        'Time',
        'Dono',
        'Total Acumulado',
        'Colocações',
        '🥇 1º',
        '🥈 2º',
        '🥉 3º'
    ]
    
    # Configurar a exibição da tabela
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Pos': st.column_config.TextColumn('Pos', width='small'),
            'Time': st.column_config.TextColumn('Time', width='medium'),
            'Dono': st.column_config.TextColumn('Dono', width='medium'),
            'Total Acumulado': st.column_config.NumberColumn(
                'Total Acumulado',
                format="R$ %.2f",
                width='medium'
            ),
            'Colocações': st.column_config.NumberColumn('Colocações', format="%d"),
            '🥇 1º': st.column_config.NumberColumn('🥇 1º', format="%d", width='small'),
            '🥈 2º': st.column_config.NumberColumn('🥈 2º', format="%d", width='small'),
            '🥉 3º': st.column_config.NumberColumn('🥉 3º', format="%d", width='small'),
        }
    )
    
    # Destaques
    st.markdown("---")
    st.markdown("### ⭐ Destaques")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🥇 Mais Primeiros Lugares")
        mais_primeiros = df.nlargest(3, 'primeiros_lugares')[['nome_time', 'primeiros_lugares']]
        for idx, row in mais_primeiros.iterrows():
            st.write(f"**{row['nome_time']}**: {int(row['primeiros_lugares'])} vitórias")
    
    with col2:
        st.markdown("#### 🎯 Mais Consistente")
        mais_consistente = df.nlargest(3, 'total_colocacoes')[['nome_time', 'total_colocacoes']]
        for idx, row in mais_consistente.iterrows():
            st.write(f"**{row['nome_time']}**: {int(row['total_colocacoes'])} colocações")
    
    with col3:
        st.markdown("#### 💰 Maior Acumulado")
        maior_valor = df.nlargest(3, 'total_acumulado')[['nome_time', 'total_acumulado']]
        for idx, row in maior_valor.iterrows():
            st.write(f"**{row['nome_time']}**: R$ {row['total_acumulado']:.2f}")
    
    # Informações adicionais
    st.markdown("---")
    with st.expander("ℹ️ Como funciona a pontuação"):
        st.markdown("""
        **Premiação por rodada:**
        - 🥇 1º Lugar: R$ 45,00
        - 🥈 2º Lugar: R$ 30,00
        - 🥉 3º Lugar: R$ 20,00
        
        **Total Acumulado**: Soma de todos os prêmios conquistados ao longo do campeonato.
        
        **Colocações**: Número de vezes que o time ficou entre os 3 primeiros.
        """)

except Exception as e:
    st.error(f"❌ Erro ao carregar ranking: {str(e)}")
    st.info("Entre em contato com o administrador.")