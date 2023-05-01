from typing import List

class IObserver:
    def update(self, message: str):
        pass

class Subject:
    def __init__(self):
        self.observers: List[IObserver] = []

    def attach(self, observer: IObserver):
        self.observers.append(observer)

    def detach(self, observer: IObserver):
        self.observers.remove(observer)

    def notify(self, message: str):
        for observer in self.observers:
            observer.update(message)

class Observer(IObserver):
    def __init__(self, name: str):
        self.name = name

    def update(self, message: str):
        print(f"{self.name} received message: {message}")

subject = Subject()
observer1 = Observer("Observer 1")
observer2 = Observer("Observer 2")

subject.attach(observer1)
subject.attach(observer2)

subject.notify("The game has been rescheduled for 2pm.")
