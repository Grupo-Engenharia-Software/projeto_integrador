
import bcrypt
import random
import string
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from models.user_model import salvar_usuario, buscar_usuario_por_email
from config.email_config import EMAIL_REMETENTE, EMAIL_SENHA, SMTP_SERVIDOR, SMTP_PORTA

BCRYPT_ROUNDS = 12


def registrar_usuario(email, senha):

    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)

    senha_hash = bcrypt.hashpw(senha.encode("utf-8"), salt)

    salvar_usuario(
        email=email,
        senha_hash=senha_hash.decode("utf-8"),
        salt=salt.decode("utf-8")
    )

    return {"sucesso": True, "mensagem": "Usuário registrado com sucesso!"}


def autenticar_usuario(email, senha):

    # Verifica se o e-mail e a senha informados são válidos.

    usuario = buscar_usuario_por_email(email)

    if usuario is None:
        return {"sucesso": False, "mensagem": "Credenciais inválidas."}

    # usuario é a tupla (id, email, senha_hash, salt)
    senha_hash_salva = usuario[2]

    senha_confere = bcrypt.checkpw(
        senha.encode("utf-8"),
        senha_hash_salva.encode("utf-8")
    )

    if not senha_confere:
        return {"sucesso": False, "mensagem": "Credenciais inválidas."}

    return {"sucesso": True, "mensagem": "Login realizado com sucesso!", "id_usuario": usuario[0]}

# Tempo (em minutos) que o código de 2FA continua válido
TEMPO_EXPIRACAO_CODIGO_MINUTOS = 5


def enviar_email_codigo(email_destino, codigo):

   # Monta e envia o e-mail com o código de verificação,
   # usando o servidor SMTP configurado em email_config.py.

    corpo_email = (
        f"Seu código de verificação é: {codigo}\n\n"
        f"Este código expira em {TEMPO_EXPIRACAO_CODIGO_MINUTOS} minutos."
    )

    mensagem = MIMEText(corpo_email)
    mensagem["Subject"] = "Código de verificação - CampusFlow"
    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = email_destino

    # Conecta no servidor SMTP do Gmail e envia o e-mail.
    # starttls() ativa a conexão criptografada (segurança no envio).
    with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA) as servidor:
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
        servidor.sendmail(EMAIL_REMETENTE, email_destino, mensagem.as_string())


def gerar_codigo_2fa(email):
    
   # Gera um código numérico de 6 dígitos para a verificação
   # em duas etapas e envia ele por e-mail para o usuário.

    codigo = "".join(random.choices(string.digits, k=6))
    horario_geracao = datetime.now()

    try:
        enviar_email_codigo(email, codigo)
    except Exception as erro:
        print(f"[2FA] Falha ao enviar e-mail: {erro}", flush=True)
        print(f"[2FA] Código gerado para {email}: {codigo}", flush=True)

    return codigo, horario_geracao


def verificar_codigo_2fa(codigo_digitado, codigo_correto, horario_geracao):

    if codigo_digitado != codigo_correto:
        return {"sucesso": False, "mensagem": "Código incorreto."}

    tempo_passado = datetime.now() - horario_geracao
    if tempo_passado > timedelta(minutes=TEMPO_EXPIRACAO_CODIGO_MINUTOS):
        return {"sucesso": False, "mensagem": "Código expirado. Faça login novamente."}

    return {"sucesso": True, "mensagem": "Código verificado com sucesso!"}
