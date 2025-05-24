class Vehicle:
    def __init__(self, vehicle_id, vehicle_type):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type  # 'bike', 'car', or 'bus'
        self.entry_time = None
        self.exit_time = None
class Slot:
    def __init__(self, slot_id, vehicle_type):
        self.slot_id = slot_id
        self.vehicle_type = vehicle_type  # type of vehicle this slot supports
        self.occupied = False
        self.current_vehicle = None
class Floor:
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.slots = []  # List of Slot objects

    def add_slot(self, slot: Slot):
        self.slots.append(slot)
import datetime

class ParkingLot:
    def __init__(self, parkinglot_id):
        self.parkinglot_id = parkinglot_id
        self.floors = []  # List of Floor objects
        self.vehicle_slot_map = {}  # vehicle_id -> Slot

    def add_floor(self, floor: Floor):
        self.floors.append(floor)

    def allocate_slot(self, vehicle: Vehicle):
        for floor in self.floors:
            for slot in floor.slots:
                if not slot.occupied and slot.vehicle_type == vehicle.vehicle_type:
                    slot.occupied = True
                    slot.current_vehicle = vehicle
                    vehicle.entry_time = datetime.datetime.now()
                    self.vehicle_slot_map[vehicle.vehicle_id] = slot
                    return f"Slot {slot.slot_id} allocated on Floor {floor.floor_number}"
        return "No slot available"

    def free_slot(self, vehicle_id):
        if vehicle_id not in self.vehicle_slot_map:
            return "Vehicle not found"

        slot = self.vehicle_slot_map[vehicle_id]
        vehicle = slot.current_vehicle
        vehicle.exit_time = datetime.datetime.now()
        fare = ParkingFare(vehicle).cal()

        # Free the slot
        slot.occupied = False
        slot.current_vehicle = None
        del self.vehicle_slot_map[vehicle_id]

        return f"Slot {slot.slot_id} freed. Fare: ₹{fare}"
class ParkingFare:
    RATES = {'bike': 10, 'car': 20, 'bus': 30}  # ₹ per hour

    def __init__(self, vehicle: Vehicle):
        self.vehicle = vehicle

    def cal(self):
        duration = self.vehicle.exit_time - self.vehicle.entry_time
        hours = max(1, duration.total_seconds() // 3600)
        return int(hours * self.RATES[self.vehicle.vehicle_type])

#test case
import time

# Create slots
bike_slots = [Slot(slot_id=f"B{i+1}", vehicle_type='bike') for i in range(2)]
car_slots = [Slot(slot_id=f"C{i+1}", vehicle_type='car') for i in range(2)]
bus_slots = [Slot(slot_id=f"BS1", vehicle_type='bus')]

# Create floor and add slots
floor_0 = Floor(floor_number=0)
for slot in bike_slots + car_slots + bus_slots:
    floor_0.add_slot(slot)

# Create parking lot and add floor
parking_lot = ParkingLot(parkinglot_id=1)
parking_lot.add_floor(floor_0)

# Create vehicles
v1 = Vehicle(vehicle_id="V001", vehicle_type="bike")
v2 = Vehicle(vehicle_id="V002", vehicle_type="car")
v3 = Vehicle(vehicle_id="V003", vehicle_type="bus")
v4 = Vehicle(vehicle_id="V004", vehicle_type="bike")  # extra bike
v5 = Vehicle(vehicle_id="V005", vehicle_type="bike")  # no slot should be available

# Allocate slots
print(parking_lot.allocate_slot(v1))  # Should allocate bike slot
print(parking_lot.allocate_slot(v2))  # Should allocate car slot
print(parking_lot.allocate_slot(v3))  # Should allocate bus slot
print(parking_lot.allocate_slot(v4))  # Should allocate second bike slot
print(parking_lot.allocate_slot(v5))  # Should return "No slot available"

# Simulate parking time
time.sleep(2)

# Free slots and show fare
print(parking_lot.free_slot("V001"))
print(parking_lot.free_slot("V002"))
print(parking_lot.free_slot("V003"))
