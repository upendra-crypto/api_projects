import streamlit as st
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("PIXELA_TOKEN")
USERNAME = os.getenv("PIXELA_USERNAME")
GRAPH_ID = os.getenv("GRAPH_ID")

PIXELA_URL = "https://pixe.la/v1/users"

headers = {
    "X-USER-TOKEN": TOKEN
}

pixel_endpoint = f"{PIXELA_URL}/{USERNAME}/graphs/{GRAPH_ID}"

st.title("📊 Habit Tracker")

st.write("Track your daily habits easily!")

quantity = st.text_input("Enter today's progress")

today = datetime.now().strftime("%Y%m%d")

col1, col2, col3 = st.columns(3)

# ADD PIXEL
with col1:
    if st.button("Add Entry"):
        pixel_config = {
            "date": today,
            "quantity": quantity
        }
        res = requests.post(pixel_endpoint, json=pixel_config, headers=headers)
        st.success(res.text)

# UPDATE PIXEL
with col2:
    if st.button("Update Entry"):
        update_endpoint = f"{pixel_endpoint}/{today}"
        res = requests.put(update_endpoint, json={"quantity": quantity}, headers=headers)
        st.success(res.text)

# DELETE PIXEL
with col3:
    if st.button("Delete Entry"):
        delete_endpoint = f"{pixel_endpoint}/{today}"
        res = requests.delete(delete_endpoint, headers=headers)
        st.success(res.text)

st.markdown("---")

st.subheader("📈 View Your Graph")

graph_url = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}.html"
st.markdown(f"[Click here to view progress]({graph_url})")
