from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    ELASTIC_INDEX: str
    ELASTIC_URL: str
    KAFKA_CLIENT_ID: str
    KAFKA_CONSUMER_TIMEOUT_MS: int
    KAFKA_CONSUMER_GROUP: str
    KAFKA_TOPIC: str
    KAFKA_URL: str

    class Config:
        case_sensitive = True


settings = Settings()
