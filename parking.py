from datetime import datetime
from math import ceil
import json

from vehicle import Vehicle


def load_data():
    with open("parking_data.json", "r") as file:
        data = json.load(file)

    return data


def save_data(data):
    with open("parking_data.json", "w") as file:
        json.dump(data, file, indent=4)


def load_history():
    with open("parking_history.json", "r") as file:
        data = json.load(file)

    return data


def save_history(data):
    with open("parking_history.json", "w") as file:
        json.dump(data, file, indent=4)


def format_duration(duration):
    total_seconds = int(duration.total_seconds())

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts = []

    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")

    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")

    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")

    if seconds > 0:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return " ".join(parts)


class ParkingSlot:

    def __init__(self, slot_number):
        self.slot_number = slot_number
        self.is_occupied = False


class ParkingLot:

    def __init__(self):
        self.slots = []
        self.parked_vehicles = []

        data = load_data()

        for record in data:
            vehicle = Vehicle(
                record["vehicle_number"],
                record["vehicle_type"]
            )

            vehicle.slot = record["slot"]
            vehicle.entry_time = datetime.fromisoformat(
                record["entry_time"]
            )

            self.parked_vehicles.append(vehicle)

    def add_slot(self, slot):
        self.slots.append(slot)

        for vehicle in self.parked_vehicles:
            if vehicle.slot == slot.slot_number:
                slot.is_occupied = True

    def find_available_slot(self):
        for slot in self.slots:
            if not slot.is_occupied:
                return slot

        return None

    def park_vehicle(self, vehicle):

        if self.find_vehicle(vehicle.vehicle_number) is not None:
            return None

        available_slot = self.find_available_slot()

        if available_slot is None:
            return None

        available_slot.is_occupied = True
        vehicle.slot = available_slot.slot_number

        self.parked_vehicles.append(vehicle)

        vehicle_data = {
            "vehicle_number": vehicle.vehicle_number,
            "vehicle_type": vehicle.vehicle_type,
            "slot": vehicle.slot,
            "entry_time": vehicle.entry_time.isoformat()
        }

        data = load_data()
        data.append(vehicle_data)
        save_data(data)

        return available_slot

    def find_vehicle(self, vehicle_number):
        for vehicle in self.parked_vehicles:
            if vehicle.vehicle_number == vehicle_number:
                return vehicle

        return None

    def exit_vehicle(self, vehicle_number):

        vehicle = self.find_vehicle(vehicle_number)

        if vehicle is None:
            return None

        vehicle.exit_time = datetime.now()

        duration = vehicle.exit_time - vehicle.entry_time

        hours = ceil(duration.total_seconds() / 3600)
        fee = hours * 20

        history_data = {
            "vehicle_number": vehicle.vehicle_number,
            "vehicle_type": vehicle.vehicle_type,
            "slot": vehicle.slot,
            "entry_time": vehicle.entry_time.isoformat(),
            "exit_time": vehicle.exit_time.isoformat(),
            "duration": str(duration),
            "fee": fee
        }

        history = load_history()
        history.append(history_data)
        save_history(history)

        for slot in self.slots:
            if slot.slot_number == vehicle.slot:
                slot.is_occupied = False

        self.parked_vehicles.remove(vehicle)

        data = load_data()

        data = [
            record
            for record in data
            if record["vehicle_number"] != vehicle_number
        ]

        save_data(data)

        return vehicle, duration, fee