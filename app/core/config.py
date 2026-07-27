from pydantic_settings  import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Industrial Edge AI"

    # DATABASE CONFIGURATION
    DATABASE_URL : str

    # SECURITY & JWT CONFIGURATION
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 

    # Tell Pydantic to read variables from the local .env file
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Instantiate settings to be imported across the application
settings = Settings()