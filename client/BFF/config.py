import os

class Settings:
    AFFILIATES_API_URL = os.environ.get("AFFILIATES_API_URL"),
    LOYALTY_API_URL = os.environ.get("AFFILIATES_API_URL"),
    ALLIANCES_API_URL = os.environ.get("AFFILIATES_API_URL"),
    DEFAULT_TIMEOUT = float(os.environ.get("DEFAULT_TIMEOUT", "2.0")),
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    PULSAR_URL = os.getenv("PULSAR_URL")
    TOPIC_COMMANDS_ALLIANCES = os.getenv("TOPIC_COMMANDS_ALLIANCES")

settings = Settings()