# Projeto Integrador

Sistema web desenvolvido em Python seguindo o padrão arquitetural **MVC**,
como parte da disciplina de Engenharia de Software.

Esta entrega cobre o item de check-list **"1. Autenticação e Gestão de
Credenciais"**.

## Arquitetura

MVC (Model-View-Controller)

## Stack

| Camada     | Tecnologia                          |
|------------|--------------------------------------|
| Linguagem  | Python 3.12                          |
| Framework  | Flask                                |
| Front-end  | HTML, CSS e JavaScript               |
| Banco de Dados | PostgreSQL                       |
| ORM        | SQLAlchemy (Flask-SQLAlchemy)        |
| Sessão     | Flask-Login                          |
| Formulários / CSRF | Flask-WTF                    |
| Rate limiting | Flask-Limiter                     |

## Estrutura do projeto (MVC)

```
app/
  models/          -> Model: User, PasswordResetToken (SQLAlchemy)
  controllers/      -> Controller: auth_controller.py, main_controller.py (Blueprints/rotas)
  views/            -> View: templates HTML (Jinja2)
  static/           -> CSS e JS
  utils/            -> validações e formulários (WTForms)
  config.py         -> configurações lidas de variáveis de ambiente
  extensions.py     -> instâncias das extensões Flask (db, login, csrf, limiter)
docs/               -> documentação técnica e checklist do projeto
run.py              -> ponto de entrada da aplicação
docker-compose.yml  -> sobe o PostgreSQL localmente
```

## Como rodar o projeto localmente

### 1. Pré-requisitos
- Python 3.10+
- Docker e Docker Compose (para o banco PostgreSQL)

### 2. Clonar o repositório
```bash
git clone https://github.com/Grupo-Engenharia-Software/projeto_integrador.git
cd projeto_integrador
```

### 3. Criar e ativar o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 4. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 5. Configurar as variáveis de ambiente
```bash
cp .env.example .env
# edite o .env e gere uma SECRET_KEY própria com:
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6. Subir o banco de dados PostgreSQL
```bash
docker compose up -d
```

### 7. Rodar a aplicação
```bash
python run.py
```

A aplicação sobe em `http://localhost:5000`. As tabelas do banco são
criadas automaticamente na primeira execução.

## Testando pelo front-end

1. Acesse `http://localhost:5000/auth/registrar` e crie uma conta.
2. Faça login em `http://localhost:5000/auth/login`.
3. Você será redirecionado ao painel protegido (`/dashboard`), que só é
   acessível com sessão autenticada.
4. Teste o bloqueio por força bruta errando a senha repetidamente.
5. Teste "Esqueci minha senha" e o link de redefinição gerado.
6. Estando logado, teste "Alterar senha" no menu superior.
7. Clique em "Sair" para encerrar a sessão e confirme que `/dashboard`
   deixa de ser acessível (redireciona para o login).

Mais detalhes de cada requisito, com evidências, estão em
[`docs/autenticacao-e-gestao-de-credenciais.md`](docs/autenticacao-e-gestao-de-credenciais.md).

## Licença

MIT License
