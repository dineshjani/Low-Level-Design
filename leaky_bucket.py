import threading
from queue import Queue

class RateLimiter:
    def __init__(self, capacity):
        self.queue = Queue(capacity)
        self.lock = threading.Lock()

    def grant_access(self):
        with self.lock:
            if not self.queue.full():
                self.queue.put(1)
                return True
            return False

class UserBucketCreator:
    def __init__(self, id):
        self.bucket = {id: RateLimiter(10)}

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

