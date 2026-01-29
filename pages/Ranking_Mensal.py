"""
Página de Ranking Mensal - Visualização pública com filtros
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import config
from core import db

# Configuração da página
st.set_page_config(
    page_title=f"{config.APP_ICON} Ranking Mensal",
    page_icon="📅",
    layout="wide"
)

# Título
st.title("📅 Ranking Mensal")
st.markdown("Acompanhe o desempenho dos participantes mês a mês.")

try:
    # Buscar dados do ranking mensal
    ranking_completo = db.get_ranking_mensal()
    
    if not ranking_completo:
        st.info("📊 Ainda não há classificações registradas.")
        st.info("👉 Entre em contato com o administrador para começar a registrar os resultados!")
        st.stop()
    
    # Converter para DataFrame
    df_completo = pd.DataFrame(ranking_completo)
    
    # Obter meses e anos disponíveis
    meses_disponiveis = sorted(df_completo['mes_referencia'].dropna().unique())
    anos_disponiveis = sorted(df_completo['ano_referencia'].dropna().unique(), reverse=True)
    
    # Filtros
    st.markdown("### 🔍 Filtros")
    col_filtro1, col_filtro2 = st.columns([1, 1])
    
    with col_filtro1:
        ano_selecionado = st.selectbox(
            "Ano",
            options=anos_disponiveis,
            index=0 if anos_disponiveis else None
        )
    
    with col_filtro2:
        # Filtrar meses disponíveis para o ano selecionado
        meses_ano = df_completo[df_completo['ano_referencia'] == ano_selecionado]['mes_referencia'].unique()
        meses_ano_sorted = sorted(meses_ano)
        
        mes_selecionado = st.selectbox(
            "Mês",
            options=meses_ano_sorted,
            format_func=lambda x: config.MESES.get(x, str(x)),
            index=len(meses_ano_sorted) - 1 if meses_ano_sorted else 0
        )
    
    # Filtrar dados
    df_filtrado = df_completo[
        (df_completo['mes_referencia'] == mes_selecionado) & 
        (df_completo['ano_referencia'] == ano_selecionado)
    ].copy()
    
    if df_filtrado.empty:
        st.warning(f"📭 Não há dados para {config.MESES[mes_selecionado]}/{ano_selecionado}")
        st.stop()
    
    # Ordenar por total do mês
    df_filtrado = df_filtrado.sort_values('total_mes', ascending=False).reset_index(drop=True)
    
    # Adicionar posição
    df_filtrado.insert(0, 'posicao', range(1, len(df_filtrado) + 1))
    
    # Adicionar emojis de medalha
    def adicionar_medalha(pos):
        if pos == 1:
            return "🥇"
        elif pos == 2:
            return "🥈"
        elif pos == 3:
            return "🥉"
        else:
            return f"{pos}º"
    
    df_filtrado['posicao_display'] = df_filtrado['posicao'].apply(adicionar_medalha)
    
    st.markdown("---")
    
    # Estatísticas do mês
    st.markdown(f"### 📊 Resumo - {config.MESES[mes_selecionado]}/{ano_selecionado}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        participantes_mes = len(df_filtrado)
        st.metric("👥 Participantes", participantes_mes)
    
    with col2:
        total_mes = df_filtrado['total_mes'].sum()
        st.metric("💰 Total Distribuído", f"R$ {total_mes:,.2f}")
    
    with col3:
        if participantes_mes > 0:
            media_mes = total_mes / participantes_mes
            st.metric("📊 Média", f"R$ {media_mes:,.2f}")
        else:
            st.metric("📊 Média", "R$ 0,00")
    
    with col4:
        total_colocacoes = df_filtrado['total_colocacoes'].sum()
        st.metric("🎯 Colocações", int(total_colocacoes))
    
    st.markdown("---")
    
    # Tabela do ranking mensal
    st.markdown("### 🏅 Classificação do Mês")
    
    df_display = df_filtrado[[
        'posicao_display',
        'nome_time',
        'nome_dono',
        'total_mes',
        'total_colocacoes',
        'primeiros_lugares',
        'segundos_lugares',
        'terceiros_lugares'
    ]].copy()
    
    df_display.columns = [
        'Pos',
        'Time',
        'Dono',
        'Total no Mês',
        'Colocações',
        '🥇 1º',
        '🥈 2º',
        '🥉 3º'
    ]
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Pos': st.column_config.TextColumn('Pos', width='small'),
            'Time': st.column_config.TextColumn('Time', width='medium'),
            'Dono': st.column_config.TextColumn('Dono', width='medium'),
            'Total no Mês': st.column_config.NumberColumn(
                'Total no Mês',
                format="R$ %.2f",
                width='medium'
            ),
            'Colocações': st.column_config.NumberColumn('Colocações', format="%d"),
            '🥇 1º': st.column_config.NumberColumn('🥇 1º', format="%d", width='small'),
            '🥈 2º': st.column_config.NumberColumn('🥈 2º', format="%d", width='small'),
            '🥉 3º': st.column_config.NumberColumn('🥉 3º', format="%d", width='small'),
        }
    )
    
    # Comparação com outros meses
    st.markdown("---")
    st.markdown("### 📈 Comparação Mensal")
    
    # Agrupar dados por mês
    df_comparacao = df_completo.groupby(['mes_referencia', 'ano_referencia']).agg({
        'total_mes': 'sum',
        'total_colocacoes': 'sum'
    }).reset_index()
    
    df_comparacao['periodo'] = df_comparacao.apply(
        lambda row: f"{config.MESES.get(row['mes_referencia'], 'N/A')}/{int(row['ano_referencia'])}", 
        axis=1
    )
    
    df_comparacao = df_comparacao.sort_values(['ano_referencia', 'mes_referencia'])
    
    # Exibir gráfico se houver mais de um mês
    if len(df_comparacao) > 1:
        import altair as alt
        
        chart = alt.Chart(df_comparacao).mark_bar().encode(
            x=alt.X('periodo:N', title='Período', sort=None),
            y=alt.Y('total_mes:Q', title='Total Distribuído (R$)'),
            color=alt.condition(
                alt.datum.mes_referencia == mes_selecionado,
                alt.value('#ff4b4b'),
                alt.value('#0068c9')
            ),
            tooltip=[
                alt.Tooltip('periodo:N', title='Período'),
                alt.Tooltip('total_mes:Q', title='Total', format=',.2f'),
                alt.Tooltip('total_colocacoes:Q', title='Colocações', format='d')
            ]
        ).properties(
            height=300
        )
        
        st.altair_chart(chart, use_container_width=True)
        
        st.caption(f"*Mês atual ({config.MESES[mes_selecionado]}) destacado em vermelho*")
    else:
        st.info("📊 Quando houver mais de um mês com dados, um gráfico comparativo será exibido aqui.")
    
    # Destaques do mês
    st.markdown("---")
    st.markdown(f"### ⭐ Destaques de {config.MESES[mes_selecionado]}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 👑 Melhor do Mês")
        if not df_filtrado.empty:
            melhor = df_filtrado.iloc[0]
            st.write(f"**{melhor['nome_time']}**")
            st.write(f"💰 R$ {melhor['total_mes']:.2f}")
            st.write(f"🎯 {int(melhor['total_colocacoes'])} colocações")
    
    with col2:
        st.markdown("#### 🥇 Mais Vitórias")
        mais_primeiros = df_filtrado.nlargest(1, 'primeiros_lugares')
        if not mais_primeiros.empty:
            row = mais_primeiros.iloc[0]
            st.write(f"**{row['nome_time']}**")
            st.write(f"🥇 {int(row['primeiros_lugares'])} vitórias")
    
    with col3:
        st.markdown("#### 🎯 Mais Consistente")
        mais_consistente = df_filtrado.nlargest(1, 'total_colocacoes')
        if not mais_consistente.empty:
            row = mais_consistente.iloc[0]
            st.write(f"**{row['nome_time']}**")
            st.write(f"🎯 {int(row['total_colocacoes'])} colocações")

except Exception as e:
    st.error(f"❌ Erro ao carregar ranking mensal: {str(e)}")
    st.info("Entre em contato com o administrador.")