from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    mongodb_uri: str
    database_name: str
    email_user: str
    email_pass: str
    smtp_host: str = "p1432.use1.mysecurecloudhost.com"
    smtp_port: int = 465
    smtp_use_ssl: bool = True
    frontend_url: str = "http://localhost:3000"
    jwt_secret: str = "default_secret_change_in_production"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env file

settings = Settings()
