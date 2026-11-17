"""Teste simples da API. Inicie app.py antes de executar este arquivo."""

import json
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "http://127.0.0.1:5000"


def requisicao(caminho, dados=None):
    corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8") if dados is not None else None
    pedido = Request(
        BASE + caminho,
        data=corpo,
        headers={"Content-Type": "application/json"},
        method="POST" if corpo is not None else "GET",
    )
    with urlopen(pedido, timeout=10) as resposta:
        return resposta.status, json.loads(resposta.read().decode("utf-8"))


def conferir():
    print("1. Testando API...")
    status, inicio = requisicao("/api")
    assert status == 200 and inicio["projeto"] == "BookTrack"
    print("   API acessivel")

    print("2. Cadastrando um livro de teste...")
    status, livro = requisicao("/livros", {
        "titulo": "Livro de teste da Etapa 2",
        "autor": "Equipe BookTrack",
        "genero": "Teste",
    })
    assert status == 201 and livro["id_livro"] > 0
    print("   Livro cadastrado com ID", livro["id_livro"])

    print("3. Cadastrando uma leitura...")
    status, leitura = requisicao("/leituras", {
        "id_livro": livro["id_livro"],
        "status_leitura": "Concluído",
        "data_conclusao": date.today().isoformat(),
    })
    assert status == 201 and leitura["id_leitura"] > 0
    print("   Leitura cadastrada com ID", leitura["id_leitura"])

    print("4. Cadastrando uma avaliacao...")
    status, avaliacao = requisicao("/avaliacoes", {
        "id_leitura": leitura["id_leitura"],
        "nota": 5,
        "comentario": "Teste de cadastro via Flask",
    })
    assert status == 201 and avaliacao["id_avaliacao"] > 0
    print("   Avaliacao cadastrada com ID", avaliacao["id_avaliacao"])

    print("5. Consultando as tres tabelas...")
    for caminho in ("/livros", "/leituras", "/avaliacoes"):
        status, registros = requisicao(caminho)
        assert status == 200 and isinstance(registros, list)
        print("   Consulta", caminho, "funcionou. Registros:", len(registros))

    print("\nSUCESSO: cadastros e consultas da etapa 2 funcionaram!")


if __name__ == "__main__":
    try:
        conferir()
    except (URLError, HTTPError, AssertionError, ValueError) as erro:
        print("FALHA NO TESTE:", erro)
        if isinstance(erro, HTTPError):
            print(erro.read().decode("utf-8"))
        print("Confira se o MySQL do XAMPP e o app.py estao ligados.")
