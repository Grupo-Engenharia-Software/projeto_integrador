"""
Configurações da aplicação.

Todos os valores sensíveis (chave secreta, credenciais de banco) vêm de
variáveis de ambiente (arquivo .env), nunca ficam fixos no código-fonte.
Isso evita vazar segredos ao versionar o projeto no Git.
"""
import os
from dotenv import load_dotenv

# Carrega as variáveis definidas no arquivo .env para o ambiente do processo
load_dotenv()


class Config:
    # Chave usada pelo Flask para assinar cookies de sessão e tokens CSRF.
    # Se não houver uma definida no .env, a aplicação não deve subir em produção.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-nao-use-em-producao")

    # Conexão com o banco de dados PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/projeto_integrador"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Regras de gestão de credenciais (proteção contra força bruta)
    MAX_LOGIN_ATTEMPTS = int(os.environ.get("MAX_LOGIN_ATTEMPTS", 5))
    LOCKOUT_MINUTES = int(os.environ.get("LOCKOUT_MINUTES", 15))

    # Cookies de sessão mais seguros
    SESSION_COOKIE_HTTPONLY = True   # impede acesso ao cookie via JavaScript
    SESSION_COOKIE_SAMESITE = "Lax"  # mitiga ataques CSRF/clickjacking básicos
