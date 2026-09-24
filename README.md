# CRUD de Produtos com FastAPI, PostgreSQL e Docker

API REST para cadastro e gerenciamento de produtos, construída durante o treinamento **Jornada de Dados**. O projeto implementa as quatro operações básicas de um CRUD (Create, Read, Update e Delete) sobre uma tabela no PostgreSQL, com validação de dados, documentação automática e ambiente totalmente containerizado.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-gerenciador-60A5FA?logo=poetry&logoColor=white)

## O que o projeto faz

- Cadastra, lista, busca por ID, atualiza e remove produtos.
- Valida os dados de entrada e saída com **Pydantic** (e-mail do fornecedor válido, valor maior que zero, campos obrigatórios).
- Persiste os dados em **PostgreSQL** usando o **SQLAlchemy ORM**.
- Cria a tabela automaticamente na inicialização da aplicação.
- Gera documentação interativa (Swagger UI) sem configuração extra.
- Sobe backend e banco com um único comando via **Docker Compose**.

## Stack

| Camada              | Tecnologia                                                   |
|---------------------|--------------------------------------------------------------|
| Linguagem           | Python 3.12                                                  |
| Framework web       | FastAPI                                                      |
| Servidor ASGI       | Uvicorn                                                      |
| Validação e schemas | Pydantic v2 (`EmailStr`, `Field`, `Annotated`)               |
| ORM                 | SQLAlchemy 2.x                                               |
| Banco de dados      | PostgreSQL 16                                                |
| Driver              | psycopg2-binary                                              |
| Containers          | Docker e Docker Compose                                      |
| Dependências        | Poetry (`pyproject.toml`) e `requirements.txt` para a imagem |
| Versionamento       | Git e GitHub                                                 |
|------------------------------------------------------------------------------------|
## Arquitetura

O backend é dividido em camadas, cada uma com uma responsabilidade:

```
               +------------------------+
               |  Cliente / Swagger UI  |
               +------------------------+
                            |
                            v
               +------------------------+
               |       router.py        |
               |       rotas HTTP       |
               +------------------------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
+------------------------+    +------------------------+
|       schema.py        |    |        crud.py         |
|   validação Pydantic   |    |   operações no banco   |
+------------------------+    +------------------------+
                                           |
                                           v
                              +------------------------+
                              |       models.py        |
                              |       tabela ORM       |
                              +------------------------+
                                           |
                                           v
                              +------------------------+
                              |      database.py       |
                              |    engine e sessão     |
                              +------------------------+
                                           |
                                           v
                              +------------------------+
                              |       PostgreSQL       |
                              +------------------------+
```

| Arquivo | Responsabilidade |
|---------------|-------------------------------------------------------------------------------------------|
| `main.py`     | Cria a aplicação FastAPI, registra o router e cria as tabelas                             |
| `router.py`   | Define os endpoints, injeta a sessão do banco (`Depends`) e trata erros 404               |
| `schema.py`   | Modelos Pydantic de entrada (`ProductCreate`, `ProductUpdate`) e saída (`ProductResponse`)|
| `crud.py`     | Funções de acesso a dados: consultar, inserir, atualizar e excluir                        |
| `models.py`   | Modelo ORM da tabela `tb_produtos`                                                        |
| `database.py` | Engine, `SessionLocal` e a dependência `get_db` (gerador com `yield`)                     |

## Estrutura de pastas

```text
CRUD/
├── BACKEND/
│   ├── main.py
│   ├── router.py
│   ├── schema.py
│   ├── crud.py
│   ├── models.py
│   ├── database.py
│   ├── requirements.txt
│   └── dockerfile-backend
├── FRONTEND/
│   └── dockerfile            # reservado para a próxima etapa
├── docker-compose.yml
├── pyproject.toml
└── poetry.lock
```

## Endpoints

| Método | Rota | Descrição |
|----------|--------------------------|-------------------------------|
| `GET`    | `/products/`             | Lista todos os produtos       |
| `GET`    | `/products/{product_id}` | Busca um produto pelo ID      |
| `POST`   | `/products/`             | Cria um produto               |
| `PUT`    | `/products/{product_id}` | Atualiza campos de um produto |
| `DELETE` | `/products/{product_id}` | Remove um produto             |

Quando o produto não existe, a API responde `404` com uma mensagem descritiva.

### Modelo de dados (`tb_produtos`)

| Campo | Tipo | Observação |
|--------------------|-------------|---------------------------------------|
| `id`               | inteiro     | chave primária                        |
| `name`             | texto       | nome do produto                       |
| `descricao`        | texto       | descrição                             |
| `valor`            | numérico    | deve ser maior que zero               |
| `categoria`        | texto       | categoria do produto                  |
| `email_fornecedor` | texto       | validado como e-mail                  |
| `dt_procs`         | data e hora | preenchida automaticamente na criação |

### Exemplo de requisição

```json
POST /products/
{
  "name": "Teclado Mecânico",
  "descricao": "Teclado ABNT2 com switch azul",
  "valor": 249.90,
  "categoria": "Periféricos",
  "email_fornecedor": "contato@fornecedor.com"
}
```

## Como executar

Pré-requisitos: [Docker](https://docs.docker.com/get-docker/) e Docker Compose.

```bash
git clone https://github.com/flrmedeiros78/Python.git
cd Python/CRUD
docker compose up --build
```

Depois de subir:

- Documentação Swagger: <http://localhost:8000/docs>
- Documentação ReDoc: <http://localhost:8000/redoc>
- PostgreSQL: `localhost:5432` (banco `mydatabase`)

Para parar e remover os containers: `docker compose down` (adicione `-v` para apagar também o volume do banco).

> As credenciais do banco no `docker-compose.yml` são de desenvolvimento. Em um ambiente real, use variáveis de ambiente e não versione senhas.

## Habilidades praticadas

**Back-end e APIs**
- Construção de API REST com FastAPI e organização em routers
- Injeção de dependências com `Depends` e geradores com `yield`
- Tratamento de erros HTTP com `HTTPException`
- Uso de `response_model` para controlar o que a API devolve

**Dados**
- Modelagem de tabelas com SQLAlchemy ORM
- Sessões, `commit`, `refresh` e consultas com `filter`
- Validação com Pydantic v2: tipos `Decimal`, `EmailStr`, `Annotated` e `Field(gt=0)`
- Separação entre schema de validação e modelo de banco de dados

**DevOps e ferramentas**
- Containerização com Dockerfile e orquestração com Docker Compose
- Rede interna entre serviços, volumes persistentes e variáveis de ambiente
- Leitura de configuração pelo ambiente com `os.getenv` e valor padrão
- Gerenciamento de dependências com Poetry
- Git e GitHub, `.gitignore`, mensagens de commit no padrão Conventional Commits
- Leitura de logs (`docker compose logs`) para diagnosticar falhas

## Desafios resolvidos durante o desenvolvimento

O projeto rendeu bons aprendizados de depuração:

1. **Problema:** `TypeError` ao usar `bool | None`
 - **Causa:** Imagem Docker com Python 3.9, enquanto o código usa sintaxe do 3.10+
 - **Resolução:** Atualizar a imagem base para `python:3.12-slim`

2. **Problema:** Build falhando com `pg_config not found`
 - **Causa:** `psycopg2` tentando compilar em imagem `slim`
 - **Resolução:** Trocar por `psycopg2-binary`

3. **Problema:** Erros de tipo no Pydantic com `condecimal`
 - **Causa:** Uso sem parênteses e sem parâmetros
 - **Resolução:** `Annotated[Decimal, Field(gt=0)]`

4. **Problema:** `create_all() got an unexpected keyword 'bin'`
 - **Causa:** Erro de digitação no parâmetro
 - **Resolução:** `bind=engine`

5. **Problema:** Compose construindo a imagem antiga
 - **Causa:** Arquivo de Dockerfile com nome diferente do configurado
 - **Resolução:** Alinhar `dockerfile:` no `docker-compose.yml`

6. **Problema:** Arquivos `__pycache__` no commit
 - **Causa:** Falta de `.gitignore` na raiz do projeto
 - **Resolução:** Criar `.gitignore` e remover do stage

7. **Problema:** Erro 500 ao devolver objetos do banco
 - **Causa:** `from_atributes` com erro de digitação, então o Pydantic não lia objetos do ORM
 - **Resolução:** `ConfigDict(from_attributes=True)`

8. **Problema:** `TypeError` ao listar ou buscar produtos
 - **Causa:** Duas funções `get_products` no mesmo arquivo; a segunda sobrescrevia a primeira
 - **Resolução:** Separar em `get_products` (lista) e `get_product` (um item)

9. **Problema:** `PUT` não atualizava corretamente
 - **Causa:** Condições testavam o objeto do banco e as atribuições sobrescreviam a variável
 - **Resolução:** Testar `product.campo` e gravar em `db_product.campo`

10. **Problema:** `create_engine` recebendo `None`
  - **Causa:** `os.getenv` chamado sem o nome da variável
  - **Resolução:** `os.getenv("DATABASE_URL", "valor_padrao")`

## Próximos passos em andamento:

- [ ] Mover as credenciais do banco para um arquivo `.env` fora do versionamento
- [ ] Adicionar healthcheck ao PostgreSQL e `depends_on` com `service_healthy`
- [ ] Migrações de banco com Alembic
- [ ] Usar `Numeric` no banco para o campo `valor`
- [ ] Testes automatizados com pytest e `TestClient`
- [ ] Construir o front-end (pasta `FRONTEND`)
- [ ] Paginação e filtros na listagem de produtos

## Créditos

Projeto desenvolvido como exercício prático do treinamento **Jornada de Dados**.

**Autor:** [flrmedeiros78](https://github.com/flrmedeiros78)