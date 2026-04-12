from confluent_kafka import KafkaException

class KafkaConsumerRunner:
    def __init__(self, consumer, handler, error_handler):
        self.consumer = consumer
        self.handler = handler
        self.error_handler = error_handler

    def start(self):
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print("Kafka error:", msg.error())
                continue

            attempt = 1

            while True:
                try:
                    self.handler.handle(msg)   # 👈 business logic
                    break

                except Exception as e:
                    action = self.error_handler.handle(msg, e, attempt)

                    if action == "RETRY":
                        attempt += 1
                        continue
                    else:
                        break