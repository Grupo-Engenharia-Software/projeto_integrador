from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from models.token_model import criar_tabela_tokens

from models.user_model import criar_tabela_usuarios
from controllers.auth_controller import (
    registrar_usuario,
    autenticar_usuario,
    gerar_codigo_2fa,
    verificar_codigo_2fa,
)
from controllers.rate_limit_controller import (
    esta_bloqueado,
    registrar_tentativa_falha,
    resetar_tentativas,
)
from controllers.recovery_controller import (
    solicitar_recuperacao_senha,
    validar_token_recuperacao,
    redefinir_senha as redefinir_senha_controller,
)

# Carrega as variáveis definidas no arquivo .env
load_dotenv()

app = Flask(__name__)

# Chave secreta usada pelo Flask para proteger a sessão do usuário
app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.permanent_session_lifetime = timedelta(minutes=15)


@app.before_request
def tornar_sessao_permanente():
    # Marca a sessão como "permanente", o que faz o Flask aplicar
    # o tempo de expiração definido em permanent_session_lifetime.
    session.permanent = True



# Rota de cadastro de usuário

@app.route("/register", methods=["GET", "POST"])
def register():
    # GET: apenas exibe o formulário de cadastro, sem mensagem
    if request.method == "GET":
        return render_template("register.html")

    # POST: o usuário enviou o formulário
    email = request.form.get("email")
    senha = request.form.get("password")

    if not email or not senha:
        return render_template(
            "register.html",
            mensagem="E-mail e senha são obrigatórios.",
            sucesso=False
        )

    resultado = registrar_usuario(email, senha)

    if resultado["sucesso"]:
        # Depois de cadastrar, redireciona o usuário para a tela de login
        return redirect(url_for("login"))

    return render_template(
        "register.html",
        mensagem=resultado["mensagem"],
        sucesso=False
    )

# Rota de login (autenticação)

@app.route("/login", methods=["GET", "POST"])
def login():
    # GET: apenas exibe o formulário de login, sem mensagem
    if request.method == "GET":
        return render_template("login.html")

    # POST: o usuário enviou o formulário
    email = request.form.get("email")
    senha = request.form.get("password")

    if not email or not senha:
        return render_template(
            "login.html",
            mensagem="E-mail e senha são obrigatórios.",
            sucesso=False
        )

    segundos_bloqueado = esta_bloqueado(email)
    if segundos_bloqueado is not None:
        minutos_restantes = (segundos_bloqueado // 60) + 1
        return render_template(
            "login.html",
            mensagem=f"Muitas tentativas erradas. Tente novamente em {minutos_restantes} minuto(s).",
            sucesso=False
        )

    resultado = autenticar_usuario(email, senha)

    if not resultado["sucesso"]:
        # Registra mais uma tentativa errada para
        # este e-mail. Se atingir o limite, ele passa a ser bloqueado
        registrar_tentativa_falha(email)

        # Login inválido: mostra o formulário de novo, com a mensagem de erro
        return render_template(
            "login.html",
            mensagem=resultado["mensagem"],
            sucesso=False
        )

    # Login correto: zera o histórico de tentativas erradas deste e-mail
    resetar_tentativas(email)

    codigo, horario_geracao = gerar_codigo_2fa(email)

    session["2fa_id_usuario_pendente"] = resultado["id_usuario"]
    session["2fa_email_pendente"] = email
    session["2fa_codigo"] = codigo
    session["2fa_horario_geracao"] = horario_geracao.isoformat()

    return redirect(url_for("verificar_2fa"))

@app.route("/verificar-2fa", methods=["GET", "POST"])
def verificar_2fa():

    if "2fa_codigo" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("two_factor.html")

    codigo_digitado = request.form.get("codigo")

    # Recupera da sessão os dados guardados temporariamente no login
    codigo_correto = session["2fa_codigo"]
    horario_geracao = datetime.fromisoformat(session["2fa_horario_geracao"])

    resultado = verificar_codigo_2fa(codigo_digitado, codigo_correto, horario_geracao)

    if not resultado["sucesso"]:
        return render_template(
            "two_factor.html",
            mensagem=resultado["mensagem"],
            sucesso=False
        )

    session["id_usuario"] = session["2fa_id_usuario_pendente"]
    session["email"] = session["2fa_email_pendente"]

    # Limpa os dados temporários do 2FA, já que não são mais necessários
    session.pop("2fa_id_usuario_pendente", None)
    session.pop("2fa_email_pendente", None)
    session.pop("2fa_codigo", None)
    session.pop("2fa_horario_geracao", None)

    return redirect(url_for("dashboard"))

# Rota para solicitar a recuperação de senha.

@app.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    if request.method == "GET":
        return render_template("forgot_password.html")
 
    email = request.form.get("email")
 
    if not email:
        return render_template(
            "forgot_password.html",
            mensagem="Informe um e-mail.",
            sucesso=False
        )
 
    resultado = solicitar_recuperacao_senha(email, request.url_root)
 
    return render_template(
        "forgot_password.html",
        mensagem=resultado["mensagem"],
        sucesso=resultado["sucesso"]
    )

# Rota para redefinir a senha usando o token recebido por e-mail

@app.route("/redefinir-senha/<token>", methods=["GET", "POST"])
def redefinir_senha(token):
    if request.method == "GET":
        resultado_token = validar_token_recuperacao(token)
 
        if not resultado_token["sucesso"]:
            return render_template(
                "reset_password.html",
                token_valido=False,
                mensagem=resultado_token["mensagem"]
            )
 
        return render_template("reset_password.html", token_valido=True, token=token)
 
    # POST: o usuário enviou a nova senha
    nova_senha = request.form.get("password")
    confirmar_senha = request.form.get("confirmar_senha")
 
    if not nova_senha or nova_senha != confirmar_senha:
        return render_template(
            "reset_password.html",
            token_valido=True,
            token=token,
            mensagem="As senhas não coincidem.",
            sucesso=False
        )
 
    resultado = redefinir_senha_controller(token, nova_senha)
 
    if not resultado["sucesso"]:
        return render_template(
            "reset_password.html",
            token_valido=False,
            mensagem=resultado["mensagem"]
        )
 
    # Senha redefinida com sucesso: manda para o login com a mensagem
    return render_template(
        "login.html",
        mensagem=resultado["mensagem"],
        sucesso=True
    )
 

# Rota da área logada (só acessível após login)

@app.route("/dashboard")
def dashboard():
    # Se não houver usuário na sessão, manda de volta para o login
    if "id_usuario" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", email=session["email"])

# Rota de logout

@app.route("/logout")
def logout():
    # Remove todos os dados da sessão
    session.clear()
    return redirect(url_for("login"))

# Início da aplicação

if __name__ == "__main__":
    criar_tabela_usuarios()
    criar_tabela_tokens()
    app.run(debug=True, port=5000)