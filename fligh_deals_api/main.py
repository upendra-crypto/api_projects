from datetime import datetime, timedelta
import time

from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import find_cheapest_flight
from notification_manager import *
# Setup
flight_search = FlightSearch()
data_manager = DataManager()
notification=NotificationManager()#if you wants telegram add notification manager form notification_manager_telegram.py
ORIGIN_CITY = "LON"

# Get sheet data
sheet_data = data_manager.get_destination_data()

# Fill missing IATA codes
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        time.sleep(2)

data_manager.update_destination_codes(sheet_data)

# Date range
tomorrow = datetime.now() + timedelta(days=1)
six_months = datetime.now() + timedelta(days=6*30)

# Search flights
for row in sheet_data:
    print(f"Searching flights to {row['city']}...")

    flights = flight_search.search_flights(
        ORIGIN_CITY,
        row["iataCode"],
        tomorrow,
        six_months
    )

    cheapest = find_cheapest_flight(flights)

    print(f"{row['city']}: £{cheapest.price}")
    if cheapest.price != "N/A" and row["lowestPrice"] > cheapest.price:
        notification.notification(
            cheapest.price,
            origin=ORIGIN_CITY,
            destination=row['city'],
            from_date=cheapest.out_date,
            to_date=cheapest.return_date
        )
    time.sleep(2)
