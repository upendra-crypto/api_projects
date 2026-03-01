# ✈️ Flight Deals Tracker

A Python flight price monitor that searches for cheap flights via the **Amadeus API**, manages destinations through **Google Sheets (Sheety)**, and automatically emails subscribers when fares drop below a set threshold. Runs locally — no cloud deployment required.

---

## 🖥️ How to Run

### GUI — Streamlit Dashboard *(recommended)*
Interactive dashboard with date pickers, live activity log, and visual results:
```bash
streamlit run app.py
```
Opens at `http://localhost:8501` in your browser.

> ⚠️ Uses the Amadeus **free test API** — results may be limited and searches may take longer than usual.
> GUI-OUTPUT:
> <img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/b2d7e34c-3516-456d-a184-ce0a91567426" />


### CLI — Headless Script
One-shot search, ideal for automation or cron jobs:
```bash
python main.py
```

---

## 📁 Project Structure

```
├── app.py                  # Streamlit GUI dashboard
├── main.py                 # CLI entry point
├── flight_search.py        # Amadeus API — auth & flight queries
├── flight_data.py          # FlightData model & cheapest fare logic
├── data_manager.py         # Sheety API — destinations & customer data
├── notification_manager.py # Gmail SMTP — deal alert emails
└── .env                    # Credentials (never commit this)
```

---

## ⚙️ Setup

### 1. Install Dependencies
```bash
pip install requests python-dotenv streamlit pandas
```

### 2. Configure Environment Variables
Create a `.env` file in the project root:
```env
AMADEUS_APIKEY=your_amadeus_api_key
AMADEUS_SECRET=your_amadeus_api_secret

SHEETY_ENDPOINT=https://api.sheety.co/your_endpoint/flightDeals/prices
SHEETY_USERNAME=your_sheety_username
SHEETY_PASSWORD=your_sheety_password

MY_EMAIL=your_gmail_address
MY_PASSWORD=your_gmail_app_password
```

> **Gmail:** Use an [App Password](https://myaccount.google.com/apppasswords), not your regular password. Requires 2FA to be enabled.

### 3. Set Up Your Google Sheet
Connect a Google Sheet via [Sheety](https://sheety.co) with the following columns:

| city | iataCode | lowestPrice |
|------|----------|-------------|
| Paris |  | 100 |
| Tokyo |  | 300 |

Leave `iataCode` blank — it is auto-filled on first run.

A second sheet named **users** should contain subscriber details:

| whatIsYourFirstName? | whatIsYourLastName? | whatIsYourEmail? |
|----------------------|---------------------|-----------------|
| John | Doe | john@example.com |

---

## 🔑 Required API Keys

| Service | Purpose | Link |
|---------|---------|------|
| Amadeus | Flight search | [developers.amadeus.com](https://developers.amadeus.com) |
| Sheety | Google Sheets as REST API | [sheety.co](https://sheety.co) |
| Gmail | Email alerts | [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) |

---

## ✨ Features

- **Smart flight search** — checks direct flights first, automatically falls back to indirect if none found
- **Threshold-based alerts** — emails all subscribers only when a fare beats the sheet price
- **Auto IATA resolution** — looks up missing airport codes by city name on first run
- **Fully local** — runs on your machine, no cloud or server needed
- **Dual interface** — GUI via `app.py` (custom origin, dates, email toggle) or CLI via `main.py`
- **Live activity log** — real-time per-route search status in the dashboard

---

## ⚠️ Important Notes

- The Amadeus **test environment** has limited route coverage. For full results, upgrade to a production key at [developers.amadeus.com](https://developers.amadeus.com).
- `main.py` defaults to origin `LON` and a 6-month search window — edit these constants directly in the file if needed.
- `app.py` lets you change origin, departure date, and return date from the sidebar without touching any code.


---

## ☁️ Optional Cloud Deployment

The app runs perfectly on localhost. Deploy only if you need remote access or 24/7 uptime:

| Platform | Notes |
|----------|-------|
| **Streamlit Community Cloud** | Free, connects to GitHub repo directly |
| **Railway / Render** | Simple setup, free tier available |
| **PythonAnywhere** | Good for scheduling `main.py` as a cron job |

