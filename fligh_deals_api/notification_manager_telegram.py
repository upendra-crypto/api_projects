from dotenv import load_dotenv
load_dotenv()

import os
import requests

class NotificationManager:

    def __init__(self):
        self.token = os.environ["TELEGRAM_TOKEN"]
        self.chat_id = os.environ["TELEGRAM_CHAT_ID"]

    def notification(self, price, origin, destination, from_date, to_date):

        message = (
            f"✈️ Low Price Alert!\n\n"
            f"From: {origin}\n"
            f"To: {destination}\n"
            f"Price: £{price}\n"
            f"Departure: {from_date}\n"
            f"Return: {to_date}"
        )

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        requests.post(url, json={
            "chat_id": self.chat_id,
            "text": message
        })
