"""Classe de dominio Livro."""


class Livro:
    def __init__(self, titulo, autor, genero=None, id_livro=None):
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.genero = genero

    def to_dict(self):
        return {
            "id_livro": self.id_livro,
            "titulo": self.titulo,
            "autor": self.autor,
            "genero": self.genero,
        }
