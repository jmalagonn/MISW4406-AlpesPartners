import os

class Settings:
    SERVICE_NAME = "Alliances"
    DATABASE_URL = os.getenv("DATABASE_URL")
    PULSAR_URL = os.getenv("PULSAR_URL")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    TOPIC_COMMANDS_TRACKING = os.getenv("TOPIC_COMMANDS_TRACKING", "commands.tracking")
    TOPIC_EVENTS_TRACKING = os.getenv("TOPIC_EVENTS_TRACKING", "events.tracking")
    TOPIC_COMMANDS_AFFILIATES = os.getenv("TOPIC_COMMANDS_AFFILIATES", "commands.affiliates")
    TOPIC_EVENTS_AFFILIATES = os.getenv("TOPIC_EVENTS_AFFILIATES", "events.affiliates")
    TOPIC_EVENTS_ALLIANCES = os.getenv("TOPIC_EVENTS_ALLIANCES", "events.alliances")

settings = Settings()
