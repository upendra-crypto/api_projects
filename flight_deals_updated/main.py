from datetime import datetime, timedelta
import time

from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager


def run_search(origin, depart_date, return_date, send_emails=True, logs=None):
    """Core engine used by dashboard or CLI"""

    def log(msg):
        if logs is not None:
            logs.append(msg)

    fs = FlightSearch()
    dm = DataManager()
    nm = NotificationManager() if send_emails else None

    log("Token obtained")

    sheet = dm.get_destination_data()
    customers = dm.get_customer_details()
    email_list = [r.get("whatIsYourEmail?", "") for r in customers]

    # Fill missing IATA codes
    for row in sheet:
        if row.get("iataCode", "") == "":
            row["iataCode"] = fs.get_destination_code(row["city"])
            time.sleep(1)
    dm.update_destination_codes(sheet)

    results = []

    for row in sheet:
        city = row["city"]
        iata = row["iataCode"]
        log(f"Searching {city}")

        flights = fs.check_flights(origin, iata, depart_date, return_date, True)
        cheapest = find_cheapest_flight(flights)

        if cheapest.price == "N/A":
            flights = fs.check_flights(origin, iata, depart_date, return_date, False)
            cheapest = find_cheapest_flight(flights)

        # duration calc
        if cheapest.out_date != "N/A":
            d1 = datetime.strptime(cheapest.out_date, "%Y-%m-%d")
            d2 = datetime.strptime(cheapest.return_date, "%Y-%m-%d")
            duration = (d2 - d1).days
        else:
            duration = "N/A"

        is_deal = (
            cheapest.price != "N/A"
            and float(row.get("lowestPrice", 99999)) > float(cheapest.price)
        )

        results.append({
            "city": city,
            "iata": iata,
            "price": cheapest.price,
            "out_date": cheapest.out_date,
            "return_date": cheapest.return_date,
            "duration": duration,
            "threshold": row.get("lowestPrice", "N/A"),
            "stops": cheapest.stops,
            "is_deal": is_deal,
        })

        if is_deal and nm:
            nm.notification(
                price=cheapest.price,
                origin=origin,
                destination=city,
                from_date=cheapest.out_date,
                to_date=cheapest.return_date,
                emails=email_list,
            )

    return results, customers
