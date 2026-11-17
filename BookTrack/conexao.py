"""Conexao com o banco booktrack no XAMPP (MySQL/MariaDB)."""

import mysql.connector


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Configuracao local padrao do XAMPP
        database="booktrack",
        connection_timeout=5,
    )


if __name__ == "__main__":
    try:
        banco = conectar()
        print("Conectado ao banco BookTrack!")
        banco.close()
    except mysql.connector.Error as erro:
        print("Erro na conexao:", erro)
