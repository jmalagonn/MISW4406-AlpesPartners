import os

class Settings:
    SERVICE_NAME = "Affiliates"
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://app:app@db:5432/app")
    BROKER_URL = os.getenv("BROKER_URL", "amqp://guest:guest@mq:5672//")
    RESULT_BACKEND = os.getenv("RESULT_BACKEND", None)
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()