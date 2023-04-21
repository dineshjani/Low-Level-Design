from enum import Enum

class RideStatus(Enum):
    IDLE = 0
    CREATED = 1
    WITHDRAWN = 2
    COMPLETED = 3


class Ride:
    AMT_PER_KM = 20

    def __init__(self):
        self.id = self.origin = self.dest = self.seats = 0
        self.ride_status = RideStatus.IDLE

    def calculate_fare(self, is_priority_rider):
        dist = self.dest - self.origin
        if self.seats < 2:
            return dist * Ride.AMT_PER_KM * (0.75 if is_priority_rider else 1)

        return dist * self.seats * Ride.AMT_PER_KM * (0.5 if is_priority_rider else 0.75)

    def set_dest(self, dest):
        self.dest = dest

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def set_origin(self, origin):
        self.origin = origin

    def get_ride_status(self):
        return self.ride_status

    def set_ride_status(self, ride_status):
        self.ride_status = ride_status

    def set_seats(self, seats):
        self.seats = seats


class Person:
    def __init__(self, name):
        self.name = name


class Driver(Person):
    def __init__(self, name):
        super().__init__(name)


class Rider(Person):
    def __init__(self, id, name):
        super().__init__(name)
        self.id = id
        self.completed_rides = []
        self.current_ride = Ride()

    def create_ride(self, id, origin, dest, seats):
        if origin >= dest:
            print("Wrong values of Origin and Destination provided. Can't create ride")
            return

        self.current_ride.set_id(id)
        self.current_ride.set_origin(origin)
        self.current_ride.set_dest(dest)
        self.current_ride.set_seats(seats)
        self.current_ride.set_ride_status(RideStatus.CREATED)

    def update_ride(self, id, origin, dest, seats):
        if self.current_ride.get_ride_status() == RideStatus.WITHDRAWN:
            print("Can't update ride. Ride was withdrawn")
            return
        if self.current_ride.get_ride_status() == RideStatus.COMPLETED:
            print("Can't update ride. Ride already complete")
            return

        self.create_ride(id, origin, dest, seats)

    def withdraw_ride(self, id):
        if self.current_ride.get_id() != id:
            print("Wrong ride Id as input. Can't withdraw current ride")
            return
        if self.current_ride.get_ride_status() != RideStatus.CREATED:
            print("Ride wasn't in progress. Can't withdraw ride")
            return

        self.current_ride.set_ride_status(RideStatus.WITHDRAWN)

    def get_id(self):
        return self.id

    def close_ride(self):
        if self.current_ride.get_ride_status() != RideStatus.CREATED:
            print("Ride wasn't in progress. Can't close ride")
            return 0

        self.current_ride.set_ride_status(RideStatus.COMPLETED)
        self.completed_rides.append(self.current_ride)
        return self.current_ride.calculate_fare(len(self.completed_rides) >= 10)


class System:
    def __init__(self, drivers, riders):
            self.drivers = drivers
            self.riders = riders

    def createRide(self, rideId, origin, dest, seats):
        if self.drivers == 0:
            print("No drivers around. Can't create ride")
            return

        for rider in self.riders:
            if rider.get_id() == rideId:
                rider.create_ride(rideId, origin, dest, seats)
                self.drivers -= 1
                break

    def updateRide(self, rideId, origin, dest, seats):
        for rider in self.riders:
            if rider.get_id() == rideId:
                rider.update_ride(rideId, origin, dest, seats)
                break

    def withdrawRide(self, rideId):
        for rider in self.riders:
            if rider.get_id() == rideId:
                rider.withdraw_ride(rideId)
                self.drivers += 1
                break

    def closeRide(self, riderId):
        for rider in self.riders:
            if rider.get_id() == riderId:
                self.drivers += 1
                return rider.close_ride()
        return 0

riders = []
rider1 = Rider(1, "Chloe")
rider2 = Rider(2, "Maze")
rider3 = Rider(3, "Maone")

riders.append(rider3)
riders.append(rider1)
riders.append(rider2)

system = System(3, riders)

rider1.create_ride(1, 50, 60, 1)
print(rider1.close_ride())
rider1.update_ride(1, 50, 60, 2)
print(rider1.close_ride())

print("*****************************************************************")

system.createRide(1, 50, 60, 1)
system.withdrawRide(1)
system.updateRide(1, 50, 60, 2)
print(system.closeRide(1))

print("*****************************************************************")

system.createRide(1, 50, 60, 1)
system.updateRide(1, 50, 60, 2)
print(system.closeRide(1))
