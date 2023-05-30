from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["INFO", "DEBUG", "WARNING", "CRITICAL", "ERROR"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:"
            f"{self.DB_PASS}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def database_test_url(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.TEST_DB_USER}:"
            f"{self.TEST_DB_PASS}@"
            f"{self.TEST_DB_HOST}:"
            f"{self.TEST_DB_PORT}/"
            f"{self.TEST_DB_NAME}"
        )

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    SECRET_KEY: str
    ALGORITHM: str

    ADMIN_MAIL: str

    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = ".env"


settings = Settings()
