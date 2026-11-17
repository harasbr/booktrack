"""Classe de dominio Avaliacao."""


class Avaliacao:
    def __init__(self, id_leitura, nota, comentario=None, id_avaliacao=None):
        self.id_avaliacao = id_avaliacao
        self.id_leitura = id_leitura
        self.nota = nota
        self.comentario = comentario

    def to_dict(self):
        return {
            "id_avaliacao": self.id_avaliacao,
            "id_leitura": self.id_leitura,
            "nota": self.nota,
            "comentario": self.comentario,
        }
