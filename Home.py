"""
Página Principal - Home
Sistema de Premiação Cartola FC
"""
import streamlit as st
import config
from core import db

# Configuração da página
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title(f"{config.APP_ICON} Sistema de Premiação Liga Kamikazze")

# Descrição
st.markdown("""
Bem-vindo ao sistema de gerenciamento de premiações da nossa liga no Cartola FC!

### 📊 O que você pode fazer aqui:

- **🏆 Ranking Geral**: Veja quem está acumulando mais prêmios no campeonato
- **📅 Ranking Mensal**: Acompanhe o desempenho mês a mês
- **🔐 Área Admin**: Cadastre times, rodadas e registre os resultados

---
""")

# Estatísticas rápidas
try:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        times = db.listar_times()
        st.metric(
            label="⚽ Times Cadastrados",
            value=len(times)
        )
    
    with col2:
        rodadas = db.listar_rodadas()
        st.metric(
            label="🎯 Rodadas Criadas",
            value=len(rodadas)
        )
    
    with col3:
        rodadas_fechadas = [r for r in rodadas if r['status'] == 'fechada']
        st.metric(
            label="✅ Rodadas Finalizadas",
            value=len(rodadas_fechadas)
        )
    
    with col4:
        ranking = db.get_ranking_geral()
        total_distribuido = sum([r['total_acumulado'] for r in ranking])
        st.metric(
            label="💰 Total Distribuído",
            value=f"R$ {total_distribuido:,.2f}"
        )

except Exception as e:
    st.warning("⚠️ Ainda não há dados cadastrados no sistema.")
    st.info("👉 Use a página de **Admin** para começar a cadastrar times e rodadas!")

# Informações sobre o sistema
st.markdown("---")
st.subheader("ℹ️ Como usar o sistema")

with st.expander("📖 Guia Rápido"):
    st.markdown("""
    **Para Administradores:**
    1. Acesse a página **🔐 Admin**
    2. Faça login com a senha
    3. Cadastre os times participantes
    4. Crie as rodadas do campeonato
    5. Após cada rodada, registre os 3 primeiros colocados
    
    **Para Visualizar:**
    - Não é necessário login
    - Acesse **🏆 Ranking Geral** para ver o acumulado
    - Acesse **📅 Ranking Mensal** para filtrar por mês
    """)

with st.expander("💡 Regras de Premiação"):
    st.markdown("""
    Em cada rodada, os prêmios são distribuídos da seguinte forma:
    
    - 🥇 **1º Lugar**: R$ 45,00
    - 🥈 **2º Lugar**: R$ 30,00
    - 🥉 **3º Lugar**: R$ 20,00
    
    **Total por rodada**: R$ 95,00
    
    Ao final do campeonato (38 rodadas), cada participante recebe o valor acumulado
    de todas as suas colocações!
    """)

# Rodapé
st.markdown("---")
st.caption("Desenvolvido por Pista para a liga Kamikazze")