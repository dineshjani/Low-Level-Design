import threading
import time
from collections import deque

class RateLimiter:
    def __init__(self, time_window_in_seconds, bucket_capacity):
        self.time_window_in_seconds = time_window_in_seconds
        self.bucket_capacity = bucket_capacity
        self.sliding_window = deque()
    
    def grant_access(self):
        current_time = time.time() * 1000  # Convert to milliseconds
        self.check_and_update_queue(current_time)
        if len(self.sliding_window) < self.bucket_capacity:
            self.sliding_window.append(current_time)
            return True
        return False

    def check_and_update_queue(self, current_time):
        while self.sliding_window:
            elapsed_time = (current_time - self.sliding_window[0]) / 1000  # Convert to seconds
            if elapsed_time >= self.time_window_in_seconds:
                self.sliding_window.popleft()
            else:
                break

class UserBucketCreator:
    def __init__(self, id):
        self.bucket = {id: RateLimiter(1, 5)}

    def access_application(self, id):
        if self.bucket[id].grant_access():
            print(threading.current_thread().name + " -> able to access the application")
        else:
            print(threading.current_thread().name + " -> Too many requests, please try after some time")

if __name__ == "__main__":
    user_bucket_creator = UserBucketCreator(1)
    num_threads = 12
    threads = []

    for i in range(num_threads):
        thread = threading.Thread(target=lambda: user_bucket_creator.access_application(1))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

