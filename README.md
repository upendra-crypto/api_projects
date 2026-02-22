# 🌦️ Rain Alert SMS Notifier

This project checks the weather forecast using the OpenWeatherMap API and sends an SMS alert via Twilio if rain is predicted.

It includes two Python scripts:

* **Local version** (for testing on your computer)
* **Deployment version** (for cloud hosting like PythonAnywhere)

---

## 📌 Features

* Fetches weather forecast data from OpenWeatherMap
* Detects rain conditions automatically
* Sends SMS notification using Twilio
* Supports secure deployment with environment variables

---

## 📂 Project Files

### 1️⃣ `openweathermap_twilio.py`

* Designed for **local execution**
* API keys stored directly in the script
* Good for learning and testing

### 2️⃣ `python_anywhere.py`

* Designed for **deployment**
* Uses environment variables for security
* Includes proxy configuration for cloud platforms

---

## ⚙️ Requirements

Install dependencies:

```bash
pip install requests twilio
```

---

## 🔑 Setup

### 1. Get API keys

* Create an account at **OpenWeatherMap**
* Create an account at **Twilio**
* Get:

  * OpenWeatherMap API key
  * Twilio Account SID
  * Twilio Auth Token
  * Twilio phone number

---

### 2. Run Locally

Edit the file and add your keys:

```python
api_key = "YOUR_KEY"
account_sid = "YOUR_SID"
auth_token = "YOUR_TOKEN"
```

Run:

```bash
python openweathermap_twilio.py
```

---

### 3. Run on PythonAnywhere / Server

Set environment variables:

```bash
export OWM_API_KEY="your_key"
export AUTH_TOKEN="your_token"
export https_proxy="your_proxy"
```

Then run:

```bash
python python_anywhere.py
```

---

## 📲 Example SMS

```
It's going to rain today. Remember to bring an ☔️
```

---

## 🎯 Purpose of the Project

This project demonstrates:

* API integration in Python
* JSON data handling
* Automation scripts
* SMS notification systems
* Secure deployment practices

---

## 👨‍💻 Author

Created by **Upendra** as part of learning API integration and automation in Python.

---

## ⭐ Future Improvements

* Add email alerts
* Add GUI dashboard
* Support multiple cities
* Deploy as a scheduled cloud job

---

If you like this project, consider starring the repository ⭐
