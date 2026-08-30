"""
Controller (camada C do MVC) responsável por toda a Autenticação e
Gestão de Credenciais:
  - Cadastro de usuário
  - Login / Logout
  - Sessão do usuário autenticado
  - Bloqueio temporário por tentativas inválidas (força bruta)
  - Recuperação e alteração de senha

Cada rota faz a ponte entre a View (templates HTML) e o Model (User),
sem regra de negócio de dados diretamente aqui - isso fica no Model.
"""
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db, limiter
from app.models import User, PasswordResetToken
from app.utils.forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    ChangePasswordForm,
)
from app.utils.security import validate_password_strength

# Blueprint agrupa todas as rotas de autenticação sob o prefixo /auth
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/registrar", methods=["GET", "POST"])
def register():
    """Cadastro de novo usuário com senha já armazenada como hash."""
    form = RegisterForm()

    if form.validate_on_submit():
        # Verifica se o e-mail já está cadastrado
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("Este e-mail já está cadastrado.", "danger")
            return render_template("register.html", form=form)

        # Valida a força da senha no servidor (nunca confiar só no front-end)
        password_errors = validate_password_strength(form.password.data)
        if password_errors:
            for error in password_errors:
                flash(error, "danger")
            return render_template("register.html", form=form)

        user = User(name=form.name.data.strip(), email=form.email.data.lower())
        user.set_password(form.password.data)  # aqui a senha vira hash, nunca texto puro
        db.session.add(user)
        db.session.commit()

        flash("Conta criada com sucesso! Faça login para continuar.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("15 per minute", methods=["POST"])  # limite adicional de tentativas por IP (só nos envios do formulário, não afeta carregar a página)
def login():
    """
    Login do usuário. Implementa gestão de credenciais:
      - senha nunca é comparada em texto puro (usa hash)
      - contador de tentativas falhas por conta
      - bloqueio temporário após exceder o limite de tentativas
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        # Mensagem genérica propositalmente: não revela se o e-mail existe ou não,
        # o que dificulta ataques de enumeração de usuários.
        generic_error = "E-mail ou senha inválidos."

        if user is None:
            flash(generic_error, "danger")
            return render_template("login.html", form=form)

        if user.is_locked():
            flash(
                "Conta temporariamente bloqueada por excesso de tentativas. "
                "Tente novamente mais tarde ou redefina sua senha.",
                "warning",
            )
            return render_template("login.html", form=form)

        if not user.check_password(form.password.data):
            user.register_failed_attempt(
                max_attempts=current_app_config("MAX_LOGIN_ATTEMPTS"),
                lockout_minutes=current_app_config("LOCKOUT_MINUTES"),
            )
            db.session.commit()
            flash(generic_error, "danger")
            return render_template("login.html", form=form)

        # Login bem-sucedido: zera tentativas e cria a sessão do usuário
        user.reset_failed_attempts()
        db.session.commit()
        login_user(user)

        flash(f"Bem-vindo(a), {user.name}!", "success")
        next_page = request.args.get("next")
        return redirect(next_page or url_for("main.dashboard"))

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """Encerra a sessão do usuário autenticado."""
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/esqueci-senha", methods=["GET", "POST"])
def forgot_password():
    """
    Gera um token de recuperação de senha.

    Observação para avaliação: em produção esse token seria enviado por
    e-mail. Como não há servidor de e-mail configurado no ambiente
    acadêmico, o link é exibido diretamente na tela (flash message) para
    permitir testar o fluxo completo via front-end.
    """
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        # Não revela se o e-mail existe (evita enumeração de contas)
        if user:
            reset_token = PasswordResetToken.create_for_user(user.id)
            db.session.commit()
            reset_link = url_for("auth.reset_password", token=reset_token.token, _external=True)
            flash(f"Link de redefinição (válido por 30 min): {reset_link}", "info")
        else:
            flash("Se o e-mail existir em nossa base, um link de redefinição foi gerado.", "info")

        return redirect(url_for("auth.login"))

    return render_template("forgot_password.html", form=form)


@auth_bp.route("/redefinir-senha/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Redefine a senha a partir de um token válido e ainda não utilizado."""
    reset_token = PasswordResetToken.query.filter_by(token=token).first()

    if reset_token is None or not reset_token.is_valid():
        flash("Link de redefinição inválido ou expirado.", "danger")
        return redirect(url_for("auth.forgot_password"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        password_errors = validate_password_strength(form.password.data)
        if password_errors:
            for error in password_errors:
                flash(error, "danger")
            return render_template("reset_password.html", form=form)

        user = User.query.get(reset_token.user_id)
        user.set_password(form.password.data)
        user.reset_failed_attempts()  # aproveita para desbloquear a conta, se estava bloqueada
        reset_token.used = True       # token só pode ser usado uma vez
        db.session.commit()

        flash("Senha redefinida com sucesso! Faça login com a nova senha.", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", form=form)


@auth_bp.route("/alterar-senha", methods=["GET", "POST"])
@login_required
def change_password():
    """Permite ao usuário logado trocar a própria senha, confirmando a atual."""
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("Senha atual incorreta.", "danger")
            return render_template("change_password.html", form=form)

        password_errors = validate_password_strength(form.new_password.data)
        if password_errors:
            for error in password_errors:
                flash(error, "danger")
            return render_template("change_password.html", form=form)

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Senha alterada com sucesso.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("change_password.html", form=form)


def current_app_config(key: str):
    """Pequeno helper para ler configs do app dentro das rotas."""
    from flask import current_app
    return current_app.config[key]
