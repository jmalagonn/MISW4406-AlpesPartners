import json, pulsar, atexit, time, signal, sys
from .pulsar_client import client

running = True

def _with_retry(fn, what, tries=40, base=0.5, cap=8.0):
    delay = base
    for i in range(tries):
        try:
            return fn()
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(delay)
            delay = min(delay * 1.7, cap)

def start_consumer(topic: str, subscription: str, handler, dead_letter_topic: str | None = None):
    global running

    dlt = dead_letter_topic or f"{topic}-DLQ"
    dlp = pulsar.ConsumerDeadLetterPolicy(
        max_redeliver_count=5,
        dead_letter_topic=dlt,
    )  

    cons: pulsar.Consumer = _with_retry(
        lambda: client().subscribe(
            topic,
            subscription_name=subscription,
            consumer_type=pulsar.ConsumerType.KeyShared,     
            initial_position=pulsar.InitialPosition.Latest,   
            dead_letter_policy=dlp,
            unacked_messages_timeout_ms=30000,                         
            negative_ack_redelivery_delay_ms=2000,                    
            receiver_queue_size=1000,                         
        ),
        "pulsar subscribe"
    )

    atexit.register(lambda: (cons and cons.close()))

    def shutdown_handler(sig, frame):
        global running
        print("⚠️ SIGTERM recibido, cerrando consumidor...")
        running = False

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    while running:
        try:
            msg = cons.receive(timeout_millis=5000)
        except pulsar.Timeout:
            continue
        
        try:
            payload = json.loads(msg.data().decode("utf-8"))
            props = msg.properties() or {}
            
            handler(payload, props)
            cons.acknowledge(msg)
        except Exception:
            cons.negative_acknowledge(msg)

    print("Cerrando consumidor Pulsar...")
    cons.close()
    print("Consumidor cerrado, worker terminado.")
    sys.exit(0)