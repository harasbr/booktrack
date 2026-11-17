"""BookTrack: Flask + POO + MySQL + interface HTML/CSS/JavaScript.

Execute este arquivo para abrir o sistema em http://127.0.0.1:5000/.
"""

from datetime import date

import mysql.connector
from flask import Flask, jsonify, render_template, request

from avaliacao import Avaliacao
from dao import AvaliacaoDAO, LeituraDAO, LivroDAO
from leitura import Leitura
from livro import Livro

app = Flask(__name__)

livros = LivroDAO()
leituras = LeituraDAO()
avaliacoes = AvaliacaoDAO()


def texto_valido(valor, tamanho_maximo):
    return isinstance(valor, str) and 0 < len(valor.strip()) <= tamanho_maximo


def id_valido(valor):
    return type(valor) is int and valor > 0


def corpo_json():
    dados = request.get_json(silent=True)
    return dados if isinstance(dados, dict) else None


def validar_data(data_conclusao):
    if data_conclusao is None:
        return None
    if not isinstance(data_conclusao, str):
        raise ValueError("Data invalida")
    return date.fromisoformat(data_conclusao).isoformat()


@app.errorhandler(mysql.connector.Error)
def erro_de_banco(erro):
    app.logger.error("Problema no banco de dados: %s", erro)
    if isinstance(erro, mysql.connector.IntegrityError):
        return jsonify({"erro": "Registro duplicado ou referencia inexistente no banco."}), 409
    return jsonify({"erro": "Nao foi possivel acessar o banco de dados. Confira o MySQL do XAMPP."}), 500


@app.get("/")
def pagina_inicial():
    return render_template("index.html")


@app.get("/api")
def informacoes_api():
    return jsonify({
        "projeto": "BookTrack",
        "mensagem": "API e interface da etapa 3 disponiveis",
        "rotas": ["/livros", "/leituras", "/avaliacoes"],
    })


@app.get("/livros")
def listar_livros():
    return jsonify(livros.listar())


@app.get("/livros/<int:id_livro>")
def buscar_livro(id_livro):
    livro = livros.buscar(id_livro)
    if livro is None:
        return jsonify({"erro": "Livro nao encontrado."}), 404
    return jsonify(livro)


@app.post("/livros")
def cadastrar_livro():
    dados = corpo_json()
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido."}), 400

    titulo = dados.get("titulo")
    autor = dados.get("autor")
    genero = dados.get("genero")
    if not texto_valido(titulo, 100) or not texto_valido(autor, 100):
        return jsonify({"erro": "Titulo e autor devem ter de 1 a 100 caracteres."}), 400
    if genero is not None and not texto_valido(genero, 50):
        return jsonify({"erro": "Genero deve ter de 1 a 50 caracteres ou ser omitido."}), 400

    livro = Livro(titulo.strip(), autor.strip(), genero.strip() if genero else None)
    livro.id_livro = livros.cadastrar(livro)
    return jsonify(livro.to_dict()), 201


@app.get("/leituras")
def listar_leituras():
    return jsonify(leituras.listar())


@app.get("/leituras/<int:id_leitura>")
def buscar_leitura(id_leitura):
    leitura = leituras.buscar(id_leitura)
    if leitura is None:
        return jsonify({"erro": "Leitura nao encontrada."}), 404
    return jsonify(leitura)


@app.post("/leituras")
def cadastrar_leitura():
    dados = corpo_json()
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido."}), 400

    id_livro = dados.get("id_livro")
    status = dados.get("status_leitura")
    if not id_valido(id_livro):
        return jsonify({"erro": "Selecione um livro valido."}), 400
    if status not in ("Quero ler", "Lendo", "Concluído"):
        return jsonify({"erro": "Status permitido: Quero ler, Lendo ou Concluído."}), 400
    try:
        data_conclusao = validar_data(dados.get("data_conclusao"))
    except ValueError:
        return jsonify({"erro": "Use uma data no formato AAAA-MM-DD."}), 400
    if status == "Concluído" and data_conclusao is None:
        return jsonify({"erro": "Informe a data de conclusao."}), 400
    if status != "Concluído" and data_conclusao is not None:
        return jsonify({"erro": "A data so e permitida para leitura concluida."}), 400
    if livros.buscar(id_livro) is None:
        return jsonify({"erro": "Livro nao encontrado."}), 404

    leitura = Leitura(id_livro, status, data_conclusao)
    leitura.id_leitura = leituras.cadastrar(leitura)
    return jsonify(leitura.to_dict()), 201


@app.patch("/leituras/<int:id_leitura>")
def mudar_status_leitura(id_leitura):
    """Permite mudar Quero ler -> Lendo -> Concluído pela interface."""
    dados = corpo_json()
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido."}), 400
    atual = leituras.buscar(id_leitura)
    if atual is None:
        return jsonify({"erro": "Leitura nao encontrada."}), 404

    status = dados.get("status_leitura")
    if status not in ("Quero ler", "Lendo", "Concluído"):
        return jsonify({"erro": "Status de leitura invalido."}), 400
    data_conclusao = None
    if status == "Concluído":
        try:
            data_conclusao = validar_data(dados.get("data_conclusao")) or date.today().isoformat()
        except ValueError:
            return jsonify({"erro": "Data de conclusao invalida."}), 400
    leituras.atualizar_status(id_leitura, status, data_conclusao)
    return jsonify(leituras.buscar(id_leitura))


@app.get("/avaliacoes")
def listar_avaliacoes():
    return jsonify(avaliacoes.listar())


@app.get("/avaliacoes/<int:id_avaliacao>")
def buscar_avaliacao(id_avaliacao):
    avaliacao = avaliacoes.buscar(id_avaliacao)
    if avaliacao is None:
        return jsonify({"erro": "Avaliacao nao encontrada."}), 404
    return jsonify(avaliacao)


@app.post("/avaliacoes")
def cadastrar_avaliacao():
    dados = corpo_json()
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido."}), 400

    id_leitura = dados.get("id_leitura")
    nota = dados.get("nota")
    comentario = dados.get("comentario")
    if not id_valido(id_leitura):
        return jsonify({"erro": "Selecione uma leitura valida."}), 400
    if type(nota) is not int or not 1 <= nota <= 5:
        return jsonify({"erro": "A nota deve ser um numero inteiro entre 1 e 5."}), 400
    if comentario is not None and (not isinstance(comentario, str) or len(comentario) > 255):
        return jsonify({"erro": "O comentario deve ter ate 255 caracteres."}), 400
    leitura = leituras.buscar(id_leitura)
    if leitura is None:
        return jsonify({"erro": "Leitura nao encontrada."}), 404
    if leitura["status_leitura"] != "Concluído":
        return jsonify({"erro": "Conclua a leitura antes de avaliar."}), 400

    avaliacao = Avaliacao(id_leitura, nota, comentario.strip() if comentario else None)
    avaliacao.id_avaliacao = avaliacoes.cadastrar(avaliacao)
    return jsonify(avaliacao.to_dict()), 201


if __name__ == "__main__":
    # Servidor local para o trabalho escolar. Nao publique com debug=True.
    app.run(debug=True, host="127.0.0.1", port=5000)
