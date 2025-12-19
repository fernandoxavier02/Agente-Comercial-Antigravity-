from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: str = "local"
    APP_NAME: str = "estetica-agent-api"
    LOG_LEVEL: str = "INFO"
    DATA_DIR: str = "./.data"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/estetica_agent"

    CLASSIFIER_PROMPT_VERSION: str = "v0.1"
    COMPOSER_PROMPT_VERSION: str = "v0.1"

settings = Settings()
