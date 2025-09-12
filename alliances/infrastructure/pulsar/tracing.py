import uuid


def new_correlation_id():
  return str(uuid.uuid4())