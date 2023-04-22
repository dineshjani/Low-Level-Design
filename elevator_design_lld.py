from enum import Enum
import heapq
from time import sleep
import time


class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0


class Location(Enum):
    INSIDE = 1
    OUTSIDE = 0


class Request:
    def __init__(self, current_floor, desired_floor, location, direction):
        self.current_floor = current_floor
        self.desired_floor = desired_floor
        self.location = location
        self.direction = direction
        
    def __lt__(self, other):
        return self.desired_floor < other.desired_floor


class Elevator:
    def __init__(self, current_floor):
        self.current_floor = current_floor
        self.direction = Direction.IDLE
        self.upQ = []
        self.downQ = []
        
    def add_up_request(self, up_request:Request):
        if up_request.location == Location.OUTSIDE:
            heapq.heappush(self.upQ,(up_request.current_floor, Request(up_request.current_floor, up_request.current_floor, Location.OUTSIDE, Direction.UP)))
            print(f"Added up request going to floor {up_request.current_floor}.")
        heapq.heappush(self.upQ,(up_request.desired_floor,up_request))
        print(f"Added up request going to floor {up_request.desired_floor}.")

    def add_down_request(self, down_request):
        if down_request.location == Location.OUTSIDE:
            heapq.heappush(self.downQ,(-down_request.current_floor, Request(down_request.current_floor, down_request.current_floor, Location.OUTSIDE, Direction.DOWN)))
            print(f"Added down request going to floor {down_request.current_floor}.")
        print(f"Added down request going to floor {down_request.desired_floor}.")
        heapq.heappush(self.downQ,(-down_request.desired_floor,down_request))


    def process_requests(self):
        if self.direction == Direction.UP or self.direction == Direction.IDLE:
            self.process_up_request()
            self.process_down_request()
        else:
            self.process_down_request()
            self.process_up_request()

    def process_up_request(self):
        while len(self.upQ) > 0:
            up_request = self.upQ.pop(0)
            self.current_floor = up_request[1].desired_floor
            print(f"Up -> Elevator stopped at floor {self.current_floor}.")
        if not len(self.downQ):
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE

    def process_down_request(self):
        while len(self.downQ) > 0:
            down_request = self.downQ.pop(0)
            self.current_floor = down_request[1].desired_floor
            print(f"Down -> Elevator stopped at floor {self.current_floor}.")
        if not len(self.upQ):
            self.direction = Direction.UP
        else:
            self.direction = Direction.IDLE

    def run(self):
        while len(self.downQ) > 0 or len(self.upQ) > 0:
            self.process_requests()
        print("Finished all requests.")
        self.direction = Direction.IDLE


class RequestProcessor:
    def __init__(self, elevator):
        self.elevator = elevator
        self.stop = False

    def set_stop(self, stop):
        self.stop = stop

    def run(self):
        up_request1 = Request(self.elevator.current_floor, 5, Location.INSIDE, Direction.UP)
        up_request2 = Request(self.elevator.current_floor, 3, Location.INSIDE, Direction.UP)

        down_request1 = Request(self.elevator.current_floor, 1, Location.INSIDE, Direction.DOWN)
        down_request2 = Request(self.elevator.current_floor, 2, Location.INSIDE, Direction.DOWN)
        down_request3 = Request(4, 0, Location.OUTSIDE, Direction.DOWN)

        self.elevator.add_up_request(up_request1)
        self.elevator.add_up_request(up_request2)
        self.elevator.add_down_request(down_request3)
        self.elevator.add_down_request(down_request1)
        self.elevator.add_down_request(down_request2)

if __name__ == "__main__":
    elevator = Elevator(0)
    requestProcessor = RequestProcessor(elevator)
    requestProcessor.run()
    elevator.run()
    # request->requestprocessor->elevator
            
            
