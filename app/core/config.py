from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=BASE_DIR / ".." / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Informations de connexion PostgreSQL (obligatoires) ---
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # URI de connexion SQLAlchemy. Peut être défini directement via .env,
    # sinon construit à partir des variables Postgres ci-dessus.
    SQLALCHEMY_DATABASE_URI: str | None = None

    # --- JWT / sécurité ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

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
