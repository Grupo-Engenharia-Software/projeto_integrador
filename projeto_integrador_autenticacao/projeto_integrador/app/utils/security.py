"""
Funções auxiliares de segurança que não pertencem a um Model específico.
"""
import re


def validate_password_strength(password: str) -> list[str]:
    """
    Valida se a senha atende à política mínima de segurança.
    Retorna uma lista de erros (vazia = senha válida).

    Política aplicada:
      - mínimo de 8 caracteres
      - pelo menos 1 letra maiúscula
      - pelo menos 1 letra minúscula
      - pelo menos 1 número
      - pelo menos 1 caractere especial
    """
    errors = []

    if len(password) < 8:
        errors.append("A senha deve ter no mínimo 8 caracteres.")
    if not re.search(r"[A-Z]", password):
        errors.append("A senha deve conter ao menos uma letra maiúscula.")
    if not re.search(r"[a-z]", password):
        errors.append("A senha deve conter ao menos uma letra minúscula.")
    if not re.search(r"[0-9]", password):
        errors.append("A senha deve conter ao menos um número.")
    if not re.search(r"[^A-Za-z0-9]", password):
        errors.append("A senha deve conter ao menos um caractere especial (ex: !@#$%).")

    return errors
