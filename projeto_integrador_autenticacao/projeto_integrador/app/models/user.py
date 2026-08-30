"""
Model (camada M do MVC): define a estrutura da tabela de usuários e as
regras de negócio relacionadas diretamente aos dados do usuário
(hash/verificação de senha, controle de tentativas de login, bloqueio).
"""
from datetime import datetime, timedelta

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(UserMixin, db.Model):
    """
    UserMixin (do Flask-Login) fornece implementações padrão de
    is_authenticated, is_active, is_anonymous e get_id(), exigidas pelo
    gerenciador de sessão.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)

    # IMPORTANTE: nunca armazenamos a senha em texto puro.
    # Guardamos apenas o hash (PBKDF2-SHA256, gerado pelo werkzeug.security).
    password_hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # --- Gestão de credenciais: controle de tentativas / bloqueio temporário ---
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)

    # ------------------------------------------------------------------
    # Senha
    # ------------------------------------------------------------------
    def set_password(self, raw_password: str) -> None:
        """Gera o hash da senha informada e armazena no lugar do texto puro."""
        self.password_hash = generate_password_hash(raw_password, method="pbkdf2:sha256")

    def check_password(self, raw_password: str) -> bool:
        """Compara a senha informada com o hash armazenado (comparação segura)."""
        return check_password_hash(self.password_hash, raw_password)

    # ------------------------------------------------------------------
    # Proteção contra força bruta
    # ------------------------------------------------------------------
    def is_locked(self) -> bool:
        """Verifica se a conta está temporariamente bloqueada."""
        return bool(self.locked_until and self.locked_until > datetime.utcnow())

    def register_failed_attempt(self, max_attempts: int, lockout_minutes: int) -> None:
        """
        Incrementa o contador de tentativas falhas. Ao atingir o limite,
        bloqueia a conta por um período (lockout_minutes).
        """
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= max_attempts:
            self.locked_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)

    def reset_failed_attempts(self) -> None:
        """Zera o contador após um login bem-sucedido."""
        self.failed_login_attempts = 0
        self.locked_until = None

    def __repr__(self):
        return f"<User {self.email}>"
