# Justificativas Técnicas

Este documento explica **por que** cada decisão técnica foi tomada no
módulo de Autenticação e Gestão de Credenciais.

## Por que bcrypt (e não MD5, SHA-256 puro, etc.)?

Algoritmos como MD5 e SHA-256 foram feitos para serem **rápidos** —
ótimo para verificar integridade de arquivos, péssimo para senhas,
porque isso permite que um atacante teste bilhões de combinações por
segundo (ataque de força bruta offline).

O bcrypt foi projetado especificamente para ser **lento de propósito**
e já inclui o salt embutido no próprio hash gerado, evitando erros
comuns de implementação manual de salt.

## Por que 12 rounds no bcrypt?

O parâmetro `rounds` controla quantas vezes o algoritmo processa a
senha internamente — cada round a mais **dobra** o tempo de
processamento.

- Poucos rounds (ex: 4): rápido, mas fraco contra força bruta.
- Muitos rounds (ex: 20+): muito seguro, mas deixa o login
  perceptivelmente lento para o usuário.

**12 rounds** é o valor recomendado atualmente pela comunidade de
segurança como equilíbrio entre proteção e desempenho, sendo o padrão
adotado por frameworks como Django e Rails.

## Por que salt único por usuário?

Sem salt, dois usuários com a mesma senha gerariam o **mesmo hash** no
banco — um atacante que descobrisse a senha de um, descobriria a do
outro também. Além disso, sem salt, um atacante pode pré-calcular
hashes de senhas comuns (rainbow tables) e comparar direto com o banco
vazado.

Com um salt aleatório e único por usuário, cada senha gera um hash
completamente diferente, mesmo que duas pessoas usem a senha
`123456`.

## Por que 2FA por e-mail (e não SMS ou aplicativo autenticador)?

- **SMS** exigiria contratar um serviço pago de envio de mensagens
  (ex: Twilio), inviável para um projeto acadêmico sem custo.
- **Aplicativo autenticador** (Google Authenticator, por exemplo)
  adiciona complexidade extra (geração de QR Code, biblioteca TOTP)
  que foge do escopo deste checklist.
- **E-mail** é gratuito, simples de implementar com bibliotecas
  nativas do Python (`smtplib`), e o suficiente para demonstrar o
  conceito de segunda camada de autenticação exigido pelo requisito
  1.5.

## Por que o código de 2FA expira em 5 minutos?

Um código sem prazo de validade poderia ser reutilizado indefinidamente
caso fosse interceptado. 5 minutos é tempo suficiente para o usuário
checar o e-mail e digitar o código, mas curto o bastante para reduzir
a janela de oportunidade de um ataque.

## Por que a sessão expira em 15 minutos de inatividade?

Sessões sem expiração automática ficam vulneráveis caso o usuário
esqueça de fazer logout (por exemplo, em um computador compartilhado).
15 minutos é um valor comum para sistemas administrativos — tempo
suficiente para não atrapalhar o uso normal, mas que limita o risco de
uma sessão esquecida aberta.

## Por que bloquear após 5 tentativas erradas por 3 minutos?

O objetivo do rate limit é tornar um ataque de força bruta
**impraticável em tempo hábil**, sem irritar demais um usuário real
que simplesmente errou a senha uma ou duas vezes.

- Poucas tentativas permitidas (ex: 2) prejudicariam usuários reais
  que só digitaram errado.
- Bloqueio muito curto (ex: 10 segundos) não impede de fato um ataque
  automatizado.

5 tentativas com bloqueio de 3 minutos é um equilíbrio comum adotado
por sistemas de login, tornando um ataque de força bruta muito lento
para ser viável.

## Por que as credenciais ficam em um arquivo `.env`?

Se a senha do banco de dados ou do e-mail estivesse escrita direto no
código-fonte, qualquer pessoa com acesso ao repositório do GitHub
(incluindo repositórios públicos) teria acesso a essas credenciais.
Separar essas informações em um arquivo `.env` — que fica fora do
controle de versão graças ao `.gitignore` — é uma prática padrão de
segurança em desenvolvimento de software.