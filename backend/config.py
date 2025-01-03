from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ASTRA_DB_ENDPOINT: str
    ASTRA_DB_APPLICATION_TOKEN: str
    GEMINI_API_KEY: str
    GEMINI_API_ENDPOINT: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    class Config:
        env_file = ".env"

settings = Settings()