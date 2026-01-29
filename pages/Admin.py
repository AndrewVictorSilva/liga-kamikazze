"""
Página Admin - Gerenciamento de Times, Rodadas e Classificações
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import config
from core import db, require_auth, show_logout_button

# Configuração da página
st.set_page_config(
    page_title=f"{config.APP_ICON} Admin",
    page_icon="🔐",
    layout="wide"
)

# Verificar autenticação
if not st.session_state.get("authenticated", False):
    st.title("🔐 Área Administrativa")
    from core.auth import check_password
    if not check_password():
        st.stop()

# Mostrar botão de logout
show_logout_button()

# Título
st.title("🔐 Painel Administrativo")

# Tabs principais
tab_times, tab_rodadas, tab_classificacoes = st.tabs([
    "⚽ Times", 
    "🎯 Rodadas", 
    "🏆 Classificações"
])

# ========== TAB TIMES ==========
with tab_times:
    st.header("⚽ Gerenciamento de Times")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Times Cadastrados")
        
        try:
            times = db.listar_times(apenas_ativos=True)
            
            if times:
                # Criar DataFrame para exibição
                df_times = pd.DataFrame(times)
                df_times = df_times[['nome_time', 'nome_dono', 'email', 'observacoes']]
                df_times.columns = ['Time', 'Dono', 'Email', 'Observações']
                
                st.dataframe(
                    df_times,
                    use_container_width=True,
                    hide_index=True
                )
                
                st.caption(f"Total: {len(times)} times cadastrados")
            else:
                st.info("Nenhum time cadastrado ainda. Use o formulário ao lado para adicionar!")
        
        except Exception as e:
            st.error(f"Erro ao carregar times: {str(e)}")
    
    with col2:
        st.subheader("➕ Adicionar Time")
        
        with st.form("form_novo_time", clear_on_submit=True):
            nome_time = st.text_input(
                "Nome do Time*",
                placeholder="Ex: Os Implacáveis FC",
                help="Nome do time no Cartola"
            )
            
            nome_dono = st.text_input(
                "Nome do Dono*",
                placeholder="Ex: João Silva",
                help="Nome real do participante"
            )
            
            email = st.text_input(
                "Email (opcional)",
                placeholder="joao@email.com"
            )
            
            observacoes = st.text_area(
                "Observações (opcional)",
                placeholder="Informações adicionais sobre o time..."
            )
            
            submit = st.form_submit_button("✅ Cadastrar Time", use_container_width=True)
            
            if submit:
                if not nome_time or not nome_dono:
                    st.error("❌ Nome do time e nome do dono são obrigatórios!")
                else:
                    try:
                        db.criar_time(
                            nome_time=nome_time,
                            nome_dono=nome_dono,
                            email=email if email else None,
                            observacoes=observacoes if observacoes else None
                        )
                        st.success(f"✅ Time '{nome_time}' cadastrado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao cadastrar time: {str(e)}")

# ========== TAB RODADAS ==========
with tab_rodadas:
    st.header("🎯 Gerenciamento de Rodadas")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Rodadas Cadastradas")
        
        try:
            rodadas = db.listar_rodadas()
            
            if rodadas:
                df_rodadas = pd.DataFrame(rodadas)
                df_rodadas = df_rodadas[['numero', 'data_rodada', 'mes_referencia', 'status']]
                df_rodadas.columns = ['Nº', 'Data', 'Mês', 'Status']
                
                # Adicionar emoji de status
                status_emoji = {
                    'aberta': '🟢',
                    'em_andamento': '🟡',
                    'fechada': '🔴'
                }
                df_rodadas['Status'] = df_rodadas['Status'].apply(
                    lambda x: f"{status_emoji.get(x, '⚪')} {x}"
                )
                
                st.dataframe(
                    df_rodadas,
                    use_container_width=True,
                    hide_index=True
                )
                
                st.caption(f"Total: {len(rodadas)} rodadas cadastradas")
            else:
                st.info("Nenhuma rodada cadastrada ainda. Use o formulário ao lado para adicionar!")
        
        except Exception as e:
            st.error(f"Erro ao carregar rodadas: {str(e)}")
    
    with col2:
        st.subheader("➕ Adicionar Rodada")
        
        with st.form("form_nova_rodada", clear_on_submit=True):
            numero_rodada = st.number_input(
                "Número da Rodada*",
                min_value=1,
                max_value=config.NUM_RODADAS,
                step=1,
                help=f"Rodadas de 1 a {config.NUM_RODADAS}"
            )
            
            data_rodada = st.date_input(
                "Data da Rodada*",
                value=datetime.now(),
                help="Data em que a rodada ocorre"
            )
            
            col_mes, col_ano = st.columns(2)
            with col_mes:
                mes_ref = st.selectbox(
                    "Mês*",
                    options=list(config.MESES.keys()),
                    format_func=lambda x: config.MESES[x],
                    index=datetime.now().month - 1
                )
            
            with col_ano:
                ano_ref = st.number_input(
                    "Ano*",
                    min_value=2020,
                    max_value=2030,
                    value=datetime.now().year,
                    step=1
                )
            
            status_rodada = st.selectbox(
                "Status*",
                options=config.STATUS_RODADAS,
                index=0
            )
            
            obs_rodada = st.text_area(
                "Observações (opcional)",
                placeholder="Informações sobre a rodada..."
            )
            
            submit_rodada = st.form_submit_button("✅ Criar Rodada", use_container_width=True)
            
            if submit_rodada:
                try:
                    # Verificar se rodada já existe
                    rodada_existente = db.buscar_rodada_por_numero(numero_rodada)
                    if rodada_existente:
                        st.error(f"❌ Rodada {numero_rodada} já existe!")
                    else:
                        db.criar_rodada(
                            numero=numero_rodada,
                            data_rodada=str(data_rodada),
                            mes_referencia=mes_ref,
                            ano_referencia=ano_ref,
                            status=status_rodada,
                            observacoes=obs_rodada if obs_rodada else None
                        )
                        st.success(f"✅ Rodada {numero_rodada} criada com sucesso!")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao criar rodada: {str(e)}")

# ========== TAB CLASSIFICAÇÕES ==========
with tab_classificacoes:
    st.header("🏆 Registro de Classificações")
    
    st.info("💡 **Fluxo**: Selecione uma rodada → Preencha os 3 primeiros colocados → Salve")
    
    # Verificar se há times e rodadas cadastrados
    times = db.listar_times(apenas_ativos=True)
    rodadas = db.listar_rodadas()
    
    if not times:
        st.warning("⚠️ Você precisa cadastrar times primeiro! Vá para a aba **Times**.")
        st.stop()
    
    if not rodadas:
        st.warning("⚠️ Você precisa cadastrar rodadas primeiro! Vá para a aba **Rodadas**.")
        st.stop()
    
    # Seletor de rodada
    col1, col2 = st.columns([1, 3])
    
    with col1:
        rodadas_opcoes = {r['numero']: r for r in rodadas}
        rodada_selecionada_num = st.selectbox(
            "Selecione a Rodada",
            options=sorted(rodadas_opcoes.keys()),
            format_func=lambda x: f"Rodada {x}"
        )
        
        rodada_selecionada = rodadas_opcoes[rodada_selecionada_num]
        rodada_id = rodada_selecionada['id']
        
        st.info(f"""
        **Data**: {rodada_selecionada['data_rodada']}  
        **Status**: {rodada_selecionada['status']}
        """)
    
    with col2:
        st.subheader(f"Rodada {rodada_selecionada_num} - Classificação")
        
        # Verificar se já existem classificações
        classificacoes_existentes = db.listar_classificacoes_rodada(rodada_id)
        
        if classificacoes_existentes:
            st.success("✅ Esta rodada já possui classificações registradas!")
            
            # Mostrar classificações existentes
            df_class = pd.DataFrame(classificacoes_existentes)
            st.dataframe(
                df_class[['posicao', 'times', 'pontuacao', 'valor_premio']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    'posicao': 'Posição',
                    'times': st.column_config.Column('Time', width='large'),
                    'pontuacao': st.column_config.NumberColumn('Pontuação', format="%.2f"),
                    'valor_premio': st.column_config.NumberColumn('Prêmio', format="R$ %.2f")
                }
            )
            
            st.warning("⚠️ Para editar, você precisará deletar as classificações existentes primeiro.")
        
        else:
            st.write("Preencha os 3 primeiros colocados:")
            
            with st.form("form_classificacoes"):
                # Buscar valores de premiação
                premiacoes = db.listar_premiacoes()
                valores_premio = {p['posicao']: p['valor'] for p in premiacoes}
                
                # Criar dicionário de times
                times_dict = {t['id']: f"{t['nome_time']} ({t['nome_dono']})" for t in times}
                
                st.markdown("### 🥇 Primeiro Lugar")
                col_t1, col_p1 = st.columns([2, 1])
                with col_t1:
                    time_1 = st.selectbox("Time", options=times_dict.keys(), 
                                         format_func=lambda x: times_dict[x], key="time_1")
                with col_p1:
                    pont_1 = st.number_input("Pontuação", min_value=0.0, step=0.01, key="pont_1")
                st.caption(f"💰 Prêmio: R$ {valores_premio[1]:.2f}")
                
                st.divider()
                
                st.markdown("### 🥈 Segundo Lugar")
                col_t2, col_p2 = st.columns([2, 1])
                with col_t2:
                    time_2 = st.selectbox("Time", options=times_dict.keys(), 
                                         format_func=lambda x: times_dict[x], key="time_2")
                with col_p2:
                    pont_2 = st.number_input("Pontuação", min_value=0.0, step=0.01, key="pont_2")
                st.caption(f"💰 Prêmio: R$ {valores_premio[2]:.2f}")
                
                st.divider()
                
                st.markdown("### 🥉 Terceiro Lugar")
                col_t3, col_p3 = st.columns([2, 1])
                with col_t3:
                    time_3 = st.selectbox("Time", options=times_dict.keys(), 
                                         format_func=lambda x: times_dict[x], key="time_3")
                with col_p3:
                    pont_3 = st.number_input("Pontuação", min_value=0.0, step=0.01, key="pont_3")
                st.caption(f"💰 Prêmio: R$ {valores_premio[3]:.2f}")
                
                st.divider()
                
                submit_class = st.form_submit_button("✅ Registrar Classificação", 
                                                     use_container_width=True,
                                                     type="primary")
                
                if submit_class:
                    # Validações
                    if time_1 == time_2 or time_1 == time_3 or time_2 == time_3:
                        st.error("❌ Um time não pode aparecer em múltiplas posições!")
                    elif pont_1 <= 0 or pont_2 <= 0 or pont_3 <= 0:
                        st.error("❌ Todas as pontuações devem ser maiores que zero!")
                    else:
                        try:
                            # Criar as 3 classificações
                            db.criar_classificacao(time_1, rodada_id, 1, pont_1, valores_premio[1])
                            db.criar_classificacao(time_2, rodada_id, 2, pont_2, valores_premio[2])
                            db.criar_classificacao(time_3, rodada_id, 3, pont_3, valores_premio[3])
                            
                            st.success(f"✅ Classificação da rodada {rodada_selecionada_num} registrada com sucesso!")
                            st.balloons()
                            st.rerun()
                        
                        except Exception as e:
                            st.error(f"❌ Erro ao registrar classificação: {str(e)}")