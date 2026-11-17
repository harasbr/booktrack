"use strict";

// A interface so exibe dados reais recebidos do Flask por fetch().
// O Flask consulta o MySQL, por meio dos DAOs da etapa 2.

const dados = { livros: [], leituras: [], avaliacoes: [] };
const meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
let toastTimer;

const $ = (seletor) => document.querySelector(seletor);

function textoSeguro(valor) {
  return String(valor ?? "").replace(/[&<>"']/g, caractere => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[caractere]));
}

function dataDeHoje() {
  const hoje = new Date();
  return `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, "0")}-${String(hoje.getDate()).padStart(2, "0")}`;
}

function mostrarAviso(mensagem, erro = false) {
  const aviso = $("#toast");
  aviso.textContent = mensagem;
  aviso.classList.toggle("error", erro);
  aviso.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { aviso.hidden = true; }, 4800);
}

function mostrarErroPersistente(mensagem = "") {
  const caixa = $("#mensagem-erro");
  caixa.hidden = !mensagem;
  caixa.textContent = mensagem;
}

function atualizarIndicador(conectado) {
  const indicador = $("#status-conexao");
  indicador.classList.toggle("online", conectado);
  indicador.classList.toggle("offline", !conectado);
  indicador.lastChild.textContent = conectado ? " Banco de dados conectado" : " Falha na conexão";
}

async function requisicao(caminho, opcoes = {}) {
  let resposta;
  try {
    resposta = await fetch(caminho, {
      ...opcoes,
      headers: { "Content-Type": "application/json", ...(opcoes.headers || {}) },
    });
  } catch (erro) {
    throw new Error("Não foi possível acessar o Flask. Verifique se o app.py está executando.");
  }
  const tipo = resposta.headers.get("content-type") || "";
  let conteudo = null;
  if (tipo.includes("application/json")) {
    try { conteudo = await resposta.json(); } catch (_) { /* resposta invalida */ }
  }
  if (!resposta.ok) {
    throw new Error(conteudo?.erro || `Erro ${resposta.status} ao acessar o servidor.`);
  }
  return conteudo;
}

function ultimaLeitura(idLivro) {
  return dados.leituras
    .filter(leitura => Number(leitura.id_livro) === Number(idLivro))
    .sort((a, b) => Number(b.id_leitura) - Number(a.id_leitura))[0] || null;
}

function avaliacaoDaLeitura(idLeitura) {
  return dados.avaliacoes.find(avaliacao => Number(avaliacao.id_leitura) === Number(idLeitura)) || null;
}

function atualizarEstatisticas() {
  const anoAtual = new Date().getFullYear();
  const anos = new Set([anoAtual]);
  dados.leituras.forEach(leitura => {
    if (leitura.status_leitura === "Concluído" && leitura.data_conclusao) {
      anos.add(Number(leitura.data_conclusao.slice(0, 4)));
    }
  });

  const seletor = $("#ano-estatisticas");
  const anterior = Number(seletor.value || anoAtual);
  const listaAnos = Array.from(anos).sort((a, b) => b - a);
  seletor.innerHTML = listaAnos.map(ano => `<option value="${ano}">${ano}</option>`).join("");
  seletor.value = listaAnos.includes(anterior) ? String(anterior) : String(anoAtual);

  const ano = Number(seletor.value);
  const concluidas = dados.leituras.filter(leitura => leitura.status_leitura === "Concluído" && leitura.data_conclusao);
  const concluidoNoAno = concluidas.filter(leitura => Number(leitura.data_conclusao.slice(0, 4)) === ano);
  const lendoAgora = dados.livros.filter(livro => ultimaLeitura(livro.id_livro)?.status_leitura === "Lendo").length;

  $("#stat-livros").textContent = dados.livros.length;
  $("#stat-lendo").textContent = lendoAgora;
  $("#stat-concluidos").textContent = concluidoNoAno.length;
  $("#stat-avaliacoes").textContent = dados.avaliacoes.length;

  const contagens = meses.map((_, mes) => concluidoNoAno.filter(leitura => Number(leitura.data_conclusao.slice(5, 7)) === mes + 1).length);
  const maior = Math.max(...contagens, 1);
  $("#grafico-mensal").innerHTML = contagens.map((total, i) => `
    <div class="month-column" title="${meses[i]}: ${total} leitura(s)">
      <div class="month-bar ${total ? "filled" : ""}" data-value="${total ? total : ""}" style="height:${Math.max(total / maior * 95, 2)}%"></div>
      <span class="month-label">${meses[i]}</span>
    </div>`).join("");
  $("#grafico-mensal").setAttribute("aria-label", `Livros concluídos em ${ano}: ${contagens.map((n, i) => `${meses[i]} ${n}`).join(", ")}`);
}

function statusClasse(status) {
  if (status === "Lendo") return "status-lendo";
  if (status === "Concluído") return "status-concluido";
  if (status === "Quero ler") return "status-quero-ler";
  return "";
}

function desenharLivros() {
  const busca = $("#busca-livros").value.trim().toLocaleLowerCase("pt-BR");
  const filtro = $("#filtro-status").value;
  const filtrados = dados.livros.filter(livro => {
    const conteudo = [livro.titulo, livro.autor, livro.genero].join(" ").toLocaleLowerCase("pt-BR");
    const status = ultimaLeitura(livro.id_livro)?.status_leitura || "Sem leitura";
    return conteudo.includes(busca) && (filtro === "todos" || status === filtro);
  });
  $("#total-listagem").textContent = `${filtrados.length} ${filtrados.length === 1 ? "livro encontrado" : "livros encontrados"}`;
  const grade = $("#lista-livros");
  if (!filtrados.length) {
    grade.innerHTML = `<div class="empty-state"><span class="empty-icon">▤</span><h3>${dados.livros.length ? "Nenhum livro encontrado" : "Sua estante está começando"}</h3><p>${dados.livros.length ? "Tente outro termo ou filtro." : "Cadastre seu primeiro livro para começar a acompanhar as leituras."}</p><a class="button button-primary" href="#cadastrar">Adicionar livro ↗</a></div>`;
    return;
  }
  grade.innerHTML = filtrados.map(livro => {
    const leitura = ultimaLeitura(livro.id_livro);
    const avaliacao = leitura ? avaliacaoDaLeitura(leitura.id_leitura) : null;
    const status = leitura?.status_leitura || "Sem leitura";
    const botoes = [];
    if (!leitura || status === "Concluído") {
      botoes.push(`<button class="text-action" data-acao="nova-leitura" data-id="${Number(livro.id_livro)}">Nova leitura</button>`);
    }
    if (leitura && status === "Quero ler") {
      botoes.push(`<button class="text-action" data-acao="comecar" data-id="${Number(leitura.id_leitura)}">Começar leitura</button>`);
    }
    if (leitura && status === "Lendo") {
      botoes.push(`<button class="text-action" data-acao="concluir" data-id="${Number(leitura.id_leitura)}">Marcar como concluído</button>`);
    }
    if (leitura && status === "Concluído" && !avaliacao) {
      botoes.push(`<button class="text-action" data-acao="avaliar" data-id="${Number(leitura.id_leitura)}">Avaliar livro</button>`);
    }
    return `<article class="book-card">
      <div class="book-cover" aria-hidden="true"></div>
      <div class="book-details">
        <h3>${textoSeguro(livro.titulo)}</h3>
        <p class="book-author">${textoSeguro(livro.autor)}</p>
        <div class="book-badges"><span class="chip ${statusClasse(status)}">${textoSeguro(status)}</span>${livro.genero ? `<span class="chip">${textoSeguro(livro.genero)}</span>` : ""}</div>
        <div class="rating-line">${avaliacao ? `${"★".repeat(avaliacao.nota)}${"☆".repeat(5 - avaliacao.nota)} <span class="rating-number">${avaliacao.nota}/5</span>` : `<span class="rating-number">Ainda sem avaliação</span>`}</div>
        ${avaliacao?.comentario ? `<p class="book-comment">“${textoSeguro(avaliacao.comentario)}”</p>` : ""}
        <div class="book-actions">${botoes.join("")}</div>
      </div>
    </article>`;
  }).join("");
}

function atualizarSelects() {
  const selectLivro = $("#livro-da-leitura");
  const selecaoLivro = selectLivro.value;
  selectLivro.innerHTML = `<option value="">Selecione um livro...</option>` + dados.livros.map(livro => `<option value="${Number(livro.id_livro)}">${textoSeguro(livro.titulo)} (${textoSeguro(livro.autor)})</option>`).join("");
  if (dados.livros.some(l => String(l.id_livro) === selecaoLivro)) selectLivro.value = selecaoLivro;

  const selectAvaliacao = $("#leitura-da-avaliacao");
  const selecaoAvaliacao = selectAvaliacao.value;
  const prontas = dados.leituras.filter(leitura => leitura.status_leitura === "Concluído" && !avaliacaoDaLeitura(leitura.id_leitura));
  selectAvaliacao.innerHTML = `<option value="">${prontas.length ? "Selecione uma leitura..." : "Não há leituras disponíveis para avaliar"}</option>` + prontas.map(leitura => {
    const livro = dados.livros.find(l => Number(l.id_livro) === Number(leitura.id_livro));
    return `<option value="${Number(leitura.id_leitura)}">${textoSeguro(livro?.titulo || "Livro não encontrado")} • ${textoSeguro(leitura.data_conclusao || "")}</option>`;
  }).join("");
  if (prontas.some(l => String(l.id_leitura) === selecaoAvaliacao)) selectAvaliacao.value = selecaoAvaliacao;
}

async function carregarDados() {
  const botao = $("#botao-atualizar");
  botao.disabled = true;
  try {
    const [livros, leituras, avaliacoes] = await Promise.all([
      requisicao("/livros"), requisicao("/leituras"), requisicao("/avaliacoes"),
    ]);
    if (![livros, leituras, avaliacoes].every(Array.isArray)) throw new Error("O servidor não retornou os dados no formato esperado.");
    Object.assign(dados, { livros, leituras, avaliacoes });
    mostrarErroPersistente();
    atualizarIndicador(true);
    atualizarEstatisticas();
    desenharLivros();
    atualizarSelects();
  } catch (erro) {
    atualizarIndicador(false);
    mostrarErroPersistente(erro.message);
    mostrarAviso(erro.message, true);
    $("#lista-livros").innerHTML = `<div class="empty-state"><span class="empty-icon">!</span><h3>Não foi possível carregar a biblioteca</h3><p>Confira o XAMPP e tente atualizar a página.</p></div>`;
  } finally {
    botao.disabled = false;
  }
}

function abrirAba(nome) {
  document.querySelectorAll("[data-tab]").forEach(botao => {
    const ativa = botao.dataset.tab === nome;
    botao.classList.toggle("active", ativa);
    botao.setAttribute("aria-selected", ativa ? "true" : "false");
  });
  ["livro", "leitura", "avaliacao"].forEach(aba => {
    $(`#painel-${aba}`).hidden = aba !== nome;
  });
}

function atualizarCampoData() {
  const concluido = $("#status-leitura").value === "Concluído";
  $("#campo-data").hidden = !concluido;
  $("#data-conclusao").required = concluido;
  if (concluido && !$("#data-conclusao").value) $("#data-conclusao").value = dataDeHoje();
  if (!concluido) $("#data-conclusao").value = "";
}

function atualizarEstrelas() {
  const selecionada = Number($("#estrelas-input input:checked")?.value || 0);
  document.querySelectorAll("#estrelas-input label").forEach(label => {
    label.classList.toggle("selected", Number(label.querySelector("input").value) <= selecionada);
  });
  $("#descricao-nota").textContent = selecionada ? `${selecionada} de 5 estrelas` : "Selecione a quantidade de estrelas.";
}

async function executarFormulario(formulario, caminho, dadosEnvio, mensagem) {
  const botao = formulario.querySelector('button[type="submit"]');
  botao.disabled = true;
  try {
    const criado = await requisicao(caminho, { method: "POST", body: JSON.stringify(dadosEnvio) });
    formulario.reset();
    atualizarCampoData();
    atualizarEstrelas();
    await carregarDados();
    mostrarAviso(mensagem);
    return criado;
  } catch (erro) {
    mostrarAviso(erro.message, true);
    return null;
  } finally {
    botao.disabled = false;
  }
}

async function acaoNoLivro(evento) {
  const botao = evento.target.closest("button[data-acao]");
  if (!botao) return;
  const id = Number(botao.dataset.id);
  const acao = botao.dataset.acao;
  if (acao === "nova-leitura") {
    abrirAba("leitura");
    $("#livro-da-leitura").value = String(id);
    $("#cadastrar").scrollIntoView({ behavior: "smooth" });
    return;
  }
  if (acao === "avaliar") {
    abrirAba("avaliacao");
    $("#leitura-da-avaliacao").value = String(id);
    $("#cadastrar").scrollIntoView({ behavior: "smooth" });
    return;
  }
  if (acao === "comecar" || acao === "concluir") {
    botao.disabled = true;
    try {
      const novaSituacao = acao === "comecar" ? "Lendo" : "Concluído";
      await requisicao(`/leituras/${id}`, {
        method: "PATCH",
        body: JSON.stringify({ status_leitura: novaSituacao, ...(novaSituacao === "Concluído" ? { data_conclusao: dataDeHoje() } : {}) }),
      });
      await carregarDados();
      mostrarAviso(novaSituacao === "Lendo" ? "Boa leitura! Status atualizado." : "Leitura concluída e registrada!");
    } catch (erro) {
      botao.disabled = false;
      mostrarAviso(erro.message, true);
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  $("#ano-rodape").textContent = new Date().getFullYear();
  $("#data-conclusao").value = dataDeHoje();
  $("#botao-atualizar").addEventListener("click", carregarDados);
  $("#busca-livros").addEventListener("input", desenharLivros);
  $("#filtro-status").addEventListener("change", desenharLivros);
  $("#ano-estatisticas").addEventListener("change", atualizarEstatisticas);
  $("#status-leitura").addEventListener("change", atualizarCampoData);
  $("#estrelas-input").addEventListener("change", atualizarEstrelas);
  $("#lista-livros").addEventListener("click", acaoNoLivro);
  document.querySelectorAll("[data-tab]").forEach(botao => {
    botao.addEventListener("click", () => abrirAba(botao.dataset.tab));
  });

  $("#form-livro").addEventListener("submit", async evento => {
    evento.preventDefault();
    const form = evento.currentTarget;
    const d = new FormData(form);
    const livro = await executarFormulario(form, "/livros", {
      titulo: String(d.get("titulo")).trim(), autor: String(d.get("autor")).trim(), genero: String(d.get("genero")).trim() || null,
    }, "Livro adicionado à sua estante!");
    if (livro) {
      abrirAba("leitura");
      $("#livro-da-leitura").value = String(livro.id_livro);
    }
  });

  $("#form-leitura").addEventListener("submit", async evento => {
    evento.preventDefault();
    const form = evento.currentTarget;
    const d = new FormData(form);
    const concluida = d.get("status_leitura") === "Concluído";
    const leitura = await executarFormulario(form, "/leituras", {
      id_livro: Number(d.get("id_livro")), status_leitura: d.get("status_leitura"),
      data_conclusao: concluida ? d.get("data_conclusao") : null,
    }, "Leitura registrada com sucesso!");
    if (leitura && concluida) {
      abrirAba("avaliacao");
      $("#leitura-da-avaliacao").value = String(leitura.id_leitura);
    }
  });

  $("#form-avaliacao").addEventListener("submit", async evento => {
    evento.preventDefault();
    const form = evento.currentTarget;
    const d = new FormData(form);
    const avaliacao = await executarFormulario(form, "/avaliacoes", {
      id_leitura: Number(d.get("id_leitura")), nota: Number(d.get("nota")), comentario: String(d.get("comentario")).trim() || null,
    }, "Avaliação salva na biblioteca!");
    if (avaliacao) $("#biblioteca").scrollIntoView({ behavior: "smooth" });
  });

  atualizarCampoData();
  atualizarEstrelas();
  carregarDados();
});
