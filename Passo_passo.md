# Passo a passo: clonar e rodar o Projeto-Crud

CRUD de produtos :
 **FastAPI** (backend), 
 **Streamlit** (frontend), 
 **PostgreSQL** 
 **Docker**. 
 **Poetry**.

## Pré-requisitos

- Git
- Docker e Docker Compose
  - No Windows: Docker Desktop, ou Docker instalado direto no WSL (Ubuntu)
  - No Linux/Mac: Docker Engine ou Docker Desktop
  - Python 3.12 ou superior e Poetry

## 1. Clonar o repositório

```bash
git clone https://github.com/flrmedeiros78/Projeto-Crud.git
cd Projeto-Crud
```

## 2. Criar o arquivo `.env` 
utilize o arquivo '.env.example'

Mantenha `DB_HOST=postgres` e `@postgres:5432`: dentro do Docker, o banco se chama `postgres`.

## 3. Iniciar o Docker

**Se o Docker foi instalado direto no WSL/Ubuntu**, terá que startar do docker:
```bash
sudo service docker start
```
**Se usa Docker Desktop**, basta abri-lo e esperar o status "Engine running". 
Em WSL, ligue também o Ubuntu em Settings → Resources → WSL Integration.

Confira se está funcionando:
```bash
docker --version
docker compose version
docker compose ps
```

## 4. Subir o projeto
```bash
docker compose up --build ou `docker compose up --build -d`
```

Na primeira vez demora um pouco pois, baixa as imagens e instala as dependências
Quando terminar, os três containers estarão rodando: `postgres`, `backend` e `frontend`.

## 5. Acessar
API (documentação interativa) - http://localhost:8000/docs
Frontend (Streamlit) - http://localhost:8501

Teste criando, editando e excluindo um produto pelo frontend ou pela documentação da API.

## 6. Parar o projeto
```bash
docker compose down
```

Os dados do banco ficam guardados no volume `postgres_data`.

Para apagar também os dados, use:
```bash
docker compose down -v
```
## Desenvolvimento local com Poetry e VS Code (opcional)
1. Instale as dependências. O ambiente virtual é criado na pasta `.venv` do projeto:

   ```bash
   poetry install
   ```

2. Confira o ambiente:

   ```bash
   poetry env info --path
   poetry run python -c "import fastapi, sqlalchemy, streamlit; print('ok')"
   ```

3. No VS Code, instale as extensões **Python**, **Pylance** e **Docker**. 
Depois pressione `Ctrl+Shift+P`, 
escolha **Python: Select Interpreter** e selecione `./.venv/bin/python`.

O `streamlit` e o `uvicorn` existem só dentro do `.venv`. 
- Para usá-los fora do Docker, rode com `poetry run`, por exemplo `poetry run streamlit run app.py` dentro da pasta `FRONTEND`. 
- Para o backend rodar fora do Docker, ajuste o `.env` para `DB_HOST=localhost` e `@localhost` na `DATABASE_URL`, e suba apenas o banco com `docker compose up -d postgres`.

## Problemas comuns
**`failed to connect to the docker API at unix:///var/run/docker.sock`**
O serviço do Docker não está rodando. 
 - No WSL, rode `sudo service docker start`. Com Docker Desktop, abra o aplicativo.

**Porta 5432 já em uso**
Você tem outro Postgres rodando. Mude `DB_PORT` no `.env` para outra porta, por exemplo `5433`. Mantenha `5432` dentro da `DATABASE_URL`, é a porta interna do container.

**Alterei o `.env` e nada mudou**
Recrie os containers:

```bash
docker compose down
docker compose up --build
```

**`streamlit: command not found`**
O Streamlit está só no `.venv`. 
- Use `poetry run streamlit ...` ou acesse o frontend que já roda no Docker, em http://localhost:8501.

**Ver os logs de um serviço**
```bash
docker compose logs backend
docker compose logs frontend
docker compose logs postgres
```

