from pydantic import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    acces_token_expire_minutes: int
    test_email: EmailStr
    PROJECT_NAME: str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"

    # we use pydantic to collect the necesary data from .env file
    # for our schema and validated it
    class Config:
        env_file = ".env"


settings = Settings()
