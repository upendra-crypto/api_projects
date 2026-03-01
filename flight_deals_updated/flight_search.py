from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
import os
import requests


class FlightSearch:

    def __init__(self):
        self.api_key = os.environ["AMADEUS_APIKEY"]
        self.api_secret = os.environ["AMADEUS_SECRET"]
        self.token = self.get_new_token()

    def get_new_token(self):

        response = requests.post(
            url="https://test.api.amadeus.com/v1/security/oauth2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.api_secret,
            }
        )


        data = response.json()

        if "access_token" not in data:
            raise Exception(f"Failed to get token: {data}")

        return data["access_token"]

    def get_destination_code(self, city):

        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(
            url="https://test.api.amadeus.com/v1/reference-data/locations/cities",
            headers=headers,
            params={"keyword": city, "max": 2, "include": "AIRPORTS"}
        )

        try:
            return response.json()["data"][0]["iataCode"]
        except:
            return "N/A"

    def check_flights(self, origin, destination, from_time, to_time,is_direct=True):

        headers = {"Authorization": f"Bearer {self.token}"}

        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop":"true" if is_direct else "false",
            "currencyCode": "GBP",
            "max": 10,
        }

        response = requests.get(
            url="https://test.api.amadeus.com/v2/shopping/flight-offers",
            headers=headers,
            params=params
        )

        if response.status_code != 200:
            return None

        return response.json()
