import json, logging


def handle_create_brand(cmd):
  logging.info("Received command=%s", json.dumps(cmd))