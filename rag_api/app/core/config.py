from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    openai_api_key: str
    embedding_model: str = "sentence-transformers/all-MiniLm-L6-v2"
    embedding_service_url: str
    generation_service_url: str
    embedding_dim: int = 384
    chat_model: str = "gpt-4.1-mini"
    upload_dir: str = "uploads"
    


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")




settings = Settings()
