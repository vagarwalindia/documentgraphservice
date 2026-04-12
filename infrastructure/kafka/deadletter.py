import json

class DeadLetterPublisher:
    def __init__(self, producer, dlt_topic):
        self.producer = producer
        self.dlt_topic = dlt_topic

    def publish(self, msg, error, attempt):
        headers = [
            ("error", str(error).encode()),
            ("attempt", str(attempt).encode()),
            ("original_topic", msg.topic().encode())
        ]

        self.producer.produce(
            self.dlt_topic,
            value=msg.value(),
            headers=headers
        )