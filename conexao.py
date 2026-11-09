
import mysql.connector


def conectar():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="booktrack"
    )
    return conexao


try:
    banco = conectar()
    print("Conectado ao banco BookTrack!")
    banco.close()

except Exception as erro:
    print("Erro na conexão:", erro)
