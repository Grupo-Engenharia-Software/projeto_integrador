import os
from dotenv import load_dotenv

# Carrega as variáveis definidas no arquivo .env
load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")

SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PORTA = 587