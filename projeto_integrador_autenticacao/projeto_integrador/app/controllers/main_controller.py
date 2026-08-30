"""
Controller com as rotas gerais da aplicação (fora do fluxo de autenticação
em si), usadas para demonstrar a proteção de rotas por sessão.
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required  # rota protegida: só acessível com sessão autenticada
def dashboard():
    return render_template("dashboard.html", user=current_user)
