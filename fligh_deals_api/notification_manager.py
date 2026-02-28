from dotenv import load_dotenv
load_dotenv()
import os
from twilio.rest import Client
class NotificationManager:
    def __init__(self):
        self.account_sid = os.environ["TWILIO_ACC_SID"]
        self.auth_token = os.environ["TWILIO_ACC_AUTH_TOKEN"]
        self.num=os.environ["TWILIO_PHONENO"]
        self.to_num=os.environ["MY_NUMBER"]
    def notification(self,price,origin,destination,from_date,to_date):
        client = Client(self.account_sid, self.auth_token)

        client.messages.create(
            body=f"Low Price alert! price:{price},{origin},{destination},{from_date},{to_date}",
            from_=self.num,
            to=self.to_num,
        )
