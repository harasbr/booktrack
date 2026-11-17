"""Classe de dominio Leitura."""


class Leitura:
    def __init__(self, id_livro, status_leitura, data_conclusao=None, id_leitura=None):
        self.id_leitura = id_leitura
        self.id_livro = id_livro
        self.status_leitura = status_leitura
        self.data_conclusao = data_conclusao

    def to_dict(self):
        data = self.data_conclusao
        if hasattr(data, "isoformat"):
            data = data.isoformat()
        return {
            "id_leitura": self.id_leitura,
            "id_livro": self.id_livro,
            "status_leitura": self.status_leitura,
            "data_conclusao": data,
        }
