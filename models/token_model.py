# models/token_model.py
#
# O "Model" responsável por guardar e buscar os tokens de
# recuperação de senha no banco de dados.

from config.database import get_connection


def criar_tabela_tokens():
    
    # Cria a tabela de tokens de recuperação de senha, caso ela
    # ainda não exista.

    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens_recuperacao (
            id SERIAL PRIMARY KEY,
            id_usuario INTEGER NOT NULL REFERENCES usuarios(id),
            token VARCHAR(255) UNIQUE NOT NULL,
            criado_em TIMESTAMP NOT NULL,
            expira_em TIMESTAMP NOT NULL,
            usado BOOLEAN NOT NULL DEFAULT FALSE
        );
    """)

    conexao.commit()
    cursor.close()
    conexao.close()


def salvar_token(id_usuario, token, criado_em, expira_em):

    # Salva um novo token de recuperação de senha no banco.
    
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO tokens_recuperacao (id_usuario, token, criado_em, expira_em)
        VALUES (%s, %s, %s, %s)
        """,
        (id_usuario, token, criado_em, expira_em)
    )

    conexao.commit()
    cursor.close()
    conexao.close()


def buscar_token(token):
    
    # Busca um token de recuperação de senha pelo valor do token.
    # Retorna uma tupla (id, id_usuario, token, criado_em, expira_em, usado)
    # ou None se o token não existir.
    
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id, id_usuario, token, criado_em, expira_em, usado
        FROM tokens_recuperacao
        WHERE token = %s
        """,
        (token,)
    )
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado


def marcar_token_como_usado(token):
    
    # Marca um token como já utilizado, para que
    # ele não possa ser usado novamente em uma segunda tentativa.

    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE tokens_recuperacao SET usado = TRUE WHERE token = %s",
        (token,)
    )

    conexao.commit()
    cursor.close()
    conexao.close()