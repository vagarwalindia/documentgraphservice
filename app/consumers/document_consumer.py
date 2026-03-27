

from infrastructure.kafka.decorator import KafkaListener


@KafkaListener(topic="documents-uploaded-topic", group_id="order-group")
def handle_order(event: dict):

    print(f"Processing order: {event}")