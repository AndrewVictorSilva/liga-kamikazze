"""
Configurações centralizadas da aplicação
"""

import os
import streamlit as st
from pathlib import Path



# ==============================
# Loader inteligente de secrets
# ==============================

def load_local_env():
    """
    Carrega .env relativo ao arquivo config.py
    """
    env_path = Path(__file__).parent.parent / ".env"

    if env_path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=env_path)
        except ImportError:
            pass


def get_secret(key: str):
    """
    Prioridade:
    1 - Streamlit Secrets (produção)
    2 - Variável de ambiente / .env (local)
    """
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)


# Carrega .env apenas local
load_local_env()


# ==============================
# Supabase
# ==============================

SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")


# ==============================
# Autenticação
# ==============================

ADMIN_PASSWORD = get_secret("ADMIN_PASSWORD")


# ==============================
# App Config
# ==============================

APP_TITLE = "🏆 Cartola FC - Premiação"
APP_ICON = "🏆"


# ==============================
# Premiações padrão
# ==============================

PREMIACOES_PADRAO = {
    1: 45.00,
    2: 30.00,
    3: 20.00
}


# ==============================
# Campeonato
# ==============================

NUM_RODADAS = 38

STATUS_RODADAS = [
    "aberta",
    "em_andamento",
    "fechada"
]


# ==============================
# Meses
# ==============================

MESES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}
