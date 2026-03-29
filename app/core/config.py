from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # --- Informations de connexion PostgreSQL (obligatoires) ---
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(..., env="POSTGRES_PORT")

    # URI de connexion SQLAlchemy. Peut être défini directement via .env,
    # sinon construit à partir des variables Postgres ci-dessus.
    SQLALCHEMY_DATABASE_URI: str | None = None

    # --- JWT / sécurité ---
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = BASE_DIR / ".." / ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **data):
        # On construit toujours avec pydantic-settings, puis on complète si besoin.
        super().__init__(**data)

        # Si l'URI n'est pas fournie, on compose à partir des variables Postgres.
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = (
                f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )

# Instance globale utilisée partout.
settings = Settings()
