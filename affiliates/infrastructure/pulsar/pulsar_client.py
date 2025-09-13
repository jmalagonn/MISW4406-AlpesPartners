import os, pulsar

PULSAR_URL = os.getenv("PULSAR_URL")

def client() -> pulsar.Client:
  return pulsar.Client(PULSAR_URL)