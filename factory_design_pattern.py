from abc import ABC, abstractmethod
from enum import Enum

class IMobile(ABC):
    @abstractmethod
    def operation(self):
        pass

class Samsung(IMobile):
    def operation(self):
        print("Samsung Mobile")

class Apple(IMobile):
    def operation(self):
        print("Apple Mobile")

class IMobileFactory(ABC):
    @abstractmethod
    def create_mobile(self):
        pass

class SamsungFactory(IMobileFactory):
    def create_mobile(self):
        return Samsung()

class AppleFactory(IMobileFactory):
    def create_mobile(self):
        return Apple()

class MobileType(Enum):
    Samsung = 1
    Apple = 2

class MobileExecutioner:
    def __init__(self):
        self._factories = {}

        for mobile_type in MobileType:
            factory = self.get_factory(mobile_type)
            self._factories[mobile_type] = factory

    def get_factory(self, mobile_type):
        if mobile_type == MobileType.Samsung:
            return SamsungFactory()
        elif mobile_type == MobileType.Apple:
            return AppleFactory()
        else:
            raise ValueError("Invalid mobile type")

    def get_mobile_factory(self, mobile_type):
        return self._factories[mobile_type]

if __name__ == "__main__":
    type = input("Enter mobile type (Samsung or Apple): ")
    mobile_type = MobileType[type]

    executioner = MobileExecutioner()
    factory = executioner.get_mobile_factory(mobile_type)
    mobile = factory.create_mobile()
    mobile.operation()
