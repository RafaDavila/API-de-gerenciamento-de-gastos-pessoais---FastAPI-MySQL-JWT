from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, categories, transactions

# Cria as tabelas no banco (para um projeto de portfólio; em produção use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gerenciamento de Gastos Pessoais",
    description="API REST para controle de receitas, despesas e categorias, com autenticação JWT.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "API de Gastos Pessoais rodando. Acesse /docs para a documentação interativa."}
