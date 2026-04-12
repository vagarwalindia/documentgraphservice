class DefaultErrorHandler:
    def __init__(self, retry_policy, dlt_publisher):
        self.retry_policy = retry_policy
        self.dlt_publisher = dlt_publisher

    def handle(self, msg, exception, attempt):
        if attempt < self.retry_policy.max_attempts:
            print(f"[Retry] attempt={attempt} error={exception}")
            self.retry_policy.backoff(attempt)
            return "RETRY"

        print(f"[DLT] sending message after {attempt} attempts")
        self.dlt_publisher.publish(msg, exception, attempt)
        return "DLT"