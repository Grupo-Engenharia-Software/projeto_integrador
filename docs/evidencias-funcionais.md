# Evidências Funcionais

Este documento orienta quais evidências (prints de tela, e/ou vídeo)
devem ser capturadas para comprovar o funcionamento de cada requisito
do checklist, conforme exigido pelo item **"Testes via Front-end"**
das diretrizes de entrega.

## Checklist de evidências

### Etapa 1 — Autenticação e Gestão de Credenciais

- [x] **Cadastro de usuário** — tela de registro preenchida.

      ![Cadastro de usuário](evidencias/01 - Tela de cadastro preenchida.png)

- [x] **Banco de dados** — print da tabela `usuarios` mostrando que a senha está salva como
      hash + salt, nunca em texto puro. *(Requisitos 1.1 a 1.4)*

      ![Banco de dados](evidencias/02 - Tabela usuarios no banco.png)

- [x] **Login com credenciais corretas** — tela de login preenchida e
      redirecionamento para a verificação de 2FA.

      ![Login com credenciais corretas](evidencias/03 - Login com e-mailsenha corretos.png)

- [x] **E-mail com o código de 2FA recebido** — print da caixa de
      entrada mostrando o e-mail chegando com o código de 6 dígitos.
      *(Requisito 1.5)*

      ![E-mail com o código de 2FA recebido](evidencias/04 - E-mail recebido na caixa de entrada com o código de 6 dígitos.png)

- [x] **Verificação do código de 2FA com sucesso** — tela digitando o
      código e sendo redirecionado ao dashboard. *(Requisito 1.6)*

      ![Verificação do código de 2FA com sucesso](evidencias/05 - Digitando o código certo.png)

- [x] **Tentativa com código de 2FA incorreto** — mensagem de erro
      "Código incorreto". *(Requisito 1.6)*

      ![Tentativa com código de 2FA incorreto](evidencias/06 - Digitando o código errado.png)

- [x] **Login com credenciais inválidas** — mensagem de erro
      "Credenciais inválidas".

      ![Login com credenciais inválidas](evidencias/07 - Login com e-mailsenha inválidos.png)

- [x] **Sessão ativa** — acesso ao `/dashboard` mostrando o e-mail do
      usuário logado.

      ![Sessão ativa](evidencias/08 - Tela do dashboard mostrando o e-mail do usuário logado.png)

- [x] **Bloqueio por força bruta** — errar a senha 5 vezes seguidas e
      receber a mensagem de bloqueio temporário na 6ª tentativa.
      *(Requisito 1.11)*

      ![Bloqueio por força bruta](evidencias/09 - Errar a senha 5 vezes seguidas → na 6ª tentativa aparece a mensagem de bloqueio temporário.png)

### Etapa 2 — Recuperação de Senha

- [x] **Solicitação de recuperação** — tela `/esqueci-senha` preenchida
      e mensagem genérica de confirmação exibida. *(Requisito 2.1)*

      ![Solicitação de recuperação](evidencias/10 - Tela esqueci senha preenchida e confirmação exibida.png)      

- [x] **E-mail de recuperação recebido** — print da caixa de entrada
      mostrando o link de redefinição. *(Requisitos 2.1, 2.2)*

      ![E-mail de recuperação recebido](evidencias/11 - Token recebido.png) 

- [x] **Redefinição de senha com sucesso** — tela de nova senha
      preenchida e redirecionamento ao login com mensagem de sucesso.
      *(Requisitos 2.1, 2.3, 2.4)*

      ![Redefinição de senha com sucesso](evidencias/12 - Tela alteração de senha preenchida.png) 
      !(evidencias/13 - Mensagem de sucesso na troca de senha.png) 

- [x] **Tentativa de reutilizar o mesmo link** — acessar o mesmo link
      de recuperação uma segunda vez após já ter sido usado, e receber
      a mensagem "Este link já foi utilizado". *(Requisito 2.4)*

      ![Tentativa de reutilizar o mesmo link](evidencias/14 - Tentativa de usar o mesmo link.png)

- [x] **Token expirado** — acessar um link de recuperação depois de
      mais de 30 minutos e receber a mensagem "Este link de
      recuperação expirou". *(Requisito 2.5)*

      ![Token expirado](evidencias/17 - Link de recuperação expirado.png)

- [x] **Log de eventos** — print do conteúdo do arquivo
      `logs/eventos.log` mostrando as linhas de `SOLICITACAO_RECUPERACAO`,
      `REDEFINICAO_SENHA_SUCESSO`

      ![Log de eventos](evidencias/15 - Solicitação recuperação.png)
      (evidencias/16 - Redefinição senha sucesso.png)

- [x] **Video requesito 2** — Video mostrando o processo de recuperação de senha.

      (evidencias/Requesito 2.mp4)
