import uuid, datetime as dt

def with_correlation(props: dict | None) -> dict:
    props = dict(props or {})
    props.setdefault("correlationId", str(uuid.uuid4()))
    props.setdefault("sagaId", props["correlationId"])
    props.setdefault("eventTime", str(int(dt.datetime.utcnow().timestamp() * 1000)))
    return props
