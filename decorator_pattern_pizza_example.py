from abc import ABC, abstractmethod

# Abstract Pizza class
class Pizza(ABC):
    def __init__(self):
        self.description = "Unknown Pizza"

    def get_description(self):
        return self.description

    @abstractmethod
    def get_cost(self):
        pass

# Decorator class for toppings
class ToppingsDecorator(Pizza):
    @abstractmethod
    def get_description(self):
        pass

# Concrete pizza classes
class PeppyPaneer(Pizza):
    def __init__(self):
        super().__init__()
        self.description = "PeppyPaneer"

    def get_cost(self):
        return 100

class FarmHouse(Pizza):
    def __init__(self):
        super().__init__()
        self.description = "FarmHouse"

    def get_cost(self):
        return 200

class Margherita(Pizza):
    def __init__(self):
        super().__init__()
        self.description = "Margherita"

    def get_cost(self):
        return 100

class ChickenFiesta(Pizza):
    def __init__(self):
        super().__init__()
        self.description = "ChickenFiesta"

    def get_cost(self):
        return 200

class SimplePizza(Pizza):
    def __init__(self):
        super().__init__()
        self.description = "SimplePizza"

    def get_cost(self):
        return 50

# Concrete toppings classes
class FreshTomato(ToppingsDecorator):
    def __init__(self, pizza):
        super().__init__()
        self.pizza = pizza

    def get_description(self):
        return self.pizza.get_description() + ", Fresh Tomato"

    def get_cost(self):
        return 40 + self.pizza.get_cost()

class Barbeque(ToppingsDecorator):
    def __init__(self, pizza):
        super().__init__()
        self.pizza = pizza

    def get_description(self):
        return self.pizza.get_description() + ", Barbeque"

    def get_cost(self):
        return 90 + self.pizza.get_cost()

class Paneer(ToppingsDecorator):
    def __init__(self, pizza):
        super().__init__()
        self.pizza = pizza

    def get_description(self):
        return self.pizza.get_description() + ", Paneer"

    def get_cost(self):
        return 70 + self.pizza.get_cost()

# Driver class and method
if __name__ == "__main__":
    pizza = Margherita()
    print(pizza.get_description() + " Cost: " + str(pizza.get_cost()))

    pizza2 = FarmHouse()
    pizza2 = FreshTomato(pizza2)
    pizza2 = Paneer(pizza2)
    print(pizza2.get_description() + " Cost: " + str(pizza2.get_cost()))


