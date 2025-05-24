'''Problem statement: Design a Parking lot management application for a building with multiple floors having 
parking slots which could accommodate different vehicles such as bikes, cars, buses. 
An available slot should be given to the entered vehicle,
after exiting the vehicle the slot has to be made available and parking fares have to be charged based on time.'''
import datetime

class Vehicle:
    def __init__(self, vehicle_id, vehicle_type):
        self._vehicle_id = vehicle_id
        self._vehicle_type = vehicle_type
        self._entry_time = None
        self._exit_time = None

    def get_vehicle_type(self):
        return self._vehicle_type

    def get_vehicle_id(self):
        return self._vehicle_id

    def set_entry_time(self):
        self._entry_time = datetime.datetime.now()

    def set_exit_time(self):
        self._exit_time = datetime.datetime.now()

    def get_entry_time(self):
        return self._entry_time

    def get_exit_time(self):
        return self._exit_time

    def __str__(self):
        return f"Vehicle({self._vehicle_id}, {self._vehicle_type})"

    def __repr__(self):
        return self.__str__()
class Slot:
    def __init__(self, slot_id, vehicle_type):
        self._slot_id = slot_id
        self._vehicle_type = vehicle_type
        self._occupied = False
        self._current_vehicle = None

    def is_available(self):
        return not self._occupied

    def assign_vehicle(self, vehicle):
        self._occupied = True
        self._current_vehicle = vehicle

    def free_slot(self):
        self._occupied = False
        self._current_vehicle = None

    def get_vehicle_type(self):
        return self._vehicle_type

    def get_slot_id(self):
        return self._slot_id

    def get_current_vehicle(self):
        return self._current_vehicle

    def __str__(self):
        status = "Occupied" if self._occupied else "Available"
        return f"Slot({self._slot_id}, Type={self._vehicle_type}, Status={status})"

    def __repr__(self):
        return self.__str__()
class Floor:
    def __init__(self, floor_number):
        self._floor_number = floor_number
        self._slots = []

    def add_slot(self, slot):
        self._slots.append(slot)

    def get_available_slot(self, vehicle_type):
        for slot in self._slots:
            if slot.get_vehicle_type() == vehicle_type and slot.is_available():
                return slot
        return None

    def get_floor_number(self):
        return self._floor_number

    def __str__(self):
        return f"Floor({self._floor_number}) with {len(self._slots)} slots"

    def __repr__(self):
        return self.__str__()
class ParkingFare:
    _RATES = {'bike': 10, 'car': 20, 'bus': 30}  # Per hour

    def __init__(self, vehicle):
        self._vehicle = vehicle

    def calculate(self):
        entry = self._vehicle.get_entry_time()
        exit_ = self._vehicle.get_exit_time()
        duration_hours = max(1, (exit_ - entry).total_seconds() // 3600)
        rate = self._RATES.get(self._vehicle.get_vehicle_type(), 0)
        return int(duration_hours * rate)
class ParkingLot:
    def __init__(self, lot_id):
        self._lot_id = lot_id
        self._floors = []
        self._vehicle_slot_map = {}

    def add_floor(self, floor):
        self._floors.append(floor)

    def allocate_slot(self, vehicle):
        for floor in self._floors:
            slot = floor.get_available_slot(vehicle.get_vehicle_type())
            if slot:
                slot.assign_vehicle(vehicle)
                vehicle.set_entry_time()
                self._vehicle_slot_map[vehicle.get_vehicle_id()] = slot
                return f"Allocated {slot.get_slot_id()} on Floor {floor.get_floor_number()}"
        return "No available slot"

    def free_slot(self, vehicle_id):
        slot = self._vehicle_slot_map.get(vehicle_id)
        if not slot:
            return "Vehicle not found"

        vehicle = slot.get_current_vehicle()
        vehicle.set_exit_time()
        fare = ParkingFare(vehicle).calculate()
        slot.free_slot()
        del self._vehicle_slot_map[vehicle_id]
        return f"Freed Slot {slot.get_slot_id()}. Fare: ₹{fare}"

    def __str__(self):
        return f"ParkingLot({self._lot_id})"

    def __repr__(self):
        return self.__str__()
#test cases
import time

# Setup
lot = ParkingLot(lot_id=101)
floor = Floor(floor_number=0)
for i in range(2):
    floor.add_slot(Slot(f"B{i+1}", "bike"))
    floor.add_slot(Slot(f"C{i+1}", "car"))
floor.add_slot(Slot("BS1", "bus"))
lot.add_floor(floor)

# Vehicles
v1 = Vehicle("V001", "bike")
v2 = Vehicle("V002", "car")
v3 = Vehicle("V003", "bus")
v4 = Vehicle("V004", "bike")
v5 = Vehicle("V005", "bike")  # Should fail

# Allocation
print(lot.allocate_slot(v1))
print(lot.allocate_slot(v2))
print(lot.allocate_slot(v3))
print(lot.allocate_slot(v4))
print(lot.allocate_slot(v5))

# Simulate duration
time.sleep(2)

# Freeing slots
print(lot.free_slot("V001"))
print(lot.free_slot("V002"))
print(lot.free_slot("V003"))
