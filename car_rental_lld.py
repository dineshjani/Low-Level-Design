from typing import List

import math
import uuid


class VehicleType:
    SUV = "SUV"
    SEDAN = "SEDAN"
    BIKE = "BIKE"


class Vehicle:
    def __init__(
        self,
        numberPlate: str,
        color: str,
        capacity: int,
        price: int,
        type: VehicleType,
        latitude: float,
        longitude: float
    ):
        self.numberPlate = numberPlate
        self.color = color
        self.capacity = capacity
        self.price = price
        self.type = type
        self.latitude = latitude
        self.longitude = longitude


class Station:
    def __init__(
        self,
        id: str,
        active: bool,
        latitude: float,
        longitude: float,
        vehicles: List[Vehicle]
    ):
        self.id = id
        self.active = active
        self.latitude = latitude
        self.longitude = longitude
        self.vehicles = vehicles


class Booking:
    def __init__(
        self,
        id: str,
        date: str,
        startTime: str,
        endTime: str,
        pickUpStationId: str,
        dropStationId: str,
        userId: str,
        invoiceAmt: int,
        vehicleId: str,
        status: bool
    ):
        self.id = id
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.pickUpStationId = pickUpStationId
        self.dropStationId = dropStationId
        self.userId = userId
        self.invoiceAmt = invoiceAmt
        self.vehicleId = vehicleId
        self.status = status


class User:
    def __init__(self, id: str, name: str, licenseNumber: str):
        self.id = id
        self.name = name
        self.licenseNumber = licenseNumber


def generate_id():
    return str(uuid.uuid4())


def generate_invoice(charge_per_hour: int, start_time: str, end_time: str) -> int:
    return max(
        math.floor(((end_time - start_time) / 60 / 60) * charge_per_hour),
        charge_per_hour
    )


def to_rad(value: float) -> float:
    return (value * math.pi) / 180


def distance_between(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371  # km
    dLat = to_rad(lat2 - lat1)
    dLon = to_rad(lon2 - lon1)
    lat1 = to_rad(lat1)
    lat2 = to_rad(lat2)

    a = (
        math.sin(dLat / 2) ** 2
        + math.sin(dLon / 2) ** 2 * math.cos(lat1) * math.cos(lat2)
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


import math
import uuid

class StationRepository:
    def __init__(self):
        self.Stations = []

    async def addStation(self, newStation):
        try:
            conflictingStations = len(list(filter(lambda station: station["latitude"] == newStation["latitude"] and station["longitude"] == newStation["longitude"], self.Stations)))
            if conflictingStations == 0:
                stationEntity = dict(newStation, id=str(uuid.uuid4()))
                self.Stations.append(stationEntity)
                return stationEntity
            else:
                raise Exception("Station already exists")
        except Exception as err:
            raise Exception(err)

    async def disableStation(self, stationId):
        try:
            self.Stations = list(map(lambda station: dict(station, active=False) if station["id"] == stationId else station, self.Stations))
        except Exception as err:
            raise Exception(err)

    async def getStations(self, latitude, longitude):
        try:
            def distanceBetween(lat1, lon1, lat2, lon2):
                R = 6371  # km
                dLat = toRad(lat2 - lat1)
                dLon = toRad(lon2 - lon1)
                lat1 = toRad(lat1)
                lat2 = toRad(lat2)

                a = (
                    math.sin(dLat / 2) * math.sin(dLat / 2) +
                    math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(lat2)
                )
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                d = R * c
                return d

            sortedStations = sorted(self.Stations, key=lambda station: distanceBetween(latitude, longitude, station["latitude"], station["longitude"]))
            return sortedStations
        except Exception as err:
            raise err

    async def addVehicle(self, vehicle, stationId):
        try:
            StationIdx = next((i for i, station in enumerate(self.Stations) if station["id"] == stationId), -1)
            if StationIdx >= 0:
                self.Stations[StationIdx]["vehicles"].append(vehicle)
        except Exception as err:
            raise err

    async def removeVehicle(self, vehicle, stationId):
        try:
            StationIdx = next((i for i, station in enumerate(self.Stations) if station["id"] == stationId), -1)
            if StationIdx >= 0:
                self.Stations[StationIdx]["vehicles"] = list(filter(lambda v: v["numberPlate"] != vehicle["numberPlate"], self.Stations[StationIdx]["vehicles"]))
        except Exception as err:
            raise err

    async def getStation(self, stationId):
        try:
            station = next((station for station in self.Stations if station["id"] == stationId and station["active"]), None)
            if station:
                return station
            else:
                raise Exception("No station registered")
        except Exception as err:
            raise err


from typing import List

class Booking:
    def __init__(
        self,
        id: str,
        date: str,
        startTime: str,
        endTime: str,
        pickUpStationId: str,
        userId: str,
        vehicleId: str,
        invoiceAmt: float,
        status: bool,
        dropStationId: str = None,
    ):
        self.id = id
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.pickUpStationId = pickUpStationId
        self.userId = userId
        self.vehicleId = vehicleId
        self.invoiceAmt = invoiceAmt
        self.status = status
        self.dropStationId = dropStationId

class BookingRepository:
    def __init__(self):
        self.bookings = []

    async def get_booking(self, booking_id):
        try:
            booking = next((booking for booking in self.bookings if booking['id'] == booking_id), None)
            if booking:
                return booking
            raise Exception('No booking found')
        except Exception as e:
            raise e

    async def create_booking(self, vehicle_id, station_id, start_time, date, end_time, user_id, vehicle_charge_per_hour):
        try:
            new_booking = {
                'id': generate_id(),
                'date': date,
                'startTime': start_time,
                'endTime': end_time,
                'pickUpStationId': station_id,
                'userId': user_id,
                'vehicleId': vehicle_id,
                'invoiceAmt': generate_invoice(vehicle_charge_per_hour, end_time, start_time),
                'status': True
            }
            self.bookings.append(new_booking)
            return new_booking
        except Exception as e:
            raise e

    async def end_booking(self, booking_id, station_id):
        try:
            booking_idx = next((i for i, booking in enumerate(self.bookings) if booking['id'] == booking_id), None)
            if booking_idx is not None:
                self.bookings[booking_idx] = {
                    **self.bookings[booking_idx],
                    'status': False,
                    'dropStationId': station_id
                }
        except Exception as e:
            raise e

class BookingService:
    def __init__(self, booking_repository):
        self.booking_repository = booking_repository

    async def create_booking(self, vehicle_id, station_id, start_time, date, end_time, user_id, vehicle_charge_per_hour):
        try:
            return await self.booking_repository.create_booking(vehicle_id, station_id, start_time, date, end_time, user_id, vehicle_charge_per_hour)
        except Exception as e:
            raise e

    async def end_booking(self, booking_id, station_id):
        try:
            await self.booking_repository.end_booking(booking_id, station_id)
        except Exception as e:
            raise e

    async def get_booking(self, booking_id):
        try:
            return await self.booking_repository.get_booking(booking_id)
        except Exception as e:
            raise e



class VehicleRepository:
    def __init__(self):
        self.Vehicles: List[Vehicle] = []

    async def addVehicle(self, vehicle: Vehicle) -> Vehicle:
        try:
            conflictingVehicles: int = len([currVehicle for currVehicle in self.Vehicles if currVehicle.numberPlate == vehicle.numberPlate])
            if conflictingVehicles == 0:
                self.Vehicles.append(vehicle)
                return vehicle
            else:
                raise Exception("Vehicle already registered")
        except Exception as err:
            raise err

    async def getVehicle(self, vehicleId: str) -> Vehicle:
        try:
            vehicle: Vehicle = next((vehicle for vehicle in self.Vehicles if vehicle.numberPlate == vehicleId), None)
            if vehicle:
                return vehicle
            else:
                raise Exception("No Vehicle found")
        except Exception as err:
            raise err

    async def removeVehicle(self, vehicleId: str):
        try:
            self.Vehicles = [vehicle for vehicle in self.Vehicles if vehicle.numberPlate != vehicleId]
        except Exception as err:
            raise err

    async def filterVehicles(self, vehicleType: VehicleType) -> List[Vehicle]:
        try:
            return [vehicle for vehicle in self.Vehicles if vehicle.type == vehicleType]
        except Exception as err:
            raise err
            
class VehicleService:
    def __init__(self, vehicle_repository):
        self.vehicle_repository = vehicle_repository

    async def getVehicle(self, vehicleNumberPlate):
        try:
            return await self.vehicle_repository.getVehicle(vehicleNumberPlate)
        except Exception as e:
            raise e

    async def addVehicle(self, vehicle):
        try:
            await self.vehicle_repository.addVehicle(vehicle)
        except Exception as e:
            raise e

    async def removeVehicle(self, vehicleId):
        try:
            await self.vehicle_repository.removeVehicle(vehicleId)
        except Exception as e:
            raise e

    async def filterVehicles(self, vehicleType):
        try:
            return await self.vehicle_repository.filterVehicles(vehicleType)
        except Exception as e:
            raise e
            
class StationService:
    def __init__(self, station_repository):
        self.station_repository = station_repository

    async def onBoardStation(self, newStation):
        try:
            return await self.station_repository.addStation(newStation)
        except Exception as err:
            raise err

    async def addVehicle(self, vehicle, stationId):
        try:
            await self.station_repository.addVehicle(vehicle, stationId)
        except Exception as err:
            raise err

    async def removeVehicle(self, vehicle, stationId):
        try:
            await self.station_repository.removeVehicle(vehicle, stationId)
        except Exception as err:
            raise err

    async def unBoardStation(self, stationId):
        try:
            await self.station_repository.disableStation(stationId)
        except Exception as err:
            raise err

    async def filterBasedOnLocation(self, userLatitude, userLongitude):
        try:
            return await self.station_repository.getStations(userLatitude, userLongitude)
        except Exception as err:
            raise err

    async def getStation(self, stationId):
        try:
            return await self.station_repository.getStation(stationId)
        except Exception as err:
            raise err
from typing import List
from datetime import datetime

from .booking import Booking, BookingService
from .station import Station, StationService
from .vehicle import Vehicle, VehicleService, VehicleType


class CarRentalService:
    def __init__(
        self,
        station_service: StationService,
        booking_service: BookingService,
        vehicle_service: VehicleService,
    ):
        self.station_service = station_service
        self.booking_service = booking_service
        self.vehicle_service = vehicle_service

    async def add_station(self, new_station: dict) -> Station:
        try:
            station = await self.station_service.on_board_station(new_station)
            for vehicle in new_station["vehicles"]:
                await self.vehicle_service.add_vehicle(vehicle)
            return station
        except Exception as e:
            raise e

    async def remove_station(self, station_id: str):
        try:
            station = await self.station_service.get_station(station_id)
            for vehicle in station.vehicles:
                await self.vehicle_service.remove_vehicle(vehicle.number_plate)
            await self.station_service.un_board_station(station_id)
        except Exception as e:
            raise e

    async def book_vehicle(
        self,
        vehicle_id: str,
        station_id: str,
        start_time: datetime,
        end_time: datetime,
        date: datetime,
        user_id: str,
    ) -> Booking:
        try:
            station = await self.station_service.get_station(station_id)
            stationed_vehicle = next(
                (
                    vehicle
                    for vehicle in station.vehicles
                    if vehicle.number_plate == vehicle_id
                ),
                None,
            )
            if stationed_vehicle is None:
                raise ValueError("Requested vehicleId and stationId are incorrect")
            price = stationed_vehicle.price
            booking = await self.booking_service.create_booking(
                vehicle_id,
                station_id,
                start_time,
                end_time,
                date,
                user_id,
                price,
            )
            await self.station_service.remove_vehicle(stationed_vehicle, station_id)
            return booking
        except Exception as e:
            raise e

    async def end_booking(self, booking_id: str, station_id: str):
        try:
            booking = await self.booking_service.get_booking(booking_id)
            vehicle = await self.vehicle_service.get_vehicle(booking.vehicle_id)
            await self.booking_service.end_booking(booking_id, station_id)
            await self.station_service.add_vehicle(vehicle, station_id)
        except Exception as e:
            raise e

    async def search_vehicle(
        self, vehicle_type: VehicleType, user_latitude: float, user_longitude: float
    ) -> List[Station]:
        try:
            stations_based_on_location = await self.station_service.filter_based_on_location(
                user_latitude, user_longitude
            )
            vehicles = await self.vehicle_service.filter_vehicles(vehicle_type)
            if len(vehicles) > 0:
                vehicles = sorted(
                    vehicles,
                    key=lambda vehicle: (
                        vehicle.price,
                        distance_between(
                            user_latitude, user_longitude, vehicle.latitude, vehicle.longitude
                        ),
                    ),
                )
            else:
                raise ValueError("No vehicles found of this type")
            return stations_based_on_location
        except Exception as e:
            raise e


def distance_between(lat1, lon1, lat2, lon2):
    # formula to calculate distance between two coordinates
    return ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5



