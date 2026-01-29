"""
Configurações centralizadas da aplicação
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Configurações de Autenticação
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# Configurações da Aplicação
APP_TITLE = "🏆 Cartola FC - Premiação"
APP_ICON = "🏆"

# Configurações de Premiação (valores padrão)
PREMIACOES_PADRAO = {
    1: 45.00,
    2: 30.00,
    3: 20.00
}

# Número de rodadas do campeonato
NUM_RODADAS = 38

# Status possíveis das rodadas
STATUS_RODADAS = ["aberta", "em_andamento", "fechada"]

# Meses do ano (para filtros)
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