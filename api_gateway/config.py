from functools import lru_cache
from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Core URLs / secrets
    JWKS_URL: AnyUrl = "http://keycloak:8080/realms/money-transfer/protocol/openid-connect/certs"
    REDIS_URL: str = "redis://redis:6379/0"

    # Load-balancer target maps
    USER_BACKENDS: str = "user_service:50051"
    TX_BACKENDS: str = "transaction_service:50052"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
