import time

class RetryPolicy:
    def __init__(self, max_attempts=3, backoff_seconds=2):
        self.max_attempts = max_attempts
        self.backoff_seconds = backoff_seconds

    def backoff(self, attempt):
        time.sleep(self.backoff_seconds * attempt)  # linear backoff