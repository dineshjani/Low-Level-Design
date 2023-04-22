from enum import Enum

class FoodItems(Enum):
    Burger = 0
    Pizza = 1
    HotDog = 2
    Sandwich = 3
    FrenchFries = 4
    OnionRings = 5

class BeverageItems(Enum):
    Cola = 0
    Lemonade = 1
    IcedTea = 2
    Coffee = 3
    Milkshake = 4
    Smoothie = 5

class Store:
    def __init__(self, foodPrices, beveragePrices):
        self.foodPrices = {}
        self.beveragePrices = {}
        self.foodUnitsSold = {}
        self.beverageUnitsSold = {}
        self.id = self.getUniqueId()
        
        for food in foodPrices:
            self.foodPrices[food[0]] = food[1]
        
        for beverage in beveragePrices:
            self.beveragePrices[beverage[0]] = beverage[1]
    
    def getUniqueId(self):
        Store.storeId = getattr(Store, "storeId", 0) + 1
        return "store" + str(Store.storeId)
    
    def setFoodRates(self, foodPrices):
        self.foodPrices = {}
        for key,value in foodPrices.items():
            self.foodPrices[key] = value
    
    def setBeverageRates(self, beveragePrices):
        self.beveragePrices = {}
        for beverage,beverage_price in beveragePrices.items():
            self.beveragePrices[beverage] = beverage_price
    
    def getId(self):
        return self.id
    
    def purchaseFood(self, foodItem, qty):
        if foodItem.value not in self.foodUnitsSold:
            self.foodUnitsSold[foodItem.value] = 0
        self.foodUnitsSold[foodItem.value] += qty
    
    def purchaseBeverage(self, beverageItem, qty):
        if beverageItem.value not in self.beverageUnitsSold:
            self.beverageUnitsSold[beverageItem.value] = 0
        self.beverageUnitsSold[beverageItem.value] += qty
    
    def getFoodUnitsSold(self):
        return self.foodUnitsSold
    
    def getBeverageUnitsSold(self):
        return self.beverageUnitsSold
    

class City:
    def __init__(self, foodPrices, beveragePrices):
        self.foodPrices = {}
        self.beveragePrices = {}
        self.stores = []
        self.id = self.getUniqueId()
        
        for food in foodPrices:
            self.foodPrices[food[0]] = food[1]
        
        for beverage in beveragePrices:
            self.beveragePrices[beverage[0]] = beverage[1]
    
    def getUniqueId(self):
        City.cityId = getattr(City, "cityId", 0) + 1
        return "city" + str(City.cityId)
    
    def addStore(self, store):
        print(self.foodPrices)
        store.setFoodRates(self.foodPrices)
        store.setBeverageRates(self.beveragePrices)
        self.stores.append(store)
    
    def purchaseFood(self, storeId, foodItem, qty):
        for store in self.stores:
            if store.getId() == storeId:
                store.purchaseFood(foodItem, qty)
                break
    
    def purchaseBeverage(self, storeId, beverageItem, qty):
        for store in self.stores:
            if store.getId() == storeId:
                store.purchaseBeverage(beverageItem, qty)
                break
    
    def getId(self):
        return self.id
    
    def getStores(self):
        return self.stores
        
class State:
    def __init__(self):
        self.id = self.get_unique_id()
        self.cities = []

    @staticmethod
    def get_unique_id():
        state_id = 1
        while True:
            yield f"state{state_id}"
            state_id += 1

    def add_city(self, city):
        self.cities.append(city)

    def purchase_food(self, city_id, store_id, food_item, qty):
        for city in self.cities:
            if city.id == city_id:
                city.purchase_food(store_id, food_item, qty)
                break

    def purchase_beverage(self, city_id, store_id, beverage_item, qty):
        for city in self.cities:
            if city.id == city_id:
                city.purchase_beverage(store_id, beverage_item, qty)
                break

    def get_cities(self):
        return self.cities

    def get_id(self):
        return self.id

class System:
    def __init__(self):
        self.states = []

    def add_state(self, state):
        self.states.append(state)

    def purchase_food(self, state_id, city_id, store_id, food_item, qty):
        for state in self.states:
            if state.get_id() == state_id:
                state.purchase_food(city_id, store_id, food_item, qty)
                break

    def purchase_beverage(self, state_id, city_id, store_id, beverage_item, qty):
        for state in self.states:
            if state.get_id() == state_id:
                state.purchase_beverage(city_id, store_id, beverage_item, qty)
                break

    def get_states(self):
        return self.states

def main():
    foodSupply = [(i, i+1) for i in range(0, 3)]
    beverageSupply = [(i, i+1) for i in range(0, 3)]
    
    foodSupply.append((3, 4))

    store = Store(foodSupply, beverageSupply)
    city = City(foodSupply, beverageSupply)
    city.addStore(store)
    
    state = State()
    state.add_city(city)
    
    system = System()
    system.add_state(state)
    
    state1 = "state1"
    city1 = "city1"
    store1 = "store1"
    
    system.purchase_food(state1, city1, store1, FoodItems.Burger, 2)

    for state in system.get_states():
        print(system.get_states()[0].get_id())
        if state.get_id() == state1:
            for city in state.getCities():
                if city.getId() == city1:
                    for store in city.getStores():
                        if store.getId() == store1:
                            for p in store.getFoodUnitsSold():
                                print(p[0], p[1])
                            break
                    break
            break
    
    system.purchase_food(state1, city1, store1, FoodItems.Burger, 3)
main()
    