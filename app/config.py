from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Banco de dados
    DATABASE_URL: str = "mysql+pymysql://root:senha@localhost:3306/expense_db"

    # JWT
    SECRET_KEY: str = "troque-esta-chave-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 dia

    class Config:
        env_file = ".env"


settings = Settings()
