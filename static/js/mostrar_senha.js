// Este arquivo cuida apenas de um detalhe visual:
// mostrar ou esconder a senha digitada.

document.addEventListener("DOMContentLoaded", () => {
  const senha = document.getElementById("password");
  const botaoMostrarSenha = document.getElementById("togglePassword");

  botaoMostrarSenha.addEventListener("click", () => {
    const senhaEscondida = senha.type === "password";
    senha.type = senhaEscondida ? "text" : "password";
    botaoMostrarSenha.textContent = senhaEscondida ? "🙈" : "👁";
  });
});