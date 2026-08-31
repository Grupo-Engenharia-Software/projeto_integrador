# Escopo do Projeto

## Visão geral

Este projeto é o desenvolvimento incremental de um sistema web, feito
em etapas ao longo do Projeto Integrador. Cada etapa entrega e
comprova um conjunto específico de requisitos, definidos em checklist
próprio.

## Etapa atual: 1. Autenticação e Gestão de Credenciais

O escopo desta etapa cobre **exclusivamente** o módulo de login do
sistema — cadastro de usuário, autenticação segura e proteção contra
ataques comuns de força bruta. Nenhuma outra funcionalidade do sistema
(além de uma tela de exemplo pós-login) faz parte desta entrega.

### Está dentro do escopo desta etapa

- Cadastro de usuário (e-mail e senha)
- Armazenamento seguro de senha (hash + salt, com bcrypt)
- Login com verificação em duas etapas (2FA) por e-mail
- Gerenciamento de sessão (criação, expiração automática e logout)
- Proteção contra tentativas de força bruta (rate limit)
- Documentação técnica e evidências de funcionamento do módulo de
  autenticação

### Fora do escopo desta etapa

- Qualquer funcionalidade da aplicação além do login (essas serão
  tratadas em etapas futuras do Projeto Integrador, conforme novos
  checklists forem liberados)
- Recuperação de senha ("esqueci minha senha")
- Edição de perfil do usuário
- Painel administrativo
- Deploy em ambiente de produção (o projeto roda em ambiente de
  desenvolvimento local, usando o servidor embutido do Flask)

## Arquitetura definida para o projeto

| Item | Definição |
|---|---|
| Arquitetura | MVC (Model-View-Controller) |
| Linguagem | Python |
| Framework web | Flask |
| Front-end | HTML, CSS e JavaScript (renderizados pelo back-end via Jinja2) |
| Banco de dados | PostgreSQL |
| Envio de e-mail (2FA) | SMTP (Gmail), via biblioteca `smtplib` |
