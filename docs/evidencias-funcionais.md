# Evidências Funcionais

Este documento orienta quais evidências (prints de tela, e/ou vídeo)
devem ser capturadas para comprovar o funcionamento de cada requisito
do checklist, conforme exigido pelo item **"Testes via Front-end"**
das diretrizes de entrega.

> ⚠️ As imagens abaixo precisam ser capturadas por vocês, testando o
> sistema rodando de verdade, e salvas na pasta `docs/evidencias/`.
> Depois de capturar, adicione os links das imagens neste arquivo no
> lugar dos itens `[ ]`.

## Como organizar

Crie a pasta `docs/evidencias/` e salve os prints com nomes claros,
por exemplo:

```
docs/evidencias/
 ├── 01-cadastro-usuario.png
 ├── 02-login-sucesso.png
 ├── 03-2fa-email-recebido.png
 ├── 04-2fa-codigo-verificado.png
 ├── 05-login-credenciais-invalidas.png
 ├── 06-sessao-expirada.png
 ├── 07-logout.png
 ├── 08-rate-limit-bloqueio.png
 └── 09-banco-hash-salt.png
```

## Checklist de evidências

- [ ] **Cadastro de usuário** — tela de registro preenchida e
      confirmação de sucesso.
- [ ] **Banco de dados** — print da tabela `usuarios` (via pgAdmin ou
      terminal do PostgreSQL) mostrando que a senha está salva como
      hash + salt, nunca em texto puro. *(Requisitos 1.1 a 1.4)*
- [ ] **Login com credenciais corretas** — tela de login preenchida e
      redirecionamento para a verificação de 2FA.
- [ ] **E-mail com o código de 2FA recebido** — print da caixa de
      entrada mostrando o e-mail chegando com o código de 6 dígitos.
      *(Requisito 1.5)*
- [ ] **Verificação do código de 2FA com sucesso** — tela digitando o
      código e sendo redirecionado ao dashboard. *(Requisito 1.6)*
- [ ] **Tentativa com código de 2FA incorreto** — mensagem de erro
      "Código incorreto". *(Requisito 1.6)*
- [ ] **Login com credenciais inválidas** — mensagem de erro
      "Credenciais inválidas".
- [ ] **Sessão ativa** — acesso ao `/dashboard` mostrando o e-mail do
      usuário logado.
- [ ] **Logout** — botão "Sair" sendo clicado e redirecionamento de
      volta ao login, com o `/dashboard` bloqueado em seguida.
      *(Requisito 1.10)*
- [ ] **Expiração de sessão** — acessar `/dashboard` depois de mais de
      15 minutos sem uso e ser redirecionado ao login automaticamente.
      *(Requisito 1.9)*
- [ ] **Bloqueio por força bruta** — errar a senha 5 vezes seguidas e
      receber a mensagem de bloqueio temporário na 6ª tentativa.
      *(Requisito 1.11)*

## Sugestão de vídeo (opcional, mas recomendado)

Além dos prints, é interessante gravar um vídeo curto (2–3 minutos)
demonstrando o fluxo completo: cadastro → login → recebimento do
e-mail → digitação do código → acesso ao dashboard → logout. Isso
facilita a correção e comprova que o sistema funciona de ponta a
ponta, como pedido nas diretrizes de entrega.