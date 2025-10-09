from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str
    MODEL_FAST: str = "gpt-4o-mini"
    MODEL_PREMIUM: str = "gpt-4o"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()