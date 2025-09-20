import os

class Settings:
    SERVICE_NAME = "Tracking"
    DATABASE_URL = os.getenv("DATABASE_URL")
    PULSAR_URL = os.getenv("PULSAR_URL")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    TOPIC_EVENTS_TRACKING = os.getenv("TOPIC_EVENTS_TRACKING", "events.tracking")

settings = Settings()
