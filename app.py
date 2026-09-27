import streamlit as st
from datetime import datetime

from parking import (
    ParkingSlot,
    ParkingLot,
    load_history,
    format_duration
)

from vehicle import Vehicle


lot = ParkingLot()

slot1 = ParkingSlot("A01")
slot2 = ParkingSlot("A02")
slot3 = ParkingSlot("A03")

lot.add_slot(slot1)
lot.add_slot(slot2)
lot.add_slot(slot3)


st.title("Parking Management System")
st.write("Welcome to the Parking Management System")


menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Park Vehicle",
        "Exit Vehicle",
        "Available Slots",
        "Parked Vehicles",
        "Parking History"
    ]
)


# Dashboard
if menu == "Dashboard":

    st.header("Dashboard")

    total_slots = len(lot.slots)

    occupied_slots = 0

    for slot in lot.slots:
        if slot.is_occupied:
            occupied_slots += 1

    available_slots = total_slots - occupied_slots

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Slots", total_slots)

    with col2:
        st.metric("Occupied Slots", occupied_slots)

    with col3:
        st.metric("Available Slots", available_slots)


# Park Vehicle
elif menu == "Park Vehicle":

    st.header("Park Vehicle")

    vehicle_number = st.text_input("Vehicle Number")

    vehicle_type = st.selectbox(
        "Vehicle Type",
        ["Car", "Bike", "Truck"]
    )

    if st.button("Park Vehicle"):

        if vehicle_number.strip() == "":
            st.error("Please enter a vehicle number")

        elif lot.find_vehicle(vehicle_number) is not None:
            st.error("Vehicle is already parked")

        else:
            vehicle = Vehicle(vehicle_number, vehicle_type)

            assigned_slot = lot.park_vehicle(vehicle)

            if assigned_slot is not None:
                st.success(
                    f"Vehicle parked successfully in slot "
                    f"{assigned_slot.slot_number}"
                )
            else:
                st.error("No parking space available")


# Exit Vehicle
elif menu == "Exit Vehicle":

    st.header("Exit Vehicle")

    vehicle_number = st.text_input("Vehicle Number")

    if st.button("Exit Vehicle"):

        result = lot.exit_vehicle(vehicle_number)

        if result is not None:

            vehicle, duration, fee = result

            st.success("Vehicle exited successfully")

            st.subheader("Parking Bill")

            st.write(
                "**Vehicle Number:**",
                vehicle.vehicle_number
            )

            st.write(
                "**Vehicle Type:**",
                vehicle.vehicle_type
            )

            st.write(
                "**Parking Slot:**",
                vehicle.slot
            )

            st.write(
                "**Entry:**",
                vehicle.entry_time.strftime(
                    "%d %b %Y, %I:%M %p"
                )
            )

            st.write(
                "**Exit:**",
                vehicle.exit_time.strftime(
                    "%d %b %Y, %I:%M %p"
                )
            )

            st.write(
                "**Duration:**",
                format_duration(duration)
            )

            st.write(
                "### Parking Fee: ₹",
                fee
            )

        else:
            st.error("Vehicle not found")


# Available Slots
elif menu == "Available Slots":

    st.header("Parking Slots")

    for slot in lot.slots:

        if slot.is_occupied:
            st.error(f"{slot.slot_number} - Occupied")
        else:
            st.success(f"{slot.slot_number} - Available")


# Parked Vehicles
elif menu == "Parked Vehicles":

    st.header("Currently Parked Vehicles")

    parked_data = []

    for vehicle in lot.parked_vehicles:

        parked_data.append({
            "Vehicle Number": vehicle.vehicle_number,
            "Vehicle Type": vehicle.vehicle_type,
            "Parking Slot": vehicle.slot,
            "Entry Time": vehicle.entry_time.strftime(
                "%d %b %Y, %I:%M %p"
            )
        })

    if parked_data:
        st.dataframe(
            parked_data,
            use_container_width=True
        )
    else:
        st.info("No vehicles are currently parked.")


# Parking History
elif menu == "Parking History":

    st.header("Parking History")

    history = load_history()

    history_data = []

    for record in history:

        entry_time = datetime.fromisoformat(
            record["entry_time"]
        )

        exit_time = datetime.fromisoformat(
            record["exit_time"]
        )

        duration = exit_time - entry_time

        history_data.append({
            "Vehicle Number": record["vehicle_number"],
            "Vehicle Type": record["vehicle_type"],
            "Parking Slot": record["slot"],
            "Entry": entry_time.strftime(
                "%d %b %Y, %I:%M %p"
            ),
            "Exit": exit_time.strftime(
                "%d %b %Y, %I:%M %p"
            ),
            "Duration": format_duration(duration),
            "Parking Fee": f"₹{record['fee']}"
        })

    if history_data:
        st.dataframe(
            history_data,
            use_container_width=True
        )
    else:
        st.info("No parking history available.")