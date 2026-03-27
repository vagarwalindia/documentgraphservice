from confluent_kafka import Consumer
import threading
import json

from infrastructure.config.settings import settings
from infrastructure.kafka.loader import load_consumers
from infrastructure.kafka.registry import listeners


def run_consumer(listener):
    consumer = Consumer({
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': listener["group_id"],
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False
    })

    consumer.subscribe([listener["topic"]])

    print(f"Started consumer for {listener['topic']}")

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print("Kafka error:", msg.error())
                continue

            try:
                data = json.loads(msg.value().decode())

                listener["function"](data)

                consumer.commit(msg)

            except Exception as e:
                print("Processing failed:", e)

    finally:
        consumer.close()


def start_kafka_consumers():
    load_consumers()
    if not listeners:
        print("No Kafka listeners found")
        return
    for listener in listeners:
        thread = threading.Thread(
            target=run_consumer,
            args=(listener,),
            daemon=True
        )
        thread.start()