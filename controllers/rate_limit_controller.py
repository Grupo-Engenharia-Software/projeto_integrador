from datetime import datetime, timedelta

# Quantas tentativas erradas são permitidas antes de bloquear
LIMITE_TENTATIVAS = 5

# Por quanto tempo o e-mail fica bloqueado após atingir o limite
TEMPO_BLOQUEIO_MINUTOS = 3

# Dicionário que guarda o controle de tentativas de cada e-mail.
# Formato: { "email@exemplo.com": {"tentativas": 2, "bloqueado_ate": None} }
controle_tentativas = {}


def esta_bloqueado(email):

   # Verifica se o e-mail informado está atualmente bloqueado por excesso de tentativas erradas.

    registro = controle_tentativas.get(email)

    if registro is None or registro["bloqueado_ate"] is None:
        return None

    agora = datetime.now()

    if agora >= registro["bloqueado_ate"]:
        # O tempo de bloqueio já passou: reseta o controle deste e-mail
        controle_tentativas.pop(email, None)
        return None

    segundos_restantes = int((registro["bloqueado_ate"] - agora).total_seconds())
    return segundos_restantes


def registrar_tentativa_falha(email):

   # Soma mais uma tentativa errada para o e-mail informado.
   # Se atingir o limite, marca o e-mail como bloqueado.

    registro = controle_tentativas.get(email, {"tentativas": 0, "bloqueado_ate": None})
    registro["tentativas"] += 1

    if registro["tentativas"] >= LIMITE_TENTATIVAS:
        registro["bloqueado_ate"] = datetime.now() + timedelta(minutes=TEMPO_BLOQUEIO_MINUTOS)

    controle_tentativas[email] = registro


def resetar_tentativas(email):

   # Zera o controle de tentativas de um e-mail. Deve ser chamado
   # sempre que o login for bem-sucedido, para não deixar um
   # histórico de erros antigos afetando logins futuros.

    controle_tentativas.pop(email, None)