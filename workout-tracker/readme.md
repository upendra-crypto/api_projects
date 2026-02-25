# 🏋️ Workout Tracker (Python API Project)

## 📌 Project Overview

This project is a **Workout Tracking Application** built using Python that converts natural language exercise input into structured workout data.

It uses:

* 🧠 Natural Language Processing API (Nutritionix)
* 📊 Google Sheets API (via Sheety)
* 🔐 Environment variables for secure API handling

The app lets users type exercises in plain English (example: *“I ran 3 km and did 20 minutes yoga”*) and automatically logs:

* Date
* Time
* Exercise name
* Duration
* Calories burned

into a connected Google Sheet.

---

## 🚀 Features

* Accepts natural language workout input
* Calculates calories burned using Nutritionix API
* Automatically logs workouts to Google Sheets
* Uses environment variables for security
* Demonstrates API authentication methods

---

## 🛠️ Technologies Used

* Python
* Requests library
* Nutritionix API
* Sheety API
* Google Sheets
* Environment Variables

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/upendra-crypto/workout-tracker.git
cd workout-tracker
```

### 2️⃣ Install dependencies

```bash
pip install requests
```

### 3️⃣ Set Environment Variables

Create environment variables for:

* Nutritionix APP ID
* Nutritionix API KEY
* Sheety Endpoint
* Sheety Username / Password or Token

In PyCharm:

```
Run → Edit Configurations → Environment Variables
```

Paste your variables in this format:

```
ENV_NIX_APP_ID=your_id
ENV_NIX_API_KEY=your_key
ENV_SHEETY_ENDPOINT=your_endpoint
ENV_SHEETY_USERNAME=your_username
ENV_SHEETY_PASSWORD=your_password
```

---

### 4️⃣ Run the project

```bash
python main.py
```

Enter your workout in plain English and the data will be logged automatically.

---

## 📊 Example Input

```
Tell me which exercises you did: I ran 2 km and cycled for 15 minutes
```

Output:

* Logs exercises to Google Sheet with calories burned

---

## 📁 Project Structure

```
main.py              → Main application logic
env_for_pycharm.txt  → Example environment variables
README.md            → Project documentation
```

---

## 🔒 Security Note

Never upload real API keys to GitHub.
Always use environment variables or `.env` files excluded via `.gitignore`.

---

