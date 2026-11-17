"""DAO: classes que realizam consultas e cadastros no MySQL."""

from conexao import conectar
from livro import Livro
from leitura import Leitura
from avaliacao import Avaliacao


def _consultar(sql, parametros=()):
    banco = conectar()
    cursor = None
    try:
        cursor = banco.cursor(dictionary=True)
        cursor.execute(sql, parametros)
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        banco.close()


def _cadastrar(sql, parametros):
    banco = conectar()
    cursor = None
    try:
        cursor = banco.cursor()
        cursor.execute(sql, parametros)
        banco.commit()
        return cursor.lastrowid
    except Exception:
        banco.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        banco.close()


def _executar(sql, parametros):
    banco = conectar()
    cursor = None
    try:
        cursor = banco.cursor()
        cursor.execute(sql, parametros)
        banco.commit()
    except Exception:
        banco.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        banco.close()


class LivroDAO:
    def cadastrar(self, livro: Livro):
        sql = "INSERT INTO livro (titulo, autor, genero) VALUES (%s, %s, %s)"
        return _cadastrar(sql, (livro.titulo, livro.autor, livro.genero))

    def listar(self):
        registros = _consultar("SELECT id_livro, titulo, autor, genero FROM livro ORDER BY id_livro")
        return [Livro(r["titulo"], r["autor"], r["genero"], r["id_livro"]).to_dict() for r in registros]

    def buscar(self, id_livro):
        registros = _consultar(
            "SELECT id_livro, titulo, autor, genero FROM livro WHERE id_livro = %s",
            (id_livro,),
        )
        if not registros:
            return None
        r = registros[0]
        return Livro(r["titulo"], r["autor"], r["genero"], r["id_livro"]).to_dict()


class LeituraDAO:
    def cadastrar(self, leitura: Leitura):
        sql = """INSERT INTO leitura (id_livro, status_leitura, data_conclusao)
                 VALUES (%s, %s, %s)"""
        return _cadastrar(sql, (leitura.id_livro, leitura.status_leitura, leitura.data_conclusao))

    def listar(self):
        registros = _consultar(
            "SELECT id_leitura, id_livro, status_leitura, data_conclusao "
            "FROM leitura ORDER BY id_leitura"
        )
        return [Leitura(r["id_livro"], r["status_leitura"], r["data_conclusao"], r["id_leitura"]).to_dict() for r in registros]

    def buscar(self, id_leitura):
        registros = _consultar(
            "SELECT id_leitura, id_livro, status_leitura, data_conclusao "
            "FROM leitura WHERE id_leitura = %s",
            (id_leitura,),
        )
        if not registros:
            return None
        r = registros[0]
        return Leitura(r["id_livro"], r["status_leitura"], r["data_conclusao"], r["id_leitura"]).to_dict()


    def atualizar_status(self, id_leitura, status_leitura, data_conclusao):
        sql = """UPDATE leitura
                 SET status_leitura = %s, data_conclusao = %s
                 WHERE id_leitura = %s"""
        _executar(sql, (status_leitura, data_conclusao, id_leitura))


class AvaliacaoDAO:
    def cadastrar(self, avaliacao: Avaliacao):
        sql = "INSERT INTO avaliacao (id_leitura, nota, comentario) VALUES (%s, %s, %s)"
        return _cadastrar(sql, (avaliacao.id_leitura, avaliacao.nota, avaliacao.comentario))

    def listar(self):
        registros = _consultar(
            "SELECT id_avaliacao, id_leitura, nota, comentario "
            "FROM avaliacao ORDER BY id_avaliacao"
        )
        return [Avaliacao(r["id_leitura"], r["nota"], r["comentario"], r["id_avaliacao"]).to_dict() for r in registros]

    def buscar(self, id_avaliacao):
        registros = _consultar(
            "SELECT id_avaliacao, id_leitura, nota, comentario "
            "FROM avaliacao WHERE id_avaliacao = %s",
            (id_avaliacao,),
        )
        if not registros:
            return None
        r = registros[0]
        return Avaliacao(r["id_leitura"], r["nota"], r["comentario"], r["id_avaliacao"]).to_dict()
