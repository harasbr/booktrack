"""Teste de leitura: interface HTML/CSS/JS e rotas conectadas ao MySQL.

Inicie o app.py e ligue o MySQL no XAMPP antes de executar.
Este teste nao adiciona registros ao banco.
"""

import json
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

BASE = "http://127.0.0.1:5000"


def ler(caminho):
    with urlopen(BASE + caminho, timeout=10) as resposta:
        return resposta.status, resposta.headers.get("Content-Type", ""), resposta.read().decode("utf-8")


def testar():
    print("1. Verificando a interface HTML...")
    status, tipo, html = ler("/")
    assert status == 200 and "text/html" in tipo and "BookTrack" in html
    assert "static/style.css" in html and "static/app.js" in html
    print("   OK: HTML carregado")

    print("2. Verificando CSS e JavaScript...")
    status_css, _, css = ler("/static/style.css")
    status_js, _, javascript = ler("/static/app.js")
    assert status_css == 200 and status_js == 200
    assert "--forest" in css and "fetch(" in javascript
    print("   OK: arquivos CSS e JavaScript disponiveis")

    print("3. Verificando API e banco de dados...")
    for rota in ("/livros", "/leituras", "/avaliacoes"):
        status_api, _, corpo = ler(rota)
        itens = json.loads(corpo)
        assert status_api == 200 and isinstance(itens, list)
        print(f"   OK: {rota} retornou {len(itens)} registros")

    print("\nSUCESSO: site e rotas da etapa 3 estao acessiveis!")
    print("Abra http://127.0.0.1:5000/ e teste um cadastro pela tela.")


if __name__ == "__main__":
    try:
        testar()
    except (AssertionError, HTTPError, URLError, ValueError) as erro:
        print("FALHA NO TESTE:", erro)
        if isinstance(erro, HTTPError):
            print(erro.read().decode("utf-8"))
        print("Confira se o XAMPP/MySQL e o app.py estao ligados.")
