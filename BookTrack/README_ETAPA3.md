# BookTrack | Etapa 3 | Entrega final: 17/11/2026

Projeto integrado DWS + POO + BD do 2º TI. Sistema de acompanhamento de livros, leituras e avaliações, com dados armazenados em MySQL (XAMPP) e interface em HTML, CSS e JavaScript consumindo a API Flask via `fetch()`.

## O que foi desenvolvido

- **Python e POO:** classes `Livro`, `Leitura` e `Avaliacao`.
- **DAO:** cadastro e consulta nas tabelas do banco; atualização de status de leitura.
- **Flask:** API de livros, leituras e avaliações e página inicial do sistema.
- **Front-end:** painel, estante de livros, busca, filtros, cadastro de livros, registro de leitura, avaliação de 1 a 5 estrelas e histórico com contagem mensal/anual.
- **Integração:** as telas usam `fetch()` para salvar e consultar dados reais no banco.

## Pré-requisitos

1. Ter Python 3 instalado no computador.
2. Ter XAMPP com **MySQL** iniciado.
3. Ter o banco `booktrack` no phpMyAdmin, com as tabelas `livro`, `leitura` e `avaliacao`.
4. Se estiver em um computador diferente do usado na etapa 1, criar o banco `booktrack` no phpMyAdmin e importar o arquivo `booktrack.sql` do GitHub **somente se o banco ainda não existir**.

> Não apague as tabelas existentes. A aplicação utiliza o banco das etapas anteriores, sem recriá-lo.

## Como instalar e executar pelo VS Code (Windows)

1. Copie os arquivos desta etapa para a **mesma pasta** do BookTrack da etapa 2. Confirme que `app.py`, `dao.py`, `templates/` e `static/` estejam na raiz dessa pasta. Mantenha seu arquivo `booktrack.sql` e as imagens dos diagramas.
2. Abra a pasta no VS Code, clique em **Terminal > New Terminal**.
3. Se a pasta `.venv` já existir e estiver funcionando, utilize-a. Caso contrário, crie o ambiente com:

   ```powershell
   py -m venv .venv
   ```

   Se `py` não funcionar, mas `python` funcionar, use `python -m venv .venv`.

4. Instale as bibliotecas no ambiente virtual:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

5. Inicie o **MySQL** no XAMPP.
6. Abra um terminal no VS Code e execute:

   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```

7. Abra **http://127.0.0.1:5000/** no navegador. **Nao abra o arquivo `templates/index.html` diretamente**, porque ele depende do Flask.
8. Abra **outro terminal** no VS Code (mantenha o Flask executando no primeiro) e verifique:

   ```powershell
   .\.venv\Scripts\python.exe testar_etapa3.py
   ```

   Saída esperada: `SUCESSO: site e rotas da etapa 3 estao acessiveis!`.

9. Na interface, faça um teste manual: cadastre um livro, marque uma leitura como concluída, avalie-a e confira a estante e o gráfico.

## Fluxo de uso

1. **Novo livro**: informe título, autor e gênero, depois salve.
2. **Leitura**: selecione o livro e o status `Quero ler`, `Lendo` ou `Concluído`. Se concluiu, informe a data.
3. **Avaliação**: escolha uma leitura concluída e dê de 1 a 5 estrelas. Uma mesma leitura pode receber somente uma avaliação.
4. **Biblioteca**: pesquise livros pelo título, autor e gênero, filtre por status, inicie ou conclua leituras.
5. **Painel**: acompanhe o total de livros, leituras em andamento, livros concluídos em cada ano e notas cadastradas. Os gráficos contam registros de leitura concluída, inclusive releituras.

## Estrutura de pastas

```text
booktrack/
  app.py                 # rotas Flask e pagina inicial
  conexao.py             # conexao com o MySQL
  dao.py                 # classes de acesso ao banco
  livro.py               # classe Livro
  leitura.py             # classe Leitura
  avaliacao.py           # classe Avaliacao
  testar_etapa2.py       # teste da API
  testar_etapa3.py       # teste da interface + API
  requirements.txt       # bibliotecas Python
  .gitignore
  templates/
    index.html           # pagina principal
  static/
    style.css            # visual e responsividade
    app.js               # fetch, formulários, filtros e gráficos
  booktrack.sql          # arquivo da etapa 1 (mantenha)
  modelo-conceitual.png  # arquivo da etapa 1 (mantenha)
  mmmodelo-logico.png    # arquivo da etapa 1 (mantenha)
  diagrama.png           # arquivo da etapa 1 (mantenha)
```

## Rotas disponíveis

| Verbo | Caminho | Finalidade |
|---|---|---|
| GET | `/` | Abrir o site |
| GET | `/api` | Testar API |
| GET | `/livros` | Listar livros |
| POST | `/livros` | Cadastrar livro |
| GET | `/livros/<id>` | Buscar livro |
| GET | `/leituras` | Listar leituras |
| POST | `/leituras` | Cadastrar leitura |
| PATCH | `/leituras/<id>` | Atualizar status da leitura |
| GET | `/leituras/<id>` | Buscar leitura |
| GET | `/avaliacoes` | Listar avaliações |
| POST | `/avaliacoes` | Cadastrar avaliação |
| GET | `/avaliacoes/<id>` | Buscar avaliação |

## GitHub e Classroom

1. Mantenha o repositório existente `https://github.com/harasbr/booktrack` e a colaboração já adicionada do professor Léo.
2. Envie os arquivos novos ou modificados desta etapa, inclusive **as pastas `static/` e `templates/`**. Não envie `.venv`, `__pycache__` nem segredos.
3. Use um novo commit: `Etapa 3 - Interface HTML CSS JS integrada ao Flask com Fetch`.
4. No Classroom, anexe o link do **mesmo repositório** e clique em Entregar. Se o professor pedir outros anexos, siga também as instruções específicas da atividade.

## Solução de problemas

- **Página não abre:** mantenha o `app.py` executando no terminal. Use `http://127.0.0.1:5000/`.
- **Erro ao carregar biblioteca:** abra o XAMPP, ligue o MySQL e confirme o banco `booktrack`.
- **Erro 500:** confira `conexao.py`, usuário, senha, nome do banco e porta usada no seu XAMPP.
- **Erro `No module named flask` ou `mysql`:** instale as dependências no `.venv` com o comando do passo 4.
- **Porta 5000 já em uso:** feche o Flask anterior com `Ctrl + C` e execute uma única instância.
- **Aviso de importação no VS Code:** use `Ctrl + Shift + P` > `Python: Select Interpreter` > `.venv\Scripts\python.exe`.

### Notas

O servidor usa `debug=True` apenas para desenvolvimento escolar local, em `127.0.0.1`. Não publique assim na internet. A senha vazia do arquivo `conexao.py` pressupõe a configuração local padrão do XAMPP. Nunca publique uma senha real no GitHub.
