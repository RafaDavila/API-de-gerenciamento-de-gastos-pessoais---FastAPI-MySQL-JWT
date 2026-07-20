# API-de-gerenciamento-de-gastos-pessoais---FastAPI-MySQL-JWT

# API de Gerenciamento de Gastos Pessoais

API REST desenvolvida com **FastAPI** para controle de receitas e despesas pessoais, com autenticação via **JWT** e persistência em **MySQL**.

## ✨ Funcionalidades

- Cadastro e login de usuários (senha com hash bcrypt, autenticação JWT)
- CRUD de categorias de gastos (ex: Alimentação, Transporte, Lazer)
- CRUD de transações (receitas e despesas), vinculadas a um usuário e opcionalmente a uma categoria
- Filtros por tipo, categoria e intervalo de datas
- Endpoint de **resumo financeiro**: total de receitas, despesas, saldo e gastos agrupados por categoria
- Documentação automática interativa (Swagger/OpenAPI) em `/docs`
- Cada usuário só acessa seus próprios dados (isolamento por usuário)

## 🛠 Stack

- **Python 3.11+**
- **FastAPI** — framework web
- **SQLAlchemy** — ORM
- **MySQL** — banco de dados
- **python-jose** — geração/validação de JWT
- **passlib (bcrypt)** — hash de senhas
- **Pydantic v2** — validação de dados

## 📁 Estrutura do projeto

```
expense-api/
├── app/
│   ├── main.py            # ponto de entrada da aplicação
│   ├── config.py          # configurações (variáveis de ambiente)
│   ├── database.py        # conexão SQLAlchemy
│   ├── models.py           # modelos ORM (User, Category, Transaction)
│   ├── schemas.py          # schemas Pydantic (validação/serialização)
│   ├── auth.py             # hash de senha e JWT
│   ├── dependencies.py     # dependência get_current_user
│   └── routers/
│       ├── auth.py          # /auth/register, /auth/login
│       ├── categories.py    # /categories
│       └── transactions.py  # /transactions (+ /transactions/summary)
├── requirements.txt
├── docker-compose.yml      # sobe um MySQL local
├── .env.example
└── README.md
```

## 🚀 Como rodar localmente

### 1. Suba o banco MySQL (via Docker)

```bash
docker compose up -d
```

Isso cria um MySQL em `localhost:3306`, banco `expense_db`, usuário `root`, senha `senha`.

> Não quer usar Docker? Só ter um MySQL rodando localmente e criar o banco `expense_db` manualmente.

### 2. Crie o ambiente virtual e instale as dependências

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` se necessário (principalmente `SECRET_KEY` em produção).

### 4. Rode a aplicação

```bash
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`. As tabelas são criadas automaticamente na primeira execução.

### 5. Explore a documentação interativa

Acesse **http://localhost:8000/docs** (Swagger UI) para testar todos os endpoints direto do navegador.

## 🔑 Fluxo de uso básico

1. `POST /auth/register` — cria um usuário
2. `POST /auth/login` — retorna um `access_token` (JWT)
3. Use o header `Authorization: Bearer <token>` nas próximas requisições
4. `POST /categories/` — cria categorias (ex: "Alimentação", "Transporte")
5. `POST /transactions/` — registra receitas/despesas
6. `GET /transactions/?type=expense&start_date=2026-01-01` — filtra transações
7. `GET /transactions/summary` — vê o resumo financeiro

## 📌 Principais endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/register` | Cria um novo usuário |
| POST | `/auth/login` | Autentica e retorna JWT |
| GET/POST | `/categories/` | Lista/cria categorias |
| PUT/DELETE | `/categories/{id}` | Atualiza/remove categoria |
| GET/POST | `/transactions/` | Lista (com filtros) / cria transações |
| GET/PUT/DELETE | `/transactions/{id}` | Detalha/atualiza/remove transação |
| GET | `/transactions/summary` | Resumo financeiro por período |


