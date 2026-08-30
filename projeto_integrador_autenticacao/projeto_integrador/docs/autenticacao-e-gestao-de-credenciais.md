# Autenticação e Gestão de Credenciais

Este documento descreve, de forma técnica, como o requisito **"Autenticação
e Gestão de Credenciais"** foi implementado, testado e evidenciado nesta
etapa do Projeto Integrador.

## 1. Visão geral

O módulo de autenticação foi implementado em Flask, seguindo o padrão MVC:

- **Model** (`app/models/user.py`, `app/models/password_reset_token.py`):
  estrutura de dados do usuário e das credenciais, e as regras de negócio
  diretamente ligadas a elas (hash de senha, controle de tentativas,
  bloqueio, tokens de redefinição).
- **View** (`app/views/*.html`): telas HTML (login, cadastro, recuperação
  de senha, alteração de senha, painel protegido) usadas para testar e
  demonstrar cada funcionalidade.
- **Controller** (`app/controllers/auth_controller.py`): rotas que recebem
  as requisições HTTP, aplicam as validações e coordenam Model e View.

## 2. Funcionalidades implementadas

| # | Funcionalidade | Onde está no código |
|---|-----------------|----------------------|
| 1 | Cadastro de usuário | `auth_controller.register()` |
| 2 | Hash de senha (nunca texto puro) | `User.set_password()` (PBKDF2-SHA256) |
| 3 | Login com verificação de credenciais | `auth_controller.login()` |
| 4 | Gestão de sessão do usuário autenticado | Flask-Login (`login_user`, `@login_required`) |
| 5 | Logout | `auth_controller.logout()` |
| 6 | Proteção de rotas | decorator `@login_required` em `/dashboard` e `/auth/alterar-senha` |
| 7 | Política de senha forte | `app/utils/security.py::validate_password_strength` |
| 8 | Bloqueio por tentativas inválidas (força bruta) | `User.register_failed_attempt`, `User.is_locked` |
| 9 | Limite de requisições por IP no login | `Flask-Limiter` em `auth_controller.login()` |
| 10 | Recuperação de senha por token com expiração | `PasswordResetToken`, `forgot_password()`, `reset_password()` |
| 11 | Token de redefinição de uso único | campo `used` em `PasswordResetToken` |
| 12 | Alteração de senha pelo próprio usuário | `auth_controller.change_password()` |
| 13 | Proteção CSRF em todos os formulários | Flask-WTF (`CSRFProtect`, `form.hidden_tag()`) |
| 14 | Cookies de sessão mais seguros | `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE` em `config.py` |
| 15 | Segredos fora do código-fonte | variáveis de ambiente via `.env` (não versionado) |

## 3. Decisões de segurança e por quê

- **Hash de senha com PBKDF2-SHA256** (`werkzeug.security`): a senha em
  texto puro nunca é armazenada nem logada. Mesmo que o banco de dados
  vaze, um invasor não recupera a senha original diretamente.
- **Mensagem de erro genérica no login** ("E-mail ou senha inválidos."):
  propositalmente não informa se o e-mail existe ou não, dificultando
  ataques de enumeração de contas.
- **Bloqueio temporário por conta** após N tentativas inválidas
  (configurável via `MAX_LOGIN_ATTEMPTS` e `LOCKOUT_MINUTES`), combinado
  com um limite de requisições por IP (`Flask-Limiter`), para dificultar
  ataques de força bruta tanto contra uma conta específica quanto vindos
  de um mesmo endereço.
- **Token de redefinição de senha** gerado com o módulo `secrets` (seguro
  criptograficamente), com validade de 30 minutos e uso único — depois de
  usado, o mesmo link não pode ser reaproveitado.
- **Proteção CSRF** em todos os formulários (Flask-WTF), evitando que um
  site malicioso induza o navegador do usuário a enviar requisições em
  seu nome.
- **Validação sempre no servidor**, nunca só no front-end: mesmo que o
  JavaScript do navegador seja desabilitado ou burlado, as regras de
  senha forte, e-mail único e confirmação de senha são reaplicadas nas
  rotas do Controller.

## 4. Como testar cada item pelo front-end

1. **Cadastro:** acessar `/auth/registrar`, preencher o formulário.
   Testar também com senha fraca (ex: `12345678`) para ver a mensagem de
   política de senha, e com um e-mail já cadastrado para ver o bloqueio
   de duplicidade.
2. **Login:** acessar `/auth/login` com as credenciais criadas.
3. **Sessão / rota protegida:** após logar, acessar `/dashboard`; deslogar
   e tentar acessar `/dashboard` novamente — deve redirecionar ao login.
4. **Bloqueio por tentativas:** errar a senha repetidamente (o padrão é
   5 tentativas, configurável no `.env`) e observar a mensagem de conta
   bloqueada temporariamente.
5. **Recuperação de senha:** em `/auth/esqueci-senha`, informar o e-mail
   cadastrado; o link de redefinição (que em produção seria enviado por
   e-mail) é exibido na tela para fins de teste acadêmico. Usar o link,
   definir uma nova senha e confirmar o login com ela.
6. **Token de uso único:** tentar reutilizar o mesmo link de redefinição
   após já tê-lo usado — deve ser recusado como inválido/expirado.
7. **Alterar senha:** logado, acessar "Alterar senha" no menu, informar a
   senha atual e a nova senha.
8. **CSRF:** qualquer tentativa de enviar um dos formulários sem o token
   oculto (`csrf_token`) é rejeitada pelo servidor com erro 400.

## 5. Limitações conhecidas / observações para a avaliação

- Em produção, o link de redefinição de senha seria enviado por e-mail
  através de um serviço de envio (ex: SMTP, SendGrid); como o ambiente
  acadêmico não possui esse serviço configurado, o link é exibido
  diretamente na tela para permitir o teste completo do fluxo via
  front-end.
- O `Flask-Limiter` está configurado com armazenamento em memória, o que
  é suficiente para esta entrega, mas não é recomendado para produção
  com múltiplas instâncias (nesse caso, se usaria Redis).
