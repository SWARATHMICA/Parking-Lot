'''Design a parking lot management system using object-oriented programming principles. The system should:

Model a small parking lot with:

2 levels

Each level has 2 rows

Each row has 2 parking slots

Each car occupies one parking slot'''
from datetime import datetime
import time
class Car:
    def __init__(self, license_number):
        self._license_number = license_number
        self._entry_time = None
        self._exit_time = None

    def get_license_number(self):
        return self._license_number

    def get_entry_time(self):
        return self._entry_time

    def get_exit_time(self):
        return self._exit_time

    def set_entry_time(self):
        self._entry_time = datetime.now()

    def set_exit_time(self):
        self._exit_time = datetime.now()

    def __str__(self):
        return f"Car[{self._license_number}]"

    def __repr__(self):
        return self.__str__()


class ParkingSlot:
    def __init__(self, level, row, spot):
        self._level = level
        self._row = row
        self._spot = spot
        self._occupied = False
        self._car = None

    def is_occupied(self):
        return self._occupied

    def park_car(self, car):
        self._car = car
        self._occupied = True
        car.set_entry_time()

    def remove_car(self):
        if self._car:
            self._car.set_exit_time()
            fare = ParkingFare(self._car).calculate()
            car = self._car
            self._car = None
            self._occupied = False
            return car, fare
        return None, 0

    def __str__(self):
        return f"Slot(Level {self._level}, Row {self._row}, Spot {self._spot})"

    def __repr__(self):
        return self.__str__()


class Level:
    def __init__(self, level_number, rows, spots_per_row):
        self._slots = [
            ParkingSlot(level_number, r, s)
            for r in range(rows) for s in range(spots_per_row)
        ]

    def find_free_slot(self):
        for slot in self._slots:
            if not slot.is_occupied():
                return slot
        return None

    def __str__(self):
        return f"Level with {len(self._slots)} slots"

    def __repr__(self):
        return self.__str__()


class ParkingLot:
    def __init__(self, levels):
        self._levels = levels

    def park(self, car):
        for level in self._levels:
            slot = level.find_free_slot()
            if slot:
                slot.park_car(car)
                return f"Parked {car} at {slot}"
        return "No available slots"

    def leave(self, license_number):
        for level in self._levels:
            for slot in level._slots:
                if slot.is_occupied() and slot._car.get_license_number() == license_number:
                    car, fare = slot.remove_car()
                    return f"{car} exited. Fare: ₹{fare:.2f}"
        return "Car not found"

    def __str__(self):
        return f"ParkingLot with {len(self._levels)} levels"

    def __repr__(self):
        return self.__str__()


class ParkingFare:
    def __init__(self, car):
        self._car = car

    def calculate(self):
        if self._car.get_entry_time() and self._car.get_exit_time():
            duration = (self._car.get_exit_time() - self._car.get_entry_time()).total_seconds() / 60
            return max(10, duration * 0.5)  # Base fare ₹10, ₹0.5 per minute
        return 0

# Test Case
if __name__ == "__main__":
    # Create 2 levels, each with 2 rows and 2 spots per row => total 8 spots
    level1 = Level(1, 2, 2)
    level2 = Level(2, 2, 2)
    parking_lot = ParkingLot([level1, level2])

    # Park a few cars
    car1 = Car("KA01AB1234")
    print(parking_lot.park(car1))

    car2 = Car("KA01CD5678")
    print(parking_lot.park(car2))

    # Wait to simulate time passing
    time.sleep(3)  # Sleep for 3 seconds

    # Car 1 leaves
    print(parking_lot.leave("KA01AB1234"))

    # Try to remove a car that is not parked
    print(parking_lot.leave("KA99XX9999"))
