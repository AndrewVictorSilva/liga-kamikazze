"""
Core module - contém a lógica de negócio da aplicação
"""
from .database import db, Database
from .auth import check_password, logout, require_auth, show_logout_button

__all__ = [
    'db',
    'Database',
    'check_password',
    'logout',
    'require_auth',
    'show_logout_button'
]