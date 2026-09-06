# O "Model" fala com o banco de dados: salva e busca os
# usuários na tabela "usuarios".

from config.database import get_connection


def criar_tabela_usuarios():

   # Cria a tabela de usuários caso ela ainda não exista.

    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            email VARCHAR(150) UNIQUE NOT NULL,
            senha_hash VARCHAR(255) NOT NULL,
            salt VARCHAR(255) NOT NULL
        );
    """)

    conexao.commit()
    cursor.close()
    conexao.close()


def salvar_usuario(email, senha_hash, salt):

   # Salva um novo usuário no banco de dados.

    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO usuarios (email, senha_hash, salt) VALUES (%s, %s, %s)",
        (email, senha_hash, salt)
    )

    conexao.commit()
    cursor.close()
    conexao.close()


def buscar_usuario_por_email(email):

   # Busca um usuário pelo e-mail.
   # Retorna uma tupla (id, email, senha_hash, salt) ou None.

    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id, email, senha_hash, salt FROM usuarios WHERE email = %s",
        (email,)
    )
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario

def atualizar_senha_usuario(id_usuario, senha_hash, salt):
    
    # Atualiza o hash e o salt da senha de um usuário existente.
    # Usado no fluxo de recuperação de senha.
    
    conexao = get_connection()
    cursor = conexao.cursor()
 
    cursor.execute(
        "UPDATE usuarios SET senha_hash = %s, salt = %s WHERE id = %s",
        (senha_hash, salt, id_usuario)
    )
 
    conexao.commit()
    cursor.close()
    conexao.close()
