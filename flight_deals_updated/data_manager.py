import os
import requests
from dotenv import load_dotenv

load_dotenv()


class DataManager:

    def __init__(self):
        self.endpoint = os.environ["SHEETY_ENDPOINT"]
        self.auth = (
            os.environ["SHEETY_USERNAME"],
            os.environ["SHEETY_PASSWORD"]
        )
        self.customer_data={}
    def get_destination_data(self):
        response = requests.get(self.endpoint, auth=self.auth)
        return response.json()["prices"]

    def update_destination_codes(self, data):
        for row in data:
            new_data = {
                "price": {
                    "iataCode": row["iataCode"]
                }
            }

            requests.put(
                url=f"{self.endpoint}/{row['id']}",
                json=new_data,
                auth=self.auth
            )
    def get_customer_details(self):
        sheety_users_endpoint="https://api.sheety.co/9c99992dd7a8571d72ff7747811b68ba/flightDeals/users"
        response=requests.get(url=sheety_users_endpoint,auth=self.auth)
        data=response.json()
        self.customer_data=data["users"]
        return self.customer_data
