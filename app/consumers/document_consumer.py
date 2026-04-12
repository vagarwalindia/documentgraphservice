from app.services.pipeline_factory import PipeLineFactory
from infrastructure.kafka.decorator import KafkaListener


@KafkaListener(topic="documents-uploaded-topic", group_id="order-group")
def handle_order(event: dict):
    pipeline = PipeLineFactory.get_pipeline(event["doc_type"])
    pipeline.process_document(doc_type=event["doc_type"], doc=event["doc_type"])
