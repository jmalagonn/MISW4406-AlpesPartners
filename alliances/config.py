import os

class Settings:
    SERVICE_NAME = "Alliances"
    DATABASE_URL = os.getenv("DATABASE_URL")
    PULSAR_URL = os.getenv("PULSAR_URL")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
