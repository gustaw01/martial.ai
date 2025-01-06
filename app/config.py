from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    PGDATABASE: str = "db"
    PGUSER: str = "db_owner"
    PGPASSWORD: SecretStr
    PGHOST: SecretStr
    PGPORT: int = 5432
    PGSSLMODE: str = "require"
    MODEL_NAME: str = "text-embedding-ada-002"
    OPENAI_API_KEY: SecretStr
    VECTOR_LENGTH: int = 1536
    DATABASE_LOGGING_LEVEL: str = "INFO"
