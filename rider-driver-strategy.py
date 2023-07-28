import uuid

class GPS:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Rider:
    def __init__(self, userId, name, location):
        self.userId = userId
        self.name = name
        self.location = location

    def requestRide(self, matching_strategy, ridesharing_system):
        # Simulate a ride request
        pickup_location = GPS(self.location.latitude + 0.01, self.location.longitude - 0.01)
        destination = GPS(self.location.latitude + 0.02, self.location.longitude - 0.02)
        ride = Ride(uuid.uuid4().int, self, None, pickup_location, destination)

        # Ask the ridesharing system to find suitable drivers using the matching strategy
        drivers = ridesharing_system.findSuitableDrivers(matching_strategy)
        if drivers:
            for driver in drivers:
                driver.acceptRide(ride)
            return True
        else:
            return False

class Driver:
    def __init__(self, userId, name, location):
        self.userId = userId
        self.name = name
        self.location = location
        self.isAvailable = True

    def acceptRide(self, ride):
        if self.isAvailable:
            self.isAvailable = False
            ride.driver = self
            print(f"{self.name} accepted the ride request from {ride.rider.name}")

class Ride:
    def __init__(self, rideId, rider, driver, pickupLocation, destination):
        self.rideId = rideId
        self.rider = rider
        self.driver = driver
        self.pickupLocation = pickupLocation
        self.destination = destination

class NearestMatchingStrategy:
    def matchRide(self, rider, drivers):
        # Implement matching logic (e.g., based on distance, rating, etc.)
        # For this example, we'll simply return the first available driver.
        suitable_drivers = [driver for driver in drivers if driver.isAvailable]
        if suitable_drivers:
            return [suitable_drivers[0]]
        return None

class RidesharingSystem:
    def __init__(self):
        self.available_drivers = []

    def addDriver(self, driver):
        self.available_drivers.append(driver)

    def findSuitableDrivers(self, matching_strategy):
        return matching_strategy.matchRide(self.available_drivers)

# Example usage
if __name__ == "__main__":
    rider1 = Rider(1, "Alice", GPS(37.7749, -122.4194))
    driver1 = Driver(101, "Bob", GPS(37.7740, -122.4180))
    driver2 = Driver(102, "Charlie", GPS(37.7750, -122.4200))

    ridesharing_system = RidesharingSystem()
    ridesharing_system.addDriver(driver1)
    ridesharing_system.addDriver(driver2)

    matching_strategy = NearestMatchingStrategy()
    rider1.requestRide(matching_strategy, ridesharing_system)
