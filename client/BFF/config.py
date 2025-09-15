import os

class Settings:
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    PULSAR_URL = os.getenv("PULSAR_URL")
    API_TIMEOUT = float(os.getenv("API_TIMEOUT", "5.0"))    
    AFFILIATES_API_URL = os.environ.get("AFFILIATES_API_URL")
    TOPIC_COMMANDS_AFFILIATES = os.environ.get("TOPIC_COMMANDS_AFFILIATES")
    LOYALTY_API_URL = os.environ.get("AFFILIATES_API_URL")
    DEFAULT_TIMEOUT = float(os.environ.get("DEFAULT_TIMEOUT", "2.0"))
    ALLIANCES_API_URL = os.getenv("ALLIANCES_API_URL")
    TOPIC_COMMANDS_ALLIANCES = os.getenv("TOPIC_COMMANDS_ALLIANCES")
    TRACKING_API_URL = os.getenv("TRACKING_API_URL")
    TOPIC_COMMANDS_TRACKING = os.getenv("TOPIC_COMMANDS_TRACKING")

settings = Settings()