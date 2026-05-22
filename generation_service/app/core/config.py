from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ollama_base_url: str = "http://ollama:11434"
    ollama_chat_model: str = "llama3.2:3b"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()