from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Optional, Any

class EnvSettings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "postgres"
    DB_TYPE: str = "postgresql"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    FIREBASE_STORAGE_BUCKET_URL: str = "your-bucket.appspot.com"
    
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @field_validator("*", mode="before")
    @classmethod
    def empty_str_to_default(cls, v: Any, info: Any) -> Any:
        if v == "":
            # Return the default value for the field if it exists
            return cls.model_fields[info.field_name].default
        return v
    

env = EnvSettings()