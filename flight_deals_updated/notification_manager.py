import smtplib
from dotenv import load_dotenv
load_dotenv()
import os

class NotificationManager:
    def __init__(self):
        self.my_email=os.environ["MY_EMAIL"]
        self.my_password=os.environ["MY_PASSWORD"]

    def notification(self, price, origin, destination, from_date, to_date, emails):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(self.my_email, self.my_password)

            for email in emails:
                message = f"""Subject:✈️ Low Price Flight Alert!

                               Low price flight found!

                               From: {origin}
                               To: {destination}
                               Price: £{price}
                               Departure: {from_date}
                               Return: {to_date}
                                """

                connection.sendmail(
                    from_addr=self.my_email,
                    to_addrs=email,
                    msg=message.encode("utf-8")
                )

        print("EMAIL SENT SUCCESSFULLY")