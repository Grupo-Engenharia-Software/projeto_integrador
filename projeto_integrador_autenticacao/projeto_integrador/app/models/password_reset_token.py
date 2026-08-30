"""
Model para os tokens de recuperação/troca de senha.

Um token é gerado quando o usuário pede para redefinir a senha, tem
validade curta e só pode ser usado uma vez (used=True depois de usado).
Isso evita que um link de recuperação antigo continue valendo para sempre.
"""
import secrets
from datetime import datetime, timedelta

from app.extensions import db

TOKEN_VALIDITY_MINUTES = 30


class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Token aleatório e único, gerado com o módulo "secrets" (seguro
    # criptograficamente, diferente do módulo "random").
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)

    @classmethod
    def create_for_user(cls, user_id: int) -> "PasswordResetToken":
        token = secrets.token_urlsafe(32)
        reset_token = cls(
            user_id=user_id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(minutes=TOKEN_VALIDITY_MINUTES),
        )
        db.session.add(reset_token)
        return reset_token

    def is_valid(self) -> bool:
        return (not self.used) and self.expires_at > datetime.utcnow()
