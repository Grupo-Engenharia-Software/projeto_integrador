"""
Formulários usados nas telas de autenticação.

Usar Flask-WTF (em vez de ler request.form diretamente) já nos dá:
  - proteção CSRF automática (token oculto validado em cada POST)
  - validação de campos no servidor (nunca confiar só no front-end)
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


MSG_REQUIRED = "Este campo é obrigatório."
MSG_EMAIL = "Informe um e-mail válido."


class RegisterForm(FlaskForm):
    name = StringField(
        "Nome completo",
        validators=[
            DataRequired(message=MSG_REQUIRED),
            Length(min=2, max=120, message="O nome deve ter entre 2 e 120 caracteres."),
        ],
    )
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message=MSG_REQUIRED),
            Email(message=MSG_EMAIL),
            Length(max=180),
        ],
    )
    password = PasswordField(
        "Senha",
        validators=[
            DataRequired(message=MSG_REQUIRED),
            Length(min=8, message="A senha deve ter no mínimo 8 caracteres."),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar senha",
        validators=[
            DataRequired(message=MSG_REQUIRED),
            EqualTo("password", message="As senhas não coincidem."),
        ],
    )
    submit = SubmitField("Criar conta")


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(message=MSG_REQUIRED), Email(message=MSG_EMAIL)])
    password = PasswordField("Senha", validators=[DataRequired(message=MSG_REQUIRED)])
    submit = SubmitField("Entrar")


class ForgotPasswordForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(message=MSG_REQUIRED), Email(message=MSG_EMAIL)])
    submit = SubmitField("Enviar link de recuperação")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Nova senha",
        validators=[
            DataRequired(message=MSG_REQUIRED),
            Length(min=8, message="A senha deve ter no mínimo 8 caracteres."),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar nova senha",
        validators=[
            DataRequired(message=MSG_REQUIRED),
            EqualTo("password", message="As senhas não coincidem."),
        ],
    )
    submit = SubmitField("Redefinir senha")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Senha atual", validators=[DataRequired(message=MSG_REQUIRED)])
    new_password = PasswordField(
        "Nova senha",
        validators=[
            DataRequired(message=MSG_REQUIRED),
            Length(min=8, message="A senha deve ter no mínimo 8 caracteres."),
        ],
    )
    confirm_new_password = PasswordField(
        "Confirmar nova senha",
        validators=[
            DataRequired(message=MSG_REQUIRED),
            EqualTo("new_password", message="As senhas não coincidem."),
        ],
    )
    submit = SubmitField("Alterar senha")
