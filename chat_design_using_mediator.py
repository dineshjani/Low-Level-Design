from typing import List

# The Mediator interface declares a method used by components to notify the
# mediator about various events. The Mediator may react to these events and
# pass the execution to other components.
class IChatMediator:
    def send_message(self, message: str, sender: 'User') -> None:
        pass

    def add_user(self, user: 'User') -> None:
        pass

# The ConcreteMediator class coordinates interactions between components by
# sending messages between them.
class ChatMediator(IChatMediator):
    def __init__(self):
        self._users = []

    def send_message(self, message: str, sender: 'User') -> None:
        for user in self._users:
            if user != sender:
                user.receive_message(message)

    def add_user(self, user: 'User') -> None:
        self._users.append(user)

# The Colleague class declares a method used by the Mediator to send and
# receive messages.
class User:
    def __init__(self, mediator: IChatMediator):
        self._mediator = mediator

    def send_message(self, message: str) -> None:
        self._mediator.send_message(message, self)

    def receive_message(self, message: str) -> None:
        pass

# Concrete Colleagues communicate with each other indirectly via the Mediator.
class ChatUser(User):
    def __init__(self, mediator: IChatMediator, name: str):
        super().__init__(mediator)
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def receive_message(self, message: str) -> None:
        print(f"{self._name} received message: {message}")
if __name__ == '__main__':
    # The client code.
    mediator = ChatMediator()

    user1 = ChatUser(mediator, "Alice")
    user2 = ChatUser(mediator, "Bob")
    user3 = ChatUser(mediator, "Charlie")

    mediator.add_user(user1)
    mediator.add_user(user2)
    mediator.add_user(user3)

    user1.send_message("Hi, everyone!")
    user2.send_message("Hello, Alice!")
    user3.send_message("Hey, what's up?")
