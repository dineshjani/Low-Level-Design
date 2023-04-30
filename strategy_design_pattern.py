from abc import ABC, abstractmethod

class IDiscountStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, price):
        pass

class RegularDiscountStrategy(IDiscountStrategy):
    def calculate_discount(self, price):
        return price * 0.9 # 10% discount
        

class PremiumDiscountStrategy(IDiscountStrategy):
    def calculate_discount(self, price):
        return price * 0.8 # 20% discount

class VIPDiscountStrategy(IDiscountStrategy):
    def calculate_discount(self, price):
        return price * 0.5 # 50% discount

class ShoppingCart:
    def __init__(self, discount_strategy: IDiscountStrategy):
        self._discount_strategy = discount_strategy
        self._items = []
        
    def add_item(self, price):
        self._items.append(price)

    def calculate_total(self):
        total = sum(self._items)
        return self._discount_strategy.calculate_discount(total)
    
    def set_discount_strategy(self, new_strategy: IDiscountStrategy):
        self._discount_strategy = new_strategy


strategy = PremiumDiscountStrategy()
cart = ShoppingCart(strategy)
cart.add_item(100)
cart.add_item(50)
total = cart.calculate_total()
print(total)

# https://justgokus.medium.com/what-is-the-strategy-design-pattern-ade12ccac543
