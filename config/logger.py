# config/logger.py
#
# Módulo responsável por registrar eventos importantes de
# segurança em um arquivo de log, usando o módulo "logging"
# nativo do Python.

import logging
import os

# Garante que a pasta "logs" existe antes de tentar escrever nela
os.makedirs("logs", exist_ok=True)

# Configuração do logger: cada linha salva vai ter data/hora,
# nível (INFO, WARNING, etc.) e a mensagem do evento.
logging.basicConfig(
    filename="logs/eventos.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("campusflow")


def registrar_evento(mensagem):
    
    # Registra uma linha no arquivo logs/eventos.log, com data e
    # hora automáticas. Usado para deixar rastro de eventos de
    # segurança, como solicitações de recuperação de senha e o
    # resultado (sucesso ou falha) de cada tentativa.
    
    logger.info(mensagem)