"""
Módulo de autenticação e controle de acesso
"""
import streamlit as st
from typing import Optional
import config


def check_password() -> bool:
    """
    Verifica se o usuário está autenticado como admin.
    Retorna True se autenticado, False caso contrário.
    """
    
    # Verifica se já está autenticado na sessão
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        return True
    
    # Formulário de login
    st.subheader("🔐 Área do Administrador")
    st.write("Digite a senha para acessar as funções administrativas.")
    
    password = st.text_input("Senha:", type="password", key="password_input")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("Entrar", use_container_width=True):
            if password == config.ADMIN_PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("❌ Senha incorreta!")
    
    return False


def logout():
    """Realiza logout do admin"""
    st.session_state.authenticated = False
    st.success("Logout realizado com sucesso!")
    st.rerun()


def show_logout_button():
    """Mostra botão de logout no sidebar"""
    if st.session_state.get("authenticated", False):
        with st.sidebar:
            st.divider()
            if st.button("🚪 Sair", use_container_width=True):
                logout()


def require_auth(func):
    """
    Decorator para proteger páginas que requerem autenticação.
    
    Uso:
    @require_auth
    def minha_pagina():
        st.write("Conteúdo protegido")
    """
    def wrapper(*args, **kwargs):
        if check_password():
            return func(*args, **kwargs)
        else:
            st.warning("⚠️ Faça login para acessar esta página.")
            st.stop()
    return wrapper