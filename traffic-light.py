import time

class SignalState:
    def display(self):
        pass

    def next_state(self):
        pass

class RedState(SignalState):
    def display(self):
        print("Signal: Red")

    def next_state(self):
        return GreenState()

class YellowState(SignalState):
    def display(self):
        print("Signal: Yellow")

    def next_state(self):
        return RedState()

class GreenState(SignalState):
    def display(self):
        print("Signal: Green")

    def next_state(self):
        return YellowState()

class SignalContext:
    def __init__(self):
        self.state = RedState()

    def change_state(self):
        self.state = self.state.next_state()

    def display_signal(self):
        self.state.display()

class Timer:
    def __init__(self):
        self.start_time = 0

    def start(self):
        self.start_time = time.time()

    def elapsed_time(self):
        return time.time() - self.start_time

if __name__ == "__main__":
    signal = SignalContext()
    timer = Timer()

    while True:
        signal.display_signal()
        timer.start()

        while timer.elapsed_time() < 2:
            pass

        signal.change_state()
