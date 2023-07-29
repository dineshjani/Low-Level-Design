Certainly! Here's the complete code in Python for the Toll Service:

```python
from enum import Enum
from datetime import datetime, timedelta

class PassType(Enum):
    ONE_WAY = 1
    ROUND_TRIP = 2
    DAILY = 3
    WEEKLY = 4
    MANDATORY = 5

class Pass:
    pass_id_counter = 0

    def __init__(self, pass_type, valid_from, valid_until):
        Pass.pass_id_counter += 1
        self.pass_id = Pass.pass_id_counter
        self.pass_type = pass_type
        self.valid_from = valid_from
        self.valid_until = valid_until

class TollBooth:
    def __init__(self, booth_id, is_mandatory):
        self.booth_id = booth_id
        self.is_mandatory = is_mandatory

    def validate_pass(self, vehicle):
        if self.is_mandatory:
            return True
        pass_obj = vehicle.get_pass()
        if pass_obj and pass_obj.valid_until >= datetime.now():
            return True
        return False

class TollPlaza:
    def __init__(self, plaza_id):
        self.plaza_id = plaza_id
        self.toll_booths = []

    def add_toll_booth(self, toll_booth):
        self.toll_booths.append(toll_booth)

class Vehicle:
    def __init__(self, vehicle_type):
        self.vehicle_type = vehicle_type
        self.pass_obj = None

    def set_pass(self, pass_obj):
        self.pass_obj = pass_obj

    def get_pass(self):
        return self.pass_obj

class TollService:
    def __init__(self):
        self.toll_plazas = []
        self.vehicles = []
        self.daily_collections = {}

    def issue_pass(self, pass_type, valid_from, valid_until, vehicle_type):
        pass_obj = Pass(pass_type, valid_from, valid_until)
        vehicle = self.find_vehicle_by_type(vehicle_type)
        if vehicle:
            vehicle.set_pass(pass_obj)
        else:
            vehicle = Vehicle(vehicle_type)
            vehicle.set_pass(pass_obj)
            self.vehicles.append(vehicle)

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def process_toll(self, toll_plaza, booth_id, vehicle):
        toll_booth = self.find_toll_booth_by_id(toll_plaza, booth_id)
        if toll_booth and toll_booth.validate_pass(vehicle):
            # Vehicle has a valid pass
            # Collect toll or perform other operations
            toll_amount = self.calculate_toll_amount(vehicle)
            self.add_to_daily_collection(toll_plaza, toll_amount)
            print("Toll collected successfully")
        else:
            # Vehicle does not have a valid pass
            # Handle invalid pass scenario
            print("Invalid pass or pass not found")

    def calculate_toll_amount(self, vehicle):
        # Example logic to calculate toll amount based on vehicle type, pass type, etc.
        base_toll_amount = 50
        pass_obj = vehicle.get_pass()
        if pass_obj:
            # Apply discounts for pass types (e.g., Daily pass gets 20% discount)
            if pass_obj.pass_type == PassType.DAILY:
                return int(base_toll_amount * 0.8)
            elif pass_obj.pass_type == PassType.WEEKLY:
                return int(base_toll_amount * 0.6)
        return base_toll_amount

    def find_toll_booth_by_id(self, toll_plaza, booth_id):
        for toll_booth in toll_plaza.toll_booths:
            if toll_booth.booth_id == booth_id:
                return toll_booth
        return None

    def find_vehicle_by_type(self, vehicle_type):
        for vehicle in self.vehicles:
            if vehicle.vehicle_type == vehicle_type:
                return vehicle
        return None

    def add_to_daily_collection(self, toll_plaza, amount):
        date_today = datetime.now().date()
        daily_collection_map = self.daily_collections.get(toll_plaza, {})
        daily_collection_map[date_today] = daily_collection_map.get(date_today, 0) + amount
        self.daily_collections[toll_plaza] = daily_collection_map

    def get_total_collection(self):
        total_collection = 0
        for toll_plaza in self.toll_plazas:
            daily_collection_map = self.daily_collections.get(toll_plaza, {})
            for amount in daily_collection_map.values():
                total_collection += amount
        return total_collection

    def get_total_collection_for_toll_plaza(self, toll_plaza):
        total_collection = 0
        daily_collection_map = self.daily_collections.get(toll_plaza, {})
        for amount in daily_collection_map.values():
            total_collection += amount
        return total_collection

if __name__ == "__main__":
    toll_service = TollService()

    # Creating TollPlazas with TollBooths
    plaza1 = TollPlaza(1)
    booth1 = TollBooth(1, False)
    booth2 = TollBooth(2, False)
    plaza1.add_toll_booth(booth1)
    plaza1.add_toll_booth(booth2)
    toll_service.toll_plazas.append(plaza1)

    plaza2 = TollPlaza(2)
    booth3 = TollBooth(1, True)  # Mandatory TollBooth
    plaza2.add_toll_booth(booth3)
    toll_service.toll_plazas.append(plaza2)

    # Issuing Passes to Vehicles
    toll_service.issue_pass(PassType.DAILY, datetime.now(), datetime.now() + timedelta(days=1), "Car")
    toll_service.issue_pass(PassType.WEEKLY, datetime.now(), datetime.now() + timedelta(days=7), "Truck")

    # Processing Tolls
    vehicle1 = Vehicle("Car")
    vehicle2 = Vehicle("Truck")
    toll_service.add_vehicle(vehicle1)
    toll_service.add_vehicle(vehicle2)

    toll_service.process_toll(plaza1, 1, vehicle1)
    toll_service.process_toll(plaza1, 2, vehicle2)
    toll_service.process_toll(plaza2, 1, vehicle1)

    # Print total collections
    print("Total collection for all toll plazas:", toll_service.get_total_collection())
    print("Total collection for TollPlaza 1:", toll_service.get_total_collection_for_toll_plaza(plaza1))
    print("Total collection for TollPlaza 2:", toll_service.get_total_collection_for_toll_plaza(plaza2))
