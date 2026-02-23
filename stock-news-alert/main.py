import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY="YOUR STOCK API KEY"
NEWS_API_KEY="YOUR NEWS API KEY"
TWILIO_SID="YOUR TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN="YOUR TWILIO ACCOUNT AUTH TOKEN"

parameters={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY
}
news_params={
    "qInTitle":COMPANY_NAME,
    "apiKey":NEWS_API_KEY
}
response=requests.get(STOCK_ENDPOINT,params=parameters)
data=response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in data.items()]
yesterday_data=data_list[0]
yesterday_closing_price=float(yesterday_data["4. close"])

day_before_yesterday_data=data_list[1]
day_before_yesterday_price=float(day_before_yesterday_data["4. close"])

diff=(yesterday_closing_price-day_before_yesterday_price)

diff_percent=(diff/yesterday_closing_price)*100

if abs(diff_percent) >0.02:
    news_response=requests.get(NEWS_ENDPOINT,params=news_params)
    articles=news_response.json()["articles"]

three_articles=articles[:3]

# Determine stock movement arrow
if yesterday_closing_price > day_before_yesterday_price:
    arrow = "🔺"
else:
    arrow = "🔻"

# Format articles properly
formatted_article_list = [
    f"""{STOCK_NAME}: {arrow}{round(diff_percent,2)}%

Headline: {article['title']}
Brief: {article['description'] or "No description available"}
"""
    for article in three_articles
]


client=Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
for article in formatted_article_list:
    message = client.messages.create(body=article,from_="YOUR TWILIO DEFAULT NUMBER",to="YOUR PHONE NUMBER")



