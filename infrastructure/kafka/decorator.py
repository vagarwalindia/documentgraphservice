from infrastructure.kafka.registry import listeners


def KafkaListener(topic: str, group_id: str):
    def decorator(func):
        listeners.append({
            "topic": topic,
            "group_id": group_id,
            "function": func
        })
        return func
    return decorator