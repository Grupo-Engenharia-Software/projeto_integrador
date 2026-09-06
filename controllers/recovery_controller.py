# controllers/recovery_controller.py
#
# Lógica de recuperação de senha: gerar token seguro, enviar
# por e-mail, validar o token e permitir a troca da senha.

import secrets
import smtplib
import bcrypt
from email.mime.text import MIMEText
from datetime import datetime, timedelta

from models.user_model import buscar_usuario_por_email, atualizar_senha_usuario
from models.token_model import salvar_token, buscar_token, marcar_token_como_usado
from config.email_config import EMAIL_REMETENTE, EMAIL_SENHA, SMTP_SERVIDOR, SMTP_PORTA
from config.logger import registrar_evento

BCRYPT_ROUNDS = 12

# Tempo (em minutos) que o token de recuperação continua válido
TEMPO_EXPIRACAO_TOKEN_MINUTOS = 30


def _enviar_email_recuperacao(email_destino, link_recuperacao):

    # Monta e envia o e-mail com o link de recuperação de senha.

    corpo_email = (
        "Recebemos uma solicitação para redefinir sua senha no CampusFlow.\n\n"
        f"Clique no link abaixo para criar uma nova senha:\n{link_recuperacao}\n\n"
        f"Este link expira em {TEMPO_EXPIRACAO_TOKEN_MINUTOS} minutos. "
        "Se você não solicitou isso, apenas ignore este e-mail."
    )

    mensagem = MIMEText(corpo_email)
    mensagem["Subject"] = "Recuperação de senha - CampusFlow"
    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = email_destino

    with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA) as servidor:
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
        servidor.sendmail(EMAIL_REMETENTE, email_destino, mensagem.as_string())


def solicitar_recuperacao_senha(email, url_base):

    registrar_evento(f"SOLICITACAO_RECUPERACAO | email={email}")

    usuario = buscar_usuario_por_email(email)

    if usuario is not None:
        id_usuario = usuario[0]

        token = secrets.token_urlsafe(32)

        criado_em = datetime.now()
        expira_em = criado_em + timedelta(minutes=TEMPO_EXPIRACAO_TOKEN_MINUTOS)

        salvar_token(id_usuario, token, criado_em, expira_em)

        link_recuperacao = f"{url_base}redefinir-senha/{token}"

        try:
            _enviar_email_recuperacao(email, link_recuperacao)
        except Exception as erro:
            # Se o e-mail falhar ao enviar, deixamos o link aparecer
            # no terminal, para não travar os testes do sistema.
            print(f"[Recuperação] Falha ao enviar e-mail: {erro}", flush=True)
            print(f"[Recuperação] Link para {email}: {link_recuperacao}", flush=True)

    # Mensagem genérica, igual tanto se o e-mail existe quanto se não existe
    return {
        "sucesso": True,
        "mensagem": "Se este e-mail estiver cadastrado, você receberá um link de recuperação."
    }


def validar_token_recuperacao(token):

    registro = buscar_token(token)

    if registro is None:
        return {"sucesso": False, "mensagem": "Link de recuperação inválido."}

    # registro = (id, id_usuario, token, criado_em, expira_em, usado)
    _, id_usuario, _, _, expira_em, usado = registro

    # Token já usado não pode ser usado de novo
    if usado:
        return {"sucesso": False, "mensagem": "Este link já foi utilizado."}

    # Falha correta quando o token expirou
    if datetime.now() > expira_em:
        return {"sucesso": False, "mensagem": "Este link de recuperação expirou."}

    return {"sucesso": True, "id_usuario": id_usuario}


def redefinir_senha(token, nova_senha):

    resultado_token = validar_token_recuperacao(token)

    if not resultado_token["sucesso"]:
        # Registra a falha no log
        registrar_evento(f"REDEFINICAO_SENHA_FALHA | token={token} | motivo={resultado_token['mensagem']}")
        return resultado_token

    id_usuario = resultado_token["id_usuario"]

    # Gera um novo hash + salt para a nova senha 
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    senha_hash = bcrypt.hashpw(nova_senha.encode("utf-8"), salt)

    atualizar_senha_usuario(
        id_usuario=id_usuario,
        senha_hash=senha_hash.decode("utf-8"),
        salt=salt.decode("utf-8")
    )

    # Marca o token como usado, para não ser reaproveitado
    marcar_token_como_usado(token)

    # Registra o sucesso da redefinição no log
    registrar_evento(f"REDEFINICAO_SENHA_SUCESSO | id_usuario={id_usuario}")

    return {"sucesso": True, "mensagem": "Senha redefinida com sucesso! Você já pode fazer login."}