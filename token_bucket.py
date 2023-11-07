import threading
import time

class RateLimiter:
    def __init__(self, bucket_capacity, refresh_rate):
        self.bucket_capacity = bucket_capacity
        self.refresh_rate = refresh_rate
        self.current_capacity = bucket_capacity
        self.last_updated_time = time.time()

    def grant_access(self):
        self.refresh_bucket()
        if self.current_capacity > 0:
            self.current_capacity -= 1
            return True
        return False

    def refresh_bucket(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_updated_time
        additional_tokens = int(time_elapsed * self.refresh_rate)
        self.current_capacity = min(self.current_capacity + additional_tokens, self.bucket_capacity)
        self.last_updated_time = current_time

class UserBucketCreator:
    def __init__(self, id):
        self.bucket = {id: RateLimiter(10, 10)}

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

