from datetime import datetime
import uuid

class Ticket:
    def __init__(self, ticket_id, train_number, passenger_name, seat_number, fare, departure_date):
        self.ticket_id = ticket_id
        self.train_number = train_number
        self.passenger_name = passenger_name
        self.seat_number = seat_number
        self.fare = fare
        self.departure_date = departure_date

class Train:
    def __init__(self, train_number, train_name, capacity):
        self.train_number = train_number
        self.train_name = train_name
        self.capacity = capacity
        self.seats_available = capacity
        self.schedule = []  # List of tuples (station_code, departure_date, departure_time, arrival_time)

    def add_station_schedule(self, station_code, departure_date, departure_time, arrival_time):
        self.schedule.append((station_code, departure_date, departure_time, arrival_time))

    def book_seat(self):
        if self.seats_available > 0:
            self.seats_available -= 1
            return True
        return False

    def cancel_seat(self):
        if self.seats_available < self.capacity:
            self.seats_available += 1

class Station:
    def __init__(self, station_code, station_name):
        self.station_code = station_code
        self.station_name = station_name

class User:
    def __init__(self, name, email, phone_number):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phone_number = phone_number

class TicketBookingSystem:
    def __init__(self):
        self.trains = {}
        self.stations = {}
        self.users = []

    def add_train(self, train_number, train_name, capacity):
        self.trains[train_number] = Train(train_number, train_name, capacity)

    def add_station(self, station_code, station_name):
        self.stations[station_code] = Station(station_code, station_name)

    def add_train_schedule(self, train_number, station_code, departure_date, departure_time, arrival_time):
        train = self.trains.get(train_number)
        if not train:
            raise ValueError("Invalid train number.")
        
        train.add_station_schedule(station_code, departure_date, departure_time, arrival_time)

    def get_available_trains(self, source_station_code, destination_station_code, departure_date):
        source_station = self.stations.get(source_station_code)
        destination_station = self.stations.get(destination_station_code)
        if not source_station or not destination_station:
            raise ValueError("Invalid station codes.")

        formatted_departure_date = datetime.strptime(departure_date, "%Y-%m-%d").date()

        available_trains = []
        for train in self.trains.values():
            if (train.seats_available > 0 and
                    self.check_stations_in_route(train, source_station, destination_station, formatted_departure_date)):
                available_trains.append(train)

        return available_trains, formatted_departure_date

    def check_stations_in_route(self, train, source_station, destination_station, departure_date):
        stations_in_route = [station for station, _, _, _ in train.schedule]
        if source_station not in stations_in_route or destination_station not in stations_in_route:
            return False

        source_index = stations_in_route.index(source_station)
        destination_index = stations_in_route.index(destination_station)

        # Check if the source station is before the destination station in the route
        if source_index >= destination_index:
            return False

        # Check if the train is running on the specified departure date for each stop in the route
        for i in range(source_index, destination_index):
            _, station_departure_date, _, _ = train.schedule[i]
            if station_departure_date != departure_date:
                return False

        return True

    def reserve_ticket(self, train_number, user_id, passenger_name, seat_number, fare):
        # ... Rest of the code ...

# Example usage:
if __name__ == "__main__":
    ticket_system = TicketBookingSystem()

    # Add trains and stations
    ticket_system.add_train("12345", "Express Train", capacity=50)
    ticket_system.add_train("67890", "Fast Train", capacity=40)
    ticket_system.add_station("A", "Station A")
    ticket_system.add_station("B", "Station B")
    ticket_system.add_station("C", "Station C")
    ticket_system.add_station("X", "Station X")
    ticket_system.add_station("Y", "Station Y")

    # Add train schedule for intermediate stations
    ticket_system.add_train_schedule("12345", "A", "2023-07-30", "09:00", "09:30")
    ticket_system.add_train_schedule("12345", "X", "2023-07-30", "10:00", "10:30")
    ticket_system.add_train_schedule("12345", "Y", "2023-07-30", "11:00", "11:30")
    ticket_system.add_train_schedule("12345", "B", "2023-07-30", "12:00",
