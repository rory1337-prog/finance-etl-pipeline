from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database
    database_url: str
    # BingX
    bingx_base_url: str = "https://open-api.bingx.com"
    bingx_api_key: str | None = None
    bingx_secret_key: str | None = None
    # ETL
    default_interval: str = "1d"
    default_limit: int = 365

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )
settings = Settings()