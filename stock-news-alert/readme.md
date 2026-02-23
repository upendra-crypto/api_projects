# 📈 Stock News Alert System

A Python automation project that monitors stock price changes and sends real-time news alerts via SMS.

## 🚀 Features

* Fetches daily stock data using Alpha Vantage API
* Calculates percentage price change between last two trading days
* Retrieves latest news related to the company using NewsAPI
* Sends SMS alerts with headlines and summaries via Twilio
* Automatically highlights stock movement direction (🔺 / 🔻)

## 🛠 Technologies Used

* Python
* Requests library
* Alpha Vantage API
* NewsAPI
* Twilio API

## 📂 Project Workflow

1. Fetch stock price data from Alpha Vantage
2. Compare closing prices of last two days
3. If price change exceeds threshold, fetch related news
4. Format headlines and summaries
5. Send alerts as SMS to the user

## 🔑 Setup Instructions

### 1️⃣ Clone the repository

```
git clone <your-repo-link>
cd stock-news-alert
```

### 2️⃣ Install dependencies

```
py -3.13 -m pip install requests twilio
```

### 3️⃣ Add your API keys

Edit `main.py` and insert:

* Alpha Vantage API key
* News API key
* Twilio SID & Auth Token

### 4️⃣ Run the program

```
python main.py
```

## 📩 Example SMS Output

```
TSLA: 🔺2.45%

Headline: Tesla launches new AI feature
Brief: Tesla announced a new AI-based driving system...

```

## 📌 Future Improvements

* Email notifications
* Telegram/WhatsApp alerts
* Automatic daily scheduling
* GUI dashboard
* Historical data storage

## 🎯 Purpose of the Project

This project demonstrates:

* API integration
* Data processing
* Automation logic
* Real-world alert system implementation

Suitable for beginner-to-intermediate Python developers and automation enthusiasts.


