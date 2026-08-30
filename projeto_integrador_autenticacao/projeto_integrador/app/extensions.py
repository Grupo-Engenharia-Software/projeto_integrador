"""
Instâncias das extensões Flask, criadas separadamente para evitar
importação circular entre app/__init__.py e os controllers/models.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ORM - camada de acesso ao banco (usado pelos Models)
db = SQLAlchemy()

# Gestão de sessão de usuário autenticado (quem está logado, cookies, etc.)
login_manager = LoginManager()
login_manager.login_view = "auth.login"          # rota para onde redireciona se não autenticado
login_manager.login_message = "Faça login para acessar esta página."
login_manager.login_message_category = "warning"

# Proteção contra CSRF em todos os formulários (Flask-WTF)
csrf = CSRFProtect()

# Limitador de requisições - usado para travar tentativas repetidas de login
# (defesa adicional contra força bruta, além do bloqueio por conta)
limiter = Limiter(key_func=get_remote_address)
