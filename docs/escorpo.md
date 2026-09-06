# Escopo do Projeto

## Tema

**CampusFlow — Sistema de Gestão de Projetos Acadêmicos**

Um sistema para organizar e acompanhar projetos acadêmicos, trabalhos
em grupo e atividades de alunos, desde a criação até a entrega.

## Visão geral

Este projeto é o desenvolvimento incremental do CampusFlow, feito em
etapas ao longo do Projeto Integrador. Cada etapa entrega e comprova
um conjunto específico de requisitos de segurança e conformidade,
definidos em checklist próprio, antes de as funcionalidades de gestão
de projetos acadêmicos propriamente ditas serem construídas sobre essa
base.

## Etapa 1: Autenticação e Gestão de Credenciais ✅ Concluída

O escopo desta etapa cobriu **exclusivamente** o módulo de login do
sistema — cadastro de usuário, autenticação segura e proteção contra
ataques comuns de força bruta.

### Esteve dentro do escopo desta etapa

- Cadastro de usuário (e-mail e senha)
- Armazenamento seguro de senha (hash + salt, com bcrypt)
- Login com verificação em duas etapas (2FA) por e-mail
- Gerenciamento de sessão (criação, expiração automática e logout)
- Proteção contra tentativas de força bruta (rate limit)
- Documentação técnica e evidências de funcionamento do módulo de
  autenticação

Detalhamento completo em [`fluxo-autenticacao.md`](./fluxo-autenticacao.md).

## Etapa 2: Recuperação de Senha ✅ Concluída

O escopo desta etapa cobriu o fluxo de "esqueci minha senha": geração
de token seguro, envio por e-mail, expiração e invalidação do token, e
registro em log das solicitações e resultados.

### Esteve dentro do escopo desta etapa

- Solicitação de recuperação de senha por e-mail
- Geração de token seguro com tempo de expiração
- Invalidação do token após o uso
- Tratamento de token expirado ou já utilizado
- Registro em log de cada solicitação e do sucesso/falha do processo

Detalhamento completo em
[`fluxo-recuperacao-senha.md`](./fluxo-recuperacao-senha.md).

## Fora do escopo até o momento

- Qualquer funcionalidade da aplicação além de autenticação e
  recuperação de senha (essas serão tratadas em etapas futuras do
  Projeto Integrador, conforme novos checklists forem liberados —
  ver [`checklist-requisitos.md`](./checklist-requisitos.md))
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
| Envio de e-mail (2FA e recuperação de senha) | SMTP (Gmail), via biblioteca `smtplib` |

## Critérios de aceite

Cada etapa é considerada concluída quando:

1. Todos os itens do checklist daquela seção estão implementados e
   testados via front-end.
2. A documentação técnica (fluxo, justificativas e evidências) está
   publicada na pasta `docs/` do repositório.
3. O código-fonte está comentado, especialmente nas camadas de
   segurança e credenciais.
4. Existem commits organizados ao longo do desenvolvimento (não um
   único commit final).
5. Uma Release foi criada no repositório do GitHub, marcando a entrega
   daquela etapa.
